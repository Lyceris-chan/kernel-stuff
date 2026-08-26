# Wannabe 7.3-rc1 tree

A preview tree of the upcoming **Linux 7.3 merge window**, built before
7.3-rc1 exists (the release is expected later in 2026). It lets us test and
prepare the 7.3 hardware-relevant changes on our RX 9070 XT / Zen 4 desktop
ahead of the official RC.

## Where it lives

`wannabe-7.3-rc1/` — a **git worktree** checked out from the `linux-next`
repository (`repos/linux-next`) at the **next-20260825** snapshot. The folder
is gitignored (`wannabe-*/`) and not part of the sleepy-kernel PKGBUILD.

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

## Deferred (needs rebase / review / provenance)

- **sirlucjan reflex 0.3.1r2** CPU governor — sched-ext-aware but the
  `cpufreq_driver_adjust_perf` API changed (4→5 args); needs a port and
  review. Brand-new single-maintainer patch.
- **Work-items #5616 / #4753**: DCN4 flip_done Atomize-GLOBAL_SYNC_STATUS
  fix (WIP tracker attachment, 7.2-based, needs rebase) and FAMS2
  mclk-stutter workaround (community, no upstream provenance).
- **ML-only series** (08-19..08-25): userq GPU-reset crash/lockdep 5-patch,
  KFD SDMA oversubscription GFX12, userq UAPI query/LIST/MODIFY — mostly
  superseded by the amd-staging merges or awaiting v2+; cherry-pick the
  on-target pieces when they land upstream.

## Rebuild instructions

```bash
# refresh from linux-next
git -C repos/linux-next fetch origin
git -C repos/linux-next worktree add wannabe-7.3-rc1 next-YYYYMMDD
# then merge the toMerge list (see the 08-26 sweep record in PATCH_SOURCES.md)
```

The tree is not part of the PKGBUILD build; it is a preview/development tree.
