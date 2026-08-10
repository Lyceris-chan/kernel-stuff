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
  series (`9033`–`9035`: FENCE-chunk leak, VM overrun, BO-VA kmap offset), and
  the gfx12 userq sub-page VA-validation fix (`9036`).
  The Exit-idle-optimizations series merged upstream into rc6 and was dropped.
  The SMU14 PPT-limits framework rework from the same tag is **deferred to 7.3**
  (does not apply cleanly to the rc7 series state).
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
false conflicts), refresh checksums after any `source=()` change, and build:

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

Per-patch manifest of the full 140-patch series. See `PATCH_SOURCES.md` for full
provenance (authors, commit hashes, Message-IDs).

### Local / upstream SMU14 + DCN401 (0001–0034)

| Patch | What it does | Source |
|---|---|---|
| `0001` | Fixes a typo in `smu_v14_0_set_irq_state()` (SMU14 IRQ `type` param). | Handmade (Antigravity) |
| `0002` | Fixes a memory leak in `smu_v14_0_fini_smc_tables()`. | Handmade (Antigravity) |
| `0003` | Lets the GFXCLK ceiling float in PROFILE_PEAK on SMU14. | Handmade (Antigravity) |
| `0004` | Disables GPU deep sleep while PROFILE_PEAK is forced; re-enables it at other levels and keeps it off under COMPUTE. | Handmade (Antigravity) |
| `0005` | Disables SMU14 mode1 reset under SR-IOV. | Handmade (Antigravity) |
| `0006` | Adds bounds checking to SMU14 I2C commands. | Handmade (Antigravity) |
| `0007` | Removes a redundant mutex lock in the SMU14 I2C update path. | Handmade (Antigravity) |
| `0008` | Fixes SMU14 power-limit reporting logic (unlocks max PPT). | Handmade (Sleepy/Antigravity) |
| `0010` | Fixes named-barrier restore in the gfx12.1 trap handler. | amd-gfx ML |
| `0030` | Proactively shrinks DET for pipes losing bandwidth. | Handmade (Antigravity) |
| `0031` | Fixes a memory leak in DCN20 link-encoder resource init. | Handmade (Antigravity) |
| `0032` | Fixes an OOB array access in the HPO FRL link encoder. | Handmade (Antigravity) |
| `0033` | Adds missing HPO FRL link-encoder register init. | Handmade (Antigravity) |
| `0034` | Prevents a memory leak during IRQ-service destroy. | Handmade (Antigravity) |

### Upstream EDID / HDMI (0050–0058)

| Patch | What it does | Source |
|---|---|---|
| `0050` | Parses the AMD VSDB for the FreeSync refresh range. | amd-gfx ML |
| `0055` | Parses HDMI 2.1 gaming (ALLM/VRR) caps from the HF-VSDB. | amd-gfx ML |
| `0058` | Restores the FRL cap on non-destructive HDMI link verify. | amd-gfx ML |

### CachyOS branches (0101–0113)

| Patch | What it does | Source |
|---|---|---|
| `0101` | Backports BBRv3 TCP congestion control; sets it as the compiled default. | CachyOS (sirlucjan) |
| `0102` | Allows `-O3` in kbuild. | CachyOS (sirlucjan) |
| `0103` | Adds x86_64 Zen 4 ISA optimizations (`-march=znver4`). | CachyOS (sirlucjan) |
| `0104` | Adds VRAM cgroup accounting for drm/ttm. | CachyOS (sirlucjan) |
| `0105` | Squashes the full 26-patch fixes branch, including off-target hardware. | CachyOS (sirlucjan) |
| `0106` | Reverts the off-target hardware changes carried in the full fixes squash (i915, btusb, rtw89, laptop audio, SOF, iwlwifi, nouveau). | CachyOS (sirlucjan) |
| `0107` | Backports the HDMI 2.1 FreeSync/VRR/PCON series (26 patches, excludes `0151`). | CachyOS (sirlucjan) |
| `0108` | Adds SMP preemption + TLB flush (14 patches). | CachyOS (sirlucjan) |
| `0109` | Adds EDID DSC BPP parsing (8 patches). | CachyOS (sirlucjan) |
| `0110` | CONFIG_CACHY config hooks — sched EEVDF latency tuning, THP defrag, lru-gen working-set, compaction/watermark off, bus_lock SLD. | CachyOS/linux fork (curated) |
| `0111` | Disable the legacy ACPI bus-master poll on AMD C3 (Zen 4 idle). | CachyOS/linux fork |
| `0112` | Skip VRAM eviction at S4/S5 poweroff (faster GPU shutdown). | CachyOS/linux fork |
| `0113` | Micro-opts: readahead 256K, sched/readdir hints, `list.h` inline, evdev `call_rcu`. | CachyOS/linux fork |

### GPU core (1000–1026)

| Patch | What it does | Source |
|---|---|---|
| `1000` | Converts gfx12.1 invalid-SDMA-engine `BUG()` to `WARN()`. | drm-next |
| `1001` | Converts gfx12 invalid-SDMA-engine `BUG()` to `WARN()`. | drm-next |
| `1002` | Allocates enough space for HPD info on gfx11. | drm-next |
| `1003` | Only remaps KCQs when reset via MMIO on gfx12. | drm-next |
| `1004` | Disallows GFXOFF around TLB flushes on GMC9. | drm-next |
| `1005` | Disallows GFXOFF around TLB flushes on GMC10. | drm-next |
| `1006` | Disallows GFXOFF around TLB flushes on GMC11. | drm-next |
| `1007` | Disallows GFXOFF around TLB flushes on GMC12. | drm-next |
| `1008` | Adds a buffer-funcs callback for TLB invalidation. | drm-next |
| `1009` | Adds a TLB-invalidation buffer-func callback to SDMA 5.0. | drm-next |
| `1010` | Adds a TLB-invalidation buffer-func callback to SDMA 5.2. | drm-next |
| `1011` | Adds a TLB-invalidation buffer-func callback to SDMA 6. | drm-next |
| `1012` | Adds a TLB-invalidation buffer-func callback to SDMA 7. | drm-next |
| `1013` | Adds a core helper for SDMA-based TLB invalidation. | drm-next |
| `1014` | Adds more GMC TLB-invalidation helpers. | drm-next |
| `1015` | Switches GMC10 to the new TLB-invalidation helpers. | drm-next |
| `1016` | Switches GMC11 to the new TLB-invalidation helpers. | drm-next |
| `1017` | Switches GMC12 to the new TLB-invalidation helpers. | drm-next |
| `1018` | Switches the order of GC and Display IP blocks (DCN42B). | drm-next |
| `1019` | Updates the mmhub 4.2.0 client list. | drm-next |
| `1020` | Fixes the MMHUB0 check in the gmc12.1 pasid TLB flush (copy-paste typo). | amd-gfx ML |
| `1023` | `amdgpu.ignore_min_pcap=1` module param — override the SMU min power cap (Liquorix, CachyOS backport). | CachyOS/linux fork |
| `1024` | Fixes dropped MES dispatches under queue oversubscription (GFX12 MES). | drm-next `288cc4a54` (7.3 last-round backport) |
| `1026` | Fixes a GFX12 KFD CRIU-restore NULL-deref panic (implemented `restore_mqd`/`checkpoint_mqd` callbacks + NULL guards). | amd-gfx ML 2026-08-04 (reconstructed from mbox) |

(`1020`–`1022` merged upstream in 7.2-rc7 and were dropped on the bump; `1025`
gfx12 priv-fault recovery dropped — needs gfx11 priv-fault infra absent from rc7.)

### Display (1100–1136)

| Patch | What it does | Source |
|---|---|---|
| `1100` | Enables PSR and Replay on DCN4 and fixes the AUX instance. | drm-next |
| `1101` | Enables pstate for DCN4 non-emulation builds; reverse-applied to keep `.pstate_enabled = false`. | drm-next |
| `1102` | Increases the dcn42b UCLK value. | drm-next |
| `1103` | Adds a dcn42b-specific SMU clock-table read. | drm-next |
| `1104` | Adds MALL status readback for DCN 4.0.1. | drm-next |
| `1105` | Adds DCN42B `VID_CRC_CONTROL` and `HBLANK_CONTROL` registers. | drm-next |
| `1106` | Updates the memclk clock-table read for dcn42. | drm-next |
| `1107` | Enables `hdmistreamclk_rcg` by default for dcn42. | drm-next |
| `1108` | Adds MCIF ARB programming structures (DCN401/DCN42). | drm-next |
| `1109` | Adds updated MCIF ARB register definitions. | drm-next |
| `1110` | Ports DCN4+ MCIF ARB programming to the new format. | drm-next |
| `1111` | Fixes `dc_stream_remove_writeback()` dropping wrong writeback entries. | drm-next |
| `1113` | Fixes DSC-over-HDMI-FRL mode pruning (compressed FRL cap check dispatch). | drm-next |
| `1114` | Ensures `dtbclk` clk_src is selected before `hdmistream_clk_en` (DCN42B HDMI clock sequence). | drm-next |
| `1115` | Fixes a wrong register field in `dccg35_set_hdmistreamclk_src_new` (`HDMISTREAMCLK0_SRC_SEL`). | drm-next |
| `1116` | Adds the dcn42b SOC/IP translator (DML2 prereq for 1117). | drm-next |
| `1117` | Fixes `dcn42b_soc_bb.h` (gpuvm_min_page_size 256→4 for 4K pages). | drm-next |
| `1118` | Adds the replay-residency function (DC/debugfs). | drm-next |
| `1119` | Fixes the force-FRL-rate debug setting. | drm-next |
| `1120` | **PSR/Replay Part 2** — actually enables PSR/Replay on DCN42B (completes 1100). | drm-next |
| `1121` | Enables IPS support for the DCN4 variant. | drm-next |
| `1122` | Enables zstate support and fixes DCN42B clk-src masks. | drm-next |
| `1123` | Enables HUBP/DPP driver power gating for DCN42. | drm-next |
| `1124` | Corrects the `vblank_end` calc for the FAMS cmd packet. | agd5f |
| `1125` | Fixes rounding errors in `CalculatePrefetchSchedule`. | agd5f |
| `1126` | Fixes debug-flag assignment in `dmub_replay.c`. | agd5f |
| `1127` | Adds block-sequence support for bandwidth programming (prereq for 1128/1129). | drm-next |
| `1128` | Registers DCN as a PMFW DF C-state client on DCN42 (DCN42B boot-hang fix). | drm-next |
| `1129` | Ensures `dtbclk` is enabled (DCN42). | amd-gfx ML (Roman.Li DC batch) |
| `1130` | Updates the VRR info packet to support 12-bit refresh rates. | amd-gfx ML (Roman.Li DC batch) |
| `1131` | Adds missing DCN42B register defines. | amd-gfx ML (Roman.Li DC batch) |
| `1132` | Adds missing DMUB CACP and PR definitions. | amd-gfx ML (Roman.Li DC batch) |
| `1133` | Adds FFE level defaults (DCN6 hunks stripped — absent from rc7). | amd-gfx ML (Roman.Li DC batch) |
| `1134` | Fixes BT.2020 YCbCr limited-output CSC matrix (too-bright HDR on calibrated panels; author-tested on 9070 XT). | amd-gfx ML (Nathan Lucas, 2026-08-02; P2 DCE copy rejected — off-target) |
| `1135` | Fixes DCN42B HPD toggle-filter unit programming (wrong HW unit → extremely long connection time). | amd-gfx ML (Tom Chung series 12/34, 2026-08-05) |
| `1136` | Updates/reverts FRL LT timeout: polls on no-timeout and bounds the ≥16 Gbps LT timer. | amd-gfx ML (Tom Chung series 20/34, 2026-08-05) |

### Power management (1200–1209)

| Patch | What it does | Source |
|---|---|---|
| `1200` | Documents missing kernel-doc members in amd-pstate. | linux-pm |
| `1201` | Updates `cppc_req_cached` before writing the MSR. | linux-pm |
| `1202` | Adds per-core EPP boost for recently-busy CPUs. | linux-pm |
| `1203` | Documents the `epp_boost` parameter. | linux-pm |
| `1205` | Skips amd-pstate-ut tests when the driver is inactive. | linux-pm |
| `1206` | Fixes the EPP return type and init error handling. | linux-pm |
| `1207` | Toggles `auto_sel` in active mode on shared-memory systems. | linux-pm |
| `1208` | Caches the firmware-programmed EPP value. | linux-pm |
| `1209` | Handles a missing policy in dynamic EPP callbacks. | linux-pm |

`1204`, `1210`–`1213` merged upstream in 7.2-rc6 and dropped from the series.

### Block / I/O (2000–2004)

| Patch | What it does | Source |
|---|---|---|
| `2000` | Passes the queue directly to `dd_insert_request()`. | CachyOS (sirlucjan) |
| `2001` | Skips expensive merge lookups in mq-deadline when contended. | CachyOS (sirlucjan) |
| `2002` | Passes the queue directly to `bfq_insert_request()`. | CachyOS (sirlucjan) |
| `2003` | Serializes request dispatching in BFQ. | CachyOS (sirlucjan) |
| `2004` | Skips expensive merge lookups in BFQ when contended. | CachyOS (sirlucjan) |

### Memory (2100–2101)

| Patch | What it does | Source |
|---|---|---|
| `2100` | Merges zstd changes from the dev tree for 7.2. | CachyOS (sirlucjan) |
| `2101` | Introduces LRU-MARIE 0.9.3 page eviction (orphaned-L1-bit self-heal fix; `vma_flags` fix kept). | firelzrd/lru_marie commit `0e08603` (2026-08-07) |

### CPU idle (2200)

| Patch | What it does | Source |
|---|---|---|
| `2200` | NAP cpuidle governor v0.5.0 for 7.2. | CachyOS (sirlucjan) |

### agd5f/staging backports (9001–9024)

| Patch | What it does | Source |
|---|---|---|
| `9001` | Drops all `BUG()`s in gfx12. | agd5f staging |
| `9002` | Drops all `BUG()`s in gfx12.1. | agd5f staging |
| `9003` | Replaces a PSP14 `BUG()` with an error. | agd5f staging |
| `9006` | Uses more optimal copy-packet sizes for copy/fill in TTM. | agd5f staging |
| `9007` | Programs DB_RING_CONTROL on gfx12. | agd5f staging |
| `9008` | Reads `TA_CNTL2.TRUNCATE_COORD_MODE` on gfx12 (conformant truncation flag). | amd-gfx ML |
| `9009` | Drops all `BUG()`s in mes12.1. | drm-next |
| `9010` | Turns imu12 `BUG()`s into `WARN()`s. | drm-next |
| `9011`–`9024` | **Retry-fault handling v3** (14 patches, Timur Kristóf): respects `noretry` on GFX12.1, enables retry-fault interrupts, IH soft-ring + `retry_cam_ack`, gmc11/12 `cam_index` passthrough, NOALLOC fault handling, IH6.0/7.0 MMIO ACK, **retry CAM on Navi 3/4 dGPUs**. | amd-gfx ML |

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch Linux build script |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `NNNN-*.patch` | Patch series (see ranges above) |
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
