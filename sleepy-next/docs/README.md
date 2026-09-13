# linux-sleepy-next

`linux-sleepy-next` is a custom Arch Linux kernel for one machine: an AMD
Ryzen 7 7700 (Zen 4) desktop with a Radeon RX 9070 XT (Navi 48 / RDNA 4). It is
built from **mainline Linux 7.3-rc2** plus a sanitized
[CachyOS](https://github.com/CachyOS/linux-cachyos) patchset and 175 targeted
upstream/local patches. It is not a general-purpose kernel.

**Base version:** `7.3.0_rc2-10` · **Artifact:** `linux-sleepy-next-7.3.0_rc2-10-x86_64.pkg.tar.zst`

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | Radeon RX 9070 XT (Navi 48) | `gfx1201` (GC 12.0), `DCN401`, `DCN42B`, `SMU14`, `PSP14` |
| NIC | Realtek RTL8125B | in-kernel `r8169` |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline`, `kyber` |
| Scheduler | sched-ext | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

## Highlights

- **Clang ThinLTO `-O3 -march=znver4`** via the kernel.org pre-built LLVM 23.1.0.
- **LRU-MARIE 0.11.0** page eviction — the author's `mm/lru_marie/` subsystem
  carried byte-identical, rebased to this base.
- **`mm/gup` folio batching** (Rik van Riel's series) for mTHP throughput.
- **BBR3** default + CAKE SQM via `net-tune`; ACPI CPPC hardening + per-core EPP
  boost for `amd-pstate`.
- **DCN4 display work**: HDMI FreeSync/VRR/ALLM, FRL, colorops, and the
  upstream HF-VSDB MCCS fix.
- **kbuild build-speedup series** — full kernel builds in ~8 minutes.

## Build and install

```bash
cd sleepy-next
rm -rf src pkg
updpkgsums          # after any source=()/patch edit
makepkg -f -s -c
sudo pacman -U linux-sleepy-next-*.pkg.tar.zst linux-sleepy-next-headers-*.pkg.tar.zst
sudo grub-mkconfig -o /boot/grub/grub.cfg   # or your bootloader
```

The build prompts for CAKE SQM speeds (default on, 80/80 Mbit); non-interactive
builds install the shipped config.

## Kernel command line (baked in)

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0 amdgpu.dcdebugmask=0x800
```

`pcie_aspm=off` + `amdgpu.aspm=0/runpm=0` are the drm/amd !5538 SMU bus-drop
stopgaps (DPM stays on). `amdgpu.dcdebugmask=0x800` disables DCN4 Idle Power
States.

## Patch series

175 patches. `PATCH_SOURCES.md` is the authoritative per-patch ledger.

| Range | Category |
|---|---|
| `0001–0049` | Handmade local (SMU14, DCN401, GFX12) |
| `0050–0099` | Upstream EDID/display ML patches |
| `0101–0113` | CachyOS squashes |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) |
| `1100–1199` | AMD Display (DCN4/42B, FRL, colorops) |
| `1200–1299` | AMD PM (amd-pstate, ACPI CPPC) |
| `2000–2099` | Block / I/O (bfq, mq-deadline, zram, io_uring) |
| `2100–2199` | Memory (zstd, LRU-MARIE, MGLRU, gup batching) |
| `2200–2299` | CPU idle (NAP) |
| `2300–2399` | Build system / kbuild |
| `2400–2499` | Core scheduler (non-CachyOS) |
| `2500–2599` | x86 / arch core |
| `2600–2699` | Time / timers |
| `9000–9099` | agd5f staging backports |

## Documentation

`GUIDE.md` (this directory) covers toolchain, PROFILE_PEAK, troubleshooting, and
net-tune. `../net-tune/README.md` documents the SQM service.
`../../CLAUDE.md` holds the maintenance rules; `../PATCH_SOURCES.md` the ledger.
