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
`/sys/kernel/mm/xswap/create` once per boot.

**The guard is load-bearing, because the kernel does not deduplicate.** Writing
a priority to `create` always makes a new device — two writes of `100` give two
devices at priority 100 (verified on the live kernel: it produced `xswap0` and
`xswap1`, both at priority 100). The unit's guard therefore matches a device at
priority 100 *specifically*, not "any xswap device": the coarse `grep -q ^xswap`
form is satisfied by a stray device at any other priority, so the configured one
would never be created and the machine would boot without the swap it expects.
Both directions were tested — no duplicate when a priority-100 device exists,
and a priority-100 device is created when only a stray one is present.

Multiple devices are supported. Each `create` takes the next free type and
appears as `xswap<N>` in `/proc/swaps`; `destroy` takes the type to remove; an
out-of-range or non-numeric type is rejected with `EINVAL`. A destroy/recreate
cycle reuses the lowest free type, so it gives `xswap0` back.

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

## Verified on the live kernel (2026-09-16, 7.3.0-rc3-16)

Beyond "it shows up in `swapon --show`", the stack was driven under real load:

- **A forced swap cycle.** 1.25 GiB of touched anonymous memory inside a cgroup
  capped at 384 MiB pushed `stored_pages` from 3,578 to 443,398 and the pool to
  501 MB holding 2.15 GiB logical — 4.4x — with `pool_limit_hit` still 0.
- **Round-trip integrity.** 262,144 pages (1 GiB) written with a per-page
  pattern, forced out to swap, then read back: **zero mismatches**, and
  `decompress_fail` stayed 0 throughout.
- **The pool shrinks again.** 15 s after the pressure ended the pool was already
  draining (443k → 384k pages) and it kept draining. It does this via
  `zswap_invalidate` as swap slots are freed, not via writeback —
  `written_back_pages` is 0, correctly, since there is no backing store.
- **No leak in the grow/shrink path.** Five full create → allocate → free →
  destroy cycles left `MemAvailable` flat (27.76, 27.96, 27.87, 28.07, 28.04 GB
  across the five). A leaking `cluster_info[]` would have shown a steady
  per-cycle decline.
- **Every error counter stayed at zero**: `reject_alloc_fail`,
  `reject_compress_fail`, `reject_compress_poor`, `reject_kmemcache_fail`,
  `reject_reclaim_fail`, `decompress_fail`, `pool_limit_hit`,
  `written_back_pages`, `stored_incompressible_pages`.

`/sys/kernel/mm/xswap/{create,destroy}` are root-write-only (`--w-------`) and
`type<N>/limit` is `0644`. The device is created at its ceiling (`si->pages`,
1xRAM = 8,107,519 pages here) and memory is allocated lazily per cluster, so a
nominally 30 GiB device costs nothing while idle.

## Code audit of the series (2026-09-16)

Patches `2155`–`2166` were read end to end against a reconstructed post-series
tree. **No reachable lifetime, locking, use-after-free, double-free, or
accounting defect was found in the xswap paths.** The concerns worth naming:

- `destroy_swap_extents(si, NULL)` is **safe** — the argument is used only inside
  `if (sis->flags & SWP_ACTIVATED)`, and `SWP_ACTIVATED` is set only by
  `setup_swap_extents()`, which only `SYSCALL_DEFINE2(swapon)` calls.
  `xswap_create` never reaches it.
- `free_swap_cluster_info()` returning early on the xswap branch is **correct**:
  for xswap, `cluster_info` is the vmalloc area address, so falling through to
  `kvfree()` is the bug it avoids.
- `swapoff`'s `p->swap_file &&` guard is **load-bearing** — an active xswap
  device has `SWP_WRITEOK` set and `swap_file == NULL`, so `swapoff <anything>`
  would NULL-deref without it.
- Growth and shrink invariants around the lazily-mapped `cluster_info[]` hold,
  including the alignment that makes a growth chunk (85 clusters × 48 B = 4080 B
  here) straddle at most two pages, so the live cluster just below a shrink
  boundary always stays inside a still-mapped page.
- Locking is sound: grow and unmap are serialized by `si->xswap_lock`; the
  shrink's `spin_trylock(&ci->lock)` under `si->lock` is what avoids an ABBA
  against `move_cluster()`'s `ci->lock → si->lock` order; RCU pairs completely
  (`rcu_read_lock()` in the allocators against
  `flush_percpu_swap_cluster()` + `synchronize_rcu()` before every unmap).

Three things are genuinely dead or soft. **All three are zero-impact on this
machine**, recorded so they are not rediscovered:

1. **`nr_real_swapfiles` is not exported** while `mm/zswap.c` reads it without a
   `CONFIG_XSWAP` guard. Confirmed live: `/proc/kallsyms` has the symbol but no
   `__ksymtab_nr_real_swapfiles`, where its neighbour `nr_swap_pages` has
   `__ksymtab_nr_swap_pages`. This breaks only a `CONFIG_ZSWAP=m` build
   (`modpost: "nr_real_swapfiles" [mm/zswap.ko] undefined!`); this kernel is
   `CONFIG_ZSWAP=y`, so it cannot bite here. **Worth reporting upstream** — it
   would block any distro that builds zswap as a module.
2. **The `-EBUSY` branch in the map path is unreachable**, and is wrong in the
   way a defensive branch must not be: `vmap_pte_range()` in this base
   `BUG()`s on a double map (`dump_page(page, "remapping already mapped page")`)
   and `return -EBUSY` appears nowhere in `mm/vmalloc.c`. Should a future base
   restore an `-EBUSY` return, the `fail_nounmap` path would free pages still
   referenced by live PTEs. Not reachable today — `si->xswap_lock` is the only
   serializer and the range is pre-scanned.
3. **`free_swap_cluster_info()` ignores `xswap_unmap_clusters()`'s `-ENOMEM`**,
   which can occur before anything is unmapped, so `free_vm_area()` would drop
   page tables without freeing data pages — up to ~744 KB on an OOM teardown
   only. It also returns before clearing `si->cluster_info`, leaving a pointer
   into a freed vmalloc area; today every caller clears it itself, so it is a
   latent trap rather than a live double-free.

None of the three justify carrying a local patch, since none can fire on a
`CONFIG_ZSWAP=y` build with no limit written.

## Tune

`/sys/kernel/mm/xswap/type<N>/limit` sets the device size in pages (1xRAM by
default). **It is a soft bound, not a hard cap**, and this README previously
overstated it. The field's own comment calls it a "growth ceiling", but the only
reader in the series is `xswap_try_shrink()` (`nr_ceiling = READ_ONCE(si->nr_clusters)`),
while the *grow* path is gated on `nr_clusters_max`, which is fixed when the
device is created. Writing a limit below current usage therefore makes the
shrinker unmap clusters the allocator immediately maps again, rather than
refusing the allocation. The store does clamp to the in-use count
(`new_pages < swap_usage_in_pages(si)`), so `si->pages` never drops below what is
actually stored and `SwapTotal`/`SwapFree` stay truthful. Nothing in this setup
writes it, so `nr_clusters == nr_clusters_max` and the whole branch is inert
here. Read it as "the size the shrinker trims back to", not as a quota.

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

The masked udev rule set `vm.swappiness=150`. The sysctl drop-in does **not**
keep that value: it sets **180**, with the reasoning in the file's comments.
Two independent sources put in-memory swap above 150 — the kernel's own
`Documentation/admin-guide/sysctl/vm.rst`, which defines swappiness as a
relative IO cost over 0-200 (100 = equal cost) and says "for in-memory swap,
like zram or zswap ... values beyond 100 can be considered", working out to 133
when swap is 2x faster than the filesystem; and the Arch Wiki's Zram article
("Optimizing swap on zram"), which recommends 180 together with
`watermark_boost_factor = 0`, `watermark_scale_factor = 125` and
`page-cluster = 0`. The other three of those are already set in
`/etc/sysctl.d/99-custom-tweaks.conf`, so 180 completes the set. This device has
no backing store at all, so its "IO" is a compress and decompress in RAM — well
past the 2x the kernel's example assumes.

The kernel documentation is explicit that this is not exact: "An optimal value
will require experimentation and will also be workload-dependent." Revert the
drop-in too if you go back to zram.
