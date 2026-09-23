---
name: kernel-build
description: >
  Builds sleepy-kernel with makepkg and verifies the result — BTF, net-tune, and the built-in cmdline. Use when asked to build the kernel, when a build fails on a patch or hunk, or to verify BTF/vmlinux after a build.
---

> Repo is single-package: everything here lives in `sleepy-next/`. Unless a step
> says otherwise, `cd sleepy-next` first. From the repo root, prefix paths with
> `sleepy-next/`.

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

**Full build runs at the PKGBUILD's `_jobs=8`** (tunable at the top of the
PKGBUILD; `-j$(nproc)` was 16 and froze the desktop by over-committing RAM).
(`2300`–`2322`, `pkgrel 3`+). Rebuilds are cheap — prefer rebuilding over
guessing. Run it in the background and watch for `Finished making` / `ERROR:`.

Compile flags are fixed: `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. Never
substitute these (see `reference.md` for why `ld.mold` specifically breaks).

## How patches apply (important)

ALL patches — including the `90xx` series (`9001`–`9003`, `9006`–`9024`;
`9000`/`9004`/`9005` merged upstream into rc6 and were dropped; the 14-patch
retry-fault v3 series lives at `9011`–`9024`) — apply through the normal `patch
-Np1 --forward` loop in `prepare()` (PKGBUILD lines ~533–542). There is **no**
special `git apply` case for `90xx` patches. If you see a `90xx` patch fail,
diagnose it exactly like any other patch — do not invent a `git apply` bypass.

**Patch layout (2026-08-11):** patches live in `patches/<range>/NNNN-*.patch`
folders. makepkg 7.1.0 cannot resolve subdirectory local sources (it strips the
directory prefix), so the PKGBUILD body auto-creates **root-level symlinks**
`NNNN-*.patch -> patches/<range>/NNNN-*.patch` when it is sourced, before source
resolution. These symlinks are gitignored (`/*.patch`). If a build reports a
patch source "not found in the build directory", re-run `updpkgsums` (or source
the PKGBUILD) — the symlinks may be missing after a fresh clone. Never commit
root-level `*.patch` files; they are always symlinks.

The only special-case reverse-apply in `prepare()` is for `1101`
(`drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch`), which is
reverse-applied with `patch -Np1 --forward -R` to keep `.pstate_enabled =
false`.

## Audit the full series before building

Run the bundled script rather than rebuilding the loop by hand — it is the
authoritative check, and it is faster than a failed build:

```bash
python3 .claude/skills/kernel-build/scripts/audit_series.py
```

It reads `source=()`, creates a throwaway worktree at the base tag derived from
`_srctag`, applies all patches in order, and removes the worktree afterwards.
Exit status: `0` clean, `1` one or more patches failed or were skipped, `2` an
environment problem (with a message saying which). Flags: `--tag`, `--keep`,
`--quiet`.

**A plain run consumes the worktree it creates.** Only `--keep` leaves
`repos/_audit` behind for later use, so any command that patches into
`repos/_audit` after a normal run is testing a directory that no longer exists.
That is worse than it sounds: `patch -d repos/_audit …` prints
`Can't change to directory …` and **exits 0**, so a classifier branching on
`FAILED|ignored` matches nothing and falls through to its default verdict —
which, if that default is "already carried", reports the entire candidate list
as duplicates. Assert the tree exists before using it, and treat "no verdict"
as an error rather than a result.

It exists because neither of the obvious shortcuts is sufficient —
`git apply --check` gives false negatives, and `patch --forward` returns
success when it *skips* a patch that is already applied, which is an inert
no-op rather than a pass.

## On failure, in this order (triage checklist)

### 1. Patch application failures
- Read the `.rej` file first:
  ```bash
  find src -name "*.rej" | head
  cat <path/to/file.c.rej>
  ```
- "Already applied" by an earlier patch or a CachyOS branch → remove the
  conflicting patch, note it in `PATCH_SOURCES.md` (Google doc style — see
  `.claude/style-guides/google-docguide/`).
- Context lines shifted → regenerate from the source repo (see `patch-audit`).
- Test a patch independently against the clean tree:
  ```bash
  git -C repos/linux-next apply --check "$PWD/<patch>"     # forward (use ABSOLUTE path — git -C changes CWD)
  git -C repos/linux-next apply --check -R "$PWD/<patch>"  # already-applied?
  patch -p1 --forward --dry-run < <patch>                     # THE authoritative check — matches prepare()'s tool
  ```
  **Lesson (2026-08-03):** `git apply --check` can PASS where GNU `patch -p1
  --forward` (the tool `prepare()` actually runs) REJECTS the same patch — for example, a hunk whose leading `if (r)` context is ambiguous, or a patch touching a file
  absent from rc7 (like DCN6 `dcn60_resource.c`). Always confirm with `patch -p1
  --forward --dry-run` against the series tree. If a patch passes `git apply`
  but `patch` still rejects it, DROP it and document why (9025 did this) rather
  than hand-forcing the hunk. For `git apply --check`, capture the real exit
  code (`git apply ... > log 2>&1; echo $?`) — never `| head && echo OK`.

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
file vmlinux | rg BTF          # confirm BTF is actually present
```

Missing BTF almost always means stale `pahole`, not a config regression.

Full `scripts/config` reference, the version-string logic, and SQM/BBR3
pre-seeding live in `reference.md` in this skill directory — read it before
touching `prepare()`, `scripts/config` calls, or the SQM service.
