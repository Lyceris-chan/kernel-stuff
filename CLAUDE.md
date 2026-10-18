# sleepy-kernel

Custom Arch Linux kernels for a single AMD Zen 4 + RDNA 4 desktop, built from a
sanitized CachyOS patchset plus upstream and local patches filtered to this
hardware.

## Two packages

| Directory | Package | Base | Role |
|---|---|---|---|
| `sleepy-rc/` | `linux-sleepy-rc` | `_major`/`_minor`/`_rcver` (mainline RC) | **the boot default**; every workflow targets it unless a step says otherwise |
| `sleepy-next/` | `linux-sleepy-next` | `_srctag` (linux-next snapshot) | preview carrying incoming merge-window content early |

Each sets its own `_pkgsuffix`, so `pkgbase`, the kernel release, the module
directories and the package names never collide — they install side by side.
They share one patch series, copied patch-for-patch into each `patches/` tree,
with preview-only deltas recorded in `sleepy-next/PATCH_SOURCES.md`; the preview
**skips** patches that no longer apply instead of failing the build.

**Never restate a value that lives in a `PKGBUILD` or the ledger — name the file
and the variable, and re-read it.** Versions, patch counts, `_jobs`, config
symbols and branch revisions live in `sleepy-rc/PKGBUILD`,
`sleepy-rc/PATCH_SOURCES.md` and `sleepy-rc/docs/README.md`; every stale
instruction this repo has carried started as a copy of one of those values.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | AMD Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401` (DCN 4.0.1), `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| NIC | Realtek RTL8125B 2.5 GbE | `r8169` (in-kernel driver, since 7.2) |
| NVMe | Phison E16 PCIe 4.0 | `kyber` (CachyOS `60-ioschedulers.rules`) |
| Scheduler | BORE | `CONFIG_SCHED_BORE=y`; sched-ext compiled but unused |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

**If a patch does not target one of these components, it does not go in.**

## Repository layout

| Path | Purpose |
|---|---|
| `sleepy-rc/PKGBUILD` | Arch build script — version vars, `source=()`, `prepare()` applies the series + config overrides |
| `sleepy-rc/config` | Base `.config` (from CachyOS) |
| `sleepy-rc/disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `sleepy-rc/patches/<range>/NNNN-*.patch` | The patch series, one folder per range (see Patch numbering). The PKGBUILD auto-creates gitignored `NNNN-*.patch` symlinks in the package directory for makepkg 7.1.0 basename resolution. |
| `sleepy-rc/net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `sleepy-rc/docs/` | User-facing package docs (`README.md`, `GUIDE.md`) |
| `sleepy-next/` | Preview package — same layout, snapshot base |
| `repos/` | Cloned upstream git repos for patch extraction (gitignored, shallow, user-managed — a missing repo is intentional; never clone into `/tmp`) |
| `*/src/`, `*/pkg/` | Build artifacts — never commit |

## Documentation

`README.md` is the entry point; `sleepy-rc/docs/` holds the package overview and
the end-user guide; `CHANGELOG.md` is per-release. Two are load-bearing:
`sleepy-rc/PATCH_SOURCES.md` is the per-patch provenance ledger (authoritative
for both packages), and **`LESSONS.md` is the incident log and the full durable
findings — read the named section before repeating a past mistake.**

## Skills

Task-specific procedures live in `.claude/skills/`, one workflow per skill —
invoke the matching skill instead of re-deriving the steps. Each skill's own
description already states what it does and when it fires.

## Patch numbering

Each range is a category; use the next unused number in the correct range, and
add a new range when a patch fits no existing category. `0001`–`0049` are the
patches we authored — the own-patch range checkpatch and verify.py run against —
and everything else is a backport. **The authoritative range table lives in the
`patch-audit` skill** — read it there rather than keeping a second copy here:

```bash
rg -n 'xx` *\|' .claude/skills/patch-audit/SKILL.md
```

CachyOS squashes are generated **against the actual series state**, not a clean
rc — the pre-CachyOS patches touch shared files like `drm_edid.c`. sirlucjan
directories live under `repos/sirlucjan-kernel-patches/7.3-rc/`; the
generation-time conflicts square in the `patch-cachy-branches` skill.

## Full maintenance cycle

Run the matching phases in order. A "check for new patches" request is phase 2
alone; a "build it" request is phase 3 alone.

1. **Version bump** — bump `_major`/`_minor`/`_rcver`/`_srctag`; rebase every
   patch; regenerate only the CachyOS squashes that fail. Report every drop and
   regeneration with its reason. → `kernel-version-bump`
2. **Patch audit** — check all six sources plus the drm/amd work-items tracker;
   list candidates with source and priority before adding anything. →
   `patch-sweep`
3. **Build and fix** — `rm -rf src pkg && makepkg -f -s -c`; iterate until it
   succeeds or a MUST NOT rule blocks you. → `kernel-build`

## YOU MUST

1. Compile with `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1` and the PKGBUILD's own kernel.org LLVM toolchain — never change it.
2. `rm -rf src pkg` before every build — old patched files cause false conflicts.
3. `updpkgsums` after any `source=()` change **or any patch-file edit**.
4. Keep every patch's original `From:`/`Date:`/`Subject:`/`Signed-off-by:` intact. Our **own** patches need a named human author (`Sleepy <sleepy@localhost>`), a matching `Signed-off-by:`, an `Assisted-by: Claude <noreply@anthropic.com>` trailer, and no `[PATCH n/N]`.
5. `patch --dry-run -Np1` (and `git apply --check`) before adding any patch.
6. Resolve conflicts yourself — fix offsets, regenerate, or drop the patch; do not stall waiting on the user.
7. Clone with `--shallow-since="YYYY-MM-DD"` — never `--depth=1`.
8. Document every new patch in `PATCH_SOURCES.md` before adding it to `PKGBUILD`.
9. Verify BTF after every build — `CONFIG_TCP_CONG_BBR` and `CONFIG_TCP_CONG_BBR3` define the same BTF kfunc symbol, so the old BBR stays disabled.
10. Use `DEBUG_INFO_DWARF5` (not `DWARF_TOOLCHAIN_DEFAULT`) with Clang 23 and pahole 1.31 — the default emits DWARF pahole 1.31 cannot convert to BTF.

## YOU MUST NOT

1. Never use `ld.mold` — it cannot link the kernel.
2. Never access `lore.kernel.org` with a browser-like client — the web UI is anti-bot gated. Use lore **git mirrors**, `lists.freedesktop.org`, or the **drm/amd work-items tracker** (plain `curl`, **no User-Agent**).
3. Never hand-write or fabricate a patch diff — no traceable commit or mailing-list submission means tell the user, not invent one. AI-assisted patches **are** allowed with a named human author, `Signed-off-by`, an `Assisted-by:` trailer and traceable provenance. Every patch must pass both `git apply --check` and `patch -p1 --dry-run` against the reference tree; one needing heavy fuzz, lacking a source, or referencing invented symbols gets reported, not carried.
4. Never use `pip --break-system-packages`, or `pip install --user` against a managed Python — use a venv, or pacman/AUR.
5. Never add patches for hardware we do not have (Intel/Nvidia, ARM/SoC, Apple T2, laptop amps, TV tuners).
6. Never clone into `/tmp` — use `repos/`.
7. Never run `make menuconfig`/`nconfig` unless explicitly asked.
8. Never remove a patch without explicit user approval.
9. Never use `8.8.8.8` in network scripts — use Quad9 (`9.9.9.9`).
10. Never set `LLVM` to a path — `tools/bpf/resolve_btfids/Makefile` checks `ifeq ($(LLVM),1)`, so a path breaks BTF ID resolution. Prepend the LLVM `bin/` to `$PATH` and set `LLVM=1`.

## Tooling

**Use `rg` (ripgrep), never `grep`** — it is faster, and it respects
`.gitignore`, so it skips `repos/`, `src/` and `pkg/` without exclusions:
`rg -n 'pattern' sleepy-rc/`, `rg -l 'pattern' .claude/skills/`,
`rg -c 'pattern' CLAUDE.md`.

## Critical traps

One line each; the evidence, commands and worked examples are under the named
section of `LESSONS.md`. Read that section before repeating the mistake.

- **DCN 4.0.1, not DCN42B.** `dcn42`/`dcn42b`/`dcn60` run only under `AMDGPU_FAMILY_GC_11_5_0` (Strix APUs): a patch there applies, compiles and does nothing. → *Hardware traps*.
- **GC 12.0 ≠ GC 12.1.** Navi 48 → `gfx_v12_0.c`; check `IP_VERSION`. → *Hardware traps*.
- **Never carry `9051`/`9052`** (DCN4 flip-schedule) — AMD reverted both. → *Hardware traps*.
- **Audit with `audit_series.py`**, the cumulative apply — single-patch dry-runs and `git apply --check` give false negatives, and `Skipping patch`/`Reversed` is an inert no-op, not a success.
- **A patch that applies can still do nothing.** `select`ed symbols, `--set-str` on a removed symbol, MGLRU under LRU-MARIE are inert. **Since 2026-09-30 `fair.c` is the LIVE scheduler (BORE) — `kernel/sched/ext/` is the inert one.** BORE's own `#ifdef` wraps the lines an EEVDF hunk targets, so the hunk lands in the dead `#else` — that is how `0110`'s `fair.c` section ended up dead and was stripped. An inert *hunk* is not an inert *patch*. → *Behaviour that silently does nothing*.
- **A patch that applies can still be a duplicate** — absorption inserts a second copy. Count the identifier: expect `base + 1`. → *A patch that applies cleanly can be installing a duplicate*.
- **Reverse-apply is not authoritative — it fails both ways.** Count the identifier. → *Reverse-apply is not authoritative for older commits*.
- **"Exists in no tree or mirror" ≠ fabricated** — check GitHub's commit search. → *"No tree or mirror has it"*.
- **A newer posting is not a supersession**; a revert is the opposite of one. Read the thread for a maintainer objection. → *A revert is not a supersession*.
- **Every clone in `repos/` is shallow**, so `merge-base --is-ancestor` lies; use `git cat-file -e` plus a content probe. → *Every clone here is shallow*.
- **`… | head && echo OK` always reports OK** — the exit status is `head`'s. → *Exit codes disappear through a pipe*.
- **Before calling a patch new, grep the series** for its subject, author and the function it changes — the fix may sit in a patch whose *subject* says otherwise. → *Dead carries, kind 3*.
- **A tunable can be set, readable, and still not used** — grep the series for the sysctl name. → *A tunable you set can be silently overridden*.
- **A README claim is not evidence, including ours.** → *A README claim is not evidence, even in this repo*.
- **A build is not an install** — the ledger, package mtime and build log describe the artifact; `pacman -Qi` and the installed module decide what runs. → *A successful build is not an installed kernel*.
- **Disabling a detector is a claim about the detector** — prove its *inputs* are misread, not that another metric looks fine. → *CORRECTION: the watchdog was right*.
- **Attribute by measurement, not narrative**, and check whether a "fix" coincides with the symptom worsening. → *"The logs disprove it" beats "the mechanism fits"*.
- **A scan whose input is missing reports success** — assert the tree exists before any dry-run loop. → *A scan whose input is missing reports success*.
- **Build time is ~6 min either way**; serial stages dominate, so `_jobs` is a poor lever — read it from the PKGBUILD. → *The build itself was the bug*.

## Configuration and packaging reference

The `scripts/config` overrides, the net-tune service, and the version-string
mechanics live in `kernel-build/reference.md`, `sleepy-rc/net-tune/README.md`
and `sleepy-rc/docs/GUIDE.md`. Do not duplicate them here.

## Local model routing

`.claude/settings.json` points `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and
`ANTHROPIC_MODEL` at a local LLM server when one is in use. On compaction,
preserve the current patch series (numbers and subjects), its `PATCH_SOURCES.md`
status, and any uncommitted diff. Push heavy one-shot work (cloning, diffing
archives) into subagents, and treat each version bump as its own session.
