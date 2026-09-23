# linux-sleepy-next: build guide

Build details for `linux-sleepy-next` (mainline **Linux 7.3-rc3** + the sleepy
series). See `README.md` for what the kernel is; `../../CLAUDE.md` for the
maintenance rules.

## Toolchain

| Setting | Value |
|---|---|
| Compiler | Clang 23.1.0 (GitHub `llvmorg-23.1.0` release asset, auto-downloaded) |
| Linker | `ld.lld` |
| LTO | ThinLTO (`CONFIG_LTO_CLANG_THIN=y`) |
| Optimization | `-O3` + `-march=znver4` |

Flags are fixed: `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. Never substitute
`ld.mold` (crashes on kernel vDSO linker scripts). The prebuilt LLVM links
against ICU 70; the PKGBUILD bundles those libs (`llvm-icu70-libs.tar.gz`).

## Build

```bash
cd sleepy-next
rm -rf src pkg          # stale patched files cause false conflicts
updpkgsums              # after any source=() or patch-file edit
makepkg -f -s -c
sudo pacman -U linux-sleepy-next-*.pkg.tar.zst linux-sleepy-next-headers-*.pkg.tar.zst
```

A full build runs at the PKGBUILD's `_jobs=16`. Build wall-clock is dominated
by the serial stages (extract, patch, vmlinux link, BTF, kallsyms, packaging)
rather than by compilation: `-j8` measures 6m22s and `-j16` 6m03s, so the job
count is not a meaningful speed lever. It was capped at 8 briefly, after an
rc4-7 thrash that was later attributed to MARIE's swappiness clamp instead —
see the PKGBUILD comment. Expect kernel ~22 MB,
headers ~34 MB.

## PROFILE_PEAK (patches `0003` / `0004`)

Local patches to `smu_v14_0.c`: `0003` lets the GFXCLK ceiling float to the
hardware boost limit (>3.0 GHz) while `PROFILE_PEAK` is forced; `0004` disables
deep sleep in `PROFILE_PEAK` (and while COMPUTE is active) to cut wake latency.

```bash
echo profile_peak | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level
```

## net-tune (CAKE SQM + latency tuning)

One systemd unit applies low-latency Ethernet tuning (`ENABLE_LATENCY`) and CAKE
shaping (`ENABLE_SQM`), each toggleable in `/etc/net-tune.conf`. SQM ships on at
80/80 Mbit, so set your real line rate. BBR3 is the compiled-in default; the
service only shapes CAKE.

See [`../net-tune/README.md`](../net-tune/README.md) for configuration,
requirements, and verification.

## Known issues

- **Display artifact (the "box")** — a rectangle over application windows that
  does not appear in screenshots, disappears when the cursor moves over it, and
  shows on whichever monitor last had VRR toggled. **This is a COSMIC
  (cosmic-comp) bug, not a kernel one**: it hands fullscreen content to an
  overlay plane. Fix it in `/etc/environment` and log back in:

  ```
  COSMIC_DISABLE_OVERLAY_SCANOUT=1
  ```

  `COSMIC_DISABLE_DIRECT_SCANOUT=1` also works, because it removes the overlay
  bit too. See `LESSONS.md` for the full diagnosis.
- **BTF symbol collision**: old `TCP_CONG_BBR` and `TCP_CONG_BBR3` define the
  same BTF kfunc — the old BBR stays disabled.
- **DWARF5 required** with Clang 23 + pahole 1.31 (`DEBUG_INFO_DWARF5`).
- **Upstream RDNA4 bugs are open** (drm/amd #5722 display panic, #5684 `optc`
  REG_WAIT hang). The DCN4 flip-schedule patches that made these worse
  (`9051`/`9052`) were dropped — AMD reverted them upstream.
- **`pcie_aspm=off`** slightly raises idle PCIe power draw (the !5538 stopgap).
- **LRU-MARIE and MGLRU are mutually exclusive**, and **scx full-switch mode
  bypasses CFS load balancing** — carried patches for either subsystem do
  nothing while the other owns it.
