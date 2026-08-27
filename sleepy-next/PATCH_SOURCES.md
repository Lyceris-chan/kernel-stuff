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
