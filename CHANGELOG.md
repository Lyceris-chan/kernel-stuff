# Changelog

All notable changes to **sleepy-kernel**, the custom Arch Linux kernel for a
Ryzen 7 7700 (Zen 4) + Radeon RX 9070 XT (RDNA 4 / gfx1201) desktop.

Format follows [Keep a Changelog](https://keepachangelog.com/) and the
[Google developer style guide](https://developers.google.com/style). Versioned
by the running kernel (base + `pkgrel`), e.g. `7.2.0-rc7-1-sleepy`.

---

## [7.3.0-rc1-12-sleepy-next-20260901] — 2026-09-02

Updated to the latest linux-next base (`next-20260901`, now carrying 7.3-rc1
content — the kernel version string advances to 7.3.0-rc1) and completed a
full re-sweep of every source. The headline change: **LRU-MARIE is now ported
to the linux-next (7.3-merge) base**, replacing the version that never applied.

### Added
- **LRU-MARIE 0.11.0, ported to linux-next** (ultracode multi-agent port of the
  original author's 7.2 patch). MARIE is a memory-reclaim accelerator: a
  per-PFN reclaim-state byte array, SIMD young-bit walker, and — new in 0.11 —
  a `kcompressd` async-compression thread with bio-coalesced swapout and an
  early-OOM gate. The 7.3-merge mm diverged (memcg soft-limit removal, mglru
  refactor, `page_io.c` rewritten around `swap_io_ctx`, `alloc_context` moved),
  so the port base-fit those. Verified: applies cleanly + compiles
  (`CONFIG_LRU_MARIE=y`). Runtime behavior needs real testing under memory
  pressure.
- The latest mm/mglru/memcg fixes from `next-20260901`.

### Changed
- **Dropped 20 patches** that target the 7.2-era base and do not apply to the
  7.3-merge tree (they were silently skipped at build): 7.2-only CachyOS
  squashes, SMU14/amd-pstate/ttm/gfx12 backports, early DCN4 backports the
  base's newer code supersedes, zram OOB, and one userq fix. Series is now a
  clean 123 patches — every one applies.

### Fixed
- Source sweep re-confirmed (all sources): no new AMD display/GPU fixes worth
  carrying beyond the base. The passive-VRR series (dri-devel) is a new v1
  feature, not a fix — assessed and deferred.

## [7.2.0-10-sleepy-next-20260828] — 2026-08-28

Patch-series cleanup and rebuild. Fixed six of the second-sweep patches that
were accidentally empty (no-ops) in -9 — they are now applied for real (the
VM-update GPU-hang fix, GFX12 no-retry PTE, flip-schedule pair, and IRQ guard
are now active). Also dropped 76 patches whose content `next-20260828` now
upstreams, so the series is back to a clean 143 patches with no redundancy.

### Fixed
- The VM-update GPU-hang fix, GFX12 no-retry PTE, and DCN4 flip-schedule fixes
  from the -9 release are now genuinely applied (they were empty no-ops before).

### Changed
- Removed 76 redundant/superseded patches the base now provides; series is 143
  patches, `source=()` matches on-disk exactly.

## [7.2.0-9-sleepy-next-20260828] — 2026-08-28

A second thorough sweep (amd-staging branch + mailing lists, 08-28 window)
surfaced 8 more patches worth carrying, all built into this release:

### Added
- **A GPU-hang fix (CC: stable)** — the VM page-table update path could
  reallocate a job and keep a stale "free space" count, encoding an enormous
  copy that ran off the command buffer and hung the GPU ring.
- **GFX12 "no-retry PTE" flags fix** — corrects the invalid flag combination
  for RDNA4.
- **Two DCN4 flip-schedule fixes** — corrected bandwidth math on the flip
  path (same code area as the earlier display-freeze investigation).
- **A DCN42 idle-power hang fix** — the display's data-path disconnect during
  an idle-power state could overrun an I/O-MMU credit and hang invalidation.
- **HDMI 2.1 FRL is now enabled by default** — the driver no longer needs a
  module option to use high-bandwidth HDMI 2.1 Fixed-Rate Link.
- **A user-queue deadlock fix** — cancels the hang-detect worker before
  taking the user-queue mutex (reviewed, real deadlock path on RDNA4).
- **A display-IRQ teardown guard** — avoids a race when the IRQ workqueue is
  torn down.

### Changed
- The base (`next-20260828`) already upstreams ~18 of the AMD fixes we had
  backported, so those no longer need local patches.

## [7.2.0-8-sleepy-next-20260828] — 2026-08-28

Updated to linux-next `next-20260828`. This snapshot upstreams a large batch of
the AMD driver fixes we had been carrying as patches — the base now includes
them, so they no longer need to be applied by hand. Re-checked every source
(AMD display/power mailing lists, lkml archives, the AMD bug tracker, and the
drm-next / amd-staging trees) for this release window.

### Added
- **CU-occupancy support for GFX12.1** — now that this snapshot is the base,
  the RX 9070 XT gets the fuller version of the compute/occupancy reporting.
- The base now absorbs our previously-backported user-queue (userq), KFD
  shared-memory (SVM), and CRIU patches — roughly 70 patches in our series
  become redundant (the same fixes are now upstream).

### Changed
- Bumped the linux-next base from `next-20260827` to `next-20260828`; the
  22 AMD commits that landed in that delta are all included.

### Fixed
- Bug fixes that landed in the delta are now in the base: a GPU-reset
  display lock leak, a user-queue fence lock, SVM migration hole/error-path
  fixes, a KFD CRIU NULL-guard, and a ring-isolation bounds check.

## [7.2.0-7-sleepy-next-20260827] — 2026-08-27

Updated the sleepy-next preview kernel to linux-next `next-20260827` and ran a
thorough sweep across every source we track — the lkml archives, the AMD
display and power-management mailing lists, the AMD driver bug tracker, and
the drm-next / amd-staging / drm-misc git trees. That surfaced **23 new
patches** relevant to this hardware, all merged into this release:

### Added
- **Better CPU frequency control (15 patches).** A rework of the ACPI CPPC
  path that `amd-pstate` uses on Zen 4. It validates the firmware-provided
  tables, reports write errors instead of silently dropping them, serializes
  update commands, and fixes a batch of register-width and memory-lifetime
  bugs. The result is more robust and predictable CPU frequency scaling.
- **Faster zstd (3 patches).** The kernel's zstd now probes for the CPU's
  BMI2 instructions once instead of on every compression context — a small
  win for zram/zswap startup and use.
- **More robust displays (3 patches).** The AMD display driver no longer
  tries receiver power control over a dead AUX channel, closes the DDC line
  when an I2C setup fails, and falls back to software I2C when the hardware
  engine stumbles. Steadier EDID/display detection on HDMI.
- **A boot-time fix (1 patch).** The early graphics init no longer runs an
  SR-IOV-only workaround on normal desktop cards.
- **sched-ext tweak (1 patch).** Skip per-CPU allocation for built-in
  schedulers — a small cleanup for the sched-ext subsystem.

### Changed
- Bumped the linux-next base from `next-20260826` to `next-20260827` (a
  one-day refresh; no AMD display changes in that delta).

## [7.2.0-6-sleepy-next-20260826] — 2026-08-26

### Fixed
- **The "box/square" artifact is now permanently fixed.** We baked the
  fix into the kernel itself, so it no longer depends on a boot argument.
  Root cause: the display controller's idle-power feature made the driver
  report a screen update as complete before the hardware had actually
  latched it, so the desktop compositor redrew into a buffer that was still
  being scanned — leaving a small square of stale content over app windows.
  Disabling that idle-power feature (via `amdgpu.dcdebugmask=0x800`) resolves
  it at a small power cost.

### Changed
- Bumped the linux-next base to `next-20260826` (a routine one-day refresh).

## [7.2.0-5-sleepy-next-20260825] — 2026-08-26

### Added
- DCN4 cursor/plane fixes carried from upstream (color-management state on
  plane recreate, a blend-mode property warning fix, and an overlay-cursor
  fallback for DCN4).

### Fixed
- **HDMI Variable Refresh Rate (VRR)** — now offered on the HDMI outputs
  (the firmware-based path missed FreeSync panels; the driver now reads the
  panel's advertised ranges directly).
- **The "box/square" artifact** — first worked around via the boot entry
  (`amdgpu.dcdebugmask=0x800`, disables Idle Power States); made permanent in
  the next release.

---

## [wannabe-7.3-rc1] — 2026-08-26 (preview tree, unreleased)

Built a **wannabe 7.3-rc1** preview tree (`wannabe-7.3-rc1/`, git worktree
from `linux-next` `next-20260825`) ahead of the 7.3-rc1 release. It is a
superset of the 7.2.0-2 build plus the 7.3 merge-window content relevant to
this hardware. See `WANNABE-7.3.md` for the full breakdown.

### Added (upstream 7.3 window, arrives with the real bump)

- **AMDGPU/DC**: amd-drm-next-7.3-2026-08-19 merge (pipeline-sync, userq
  destroy hang/race, KIQ ring fence, VCN overflow, brightness curve,
  VA-map-before-restore) + 17 amd-staging backports (KFD CRIU, userq
  fence-lock/wptr-restore, MES teardown, SVM migrate, AQL zero-size,
  CU-occupancy GFX12, no-retry PTE, VM dw-estimate, DCN42 fixes, HPD IRQ
  logging).
- **MM**: ~30 commits (MGLRU exec-folio promote/young-counter, vmscan
  lru_lock/folio_referenced, zram/zsmalloc/zswap, swap single-folio revert,
  memcg reparent) + drm/sched `entity_is_idle()` lock.
- **amd-pstate**: dynamic EPP as `energy_performance_preference`, CPPC
  hot-path, `bios_min_perf` — the old `amd_dynamic_epp` cmdline is gone.
- **Latency**: ByteDance SMP-IPI preemption rework (~90% scheduling-latency
  drop; covers Phoronix 08-17/08-22 articles) + x86/mm `flush_tlb_multi`
  preemption.
- **TTM** (Valve): aggressive eviction below the protection limit.
- **sched-ext**: sub-scheduler support "feature complete" (`scx_bpf_dsq_move`
  fix, header syncs).

### Added (sleepy-kernel series carried over)

- The full 69-patch additive series from the 7.2.0-2 build: CachyOS squashes
  (bbr3, kbuild, cpu-isa, config-hooks, preempt-ipi, ACPI-BM/S5, fork
  backports), local GPU fixes (PROFILE_PEAK, SMU14, DCN/EDID, TLB-invalidate,
  retry-fault, userq, MES CRIU, VCN util, soft-evicted), bfq/mq-deadline,
  LRU-MARIE 0.10.5, zstd/zswap, NAP governor.

### Added (Phoronix WIP, RFC)

- **Rik van Riel `mm/gup` follow_page_mask() batching** (RFC v3) — up to
  12.8× in gup_test on mTHP paths (GPU userptr / io_uring / VMA walkers
  benefit). Applies cleanly to next-20260825; marked RFC (v4 exists), expect
  upstream revisions to supersede.
- **Clean 7.3 HDMI — upstream HDMI 2.1 VRR + ALLM v4** (amd-gfx ML): the
  three amdgpu-side patches (`SIGNAL_TYPE_HDMI_FRL` FreeSync + VTEM,
  HF-VSDB VRR-range fallback, ALLM_Mode in HF-VSIF). The drm/edid part
  equals our additive `0055`. **The CachyOS `0107` hdmi squash contributes
  nothing to this tree** (base supersedes it via `dc_edid_parser` +
  `update_freesync_caps` + FRL fixes) — clean upstream, no CachyOS fluff.
- **ML WIP merges** (amd-gfx + dri-devel, 08-24/08-25): userq GPU-reset
  crash + lockdep 5-patch (Vitaly Prosyak — dma_resv slot, hang_detect_work
  deadlock, reset-lock order, psp resume), BO-bind for imported user-queue
  BOs (v5), KFD mark queues as reset after full GPU reset, amdgpu_vm_init
  error-path NULL-deref reorder. All isolated commits.

### Verified during the FAAA / month audit

- MARIE LRU **0.10.5 is current** (no newer from firelzrd or sirlucjan).
- zstd `2100` already has the gcc<11.4 segfault workaround.
- **0107 vs clean ML HDMI**: verified the ML VRR/ALLM v4 amdgpu-side
  patches can't replace `0107` on 7.2 (they target the amdgpu_dm split,
  absent there) — `0107` stays required on 7.2; clean ML HDMI is already
  adopted in the wannabe 7.3 tree.
- **Leo Li (sunpeng.li) display fixes** — confirmed in the wannabe base
  (402 commits, incl. flip-done timeouts on mode1 reset + DCN vblank/flip
  consolidation); arrive with the 7.3 bump, not backported to 7.2.
- Work items tracked: **#5693** (RX 9070 XT VCN-unigate + SMU deadlock,
  no fix yet), #5649 (HDMI FRL blanking, RDNA3), #5671, #5656.
- Candidates under review (not merged): 30-patch GPU TLB-invalidation
  rework (`151442`), MMIO-TLB fallback RFC v3, userq-reset 5-patch.

### Deferred (off-target or WIP)

- Menu-governor wakeup fix (Intel Xeon; we run NAP), RTL8261C/D (not our NIC),
  DRM fair-policy fix (FIFO default), k10temp per-CCD (EPYC-only), reflex
  governor (needs cpufreq API port), work-items #5616/#4753 (no provenance).

### Fixed (2026-08-26) — DCN401 "box/square" scanout artifact

The fixed small square over app windows (absent from screenshots, color tracks
the content behind it) on this base was caused by DCN4 Idle Power States
pipe-gating. `hubp2_is_flip_pending()` returns `false` when `hubp->power_gated`,
so the 7.3 VUPDATE_NO_LOCK flip-event handler (which replaced the HW-latch
GRPH_PFLIP path) delivers flip completion before HW latches → the compositor
re-paints a buffer the display is still scanning → a fixed content-tracking
region. Fixed with `amdgpu.dcdebugmask=0x800` (`DC_DISABLE_IPS`) in the built-in
CMDLINE (PKGBUILD). A/B verified: `0x20000` (FAMS) and `0x8` (clock gating) did
not help; `0x800` (IPS off) fixed it. Same class as AMD drm/amd work item
#5570 (Navi 21, closed 2026-08-25). Re-evaluate when a proper DCN401
flip-pending fix lands upstream.

### Updated (2026-08-27) — sleepy-next bumped to next-20260827 + sweep patches

- **Bump**: linux-next `next-20260827` (pkgrel 7). No drm/amd changes in the
  one-day delta; the 188-patch series applies/skips identically.
- **zstd BMI2 probe series** (`2128`–`2130`, Usama Arif/Meta) — probe the CPU
  for BMI2 once instead of per context (`lib/zstd`).
- **ACPI CPPC v5** (`1210`–`1224`, Christian Loehle) — 15-patch rework of the
  CPPC control path amd-pstate runs on Zen 4 (register access + lifetime fixes).
- **drm/amd/display** (`1141`–`1143`, NepNep7601) — RX power control without
  AUX, DDC-close on I2C failure, software-I2C fallback.
- **drm/amdgpu** `1059` (Mario Limonciello, Cc:stable) — restrict BAR0 fallback
  read to SR-IOV VFs (boot-path regression fix).
- **sched_ext** `2005` (Qiurong Fang) — skip per-CPU allocation for built-in
  DSQs.
- Block merge `55ab7e14222e` confirmed already in base.

---

## [7.2.0-2-sleepy] — 2026-08-19 (sweep candidates merged)

Merged the 17 verified candidates from the 08-19 ultracode sweep onto the 7.2
base. The series grew from 157 to 174 patches.

### Added

- **GPU core** (`1056`–`1058`): drm/sched `entity_is_idle()` lock (Philipp
  Stanner), TTM grab-BO-ref-before-lock (Natalie Vock), amdgpu soft-evicted
  tracking for always-valid BOs (Natalie Vock).
- **Memory management** (`2114`–`2119`): RCU-tasks quiescent states in
  `shrink_lruvec()` (Breno Leitao), swap bad-entry ratelimit, khugepaged
  pte-unmap ordering (Nico Pache), zswap batch writeback (Hao Jia), shmem
  fallocate overflow reject (Zhiling Zou), memcontrol vmstats/events
  false-sharing (Usama Arif).
- **Backports** (`9041`–`9048`): 4 userq fixes (doorbell xa-lock, destroy
  hang/race, wptr-BO validate, wait_for_signal skip), KFD CU-occupancy GFX12
  (David Belanger), KFD ring-buffer overflow (Vladimir Marioukhine), and 2
  amdkfd SVM migration fixes (Xiaogang Chen).

### Deferred / dropped

- **Deferred:** pgrotate vmstat counters (standalone-inert, consumer not yet
  rebased), AQL zero-size reject (awaiting v2 after Alex Deucher review).
- **Dropped:** `MEMORY_FAILURE select MIGRATION` (no-op for our config),
  KFD CU-occupancy GFX12.1 (off-target gfx1210).
- **Not adopted:** pixelcluster "Don't evict page tables" — explicitly marked
  `XXX super scuffed ... needs to be reworked` (hacky private-fork workaround);
  work-items DDC fix requires the post-7.2 `amdgpu_dm_connector.c` split.

---

## [7.2.0-1-sleepy] — 2026-08-19 (Linux 7.2 stable bump)

Bumped the base from 7.2-rc7 to the **7.2 stable release**. Version is now
`7.2.0-1-sleepy`. The series dropped from 184 to 157 patches.

### Changed

- **Base → Linux 7.2 stable.** Reference tree `repos/linux-7.2`, source
  tarball `linux-7.2.tar.gz`, version string `7.2.0-1-sleepy`.
- **Dropped the DRM scheduler FAIR revert series (`1029`–`1046`) and the
  min_vruntime fix (`1053`).** 7.2 stable upstream already reverted FAIR→FIFO
  (commit `2bbea6b81`) and defaults to FIFO with multi-rq — our rc7 revert
  series is now obsolete.
- **Dropped 8 patches merged upstream in 7.2:** `1048`, `1049`, `1052`,
  `1134`, `1141`, `9033`, `9037`, `9008`.
- **Regenerated the CachyOS `0105`/`0106` fixes squashes** from the current
  sirlucjan fixes branch (24-patch). The branch now carries the MM exec-folio
  series (vma_flags_t, exec-folio helper, MGLRU promote-exec) inside `0105`.
- **Upgraded LRU-MARIE to 0.10.5** (`2101`), with the `vma_flags_test` fix
  preserved against the CachyOS vma_flags_t rename.
- **MuQSS / CK patchset evaluated and rejected:** the new MuQSS v0.31 series is
  mutually exclusive with sched-ext (the patch adds `scx_cpuperf_target()`/
  `scx_switched_all()` stubs disabling SCX); our config uses
  `CONFIG_SCHED_CLASS_EXT=y`, so it is not adoptable.

---

## [7.2.0-rc7-8-sleepy] — 2026-08-15 (zstd 1.6.0 + work-items recheck)

### Changed

- **zstd upgraded to 1.6.0** (`2100`): swapped the carried "dev tree" merge for
  the newer sirlucjan `zstd-7.2: merge v1.6.0 into kernel tree` revision — the
  same 1.6.0 code plus the Nick Terrell **gcc-BMI2 segfault guard** (DYNAMIC_BMI2
  gated on gcc ≥ 11.4; avoids a `HUF_compress1X_usingCTable_internal_body` crash
  on older gcc). Same 18 files, applies cleanly to rc7.

### Unchanged (evaluated)

- **HDMI 2.1 VRR/ALLM v4 (upstream)** is not backportable to rc7: patches 1/3/4
  target `amdgpu_dm_connector.c`/`amdgpu_dm_freesync.c` (post-rc7 split absent
  here); only 2/4 (drm_edid HF-VSDB) applies — already carried as `0055`. The
  CachyOS `0107` branch is the only HDMI implementation that works on rc7
  (targets the pre-split `amdgpu_dm.c`) and already excludes the `0055`
  duplicate (`0151`). Switch to the upstream series at the 7.3 bump.
- **GitLab work-items**: open reports are firmware/user-space/Mesa-side (VCN5
  decode needs a firmware update; flip_done is compositor/VRR; artifacts are
  FreeSync/Plasma). No new adoptable driver-side kernel patch.

---

## [7.2.0-rc7-7-sleepy] — 2026-08-15 (six-source sweep)

Six-source sweep (drm-next, drm-misc, linux-next `next-20260814`, linux-pm,
agd5f, amd-gfx + dri-devel ML, sirlucjan, GitLab drm/amd work-items,
x86/security, akpm-mm). The series grew from 179 to 184 patches.

### Added

- **GFX12 userq fence error-set lock fix** (`1054`, amd-gfx ML, Prike Liang):
  `amdgpu_userq_fence_driver_destroy()` now takes the fence spinlock around
  `dma_fence_set_error()`/`dma_fence_signal()` (locked variants).
- **SMU14 VCN utilization fix** (`1055`, amd-gfx ML, Boqun Feng): `gpu_metrics`
  now reports VCN activity as a percentage (`/100`) instead of raw permyriad.
  Our GPU is `smu_v14_0_0`.
- **MGLRU fixes** (`2111`–`2112`, akpm-mm, Kairui Song + Hui Zhu): drop
  redundant unevictable-folio handling; fix young-counter undercount for large
  folios (under-aging hot PMDs). We run `CONFIG_LRU_GEN=y`.
- **zswap reclaim lock contention** (`2113`, akpm-mm, Yunzhao Li/Cloudflare):
  ratelimited cgroup stats flush in `zswap_shrinker_count()` removes 2.88%
  osq_lock contention in the kswapd path.

### Deferred / not taken

- `drm/amdkfd` gfx12 dynamic-VGPR trap handler (08-14, v1, large generated-hex
  change; conflicts on the series).
- `drm/amdgpu` bind-imported-BOs (v3/v4, 08-12/14) — two competing
  same-day revisions still in review.
- `drm/ttm` LRU bulk-move nested-sublist refactor (08-14, v2 under rapid
  revision) — invasive core-TTM change.
- Infinity Scheduler (sirlucjan) — EEVDF mod that conflicts with our sched-ext.
- HDMI 2.1 VRR/ALLM v4 — overlaps carried `0055`; needs the absent
  `amdgpu_dm_connector.c` split.
- Work-items tracker: open reports are firmware/user-space (AV1 artifacts from
  `linux-firmware` 20260810, VRR/blanking via compositor) — no driver-side
  kernel patch to adopt.

---

## [7.2.0-rc7-6-sleepy] — 2026-08-14 (AI-proposed DRM scheduler min_vruntime fix)

Adds `1053` — the **AI-proposed DRM scheduler fix** from the 9070XT fair-policy
regression thread (Luke Wildhardt's AI suggestion, refined by Tvrtko Ursulin):
cache `rq->min_vruntime` on the run-queue instead of re-scanning the entity tree
per add/pop (`drm_sched_rq_get_min_vruntime` removed). Applies to our 7.2-rc7
vruntime tree scheduler — unlike the later full-fair 1047/1048 ML fixups (which
target the 7.3 fair-policy codebase and are not backportable here).

---

## [7.2.0-rc7-5-sleepy] — 2026-08-14 (drm-next 08-12 backports)

Seven new clean backports from the `amd-drm-next-7.3-2026-08-12` tag, surfaced by
the 2026-08-14 six-source sweep (linux-next has no new amdgpu/drm-sched commits
as of `next-20260814`; the GitLab SMU-IF #5538 / RDNA4 MES #5274/#5294 / display
#5343 items remain OPEN with no driver-side fix):

- `1047` drm/amdgpu: don't disable ttm buffer funcs on reset (Pelloux-Prayer).
- `1048` drm/amdgpu: fix missing check in vm_flush() (gfx12 SPM, Deucher).
- `1049` drm/amdgpu: fix nbif 6.3.1 l1 low power not functional (Yang Wang;
  effect muted by our `pcie_aspm=off` !5538 stopgap).
- `1050` drm/amdgpu: keep PRT mappings off the vm_bo state lists (Jesse Zhang;
  fixes the gfx12 userq NULL-bo deref on reset — complements `9038`).
- `1051` drm/amdgpu: skip BOs being torn down during GTT recovery (Yifan Zhang).
- `1052` drm/amdgpu: validate GEM_CREATE domain combinations (Candice Li).
- `1141` drm/amd/display: fix NULL ptr deref in `amdgpu_dm_crtc_set_vblank()`
  (Pitoiset; DCN401 vblank path).

**Not merged:** Tvrtko Ursulin's `[PATCH 0/2] drm/sched: Fair policy fixups`
(2026-08-14) — the two vruntime fixes target the full fair-scheduler codebase
(`drm_sched_policy`, `update_fifo_locked`, `submit_ts`) that 7.2-rc7 and our
carried revert (`1029`–`1046`, FIFO default) do not contain; they do not apply.
Re-enabling fair would require re-applying the whole fair series — deferred,
watching the maintainer direction (fixups vs revert v3).

---

## [7.2.0-rc7-4-sleepy] — 2026-08-12 (conservative SMU/ASPM stopgaps)

Same patch set as `7.2.0-rc7-3`; the built-in CMDLINE gains two conservative
amdgpu-side stopgaps for the silent gaming freeze (SMU IF mismatch 0x2e vs
0x33, work-item !5538): **`amdgpu.aspm=0`** and **`amdgpu.runpm=0`** (no GPU
ASPM or BACO/runtime-PM power transitions; DPM stays enabled so clocks still
downclock at idle). Diagnostic step — if the freeze is SMU power-transition
related, this removes the transition source without running the GPU pinned
at fixed high clocks.

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
