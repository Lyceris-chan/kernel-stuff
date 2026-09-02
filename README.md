# linux-sleepy-next

`linux-sleepy-next` is a custom Arch Linux kernel built for one machine: an AMD
Zen 4 desktop with an RDNA 4 graphics card. It is based on a **linux-next**
snapshot (the 7.3 merge-window content) and layers a sanitized
[CachyOS](https://github.com/CachyOS/linux-cachyos) patchset plus targeted
local and upstream patches on top. The older 7.2 `linux-sleepy` kernel this
descends from was retired on 2026-09-02.

**Running kernel:** `7.3.0-rc1-13-sleepy-next-20260902`
**Artifact:** `linux-sleepy-next-20260902-13-x86_64.pkg.tar.zst`

This is not a general-purpose kernel; the configuration is opinionated for the
hardware below.

## Target audience

This kernel targets enthusiasts who want the latest AMD display and power fixes
for a single desktop, value low-latency networking (BBR3 + CAKE SQM), and want
maximum per-core throughput. Running it on other hardware is unsupported.

## Target hardware

| Component | Hardware | Kernel support |
|---|---|---|
| CPU | AMD Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14` |
| NIC | Realtek RTL8125B 2.5 GbE | In-kernel `r8169` driver |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline` schedulers |
| Scheduler | sched-ext BPF schedulers | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

## Highlights

- **Clang ThinLTO with `-O3` and `-march=znver4`.** The kernel compiles with a
  pre-built LLVM toolchain from kernel.org (`CC=clang LD=ld.lld LLVM=1
  LLVM_IAS=1`). See [Build](#build).
- **LRU-MARIE page eviction** carried as a strict 1-to-1 rebase of the author's
  0.11.0 patch (SIMD young-bit walker, async compression, bio-coalesced
  swapout, early-OOM gate).
- **`mm/gup` folio batching** (Rik van Riel's `follow_page_mask()` RFC series)
  for large-folio page-fault throughput.
- **BBR3** is the compiled-in TCP default, with CAKE SQM shaping available via
  `net-tune`. ACPI CPPC hardening and per-core EPP boost stabilize `amd-pstate`
  on Zen 4.
- **DCN4 display work** for the RX 9070 XT: FreeSync/VRR and HDMI 2.1 support,
  FRL fixes, DET/pipe handling, and the Idle-Power-State fix for the scanout
  "box" artifact.
- The NAP cpuidle governor, sched-ext schedulers, and a stripped config
  (no Intel/NVIDIA DRM, IIO, InfiniBand, ISDN, CAN).

## What this kernel adds

This package layers the CachyOS patchset and targeted upstream/local patches on
a linux-next snapshot. `PATCH_SOURCES.md` is the authoritative per-patch
manifest; the categories below are the cumulative delta.

- **CachyOS hardware subset**: BBR3 default, `-O3` + Zen 4 ISA, sched-ext
  preemption, config hooks, and an ACPI bus-master-check disable for AMD.
- **AMD display and power** (drm-next, linux-pm, agd5f, ML): SMU14 fixes, the
  `PROFILE_PEAK` GFXCLK-float and deep-sleep disable (`0003`/`0004`), DCN401/
  DCN42B display fixes, HDMI FreeSync/VRR/ALLM (`0050`–`0061`), AMD VSDB
  FreeSync, colorops, and HDMI FRL (`1137`–`1144`).
- **amd-pstate / ACPI CPPC**: per-core EPP boost and the CPPC validation series
  that hardens `amd-pstate` on Zen 4 (`1200`–`1299`).
- **GPU core** (`1000`–`1099`): GMC TLB-invalidation buffer plumbing, GFX12
  named-barrier and retry-fault fixes, MES fence completion on reset, BAR0
  SR-IOV fallback restriction, userq deadlock fixes.
- **agd5f staging backports** (`9000`–`9099`): IH retry-CAM handling, VM
  PTE/userq correctness, gfx12 fixes.
- **Memory and block**: the zstd 1.6.0 merge, LRU-MARIE (`2101`), `mm/gup`
  folio batching (`2120`–`2127`), and bfq/mq-deadline contention fixes.
- **CPU idle**: the NAP governor (`2200`).

## Requirements

- Arch Linux with `makepkg` and `base-devel`
- `pahole` >= 1.31 (package `dwarves`)
- Network access to download the kernel source and the LLVM toolchain

You do **not** need Clang, LLD, or LLVM packages; the PKGBUILD downloads a
pre-built LLVM toolchain from `mirrors.edge.kernel.org/pub/tools/llvm/`.

## Build

From the repository root, remove stale build artifacts (old patched files cause
false conflicts), refresh checksums after any `source=()` change, and build:

```bash
rm -rf src pkg
updpkgsums
makepkg -f -s -c
```

The build produces `linux-sleepy-next-<pkgver>-<pkgrel>-x86_64.pkg.tar.zst`
and `linux-sleepy-next-headers-...pkg.tar.zst`. During the build you are
prompted whether to enable CAKE SQM shaping (via `net-tune`); the prompt is
skipped in non-interactive environments.

See `GUIDE.md` for toolchain details, PROFILE_PEAK behavior, and the net-tune
service.

## Install

```bash
sudo pacman -U linux-sleepy-next-20260902-13-x86_64.pkg.tar.zst \
              linux-sleepy-next-headers-20260902-13-x86_64.pkg.tar.zst
sudo grub-mkconfig -o /boot/grub/grub.cfg   # or refresh your bootloader
```

## Kernel command line

The kernel bakes these into `CONFIG_CMDLINE`:

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0 amdgpu.dcdebugmask=0x800
```

- `cpuidle.governor=nap` selects the NAP governor.
- `amd_pstate.epp_boost=1` enables per-core EPP boost.
- `pcie_aspm=off` + `amdgpu.aspm=0` + `amdgpu.runpm=0` are the drm/amd !5538
  SMU bus-drop stopgaps (ASPM and BACO/runtime-PM power transitions disabled;
  DPM stays on).
- `amdgpu.dcdebugmask=0x800` disables DCN4 Idle Power States, fixing the
  scanout-time "box" artifact over app windows on the RX 9070 XT (IPS
  pipe-gating made the flip-pending read return false).

## sched-ext scheduler (optional)

Enable sched-ext schedulers with `scx_loader` (`SCX_SCHED=scx_cake` in
`/etc/default/scx`) or start one directly, for example:

```bash
sudo scx_cake
```

## net-tune (SQM + latency tuning)

`net-tune/` ships one service that applies low-latency ethernet settings and
CAKE bufferbloat shaping at boot. Toggle `ENABLE_LATENCY` and `ENABLE_SQM`
independently in `/etc/net-tune.conf` (CAKE shaping is enabled by default at
80/80 Mbit):

```bash
sudo systemctl enable --now net-tune.service
```

BBR3 is the compiled-in default TCP controller; the service only shapes CAKE,
it does not change the congestion controller.

## Disabled subsystems

The build strips subsystems a single AMD desktop does not use: Intel/NVIDIA
DRM, IIO, InfiniBand, ISDN, CAN, and more (see `disable_configs.py` and the
`scripts/config` calls in `PKGBUILD`).

## Patch series

The series carries 112 patches. `PATCH_SOURCES.md` is the authoritative
per-patch manifest (authors, hashes, Message-IDs); `PATCH_SOURCES-7.2.md`
archives the retired 7.2 ledger.

| Range | Category | Source |
|---|---|---|
| `0001–0049` | Handmade local patches (SMU14, DCN401, GFX12) | Sleepy/Antigravity |
| `0050–0099` | Upstream EDID/display ML patches not yet landed | amd-gfx / dri-devel ML |
| `0101–0113` | CachyOS branch squashes (0106 = off-target drops) | sirlucjan / CachyOS fork |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | drm-next / agd5f |
| `1100–1199` | AMD Display (DCN4, DCN42B, FRL, colorops) | drm-next |
| `1200–1299` | AMD Power Management (amd-pstate, ACPI CPPC) | linux-pm / sirlucjan |
| `2000–2099` | Block / I/O schedulers (bfq, mq-deadline) | sirlucjan |
| `2100–2199` | Memory management (zstd, LRU-MARIE, gup batching) | sirlucjan / lkml |
| `2200–2299` | CPU idle (NAP governor) | sirlucjan |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux |

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch Linux build script |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `patches/<range>/NNNN-*.patch` | Patch series, one folder per number range |
| `net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `repos/` | Cloned upstream git repos for patch extraction |
| `GUIDE.md` | Build/install guide and PROFILE_PEAK notes |
| `CHANGELOG.md` | Per-release summary of what changed |
| `PATCH_SOURCES.md` | Per-patch provenance ledger |
| `CLAUDE.md` | Maintenance rules and workflow for LLM agents |

## Known issues

- **BTF symbol collision.** Old BBR and BBR3 define the same BTF kfunc symbol;
  the build disables `CONFIG_TCP_CONG_BBR` after `olddefconfig`.
- **DWARF5 required.** Clang 23 with `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`
  produces DWARF that pahole 1.31 cannot convert to BTF; the build uses
  `DEBUG_INFO_DWARF5`.
- **`pcie_aspm=off` is a stopgap.** It raises idle PCIe power draw slightly but
  prevents the !5538 SMU bus-drop black screens.
- **Local patches are not upstream.** The `PROFILE_PEAK` patches (`0003`/`0004`)
  modify AMD power management in ways not yet reviewed upstream.

## Contributing

This is a single-user kernel for fixed hardware. Before changing the patch
series, read `CLAUDE.md` for the patch numbering rules, CachyOS branch refresh,
and build-failure triage. Never hand-write a patch diff; every patch must trace
to a real commit or mailing-list submission.
