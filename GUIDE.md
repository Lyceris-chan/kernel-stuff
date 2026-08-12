# linux-sleepy

A custom Arch Linux kernel package (`linux-sleepy`) based on Linux 7.2-rc7, targeting AMD Zen 4 CPUs and RDNA 4 (Navi 48 / gfx1201) GPUs.

## Target audience

This kernel is written for one specific hardware configuration:

- **CPU**: AMD Ryzen 7 7700 (Zen 4)
- **GPU**: AMD Radeon RX 9070 XT (Navi 48, RDNA 4, gfx1201)
- **NIC**: Realtek RTL8125B 2.5 GbE
- **Storage**: Phison E16 NVMe (PCIe 4.0)

It is not a general-purpose distribution kernel. Configuration choices are intentionally opinionated for this hardware and may break other setups.

---

## Differences from vanilla linux-7.2-rc7

### Build toolchain

| Setting | Vanilla | This kernel |
|---------|---------|-------------|
| Compiler | GCC | Clang 23.1.0-rc2 (kernel.org pre-built) |
| Linker | ld (GNU) | `ld.lld` |
| LTO | None | ThinLTO (`CONFIG_LTO_CLANG_THIN=y`) |
| Optimization | `-O2` | `-O3` (`CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE_O3=y`) |
| CPU tuning | Generic x86-64 | `-march=znver4` (`CONFIG_MZEN4=y`) |

The LLVM toolchain is downloaded automatically from [mirrors.edge.kernel.org/pub/tools/llvm/](https://mirrors.edge.kernel.org/pub/tools/llvm/files/), maintained by Nathan Chancellor. On Wednesdays and Thursdays it checks for a newer weekly release candidate build before falling back to `llvm-23.1.0-rc2-x86_64.tar.xz`.

### Scheduler and core patches

The following patches come from the [CachyOS linux-cachyos](https://github.com/CachyOS/linux-cachyos) patchset, squashed to one patch per branch (`0101`–`0109`), rebased onto 7.2-rc7:

<details>
<summary>CachyOS patch subsystems included</summary>

| Branch (squash) | Description |
|-----------------|-------------|
| `bbr3` (`0101`) | Google BBR3 TCP congestion control |
| `kbuild` (`0102`) | CachyOS Kconfig hooks / `-O3` build |
| `cpu-isa` (`0103`) | x86_64 Zen 4 ISA optimizations (`-march=znver4`) |
| `cgroup-vram` (`0104`) | VRAM accounting in memory cgroups |
| `fixes` (`0105` + `0106`) | Hardware-relevant kernel fixes; off-target parts reverted by `0106-cachy-drops` |
| `hdmi` (`0107`) | HDMI 2.1 FreeSync/VRR/PCON fixes (excl. `0151`) |
| `preempt-ipi` (`0108`) | IPI-based preemption |
| `vesa-dsc-bpp` (`0109`) | DSC bits-per-pixel fixes |

</details>

### Additional out-of-tree patches

Per-patch provenance — authors, commit hashes, Message-IDs, and every dropped
or deferred entry — lives in `PATCH_SOURCES.md` and is not duplicated here. The
series is grouped by range:

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

### Realtek RTL8125B NIC

The RTL8125B 2.5 GbE NIC is driven by the in-kernel `r8169` driver (shipped as a module since 7.2). No out-of-tree Realtek driver is needed.

### Kconfig changes from defconfig

The following options differ from the CachyOS base `.config` (which itself differs from vanilla defconfig). See `config` in this repository for the full file.

| Symbol | Vanilla/CachyOS | This kernel | Reason |
|--------|----------------|-------------|--------|
| `MZEN4` | `n` | `y` | Hardware: Zen 4 |
| `LTO_CLANG_THIN` | `n` | `y` | ThinLTO via LLVM 23 |
| `CC_OPTIMIZE_FOR_PERFORMANCE_O3` | `n` | `y` | `-O3` optimization |
| `TCP_CONG_BBR` | `y` | `n` | Removed; conflicts with BBR3 BTF symbols |
| `TCP_CONG_BBR3` | `n` | `y` (built-in) | BBR3 is the default TCP congestion control |
| `DEFAULT_TCP_CONG` | `"cubic"` | `"bbr3"` | BBR3 default |
| `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT` | `y` | `n` | Disabled to fix pahole 1.31 + Clang 23 BTF generation |
| `DEBUG_INFO_DWARF5` | `n` | `y` | Required for pahole BTF with Clang 23 |
| `DEBUG_INFO_BTF` | `n` | `y` | BPF type information for bpftune |
| `LRU_GEN` | depends | `y` | Multi-generational LRU |
| `LRU_MARIE` | `n` | `y` | MARIE LRU variant |
| `CPU_IDLE_GOV_NAP` | `n` | `y` | NAP cpuidle governor |
| `V4L2_LOOPBACK` | `n` | `m` | Virtual camera device |
| `DRM_I915`, `DRM_XE`, `DRM_NOUVEAU` | varies | `n` | Not present on target hardware |
| `CMDLINE` | `""` | see below | Embedded boot parameters |

**Embedded kernel command line** (`CONFIG_CMDLINE`):

```
cpuidle.governor=nap amd_pstate.epp_boost=1 elevator=kyber pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0
```

- `cpuidle.governor=nap` — activates the NAP cpuidle governor by default; without this the module loads but does not activate.
- `amd_pstate.epp_boost=1` — enables per-core EPP boost for recently-busy CPUs on Zen 4. Requires the `epp_boost` patch series (`1202`).
- `elevator=kyber` — selects the kyber I/O scheduler as default.
- `pcie_aspm=off` — disables PCIe Active State Power Management entirely. This is the drm/amd !5538 SMU bus-drop stopgap (see the ASPM note in README "What this kernel adds").
- `amdgpu.aspm=0` / `amdgpu.runpm=0` — disable the GPU's own ASPM and runtime-PM (BACO) transitions (added 2026-08-12, `7.2.0-rc7-4`). Conservative stopgaps for the silent gaming freeze (SMU IF mismatch 0x2e vs 0x33); DPM stays on.

---

## PROFILE_PEAK Behavior & Deep Sleep Control (patches 0003 & 0004)

**These patches are custom (`0003` and `0004`).** They modify `drivers/gpu/drm/amd/pm/swsmu/smu14/smu_v14_0.c`.

### What the patches do

- **`0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch`**:
  Refactors `smu_v14_0_set_soft_freq_limited_range()` into `smu_v14_0_set_soft_freq_limited_range_split()` to support independent `min_automatic` and `max_automatic` flags. Sets `sclk_max_auto = true` for GFXCLK during `PROFILE_PEAK` so GPU core clocks float freely to full hardware boost speeds (>3.0 GHz) while keeping `sclk_min` pinned to peak DPM levels.

- **`0004-drm-amd-pm-Disable-deep-sleep-in-PROFILE_PEAK.patch`**:
  Disables deep sleep (`smu_v14_0_deep_sleep_control(smu, false)`) when entering `PROFILE_PEAK` to eliminate power state wake-up latencies and micro-stutter. Evaluates deep sleep control uniformly across all performance levels, re-enabling deep sleep on transitions away from `PROFILE_PEAK` to `AUTO`, `HIGH`, `LOW`, `MANUAL`, or `PROFILE_STANDARD` (unless compute profile mode is active).

### Effect

Setting `profile_peak` on RDNA 4 provides full hardware boost clocks (eliminating the stuck 2.0 GHz cap) while explicitly disabling deep sleep for minimum frame latency. Switching back to `auto`, `high`, `low`, or `manual` correctly restores deep sleep power management.

---

## Build

### Requirements

- Arch Linux with `makepkg`
- `pahole` >= 1.31 (`dwarves` package)
- `base-devel`
- Network access (downloads kernel source, LLVM toolchain)

No Clang or LLD packages are required. The PKGBUILD downloads a pre-built LLVM toolchain from kernel.org.

### Build and install

```bash
rm -rf src pkg           # old patched files cause false conflicts
makepkg -f -s -c
sudo pacman -U linux-sleepy-*.pkg.tar.zst linux-sleepy-headers-*.pkg.tar.zst
sudo grub-mkconfig -o /boot/grub/grub.cfg  # or equivalent
```

The build prompts interactively for your upload/download speeds and defaults to
enabling CAKE SQM. In non-interactive environments (CI, pipes) the prompt is
skipped and the shipped config is installed — CAKE shaping enabled at 80/80 Mbit
by default.

### SQM / bufferbloat mitigation

The `net-tune` service ships one unit (`/usr/lib/systemd/system/net-tune.service`)
that applies low-latency ethernet tuning (`ENABLE_LATENCY`) and CAKE SQM shaping
(`ENABLE_SQM`), each independently toggleable in `/etc/net-tune.conf`. The shipped
config enables SQM by default (80/80 Mbit); answering the build prompt lets you
enter your own upload/download speeds, and answering `n` (or editing
`/etc/net-tune.conf` to `ENABLE_SQM=no`) disables shaping while keeping latency
tuning.

BBR3 does **not** need to be set by this service; it is the kernel-compiled default.

To adjust speeds without rebuilding, edit `/etc/net-tune.conf` and restart the
service (`sudo systemctl restart net-tune.service`).

To confirm CAKE is actually shaping (both directions), check
`journalctl -u net-tune -n 20` for the `net-tune: OK - CAKE shaping active` line
after a restart, or inspect by hand:

```bash
tc qdisc show dev <iface>          # expect a root cake AND "qdisc ingress ffff:"
ip link show ifb4cake              # expect state UP, qdisc cake
tc filter show dev <iface> ingress # expect a mirred redirect to ifb4cake
```

If the ingress (download) half is missing — no `ingress ffff:` qdisc and no
`ifb4cake` device — downloads run unshaped and you'll see bufferbloat on the
download leg of a test while upload stays clean. Download shaping requires the
`ingress` qdisc to be built into the kernel (`CONFIG_NET_SCH_INGRESS=y`, enabled
in the PKGBUILD) — on a kernel without it, no amount of service configuration
can create the ingress path, and the service will log
`net-tune: ERROR - no ingress qdisc on <iface> ...`.

---

## Known issues and limitations

- **BTF symbol conflict**: `CONFIG_TCP_CONG_BBR` (old BBRv1/v2) and `CONFIG_TCP_CONG_BBR3` both define `BTF_KFUNCS_START(tcp_bbr_check_kfunc_ids)`. Having both built-in causes `resolve_btfids` to exit 255 silently, which presents as `Failed to generate BTF for vmlinux`. This build disables the old BBR.
- **DWARF5 required with Clang 23**: `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT` produces DWARF output that `pahole` 1.31 cannot convert to BTF. This build uses `DEBUG_INFO_DWARF5` explicitly.
- **LRU MARIE conflict with vm_swappiness**: The MARIE patch (`2101`) was sourced from the CachyOS-rebased version rather than the raw sirlucjan tree to avoid a `CONFIG_CACHY` vm_swappiness conflict.
- **NAP governor**: NAP requires the `cpuidle.governor=nap` kernel parameter to activate. This build bakes it into `CONFIG_CMDLINE` so it is not needed on the boot command line.
- **Patch `1101` is reverse-applied**: the DCN4 pstate-enable patch is applied then immediately reverse-applied in `prepare()` so `.pstate_enabled = false` avoids UCLK-switching display freezes on the RX 9070 XT. Restoring the vanilla setting keeps the GPU cool and power-efficient in `auto` mode without screen glitches.
- **Patch 0003 is not upstream**: The PROFILE_PEAK patch modifies SMU14 power management in ways that have not been reviewed by AMD or the upstream community.

---

## Repository layout

```
PKGBUILD                  Build script (Arch Linux makepkg format)
config                    Base kernel .config (from CachyOS)
disable_configs.py        Script to strip CachyOS-specific symbols before olddefconfig
patches/<range>/NNNN-*.patch   The patch series, one folder per number range
net-tune/                 Unified CAKE SQM + latency tuning systemd service
PATCH_SOURCES.md          Per-patch source URLs and commit hashes
GUIDE.md                  Developer notes (build, patch workflow, CI)
```

The PKGBUILD auto-creates gitignored root-level symlinks
(`NNNN-*.patch -> patches/<range>/NNNN-*.patch`) so makepkg can resolve the
folder-stored patches by basename (a makepkg 7.1.0 limitation). You do not need
to create them by hand; they are regenerated on every build.
