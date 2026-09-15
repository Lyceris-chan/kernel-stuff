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

## Tune

`/sys/kernel/mm/xswap/type<N>/limit` caps a device, in pages. Grow and shrink
both work without it, and the default ceiling is 1xRAM.

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
