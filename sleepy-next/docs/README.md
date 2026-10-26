# linux-sleepy-next

`linux-sleepy-next` is a custom Arch Linux kernel for one machine: an AMD
Ryzen 7 7700 (Zen 4) desktop with a Radeon RX 9070 XT (Navi 48 / RDNA 4). It is
built from a **linux-next snapshot (`next-20261026`)** plus a sanitized
[CachyOS](https://github.com/CachyOS/linux-cachyos) patchset, in a 135-patch
series. It is not a general-purpose kernel.

**Base version:** `2026.10.26-2` · **Artifact:**
`linux-sleepy-next-2026.10.26-2-x86_64.pkg.tar.zst`

The release is named for the **snapshot date**, not the mainline release the
snapshot was cut from — linux-next is a daily tree, and its base release goes
stale within days of the cut. The date is dotted (`2026.10.26`) because both
`depmod` and `mkinitcpio` require the release string to begin with dotted
decimal notation; a bare `20261026` breaks module dependency generation and the
initramfs build.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | Radeon RX 9070 XT (Navi 48) | `gfx1201` (GC 12.0), `DCN401` (DCN 4.0.1), `SMU14`, `PSP14` |
| NIC | Realtek RTL8125B | in-kernel `r8169` |
| NVMe | Phison E16 PCIe 4.0 | `kyber` (`bfq`, `mq-deadline` built) |
| Scheduler | **BORE** (burst-oriented) | `CONFIG_SCHED_BORE=y`, `CONFIG_MIN_BASE_SLICE_NS=2000000` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

## Highlights

- **Clang ThinLTO `-O3 -march=znver4`** via the kernel.org ClangBuiltLinux
  pre-built LLVM 23.1.4.
- **lru_cast 0.2.5 (CAST)** page eviction — Masahito Suzuki's successor to
  LRU-MARIE, carried as `2102`. The same patch is applied here as a port to
  this base (three insertion sites and one helper rename; recorded in
  `../PATCH_SOURCES.md`). It keeps Marie's per-PFN state array, SIMD walker,
  look-around, kcompressd and clean-file floor, and replaces the generational
  ring with a measured LRFU. Both packages carry it.
- **`mm/gup` folio batching** (Rik van Riel's series) for mTHP throughput.
- **BBR3** default + CAKE SQM via `net-tune`; ACPI CPPC hardening + per-core EPP
  boost for `amd-pstate`.
- **DCN4 display work**: HDMI FreeSync/VRR/ALLM, colorops, and the upstream
  HF-VSDB MCCS fix.
- **kbuild build-speedup series**. Build parallelism is `_jobs=16` in the
  PKGBUILD. It was briefly capped at 8 after an rc4-7 build thrashed — but that
  measurement was taken with MARIE's swappiness clamp cleared, so the machine
  was already thrashing before the build started, and the kills blamed on
  parallelism were in the patch phase, before any compilation. Re-measured
  against the fixed policy, `MemAvailable` never fell below 19 GB at `-j16`.
  Note the build is dominated by its serial stages: `-j8` takes 6m22s and
  `-j16` 6m03s, so the job count is not a meaningful speed lever.
- **userq hardening** — Zhu Lingshan's kref lifecycle series closes use-after-free
  races in the user-queue submission path (`9062`–`9071`).
- **sched-ext fixes** — the batch that closed a use-after-free (an error raised
  before the scheduler finished enabling left it running but undisableable) and
  a NULL sub-sched dereference in the compat kfuncs. Those landed upstream in
  `v7.3-rc4` and are no longer carried as patches.
- **zswap + swapfile** — a zstd-compressed pool in RAM in front of a 16 GiB
  swapfile on the NVMe. Chosen because its drain is automatic: the shrinker
  writes pool entries back to the entry's own swap device, so a real file
  behind the pool keeps anonymous pages reclaimable. zram's writeback never
  runs on its own, and `backing_dev` rejects a file outright.
  `swap-stack/` carries the userspace side. It replaced an xswap device on
  2026-09-22 (series removed, 15 patches).
- **CAST ranking is active; the anon/file split is held file-first.**
  `vm.swappiness` stays **1**, which CAST treats as a promise: reclaim file
  down to the clean-file floor (10% of memory), then anon. That is the
  measured-correct policy for this workload — roughly 27 GB of largely-cold
  page cache against ~2.3 GB of live anonymous working set. Letting anon go
  first was tried under MARIE on 2026-09-22 and produced 201M anon steals,
  192M anon refaults and PSI `full` at 16%. CAST's own measured split sits
  behind that promise: setting `vm.swappiness` to `60` would enable it, but
  that is a user decision, not a default. The LRFU ordering, per-lruvec
  reclaim, kcompressd and the clean-file floor all remain active. See
  `../../sleepy-rc/swap-stack/README.md`.

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
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0
```

`pcie_aspm=off` + `amdgpu.aspm=0/runpm=0` are the drm/amd !5538 SMU bus-drop
stopgaps (DPM stays on). `cpuidle.governor=nap` activates the NAP governor, and
`amd_pstate.epp_boost=1` enables the per-core EPP boost.

`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is deliberately **not** set in the
preview: it exists to exercise the snapshot's display code with IPS enabled.
`sleepy-rc` keeps the mask for the MAG251RX flicker history, documented in
`sleepy-rc/docs/README.md`.

## Patch series

135 patch entries in `source=()` (142 files; seven are excluded from the build). `PATCH_SOURCES.md` is the authoritative per-patch ledger.
On a linux-next snapshot a large fraction are skipped rather than failed, since
the snapshot already carries much of what the series adds — a skip is only safe
for a self-contained patch, so interdependent groups are excluded outright
instead.

| Range | Category |
|---|---|
| `0001–0049` | Handmade local (SMU14, DCN401, GFX12) |
| `0050–0099` | Upstream EDID/display ML patches |
| `0101–0113` | CachyOS squashes |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) |
| `1100–1199` | AMD Display (DCN4, colorops) |
| `1200–1299` | AMD PM (amd-pstate, ACPI CPPC) |
| `1300–1399` | GPU core follow-ups (KFD SMI/VM, CS validation) |
| `2000–2099` | Block / I/O (bfq, mq-deadline, zram, io_uring) |
| `2100–2199` | Memory and swap (zstd, lru_cast, gup, zswap) |
| `2200–2299` | CPU idle (NAP) |
| `2300–2399` | Build system / kbuild |
| `2400–2499` | Core scheduler (non-CachyOS) |
| `2500–2599` | x86 / arch core |
| `2600–2699` | Time / timers |
| `2700–2799` | zswap request stack (preview only) |
| `2800–2899` | Memory / swap follow-ups |
| `2900–2999` | VFS / core filesystem |
| `9000–9099` | agd5f staging + userq lifecycle backports |

## Documentation

`GUIDE.md` (this directory) covers toolchain, PROFILE_PEAK, troubleshooting, and
net-tune. `../net-tune/README.md` documents the SQM service, and
`../swap-stack/README.md` the zswap + swapfile stack and the swappiness policy.
`../../CLAUDE.md` holds the maintenance rules; `../PATCH_SOURCES.md` the ledger.
