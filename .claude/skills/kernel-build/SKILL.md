---
name: kernel-build
description: Build sleepy-kernel with makepkg, diagnose and fix a failed build, or verify bpftune/BTF requirements survived the build. Use for any request to build the kernel, run makepkg, triage a build failure, resolve a patch/hunk conflict during a build, or verify BTF/vmlinux after building.
---

# Kernel build

## Build

```bash
cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export
rm -rf src pkg
updpkgsums          # only if source=() changed since the last build
makepkg -f -s -c
sudo pacman -U linux-sleepy-*.pkg.tar.zst
```

Expect: kernel 19–25MB, headers 65–75MB. Core kernel >40MB
means bloat-removal failed — check that `disable_configs.py` actually ran
during `prepare()`. The NIC uses the in-kernel `r8169` (no `r8125` package);
webcams use `uvcvideo`; the build ships the `net-tune` service (CAKE SQM +
latency tuning).

Compile flags are fixed: `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. Never
substitute these (see `reference.md` for why `ld.mold` specifically breaks).

## How patches apply (important)

ALL patches — including the `9000` series — apply through the normal
`patch -Np1 --forward` loop in `prepare()` (PKGBUILD lines ~533–542). There is
**no** special `git apply` case for `9000` patches anymore (that changed this
maintenance session). `9000-drm-amd-display-Exit-idle-optimizations-before-programming.patch`
is a proper `git format-patch` file (v2, commit `8419331e64d9`, Leo Li) and
flows through the same loop as every other patch. If you see a 9000 patch fail,
diagnose it exactly like any other patch — do not invent a `git apply` bypass.

The only special-case reverse-apply in `prepare()` is for `1101`
(`drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch`), which is
reverse-applied with `patch -Np1 --forward -R` to keep `.pstate_enabled = false`.

## On failure, in this order (triage checklist)

### 1. Patch application failures
- Read the `.rej` file first:
  ```bash
  find src -name "*.rej" | head
  cat <path/to/file.c.rej>
  ```
- "Already applied" by an earlier patch or a CachyOS branch → remove the
  conflicting patch, note it in `PATCH_SOURCES.md`.
- Context lines shifted → regenerate from the source repo (see `patch-audit`).
- Test a patch independently against the clean tree:
  ```bash
  git -C repos/linux-7.2-rc5 apply --check <patch>     # forward
  git -C repos/linux-7.2-rc5 apply --check -R <patch>  # already-applied?
  ```

### 2. BTF failures (`Failed to generate BTF for vmlinux`)
Check in this order:
1. **Duplicate BTF kfunc symbol**: both `tcp_bbr.c` and `tcp_bbr3.c` define
   `BTF_KFUNCS_START(tcp_bbr_check_kfunc_ids)`. If both are built-in,
   `resolve_btfids` exits 255 silently. Fix — disable old BBR AFTER
   `olddefconfig` (which re-enables it via dependency resolution):
   ```bash
   scripts/config -d TCP_CONG_BBR
   ```
2. **DWARF format mismatch**: Clang 23 with `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`
   produces DWARF that pahole 1.31 can't convert to BTF. Fix:
   ```bash
   scripts/config -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5
   ```
3. **LLVM path vs boolean**: `LLVM` must be `1`, never a directory path
   (a path makes `resolve_btfids` skip compilation). Set `LLVM=1` and prepend
   the LLVM `bin/` to `$PATH`.
4. **Missing pahole**: `sudo pacman -S pahole` (package: `dwarves`).

### 3. Linker failures
- `ld.mold` error → someone changed the linker; force back to `ld.lld`.
  `ld.mold` crashes on kernel vDSO linker scripts — never adopt it.
- `ld.lld: error: undefined symbol` in vDSO → ensure the custom LLVM `bin/` is
  on `$PATH`.

Resolve conflicts yourself — fix hunk offsets, regenerate from source, or drop
the patch. Don't stall waiting on the user; report what you did once it builds.

## Verify bpftune/BTF after a build

Required configs (re-checked after `olddefconfig`, which can silently reset
them): `BPF_SYSCALL`, `DEBUG_INFO_BTF`, `DEBUG_INFO_BTF_MODULES`, `FTRACE`,
`BPF_EVENTS`, `DYNAMIC_FTRACE`, `FUNCTION_TRACER`, `KPROBE_EVENTS`,
`HAVE_KPROBES_ON_FTRACE`.

```bash
scripts/config -g <OPT>          # repeat for each option above
file vmlinux | grep BTF          # confirm BTF is actually present
```

Missing BTF almost always means stale `pahole`, not a config regression.

Full `scripts/config` reference, the version-string logic, and SQM/BBR3
pre-seeding live in `reference.md` in this skill directory — read it before
touching `prepare()`, `scripts/config` calls, or the SQM service.
