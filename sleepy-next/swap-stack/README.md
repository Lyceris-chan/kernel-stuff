# swap stack: zswap + swapfile

This machine swaps into a zswap pool held in RAM, backed by a swapfile on the
NVMe that the pool drains into when it fills.

- `setup-swapfile.sh` — creates `/swapfile` (16 GiB) and the fstab entry
- `99-zswap-swappiness.conf` -> `/etc/sysctl.d/`
- `marie-low-swappiness-mode.conf` -> `/etc/tmpfiles.d/`

No kernel patches are involved. zswap, the shrinker that drains it, and the
swapfile are all upstream, which is the point.

## The layout

```
anon page --swap--> zswap pool (RAM, zstd, capped at 20% of RAM = 6.4 GB)
                       |
                       |  shrinker, when the pool is under pressure
                       v
                    /swapfile (16 GiB, NVMe, priority 100)
```

`/proc/swaps` shows one device. The pool is not a device — it is a cache in
front of one, which is why it cannot be "used" on its own.

## Why zswap, and not zram or the xswap series

All three are compressed swap; the difference that decided it is **what
happens when the tier fills.**

- **zswap's drain works automatically.** The shrinker calls
  `zswap_writeback_entry()`, which writes back to *the entry's own swap
  device*:

  ```c
  si = get_swap_device(swpentry);
  if (!si)
          return -ENOENT;
  ```

  With a real swapfile behind it, that succeeds, the pool empties, and anon
  stays reclaimable. This is the whole reason a swapfile was created: zswap
  needs a device to drain to, and *any* real device will do — including a
  file.

- **zram's drain does not, ever.** It is never triggered by the kernel; it
  runs only on an explicit `echo <policy> > /sys/block/zramX/writeback`
  (`systemd/zram-generator#164`). Worse for this machine, `backing_dev`
  requires a **raw block device** — `backing_dev_store()` rejects anything
  that is not `S_ISBLK`, so a swapfile would not have worked and there is no
  spare partition. When zram fills it fails the write
  (`BLK_STS_IOERR`), and the documented failure mode is a very long stall:
  Matt Fleming's RFC *"mm: Reduce direct reclaim stalls with RAM-backed
  swap"* — *"Systems with zram-only swap can spin in direct reclaim for
  20-30 minutes without ever invoking the OOM killer"*, because free zram
  slots inflate the reclaimable estimate with nothing to back them.

- **The xswap series blocked its own drain by construction** (`2155` inserted
  an explicit `-EINVAL` for `SWP_XSWAP` into `zswap_writeback_entry()`, and
  gated the shrinker on `nr_real_swapfiles`, which is zero with no real
  device). It also advertised a capacity it could not hold. It was removed on
  2026-09-22 — see `../PATCH_SOURCES.md`. One piece of it survives as a
  standalone zswap fix: patch `2196`, which is carried.

This follows the upstream direction rather than fighting it: the xswap RFC
*"fall back to disk when zswap refuses an xswap page"* is the same idea —
RAM first, disk when it fills — and it is what the xswap series was missing.

### What upstream actually says, since it decided this

**Johannes Weiner (kernel MM), 2026-03-03**, in the RAM-backed-swap RFC thread:

> "What keeps users in the zram camp is **disk-less setups**. What keeps users
> in the zswap camp is reclaim-writeback, cgroup accounting & control, and the
> prospect of fully dynamic sizing. ... So I fully agree. **We should try to
> make zswap the single compressed swap implementation.**"

Adding the swapfile is what moves this machine out of the zram camp and into
the zswap one — that split is not a preference, it is the stated dividing
line, and it is on the side upstream says it is heading.

**Shakeel Butt, 2026-04-15**, named the livelock mechanism precisely:

> "Or **incompressible memory on zswap with writeback disabled** or
> overcommitted memory.min."

That is the configuration that livelocks, and it is the one just removed.
Writeback being *enabled* is the whole point of the swapfile.

**On the xswap series that was removed**, the reviewers' objection was exactly
its missing writeback. Johannes Weiner, NACKing the related ghost-swapfile
design (2025-11-21):

> "for a solution to this to be acceptable, it has to work with the primary
> usecase and **support disk writeback**. This direction is a dead-end."

and Nhat Pham, 2026-09-04, restating it as a requirement for any successor:

> "**Writeback is core functionality for zswap, not an add-on**, and a design
> needs to account for it from the start."

**One dissent, recorded rather than buried:** Sergey Senozhatsky (zram
maintainer), 2026-03-12 — *"There are also setups where zram is configured
with a backing device (a real physical device) to which zram writeback pages,
effectively releasing pool memory that they occupied."* True, and it is why
zram was evaluated rather than dismissed. It is not available here: the
backing device must be a raw block device and there is no spare partition.

**Not found, stated as such:** no mail in `lore-linux-mm` frames the failure
as *"zswap pool full → `zswap_store()` fails → page returns to the LRU →
livelock"*. The discussions run through reclaim-efficiency counters and
`no_progress_loops` instead. That specific chain belongs to the xswap patch
set's own `SWP_XSWAP` guard, which was removed with it.

## The MARIE swappiness clamp — the OOM this does NOT fix

**Switching backends did not fix the 2026-09-22 OOM, and would not have.** The
cause was LRU-MARIE, and it applied to every backend equally.

MARIE's reclaim driver clamps the effective swappiness before choosing between
the anon and file lists:

```c
u8 configured = (u8)mem_cgroup_swappiness(memcg);
u8 swappiness = (READ_ONCE(marie_low_swappiness_mode) && configured > 1) ?
                1 : configured;
```

`marie_low_swappiness_mode` defaults to **1**, so `vm.swappiness = 180` had
never taken effect here. MARIE's own header says so: the clamp applies
*"regardless of the higher values vm.swappiness / memory.swappiness udev
rules, tuning daemons, or distro defaults have installed."*

swappiness = 1 makes reclaim file-dominant, which is the wrong direction when
swap is compressed and fast: an evicted file page costs an NVMe re-read, while
an anonymous page is only compressed. Measured over one boot: `pgsteal_file`
31,181,709 against `pgsteal_anon` 8,779,224 — file reclaimed **3.55x** more
than anon — with both lists refaulting at ~6.8M.

At 21:14:27 on 2026-09-22 that ended in a kill:

```
thrash livelock: net-progress 131141 refault / 192089 steal, free 175450, invoking OOM
Workqueue: events thrash_wd_fn
 out_of_memory+0x26b/0x340
 thrash_wd_fn+0x4c8/0x600
```

`thrash_wd_fn` is MARIE's own livelock watchdog, and it fired on a premise
that was false at that moment: free swap was 27,235,488 kB of 32,432,124 kB
(84% free), 21,599,852 kB of clean inactive page cache was still resident, and
only 685 MB was free. Its escape gate is `free > high`; the zone highs sum to
219,589 pages (857 MB), so 685 MB sat below it, the gate never tripped, and
after 8 consecutive two-second windows of refault:steal at or above 1:2 it
invoked the OOM killer against `electron` (Discord).

`marie-low-swappiness-mode.conf` clears the knob so the configured 180 reaches
the pick driver. **That, not the backend change, is the fix.**

## Install

```bash
sudo install -Dm644 99-zswap-swappiness.conf      /etc/sysctl.d/99-zswap-swappiness.conf
sudo install -Dm644 marie-low-swappiness-mode.conf /etc/tmpfiles.d/99-marie-low-swappiness-mode.conf
sudo ./setup-swapfile.sh
```

zswap is on by default (`CONFIG_ZSWAP_DEFAULT_ON=y`) and so is the shrinker
(`CONFIG_ZSWAP_SHRINKER_DEFAULT_ON=y`) — the latter is **load-bearing**, since
without it nothing ever drains the pool.

## Verify after a reboot

```bash
swapon --show                             # /swapfile, priority 100
cat /proc/sys/vm/swappiness               # 180
cat /sys/kernel/mm/lru_marie/low_swappiness_mode   # 0   <- the OOM fix
cat /sys/module/zswap/parameters/enabled           # Y
cat /sys/module/zswap/parameters/shrinker_enabled  # Y
sudo cat /sys/kernel/debug/zswap/stored_pages      # grows under pressure
sudo cat /sys/kernel/debug/zswap/written_back_pages # >0 once the pool drains
```

If `low_swappiness_mode` reads 1, the swappiness fix is **not** in effect —
check `/etc/tmpfiles.d/` and re-run `systemd-tmpfiles --create`.

`/sys/kernel/debug/zswap` is readable **only as root**. An unprivileged `[ -d ]`
or `ls` on it fails with `EACCES` and looks exactly like the directory not
existing; that mistake was made once here already.

## Known limitations

- **Hibernation remains impossible.** The image must go to a swap device that
  survives power-off; this is a swapfile, so it *could* be made to work, but
  the kernel command line carries no `resume=` and the swapfile is not sized
  for it. `mem_sleep_default=deep` (suspend-to-RAM) is what this setup is for.
- **The swapfile is the overflow, not a second RAM tier.** Entries only reach
  it after the shrinker decides they are cold, so ordinary use should write
  very little to the NVMe. Under sustained pressure the write volume rises —
  that is the trade for a drain that works.
- **`max_pool_percent` stays at the default 20** (6.4 GB compressed here,
  ~19 GB uncompressed at 3:1). That is ample for a measured ~6 GB anonymous
  working set. Raise it if the pool pressure-thrashes; it is a live sysfs
  write.

## What changed on 2026-09-22

- **MARIE's swappiness clamp cleared** — the actual OOM fix.
- **Swap backend: xswap -> zswap + a 16 GiB swapfile.** The xswap series
  (`2155`-`2168`, `2199`; 15 patches) was removed; patch `2196`, a standalone
  zswap fix salvaged from that series, was added.
- `CONFIG_XSWAP` removed. `CONFIG_ZSWAP_DEFAULT_ON` stays on.
- zram was evaluated and rejected on the drain argument above, not on the
  older and **incorrect** claim that it never returns memory — that claim was
  in this file's previous revision and is false: zsmalloc has a shrinker and
  frees a zspage as soon as it empties. Only the device *size* is fixed.
