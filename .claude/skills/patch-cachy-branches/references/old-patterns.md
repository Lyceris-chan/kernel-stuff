# CachyOS branch machinery no longer carried

**Archived 2026-10-16.** These branches and patterns were carried by an earlier
version of this skill and are **not** in the series today — the `01xx` range
holds only the squashes listed in the parent skill. Everything below is kept so
a later refresh can re-adopt a branch without re-deriving the method, not
because it is live. Verify each fact against the trees before acting on it; the
branch directories in `repos/sirlucjan-kernel-patches/<line>/` may have moved on
since.

## Contents

- [The `fixes` branch pair — squash whole, then revert off-target](#the-fixes-branch-pair--squash-whole-then-revert-off-target)
- [`hdmi` branch (`0107-cachy-hdmi.patch`)](#hdmi-branch-0107-cachy-hdmipatch)
- [Single-branch squashes](#single-branch-squashes)
- [Removed by user decision](#removed-by-user-decision)
- [`vma_flags_t` compile fix (pre-v12 LRU-MARIE only)](#vma_flags_t-compile-fix-pre-v12-lru-marie-only)
- [Branches evaluated and rejected](#branches-evaluated-and-rejected)

## The `fixes` branch pair — squash whole, then revert off-target

The pattern, worth reusing for any mixed branch: squash the branch **in full**
(co-target hardware included) into one patch, then build a **second patch that
reverts the off-target groups**, so the net applied effect is only what this
machine needs. Keep the branch whole in the squash — do not try to exclude
patches from it — and revert in the pair.

- `0105-cachy-fixes.patch` — full squash of `cachyos-fixes-patches-<ver>-sep`
  (v11 at the time: 25 patches; earlier revisions had 26).
- `0106-cachy-drops.patch` — reverse diff of the off-target groups below.
- Proof of net effect is required after regenerating: diff the pair's net result
  against the intended set, not the two patches separately.

Off-target groups the drop patch reverted:

| Subject keywords | Reason |
|---|---|
| `drm/i915/rc6` | Intel GPU |
| `drm/i915/psr`, `intel_frontbuffer`, `intel_psr.h` | Intel display PSR |
| `bluetooth/btusb`, `Add BT support` | BT dongle IDs not for this hardware |
| `rtw89` | Realtek PCIe WiFi, not our RTL8125 NIC |
| `drm/edid.*DisplayID.*adaptive` | eDP OLED panels — external monitors only |
| `drm/nouveau` | Nvidia OSS — `DRM_NOUVEAU=n` in our config |
| `i2c.*touchpad`, `i2c-core-acpi.*ASUE` | Laptop touchpad |
| `ALSA.*realtek.*internal speakers.*ASUS` | Laptop internal speakers |
| `wifi.*iwlwifi` | Intel WiFi |
| `ASoC.*amd.*acp.*DMI` | ASUS laptop audio DMI overrides (later self-reverted in-branch) |
| `sof.*Dell`, `sof.*XPS` | Intel SoundOpen Firmware |
| `mt76` | MediaTek WiFi |

Kept by the pair (net effect): `x86/cpu/amd` (RDSEED32), `sched/fair`,
`sched/idle`, `sched/core`, USB-core string-descriptor sanitize, `mm/mglru`,
`mm/vmscan`, `drivers/pci/quirks.c` (PCI Skip Target Speed quirk, ~2 s boot on
empty/clamped PCIe slots).

**`0104` is the survivor of this machinery**: the sched/core
`finish_task_switch()` inline patch was extracted from the `fixes` branch
(commit `909c59d8ef23`, part 07/12 of `cachyos-fixes-patches-v6`) and is now
carried alone. The premise for it (Spectre mitigations active, `finish_task_switch()`
core code scx does not bypass) was re-verified for BORE — but note the ledger
records that this pair "was not regenerated at the 7.3 bump, with no reason
recorded", i.e. the drop table above was last proven against 7.2-rc.

## `hdmi` branch (`0107-cachy-hdmi.patch`)

Two conflicts had to be handled inside the squash:

- **`0151` duplicates `0055`** — when
  `0055-drm-edid-parse-HDMI-2.1-gaming-ALLM-VRR-caps-from-HF-VSDB.patch` is in
  the series, the branch's `drm-edid-Parse-more-info-from-HDMI-Forum-vsdb`
  patch adds identical content. Exclude `0151` from the squash input. Check with
  `git apply --check -R <0151 patch>`: if the reverse check passes, it is
  already present.
- **`0053` vs the branch** — `0053` deletes `dc_edid_parser.h`, which the hdmi
  branch still `#include`s via `amdgpu_dm.c`. When a hdmi squash is in the
  series, do not include `0053`.

The branch is not carried today because our own `0050`–`0099` HDMI/EDID patches
cover the same ground.

## Single-branch squashes

- `0108-cachy-preempt-ipi.patch` — `preempt-ipi-patches-<ver>-sep`.
- `0109-cachy-vesa-dsc.patch` — `vesa-patches-<ver>-sep` (vesa-dsc-bpp).
- `0104-cachy-cgroup-vram.patch` — `cgroup-patches-sep`; the number was later
  reused for the sched/core patch above.

## Removed by user decision

- `0112-cachy-amdgpu-avoid-evicting-resources-at-S5.patch` — **removed
  2026-09-21** (user-approved), together with `9007`.
- `0113` — the micro-opts bundle; gone from the range by the same period.

## `vma_flags_t` compile fix (pre-v12 LRU-MARIE only)

When the `fixes` squash (which contains
`mm: vmscan: convert folio_referenced() to use vma_flags_t`) was applied
alongside an older LRU-MARIE, the build failed at `mm/vmscan.c` because MARIE's
`#ifdef CONFIG_LRU_MARIE` block still used the old expression. LRU-MARIE v12
(`2101`) ships the `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` form itself, so
this in-tree edit is only needed for older MARIE revisions:

```c
// Change:
if (referenced_ptes > 0 && (vm_flags & VM_EXEC) && folio_is_file_lru(folio))
// To:
if (referenced_ptes > 0 && vma_flags_test(&vma_flags, VMA_EXEC_BIT) && folio_is_file_lru(folio))
```

It was an in-tree source edit only, never a patch file.

## Branches evaluated and rejected

Recorded with the reason they were rejected at the time; re-check the reason
still holds before re-evaluating (the scheduler is BORE now, so "sched-ext
conflict" reasons in particular need re-reading).

| Branch | Reason |
|---|---|
| `snd-codecs` | laptop audio |
| `t2` | Apple Mac |
| `adios-iosched-default-on` | would change the default I/O scheduler (reason recorded as "sched-ext conflict") |
| `gaming-sched` | reason recorded as "sched-ext conflict" |
| `clang-patches` | LLVM Polly risk |
