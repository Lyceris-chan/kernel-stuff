# Changelog

All notable changes to **sleepy-kernel**, the custom Arch Linux kernel for a
Ryzen 7 7700 (Zen 4) + Radeon RX 9070 XT (RDNA 4 / gfx1201) desktop.

Format follows [Keep a Changelog](https://keepachangelog.com/) and the
[Google developer style guide](https://developers.google.com/style). Versioned
by the running kernel (base + `pkgrel`), e.g. `7.2.0-rc7-1-sleepy`.

---

## [7.2.0-rc7-3-sleepy] — 2026-08-12 (DRM scheduler revert)

Full revert of the 7.2 DRM scheduler **FAIR** series (Tvrtko Ursulin,
`[PATCH v2 00/20] Revert switching default DRM scheduler policy to fair`,
dri-devel ML 08-11). The FAIR default caused a performance regression on the
RX 9070 XT under sustained 100% GPU load (foreground app drops to ~10 fps or
freezes — 7.1.5 and FIFO both pass). This restores the pre-fair
multi-run-queue FIFO/RR scheduler and makes **FIFO the default** again.

### Changed

- **DRM scheduler reverted to FIFO default** (`1029`–`1046`, replacing the
  earlier `1028` `min_vruntime` partial fix, which is dropped as superseded).
  `sched_policy` module param restored: 0=RR, 1=FIFO (default), 2=fair
  (experimental). Series order is preserved in the numbering. `01/20` and
  `11/20` of the upstream series were not carried (01's target commit absent
  from rc7 = already reverted; 11 is the imagination/PVR driver, not built).
  `1043` (Embed-rq revert) carries one rc7-adapted `amdgpu_xcp.c` hunk.
- Not related to the SMU-IF blackscreen/bus-drop issue (work-item !5538,
  `pcie.aspm=off` stopgap) — that is a separate firmware-side problem and
  remains tracked separately.

---

## [7.2.0-rc7-2-sleepy] — 2026-08-12 (maintenance)

Six-source sweep (drm-next, drm-misc, agd5f, amd-staging, linux-next, linux-pm,
amd-gfx + dri-devel ML, sirlucjan, firelzrd, GitLab drm/amd work-items,
x86/security) plus the two user-flagged lore.kernel.org threads (fetched via
the freedesktop mbox archives). The series grew from 151 to 154 patches.

### Added

- **DRM scheduler `min_vruntime` fix** (`1028`, dri-devel ML, Tvrtko Ursulin).
  Addresses the FAIR-policy regression on the RX 9070 XT: since 7.2 made FAIR
  the scheduler default, sustained 100% GPU load degraded the foreground app to
  ~10 fps or froze the desktop (7.1.5 and FIFO both pass). A run-queue entity
  that never exits is penalized as its virtual runtime only grows; the fix
  tracks `min_vruntime` strictly monotonically. ML-only v1 partial fix — the
  full v2 20-patch revert was evaluated and does not apply cleanly to rc7.
- **memcg OOM exit-path fix** (`2109`, akpm-mm mm-unstable, Shakeel Butt). An
  OOM-killed process could be stuck in the exit path for hours when zswap held
  its memory (nothing left on the LRUs, and swapin re-charges re-triggered
  OOM); dying tasks now bypass reclaim/OOM once oom_reaper is done. Matches
  this build's zswap-default-on + memory.max setup.
- **zsmalloc size-class lookup fix** (`2110`, akpm-mm mm-unstable, Longlong
  Xia). zram recompression misjudged size-class movement near boundaries
  because class lookup ignored `ZS_HANDLE_SIZE`; class selection is now shared
  between lookup and allocation.

### Reviewed, not taken

- Rik van Riel's `[RFC PATCH v3 0/8] batch lookups in follow_page_mask()` (gup
  perf series, 2.2–5.9× on mTHP) — RFC, not merged, not adoptable as-is.
- Full Tvrtko v2 scheduler revert series — 5+ hunks conflict with rc7.
- mm/swap single-folio revert (needs unmerged swap_ops prereqs), DCN42
  DCHVM↔rIOMMU series (display virtualization), zram big-endian slot-lock fix,
  zswap memcg-disabled shrinker fix (`CONFIG_MEMCG=y` here).

---

## [7.2.0-rc7-1-sleepy] — 2026-08-11 (maintenance)

Full six-source sweep (drm-next, drm-misc, linux-next — incl. the
next-20260811 snapshot —, linux-pm, agd5f, amd-gfx + dri-devel ML, sirlucjan,
GitLab drm/amd work-items, x86/security). The series grew from 140 to 151
patches.

### Added

- **GFX12 MES scheduler ring fence force-completion** (`1027`, amd-gfx ML,
  Jesse Zhang/AMD). The MES ring has no drm scheduler, so it is skipped by the
  reset force-completion loop; its wb-backed polling fence survives a MODE1
  reset while `sync_seq` keeps advancing, wedging the first post-resume
  submission ("MES ring buffer is full"). Now force-completed alongside the
  scheduler rings. ML-only; not yet in drm-next.
- **GFX12 userq/HMM correctness fixes** (`9038`–`9040`, amd-gfx ML 08-11,
  Junrui Luo): reject PRT mappings as user-queue buffer VAs (NULL-bo deref on
  GEM unmap), bound the eviction-fence rearm retry loop, and free userptr HMM
  ranges on the CS error path. Same author/series family as the carried
  `9033`–`9035`. Apply after `9036` (userq VA-validation rewrite).
- **zram zstd error-path + param fixes** (`2102`–`2104`, linux-next via
  akpm-mm, Haoqin Huang/Tencent): no longer release zstd global params from
  per-CPU error paths, reject zero-size dictionaries, and reset per-priority
  params when the algorithm changes before init. 3 of 5 series patches carried;
  the `pr_fmt` + per-backend validation hunks target a newer `backend_deflate.c`
  absent from rc7.
- **zram stability fixes** (`2105`–`2108`, linux-next via akpm-mm, `Cc:
  stable`): OOB access in `read_block_state()`/`writeback_store()` after a
  reset with smaller disksize (Longlong Xia/Kylin), deflate winbits range
  validation (Sergey Senozhatsky), and a NULL primary compressor after
  `zram_destroy_comps()` (Senozhatsky).

### Changed

- **Patches now live in `patches/<range>/` folders.** makepkg 7.1.0 resolves
  local sources by basename only, so the PKGBUILD body auto-creates gitignored
  root-level symlinks (`NNNN-*.patch -> patches/<range>/NNNN-*.patch`) when it
  is sourced, before source resolution. This keeps the GitHub repo root clean
  while the real patches stay organized in folders. (An earlier folder refactor
  `16fd28b` was committed untested and broken; the working folder layout with
  the symlink mechanism is verified — 151 patches apply with 0 rejects, build
  passes with BTF present.)

### Fixed

- **DRM scheduler FAIR policy regression** (RX 9070 XT, amd-gfx + linux-kernel
  ML 2026-08-08/10): tracked. No formal fix has landed (Tvrtko Ursulin proposed
  a `min_vruntime` fix; maintainers leaning toward reverting the FAIR-default
  switch). Our rc7 tree carries the FAIR-only scheduler, so this is a known
  upstream issue to watch — not yet carryable without a merged patch. Note:
  scx_sched (the CPU scheduler) does not affect this GPU-side scheduler
  regression.

---

## [7.2.0-rc7-1-sleepy] — 2026-08-10

Bump to **Linux 7.2-rc7** (tag `linux-7.2-rc7`). The series grew from 127 to
140 patches. Build verified: BTF present for `vmlinux` + modules, `bbr3`
built-in with the old `bbr` disabled, CAKE SQM ingress enabled.

### Fixed

- **GFX12 KFD CRIU-restore NULL-deref panic** (`1026`, amd-gfx ML). On
  gfx1201 the MQD managers leave `restore_mqd`/`checkpoint_mqd` unset, so a
  user holding `CAP_CHECKPOINT_RESTORE` could panic the machine via
  `KFD_IOC_CRIU_OP_RESTORE`. Reconstructed from the mbox (Outlook stripped the
  diff's context whitespace); ML-only, pending an upstream v2.
- **AMDGPU 7.3 backports** (11 total): DCN401 HDR/SDR seamless switch, MST
  `connector->index` bounds check, MST HDCP array resize, DCN42B
  `force_min_dcfclk` clamp, smu_v14_0_0 DPM trio (DCLK metric, DCEFCLK,
  `find_clk_level()`), amdgpu CS/VM correctness (FENCE-chunk leak, VM overrun,
  BO-VA kmap offset), gfx12 userq sub-page VA validation, and the `9037`
  prefer-default-discovery-offset backport.
- **mes12 dropped-dispatches fix** (`1024`): pads the MES queue dispatch so
  concurrent queue oversubscription no longer drops dispatches.
- **DCN42B display fixes**: HPD toggle-filter unit fix (`1135`) and FRL link
  training timeout update (`1136`).
- **LRU-MARIE 0.9.3**: orphaned-L1-bit self-heal — reclaim no longer wedges
  under hot single-type bursts.
- Dropped `1020`/`1021`/`1022` (verified merged upstream in rc7).

### Changed

- **PCIe ASPM off** by default (`pcie_aspm=off` on the built-in command line).
  Stopgap for the drm/amd !5538 SMU bus-drop class — the RX 9070 XT can drop
  off the PCIe bus during SMU power transitions (firmware-side issue; AMD
  engineers suggested ASPM-off).
- **CachyOS fixes branch v11** (`0105`/`0106` regenerated): the branch adds
  the PCI Skip Target Speed quirk (skips 2.5GT/s link-retrain on empty/clamped
  slots, saving ~2s boot) and reworks `mm/mglru`/`mm/vmscan` to the
  `vma_flags_t` API. Net applied effect unchanged except the new quirk.
- `0050` swapped to Alex Huang's v3 (future-VSDB tolerance).

### Deferred (documented, not carried)

- HDMI 2.1 VRR/ALLM v2 (needs the `amdgpu_dm_connector` split not in rc7).
- Valve dmemcg aggressive-protect stack (conflicts with `0104` cgroup-vram).
- gfx12 priv-fault recovery set (needs gfx11 `userq_priv_fault_work` fields).

## [7.2.0-rc6-7-sleepy] — 2026-08-04

Bump to **Linux 7.2-rc6** (tag `linux-7.2-rc6`). Final `pkgrel` of the rc6
line (`rc6-1` … `rc6-7`); `pkgrel` 6 was skipped in git history.

### Fixed

- **36-patch six-source sweep** (biggest single addition): the **retry-fault
  handling v3 series** (`9011`–`9024`, 14 patches — the main RDNA4 stability
  gap), DCN4/DCN42B display fixes including the actual PSR/Replay enable
  (Part 2), IPS/zstate/HUBP-DPP-PG idle-power, the DCN42 DF C-state boot-hang
  backport, and Roman.Li's July-31 DC batch.
- **AMDGPU backports**: gmc12.1 MMHUB0 pasid TLB flush fix, TLB-invalidation
  semaphore, compressed-FRL-cap dispatch fix, gfx12 `TRUNCATE_COORD_MODE` fix,
  mes12.1/imu12 `BUG()`→`WARN()` drops (completes the `9001`–`9003` family),
  oversized-IB rejection (`1022`), and the `ignore_min_pcap` module param
  (`1023`).
- **BT.2020 YCbCr output CSC fix** (`1134`).

### Added

- **`net-tune` systemd service** — unified low-latency ethernet tuning +
  CAKE SQM shaping, replacing the separate `sqm-qos/` scripts. SQM is enabled
  by default at 80/80 Mbit; ingress shaping requires `CONFIG_NET_SCH_INGRESS`
  and a named `ifb4cake` device (fixed across `pkgrel 2–3`).
- **CachyOS fork backports** (`0110`–`0113`): `CONFIG_CACHY` config hooks
  (EEVDF base_slice, THP defrag, lru_gen_min_ttl), ACPI bus-master check
  disable for AMD C3, amdgpu S4/S5 eviction skip, and a micro-opts bundle.
- Dropped custom `r8125` module (in-kernel `r8169` covers the RTL8125B NIC).

### Changed

- Bloat removal: disabled Intel-only audio/thermal, debug hooks, NVMe
  multipath/host-auth, I2C/SPI slave, IPv6 IOAM, and F2FS; kept `autofs`.
- Enabled `uvcvideo` for UVC webcams (replaces the dead `V4L2_LOOPBACK` line).
- Dropped `1204`/`1210`/`1211`/`1212`/`1213`/`9000`/`9004`/`9005` (merged
  upstream in rc6).

## [7.2.0-rc5-1-sleepy] — 2026-08-02

Initial release of sleepy-kernel as a maintained package. Series renumbered
into coherent ranges (`0001`–`9007`), CachyOS squashed to one patch per branch
(`0101`–`0109`, with the off-target `0106` drops), and README/PATCH_SOURCES
rewritten in the Google developer style. Build verified: `linux-sleepy
7.2.rc5-1`, BTF present.

[7.2.0-rc7-1-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc7.tar.gz
[7.2.0-rc6-7-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc6.tar.gz
[7.2.0-rc5-1-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc5.tar.gz
