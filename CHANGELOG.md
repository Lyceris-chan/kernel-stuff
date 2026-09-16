# Changelog

Notable changes to `linux-sleepy-next`, the only package in this repository. It
targets one machine: an AMD Ryzen 7 7700 (Zen 4) with a Radeon RX 9070 XT
(Navi 48 / RDNA 4).

One entry per released package version, newest first. On the mainline line a
version is `<kernel base>-<pkgrel>-sleepy-next`, which is what `uname -r`
reports. The earlier linux-next preview releases appended their snapshot date,
as in `7.2.0-10-sleepy-next-20260828`. The format follows
[Keep a Changelog](https://keepachangelog.com/).

Two earlier artifacts are summarised at the end under
[Earlier packages](#earlier-packages): the 7.2 `linux-sleepy` package and the
`wannabe-7.3` preview tree. Both were removed from the working tree, and their
full entries remain in git history.

## [7.3.0-rc3-16-sleepy-next]: 2026-09-15

### Boot speed

Measured before touching anything: `9.406s firmware + 485ms loader + 2.099s
kernel + 2.777s initrd + 14.751s userspace = 29.521s`. The userspace half was
almost entirely one thing, visible straight from the critical chain:

```
graphical.target @14.751s
└─ multi-user.target @14.720s
   └─ net-tune.service @14.689s
      └─ network-online.target @14.685s
         └─ NetworkManager-wait-online.service @2.339s +12.346s
```

**The session was waiting 12.3s for DHCP.** Two of our own units were pulling
that wait into the boot: `net-tune.service` was `WantedBy=multi-user.target`
with `After=network-online.target`, and the same shape had been added to
`blocky.service` by a drop-in. A unit that `multi-user.target` pulls in **is
waited for**, so an `After=network-online` service enabled there holds the
desktop back until the link is up — the earlier note in the unit ("deliberately
NOT ordered Before=network.target") had fixed one half of this and missed the
other.

- Both are now pulled in by `network-online.target` instead:
  `net-tune.service` in the package (its `WantedBy`, the enable symlink, and the
  `install` step), `blocky.service` by an explicit
  `network-online.target.wants` symlink — `systemctl enable` reads `[Install]`
  from the unit file and ignores a drop-in's `WantedBy`, so the symlink is the
  mechanism and the drop-in keeps only the ordering. Both still start the moment
  the link is up; the desktop no longer waits for either.
- **`2170`-adjacent, found by `systemd-analyze verify` while doing this:**
  `xswap-create.service` had an ordering *cycle*
  (`tmp.mount → swap.target → xswap-create → local-fs.target → tmp.mount`),
  which systemd resolved by deleting the `tmp.mount` job at every boot. It
  happened to mount anyway, but the fix is to drop `After=local-fs.target` —
  the root is mounted by the initramfs, so `Before=swap.target` is all the unit
  needs.
- **`R8169` and `REALTEK_PHY` are built in, not modules.** As modules, udev
  loaded them after the root switch: probe at 6.26s, PHY attached at 7.05s,
  carrier at 10.13s — the ~3s of link negotiation ran *after* most of the boot
  and pushed DHCP to the very end. Built in, the probe happens during kernel
  init and that negotiation overlaps with the rest of boot. The PHY driver has
  to be built in too, or the carrier waits for it to be loaded anyway.

Not touched, with reasons: the initramfs (`54.5 MB`, but it unpacks in 25 ms —
`Unpacking initramfs...` at 0.311756 to `Freeing initrd memory: 55776K` at
0.336762 — so trimming it saves almost nothing). The bulk is not microcode: the
`microcode` hook adds one 128,644-byte file, and the rest is mkinitcpio moving
already-compressed payloads into the early CPIO so they are not compressed
twice — here ~29 MiB of `amdgpu` firmware (699 `.bin.zst` files, pulled in
because the driver declares 638 firmware entries) plus `amdgpu.ko.zst`. The
`kms` hook could shave the initrd's early module load but changes when the
display modesets, which is not a trade to make blind on this monitor. The 9.4s
of firmware time is POST, not the kernel.

### Boot speed, second pass (Arch wiki + CachyOS wiki)

Both wikis were read against this machine's measured boot. Most of what they
recommend is already in place or does not apply, so the useful output is
negative results — recorded here so the same ground is not covered twice.

- **The 12.346s is DHCP, not systemd overhead.** NetworkManager starts at
  22:29:37.69, carrier at 40.90 (+3.2s), lease at 50.19 (+9.3s). Building the
  NIC in moves the driver probe from 7.2s to kernel init, so the negotiation
  overlaps boot instead of following it.
- **`cachyos-rate-mirrors.timer` reads like a second gate and is not one.** It
  carries `Wants=` *and* `After=network-online.target`, and `timers.target` is
  `WantedBy=basic.target`, which looks like a CachyOS packaging bug holding the
  whole session. On this boot `basic.target` entered at `6883384µs` and
  `timers.target` at `19563507µs`, and `basic.target` is `After=timers.target`:
  systemd had already broken that edge as part of the cycle `basic.target →
  timers.target → cachyos-rate-mirrors.timer → network-online.target →
  NetworkManager-wait-online → NetworkManager → basic.target`. The timer waits
  on the network-online wave; it does not cause it. A drop-in clearing its
  `After=` was written, measured to change nothing — an empty `After=` does not
  reset an ordering list from a drop-in — and reverted. Its `Wants=` is
  load-bearing and stays: it is one of the units that pulls
  `network-online.target` in, and `net-tune` and `blocky` are `WantedBy` that
  target.
- **Disabled: `system76-power-monitor.service`.** Hand-written, owned by no
  package, ordered `After=com.system76.PowerDaemon.service` which does not
  exist, running `/usr/local/bin/s76-profile-monitor` — a
  `while true; do system76-power profile; sleep 3; done` loop for a binary that
  is not installed. It forks three processes every three seconds and can never
  succeed. The unit and the script are left on disk; re-enable with
  `systemctl enable --now system76-power-monitor.service`.
- **Rejected, with the reason.** `kexec` reboots would skip the 9.4s POST but
  re-initialise the GPU from a running kernel, which is not a change to make
  while the display path is under A/B. Also rejected: dropping the `kms` hook;
  dropping the `base` hook (it is the recovery shell, and the presets build no
  fallback image); `MODULES_DECOMPRESS="yes"` with `xz -9e` (trades a ~250 ms
  ESP read for single-threaded decompression); `libahci.ignore_sss=1`
  (applicable — `ahci 0000:10:00.0: SSS flag set, parallel bus scan disabled` —
  but the MX500 is `x-systemd.automount` and nothing on the critical path waits
  for it); and the silent-boot console flags (the console is the GPU
  framebuffer, so they touch the display path). Each is worth a few hundred ms
  at most, against a 12.3s win already taken.
- **Left open.** A 748 ms gap inside the initrd, between the root fsck
  finishing (2.730555) and `/sysroot` being mounted (3.478237), with only USB
  enumeration in the log. Nothing in the initrd accounts for it.

### Changed
- `pkgrel` 15 → 16.

### Verified after the reboot (2026-09-16 05:34, running `7.3.0-rc3-16`)

- **The gate is gone.** `graphical.target` is reached after **2.083s** of
  userspace, down from 14.751s: 29.5s → 24.9s total, and **17.2s from power-on
  to a usable desktop**. `NetworkManager-wait-online.service` still takes
  7.666s but now runs behind the desktop — nothing waits for it. The NIC change
  landed as well: `r8169` probes at **0.663s**, down from 7.211s. Carrier only
  moved 10.13s → 9.79s, because the PHY attach and link-up are now gated by
  userspace (udev renames at 6.4s) rather than by the driver, and ~2.9s of that
  is autonegotiation.
- **New finding, unrelated to the boot work: LRU-MARIE underflows memcg LRU
  accounting on every boot.**

  ```
  mem_cgroup_update_lru_size(...): lru_size -2522
  WARNING: mm/memcontrol.c:1548 at mem_cgroup_update_lru_size
    lru_reparent_memcg+0x1c4/0x460      <- the classic-LRU branch
    mem_cgroup_css_offline+0x20f/0x440
  ```

  It fires on **every `sleepy-next` boot from rc3-6 through rc3-16 and on
  neither `cachyos-rc` boot**, so it is ours rather than upstream's.
  `mm/memcontrol.c` calls `lru_gen_reparent_memcg()` when `lru_gen_enabled()` is
  true and the classic `lru_reparent_memcg()` otherwise; `2101` forces
  `lru_gen_enabled()` false whenever LRU-MARIE is on, so we always take the
  classic branch, which sums the child's `lru_zone_size` into the parent. The
  child's counter was already `-2522` — something debited it more often than it
  credited it.

  The LRU-MARIE patch documents this failure mode in its own comments — *"a
  legacy debit, so `mz->lru_zone_size` drifts and a later legacy/Marie del
  underflows ("marie underflow-del" / `mem_cgroup_update_lru_size lru_size
  -1`)"* — and carries fixes for several instances. At least one path remains
  in 0.11.1r2, and that is the newest revision upstream, so there is nothing to
  upgrade to.

  Two things make this more than cosmetic. The warning is `WARN_ONCE`, so only
  the first occurrence per boot prints while the `*lru_size = 0` recovery runs
  on *every* occurrence — the real frequency is unknown and one per boot is a
  lower bound. And `lru_zone_size` is what `lruvec_lru_size()` sums, which
  reclaim reads. `CONFIG_DEBUG_VM` is off, so the `VM_BUG_ON(1)` next to the
  warning is inert; with it on this would be a `BUG()`, not a warning.
- **What is left, and why none of it is worth taking.** Firmware 9.835s is BIOS
  POST — the only Linux-side lever is `kexec` on reboots, which re-initialises
  the GPU from a running kernel. Kernel 2.100s is PCI/USB/SATA enumeration with
  no gap above 250 ms and nothing dominant. The initrd's 2.717s includes a
  725 ms wait between fsck finishing (2.789) and `/sysroot` mounting (3.489),
  filled with a USB hub cascade; `systemd-udev-settle` is not in the initramfs,
  so the usual cause is ruled out. Userspace is 2.083s. Dropping the `kms` hook
  would cut roughly 245 ms from the 485 ms ESP read, at the cost of moving when
  the display modesets.

### Third pass: service audit and dead config (2026-09-16)

Every enabled unit was audited against this hardware, plus the wiki pages the
first two passes had not read (`Systemd`, `Improving performance`, `Solid state
drive`, `Ext4`, `Power management`, `XDG Autostart`).

- **`nowatchdog` is inert on this kernel, and the kernel says so:**
  `Unknown kernel command line parameters "nowatchdog"`.
  `CONFIG_SOFTLOCKUP_DETECTOR` and `CONFIG_HARDLOCKUP_DETECTOR` are both unset,
  so the parameter has nothing to disable. What *is* running is
  `CONFIG_CLOCKSOURCE_WATCHDOG=y`, which `nowatchdog` never controlled.
- **The 159 ms stall that watchdog reports is not its fault.** `Watchdog remote
  CPU 4 read timed out` lands inside the 725 ms initrd gap and reads like a
  cheap 159 ms win. It is not: `watchdog_handle_remote_timeout()`
  (`kernel/time/clocksource.c`) runs from `schedule_work(&watchdog_work)` and
  prints *after* the stall it detected, so the line is a symptom. Disabling the
  watchdog would hide it and cost TSC-drift detection on a machine whose A/B
  methodology depends on stable timing. Left on.
- **`bpftune` is malfunctioning against this kernel's deliberate config.**
  Because this package builds `-d TCP_CONG_BBR -e TCP_CONG_BBR3`, CachyOS's
  bpftune hunts a congestion control named `bbr` that cannot exist here —
  `modprobe: FATAL: Module tcp_bbr not found in directory
  /lib/modules/7.3.0-rc3-16-sleepy-next` — then rewrites
  `net.ipv4.tcp_allowed_congestion_control` three times per boot
  (`reno bbr3 cubic` → `+htcp` → `+dctcp`) chasing it, and counts the failed
  attempts as successes. It holds 69 MB, and `net-tune` sets that key anyway.
  Recommended but not done, because it is a working tuning tool with a broken
  edge rather than a defect, so the call is the user's:
  `systemctl disable --now bpftune.service`.
- **`network-online.target` is not reached until ~12 s into the boot**, so
  `net-tune` (CAKE) and `blocky` (DNS) are both down until then. A functional
  gap, not a boot-time one — `graphical.target` is at 2.083s and nothing waits
  for the target. Closing it means triggering those two off the interface coming
  up rather than off the target, and `net-tune.sh` `exit 1`s when no UP
  interface exists, so it is not a one-line change.
- **Dead config that prints errors every boot**, all of it owned by CachyOS
  packages under `/usr/lib`, so the fix belongs upstream rather than in an
  override: amdgpu's `si_support=1 cik_support=1` (GCN-era options that no longer
  exist for Navi 48); `70-cachyos-settings.conf` writing `kernel/nmi_watchdog`
  and `kernel/unprivileged_userns_clone`, neither of which this kernel has; and a
  `sp5100_tco` blacklist for a driver that is not built. The swappiness conflict
  is ours: `99-custom-tweaks.conf` sets 180 and `99-xswap-swappiness.conf` sets
  150, so 180 is dead by lexicographic order and still carries a comment about
  zram.
- **`journald` `SystemMaxUse=50M` retains about 14 boots, or two days.** That is
  the history every A/B comparison depends on, and raising it is free on a 1 TB
  NVMe — but clear the `faillock` entries first (see `LESSONS.md`), or the extra
  space preserves those too.
- Verified as deliberate and left alone: `power-profiles-daemon` is CachyOS's
  build and is wired to `scx_loader` (its binary carries `org.scx.Loader`
  strings), so the two are not duplicates and changing the power profile also
  switches sched-ext mode. `cachyos-iw-set-regdomain.path` watches
  `/etc/localtime` rather than a NIC and is enabled only because `iw` is
  installed; it costs no boot time. `lvm2-monitor` (47 ms) and `acpid` have no
  work here but are equally cheap.

### swappiness corrected to 180 (2026-09-16)

The swap stack shipped `vm.swappiness=150`, which was only ever CachyOS's zram
udev-rule default preserved for continuity. Checked against the primary sources:

- **`Documentation/admin-guide/sysctl/vm.rst`** defines swappiness as a relative
  IO cost over 0-200, where 100 means equal cost between swap and filesystem
  paging, and says "for in-memory swap, like zram or zswap, as well as hybrid
  setups that have swap on faster devices than the filesystem, values beyond 100
  can be considered". Its worked example gives **133** when swap is 2x faster
  than the filesystem (`x + 2x = 200, 2x = 133.33`).
- **The Arch Wiki's Zram article** ("Optimizing swap on zram") recommends
  **180**, together with `watermark_boost_factor = 0`,
  `watermark_scale_factor = 125` and `page-cluster = 0`.

The second point is what settles it: `/etc/sysctl.d/99-custom-tweaks.conf`
*already* sets the other three values of that Arch Wiki block — so the machine
was running three quarters of a scheme whose fourth member is 180, and 150 was
mixed in from a different origin entirely. An xswap device has no backing store,
so its "IO" is a compress and decompress in RAM, further past the kernel's
2x example than zram itself.

An earlier note in this session claimed "no official source recommends 180" —
that was wrong, and came from reading only the first paragraph of the sysctl
documentation. The section continues past it.

`vm.swappiness` is therefore 180, documented in
`sleepy-next/swap-stack/99-xswap-swappiness.conf`. The kernel documentation is
explicit that the optimum is workload-dependent: "An optimal value will require
experimentation."

### Six-source sweep (2026-09-16)

Base is current: **v7.3-rc3 is still the newest mainline tag** (no rc4 yet).
Today's snapshot is **next-20260916**.

**1. xswap v1 → v2 — the sweep's actionable item.** Baoquan He has posted a v2
of the series we carry as `2155`–`2166`: **12 patches became 14**. It is present
in both `sirlucjan-kernel-patches/7.3-rc/xswap-patches-v2-sep/` and the CachyOS
`7.3/xswap` branch independently. The two additions are:

- `0012 mm, swap: cap xswap growth at nr_clusters` — not carried
- `0014 mm, swap: shrink xswap to the ceiling when it drops` — not carried

These fix exactly what the code audit recorded in *"Code audit of the series
(2026-09-16)"* above: the `type<N>/limit` attribute is a soft bound because the
**grow** path is gated on `nr_clusters_max` (fixed at creation) while the only
reader of `nr_clusters` is `xswap_try_shrink()`. The author has closed that gap
upstream. Adopting v2 is a series replacement, not a two-patch append: most v2
patches differ from ours in content, so v2 is a revision of the whole set.

Tested against a clean `v7.3-rc3` worktree: **v2 applies 14/14 clean**, while our
v1 fails 8/12 there (expected — earlier patches in our series supply its context,
per the *"clean-base FAIL is not a series FAIL"* rule).

**2. Verified drop list for the next bump.** Subjects of all 217 patches were
matched against linux-next; the 15 hits were then checked **by content**, because
subject matching alone produces false positives — four were exactly that
(`1061`, `1062`, `1152`, `2005` all matched a subject but differ in content and
stay). **Eleven are content-identical to upstream commits:**

| Ours | Upstream | Subject |
|---|---|---|
| `0050` | `5c1a6c9736a6` | drm/edid: Parse AMD VSDB for FreeSync refresh range |
| `0058` | `482b6542a862` | drm/amd/display: restore FRL cap on non-destructive |
| `0061` | `8b607d6f54b0` | drm/amd/display: Enable HDMI ALLM for Gaming-VRR |
| `1056` | `0e118b936dc5` | drm/sched: Lock drm_sched_entity_is_idle() |
| `1060` | `38f4fe785b5d` | drm/amdgpu: cancel hang_detect_work before taking |
| `1135` | `6ee70c955ffc` | drm/amd/display: fix HPD program filter programming |
| `1136` | `455c7c34707c` | drm/amd/display: Update and revert FRL LT Timeout |
| `1138` | `20331505df9c` | drm/amd/display: pull colorops into state |
| `1140` | `50eed169c0ab` | drm/amd/display: clamp force_min_dcfclk to dcn42b |
| `1154` | `dd601ed4ce28` | drm/amd/display: Fix NULL deref of new_stream->sink |
| `2006` | `3de3d4336b8c` | zram: convert to SG-list zsmalloc object read API |

**These are drop-at-the-bump, not drop-now.** They are in linux-next (7.4-bound),
not in our 7.3-rc3 base — dropping them today would remove the fixes. `1140` is
the one to drop first when its base arrives: it is a DCN42B clamp, inert on
DCN 4.0.1, and already flagged for removal.

**3. 7.4 conflicts to watch** — all land with the next base, none need action now:

- **amd-pstate EPP rework** (`amd-pstate-v7.4-2026-09-14`, Mario Limonciello):
  adds a per-SoC / per-core-type EPP table and `cpudata->epp_default_ac/dc`.
  **Collides with our `1202`** (`epp_boost`): both add fields to
  `struct amd_cpudata` and both touch `amd_pstate_epp_cpu_init()`. Ours is *not*
  superseded — upstream never mentions `epp_boost`; they are different
  mechanisms that clash textually.
- **zswap rework** (Longlong Xia, Kefeng Wang, Jianyue Wu; 2026-09-06..10):
  rewrites the tail of `zswap_store()` (`bcfacfe16322`) where **our `2155` hunk
  lives**, changes `zswap_invalidate()` to take a **range** (`6a391b347b5e`) —
  the path xswap pages leave the pool by — and moves pools to an xarray with
  `entry->pool` becoming `pool_idx`. Our series barely touches the structs
  (one `struct zswap_entry` reference, zero `->pool`), so the struct churn is
  harmless; the `zswap_store()` overlap is not.
- **`0412b1064a3b` "Cover EDID CEA parsing helpers"** — refactors
  `dm_edid_parser_send_cea()` in `amdgpu_dm_connector.c`, the file our flicker
  fix patches (`1151`: 8 hunks, `1163`: 4, `1164`: 9). Mechanical
  (`STATIC_IFN_KUNIT` visibility), so a rebase rather than a redesign.

**4. Work items.** `#5616` (RX 9070 XT `flip_done timed out`) **closed
2026-09-16** — its whole history is the Atomize GLOBAL_SYNC_STATUS patch, which
is our `1159`. Confirmed as the fix. `#5663` (artifacts after S3 resume on
RX 9070 XT) remains open with only a **user-posted, unmerged workaround diff**
pinning DCC BO moves to move-entity 0 in `amdgpu_move_blit()`; the maintainer
calls it a Navi 4x SDMA hardware bug. Not adopted — no upstream commit, and it
is not ours to carry. The `[PATCH 00/66] DC Patches Sep 14 2026` series (source
of `1159`/`1166`, heading to 7.3-rc4) contains on-target items we lack,
notably `40/66 Decouple HUBP_UPDATE_PLANE_ADDR from pipe_ctx` — the HUBP
plane-address path our "box" misread lives in. They arrive with the bump.

**5. Source health.** `repos/drm-next` is stuck at 2026-09-11 (its shallow clone
fails to unshallow: *"error in object: unshallow 00d66b29…"*) — its content is
covered because linux-next aggregates it. `repos/amd-staging-drm-next` is stale
at **2026-07-23**, and `repos/akpm-mm` at **2026-08-10** and will not refresh;
treat negative results from those two as weak. `repos/linux-tkg` and
`repos/cachyos-linux` local refs are behind their remotes.

**6. Nothing new** from `firelzrd-lru-marie` (our `2101` is code-identical to
0.11.1r2), `firelzrd-bore-scheduler`, `firelzrd-le9uo` (dormant since May),
`clearlinux-linux` (archived), or the CachyOS fixes branch (off-target by
policy — we do not carry the fixes squash). x86/security: nothing on-target
since 09-13.

## [7.3.0-rc3-15-sleepy-next]: 2026-09-15

### Added
- **`1166`** — "drm/amd/display: Return success status from check_mode_supported"
  (Alvin Lee, `Reviewed-by: Wenjing Liu`, DC 3.2.398 patch 59/66,
  `<20260908113338.2433445-60-chen-yu.chen@amd.com>`). `dml2_top_utm_check_mode_supported()`
  logged DML2's verdict and then returned a hardcoded `true`, so a mode the
  display mode library had rejected was still programmed. The fix returns
  `status == DML2_STATUS_OK`; it is the patch AMD recommends in the reports of
  **#5834** — a NULL pointer dereference in `update_config` that hits roughly 30%
  of the time when waking from screen-off (plain DPMS, not suspend) on a 9070 XT,
  leaving a blank screen and no usable tty. DPMS cycling is daily use here, and
  the same series' patch 58 is already carried as `1159`.
  *Watch on the first boot:* this makes mode validation authoritative, so a mode
  DML2 rejects is now refused instead of programmed. 1920x1080@240 and 1080p are
  ordinary modes for DCN 4.0.1 and unlikely to be rejected, but if the display
  comes up at the wrong mode after rebooting, drop `1166` (or boot the
  cachyos-rc entry) — that is the revert, and the changelog is the record.

### Verified after the reboot (2026-09-15 22:29, running `7.3.0-rc3-15`)

- **xswap is live**: `zswap/enabled=Y`, `compressor=zstd`, `/proc/swaps` shows a
  single `xswap0` of 30.9G at priority 100 with pages already in it (83 MB
  compressed holding 268 MB, ~3.2x), `/sys/kernel/mm/xswap/{create,destroy,type0}`
  present, and `xswap-create.service` exited 0. No zram swap anywhere; the
  leftover `zram0` node is size 0 and its setup unit is dead. `vm.swappiness`
  is 150 from the sysctl drop-in, replacing what the masked udev rule used to set.
- **The flicker fix holds**: `vrr_capable=0` and `passive_vrr_capable=0` on both
  HDMI connectors, `VRR_ENABLED=0`, `PASSIVE_VRR_DISABLED=1` — the same state the
  clean cachyos-rc kernel showed.
- **`1166` did not reject the mode**: CRTC 438 is driving 1920x1080 at
  **239.96 Hz** as before. This was the one item to watch after making DML2 mode
  validation authoritative, and it is the outcome that mattered.
- One `amdgpu` message appears (`Failed to setup vendor infoframe on connector
  HDMI-A-2: -22`); it is present with the **same count in the previous boot**, so
  it predates this series and belongs to the second monitor's sink, not to any
  patch here.

### Changed
- `pkgrel` 14 → 15. Series is now 217 patches.

## [7.3.0-rc3-14-sleepy-next]: 2026-09-15

### Added
- **`2170`** — "mm: vmalloc: fix `vmap_purge_lock` livelock under memory
  pressure" (Ye Liu, `6c06fec56a63d`, `Fixes: 7679ba6b36db`,
  `Reviewed-by: Uladzislau Rezki (Sony)`, in akpm's tree). `__purge_vmap_area_lazy()`
  holds `vmap_purge_lock` across a `flush_work()` while `vmap_node_shrink_scan()`
  can block on that same lock from direct reclaim — a circular wait that
  deadlocks the whole system under memory pressure. The fix takes the lock with
  `mutex_trylock()` in both reclaim-reachable paths and reports
  `SHRINK_STOP`; skipping a pool decay is harmless. `mm/vmalloc.c` is not
  touched by any other patch in the series.

### Changed
- **Renumbered for order.** `1165` now sits after `1164` instead of back at the
  `1140` slot it kept when it was renamed from `1140`, and `2142` became
  **`2169`** so the three parts of its series read `2167`, `2168`, `2169`.
  `source=()` is now sorted ascending end to end. No patch content changed.
- `pkgrel` 13 → 14. Series is now 216 patches.

### Ledger repair
- `PATCH_SOURCES.md` had a stale index row for `9061` (evaluated and dropped
  for a compile failure, never carried) and **no row at all for `0055`**, which
  is carried. Both fixed; `0055`'s row now names its real provenance (a
  `[sleepy]`-stripped version of Fangzhi Zuo's submission, not the
  `150619` archive id the prose implied). Every remaining row without a file is
  an intentional "Dropped" record.

## [7.3.0-rc3-13-sleepy-next]: 2026-09-15

### Fixed
- **`2142` was an incomplete series, and incomplete made it wrong.** It is
  patch 3/4 of Xueyuan Chen's "[PATCH v7 0/4] mm: avoid large folio splits when
  swap is unavailable"; only 3/4 was carried. It gates the large-folio split
  fallback in `shrink_folio_list()` on `ret != -E2BIG`, and **nothing in the
  tree returned `-E2BIG`** — 2/4 is what introduces that classification — so
  every `folio_alloc_swap()` failure took the "do not split" branch. The THP /
  mTHP swapout fallback was unreachable dead code, the exact opposite of the
  patch's intent, and it made large anon folios that could not get swap get
  reactivated instead of split. Added **`2167`** (1/4, `page_counter_margin()`)
  and **`2168`** (2/4, the `0`/`-E2BIG`/`-ENOSPC`/`-ENOMEM` classification,
  `Acked-by: David Hildenbrand`), which restores the intended behaviour: split
  only when splitting might help, skip the pointless split when swap is
  exhausted. Patch 4/4 (shmem) is not carried and not needed for correctness.
  This is the failure mode the "a patch that applies can still do nothing" rule
  warns about, in the opposite direction: the patch did something, and the
  something was wrong.

### Deep sweep results not adopted
- **Work items**: `dc66/59` ("Return success status from check_mode_supported",
  Alvin Lee, AMD) is the one AMD recommends in #5834's NULL-deref reports and
  it applies cleanly to our series. Not adopted yet **because of what it
  changes**: it makes DML2 mode validation actually return failure instead of a
  hardcoded `true`. If DML2 dislikes 1920x1080@240 it would now be rejected, and
  this display just got fixed. It arrives with the DC 3.2.398 drop in the next
  drm merge, where AMD tests the set together — re-evaluate then.
- Wentland's RGBA8888 surface-format enablement (#5339, field-tested on Navi 48)
  is skipped on evidence: this machine logs **zero** "Unsupported screen format"
  messages in dmesg and the journal, so it is not hit here.
- superm1's EDID-override pair (#5779) only matters if an override is in use.
  Correcting an earlier note: it does **not** collide with our `1143` (different
  files entirely).
- MM: Kefeng Wang's zswap invalidate/store v3 has **no measured claim** in its
  cover letter ("eliminate redundant per-slot lookups"), and it shares
  `swap_range_free()` with our xswap series — still deferred for that reason.
  Usama Arif's PMD-level swap v7 does not apply as posted (needs `f078c72e5ca2`
  + `94edc3c732625` for 12/29 and a hugetlb patch absent from rc3 for 14/29).
  Hugh Dickins' fbatch v2 collides with LRU-MARIE in `mm/folio.c` (436 changed
  lines) and its author expects "some disappointments".
- The Ghiti zswap-writeback fixes fail on our series state at `mm/zswap.c:1001`
  — exactly where xswap's `2155` rewrites the store/writeback path. They are
  accounting fixes, and we have no writeback target (no disk swap).

### Changed
- `pkgrel` 12 → 13. Series is now 215 patches.

## [7.3.0-rc3-12-sleepy-next]: 2026-09-15

### Added (from the 2026-09-15 sweep)
- **`2012`–`2013`** — Zhenxian Ma's "block: avoid redundant flushes for O_DSYNC
  direct writes" pair (linux-next `bec7d36a6514`, `0d492f40c4ad`, `Reviewed-by:
  Christoph Hellwig`, merged by Jens for 7.4). `blkdev_write_iter()` called
  `generic_write_sync()` unconditionally, so an `O_DIRECT|O_DSYNC` write paid a
  `REQ_PREFLUSH` on top of the `REQ_FUA` the direct path had already set. The
  author measured 4 KiB `O_DIRECT|O_DSYNC` writes on a Seagate ST20000NM007D
  going from 119.7 to 7497 IOPS. This machine's Phison E16 reports `fua=1`, so
  `2013` (use FUA only when the device supports it) is inert here; `2012` is the
  one that removes the redundant flush.
- **`2100`** regenerated from sirlucjan's 2026-09-14 `zstd-7.3` cut
  (`e0f9795534f4`, 2741 lines, 25 files vs 20). The newer cut carries more
  upstream zstd work, including a BMI2 dispatch refactor
  (`lib/zstd/common/bmi2.h`). zstd is now load-bearing for the swap stack, not
  just for btrfs.

### Removed (superseded by `2100`)
- **`2128`** (use `ZSTD_cpuSupportsBmi2()` in `ZSTD_initStaticCCtx()`) and
  **`2143`** (DDict hash-set probe wrap-around) are inside the new `2100`; its
  hunk reports already-applied and `2143` is skipped as present. Removed with
  the user's approval — the code stays in the tree through `2100`.

### Sweep 2026-09-15: three parallel sweeps (MM, crypto/block/net, PM/x86/sched + work items)

**Hazard for the 7.4 bump — re-test the flicker fix.** Upstream has merged
"Enable HDMI FRL by default" (`af6139855b55`, in amd-staging only for now,
targeted 7.4), which sets `DC_FRL_MASK` in `amdgpu_dc_feature_mask`. That is
exactly the variable this project bisected for the 240 Hz flicker and dropped
as `1144` (`PATCH_SOURCES.md`). When the bump lands, re-check the MAG251RX at
1920x1080@240 Hz before shipping. Related: Fangzhi Zuo's FRL patches 61/66 and
65/66 in Chenyu Chen's DC 3.2.398 series sit on the same surface as our `0058`
and `1136`.

**Already carried — the sweeps re-found our own patches.**
- `2500` is `f7491d7c81db` (the Phoronix "silent user-space data loss since
  2023" item); `2502` is `27600805e62f` (x86/amd_node PCI refcount);
  `2404` is `c7a1c6e8004a` (sched_ext). All three are now upstream post-rc3
  and go on the drop-list for the next bump.
- `1159` is patch 58/66 of Chenyu Chen's DC 3.2.398 series — the patch AMD
  developers recommend in work items #5829, #5834 and #5839 for `update_config`
  NULL dereferences. Carrying it already.
- The kbuild series Phoronix covered on 2026-09-15 ("~36% faster builds") is
  the `[PATCH v2 00/21]` series we already carry as `2302`–`2322`.
- `2140` (direct compaction for costly `__GFP_NORETRY`) is in mm-unstable —
  ours already. `2011` is byte-identical to the r8169 LTR ML v4.

**Deferred, with reasons.**
- zswap "optimize zswap invalidate and store" v3 (Kefeng Wang, 3 patches)
  applies cleanly and is on-target now that zswap backs the swap stack. Held
  back deliberately: it rewrites `swap_range_free()`, the same function the
  xswap series (`2155`–`2166`) rewrites, and both are unmerged review-stage
  series. Composing two of those in the swap hot path is how this project got
  the flicker. Re-evaluate at the 7.4 bump, when at least one of them lands.
- Usama Arif's PMD-level swap entries for anonymous THPs v7 (29 patches) is
  the most on-target MM series found (THP swap + zswap + xswap all in play),
  but it is a large review-stage rewrite of the same paths. Watch.
- Hugh Dickins' `mm/fbatch` drain v2 (26 patches): the author states he is
  taking three weeks off, expects "some disappointments" on performance, and
  asks someone else to shepherd it.
- Lorenzo Stoakes' VMA-flag semantics v2 (40 patches) is the same churn that
  already broke LRU-MARIE once (`vm_flags` → `vma_flags`).
- CPPC: our `1210`–`1224` are Christian Loehle's **v5**; a **v6** exists
  (2026-08-30, same 15-patch shape, still under review with an outstanding
  request from Rafael Wysocki). Refresh at the bump rather than mid-cycle.
- amd-pstate 7.4 pull: Zen 6 EPP tunings do not apply to Zen 4, but the pull
  restructures `amd-pstate.c`/`.h` where our `1201`/`1202` live — expect a
  rebase surface.
- **BBR3 rebase surface**: linux-next `cb145191e9d3` renames `min_tso_segs()`
  to `tso_segs()` with a new signature; `0101-cachy-bbr3.patch` references the
  old name 13 times.
- io_uring: cancel-at-ring-close (merged for 7.4) and Jens Axboe's 15-patch
  thread-identity handoff RFC are 7.4 material — the RFC's own table shows
  large queue-depth-1 wins but losses at higher depth (−65% fsync on ext4 at
  qd32), so it is not obviously a win. `net/sched` qdisc handle scan needs 32767 HTB classes to
  matter (ours has one). Rejected as off-target: r8169 RSS v13 (RTL8127),
  realtek PHY firmware writes (RTL8261x), `xor_gen` AVX-512 (`CONFIG_BLK_DEV_MD`
  is off), `tcp_poll()` `smp_rmb()` (an ARM64 win), zonelist/NUMA and
  cache-aware-scheduling work (single-CCD desktop), ESMTP (SEV-SNP guests).

**Checked and dismissed: the NAP governor.** A sweep pass reported that the
NAP cpuidle governor never tests `states_usage[].disable` and could enter a
C-state disabled via sysfs. It does test it — in `nap_fallback_heuristic()`,
in `nap_find_min_valid_state()` (behind the cached-minimum path), and in the
neural-net decision loop inside `nap_fpu_select()` before it accepts a
candidate. No action.

**Machine profile corrections that shrink the search space.** `CONFIG_NUMA` is
**not set** in this build, so the NUMA-targeted optimizations that dominate mm
and net-next (zonelist refactors, per-node reclaim, `skb_defer_free` node
iteration, cache-aware scheduling) are inert here, and `for_each_node()` and
`for_each_online_node()` compile to the same thing. `CONFIG_BLK_DEV_MD` is off,
so the raid6/xor `vzeroupper` work is inert. `CONFIG_EROFS_FS` is off.

**Two branches/dirs we do not adopt from, checked.** CachyOS's `7.3/vesa-dsc-bpp`
carries VESA DSC EDID parsing and a DSC `max_qp` spec fix; the EDID side is
already upstream in rc3 and this machine never negotiates DSC (1080p240 fits
HDMI 2.0's 600 MHz TMDS without it), so nothing to take. sirlucjan ships
**ADIOS**, a 2,062-line non-upstream "Adaptive Deadline I/O scheduler"
(`block/adios.c`, Piotr Gorski, 3.3.0) that CachyOS patches to be the default.
Not adopted: it is unreviewed third-party block-layer code, and this machine's
scheduler is a deliberate distro choice — `60-ioschedulers.rules` sets **kyber**
for NVMe, bfq for rotating, mq-deadline for other flash. Worth revisiting only
if desktop I/O latency ever becomes a complaint.

**Verified drop-list (reverse-apply audit against torvalds master, 2026-09-15).**
Five carried patches are already in master and disappear at the next bump:
`2141` (filemap retain mapped dropbehind folios), `2145` (mm/vma unaccount on
mmap_prepare failure), `2146` (mm/mlock IRQ-safe NR_MLOCK accessor), `2500`
(MADV_FREE/THP data loss) and `2502` (x86/amd_node PCI refcount). The check is
`git apply --check -R` per patch against a worktree at `origin/master` — note it
must run against a master checkout, not the repo's working tree, which sits at
rc3 and makes every patch look un-applied.

**Work items.** The five tracked issues (#5821 hang, #5820 SMU bus loss, #5800
vblank timeout, #5812 VRR black level, #5780 HDMI FRL) still have no referenced
fix. #5720's fix (`c4a5160e3be0`) is absent from rc3 but concerns YCbCr-4:2:0
sinks, which this monitor is not. #5663 (TTM/SDMA artifacts after resume) is
acknowledged by Christian König as known and being investigated.

### Deep sweep 2026-09-15 (second pass): GPU/display, core, work items

**A patch we carry does nothing on this hardware — `1140`.** It modifies only
`dc/clk_mgr/dcn42b/dcn42b_clk_mgr.c`. That clk_mgr is instantiated exclusively
under `AMDGPU_FAMILY_GC_11_5_0` with `DCN_VERSION_4_2B`
(`dc/clk_mgr/clk_mgr.c`). Our GPU is GC IP (12,0,1), which
`amdgpu_discovery.c` maps to `AMDGPU_FAMILY_GC_12_0_0` → `dcn401_clk_mgr_construct`,
and the kernel reports "Display Core v3.2.392 initialized on DCN 4.0.1". The
DCN42B file is dead code here, so the patch is inert — the "a patch that applies
can still do nothing" trap again. A scan of every carried patch against the
display blocks we do not instantiate (dcn42, dcn42b, dcn60) found this as the
only case. Removal needs the user's approval; it is harmless where it sits.

**DC 3.2.398 (66 patches) triage — nothing adopted.** The reviewer-recommended
patch 58 is already ours (`1159`). The rest of the fix-shaped subset is
off-target or inert:
- patches 42, 43, 56, 57, 60 touch `pg/dcn42/`, `resource/dcn42b/` and the
  DCN42B MALL/HPO paths — the same dead blocks as `1140`; patch 61 touches
  `hpo/dcn42/` and `hpo/dcn60/`; patch 04 targets DCN31/35/42.
- `35c21515dbe1` ("fix MALL hysteresis timer underflow at high refresh rates")
  looked ideal — a 240 Hz-relevant underflow in the hysteresis timer — but it
  patches `dcn30_apply_idle_power_optimizations()`, and DCN 4.0.1 has its own
  `dcn401_apply_idle_power_optimizations()` (DMUB CAB based, no such timer).
  It is the DCN 3.x implementation that underflows, not ours.
- `37531443a4f3` ("mes12: clear event log on resume to avoid MES page fault",
  Jesse Zhang, AMD, 2026-09-15) is on-target but **inert at defaults**: its
  guard checks `amdgpu_mes_log_enable`, and
  `amdgpu_mes_event_log_init()` returns before allocating the buffer unless
  that parameter is set — it defaults to 0.
- DC 59 and DC 52 are behaviour changes inside a 66-patch drop that lands with
  the next drm merge; taking them piecemeal invites conflicts with the rest.

**Deferred for breadth, not doubt.** `2d606b35a24c` ("drm/sched: fix
use-after-free of the fence timeline name", v3 0/2) is a real UAF fix but a
121-line rewrite of fence lifetime across `sched_fence.c`, `sched_main.c` and
`gpu_scheduler.h` — and this series already carries four drm/sched patches.
`1528781b16c7` ("drm/vblank: Don't arm vblank timer with invalid frame
duration", v4) changes `drm_calc_timestamping_constants()` from `void` to `int`
across DRM. Both land upstream; revisit at the bump.

**Core sweep:** nothing includable. The only real candidate, a hrtick repick
fix (Shubhang Kaushik), is measured on ARM64 and the author partially withdrew
v2 ("please disregard the DL portion of v2") — and `CONFIG_SCHED_HRTICK` plus
HRTICK_DL are on here, so the withdrawn half is not inert. Wait for v3.
Everything else was already carried (`2012`/`2013`, `2148`/`2149`, `2302`–`2322`),
queued for 7.4, or inert.

### Changed
- `pkgrel` 11 → 12.

## [7.3.0-rc3-11-sleepy-next]: 2026-09-15

### Added
- **`2155`–`2166`** — Baoquan He's **v2 xswap series**, "mm, swap: extendable
  swap devices" (linux-mm, 2026-09-13,
  `<20260913075014.1732524-2..13-hebaoquan@kylinos.cn>`), 12 patches: the
  `XSWAP` Kconfig option, a sparse-vmalloc `cluster_info[]`, grow and shrink
  triggers driven by allocation and free, the `sysfs create` interface, a
  workqueue-deferred shrink, `xswap_destroy`, the zswap requirement, and a
  per-device size limit. An xswap device has no backing store — swapped pages
  live in zswap — and its metadata is mapped lazily, so it starts at 1xRAM and
  costs nothing until used. CachyOS carries the same series in its `7.3/xswap`
  branch. `CONFIG_XSWAP=y` is set. Upstream work in review: drop it when it
  lands, and check for a v3 before rebasing.
- **Swap stack switched from zram to zswap + xswap** on this machine. zram
  allocated a fixed 30.9 GB compressed block device and never gave the memory
  back; xswap grows and shrinks with use. The kernel side is the series above;
  the userspace side is `/etc/systemd/system/xswap-create.service` (creates one
  device at priority 100), `/etc/systemd/zram-generator.conf` and
  `/etc/udev/rules.d/30-zram.rules` symlinked to `/dev/null`, and
  `zswap.enabled=0` removed from `LINUX_OPTIONS` in `/etc/sdboot-manage.conf`
  so the built-in `CONFIG_ZSWAP_DEFAULT_ON=y` takes effect. Masking the udev
  rule matters: it forces `zswap/parameters/enabled` to `N` whenever a zram
  device appears, which would make `xswap/create` return `-EOPNOTSUPP`.
  `vm.swappiness=150` moves to `/etc/sysctl.d/99-xswap-swappiness.conf`; the
  masked udev rule used to set it.




### Changed
- **`2101`** now carries LRU-MARIE **0.11.1r2** from the author's repository
  (<https://github.com/firelzrd/lru_marie>). The r2 revision is 0.11.1 minus
  the `localversion` file creation (the `-marie` version suffix), which this
  repository had already stripped. It also restores the author's
  `scripts/setlocalversion` change — an `echo "+"` commented out — which is
  inert here because the kernel is built from a tarball and that branch only
  runs inside a git tree. The built version string is unchanged.
- `pkgrel` 10 → 11. Series is now 213 patches.

### Reviewed and not included: cachymod
[cachymod](https://github.com/marioroy/cachymod) is a CachyOS kernel
customization toolkit (TUI, build configs, and a patch set). Reviewed on
2026-09-15; nothing was adopted:
- `0280-prefer-idle-core` was **reverted by CachyOS itself**
  (`a4808133047d`), and its author calls it trial-and-error EEVDF tuning
  measured on a Threadripper 3970X (many CCDs) — this machine has one CCD.
- `0000-revert-prop-newidle-bal` reverts mainline `9fe89f022c05` ("More
  complex proportional newidle balance"), which is present in rc3, and it
  applies cleanly. Not adopted: the supporting measurement is a 6.18.5-era
  easyWave regression ("persists with 7.1-rc, though not as bad"), and
  upstream has since reworked that area (`b3a2dfa8b42e`, `c095741713d1`).
  Reverting it would be a permanent divergence from the scheduler mainline.
- `0300-x86-prevent-avx2-vector` adds `-mno-avx2 -fno-tree-vectorize
  -mpopcnt`. Not adopted: `CONFIG_MZEN4` selects `-march=znver4` and the
  kernel appends `-mno-sse -mno-avx` after it, and an audit of the linked
  vmlinux (disassembled, mapped through `/proc/kallsyms`) found all 3,089
  `ymm`/`zmm` instructions confined to 27 deliberate vector functions — the
  x86 crypto assembly (poly1305, chacha, sha1/sha256/sha512, crc32/crc64
  AVX2 and AVX-512) and the NAP governor's AVX2 neural-network predictor.
  None appear in compiler-generated generic code. cachymod's own configs
  leave the option off by default too (`_prevent_avx2:=no`).
- `0200-clearlinux-extras` is the Clear Linux patch set. Several entries are
  Intel-only (`itmt_epb`, `itmt2` ADL fixes, `epp-retune`); the rest are
  generic micro-optimizations with no target here. Modern CachyOS does not
  carry them either (its `clearlinux-5.18` branch was reverted).
- The remaining patches revert CachyOS scheduler modifications that this
  series never carried (`gaming-sched`, POC, `sched/fair` tunings), or belong
  to cachymod's own build framework (gnu17 switch, DKMS clang, 800 Hz tick
  option — this kernel runs `CONFIG_HZ=1000`).
- Config comparison: this kernel already matches or exceeds cachymod's
  defaults — THP `always`, `CONFIG_PREEMPT=y`, `CONFIG_HZ=1000`, plus BBR3.

### Sweep 2026-09-15 (evening)
- Nothing new in agd5f, drm-next, linux-pm, or the CachyOS branches today.
- **`next-20260915`**: its tree diff against `next-20260914` is 737 files
  (+42k/-12k). Nothing in it needs adding. Two commits checked by content:
  `aa55d949bf9f` is byte-identical to `f7491d7c81db`, the fix we already carry
  as `2500` (same author, same date, identical diff), and `eddf1f80667e` is our
  `2151`. *Method note:* `git log A..B` between two linux-next tags returns
  **1.47 million** commits, because the tags are rebased onto fresh bases daily
  — the commit list is meaningless. Use `git diff` for content and the tag's own
  merge commits for attribution; `git log` between tags produces a confident,
  wrong "delta". The hugetlb subpool accounting fix
  (`1ff1504af83d`) is unreachable here — `HugePages_Total` is 0, so nothing
  allocates from a hugetlbfs subpool. `228200f695c0` fixes Zen 5 TLB size
  reporting (a CPUID bit Zen 4 does not set). The block delta is entirely
  zoned-storage work, which this NVMe does not use.
- xswap had no v3 and no review replies at the time of the check.

### Housekeeping
- Removed the accumulated `*.pacnew` / `*.pacsave` files (13 of them, some
  from January) after diffing each against its live config; they are archived
  at `~/etc-pacnew-pacsave-20260915.tar.gz`. The live configs were the
  deliberate ones in every case (for example `resolved.conf` sets `FallbackDNS=`
  empty and `MulticastDNS=no`; `system.conf` sets `DefaultTimeoutStartSec=0s`).
- Removed four dangling systemd-boot entries (`linux-cachyos-cacule`,
  `linux-cachyos`, `linux-next`, `linux-sleepy`) whose kernels no longer exist
  on disk, via `sdboot-manage remove`. Three valid entries remain.
- `xswap-create.service` needed `DefaultDependencies=no` + `After=local-fs.target`:
  `systemd-analyze verify` found an ordering cycle (swap.target is ordered
  before sysinit.target, so a default-dependency service that is `Before=swap.target`
  deadlocks the graph and systemd deletes the swap.target job to break it —
  which would have silently skipped the unit at boot).

## [7.3.0-rc3-10-sleepy-next]: 2026-09-15

### Added
- **`9062`–`9071`** — Zhu Lingshan's "secure userq lifecycle by its kref"
  series (10 patches, amd-gfx, RESEND 2026-09-14,
  `<20260914130724.130794-2..11-lingshan.zhu@amd.com>`). A doorbell lookup
  helper that holds the queue kref, userq-manager lifetime tied to its
  queues, kref held in the gfx11/gfx12 private fault workers (our chip is
  the gfx12 one), asynchronous userq destruction, kref held across MES
  reset / isolation scheduling / suspend-resume, and create-path UAF fixes.
  Hardens the user-queue submission path that the 9000s backports ship.
  Still under review (the author pinged AMD on 2026-09-14); drop or refresh
  when the series lands in agd5f. Two of the ten patches apply only against
  our series-applied tree, not clean rc3 — the context comes from our
  existing userq backports.

### Sweep 2026-09-15
- **Upstream now — drop at the next bump**: `2148`/`2149` (crypto zstd
  init dedup) are in linux-next for 7.4 (`0db478c2e26f`, `57818119c9eb`);
  `2500` (x86/mm MADV_FREE-THP data loss) is in mainline x86_urgent
  (`f7491d7c81db`) and arrives with rc4.
- **Watch for 7.4**: amd-pstate per-SoC EPP tunings (linux-pm pull,
  2026-09-14) — the override table is empty for non-hybrid platforms, so
  Zen 4 keeps the legacy defaults; a no-op here, skip. The mqd_prop
  modify-flag series (v4, amd-gfx) depends on agd5f CU-mask work. Alex
  Hung's 66-patch DC series (KUnit tests, dcn42b power gating, MALL
  removal) heads for amd-staging. Jens Axboe's io_uring rsrc prefill and
  thread-identity RFCs. sirlucjan's zstd-dev-patches v3 (2026-09-14) —
  regenerate `2100` from it at the next bump instead of churning now.
- **Work items tracked, no fix referenced yet**: RX 9070 XT hard
  hang/reset deadlock (#5821), SMU bus loss (#5820), vblank-wait timeout
  (#5800), VRR black level over DisplayPort (#5812), HDMI FRL after
  standby (#5780).
- **Skipped**: ESMTP guest hardening (EPYC/SEV, not this machine), EROFS
  LZ4 rollback (not our filesystem), jitterentropy hardware mixer (watch
  only), Zen6 EPP tunings (wrong CPU).

### Changed
- `pkgrel` 9 → 10. Series is now 201 patches.

### Handmade-patch audit (0001–0049)
All 12 patches in the handmade range were checked against rc3 upstream code:
every one is still valid (applies and compiles in rc3-10) and still needed —
none of the fixes has an upstream equivalent yet. Notably `0001`'s `unsigned
tyep` typo and `0005`'s `// TODO` mode1-reset stub are both still in rc3
verbatim, and the `0031`/`0034` resource leaks are still present in rc3's
dcn401 code. `0055` (the local `drm_hdmi_vrr_cap` struct) stays: rc3 does not
define the field anywhere, and `1163`'s guard reads it.

## [7.3.0-rc3-9-sleepy-next]: 2026-09-15

### Fixed
- **VRR advertisement regression — the MAG251RX flicker bisect ends here.**
  The clean CachyOS 7.3 rc kernel (rc2-based) reports `vrr_capable=0` and
  `passive_vrr_capable=0` on both HDMI ports and does not flicker; our rc3
  line reported 1/1 and flickered at 240 Hz. Bisecting the diff between the
  two trees: the MSI MAG251RX EDID has an AMD VSDB **v1** (48–240 Hz, MCCS
  flag) and no HF-VSDB VRR block (`hdmi.vrr_cap.supported=0`), so the only
  path to `freesync_capable=true` is the AMD-VSDB parse plus the MCCS gate.
  Upstream `cfdcf5571c31` ("Consult MCCS FreeSync cap only if requested &
  supported", merged for rc3) moved the MCCS clear inside `if (do_mccs)`; the
  later `do_mccs=false` pass from `amdgpu_dm_connector_ddc_get_modes()` then
  re-advertises VRR on HDMI sinks whose MCCS VCP does not answer. rc2 (and
  cachy) cleared unconditionally and stayed at 0.
- **`1164`** reverts `cfdcf5571c31` (adapted to the 1163 form in the series),
  restoring the unconditional clear with the HF-VSDB VRR exemption kept.
  Result: `vrr_capable=0` + `passive_vrr_capable=0` on both HDMI ports, the
  VRR option disappears from cosmic-settings, and the runtime state matches
  the cachy kernel verified clean on this monitor.
- Box bug: the rc2→rc3 window carried zero DCN401/HUBP/clock-manager changes
  (verified by log), and CachyOS carries no extra DCN401 fix — the baked
  `amdgpu.dcdebugmask=0x800` (IPS power states off) remains the documented
  mitigation for the HUBP flip-pending artifact, unchanged in this release.

### Changed
- `pkgrel` 8 → 9. Series is now 191 patches.

## [7.3.0-rc3-8-sleepy-next]: 2026-09-14

### Added
- **`2011`** r8169: don't enable chip LTR when the platform has not enabled
  LTR (Yogesh Gaur, `[PATCH net v4]`,
  `<20260914130050.304-1-yogeshgaur.83@gmail.com>`). This machine's NIC.
  rc3's `rtl_hw_aspm_clkreq_enable()` calls `rtl_enable_ltr()` on every ASPM
  enable, gated only on `tp->aspm_manageable`, which says nothing about LTR;
  the PCI core's `pci_dev->ltr_path` verdict is never consulted. On platforms
  where LTR is not end-to-end the chip still programmes ALDPS_LTR_EN and can
  trigger L1.2 — the reported symptom class is link flaps and downshifts.
  Applies clean.

### From the sweep, deferred with reasons
- sched_ext lazy preemption v3 (Righi, for-7.4): a feature for the next
  window, not a fix for this base.
- MGLRU rejected-folios v3 (Baolin Wang): inert here — LRU-MARIE owns
  reclaim — and it needs a rebase past our eight `mm/vmscan.c` patches.
- Seven post-rc3 mm fixes (`12e9ac7bc5b2` SWAP_USAGE_OFFLIST_BIT,
  `6e673d0879ef` root-memcg charging, `397432cab17b` mremap locked_vm,
  `e384abeb559d` THP tuneables, `932cfb25e7ce` shrinker nokmem, plus two
  inert): all apply-tested clean upstream but arrive with the rc4 bump — no
  point carrying them for a day.
- amd-pstate 7.4 pull: a no-op for this machine — the `epp_soc_ids[]` table
  is empty and non-hybrid Zen 4 keeps the legacy defaults.

### Drop-list data for the next bump
- `2141`, `2145`, `2146` are now upstream in rc4.
- `2140`, `2144`, `2150`–`2154` are still akpm-only.
- `2500` is upstream in rc4 (`f7491d7c81db` via `x86_urgent_for_7.3-rc4`).

## [7.3.0-rc3-7-sleepy-next]: 2026-09-14

### Removed
- **`0055` and `0060`** — `0055` (drm/edid: parse HDMI 2.1 gaming ALLM/VRR capabilities from
  HF-VSDB). The decisive bisect step for the 240 Hz flicker, and the first one
  grounded in a value difference, not a guess.

  Captured from the flicker-free cachyos-rc kernel at runtime: `vrr_capable=0`
  and `passive_vrr_capable=0` on **every** connector, so cosmic-settings offers
  no VRR option at all. Ours advertised `vrr_capable=1` on both HDMI outputs.
  `0055` is the patch that creates that advertisement: its
  `drm_parse_hdmi_gaming_info()` sets `vrr_cap.supported=true` from the
  HF-VSDB VRR range in the MAG251RX's EDID. CachyOS's tree carries the
  `drm_hdmi_vrr_cap` struct but never sets the flag.

  The chain that follows from the advertisement: our `0060` (dropped in the same build) had a fallback that set
  `freesync_capable=true`, the driver sends FreeSync signalling to a G-Sync
  Compatible panel whose scalar then sits in a half-negotiated VRR state —
  flicker at 240 Hz where content changes (cursor movement), and the box, whose
  old symptom was that it moved to whichever monitor last had VRR toggled.

  Without `0055`, the advertisement is gone, `0060`'s fallback becomes inert,
  and the whole chain matches the known-good kernel. VRR over HDMI disappears
  as a feature; that is the accepted trade for this machine, and it matches
  the stock kernel's behaviour exactly.

  *Correction (rc3-9):* this hypothesis was wrong — dropping `0055`/`0060`
  did not zero the chain (`vrr_capable` stayed 1). The actual cause was
  upstream `cfdcf5571c31`, fixed by `1164`; see the rc3-9 entry.

### Added
- **`1163`** drm/amd/display: keep `freesync_capable` for HF-VSDB VRR sinks in
  the MCCS fallback. A rebase of Fangzhi Zuo's upstream submission
  `<20260901191251.2653684-4-jerry.zuo@amd.com>`, which this series carried as
  patch `1145` until the rc3 rebase dropped it on the assumption that rc3's
  rewrite of `amdgpu_dm_update_freesync_caps()` superseded its purpose.

  The rewrite restructured the function but kept the MCCS clear without the
  `vrr_cap.supported` term — and the kernel-to-kernel diff against the
  flicker-free CachyOS `7.3/base` tree shows they carry exactly that guarded
  version. The user's test on `pkgrel 6` exonerated both `1144` and `0030`, and
  this is the next bisect step with the strongest evidence yet:

  - The MAG251RX is a G-Sync Compatible panel: its EDID carries a FreeSync VCP
    code and an HF-VSDB VRR range. Its MCCS does not answer the AMD VCP read.
  - Without the guard, the rc3 code clears `freesync_capable` for exactly this
    sink, so the driver stops FreeSync signalling while the monitor's
    Adaptive-Sync OSD stays on — the panel sits in a half-negotiated state that
    flickers, worst where content changes (cursor movement) and worst at
    240 Hz timing.
  - The guard skips the clear for `vrr_cap.supported` sinks, keeping the
    HF-VSDB fallback alive.

### The bisect record
- `pkgrel 6` was tested: **`1144` and `0030` are exonerated** — the flicker
  persists with both dropped. Recorded rather than quietly extended.

## [7.3.0-rc3-6-sleepy-next]: 2026-09-14

### Removed
- **`0030`** (handmade: proactively shrink DET for pipes losing space). The
  second bisect step for the 240 Hz flicker, dropped in the same build as
  `1144`. `0030` patches `dcn401_prepare_bandwidth()` — the DCN401
  bandwidth-transition function that programs watermarks, the arbiter, compbuf
  and DET before a clock update — and immediately programs a smaller DET size
  for pipes that are losing space, *before* the pipe stops scanning at its old
  requirements. That transient can underflow the pipe's DET buffer and the
  shared CRB: visible at 240 Hz timing margins, invisible at 144 Hz, and
  triggered exactly by cursor-driven surface updates, which set the
  `det_size` update flag on pipes. CachyOS does not carry it.

  The identification came from the kernel-to-kernel diff the bisect demanded:
  our applied display tree against CachyOS `7.3/base` shows 32 differing
  files, and the DCN401 hardware-sequencer difference is this patch alone —
  everything else in `dcn401_hwseq.c` is identical between the two trees.

  Two variables are changed in this build (`1144` and `0030`). If the flicker
  is gone, a follow-up build can re-add one of them to isolate; if it
  persists, both are exonerated and the next suspect is the baked command line
  (`cpuidle.governor=nap`).

### Changed
- **The kbuild build-speedup series is upgraded from v1 to v2**
  (`20260914-build-speedup-v2-0-39817ec5db23@kernel.org`, 21 patches,
  replacing the v1 content on the same numbers `2302`–`2322`). v2 drops two v1
  patches (the modpost srcversion hashing and its source-per-file companion),
  adds two (the toolchain checks moved into `init/Kconfig.toolchain`, and
  objtool sizing its instruction hash to the text), and refreshes the rest with
  the review feedback from the v1 thread. Renumbered in v2 order. The whole
  189-patch series still applies cleanly, and this is build-time only, so the
  runtime behaviour is unchanged from `pkgrel 5`.

### Noted, nothing to add
- **The Vernon Yang link** (`20260903031608.1194238-1-vernon2gm`) is a reply on
  the thread of our `2500` (x86/mm `pmd_modify()` dropping the dirty bit) — it
  just accepts the `Reported-by:` trailer Andrew Morton added. No new patch.
- **linux-next `next-20260914` is out**, and it is the 7.4 merge-window preview
  (455 display files changed, 33k insertions; mm +5.4k lines). Per this
  project's policy linux-next is a preview base, not a patch source mid-RC.
  The only delta in `crypto/zstd.c` is the workspace series already carried as
  `2148`/`2149`. Nothing worth backporting onto 7.3-rc3.

## [7.3.0-rc3-5-sleepy-next]: 2026-09-14

### Removed
- **`1144`** (drm/amd/display: Enable HDMI FRL by default). This is a bisect
  step aimed at the MSI MAG251RX 240 Hz flicker, not a value judgement on the
  patch itself.

  The evidence chain that made it the first variable to test:

  - The user A/B-tested: the cachyos-rc kernel (rc2-based) is flicker-free at
    240 Hz, this kernel flickers, and 144 Hz works. Something in this kernel's
    delta is the cause.
  - Captured from the good kernel: `amdgpu.dcfeaturemask=2`. Ours was `0x402`.
    The extra bit is `DC_FRL_MASK`, added by this patch.
  - CachyOS reverted the same change twice in their 7.3 branches
    (`cc29db585c84`, `143e44f57bf8`), both by their maintainer with no reason
    stated, and the change is implicated in open upstream work item #5649
    (HDMI FRL blanking).

  Ruled out before this move: rc3's display commits versus rc2 (all benign), the
  FRL status-polling workqueue (inert without a trained FRL link), FBC (off on
  both kernels), the display driver configuration (identical between the two
  kernels apart from the command line and the NAP governor), and passive VRR
  (the good kernel has it *on* and is fine, so it cannot be the cause).

  Dropping the patch restores the upstream default mask of exactly 2, the
  known-good value. If the flicker persists on this build, the next suspect is
  the baked command line (`cpuidle.governor=nap`).

## [7.3.0-rc3-4-sleepy-next]: 2026-09-14

### Changed
- **`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is back in the baked command
  line.** It was removed in `pkgrel 11` because the display "box" turned out to
  be a COSMIC overlay-plane bug rather than an IPS one. That is still true of the
  box — but the IPS gap is a separate, real artifact, and this machine shows it.

  `dc_get_flip_pending_on_otg()` reads `hubp2_is_flip_pending()`, which returns
  false while the HUBP is clock-gated, so flip completion can be delivered
  before the hardware latches and the compositor repaints a buffer that is still
  being scanned. Leo Li's own comment in `f64a9be56536` concedes it: *"DCN HUBP
  may be clock-gated, so the flip-pending status may be undefined"*.

  The MSI MAG251RX flickers exactly where that bites. Cursor movement is the
  most frequent source of flips, which is why the artifact is severe under the
  cursor and mild when idle, and why it is **independent of VRR** — every VRR
  knob, including disabling passive VRR, changed nothing. `1159` fixed the
  software half of the race (the non-atomic read-modify-write that clears
  `VUPDATE_NO_LOCK_EN`); this mask covers the clock-gating half, which is
  hardware. It costs idle power, and should be dropped again if a proper DCN4
  flip-pending fix lands.

  **This is a hypothesis under test, not a proven fix.** The passive-VRR
  diagnosis in `pkgrel 2` was wrong: the fix applied cleanly — both CRTCs read
  `PASSIVE_VRR_DISABLED=1` — and the flicker persisted. Two related things were
  established while re-diagnosing: the MSI runs 1920x1080@239.96Hz at a 571 MHz
  pixel clock on HDMI-A-2 (legal against HDMI 2.0's 600 MHz TMDS ceiling, but
  near the top of it), and the kernel logs **no runtime display errors at all**.
  The only complaints are at boot: a `REG_WAIT` timeout in
  `optc401_disable_crtc`, and an InfoFrame failure on HDMI-A-1 — the *other*
  monitor, not the MSI.

## [7.3.0-rc3-3-sleepy-next]: 2026-09-14

### Added
- **Nineteen fixes from the multi-source sweep**, every one apply-tested against
  the full series before being added. Series: 172 -> 191 patches. Twelve are
  display and GPU core (below), eight are subsystem fixes (further down).
  - **`1159`** drm/amd/display: atomize IRQ register read/modify/write ops. The
    upstream fix for a non-atomic read-modify-write on `OTG_GLOBAL_SYNC_STATUS`
    that can clear `VUPDATE_NO_LOCK_EN`. That is the same mechanism as this
    machine's `flip_done` timeouts and the display artifacts recorded in
    `LESSONS.md`, and it matters most on high-refresh panels.
  - **`1161`** drm/amd/display: guard NULL DDC pins in `dal_ddc_open`, a hard
    wedge when a NULL pin meets `+0x28` (upstream issue #5716).
  - **`1162`** drm/amd/display: check `dc_state_create_copy()` for NULL in
    `dm_suspend`.
  - **`1064`** drm/amdgpu: don't release the fence reference the scheduler
    consumed — a cross-thread use-after-free in `amdgpu_vm_sdma_update()`.
  - **`2403`** drm/sched: do not restore unsaved virtual runtime (Tvrtko
    Ursulin, `Cc: stable`).
  - **`9055`**, **`9056`** drm/amdgpu/userq: a `userq_signal_ioctl` hang inside
    `drm_exec_until_all_locked()`, and filtering idle userqs out of the pending
    signal list.
  - **`9057`** drm/amdgpu: keep freed VM mappings on clear failure (`Cc:
    stable`).
  - **`9058`** drm/amdgpu: hold a runtime PM reference for P2P dma-buf
    attachments (`Cc: stable`).
  - **`9059`**, **`9060`** drm/amdkfd: don't gate userptr cleanup on the owning
    mm, and skip migration when the fault window is already in VRAM.

### Also added — eight subsystem fixes
- **`2009`** fs/buffer: check for a NULL pointer before
  `folio_test_dropbehind()`. The most severe find of the sweep: `bh->b_folio`
  is dereferenced unguarded, and jbd2 submits buffer heads with no folio — a
  NULL-dereference panic on the ext4 journal commit path, which is this
  machine's root filesystem. Crash reported on 7.3.0-rc2-next; the culprit
  commit is in rc3.
- **`2152`** khugepaged: hold `invalidate_lock` across `collapse_file()`
  readahead. A syzbot-reported deadlock between collapse and truncate,
  reachable in about 20 seconds under a collapse/truncate race.
- **`2150`** mm/huge_memory: fix pgtable withdrawal for huge zero PMDs, a NULL
  dereference on `munmap()` (`Cc: stable`).
- **`2154`** mm/page_alloc: apply the per-task GFP context in the bulk
  allocator, so `PF_MEMALLOC_NOIO`/`NOFS`/`PIN` are honoured (`Cc: stable`).
- **`2153`** writeback: report a Tasks-RCU quiescent state per cgwb drain pass.
  Without it any `synchronize_rcu_tasks()` under `PREEMPT_LAZY` can stall for
  minutes and trip the hung-task detector (`Cc: stable`).
- **`2151`** mm/shmem: ignore sysfs configs for forced collapse, restoring the
  documented `MADV_COLLAPSE` behaviour (`Cc: stable`).
- **`2010`** blk-cgroup: save IRQ state in `blkg_tryget_closest()`, where an
  unconditional `spin_unlock_irq()` could re-enable interrupts under a caller
  holding the lock with `spin_lock_irq()`.
- **`2404`** sched_ext: close the pre-enable ops error claim window — a
  use-after-free in `kernel/sched/ext/ext.c` (`Cc: stable`). Worth having
  because this machine actually runs sched-ext (`scx_cake`), and unlike the
  `fair.c` patches this one is **not** inert under full-switch mode.

### Not carried
- **`1160`** drm/amd/display: only allow freesync on a `VRR_ENABLED` crtc. The
  most conceptually interesting find: it addresses the same condition as the
  passive-VRR fix in `pkgrel 2` from the other side, by refusing to let
  VRR-capable sinks set `allow_freesync` while `VRR_ENABLED=0` — the path that
  lets FPO stretch frames during UCLK switches. Three hunks apply; the fourth
  fails because the author's tree has `dc/dml2_wrapper/dml21_wrapper/` while
  rc3 has `dc/dml2_0/dml21/`, and that file's content differs around the hunk
  too. Deferred rather than hand-rebased.
- **`9061`** drm/amdkfd: fix a TCP XNACK scoreboard reset race. It applied
  cleanly but **failed to compile**: its new `gfx_v9_4_2_run_shader()` call
  passes 11 arguments while rc3's definition takes 10, so the patch depends on
  a signature-changing prerequisite that is not in v7.3-rc3. Dropped for that
  reason, not for irrelevance. This is the "applies but does not belong" case
  the cumulative-apply check cannot catch — only a build can.
- **`2155`** mm/zswap: return `-ENOENT` when the swap device is gone. Two hunks
  fail against the current series.
- **sirlucjan's full zstd dev update.** Asked for explicitly, and the answer is
  no: it is a 1.5.7 → 1.6.0 vendored sync whose only x86-relevant deltas are
  already our `2128` and `2143` — and it **conflicts with both**, so carrying it
  would mean dropping them. Its bulk is ARM SVE2 and RISC-V RVV code that
  cannot execute on Zen 4, and its gcc workaround is inert under Clang.
- **CachyOS `sched/fair: do not scan twice in detach_tasks()`.** `fair.c` is
  inert here: sched-ext full-switch mode gates the CFS balance path.
- **CachyOS `finish_task_switch()` always-inline.** Evaluated before and
  rejected: the quoted 34.8% figure is for spectre_v2 retpolines, while this
  machine reports Enhanced/Automatic IBRS, leaving under 0.3% end to end.
- **`mm, swap: extendable swap devices (xswap)`, v2 12-patch series.** Applies
  cleanly, but it is a feature, not a fix, on a subsystem this machine does not
  need extended (zram swap).
- **`nvme: bump genctr when cancelling a request`.** Directly on the Phison E16
  reset path, but v1 with no `Fixes:`, no `Cc: stable` and no acks.
- **maple_tree range64 RCU pointer corruption.** Genuine memory corruption, but
  v1, unreviewed, with no `Fixes:` or `Cc: stable`. Worth re-checking after
  maintainer review.
- `repos/drm-misc` could not be refreshed (every fetch fails with HTTP 503
  during the `acknowledgments` phase), so drm-misc is the one source this sweep
  could not cover.

### Decision recorded — `1144` is kept
The MAG251RX is **HDMI 2.0 and DP 1.2a**, so `1144` ("Enable HDMI FRL by
default") is inert on the hardware: FRL is an HDMI 2.1 feature. It is
bit-identical to the change CachyOS reverted with no stated reason, and it is
implicated in open upstream work item #5649 (HDMI FRL blanking). Removing it
was considered and **declined on 2026-09-14**: being inert, removing it buys
nothing measurable today, and the 7.4 bump replaces this area with drm-next's
reworked VSDB/FRL handling anyway. Revisit then rather than re-arguing it.

### Open question (not acted on)
- The sweep flagged that `CLAUDE.md` lists `DCN42B` as a Navi 48 identifier and
  claimed it is really GC 11.5.0 with the DCN4A SoC variant B. `DCN_VERSION_4_2B`
  does exist as its own variant in `dal_types.h`, but that mapping could not be
  confirmed from the source here, so the hardware table is left alone and the
  question is recorded rather than resolved.

## [7.3.0-rc3-2-sleepy-next]: 2026-09-14

### Fixed
- **The MSI MAG251RX flicker.** That panel, running 1920x1080 at 240 Hz over
  HDMI, flickered continuously and became close to blank under cursor movement.

  The cause was **passive VRR**. It is the feature that keeps a sink in its
  variable-refresh state during fixed-refresh desktop use, and it is **opt-out**:
  patch `1150` defaults it on for every connector that advertises
  `passive_vrr_capable`, and patch `1151` drives `stream->freesync_on_desktop`
  from the inverse of that flag, so the driver keeps the FreeSync-Active bit set
  on the desktop even when VRR is switched off. The panel was therefore never in
  fixed-refresh mode. Cursor movement makes the compositor repaint, the frame
  interval swings, and the panel follows — which is why idle flicker was mild and
  cursor use was severe.

  It also explains why toggling VRR in COSMIC never helped: that control moves
  `VRR_ENABLED`, which is a different property from `PASSIVE_VRR_DISABLED`.
  Both outputs read `VRR_ENABLED=0  PASSIVE_VRR_DISABLED=0`.

  Fixed by inverting the default: the pristine CRTC state in
  `drm_atomic_helper_crtc_state_init()` now sets `passive_vrr_disabled = true`,
  so passive VRR is opt-in on this machine. The property stays exposed and
  writable, so a userspace that does want desktop passive VRR can still set
  `PASSIVE_VRR_DISABLED=0` on the CRTC.

  This is a deliberate local deviation from the upstream series, recorded in a
  `[sleepy]` block in patch `1150`'s commit message.

## [7.3.0-rc3-1-sleepy-next]: 2026-09-13

### Changed
- **Base moved to Linux 7.3-rc3.** `pkgrel` restarts at 1, and the series drops
  from 176 patches to 169.

### Removed
- **Ten patches that rc3 merges upstream**: `1155`–`1157` and `1153` (the HDMI
  RGB quantization series and its VTEM companion), `2300` and `2301` (kbuild
  `mksysmap`), `2401` and `2402` (the EEVDF fixes), `2501` (AMD MCE threshold
  interrupts) and `2600` (hrtimer). Each was confirmed present in a pristine
  rc3 tree by checking that the lines it adds are already there.
- **`1145`** (the HF-VSDB MCCS FreeSync guard). rc3 rewrites
  `amdgpu_dm_update_freesync_caps()`, so the block the patch guarded no longer
  exists — it cannot be rebased without re-authoring it, and the rc3 code
  supersedes its purpose.

### Added
- **Four memory-management fixes**, each verified to apply on top of the whole
  series:
  - **`2144`** xarray: fix the index jumping backwards in `xas_find()`. A syzbot
    use-after-free: the index moves backwards while a multi-index entry is
    concurrently split, and `filemap_map_pages()` then dereferences a page-table
    page already freed through `tlb_remove_table_rcu()`.
  - **`2145`** mm/vma: unaccount correctly when `mmap_prepare()` fails, which
    otherwise leaks security accounting over the `RLIMIT_AS` budget. The
    regression source is in the base tree.
  - **`2146`** mm/mlock: use the IRQ-safe accessor for `NR_MLOCK` in
    `__munlock_folio()`, where a bio-completion softirq can corrupt the counter.
  - **`2147`** mm/memcg: clear the folio's memcg after updating the per-memcg
    stats, so the swapcache counter stops drifting. This machine swaps
    constantly, so its `memory.stat` was reporting swapcache that had already
    gone.

### Fixed
- **The patch files themselves**, following the provenance audit:
  - the `Cc:` label restored in the 23 kbuild patches, where a stripped field
    name had left a 36-line address list orphaned under `Message-Id`;
  - mail-transport headers stripped from `2138` and `2400` (15 and 63 lines),
    completing an earlier strip that had left debris behind;
  - 43 files had a placeholder or fabricated value in their `From <id> Mon Sep
    17` slot replaced with `nobody`, so no false commit id remains anywhere in
    the series;
  - 28 files gained the `Message-ID` of their original submission, recovered
    from the lore git mirrors;
  - 16 files had their commit-message body restored from the original mail,
    which also restored the `Signed-off-by` they were missing.

### Verified
- The 169-patch series applies to a pristine `v7.3-rc3` tree with 0 failures and
  0 silently skipped patches (cumulative `patch -p1 --forward -F2`).

### Evaluated and not carried
- **`drm/amd/display: Try RGB before YCbCr 4:4:4 in stream validation`**
  (Adrian Betschart, dri-devel 2026-09-11). Its `amdgpu_dm_connector.c` hunk
  applies, but both hunks in the KUnit file fail, and that file is not built
  here. Carrying an extracted subset would mean shipping a behaviour change to
  stream validation — an ordering preference rather than a bug fix — so it is
  deferred rather than forced.
- **`drm/amd/display: invalidate DP CEC state on s3 suspend`** (Dan Himebauch,
  dri-devel 2026-09-12, reported tested on an RX 9070 XT). The mail is
  MIME-encoded and did not survive conversion intact. CEC is not used here, so
  it is deferred.

## [7.3.0-rc2-11-sleepy-next]: 2026-09-13

### Changed
- **`amdgpu.dcdebugmask=0x800` is gone from the built-in command line.** It was
  carried from August to mask a display artifact by disabling DCN4 idle power
  states, on the theory that IPS/DPG pipe-gating made `dc_get_flip_pending_on_otg()`
  misread a pending flip. That theory is disproved: the artifact is a COSMIC
  compositor bug (see `7.3.0-rc2-10`), and it reappeared while the mask was
  still in effect. The mask cost idle power. Re-add it if `flip_done` or vblank
  timeouts appear — the gap Leo Li documents in `f64a9be56536` is real, just not
  this machine's failure mode. The `pcie_aspm=off`, `amdgpu.aspm=0` and
  `amdgpu.runpm=0` stopgaps stay, because the drm/amd !5538 SMU bus-drop is
  still unfixed upstream.
- **The dead `--set-str DEFAULT_IOSCHED "kyber"` line is removed.** The symbol
  no longer exists (it went with the blk-mq rework), so `olddefconfig` discarded
  it silently. The NVMe scheduler is set by udev's
  `60-ioschedulers.rules`.

### Added
- **`2143`** — zstd: fix a DDict hash-set probe index wrap-around. An
  out-of-bounds write in vendored code: `ZSTD_DDictHashSet_emplaceDDict()`
  advances the probe index with `idx &= idxRangeMask; idx++;`, which leaves
  `idx == ddictPtrTableSize` when the probe starts on the last slot. Reachability
  here is low, because the DDict hash set needs multi-dictionary streaming
  decompression while zram and zswap use dictionary-less contexts.
- **The `kernel-verify` skill**, a tiered verification suite: patch hygiene,
  checksums, provenance, documented claims, skill-spec compliance and dangling
  symlinks in the fast tier; the cumulative apply in the series tier;
  `checkpatch`, `sparse`, `coccinelle` and `W=1` in the deep tier. A missing
  tool is reported as a `SKIP` with its reason, never as a silent pass.

### Fixed
- **`2138` and `2400` carried mail-transport headers**: 64 and 43 lines of
  `Return-Path`, `X-Spam-Checker-Version`, `Received` and `ARC-Seal`. Stripped.
  The diff bodies are byte-identical and the `Message-ID` is preserved.

## [7.3.0-rc2-10-sleepy-next]: 2026-09-13

### Added
- **Ten upstream fixes** from the distro-patchset and stable sweep. Eight carry
  `Cc: stable`; two are `mm-new` material.
  - **`1061`** drm/ttm bulk_move — a use-after-free. `ttm_tt_swapout()` returns a
    page count, but `ttm_bo_swapout_cb()` gates its bookkeeping on `if (!ret)`,
    so swapped-out resources never leave their bulk_move range and an endpoint
    is left dangling (`Closes` drm/amd#5387). Carried as the one-hunk original,
    *not* the botched merge `3db7d7d58341`.
  - **`1062`**, **`1063`** dma-fence — a use-after-free in which most amdgpu and
    drm_sched fences lose RCU protection after signalling, plus its doc
    companion.
  - **`2006`**, **`2007`** zram and zsmalloc — convert to the SG-list object read
    API. This machine runs zram-on-zstd swap, so it saves CPU per decompress.
  - **`2008`** io_uring — a single `IORING_ASYNC_CANCEL_ONE` cancelled in both
    the bounded and unbounded accounts, killing an unrelated operation.
  - **`2141`** mm/filemap — retain mapped dropbehind folios. Also fixes a
    sleeping-in-atomic warning on the `fadvise(DONTNEED)` path.
  - **`2142`** mm/vmscan — stop splitting mTHPs when swap is exhausted, that is,
    when zram is full. Splitting cannot make progress and only destroys the huge
    page.
  - **`2501`** x86/MCE/AMD — threshold interrupts were enabled when a storm
    started and disabled when it ended, which is backwards. The culprit commit
    is in rc2.
  - **`2600`** hrtimer — rearming a queued timer with slack left the timerqueue
    mis-sorted, so the next event could fire before the head's hard expiry.
    Mistimed wakeups affect compositor timers, `timerfd` and `poll`/`epoll`,
    that is, frame pacing.

### Changed
- **New patch range `2600–2699`** for time and timers.

### Fixed
- **The display artifact ("the box") is fixed outside the kernel.** The
  rectangular artifact over application windows was misattributed to the kernel
  from August. Three traits identified it as a COSMIC (`cosmic-comp`) bug:
  screenshots never showed it, moving the cursor over it dismissed it, and it
  appeared on whichever monitor last had VRR toggled. The compositor was handing
  fullscreen content to an overlay plane. Either setting below clears it; add
  one to `/etc/environment` and log in again.

  ```
  COSMIC_DISABLE_OVERLAY_SCANOUT=1     # sufficient on its own
  COSMIC_DISABLE_DIRECT_SCANOUT=1      # also works; removes the overlay bit too
  ```

  No kernel change is involved. The `dcdebugmask=0x800` workaround that fixed
  this in August and then stopped working was the signal that the cause had
  changed. The evidence chain is in `LESSONS.md`.

## [7.3.0-rc2-9-sleepy-next]: 2026-09-13

### Added
- **`1158`** — DMCUB busy-wait fix (Sultan Alsawaf, `dfd0e5aa6aad`).
  `dmub_srv_wait_for_idle()` polls with `udelay(1)` in a loop bounded by
  `timeout_us`, and callers pass up to 100000 — as much as 100 ms of CPU
  spinning per call, on the DMCUB path DCN401 uses. Replaced with progressive
  backoff using `usleep_range()` when `preemptible()`, so the CPU can reach
  idle. Out-of-tree, so it will not arrive on a version bump; it is a
  self-contained function, which keeps the carry cost low.

## [7.3.0-rc2-8-sleepy-next]: 2026-09-13

### Added
- **HDMI RGB quantization fix (`1155`–`1157`)** — Satyajit Roy's
  `[PATCH 0/3] drm/amd/display: Fix HDMI RGB quantization updates`. Post-rc2
  upstream work. `resource_build_info_frame()` derives colorimetry and RGB
  quantization from `stream->output_color_space`, but the InfoFrame-update
  predicates did not include `output_color_space`; a commit that changes the
  colour space therefore reprogrammed the output CSC while the sink kept the
  previous AVI InfoFrame range, leaving source and sink disagreeing about RGB
  limited-versus-full range. `1157` adds the missing predicate at the three
  sites in `dc/core/dc.c`. Prompted by drm/amd work item **!5812**, which
  reports on an RX 9070 XT (DCN401) that toggling Adaptive Sync raises or clears
  washed-out colour every time — the same VRR-toggle trigger this machine shows.
  The desync is screen-global, so this is carried as an on-target correctness
  fix, not as a confirmed cure for the artifact.
- **Five upstream fixes** from the MM/PM/sched sweep:
  - **`2139`** mm/vmscan — avoid anon scanning for `GFP_NOIO` with low swapcache.
    Explicitly a zRAM optimisation, and live here: it uses the
    `vmscan_can_reclaim_anon_pages()` wrapper LRU-MARIE adds.
  - **`2140`** mm/page_alloc — avoid direct compaction for costly `__GFP_NORETRY`
    allocations, which removes a cross-CPU drain-IPI storm on the buffered-write
    path. Its regression source is in rc2.
  - **`2401`**, **`2402`** sched/eevdf — fix the augmented `max_slice`, and fix
    rbtree corruption where only one of three augmented fields propagated.
  - **`2500`** x86/mm — a one-line data-loss fix: `pmd_modify()` masked out
    `_PAGE_DIRTY` where `pte_modify()` and `pud_modify()` do not, so pages
    rewritten after `MADV_FREE` on a PMD-mapped THP could be discarded.

## [7.3.0-rc2-7-sleepy-next]: 2026-09-12

### Changed
- **The repository became single-package.** The root 7.2 `linux-sleepy` package
  was dropped, and `linux-sleepy-next` in `sleepy-next/` became the only
  package. Two couplings had to be cut first: its `prepare()` read `../config`,
  and it deliberately did not install `net-tune` because the 7.2 package owned
  it.
- **`linux-sleepy-next` now ships `net-tune`** (CAKE SQM plus low-latency
  ethernet tuning) and enables the service. The shipped template defaults to
  `ENABLE_SQM=yes` at 80/80 Mbit, so an unattended build installs shaping rather
  than silently disabling it. Set your real line rate in `/etc/net-tune.conf`.
- **`/etc/net-tune.conf` is now a pacman backup file.** Without `backup=()`,
  pacman would overwrite local edits on every kernel upgrade, which matters now
  that the service ships enabled with a placeholder line rate.

### Added
- **MGLRU v3 (`2131`–`2137`)** — Barry Song's `mm/mglru: speed up inc_min_seq()
  and fix cold/hot inversions`, from akpm's `mm-unstable`. Batches the per-folio
  work in `inc_min_seq()` and fixes hot/cold inversion by keeping promoted
  folios ahead.
- **`2138`** — memcg: trim the per-cpu charge stock instead of draining it,
  splitting the high watermark from its emptying target.
- **`2400`** — sched: set the need-resched flags before tracing. The unpatched
  order emitted the tracepoint before setting the `TIF` bit, so a BPF tracepoint
  program could recurse through `rcu_read_unlock_special()` into a kernel stack
  overflow. Relevant here, because this package ships `bpftune` and runs
  sched-ext.

### Removed
- **The dangling ADIOS config.** `PKGBUILD` ran `scripts/config -e
  MQ_IOSCHED_ADIOS`, `config` set `CONFIG_MQ_IOSCHED_ADIOS=y`, and `provides=()`
  listed `ADIOS-MODULE`, but no patch adds `block/adios.c`, so `olddefconfig`
  dropped the symbol and the package advertised a module it did not ship.

### Changed
- **New patch range `2400–2499`** for the core scheduler.

## [7.3.0-rc2-6-sleepy-next]: 2026-09-12

### Changed
- **LRU-MARIE updated to the author's official 0.11.1 port for 7.3.** firelzrd
  ships `patches/testing/0001-linux7.3-rc1-lru_marie-0.11.1.patch`, an
  author-written port that applies cleanly to this base. It supersedes the
  hand-rebased 0.11.0, which needed a "legacy writeout" shim to re-provide the
  per-folio swap helpers that 7.3 deleted; the author instead adapts MARIE to
  the native `swap_ops.h` and `swap_io_ctx` path. Two build-artifact sections
  the patch bundled (`localversion`, `scripts/setlocalversion`) were stripped.

## [7.3.0-rc2-5-sleepy-next]: 2026-09-10

### Added
- **The final pieces of AMD's Linux 7.4 HDMI 2.1 pull (`1152`–`1154`).** The
  core was already carried (`0059` HDMI 2.1 FreeSync, `0060` HDMI 2.1 VRR,
  `0061` ALLM, `1144` FRL by default, `1150`/`1151` passive VRR); this adds emit
  VTEM for HF-VSDB VRR on TMDS links, fix HF-VSDB DSC bpc detection to be
  cumulative, and fix a NULL dereference of `new_stream->sink` in the VTEM
  guard.

## [7.3.0-rc2-4-sleepy-next]: 2026-09-09

### Added
- **Passive VRR (`1150`, `1151`)** — Tomasz Pakuła's passive VRR series. Keeps
  the sink in its variable-refresh state during fixed-refresh desktop use,
  avoiding the blanking and flicker HDMI sinks show on VRR entry and exit. Part
  3/3 is the HF-VSDB MCCS fix already carried as `1145`. The author header was
  de-MIME-encoded to the proper UTF-8 name.

## [7.3.0-rc2-3-sleepy-next]: 2026-09-09

### Removed
- **The two DCN4 flip-schedule patches (`9051`, `9052`).** AMD is reverting both
  upstream for causing a regression: `Revert "drm/amd/display: Fix
  CalculateFlipSchedule Calculation"` and `Revert "drm/amd/display: Unify
  CalculateFlipSchedule Logic"`, each stating *"Because it causes some
  regression"*. Both land in `dml2_core_dcn4_calcs.c`, which is DCN4 — this GPU.
  The un-reverted "fix" makes the flip-bandwidth math more conservative, by
  adding `meta_row_bytes` and halving `row_time_budget`, which mis-schedules
  flips.

### Added
- **The kbuild build-speedup series (`2300`–`2322`)** — Lorenzo Stoakes'
  `[PATCH 00/23] kbuild: significantly speed up kernel builds`. Up to 36% faster
  full builds and about 90% faster no-op builds, which matters for this
  project's build loop. All 23 apply cleanly.

### Changed
- **New patch range `2300–2399`** for the build system.

## [7.3.0-rc2-2-sleepy-next]: 2026-09-07

### Changed
- **Moved off the linux-next snapshot line onto Linux 7.3-rc2 (mainline).** The
  post-rc1 linux-next bases (0902 and 0904) carried unfixed upstream RDNA4
  display bugs that froze and panicked this RX 9070 XT: drm/amd work items
  #5722 (`duplicate_state` panic), #5684 (optc `REG_WAIT` hang) and
  #5759/#5763 (MES wedge). rc2 sidesteps the linux-next mm churn and is the
  actual release-candidate line.
- **LRU-MARIE 0.11.0 ported to rc2.** The `mm/lru_marie/` subsystem stays
  byte-identical to firelzrd's 0.11.0, apart from the three earlier one-line
  compile fixes for the base API. The three host-file hooks were re-anchored to
  rc2's renamed and simplified code.
- **Series reconciled for rc2**: 121 patches. Dropped 19 that linux-next 0902 to
  0904 merged upstream, the retry-fault, flip-schedule and userq groups that
  also landed, `1059` (merged in rc2) and `1139` (code changed).
- **VRR fix in `pkgrel 2`.** The local `1137` — a hand-rolled MCCS VCP re-enable
  that force-enabled VRR from the kernel-parsed AMD VSDB — was replaced with
  Fangzhi Zuo's upstream `1145`, which skips the MCCS `freesync_capable` clear
  when the sink advertises HF-VSDB VRR. VRR now engages the way AMD intends
  rather than through a local hack.

### Fixed
- **The recurring freezes and the boot NULL-oops were upstream RDNA4 display
  bugs in the 0902+ linux-next bases**, not this series. Reproduced on a stock
  CachyOS release kernel and matched to open upstream work items.

## [7.3.0-rc1-13-sleepy-next-20260902]: 2026-09-02

### Added
- **LRU-MARIE 0.11.0 carried verbatim**, byte-identical to firelzrd's patch,
  with only two compile-fix lines and a clearly separated legacy-writeout shim
  that re-provides the per-folio swap helpers linux-next deleted.

### Changed
- Base bumped to linux-next `next-20260902`. The series dropped 11 patches
  merged upstream (CLIFF FRL cap and restore, HPD filter, FRL link-training
  timeout, overlay cursor, dw estimate, no-retry PTE, flip-schedule fixes,
  clamp-dcfclk, sched-ext DSQ and unify-flip-schedule), and three were rebased.
  Series: 112 patches.

## [7.3.0-rc1-12-sleepy-next-20260901]: 2026-09-02

### Added
- **LRU-MARIE 0.11.0 ported to the linux-next base**, replacing the version that
  never applied. MARIE is a memory-reclaim accelerator: a per-PFN reclaim-state
  byte array, a SIMD young-bit walker, and a `kcompressd` async-compression
  thread with bio-coalesced swapout and an early-OOM gate. The 7.3-merge mm had
  diverged (memcg soft-limit removal, mglru refactor, `page_io.c` rewritten
  around `swap_io_ctx`, `alloc_context` moved), so the port base-fit those.
- The latest mm, mglru and memcg fixes from `next-20260901`.

### Changed
- **Dropped 20 patches** that target the 7.2-era base and do not apply to the
  7.3-merge tree; the build had been skipping them silently. They were 7.2-only
  CachyOS squashes, SMU14, amd-pstate, ttm and gfx12 backports, early DCN4
  backports the base's newer code supersedes, a zram out-of-bounds fix, and one
  userq fix. Series: 123 patches.

## [7.2.0-10-sleepy-next-20260828]: 2026-08-28

The last release on the linux-next preview line before the move to mainline rc2.

### Fixed
- **Six patches from `-9` were empty no-ops** and are now applied for real: the
  VM-update GPU-hang fix, the GFX12 no-retry PTE fix, the DCN4 flip-schedule
  pair, and the display IRQ guard.

### Changed
- Dropped 76 patches whose content `next-20260828` upstreams. Series: 143
  patches.

## [7.2.0-9-sleepy-next-20260828]: 2026-08-28

### Added
- Eight patches from the amd-staging branch and the mailing lists: a GPU-hang
  fix for the VM page-table update path (`Cc: stable`), GFX12 no-retry PTE
  flags, two DCN4 flip-schedule fixes, a DCN42 idle-power hang fix, HDMI 2.1 FRL
  enabled by default, a user-queue deadlock fix, and a display-IRQ teardown
  guard.

## [7.2.0-8-sleepy-next-20260828]: 2026-08-28

### Changed
- Base bumped from `next-20260827` to `next-20260828`. This snapshot upstreams a
  large batch of AMD driver fixes that were being carried as patches, which made
  roughly 70 of them redundant. The 22 AMD commits in the delta are included.

## [7.2.0-7-sleepy-next-20260827]: 2026-08-27

### Added
- **23 patches** surfaced by a sweep of the lkml archives, the AMD display and
  power-management mailing lists, the AMD bug tracker, and the drm-next,
  amd-staging and drm-misc trees: a 15-patch ACPI CPPC rework that `amd-pstate`
  uses on Zen 4, three zstd BMI2 probe patches, three display robustness fixes,
  a boot-time SR-IOV workaround guard, and a sched-ext allocation cleanup.

## [7.2.0-6-sleepy-next-20260826]: 2026-08-26

### Fixed
- **The "box" artifact was masked in-kernel** by adding
  `amdgpu.dcdebugmask=0x800` to the built-in command line, so it no longer
  depended on a boot argument. Root cause at the time was understood to be
  display idle-power making the driver report an update complete before the
  hardware latched it. This mask was removed in `7.3.0-rc2-11` once the real
  cause turned out to be in the compositor.

## [7.2.0-5-sleepy-next-20260825]: 2026-08-26

### Added
- DCN4 cursor and plane fixes carried from upstream: colour-management state on
  plane recreate, a blend-mode property warning fix, and an overlay-cursor
  fallback.

### Fixed
- **HDMI variable refresh rate** is now offered on the HDMI outputs. The
  firmware path missed FreeSync panels; the driver reads the panel's advertised
  ranges directly.
- The "box" artifact was first worked around with `amdgpu.dcdebugmask=0x800` on
  the boot entry.

## Earlier packages

Both of the following were removed from the working tree. Their `PKGBUILD`,
`patches/` and `config` trees remain in git history, as do their full changelog
entries: `git log --follow CHANGELOG.md`, and
`git show 34e0f98:CHANGELOG.md` for the text as it stood before this file was
consolidated.

### 7.2 `linux-sleepy` (dropped 2026-09-12)

The repository's original package. It was dropped in favour of the single 7.3
package; the `net-tune` service it owned moved to `linux-sleepy-next`.

| Version | Date | Summary |
|---|---|---|
| `7.2.0-2-sleepy` | 2026-08-19 | 17 verified sweep candidates merged; series 157 → 174 patches. |
| `7.2.0-1-sleepy` | 2026-08-19 | Base moved to Linux 7.2 stable; the FAIR revert series dropped as obsolete. |
| `7.2.0-rc7-8-sleepy` | 2026-08-15 | zstd 1.6.0 with the gcc-BMI2 segfault guard. |
| `7.2.0-rc7-7-sleepy` | 2026-08-15 | Six-source sweep; series 179 → 184 patches. |
| `7.2.0-rc7-6-sleepy` | 2026-08-14 | `1053`, an AI-proposed DRM scheduler `min_vruntime` fix. |
| `7.2.0-rc7-5-sleepy` | 2026-08-14 | Seven backports from the `amd-drm-next-7.3-2026-08-12` tag. |
| `7.2.0-rc7-4-sleepy` | 2026-08-12 | Added `amdgpu.aspm=0` and `amdgpu.runpm=0` stopgaps. |
| `7.2.0-rc7-3-sleepy` | 2026-08-12 | Full revert of the DRM scheduler FAIR series; FIFO default restored. |
| `7.2.0-rc7-2-sleepy` | 2026-08-12 | Maintenance sweep; series 151 → 154 patches. |
| `7.2.0-rc7-1-sleepy` | 2026-08-11 | Maintenance sweep; series 140 → 151 patches. |
| `7.2.0-rc7-1-sleepy` | 2026-08-10 | Bump to Linux 7.2-rc7; series 127 → 140 patches. |
| `7.2.0-rc6-7-sleepy` | 2026-08-04 | Bump to Linux 7.2-rc6; 36-patch sweep, `net-tune` introduced. |
| `7.2.0-rc5-1-sleepy` | 2026-08-02 | First maintained release; series renumbered into ranges. |

`7.2.0-rc7-1` was used twice, on 2026-08-10 and 2026-08-11.

### `wannabe-7.3-rc1` (2026-08-26, removed 2026-09-02)

A git-worktree preview built from `next-20260825` ahead of the 7.3-rc1 release,
with its own `wannabe-7.3-patches/` series and `WANNABE-7.3.md`. It was
superseded by the `sleepy-next` package, which carries the same content: the
`mm/gup` batching series (`2120`–`2127`), the HDMI VRR and ALLM patches
(`0059`–`0061`), and the userq and KFD work in the `9000` range.
