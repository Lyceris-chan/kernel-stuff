# swap stack: zswap + xswap

This machine swaps into compressed RAM instead of a zram block device. The
kernel side is `CONFIG_XSWAP` plus patches `2155`–`2166`; the userspace side is
the two files in this directory.

## Why not zram

zram creates a block device with a fixed size (here 30.9 GB, `zram-size = ram`)
and never returns that memory when the workload shrinks. An xswap device has no
backing store at all: swapped pages live in zswap's compressed pool, the
`cluster_info[]` array is mapped lazily out of a sparse vmalloc area, and the
device grows and shrinks with use. An idle device costs nothing.

Two properties matter for this machine:

- `xswap/create` refuses to create a device unless zswap is enabled
  (`-EOPNOTSUPP`), so zswap is a hard requirement, not an optimization.
- The device appears in `/proc/swaps` as `xswap<N>` and takes a priority, like
  any other swap device. This setup gives it `100`, which is what zram used.

## Install

```bash
sudo install -Dm644 xswap-create.service /etc/systemd/system/xswap-create.service
sudo install -Dm644 99-xswap-swappiness.conf /etc/sysctl.d/99-xswap-swappiness.conf
sudo systemctl daemon-reload
sudo systemctl enable xswap-create.service

# Turn zram off. An empty config means "create no devices".
sudo ln -sf /dev/null /etc/systemd/zram-generator.conf

# The zram udev rule forces zswap/enabled to N whenever a zram device appears,
# which would make xswap/create fail. Mask it.
sudo ln -sf /dev/null /etc/udev/rules.d/30-zram.rules
```

Then enable zswap at boot. `CONFIG_ZSWAP_DEFAULT_ON=y` is set, so removing the
disable is enough:

```bash
sudo sed -i 's/^LINUX_OPTIONS="zswap.enabled=0 /LINUX_OPTIONS="/' /etc/sdboot-manage.conf
sudo sdboot-manage gen
```

The action of record is `xswap-create.service`: it writes `100` to
`/sys/kernel/mm/xswap/create` once per boot, guarded so a second start does not
create a second device.

## Verify after a reboot

```bash
cat /sys/module/zswap/parameters/enabled     # Y
cat /sys/module/zswap/parameters/compressor  # zstd
swapon --show                                # one xswap device, priority 100
grep -c zram /proc/swaps                     # 0
```

## Other kernels on this machine

Only kernels built with `CONFIG_XSWAP` get a swap device from this setup —
this package, and anything built from the same series. The stock
`linux-cachyos-rc` and `linux-cachyos-lts` kernels do not have it, and since
zram is masked system-wide they boot with **no swap at all**. zswap does not
help there: it is a compressed cache in front of a swap device, not a swap
device itself. `xswap-create.service` skips cleanly on those kernels
(`ConditionPathExists`), it just leaves them without swap. Bring zram back for
a comparison boot by removing the two mask symlinks, or add a disk swap file.

## Known cosmetic artifacts

Two things look like faults and are not. Both follow from an xswap device having
no backing store, and therefore no device node.

- **`xswap0.swap` reports `Loaded: error`.** systemd builds a swap unit from each
  entry in `/proc/swaps` and expects to map that entry to a device; `xswap0` has
  no `/dev/xswap0` to map, so the unit fails to load with `InvalidArgs` while
  still showing `active`:

  ```
  ● xswap0.swap - xswap0
       Loaded: error (Reason: Unit xswap0.swap failed to load properly: Invalid argument)
       Active: active since ...
         What: xswap0
  ```

  It costs nothing: `swap.target` is reached, the device is live, and the
  shutdown path logs no swap errors. `udisksd` makes the same lookup and logs
  `Error statting xswap0: No such file or directory` three times per boot for
  the same reason.

  **The precise mechanism**, so this is not re-investigated: `swap_verify()`
  (`src/core/swap.c`) re-derives the unit name from the swap's `What=` with
  `unit_name_from_path(s->what, ".swap")` and requires it to match the unit's own
  name. An xswap device has no `swap_file`, so the kernel prints a synthetic bare
  name in `/proc/swaps` — `xswap0` — which is not an absolute path, and
  `unit_name_from_path()` cannot derive a name from it. It can never round-trip.

  **It cannot be silenced from userspace, and that was tested rather than
  assumed.** Masking the unit (`ln -sf /dev/null /etc/systemd/system/xswap0.swap`)
  leaves it in `error`, because systemd rebuilds the unit from `/proc/swaps`
  regardless; a drop-in supplying `[Swap] What=/xswap0` is ignored; and
  `daemon-reload` never re-runs the verification on an already-loaded unit. A
  kernel-side change is worse than the disease: the only path that keeps the unit
  named `xswap0.swap` — and therefore passes the name check — is `/xswap0`, and a
  swap unit that loads is stopped by spawning `swapoff "$what"` (`swap.c`,
  "Failed to spawn 'swapoff' task"), which can never succeed for a file-less
  swap. That trades a cosmetic load error for a cosmetic shutdown failure.

  As it stands `systemctl --failed` is empty, the device is live, nothing about it
  is logged at boot, and shutdown is clean — it is visible only if you go looking
  at swap units specifically. The real fix belongs upstream: either the series
  registers a name systemd can consume, or systemd stops requiring a
  round-trippable path for a swap it discovered from `/proc/swaps` itself.

- **Hibernation is impossible.** `disk` is listed in `/sys/power/state`, but the
  image has to be written to a swap device that survives power-off, and an xswap
  device lives entirely in zswap's compressed RAM pool. Nothing regressed here:
  this machine configures no hibernation either way (there is no `resume=` on
  the kernel command line), so adding it would need a disk swap file or
  partition alongside this stack. Suspend-to-RAM
  (`mem_sleep_default=deep`) is what this setup is for.

## Tune

`/sys/kernel/mm/xswap/type<N>/limit` caps a device, in pages. Grow and shrink
both work without it, and the default ceiling is 1xRAM.

`/sys/module/zswap/parameters/max_pool_percent` (default 20) is the real memory
ceiling: with no disk swap behind it, the compressed pool *is* the swap
capacity, so the pool cap times the compression ratio is how much can be
swapped. Raise it only if you see swap allocation failures.

## Revert to zram

```bash
sudo rm /etc/systemd/zram-generator.conf /etc/udev/rules.d/30-zram.rules
sudo systemctl disable xswap-create.service
sudo rm /etc/systemd/system/xswap-create.service /etc/sysctl.d/99-xswap-swappiness.conf
sudo sed -i 's/^LINUX_OPTIONS="/LINUX_OPTIONS="zswap.enabled=0 /' /etc/sdboot-manage.conf
sudo sdboot-manage gen
```

The masked udev rule set `vm.swappiness=150`; the sysctl drop-in keeps that
value once the rule is gone. Revert it too if you go back to zram.
