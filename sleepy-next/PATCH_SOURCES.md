# sleepy-next — patch provenance

`linux-sleepy-next` builds the **wannabe 7.3-next preview** kernel from the
linux-next **next-20260825** snapshot + the sleepy 7.2 patch series (the same
patches the `linux-sleepy` 7.2 build uses) + the clean upstream HDMI VRR/ALLM
patches. See `../PATCH_SOURCES.md` (the 7.2 ledger) for the 173 shared patches
— every one is the identical, traceable 7.2 series file (CachyOS squashes,
upstream ML patches, agd5f backports, local patches).

## Base

- `next-20260825` snapshot (the 7.3 merge-window content).
- Toolchain: official **LLVM 23.1.0** release from the llvm-project GitHub
  release (the prebuilt binary links ICU 70; Arch ships ICU 78, so the ICU 70
  libs are bundled via `llvm-icu70-libs.tar.gz`).

## Excluded from the 7.2 series

- **`0107-cachy-hdmi`** — the CachyOS HDMI branch. The 7.3 base already has the
  clean upstream HDMI path (`dc_edid_parser` + `amdgpu_dm_update_freesync_caps`
  in the split connector file + FRL fixes). Shipping it would conflict.
- **LRU-MARIE (`2101`)** — 0.10.5 does not port to 7.3 (12+ hunks fail across
  huge_memory/rmap/vmscan/page_io). Skipped cleanly by `patch --forward`;
  re-evaluate when a 7.3 port exists.

## Added (clean upstream, vanilla)

The HDMI 2.1 VRR + ALLM v4 series (amdgpu-side, amd-gfx ML 2026-08), replacing
the earlier squash — each is the original submission:

| Patch | Author | ML Message-ID | Content |
|---|---|---|---|
| `0059` | Fangzhi Zuo | `150622` (lists.freedesktop.org amd-gfx 2026-August) | Add 2.1 FreeSync support for AMD VSDB EDID Block — `SIGNAL_TYPE_HDMI_FRL` FreeSync + VTEM info packet |
| `0060` | Fangzhi Zuo | `150623` | Add HDMI 2.1 VRR support from HF-VSDB — VRR-range fallback when the AMD VSDB has none |
| `0061` | Fangzhi Zuo | `150621` | Enable HDMI ALLM for Gaming-VRR — `ALLM_Mode` in the HF-VSIF |

The drm/edid part of the series (`150619`, HF-VSDB gaming caps) is already
present as `0055` (the 7.2 series' Fangzhi Zuo HF-VSDB patch).

## Verification

Every patch is applied with `patch -p1 --forward -F2` and a dry-run check:
patches that do not apply cleanly to next-20260825 (e.g. MARIE) are skipped
entirely, never half-applied. The VRR/ALLM series is verified to apply on
next-20260825 + the 0050s, with the HF-VSDB VRR fallback and
`drm_connector_attach_vrr_capable_property` present in the built kernel.

## Added (Phoronix 08-11 WIP — RFC, 7.4-target)

The `mm/gup` follow_page_mask() batching series (Rik van Riel, Meta; RFC v3,
lkml `20260811025157.1632867-1-riel@surriel.com`) — up to 12.8× in gup_test on
mTHP paths (GPU userptr, io_uring, VMA walkers). Phoronix 08-11 "Up To 12.8x
Improvement Observed For gup_test". Not in next-20260825 (targets 7.4);
applies cleanly. 8 patches, `2120`–`2127`, each with the original
From:/Signed-off-by: (Rik van Riel) preserved. Marked RFC — re-evaluate when
it lands upstream (7.4).

## Added (local fix, 2026-08-26)

- **`0040`** — drm/amd/display: fall back to DRM-core AMD VSDB FreeSync info.
  The amdgpu-side `parse_hdmi_amd_vsdb()` relies on the DMUB/DMCU firmware to
  report the AMD VSDB; on RDNA4 the firmware does not detect it, leaving
  `vrr_capable=0` even for displays that advertise FreeSync via the AMD VSDB
  (verified: modetest `vrr_capable: 0` on an HDMI display whose EDID has AMD
  VSDB v2, Feature Caps 0x09, 48-120 Hz). `drm_edid.c` (patch `0050`) already
  parses the AMD VSDB kernel-side into `connector->display_info.amd_vsdb`
  (`freesync_supported`, `min/max_frame_rate`) for v1/v2/v3 — use it as a
  fallback in `amdgpu_dm_update_freesync_caps()` when the firmware path found
  nothing. Local fix (Sleepy + Claude-assisted), applies on top of the
  VRR/ALLM series.

## Fixed (cmdline, 2026-08-26) — DCN401 "box/square" artifact

Not a patch: `amdgpu.dcdebugmask=0x800` (`DC_DISABLE_IPS`) added to the
built-in CMDLINE in `PKGBUILD`. On DCN401, IPS/DPG pipe-gating sets
`hubp->power_gated`, making `hubp2_is_flip_pending()` return `false` while a
flip is still pending → the VUPDATE_NO_LOCK flip-event handler delivers the
completion before HW latches → the compositor re-paints a buffer still being
scanned → a fixed content-tracking square over app windows (the sleepy-next
"box", absent from compositor screenshots). Matches AMD drm/amd work item
#5570 class. A/B verified 2026-08-26: `0x20000` (FAMS) and `0x8` (clock
gating) did not help; `0x800` (IPS off) fixed it. Re-evaluate when a proper
DCN401 flip-pending fix lands upstream.

## Added (2026-08-27) — zstd BMI2 probe series (Usama Arif, Meta)

`2128`–`2130`, "zstd: probe the CPU for BMI2 support once, not per context"
(lkml `20260826122558.2662013-1-usama.arif@linux.dev`, via the lkml
public-inbox git mirror — lore.kernel.org web is Anubis-blocked, the
`repos/lore-mirror` epoch-20 clone is the working access path). Three patches
on `lib/zstd`:
- `2128` — `ZSTD_initStaticCCtx()` routes its BMI2 probe through
  `ZSTD_cpuSupportsBmi2()` (requires BMI1+BMI2, matching the dynamic-dispatch
  bodies; latent inconsistency, no field-visible change).
- `2129` — `ZSTD_cpuSupportsBmi2()` returns 0 when `DYNAMIC_BMI2` is unset
  (nothing reads the flag in static dispatch).
- `2130` — probe the CPU once and cache the result with READ_ONCE/WRITE_ONCE
  instead of re-probing per context.

Relevant: this kernel ships `CONFIG_ZSTD_COMMON/COMPRESS/DECOMPRESS=y` (zram/
zswap use zstd). Original `From:`/`Date:`/`Subject:`/`Signed-off-by:` headers
kept intact (mailing-list noise headers trimmed). Applies cleanly to
next-20260827 with `patch -p1 --forward -F2` (cumulative order 2128→2129→2130).

## Added (2026-08-27 sweep — 20 patches)

Fresh 08-26/27 ML submissions found in the lkml public-inbox mirror
(`repos/lore-mirror`) and the amd-gfx/dri-devel August archives. All apply
cleanly to next-20260827 with `patch -p1 --forward -F2` (verified in series
order) and keep original headers/Signed-off-by.

- **`1210`–`1224` — ACPI: CPPC v5 (15 patches)**, Christian Loehle (arm.com),
  lkml `2026082711…`. Reworks the CPPC control path amd-pstate runs on Zen 4:
  validate `_CPC` packages, propagate control-write errors, serialize PCC
  payload updates (single-reg + EPP), 64-bit register masks, reject unsafe
  cross-CPU SystemMemory RMW, lifetime-leak fixes. High value for our
  `amd_pstate.epp_boost=1` setup.
- **`1141`–`1143` — drm/amd/display** (NepNep7601, amd-gfx ML 08-27): skip
  receiver power control without AUX; close DDC on I2C engine setup failure;
  fall back to software I2C on hardware engine failure. Display-link power
  sequencing + DDC/I2C robustness on the shared path.
- **`1059` — drm/amdgpu: restrict BAR0 fallback read to SR-IOV VFs only**
  (Mario Limonciello, amd-gfx 08-26, `Cc: stable`). Early-init boot-path
  regression fix (`Fixes: ea8ac194077d`).
- **`2005` — sched_ext: skip per-CPU data allocation for built-in DSQs**
  (Qiurong Fang, lkml 08-27). Relevant to `CONFIG_SCHED_CLASS_EXT=y`.

Deferred (tracked, not merged): the 30-patch Alex Deucher **TLB-invalidation
v2** upgrade of `1004`–`1017` (under review; swap in a dedicated session);
gfx12 mes_dbgext; job-based IB refactor; blend-mode v4 (drm-helper piece).

## Added (2026-08-28 — second sweep window, 8 patches)

Fresh 08-27/28 finds from the amd-staging-drm-next branch (agd5f) and the
amd-gfx ML. All verified `patch -p1 --forward -F2` against next-20260828.

- **`9049` — drm/amdgpu: recompute dw estimate after allocating a new VM
  update job** (YuBiao Wang, `Cc: stable`). Stale free-dw count after job
  realloc can encode a 1 GB copy inside the IB pool → GART fault + ring hang.
  Coexists with our `9034` (same file, no hunk overlap).
- **`9050` — drm/amdgpu: Update no-retry PTE flags for GFX12** (RDNA4 gfx12.0).
- **`9051`/`9052` — DCN4 flip-schedule pair** (Unify + Fix CalculateFlipSchedule):
  flip-path bandwidth calc; relevant to the VUPDATE_NO_LOCK "box" class.
- **`9053` — DCN42 IPS1 rIOMMU hang fix** (DCHVM↔rIOMMU SDP port disconnect).
- **`9054` — Guard amdgpu_dm_irq_schedule_work against NULL irq_wq** (teardown race).
- **`1144` — drm/amd/display: Enable HDMI FRL by default** (Jerry Zuo, v2,
  `20260827155409.1426730-1`, Reviewed-by Harry Wentland). Adds `DC_FRL_MASK`
  to the default `amdgpu_dc_feature_mask` so HDMI 2.1 FRL is on.
- **`1060` — drm/amdgpu: cancel hang_detect_work before taking userq_mutex**
  (Vitaly Prosyak, `20260827222531.127950-1`, Reviewed-by Christian Koenig).
  Deadlock fix on the gfx12 userq path.

Note: next-20260828 upstreams ~18 more amd-staging commits (the ones we had
backported as `1054`, `9043`, `9045`, `9047`, `9048` are now redundant; `1026`
needs a rebase to drop the duplicate guard while keeping the CRIU callbacks).
The remaining pending amd-staging content is off-target (GC12.1/datacenter,
SMU15, DCN5/6) or refactor — nothing else worth carrying this window.

## Cleanup (2026-08-28, pkgrel 10)

Dropped **76 patches** whose content next-20260828 now upstreams (verified by
`patch -p1 --forward -F2 -R` reverse-apply against the base): `1000`-`1002`,
`1019`, `1024`, `1047`, `1050`, `1051`, `1101`-`1104`, `1106`-`1111`,
`1113`-`1115`, `1117`-`1126`, `1129`-`1133`, `1137`-`1139`, `1200`, `1205`,
`1207`, `1208`, `2102`-`2105`, `2108`-`2119`, `9001`-`9003`, `9006`, `9009`,
`9010`, `9030`, `9031`, `9032`, `9036`, `9042`, `9043`, `9048`, plus the
superseded `1054`, `9045`, `9047` (base has refined revisions) and `9053`
(DCN42 rIOMMU — already in base). `1026` (GFX12 CRIU callbacks) applies
cleanly and is kept. Fixed the six `9049`-`9054` amd-staging patches that were
accidentally empty (re-extracted via `git format-patch` from agd5f; `9053`
dropped as redundant). `source=()` now matches on-disk exactly (143 patches).

## Sweep 2026-09-02 — base bump to next-20260901, no new fixes worth carrying

Full source re-check (linux-next next-20260901 fetched; amd-gfx + dri-devel
2026-September archives; lkml mirror; drm/amd work-items tracker; CachyOS /
sirlucjan / firelzrd; x86/security line). Findings, all **deferred/not carried**
with reasons:

- **LRU-MARIE 0.11.0** (firelzrd, 2026-08-31) — fetched. Does NOT port to the
  7.3-merge-window base (both 0.10.5 and 0.11.0 fail `patch` against
  next-20260828/0901: the mm memcg soft-limit removal shifted
  memcontrol.h/vmscan.c). Our carried 2101 (0.10.5) is itself skipped by the
  build for the same reason. Needs a dedicated 7.3 port before it can land.
- **"passive VRR" series** (Jerry Zuo / Fangzhi Zuo + Tomasz Pakuła, v1
  2026-09-01, `20260901191251.2653684-1`, dri-devel) — a NEW feature (keeps
  sinks in their variable-refresh state during desktop/fixed-refresh use to
  avoid HDMI blanking flicker), not a fix; touches DRM core + the 7.3 split
  amdgpu_dm files; not in next-20260901. V1 unreviewed; our VRR already works
  (HF-VSDB freesync_capable via 0059-0061/0063). pvr-01/pvr-03 apply clean,
  pvr-02 needs a manual rebase. Deferred — re-evaluate on a v2/review.
- **drm/amd/display cursor-disable w/ horizontal split planes** (yulingli,
  08-31) — cursor fix; targets horizontal-split (ultrawide/ODM) configs, not
  our 1920x1080 layout; not carried.
- **Work items**: #5709 (HDMI FRL link-training fail on DPMS wake), #5717
  (NAVI48/RX 9070 XT evicted-surface corruption) — open, no landed fix
  referenced; track. #5616/#5705 flip_done class still open (no new fix).
- CachyOS fixes v5 = cosmetic (HID touchpad); cachyos-linux/build forks stale.
- x86/security: nothing new for Zen 4 since 08-01.

Net: no new AMD fixes worth carrying this window; bumped base to
`next-20260901` for the current mm/mglru + 7.3-rc1 content.

## Dropped (2026-09-02) — 20 non-applying patches removed from sleepy-next

These 20 patches target the vanilla-7.2 / 7.2-era base and do NOT apply to the
7.3-merge linux-next base (the build was skipping them — verified: each fails
`patch -p1 --forward` and does NOT reverse-apply). Removed from source=() and
disk so the series only carries patches that actually apply:
`0008` (SMU14 power-limit), CachyOS `0104`-`0113` 7.2-only squashes that don't
port (cgroup-vram, fixes, drops, preempt-ipi, vesa-dsc, micro-opts), `1003`
(gfx12 KCQ remap), `1023` (min_power_limit), `1057` (ttm BO ref), `1100`/
`1105`/`1116`/`1127`/`1128` (DCN4/42b backports the base's newer DCN4 code
supersedes), `1206`/`1209` (amd-pstate EPP — base CPPC v4+ path differs),
`2106`/`2107` (zram OOB — base zram rewritten), `9041` (userq doorbell xa-lock
— base userq evolved). `2101` (MARIE 0.10.5) retained pending the 0.11.0 port.
Series now 123 patches.

## Ported (2026-09-02) — LRU-MARIE 0.11.0 onto next-20260901 (replaces 2101 0.10.5)

`2101` is now the **ultracode-ported LRU-MARIE 0.11.0** for the linux-next
7.3-merge base (firelzrd's vanilla-7.2 patch does NOT apply to next-20260901;
a multi-agent recon/port/verify pass base-fit it). The 7.3 base diverged:
`mm/swap.c` content moved to `mm/folio.c`, `struct alloc_context` moved to
`mm/page_alloc.h`, `page_io.c` was rewritten around `struct swap_io_ctx`
(the old `swap_iocb**` per-folio path is gone), vma_flags became
`vma_flags_t`, and the memcg soft-limit rbtree was removed. Port notes:
- swapout batching delivered via the base's native ctx/bio coalescing (not
  MARIE's removed `do_swapout_batch`); kcompressd kthread + store/drain +
  nr_swap_write_failed early-OOM gate all present.
- `FOLIOREF_RECLAIM_CLEAN` enum restored (base removed it); `vm_flags & VM_EXEC`
  fixed to the base's `is_exec_file_folio`/vma_flags_t API.
- 3 compile fixes applied: `#include "../swap.h"` (state_reclaim.c, for
  mem_cgroup_swappiness), `#include "../page_alloc.h"` (defrag.c, for
  buddy_order/post_alloc_hook), and 4-arg `post_alloc_hook(..., ALLOC_DEFAULT)`
  in defrag_compat.h. Verified: applies clean (`patch -p1 --forward`, 0 rejects)
  and the mm/ subtree builds (gcc) with these fixes.
- Runtime invariants (kcompressd folio_get/drain balance, queued-folio locking
  across the keep path) match base semantics but need real boot testing.
