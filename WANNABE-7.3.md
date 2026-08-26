# Wannabe 7.3-rc1 tree

A preview tree of the upcoming **Linux 7.3 merge window**, built before
7.3-rc1 exists (the release is expected later in 2026). It lets us test and
prepare the 7.3 hardware-relevant changes on our RX 9070 XT / Zen 4 desktop
ahead of the official RC.

## Where it lives

`wannabe-7.3-rc1/` — a **git worktree** checked out from the `linux-next`
repository (`repos/linux-next`) at the **next-20260825** snapshot, on branch
`wannabe-7.3`. The folder is gitignored (`wannabe-*/`) and not part of the
sleepy-kernel PKGBUILD.

History (bottom → top):

1. `a8406e6c0b79` — **base**: `next-20260825`.
2. `759b7fb8fbe9` — **18 upstream merges** (amd-staging + drm/sched lock).
3. `4834e3546e26` — **69 sleepy-kernel additive patches** (CachyOS + local).
4. `7afdec79e9f0 … 6c2092bc8448` — **8 RFC gup-batching commits** (Phoronix
   WIP, Rik van Riel).
5. `5ea4142645e4` — **3 upstream HDMI 2.1 VRR/ALLM v4 commits** (clean
   HDMI, amd-gfx ML).
6. `cd4af3bd9966`, `9d45255b110d`, `89caac2e1573` — **3 ML WIP merges**
   (userq GPU-reset 5-patch + BO-bind + KFD queues-reset).

## What the base already contains

`next-20260825` is the current 7.3 merge-window content. Already present in
the base (no backport needed — they arrive with the real 7.3 bump):

- **amd-drm-next-7.3-2026-08-19 merge**: bulk AMD display/amdgpu changes
  (pipeline-sync-without-VM-fence, userq destroy hang/race, KIQ ring fence
  completion, VCN dec_msg overflow, brightness curve, userq duplicate-BO
  locks, VA-map-before-restore).
- **amdgpu userq**: wptr/rptr validation, MES ring fence completion,
  sysfs ip-base, autosuspend cleanup.
- **Memory management**: ~30 commits — MGLRU (unevictable, young-counter,
  exec-folio promote), vmscan (lru_lock contention, pgrotate, swappiness,
  folio_referenced→vma_flags_t), zram (OOB fixes, params, zstd), zsmalloc
  handle size, zswap ratelimit, swap single-folio revert, memcg LRU reparent.
- **sched-ext**: `scx_bpf_dsq_move()` fix, sleepable `cgroup_set_bandwidth`,
  header syncs.
- **sch_cake**: autorate reconfiguration throttling (net-tune CAKE).
- **amd-pstate 7.3 set**: `min_limit_freq` from `bios_min_perf`, dynamic EPP
  as `energy_performance_preference`, CPPC hot-path (desired_perf reads,
  full-width register access), `amd_dynamic_epp` cmdline removed.
- **SMP / x86-mm latency series (Phoronix 08-17/08-22)**: ByteDance SMP-IPI
  preemption rework (`smp-core-2026-08-17`: task-local IPI cpumask, preempt
  re-enabled before the wait — ~90% scheduling-latency drop) plus the
  `x86_mm_for_7.3` TLB flush series (preempt around `flush_tlb_multi()`,
  stack `flush_tlb_info`).
- **TTM aggressive eviction (Phoronix 08-07, Valve)**: "be more aggressive
  when allocating below protection limit" + shared-limit-pool.
- **k10temp per-CCD** for EPYC Zen 5 Turin (in base; EPYC-only — harmless for
  the single-CCD 7700).

## What we merged on top (commit `759b7fb8fbe9`)

Hardware-relevant 7.3-window commits **not yet in next-20260825**, cherry-picked
from the source repos:

- **amd-staging-drm-next (17)**: KFD CRIU restore_mqd NULL guard, userq
  fence-lock + wptr-restore, MES process-context teardown, SVM migrate
  error-path + hole-range, AQL zero-size reject, CU-occupancy GFX12,
  no-retry PTE flags, VM dw-estimate recompute, DCN42 min-dispclk ODM,
  OPP/DPP accounting, dc_lock leak on reset, DM IRQ NULL guard, dml2 bpp,
  vblank_nom, mes_userqueue indenting, HPD IRQ logging.
- **drm/sched**: lock `drm_sched_entity_is_idle()` (data-race fix, fuzz-3
  apply).

## Sleepy-kernel additive series (commit `4834e3546e26`)

The 69 patches we already carry on the 7.2 build (CachyOS branch squashes +
handmade local fixes), applied so the wannabe tree is a superset of today's
build — **not just upstream 7.3 content**:

- **CachyOS**: `0101` bbr3, `0103` kbuild flags, `0104` cpu-isa,
  `0105` config-hooks + fixes, `0106` off-target drops, `0108` preempt-ipi
  (SMP preemption + TLB flush), `0109` ACPI bus-master / S5-eviction, plus
  the `0110`–`0113` CachyOS-fork backports.
- **Local GPU (0001–0049)**: PROFILE_PEAK power profile, SMU14 fixes,
  DCN/EDID, TLB-invalidation, retry-fault series, userq fixes, MES CRIU,
  VCN utilization, soft-evicted tracking.
- **Schedulers**: `2000`-range bfq / mq-deadline.
- **MM (2100-2199)**: LRU-MARIE 0.10.5 (`mm/lru_marie/`), zstd, zswap batch.
- **CPUIdle**: NAP governor (`drivers/cpuidle/governors/nap/`).

## Phoronix 08-11 WIP merge (commits `7afdec79e9f0…6c2092bc8448`)

Rik van Riel's (Meta) **`mm/gup` follow_page_mask() batching** RFC — up to
**12.8× in gup_test** (mTHP-heavy paths, GPU userptr / io_uring / VMA walkers
benefit). RFC **v3** (lkml `20260811025157.1632867-1-riel@surriel.com`)
applies cleanly to next-20260825 (8 patches, `git am`). Benchmark (gup_test
`-L -m 256 -n 65536 -r 16 -t`): 64 kB mTHP 2946→231 µs, 4 kB 2753→1198 µs,
2 MB flat. Authored by Rik van Riel, suggested by David Hildenbrand,
`Assisted-by: Claude:claude-opus-4-8`. Still RFC (v4 posted 07-24 as part of
a wider series) — expect upstream revisions to supersede these commits; the
wannabe tree marks the merge point so they're easy to drop.

## ML WIP merges (commits `cd4af3bd9966`, `9d45255b110d`, `89caac2e1573`)

Additional amd-gfx ML series (08-24/08-25) that apply cleanly to
next-20260825, merged as isolated commits so they're easy to drop when they
land upstream:

- **userq GPU-reset crash + lockdep 5-patch** (Vitaly Prosyak, `151398`–
  `151403`): reserve a dma_resv slot before adding the eviction fence,
  cancel `hang_detect_work` before `userq_mutex` (deadlock), take the reset
  lock after `halt_activities`, skip `firmware.mutex` in `psp_resume` during
  GPU reset, move `drm_client_dev_resume` outside `reset_domain->sem`.
- **BO-bind for imported BOs** (v5, `151460`): `amdgpu_evf_mgr_attach_fence`
  validates imported (dmabuf) BOs even when the eviction fence is signaled,
  so VMs using user queues can bind them.
- **KFD mark queues as reset** (`151019`): after a full GPU reset the MES
  queue table is wiped; mark queues as reset so teardown doesn't try to
  remove them from MES again (gfx1201 is MES-based).

## Clean 7.3 HDMI (commit `5ea4142645e4`) — upstream VRR/ALLM, no CachyOS fluff

The base (`next-20260825`) carries the clean upstream 7.3 HDMI path:
`dc_edid_parser` (DC-level EDID parser, used by `amdgpu_dm_connector.c`),
`amdgpu_dm_update_freesync_caps()` in the split connector file, freesync
module HDMI support, and the FRL fixes from the `amd-drm-next-7.3-2026-08-06`
pull (FRL rate/FFE caps, gated FRL polling — incl. our old `1113`/`1119`).
On top we merged the **HDMI 2.1 VRR + ALLM series v4** (amd-gfx ML,
2026-08, `150619`–`150623`), the three amdgpu-side patches that apply
cleanly: `SIGNAL_TYPE_HDMI_FRL` FreeSync + VTEM packet (Fangzhi Zuo),
HF-VSDB VRR-range fallback when the AMD VSDB has none, and `ALLM_Mode` in
the HF-VSIF when Gaming-VRR is active (HDMI 2.1 §7.6.6). The drm/edid part
(`150619`) is already present as our additive `0055` (functionally identical
to v4 2/4). The **CachyOS `0107` hdmi squash contributed nothing to this
tree** — the 7.3 base supersedes it (all 11 shared files unchanged; the
squash is only meaningful on 7.2, where the amdgpu_dm split is absent).
Series targets 7.4; isolated and easy to drop when it lands upstream.

**Why `0107` stays in the 7.2 PKGBUILD series (and the ML HDMI can't replace
it there):** the ML VRR/ALLM v4 patches 1/4, 3/4, 4/4 target
`amdgpu_dm_connector.c` / `amdgpu_dm_freesync.c` — the 7.3 amdgpu_dm split.
Verified against `repos/linux-7.2`: those files are absent (monolithic
`amdgpu_dm.c`), so p1/p3/p4 fail `git apply --check`; only p2 (drm/edid,
= our `0055`) applies. On 7.2, `0107` is the workable HDMI FreeSync/VRR
path (dc_edid_parser exists on 7.2 too, wired into monolithic amdgpu_dm.c)
and is proven good (work-item #5649: CachyOS 7.2 HDMI works where vanilla
doesn't). Clean ML HDMI is a 7.3+ path — already adopted here.

**Leo Li (`sunpeng.li@amd.com`) display fixes — in the base (verified):**
402 commits from Leo Li in next-20260825, including the flip_done work that
work-item #5616 references: "Fix flip-done timeouts on mode1 reset"
(`82730dba0cf9`), "consolidate DCN vblank/flip handling onto
vupdate_no_lock" (`c87e6635d2db`), "check GRPH_FLIP status before sending
event" (`f64a9be56536`), "Exit idle optimizations before programming"
(`8419331e64d9`). Not backported to the 7.2 series (7.3-window display
refactor — same amdgpu_dm-split reason as HDMI); they arrive with the 7.3
bump.

## FAAA / Phoronix month audit (290 articles, through 08-26)

Scanned the full Phoronix month index (`/home/sleepy/Desktop/FAAA`) plus the
amd-gfx and dri-devel MLs, work-items tracker, sirlucjan, and firelzrd:

- **In base (verified in tree)**: SMP-IPI preemption (17 & 22 Aug),
  `flush_tlb_multi` preemption (22 Aug), TTM-aggressive (07 Aug),
  amd-pstate dynamic-EPP per-policy + epp_boost (28 & 31 Jul),
  sched-ext feature-complete (22 Aug), zsmalloc/rmap_walk_ksm MM (19 Aug),
  SMU14 fixes + OD-PPT (`93bd6de5518d`), AMD VSDB parse + FRL fixes.
- **WIP merged** (this tree): `follow_page_mask()` batching (11 Aug),
  HDMI 2.1 VRR/ALLM v4 (07-30→08-26 series).
- **MARIE LRU**: **0.10.5 is current** — firelzrd repo at the same
  `55d2c27` commit, sirlucjan has no 7.3 dir yet. No update.
- **zstd**: our `2100` already includes the gcc<11.4 segfault workaround;
  sirlucjan's new `zstd-dev-patches-v2` is the same merge reorganized.
- **Work items worth tracking**: **#5693** (RX 9070 XT VCN-unigate + SMU
  deadlock → Mode 1 reset on hw video decode, created 08-25 — no fix yet),
  #5649 (HDMI FRL blanking on 4k TVs — CachyOS 7.2 known-good, RDNA3),
  #5671 (RX9070XT link-2 enable fail), #5656 (HDMI IEC958 passthrough).
- **Candidates not merged (review)**: amd-gfx `[PATCH 00/30] Rework GPU TLB
  invalidation` (Alex Deucher, gmc12 MES/SDMA pasid TLB — 30 patches, v1,
  major rework that supersedes our TLB series; defer to the 7.4 window,
  watch `agd5f tlb_inv_rework`); dri-devel MMIO-TLB fallback RFC v3 (S4
  KIQ-wedge) — **dropped by its author**; `151407` keep-userq-manager —
  **rejected by Christian König**.

## Repo + work-items re-check (08-26)

- **Repos**: linux-next still at `next-20260825` (our base is current);
  drm-next HEAD 08-24 and linux-pm HEAD 08-18 are in base;
  amd-staging-drm-next tip `75a5e1b6b` (08-12) is exactly our Layer-1
  cherry-pick — no newer on-target commits (post-08-12 content is GC 12.1 /
  NPS / datacenter, off-target for gfx1201).
- **Work items re-scan**: nothing new actionable. The **flip_done timed out
  on RX 9070 XT** cluster (#5616, #5625, #5647, #5696) is an open bug — the
  amd-drm-next-7.3 merges already carry the DCN flip_done/atomize fixes.
  **#5693** (VCN ungate + SMU deadlock → Mode 1 reset, created 08-25) still
  has no referenced fix — tracked. #5695 (DCN401 RA24 format), #5671 (link-2
  enable) — open, no fixes.
- **sirlucjan**: new `zstd-dev-patches-v2` (same merge as our `2100`), aufs
  + handheld (off-target). No 7.3 dir yet.
- **Off-target**: menu-governor 5× wakeup (Intel Xeon; we run NAP),
  RTL8261C/D 5 GbE (RTL8125B/r8169), DRM fair-policy fix (FIFO default),
  k10temp per-CCD (EPYC only), UALink (datacenter), aufs/handheld
  (sirlucjan new — off-target).

## Deferred (needs rebase / review / provenance)

- **sirlucjan reflex 0.3.1r2** CPU governor — sched-ext-aware but the
  `cpufreq_driver_adjust_perf` API changed (4→5 args); needs a port and
  review. Brand-new single-maintainer patch.
- **Work-items #5616 / #4753**: DCN4 flip_done Atomize-GLOBAL_SYNC_STATUS
  fix (WIP tracker attachment, 7.2-based, needs rebase) and FAMS2
  mclk-stutter workaround (community, no upstream provenance).
- **`mm/gup` follow_page_mask v4** and **GPU TLB invalidation rework
  (`151442`)** — bigger series, review before merging.
- **ML-only series** (08-19..08-26): userq GPU-reset crash/lockdep 5-patch
  (`151398`), KFD SDMA oversubscription GFX12, userq UAPI query/LIST/MODIFY
  — mostly superseded by the amd-staging merges or awaiting v2+; cherry-pick
  the on-target pieces when they land upstream.

## Rebuild instructions

```bash
# refresh from linux-next
git -C repos/linux-next fetch origin
git -C repos/linux-next worktree add wannabe-7.3-rc1 next-YYYYMMDD
# then re-apply the three merge layers (see the 08-26 sweep record in PATCH_SOURCES.md)
```

The tree is not part of the PKGBUILD build; it is a preview/development tree.
