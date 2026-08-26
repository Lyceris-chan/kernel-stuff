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
