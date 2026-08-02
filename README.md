# linux-sleepy

`linux-sleepy` is a custom Arch Linux kernel package built for one machine: an
AMD Zen 4 desktop with an RDNA 4 graphics card. It is based on Linux mainline
`7.2-rc5` and layers a sanitized [CachyOS](https://github.com/CachyOS/linux-cachyos)
patchset plus targeted local and upstream patches on top.

**Base version:** `7.2.0-rc5-1-sleepy`
**Artifact:** `linux-sleepy-7.2.rc5-1-x86_64.pkg.tar.zst`

This is not a general-purpose kernel; the configuration is opinionated for the
hardware below.

## Target audience

This kernel is built for a single AMD desktop: a Ryzen 9 7950X (Zen 4) CPU, a
Radeon RX 9070 XT (Navi 48 / RDNA 4) GPU, and a Realtek RTL8125B NIC. It is not
a general-purpose distro kernel. It targets enthusiasts who want the latest AMD
display and power fixes on top of a CachyOS base, value low-latency networking
(BBRv3 + CAKE SQM), and want maximum per-core throughput. Running it on other
hardware is unsupported.

## Target hardware

| Component | Hardware | Kernel support |
|---|---|---|
| CPU | AMD Ryzen 9 7950X (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14` |
| NIC | Realtek RTL8125B 2.5 GbE | Out-of-tree `r8125` driver |
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

**Over vanilla Linux 7.2-rc5:**

- The hardware-relevant subset of CachyOS: BBRv3 TCP, `-O3` + Zen 4 ISA, VRAM
  cgroups, sched-ext preemption, HDMI 2.1 FreeSync/VRR, and EDID DSC BPP.
- ~50 AMD-specific backports from `drm-next`, `linux-pm`, and `amd-gfx`: SMU14
  power fixes, DCN401/DCN42B display fixes, `amd-pstate` EPP boost, ACPI CPPC
  fixes, and GFX12 stability work.
- agd5f staging backports: the Exit-idle-optimizations v2 series and
  `BUG()` → `WARN()` conversions for GFX12/PSP14.
- Local handmade SMU14/DCN401 patches, including the `PROFILE_PEAK` GFXCLK
  ceiling float.
- BFQ/mq-deadline contention fixes, LRU-MARIE page eviction, the zstd 7.2
  merge, and the NAP cpuidle governor.

**Over stock CachyOS:**

- Only hardware-relevant branches are kept; off-target patches (i915, btusb,
  rtw89, laptop audio, and more) are reverted by the `0106` drop patch.
- The kernel is trimmed for a single machine: `DRM_I915`, `DRM_NOUVEAU`,
  `DRM_XE`, `IIO`, `ISDN`, `CAN`, and AppArmor are disabled.
- A custom `PROFILE_PEAK` power-profile enhancement and an optional CAKE SQM
  service are included.

## Requirements

- Arch Linux with `makepkg` and `base-devel`
- `pahole` >= 1.31 (package `dwarves`)
- Network access to download the kernel source, the LLVM toolchain, and the
  `r8125` driver

You do **not** need Clang, LLD, or LLVM packages; the PKGBUILD downloads a
pre-built LLVM toolchain from `mirrors.edge.kernel.org/pub/tools/llvm/`.

## Build

In the repository root, remove stale build artifacts (old patched files cause
false conflicts), refresh checksums after any `source=()` change, and build:

```bash
rm -rf src pkg
updpkgsums
makepkg -f -s -c
```

The build produces these packages:

- `linux-sleepy-7.2.rc5-1-x86_64.pkg.tar.zst`
- `linux-sleepy-headers-7.2.rc5-1-x86_64.pkg.tar.zst`
- `linux-sleepy-r8125-7.2.rc5-1-x86_64.pkg.tar.zst` (Realtek NIC driver)

During the build you are prompted whether to configure the CAKE SQM service;
in non-interactive environments (CI, piped input) the prompt is skipped.

## Install

Install the kernel, headers, and NIC driver:

```bash
sudo pacman -U linux-sleepy-7.2.rc5-1-x86_64.pkg.tar.zst \
              linux-sleepy-headers-7.2.rc5-1-x86_64.pkg.tar.zst \
              linux-sleepy-r8125-7.2.rc5-1-x86_64.pkg.tar.zst
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
cpuidle.governor=nap amd_pstate.epp_boost=1
```

- `cpuidle.governor=nap` activates the NAP cpuidle governor.
- `amd_pstate.epp_boost=1` enables per-core EPP boost for recently busy cores.

### sched-ext scheduler (optional)

For a gaming-focused scheduler, run `scx_cake` with the esports preset:

```bash
sudo scx_cake --preset esports
```

Or configure `scx_loader` in `/etc/default/scx` with `SCX_SCHED=scx_cake` and
`SCX_FLAGS="--preset esports"`.

### SQM QoS (optional)

The `sqm-qos/` directory ships a CAKE bufferbloat-mitigation service:

```bash
sudo systemctl enable --now sqm-qos.service
```

Adjust your line rate by editing `/etc/sqm-qos.conf` and restarting the service.
BBR3 is the kernel-compiled default TCP controller; the service only applies CAKE.

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

The patch series is organized into numbered ranges (see `PATCH_SOURCES.md` for
per-patch provenance). The full series is 88 patches.

| Range | Category | Source |
|---|---|---|
| `0001–0034` | Local SMU14 / DCN401 fixes | Handmade (Sleepy/Antigravity) and upstream ML |
| `0050–0058` | EDID / HDMI upstream patches | `b4` mbox, freedesktop archives |
| `0101–0109` | CachyOS per-branch patchset | sirlucjan `kernel-patches` repo |
| `1000–1019` | GPU core (GFX12, GMC, SDMA, TLB) | `drm-next` |
| `1100–1111` | Display (DCN4, DCN42B, PSR, MCIF) | `drm-next` |
| `1200–1213` | amd-pstate / ACPI CPPC / cpufreq | `linux-pm`, mainline post-rc5 |
| `2000–2004` | Block I/O (bfq, mq-deadline) | sirlucjan `block-patches-sep` |
| `2100–2101` | Memory (zstd, LRU-MARIE) | sirlucjan |
| `2200` | CPU idle (NAP governor) | sirlucjan `nap-patches` |
| `9000–9007` | agd5f staging backports | `agd5f/linux` |

Each CachyOS branch is a single patch:

- `0101` cachy-bbr3 — BBRv3 TCP congestion control
- `0102` cachy-kbuild — allows `-O3`
- `0103` cachy-cpu-isa — Zen 4 ISA (`-march=znver4`)
- `0104` cachy-cgroup-vram — VRAM cgroups
- `0105` cachy-fixes — hardware-relevant subset
- `0106` cachy-drops — reverts the off-target hardware included in the full
  fixes branch: i915, btusb, rtw89, touchpad, laptop audio, SOF, iwlwifi,
  nouveau
- `0107` cachy-hdmi — HDMI 2.1 FreeSync/VRR/PCON
- `0108` cachy-preempt-ipi — SMP preemption + TLB
- `0109` cachy-vesa-dsc — EDID DSC BPP

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch Linux build script |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `NNNN-*.patch` | Patch series (see ranges above) |
| `sqm-qos/` | Optional CAKE SQM systemd service |
| `r8125/` | RTL8125B out-of-tree driver source |
| `repos/` | Cloned upstream git repos for patch extraction |
| `GUIDE.md` | End-user guide with build details and PROFILE_PEAK notes |
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
