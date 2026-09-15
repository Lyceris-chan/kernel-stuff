# linux-sleepy-next

`linux-sleepy-next` is a custom Arch Linux kernel for one machine: an AMD
Ryzen 7 7700 (Zen 4) desktop with a Radeon RX 9070 XT (Navi 48 / RDNA 4). It is
built from **mainline Linux 7.3-rc3** plus a sanitized
[CachyOS](https://github.com/CachyOS/linux-cachyos) patchset and 216 targeted
upstream/local patches. It is not a general-purpose kernel.

**Base version:** `7.3.0_rc3-14` · **Artifact:**
`linux-sleepy-next-7.3.0_rc3-14-x86_64.pkg.tar.zst`

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | Radeon RX 9070 XT (Navi 48) | `gfx1201` (GC 12.0), `DCN401` (DCN 4.0.1), `SMU14`, `PSP14` |
| NIC | Realtek RTL8125B | in-kernel `r8169` |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline`, `kyber` |
| Scheduler | sched-ext | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

## Highlights

- **Clang ThinLTO `-O3 -march=znver4`** via the kernel.org pre-built LLVM
  23.1.0.
- **LRU-MARIE 0.11.1r2** page eviction — the author's `mm/lru_marie/` subsystem
  carried byte-identical, rebased to this base.
- **`mm/gup` folio batching** (Rik van Riel's series) for mTHP throughput.
- **BBR3** default + CAKE SQM via `net-tune`; ACPI CPPC hardening + per-core EPP
  boost for `amd-pstate`.
- **DCN4 display work**: HDMI FreeSync/VRR/ALLM, colorops, and the upstream
  HF-VSDB MCCS fix.
- **kbuild build-speedup series** — full kernel builds in ~8 minutes.
- **userq hardening** — Zhu Lingshan's kref lifecycle series closes use-after-free
  races in the user-queue submission path (`9062`–`9071`).
- **xswap** — extendable compressed swap backed by zswap (`2155`–`2166`); it
  replaces the fixed-size zram device on this machine.

## Build and install

```bash
cd sleepy-next
rm -rf src pkg
updpkgsums          # after any source=()/patch edit
makepkg -f -s -c
sudo pacman -U linux-sleepy-next-<version>-x86_64.pkg.tar.zst \
               linux-sleepy-next-headers-<version>-x86_64.pkg.tar.zst
```

Name the packages explicitly instead of globbing
`linux-sleepy-next-*.pkg.tar.zst`: older builds stay in this directory, so the
glob installs several versions at once.

Pacman regenerates the boot entry itself. The hook
`/usr/share/libalpm/hooks/sdboot-kernel-update.hook` fires on
`usr/lib/modules/*/vmlinuz` and runs `sdboot-manage autogen`; the `mkinitcpio`
hook rebuilds the initramfs in the same transaction. To do it by hand, run
`sudo sdboot-manage autogen`.

This machine boots **systemd-boot**, so there is no `grub-mkconfig` step. The
effective default entry comes from an EFI variable, not from
`/boot/loader/loader.conf` — check it with `bootctl status`, which is
authoritative, rather than by reading that file.

The build prompts for CAKE SQM speeds (default on, 80/80 Mbit); non-interactive
builds install the shipped config.

## Kernel command line (baked in)

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0 amdgpu.dcdebugmask=0x800
```

`pcie_aspm=off` + `amdgpu.aspm=0/runpm=0` are the drm/amd !5538 SMU bus-drop
stopgaps (DPM stays on). `cpuidle.governor=nap` activates the NAP governor, and
`amd_pstate.epp_boost=1` enables the per-core EPP boost.

`amdgpu.dcdebugmask=0x800` disables the DCN4 idle power states. The 7.2 line
dropped it after the display "box" turned out to be a COSMIC compositor bug,
and the rc3 line re-added it while bisecting the MSI MAG251RX flicker at
1920x1080@240Hz (worst under cursor movement). The flicker itself stopped in
rc3-9: patch `1164` restores the rc2 MCCS clear so the MAG251RX is no longer
advertised as VRR-capable, matching the cachyos-rc kernel that was verified
clean on this monitor. The mask stays because it reduced the flicker frequency
before that fix and covers the clock-gated HUBP flip-pending misread: when the
HUBP is clock-gated, `hubp2_is_flip_pending()` reports no pending flip, so flip
completion can arrive before the hardware latches (AMD's `f64a9be56536`
concedes the gap). It costs idle power; drop it if a proper DCN4 flip-pending
fix lands.

## Patch series

216 patches. `PATCH_SOURCES.md` is the authoritative per-patch ledger.

| Range | Category |
|---|---|
| `0001–0049` | Handmade local (SMU14, DCN401, GFX12) |
| `0050–0099` | Upstream EDID/display ML patches |
| `0101–0113` | CachyOS squashes |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) |
| `1100–1199` | AMD Display (DCN4, colorops) |
| `1200–1299` | AMD PM (amd-pstate, ACPI CPPC) |
| `2000–2099` | Block / I/O (bfq, mq-deadline, zram, io_uring) |
| `2100–2199` | Memory and swap (zstd, LRU-MARIE, MGLRU, gup, xswap) |
| `2200–2299` | CPU idle (NAP) |
| `2300–2399` | Build system / kbuild |
| `2400–2499` | Core scheduler (non-CachyOS) |
| `2500–2599` | x86 / arch core |
| `2600–2699` | Time / timers |
| `9000–9099` | agd5f staging + userq lifecycle backports |

## Documentation

`GUIDE.md` (this directory) covers toolchain, PROFILE_PEAK, troubleshooting, and
net-tune. `../net-tune/README.md` documents the SQM service, and
`../swap-stack/README.md` the zswap + xswap swap setup.
`../../CLAUDE.md` holds the maintenance rules; `../PATCH_SOURCES.md` the ledger.
