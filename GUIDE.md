# linux-sleepy-next — build guide

A custom Arch Linux kernel package (`linux-sleepy-next`) built from a
**linux-next** snapshot (`next-20260902`, the 7.3 merge-window content),
targeting AMD Zen 4 CPUs and RDNA 4 (Navi 48 / gfx1201) GPUs. It descends from
the 7.2 `linux-sleepy` package, which was retired on 2026-09-02.

## Target audience

This kernel is written for one specific hardware configuration:

- **CPU**: AMD Ryzen 7 7700 (Zen 4)
- **GPU**: AMD Radeon RX 9070 XT (Navi 48, RDNA 4, gfx1201)
- **NIC**: Realtek RTL8125B 2.5 GbE
- **Storage**: Phison E16 NVMe (PCIe 4.0)

It is not a general-purpose distribution kernel. Configuration choices are
intentionally opinionated for this hardware and may break other setups.

---

## Differences from the linux-next baseline

### Build toolchain

| Setting | Baseline | This kernel |
|---------|----------|-------------|
| Compiler | GCC | Clang 23 (kernel.org pre-built) |
| Linker | ld (GNU) | `ld.lld` |
| LTO | None | ThinLTO (`CONFIG_LTO_CLANG_THIN=y`) |
| Optimization | `-O2` | `-O3` (`CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE_O3=y`) |
| CPU tuning | Generic x86-64 | `-march=znver4` (`CONFIG_MZEN4=y`) |

The LLVM toolchain downloads automatically from
[mirrors.edge.kernel.org/pub/tools/llvm/](https://mirrors.edge.kernel.org/pub/tools/llvm/files/)
(Nathan Chancellor's weekly RC builds). On Wednesdays and Thursdays the
PKGBUILD checks for a newer release candidate before falling back to the pinned
`llvm-23.1.0-rc2-x86_64.tar.xz`.

### CachyOS patch subsystems

The kernel layers a sanitized CachyOS patchset, squashed to one patch per branch
(`0101`–`0113`), rebased onto the linux-next snapshot:

| Squash | Description |
|--------|-------------|
| `0101` | BBR3 TCP congestion control |
| `0102` | CachyOS kbuild (`-O3`) hooks |
| `0103` | x86_64 Zen 4 ISA optimizations (`-march=znver4`) |
| `0110` | CachyOS config hooks |
| `0111` | ACPI: disable bus-master check for AMD |
| `0112` | amdgpu: avoid evicting resources at S5 |

(There is no `0106`/`0107` in this series: the off-target-drop and hdmi
squashes were superseded by the linux-next base, which carries the clean
upstream HDMI path.)

### Additional out-of-tree patches

Per-patch provenance — authors, commit hashes, Message-IDs, and every dropped
or deferred entry — lives in `PATCH_SOURCES.md` and is not duplicated here. The
series is grouped by range:

| Range | Category | Source |
|---|---|---|
| `0001–0049` | Handmade local patches (SMU14, DCN401, GFX12) | Sleepy/Antigravity |
| `0050–0099` | Upstream EDID/display ML patches not yet landed | amd-gfx / dri-devel ML |
| `0101–0113` | CachyOS branch squashes | sirlucjan / CachyOS fork |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TLB) | drm-next / agd5f |
| `1100–1199` | AMD Display (DCN4, DCN42B, FRL, colorops) | drm-next |
| `1200–1299` | AMD Power Management (amd-pstate, ACPI CPPC) | linux-pm / sirlucjan |
| `2000–2099` | Block / I/O schedulers (bfq, mq-deadline) | sirlucjan |
| `2100–2199` | Memory management (zstd, LRU-MARIE, gup batching) | sirlucjan / lkml |
| `2200–2299` | CPU idle (NAP governor) | sirlucjan |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux |

### Realtek RTL8125B NIC

The RTL8125B 2.5 GbE NIC is driven by the in-kernel `r8169` driver (built as a
module). No out-of-tree Realtek driver is needed.

### Notable Kconfig changes

The full set of `scripts/config` calls lives in `prepare()` in `PKGBUILD` (and
`disable_configs.py`). Highlights:

| Symbol | This kernel | Reason |
|--------|-------------|--------|
| `MZEN4` | `y` | Hardware: Zen 4 |
| `LTO_CLANG_THIN` | `y` | ThinLTO via LLVM 23 |
| `CC_OPTIMIZE_FOR_PERFORMANCE_O3` | `y` | `-O3` |
| `TCP_CONG_BBR` | `n` | Removed; conflicts with BBR3 BTF symbols |
| `TCP_CONG_BBR3`, `DEFAULT_TCP_CONG` | `y` / `"bbr3"` | BBR3 is the default |
| `DEBUG_INFO_DWARF5`, `DEBUG_INFO_BTF` | `y` | pahole BTF with Clang 23 |
| `LRU_GEN`, `LRU_MARIE` | `y` | Multi-generational LRU + MARIE |
| `CPU_IDLE_GOV_NAP` | `y` | NAP cpuidle governor |
| `SCHED_CLASS_EXT` | `y` | sched-ext BPF schedulers |
| `NET_SCH_INGRESS`, `IFB` | `y` / `m` | CAKE SQM download shaping |
| `DRM_I915`, `DRM_XE`, `DRM_NOUVEAU` | `n` | Not present on target hardware |

**Embedded kernel command line** (`CONFIG_CMDLINE`):

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0 amdgpu.dcdebugmask=0x800
```

- `cpuidle.governor=nap` activates the NAP governor (without it the module
  loads but does not activate).
- `amd_pstate.epp_boost=1` enables per-core EPP boost (`1202`).
- `pcie_aspm=off` + `amdgpu.aspm=0` + `amdgpu.runpm=0` are the drm/amd !5538
  SMU bus-drop stopgaps; DPM stays on so clocks still downclock.
- `amdgpu.dcdebugmask=0x800` disables DCN4 Idle Power States, fixing the
  scanout-time "box" artifact on the RX 9070 XT.

---

## PROFILE_PEAK behavior and deep-sleep control (patches 0003 & 0004)

**These patches are custom.** They modify
`drivers/gpu/drm/amd/pm/swsmu/smu14/smu_v14_0.c`.

- **`0003` — Allow PROFILE_PEAK GFXCLK ceiling to float.** Lets the GPU clock
  ceiling float to the hardware boost limit (>3.0 GHz) while `PROFILE_PEAK` is
  forced, instead of pinning it to the DPM table's peak entry.
- **`0004` — Disable deep sleep in PROFILE_PEAK.** Disables deep sleep while
  `PROFILE_PEAK` is forced (and while the COMPUTE workload profile is active)
  to remove power-state wake-up latency; switching back to `auto`, `high`,
  `low`, or `manual` restores it.

Set the profile with:

```bash
echo profile_peak | sudo tee /sys/class/drm/card0/device/power_dpm_force_performance_level
```

---

## Build

### Requirements

- Arch Linux with `makepkg`
- `pahole` >= 1.31 (`dwarves` package)
- `base-devel`
- Network access (downloads the kernel source and the LLVM toolchain)

No Clang or LLD packages are required. The PKGBUILD downloads a pre-built LLVM
toolchain from kernel.org.

### Build and install

```bash
rm -rf src pkg           # old patched files cause false conflicts
makepkg -f -s -c
sudo pacman -U linux-sleepy-next-*.pkg.tar.zst linux-sleepy-next-headers-*.pkg.tar.zst
sudo grub-mkconfig -o /boot/grub/grub.cfg  # or equivalent
```

Run `updpkgsums` after any `source=()` change or patch-file edit. The build
prompts interactively for your CAKE SQM upload/download speeds and defaults to
enabling shaping; in non-interactive environments the prompt is skipped and the
shipped config installs (CAKE shaping enabled at 80/80 Mbit by default).

### net-tune (SQM / bufferbloat mitigation)

The `net-tune` service ships one unit
(`/usr/lib/systemd/system/net-tune.service`) that applies low-latency ethernet
tuning (`ENABLE_LATENCY`) and CAKE SQM shaping (`ENABLE_SQM`), each
independently toggleable in `/etc/net-tune.conf`. BBR3 is the kernel-compiled
default; the service only shapes CAKE, it does not change the congestion
controller.

To adjust speeds without rebuilding, edit `/etc/net-tune.conf` and restart:
`sudo systemctl restart net-tune.service`.

Confirm CAKE is shaping both directions by checking
`journalctl -u net-tune -n 20` for `net-tune: OK - CAKE shaping active`, or by
hand:

```bash
tc qdisc show dev <iface>          # expect a root cake AND "qdisc ingress ffff:"
ip link show ifb4cake              # expect state UP, qdisc cake
tc filter show dev <iface> ingress # expect a mirred redirect to ifb4cake
```

Download shaping requires the `ingress` qdisc built in
(`CONFIG_NET_SCH_INGRESS=y`) and a named `ifb4cake` device. If the ingress half
is missing the service logs
`net-tune: ERROR - no ingress qdisc on <iface> ...` and downloads run unshaped.

---

## Known issues and limitations

- **BTF symbol conflict**: old BBR (`TCP_CONG_BBR`) and BBR3 both define
  `BTF_KFUNCS_START(tcp_bbr_check_kfunc_ids)`; having both built-in makes
  `resolve_btfids` exit 255. This build disables the old BBR.
- **DWARF5 required with Clang 23**: `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`
  produces DWARF that pahole 1.31 cannot convert to BTF. This build uses
  `DEBUG_INFO_DWARF5`.
- **NAP governor**: NAP requires `cpuidle.governor=nap`, baked into
  `CONFIG_CMDLINE`.
- **`0003`/`0004` are not upstream**: they modify SMU14 power management in ways
  not yet reviewed by AMD.
- **`pcie_aspm=off` is a stopgap** for the !5538 SMU bus-drop; it slightly
  raises idle PCIe power draw.

---

## Repository layout

```
PKGBUILD                  Build script (Arch Linux makepkg format)
config                    Base kernel .config (from CachyOS)
disable_configs.py        Script to strip unwanted symbols before olddefconfig
patches/<range>/NNNN-*.patch   The patch series, one folder per number range
net-tune/                 Unified CAKE SQM + latency tuning systemd service
PATCH_SOURCES.md          Per-patch source URLs and commit hashes
PATCH_SOURCES-7.2.md      Archived ledger of the retired 7.2 series
README.md                 User-facing overview
GUIDE.md                  This guide
CHANGELOG.md              Per-release summary of what changed
```

The PKGBUILD auto-creates gitignored root-level symlinks
(`NNNN-*.patch -> patches/<range>/NNNN-*.patch`) so makepkg can resolve the
folder-stored patches by basename (a makepkg 7.1.0 limitation). You do not need
to create them by hand; they are regenerated on every build.
