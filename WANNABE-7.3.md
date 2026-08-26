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

## Phoronix check result (month through 08-25)

Scanned the full month's kernel articles for on-target items:

- **In base (verified in tree)**: SMP-IPI preemption (17 & 22 Aug),
  `flush_tlb_multi` preemption (22 Aug), TTM-aggressive (07 Aug),
  amd-pstate dynamic-EPP per-policy + epp_boost (28 & 31 Jul),
  sched-ext feature-complete (22 Aug), zsmalloc/rmap_walk_ksm MM (19 Aug).
- **WIP merged** (this tree): `follow_page_mask()` batching (11 Aug).
- **Off-target / not applicable**: menu-governor 5× wakeup (Intel Xeon; we
  run the NAP governor), RTL8261C/D 5 GbE (we have RTL8125B/r8169), DRM
  scheduler fair-policy fix (we default FIFO; upstream reverted fair),
  HDMI 2.1 VRR/ALLM (missed 7.3, WIP — deferred), k10temp per-CCD
  (EPYC Zen 5 only).

## Deferred (needs rebase / review / provenance)

- **sirlucjan reflex 0.3.1r2** CPU governor — sched-ext-aware but the
  `cpufreq_driver_adjust_perf` API changed (4→5 args); needs a port and
  review. Brand-new single-maintainer patch.
- **Work-items #5616 / #4753**: DCN4 flip_done Atomize-GLOBAL_SYNC_STATUS
  fix (WIP tracker attachment, 7.2-based, needs rebase) and FAMS2
  mclk-stutter workaround (community, no upstream provenance).
- **HDMI 2.1 VRR/ALLM** (AMD, amd-gfx ML): will miss 7.3; re-evaluate when
  they land.
- **ML-only series** (08-19..08-25): userq GPU-reset crash/lockdep 5-patch,
  KFD SDMA oversubscription GFX12, userq UAPI query/LIST/MODIFY — mostly
  superseded by the amd-staging merges or awaiting v2+; cherry-pick the
  on-target pieces when they land upstream.

## Rebuild instructions

```bash
# refresh from linux-next
git -C repos/linux-next fetch origin
git -C repos/linux-next worktree add wannabe-7.3-rc1 next-YYYYMMDD
# then re-apply the three merge layers (see the 08-26 sweep record in PATCH_SOURCES.md)
```

The tree is not part of the PKGBUILD build; it is a preview/development tree.
