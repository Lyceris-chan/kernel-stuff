# sleepy-kernel

Custom Arch Linux kernel for a single AMD Zen 4 + RDNA 4 desktop, built from a
sanitized CachyOS patchset plus upstream and local patches filtered to this
hardware.

One package: `sleepy-next/PKGBUILD` (`linux-sleepy-next`, currently **Linux
7.3-rc3**). Track mainline RCs; linux-next snapshots are a preview base only
when the RC line is unusable.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | AMD Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| NIC | Realtek RTL8125B 2.5 GbE | `r8169` (in-kernel driver, since 7.2) |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline` |
| Scheduler | sched-ext BPF schedulers | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

**If a patch does not target one of these components, it does not go in.**

## Repository layout

| Path | Purpose |
|---|---|
| `sleepy-next/PKGBUILD` | Arch build script — version vars, `source=()`, `prepare()` applies the series + config overrides |
| `sleepy-next/config` | Base `.config` (from CachyOS) |
| `sleepy-next/disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `sleepy-next/patches/<range>/NNNN-*.patch` | The patch series, one folder per range (see Patch numbering). `NNNN-*.patch` symlinks are auto-created inside `sleepy-next/` by the PKGBUILD for makepkg 7.1.0 basename resolution, and are gitignored. |
| `sleepy-next/net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `sleepy-next/docs/` | User-facing package docs |
| `repos/` | Cloned upstream git repos for patch extraction (gitignored; never clone into `/tmp`) |
| `sleepy-next/src/`, `sleepy-next/pkg/` | Build artifacts — never commit |

## Documentation

`README.md` is the entry point; `sleepy-next/docs/` holds the package overview
and the end-user guide; `CHANGELOG.md` is per-release. Two are load-bearing:
`sleepy-next/PATCH_SOURCES.md` is the per-patch provenance ledger, and
**`LESSONS.md` is the incident log and the full durable findings — read it
before repeating a past mistake.**

## Skills

Task-specific procedures live in `.claude/skills/`, one workflow per skill.
Invoke the matching skill instead of re-deriving the steps; this file records
only the durable rules that apply across them. Each skill's own description
already states what it does and when it fires, so it is not repeated here.

## Patch numbering

Each range is a category; use the next unused number in the correct range, and
add a new range when a patch fits no existing category. **The authoritative
range table lives in the `patch-audit` skill** — read it there rather than
keeping a second copy here:

```bash
rg -n 'xx` *\|' .claude/skills/patch-audit/SKILL.md
```

CachyOS squashes are generated **against the actual series state**, not a clean
rc — the pre-CachyOS patches touch shared files like `drm_edid.c`. Two known
conflicts are handled inside the squashes: `0151` duplicates `0055`, and `0053`
must be dropped when the hdmi branch is present. sirlucjan directories live
under `repos/sirlucjan-kernel-patches/7.3-rc/`.

## Full maintenance cycle

Run the matching phases in order. A "check for new patches" request is phase 2
alone; a "build it" request is phase 3 alone.

1. **Version bump** — bump `_major`/`_minor`/`_rcver`/`_srcname`; rebase every
   patch; regenerate only the CachyOS squashes that fail. Report every drop and
   regeneration with its reason. → `kernel-version-bump`
2. **Patch audit** — check all six sources plus the drm/amd work-items tracker;
   list candidates with source and priority before adding anything. →
   `patch-sweep`
3. **Build and fix** — `rm -rf src pkg && makepkg -f -s -c`; iterate until it
   succeeds or a MUST NOT rule blocks you. → `kernel-build`

## YOU MUST

1. Compile with `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. The PKGBUILD downloads a
   pre-built LLVM toolchain from kernel.org. Never change the toolchain.
2. `rm -rf src pkg` before every build. Old patched files cause false conflicts.
3. `updpkgsums` after any `source=()` change **or any patch-file edit**.
4. Keep every patch's original `From:`/`Date:`/`Subject:`/`Signed-off-by:`
   intact. For our **own** patches use a named human author
   (`Sleepy <sleepy@localhost>`), a matching `Signed-off-by:`, an
   `Assisted-by: Claude <noreply@anthropic.com>` trailer, and no leftover
   `[PATCH n/N]` series numbering.
5. `patch --dry-run -Np1` (and `git apply --check`) before adding any patch.
6. Resolve conflicts yourself — fix offsets, regenerate from source, or drop the
   patch. Do not stall waiting on the user.
7. Clone with `--shallow-since="YYYY-MM-DD"` — never `--depth=1`.
8. Document every new patch in `PATCH_SOURCES.md` before adding it to
   `PKGBUILD`.
9. Verify BTF after every build. `CONFIG_TCP_CONG_BBR` (old) and
   `CONFIG_TCP_CONG_BBR3` define the same BTF kfunc symbol, so only one can be
   built-in — the old BBR must stay disabled.
10. Use `DEBUG_INFO_DWARF5` (not `DWARF_TOOLCHAIN_DEFAULT`) with Clang 23 and
    pahole 1.31 — the default produces DWARF pahole 1.31 cannot convert to BTF.

## YOU MUST NOT

1. Never use `ld.mold` — it cannot link the kernel.
2. Never access `lore.kernel.org` with a browser-like client; the web UI is
   anti-bot gated. Use lore **git mirrors**, `lists.freedesktop.org` archives,
   or the **drm/amd work-items tracker** (plain `curl` with **no User-Agent**).
3. Never hand-write or fabricate a patch diff. No traceable commit or
   mailing-list submission → tell the user, do not invent one. AI-assisted
   patches **are** allowed with a named human author, `Signed-off-by`, an
   `Assisted-by:` trailer, and traceable provenance. Every patch must pass both
   `git apply --check` and `patch -p1 --dry-run` against the reference tree; one
   that needs heavy fuzz, lacks a traceable source, or references symbols I
   invented must be reported, not silently carried.
4. Never use `pip --break-system-packages`, or `pip install --user` against a
   managed Python. Use a venv, or pacman/AUR.
5. Never add patches for hardware we do not have (Intel/Nvidia, ARM/SoC,
   Apple T2, laptop amps, TV tuners).
6. Never clone into `/tmp` — use `repos/`.
7. Never run `make menuconfig`/`nconfig` unless explicitly asked.
8. Never remove a patch without explicit user approval.
9. Never use `8.8.8.8` in network scripts — use Quad9 (`9.9.9.9`).
10. Never set `LLVM` to a path. `tools/bpf/resolve_btfids/Makefile` checks
    `ifeq ($(LLVM),1)`, so a path value breaks BTF ID resolution. Prepend the
    LLVM `bin/` to `$PATH` and set `LLVM=1`.

## Tooling

**IMPORTANT — use `rg` (ripgrep), never `grep`.** ripgrep is installed and is
faster, respects `.gitignore` (so it skips `repos/`, `src/` and `pkg/` without
exclusions), and handles the recursive searches this repo needs:

```bash
rg -n 'pattern' sleepy-next/          # recursive, with line numbers
rg -l 'pattern' .claude/skills/       # filenames only
rg -c 'pattern' CLAUDE.md             # match count per file
```

## Critical traps

Evidence, exact commands, and the source-access mechanics are in `LESSONS.md`.
The short version:

- **GC 12.0 ≠ GC 12.1.** Navi 48 is GC IP **(12,0,1)** → `gfx_v12_0.c`.
  `gfx_v12_1.c` is a different chip. Check `IP_VERSION` before any gfx12 patch.
- **Never carry `9051`/`9052`** (DCN4 flip-schedule) — AMD reverted both
  upstream.
- **Audit with a cumulative apply** — run
  `python3 .claude/skills/kernel-build/scripts/audit_series.py`. It applies the
  whole series to a throwaway worktree at the base tag and flags
  `FAILED` **and** `Skipping patch`/`Reversed` (a skipped patch is an inert
  no-op, not a success). Single-patch dry-runs and `git apply --check` give
  false negatives. Exit 0 = clean, 1 = failures, 2 = environment problem.
- **A patch that applies can still do nothing.** `select`ed config symbols,
  `--set-str` on a symbol that no longer exists, MGLRU under LRU-MARIE, and
  `fair.c` under scx full-switch mode are all inert. Confirm the subsystem is
  actually owned by the code you are patching.
- **Verify clones are fresh before trusting a sweep**, and **never `git
  format-patch` a lore mirror** (it diffs email headers, not code). Each has
  produced a confidently wrong "nothing to do" conclusion.
- **Build time is ~8 min** — prefer rebuilding over guessing.

## Configuration and packaging reference

The `scripts/config` overrides, the net-tune service, and the version-string
mechanics are documented in `kernel-build/reference.md`,
`sleepy-next/net-tune/README.md`, and `sleepy-next/docs/GUIDE.md`. Do not
duplicate them here.

## Local model routing

`.claude/settings.json` points `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and
`ANTHROPIC_MODEL` at a local LLM server when one is in use. On compaction,
preserve the current patch series (numbers and subjects), its
`PATCH_SOURCES.md` status, and any uncommitted diff. Push heavy one-shot work
(cloning repos, diffing archives) into subagents, and treat each version bump as
its own session.
