# linux-sleepy-rc: build guide

Build details for `linux-sleepy-rc` (mainline **Linux 7.3** + the sleepy
series). See `README.md` for what the kernel is; `../../CLAUDE.md` for the
maintenance rules.

## Toolchain

| Setting | Value |
|---|---|
| Compiler | Clang 23.1.4 (kernel.org ClangBuiltLinux `llvm-23.1.4-x86_64.tar.xz`, auto-downloaded) |
| Linker | `ld.lld` |
| LTO | ThinLTO (`CONFIG_LTO_CLANG_THIN=y`) |
| Optimization | `-O3` + `-march=znver4` |

Flags are fixed: `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. Never substitute
`ld.mold` (crashes on kernel vDSO linker scripts). The prebuilt toolchain is a
multicall build — `clang`, `ld.lld` and the `llvm-*` tools are symlinks to one
`llvm` binary — and links only the system `libz`/`libzstd`/`libstdc++`; no ICU
bundle is needed.

## Build

```bash
cd sleepy-rc
rm -rf src pkg          # stale patched files cause false conflicts
updpkgsums              # after any source=() or patch-file edit
makepkg -f -s -c
sudo pacman -U linux-sleepy-rc-*.pkg.tar.zst linux-sleepy-rc-headers-*.pkg.tar.zst
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

## Reclaim policy: lru_cast (CAST)

The rc package carries **lru_cast 0.2.5** (`2102`) as its page-replacement
policy. It is on at boot. Both packages carry it; the preview applies a port
of the same patch to the linux-next base.

```bash
cat /sys/kernel/mm/lru_cast/version      # 0.2.5
cat /sys/kernel/mm/lru_cast/enabled      # 1
cat /sys/kernel/mm/lru_cast/estimate     # anon share, measured swappiness, costs
```

`vm.swappiness` is **1**, which CAST honours as the file-first promise (file
down to the clean-file floor, then anon) rather than as the start of its
measured split. Set it to `60` to let CAST measure the anon/file split itself;
`0` and `200` are the other two promises. The clean-file floor is
`/sys/kernel/mm/lru_cast/clean_min_ratio` (default 10, % of node memory).

To fall back without rebuilding, switch CAST off and MGLRU on — the two are
never on at once, and enabling the active one's alternative returns `EBUSY`:

```bash
echo 0 > /sys/kernel/mm/lru_cast/enabled   # CAST off -> legacy LRU
echo y > /sys/kernel/mm/lru_gen/enabled    # MGLRU on
```

Boot with `lru_cast=0` to start with CAST off.

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
- **CAST and MGLRU are never on at once** (both are built; switch the active
  one off before enabling the other), and **scx full-switch mode bypasses CFS
  load balancing** — carried patches for either subsystem do nothing while the
  other owns it.
