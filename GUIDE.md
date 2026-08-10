# linux-sleepy

A custom Arch Linux kernel package (`linux-sleepy`) based on Linux 7.2-rc7, targeting AMD Zen 4 CPUs and RDNA 4 (Navi 48 / gfx1201) GPUs.

## Target audience

This kernel is written for one specific hardware configuration:

- **CPU**: AMD Ryzen Threadripper Pro 7950X (Zen 4)
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

These patches are applied on top of the CachyOS base, numbered `1xxx` (upstream mailing list / development trees) and `0xxx` (local patches).

<details>
<summary>SMU14 / power management (0001–0003, 0012)</summary>

| File | Source | Description |
|------|--------|-------------|
| `0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch` | Upstream | Fix typo in `smu_v14_0_set_irq_state` |
| `0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch` | Upstream | Fix memory leaks in `smu_v14_0_fini_smc_tables` |
| `0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch` | **Local** | PROFILE_PEAK GFXCLK float (see below) |
| `0012-drm-amd-pm-Fix-SMU14-power-limit-reporting-logic.patch` | Upstream | Fix SMU14 power limit reporting |

</details>

<details>
<summary>DCN401 / display (0004–0011)</summary>

| File | Source | Description |
|------|--------|-------------|
| `0004–0006` | Upstream | SMU14 SR-IOV, I2C bounds checking, mutex fixes |
| `0007` | Upstream | DCN401: proactively shrink DET for pipes losing planes |
| `0008–0011` | Upstream | DCN401 resource: memory leak, OOB, HPO, IRQ fixes |

</details>

<details>
<summary>amd-pstate / Zen 4 (0016–0019, 1070–1076)</summary>

| File | Source | Description |
|------|--------|-------------|
| `0016` | Upstream | Document missing kernel-doc members |
| `0017` | Upstream | Update `cppc_req_cached` before writing EPP |
| `0018` | Upstream | Per-core EPP boost for `recalibrate` mode |
| `0019` | Upstream | Document `epp_boost` parameter |
| `1070` | linux-pm | Bail early if `!X86_FEATURE_HW_PSTATE` |
| `1071` | linux-pm | Skip unit tests when driver is not active |
| `1072` | linux-pm | Fix EPP return type and init errors |
| `1073` | linux-pm | Toggle `auto_sel` in active mode on shared memory systems |
| `1074` | linux-pm | Cache firmware-programmed EPP value |
| `1075` | linux-pm | Handle missing policy in dynamic EPP callbacks |
| `1076` | linux-pm | Loosen requirement on lowest nonlinear frequency |

</details>

<details>
<summary>RDNA 4 / amdgpu (1002–1003, 1025–1065)</summary>

| File | Source | Description |
|------|--------|-------------|
| `1002–1003` | amd-gfx | gfx12: warn (not BUG) for invalid SDMA engine |
| `1025` | amd-gfx | DCN4: enable PSR and Replay on DCN4 variants |
| `1031` | amd-gfx | DCN4: enable pstate for non-emulation builds |
| `1033` | amd-gfx | DCN42b: increase uclk value |
| `1039` | amd-gfx | gfx11: allocate enough space for HPD info |
| `1041` | amd-gfx | gfx12: only remap KCQs when reset via MMIO |
| `1050–1053` | amd-gfx | GMC 9/10/11/12: disallow GFXOFF around TLB flushes |
| `1054–1058` | amd-gfx | SDMA 5.0/5.2/6/7: TLB invalidation buffer func callbacks |
| `1059–1060` | amd-gfx | GMC: core TLB invalidation helper via SDMA |
| `1061–1063` | amd-gfx | GMC 10/11/12: switch to new TLB inv helpers |
| `1064` | amd-gfx | amdgpu: switch order of GC and Display IP blocks |
| `1065` | amd-gfx | DCN42b: add SMU clock table read |

</details>

<details>
<summary>Block I/O (1077–1081)</summary>

| File | Source | Description |
|------|--------|-------------|
| `1077–1078` | Upstream (Jens Axboe) | mq-deadline: direct queue pass-in, skip merges if contended |
| `1079–1081` | Upstream (Jens Axboe) | bfq: direct queue pass-in, serialize dispatch, skip merges |

</details>

<details>
<summary>Memory management and cpuidle (1082–1084)</summary>

| File | Source | Description |
|------|--------|-------------|
| `1082` | sirlucjan | zstd 7.2: merge changes from dev tree |
| `1083` | sirlucjan | mm 7.2: introduce LRU MARIE |
| `1084` | Masahito S | nap v0.5.0 cpuidle governor |

</details>

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
cpuidle.governor=nap amd_pstate.epp_boost=1
```

- `cpuidle.governor=nap` — activates the NAP cpuidle governor by default; without this the module loads but does not activate.
- `amd_pstate.epp_boost=1` — enables per-core EPP boost for recently-busy CPUs on Zen 4. Requires the `epp_boost` patch series (patches 0018–0019).

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
makepkg -s
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
- **LRU MARIE conflict with vm_swappiness**: The MARIE patch (`1083`) was sourced from the CachyOS-rebased version rather than the raw sirlucjan tree to avoid a `CONFIG_CACHY` vm_swappiness conflict.
- **NAP governor**: NAP requires the `cpuidle.governor=nap` kernel parameter to activate. This build bakes it into `CONFIG_CMDLINE` so it is not needed on the boot command line.
- **Patches 1025, 1031, 1033 reverse-applied**: `1025` (PSR/Replay), `1031` (DCN4 pstate enable), and `1033` (dcn42b uclk increase) are applied then immediately reverse-applied in `prepare()` because they cause display freezes and UCLK switching glitches on the RX 9070 XT. Restoring the vanilla `.pstate_enabled = false` setting keeps the GPU cool and power-efficient in `auto` mode without screen glitches.
- **Patch 0003 is not upstream**: The PROFILE_PEAK patch modifies SMU14 power management in ways that have not been reviewed by AMD or the upstream community.

---

## Repository layout

```
PKGBUILD                  Build script (Arch Linux makepkg format)
config                    Base kernel .config (from CachyOS)
disable_configs.py        Script to strip CachyOS-specific symbols before olddefconfig
0001-0058-*.patch         Local and upstream SMU14/DCN401/EDID/HDMI patches
0101-0109-cachy-*.patch   Squashed CachyOS branch patches (one per branch)
1000-2200-*.patch         Upstream patches (amd-gfx, drm-next, linux-pm, block, mm, cpuidle)
9001-9007-*.patch         agd5f staging backports
net-tune/                 Unified CAKE SQM + latency tuning systemd service
PATCH_SOURCES.md          Per-patch source URLs and commit hashes
GUIDE.md                  Developer notes (build, patch workflow, CI)
```
