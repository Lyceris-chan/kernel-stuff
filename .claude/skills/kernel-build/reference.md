# Kbuild configuration reference

Detail doc for the `kernel-build` skill. Load this when touching `prepare()`,
`scripts/config` calls, version strings, or the SQM service.

## Key `scripts/config` calls already in `prepare()`

```bash
# CPU target
scripts/config -d GENERIC_CPU -e MZEN4

# Compiler optimization
scripts/config -d LTO_NONE -e LTO_CLANG_THIN
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3

# CachyOS config hooks (no CONFIG_CACHY — the Kconfig symbol exists only in the
# CachyOS/linux fork, not the sirlucjan branches we carry, so -e CACHY was dropped)

# NAP governor baked into cmdline (bootloader params still appended, not replaced)
scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap" -d CMDLINE_OVERRIDE

# BPF/debug (bpftune)
scripts/config -d DEBUG_INFO_NONE -e DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_BTF
scripts/config -e BPF_SYSCALL -e FTRACE -e BPF_EVENTS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e KPROBE_EVENTS

# Memory management
scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE
scripts/config -e CPU_IDLE_GOV_NAP

# Network (CAKE SQM)
scripts/config -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32

# Bloat removal
scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU
scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN
scripts/config -d SECURITY_APPARMOR
scripts/config -d AUDIT -d AUDITSYSCALL
```

## Version string

```bash
echo "-$pkgrel" > localversion.10-pkgrel
echo "-${pkgbase#linux-}" > localversion.20-pkgname
scripts/config --set-str LOCALVERSION ""
```

Resolves to `uname -r` → `<version>-<pkgrel>-sleepy`.

## net-tune (SQM / latency) / BBR3

The build ships the unified `net-tune` service (CAKE SQM + low-latency ethernet
tuning), enabled at boot. The shipped template enables SQM by default
(`ENABLE_SQM=yes`, 80/80 Mbit), so a build that skips the interactive prompt
(no TTY) installs shaping — it no longer silently ships `ENABLE_SQM=no`. The
interactive prompt during `prepare()` defaults to Y; an explicit "n" writes a
disabled conf. Pre-seed non-interactively only when you need custom speeds —
note `src/` must exist and is NOT wiped by makepkg (only `src/<kernel>/` is):

```bash
mkdir -p src
cat > .../src/net-tune.conf << EOF
ENABLE_SQM=yes
DOWNLOAD_MBIT="80"
UPLOAD_MBIT="80"
ENABLE_LATENCY=yes
EOF
touch .../src/.enable_sqm
```

Important: editing ANY `.patch` file (even only its commit-message body) changes
its BLAKE2 checksum — run `updpkgsums` after any patch-file change or the build
fails the source-validity check.

Files go in `src/` (after `prepare()` extracts source), not the repo root. The
route-detection probe uses Quad9 (`9.9.9.9`), never `8.8.8.8`.

## Why not `ld.mold`

Crashes on kernel vDSO linker scripts. If any future patch or config change
pulls it in as a dependency or default, force back to `ld.lld` — never adopt
`ld.mold` for this build.
