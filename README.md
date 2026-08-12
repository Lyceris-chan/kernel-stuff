# linux-sleepy

`linux-sleepy` is a custom Arch Linux kernel package built for one machine: an
AMD Zen 4 desktop with an RDNA 4 graphics card. It is based on Linux mainline
`7.2-rc7` and layers a sanitized [CachyOS](https://github.com/CachyOS/linux-cachyos)
patchset plus targeted local and upstream patches on top.

**Base version:** `7.2.0-rc7-1-sleepy`
**Artifact:** `linux-sleepy-7.2.rc7-1-x86_64.pkg.tar.zst`

This is not a general-purpose kernel; the configuration is opinionated for the
hardware below.

## Target audience

This kernel is built for a single AMD desktop: a Ryzen 7 7700 (Zen 4) CPU, a
Radeon RX 9070 XT (Navi 48 / RDNA 4) GPU, and a Realtek RTL8125B NIC. It is not
a general-purpose distro kernel. It targets enthusiasts who want the latest AMD
display and power fixes on top of a CachyOS base, value low-latency networking
(BBRv3 + CAKE SQM), and want maximum per-core throughput. Running it on other
hardware is unsupported.

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
  pre-built LLVM toolchain from kernel.org (`CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`).
- **RDNA 4 display and power work.** Backports fix PSR/Replay on DCN4, add
  SDMA-assisted TLB invalidation, and convert driver panics (`BUG()`) to
  non-fatal warnings (`WARN()`).
- **`PROFILE_PEAK` GFXCLK float.** Local patches let the GPU clock ceiling float
  above 3.0 GHz and disable deep sleep while in `PROFILE_PEAK`. See
  [PROFILE_PEAK](#profile_peak-behavior).
- **`amd-pstate` EPP boost.** Per-core EPP boosting (`amd_pstate.epp_boost=1`)
  keeps active cores at `performance` EPP without raising idle power.
- **BBR3 TCP congestion control** is the compiled-in system default, with an
  optional CAKE SQM service for bufferbloat mitigation.
- **Scheduler and VM additions:** sched-ext BPF schedulers (`scx_cake`), the NAP
  cpuidle governor, and LRU-MARIE page eviction. Intel/NVIDIA DRM drivers and
  unused subsystems (IIO, InfiniBand, ISDN, CAN) are stripped out.

## What this kernel adds

Here's what `linux-sleepy` gives you on top of each baseline.

**Over vanilla Linux 7.2-rc7:**

- The hardware-relevant subset of CachyOS: BBRv3 TCP, `-O3` + Zen 4 ISA, VRAM
  cgroups, sched-ext preemption, HDMI 2.1 FreeSync/VRR, and EDID DSC BPP.
- ~90 AMD-specific backports from `drm-next`, `linux-pm`, `amd-gfx`, and the
  amd-gfx/dri-devel lists: SMU14 power fixes (incl. the smu_v14_0_0 DPM
  clock-query set), DCN401/DCN42B display fixes (incl. PSR/Replay Part 2,
  IPS/zstate, HDMI clock + DML fixes, HDR/SDR seamless switch, MST HDCP
  bounds-check), `amd-pstate` EPP boost, and GFX12 stability work.
- agd5f/staging backports: `BUG()` → `WARN()` conversions for GFX12/PSP14/MES/IMU
  (`9001`–`9003`, `9009`–`9010`), the TTM copy-packet-size optimization (`9006`),
  `DB_RING_CONTROL` / `TRUNCATE_COORD_MODE` GFX12 fixes (`9007`–`9008`), the
  **retry-fault handling v3 series** (`9011`–`9024`, Timur Kristóf), and the
  **amd-drm-next-7.3-2026-08-06 backports** (`9030`–`9032`: smu_v14_0_0 DCLK metric,
  DCEFCLK, and `find_clk_level()` DPM fixes), the amdgpu CS/VM correctness
  series (`9033`–`9035`: FENCE-chunk leak, VM overrun, BO-VA kmap offset), the
  gfx12 userq sub-page VA-validation fix (`9036`), the RDNA4/gfx1201
  prefer-default-discovery-offset fix (`9037`), and the GFX12 userq/HMM
  correctness set (`9038`–`9040`: PRT-mapping reject, eviction-fence rearm
  bound, HMM range free on the CS error path).
  The Exit-idle-optimizations series merged upstream into rc6 and was dropped.
  The SMU14 PPT-limits framework rework from the same tag is **deferred to 7.3**
  (does not apply cleanly to the rc7 series state).
- Local handmade SMU14/DCN401 patches, including the `PROFILE_PEAK` GFXCLK
  ceiling float.
- BFQ/mq-deadline contention fixes, LRU-MARIE page eviction, the zstd 7.2
  merge, zram zstd + stability fixes (`2102`–`2108`), and the NAP cpuidle
  governor.

**Over stock CachyOS:**

- Only hardware-relevant branches are kept; off-target patches (i915, btusb,
  rtw89, laptop audio, and more) are reverted by the `0106` drop patch.
- The kernel is trimmed for a single machine: `DRM_I915`, `DRM_NOUVEAU`,
  `DRM_XE`, `IIO`, `ISDN`, `CAN`, and AppArmor are disabled.
- A custom `PROFILE_PEAK` power-profile enhancement and an optional CAKE SQM
  service are included.

**PCIe ASPM is disabled.** The kernel no longer forces a compile-time ASPM policy
(was `PCIEASPM_PERFORMANCE` — there is no Kconfig "off" option) and the built-in
cmdline passes **`pcie_aspm=off`**, which disables PCIe Active State Power
Management entirely at boot. This is the drm/amd work-item **!5538** stopgap: our
RX 9070 XT's SMU driver/firmware IF mismatch (driver `0x2e` vs fw `0x33`) can drop
the GPU off the PCIe bus during power transitions (black screen → hard reset), and
an AMD engineer recommended testing ASPM off. Trade-off: slightly higher idle PCIe
power draw. The primary mitigations remain the LACT
`power_dpm_force_performance_level=high` stopgap and (recommended) removing
`nowatchdog` from the bootloader cmdline so a repeat is diagnosable.

## Requirements

- Arch Linux with `makepkg` and `base-devel`
- `pahole` >= 1.31 (package `dwarves`)
- Network access to download the kernel source and the LLVM toolchain

You do **not** need Clang, LLD, or LLVM packages; the PKGBUILD downloads a
pre-built LLVM toolchain from `mirrors.edge.kernel.org/pub/tools/llvm/`.

## Build

In the repository root, remove stale build artifacts (old patched files cause
false conflicts), refresh checksums after any `source=()` change, and build.
Patches are stored in `patches/<range>/` folders; the PKGBUILD auto-creates the
gitignored root symlinks makepkg needs, so no setup is required:

```bash
rm -rf src pkg
updpkgsums
makepkg -f -s -c
```

The build produces these packages:

- `linux-sleepy-7.2.rc7-1-x86_64.pkg.tar.zst`
- `linux-sleepy-headers-7.2.rc7-1-x86_64.pkg.tar.zst`

During the build you are prompted whether to enable CAKE SQM shaping (via the
`net-tune` service); in non-interactive environments (CI, piped input) the
prompt is skipped.

### Compiler toolchain (custom LLVM)

`linux-sleepy` is compiled with **ClangBuiltLinux's pre-built LLVM toolchain
from kernel.org** — the same weekly RC builds the kernel community tests
against — not with your distro's compiler.

- **Download URL**: `https://mirrors.edge.kernel.org/pub/tools/llvm/files/`
- **Selection**: the PKGBUILD auto-picks the newest weekly RC build
  (`_auto_fetch_latest_llvm=yes`; Nathan Chancellor publishes new builds on
  Wednesdays/Thursdays). The current version and fallback are pinned in
  `_kernel_org_llvm_tarball`.
- **Current version**: `llvm-23.1.0-rc2-x86_64.tar.xz` (81 MB download,
  ~412 MB unpacked) — Clang 23.1.0-rc2 / LLD 23.1.0 from llvm-project commit
  `561093d94eb7156dea780c1c71a779824ef90e5b`.
- **Flags**: the toolchain's `bin/` is prepended to `$PATH` and the kernel
  builds with `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`, plus
  `PAHOLE=/usr/bin/pahole` (from the `dwarves` package) for BTF.
- **ThinLTO**: `CONFIG_LTO_CLANG_THIN=y` with `-O3` and `-march=znver4`
  (`_use_llvm_lto=thin`).
- **Headers**: `linux-sleepy-headers` declares a runtime dependency on
  `clang llvm lld` so DKMS / out-of-tree modules compiled against its build tree
  use the same toolchain.

## Install

Install the kernel and headers:

```bash
sudo pacman -U linux-sleepy-7.2.rc7-1-x86_64.pkg.tar.zst \
              linux-sleepy-headers-7.2.rc7-1-x86_64.pkg.tar.zst
```

Regenerate your bootloader config (for GRUB):

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

## Configuration

### Kernel command line

The kernel bakes the following parameters into `CONFIG_CMDLINE`, so you do not
need them on your boot command line:

```
cpuidle.governor=nap amd_pstate.epp_boost=1 elevator=kyber pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0
```

- `cpuidle.governor=nap` activates the NAP cpuidle governor.
- `amd_pstate.epp_boost=1` enables per-core EPP boost for recently busy cores.
- `elevator=kyber` selects the kyber I/O scheduler as default.
- `pcie_aspm=off` disables PCIe Active State Power Management entirely — the
  drm/amd !5538 SMU bus-drop stopgap (see the ASPM note under "What this kernel
  adds").
- `amdgpu.aspm=0` and `amdgpu.runpm=0` (added 2026-08-12) disable the GPU's own
  ASPM handling and runtime power-management (BACO) transitions — conservative
  amdgpu-side stopgaps for the silent gaming freeze (SMU IF mismatch 0x2e vs
  0x33). DPM stays enabled, so clocks still downclock at idle.

### sched-ext scheduler (optional)

For a gaming-focused scheduler, run `scx_cake` with the esports preset:

```bash
sudo scx_cake --preset esports
```

Or configure `scx_loader` in `/etc/default/scx` with `SCX_SCHED=scx_cake` and
`SCX_FLAGS="--preset esports"`.

### net-tune (SQM + latency tuning)

The `net-tune/` directory ships one service that applies low-latency ethernet
settings and CAKE bufferbloat shaping at boot. The two parts are independent —
toggle `ENABLE_LATENCY` and `ENABLE_SQM` in `/etc/net-tune.conf`. CAKE shaping
is enabled by default (80/80 Mbit) — set `ENABLE_SQM=no` to disable:

```bash
sudo systemctl enable --now net-tune.service
```

The latency part disables Wake-on-LAN, GRO/GSO/TSO/LRO, EEE, and adaptive
interrupt coalescing; sets static low-latency coalescing and 256-entry ring
buffers; and enables busy-polling sysctls. The SQM part applies CAKE at the
bandwidth in the config (set it a few percent under your real sync rate).
BBR3 is the kernel-compiled default TCP controller; the service only shapes
CAKE, it does not change the congestion controller.

### Webcam support (UVC)

The kernel builds the `uvcvideo` module (`CONFIG_USB_VIDEO_CLASS=m`) for USB
Video Class webcams. This also covers Android phones in native USB-webcam mode:
the phone presents itself as a UVC gadget and the host reads it with `uvcvideo`
(no extra kernel module involved). Load it with:

```bash
sudo modprobe uvcvideo
```

`v4l2loopback` is an **out-of-tree** module, not part of this kernel. The native
Android USB-webcam path does not use it. If you route a phone camera into a
desktop app via DroidCam or `scrcpy --v4l2-sink`, install `v4l2loopback-dkms` or
`droidcam` from the AUR instead.

### Disabled subsystems

The build strips subsystems a single AMD desktop does not use: Intel/NVIDIA DRM,
IIO, InfiniBand, ISDN, CAN, FireWire, PCMCIA, Gameport, Intel-only audio
(NHLT/DPTF/silent-stream), kernel debug hooks, and more (see
`disable_configs.py` and the `scripts/config` calls in `PKGBUILD`). One worth
knowing about:

- **F2FS** (`CONFIG_F2FS_FS`) is disabled. It is a flash/Android-oriented
  filesystem; this build's NVMe SSD uses ext4 (with `vfat`/`exfat` for
  removable media). To re-enable it, remove `-d F2FS_FS` from the
  `scripts/config` bloat line in `PKGBUILD`'s `prepare()` and rebuild.

## PROFILE_PEAK behavior

Two local patches (`0003`, `0004`) modify `smu_v14_0.c`:

- `0003` lets the GFXCLK ceiling float to the hardware boost ceiling (above
  3.0 GHz) while `PROFILE_PEAK` is forced, instead of pinning it to the DPM
  peak entry.
- `0004` disables deep sleep while `PROFILE_PEAK` is forced to remove
  power-state wake-up latency; switching back to `auto`, `high`, `low`, or
  `manual` restores it. Deep sleep also stays disabled while the COMPUTE
  workload profile is active.

Set the profile with:

```bash
echo profile_peak | sudo tee /sys/class/drm/card0/device/power_dpm_force_performance_level
```

## Patch series

The series carries 151 patches in the ranges below. `PATCH_SOURCES.md` is the
authoritative per-patch manifest — authors, commit hashes, Message-IDs, and every
dropped or deferred entry — so it is not duplicated here.

| Range | Category | Source |
|---|---|---|
| `0001–0049` | Handmade local patches (SMU14, DCN401, GFX12) | Sleepy/Antigravity |
| `0050–0099` | Upstream EDID/display ML patches not yet landed | amd-gfx / dri-devel ML |
| `0101–0113` | CachyOS branch squashes (0106 = off-target drops; 0110–0113 = fork backports) | sirlucjan / CachyOS fork |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | drm-next / agd5f |
| `1100–1199` | AMD Display (DCN4, DCN42B, PSR, Replay, pstate, MCIF ARB) | drm-next |
| `1200–1299` | AMD Power Management (amd-pstate, cpufreq) | linux-pm / sirlucjan |
| `2000–2099` | Block / I/O schedulers (bfq, mq-deadline) | sirlucjan |
| `2100–2199` | Memory management (zstd, LRU-MARIE) | sirlucjan |
| `2200–2299` | CPU idle (NAP governor) | sirlucjan |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux |

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch Linux build script |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `patches/<range>/NNNN-*.patch` | Patch series, one folder per number range (see ranges above). Root-level `NNNN-*.patch` symlinks are auto-created by the PKGBUILD for makepkg 7.1.0 basename resolution (gitignored). |
| `net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `repos/` | Cloned upstream git repos for patch extraction |
| `GUIDE.md` | End-user guide with build details and PROFILE_PEAK notes |
| `CHANGELOG.md` | Per-release summary of what changed |
| `PATCH_SOURCES.md` | Per-patch provenance ledger |
| `CLAUDE.md` | Maintenance rules and workflow for LLM agents |

## Known issues

- **BTF symbol collision.** Old BBR and BBR3 define the same BTF kfunc symbol;
  the build disables `CONFIG_TCP_CONG_BBR` after `olddefconfig`.
- **DWARF5 required.** Clang 23 with `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`
  produces DWARF that pahole 1.31 cannot convert to BTF; the build uses
  `DEBUG_INFO_DWARF5`.
- **Local patches are not upstream.** The `PROFILE_PEAK` patches (0003, 0004)
  modify AMD power management in ways not yet reviewed upstream.
- **`1101` is reverse-applied.** The DCN4 pstate-enable patch is reverse-applied
  in `prepare()` so `.pstate_enabled = false` avoids UCLK-switching display
  freezes on the RX 9070 XT.

## Contributing

This is a single-user kernel for fixed hardware. Before changing the patch
series, read `CLAUDE.md` for the patch numbering rules, CachyOS branch refresh,
and build-failure triage. Never hand-write a patch diff; every patch must trace
to a commit or mailing-list submission and be documented in `PATCH_SOURCES.md`.
