# sleepy-kernel

Custom Arch Linux kernel for a single AMD Zen 4 + RDNA 4 desktop, built from a
sanitized CachyOS patchset plus upstream and local patches filtered to this
hardware.

One package: `sleepy-next/PKGBUILD` (`linux-sleepy-next`). Track mainline RCs —
`_major`/`_minor`/`_rcver` in the PKGBUILD are the authoritative version, so
read them rather than trusting a copy here. linux-next snapshots are a preview
base only when the RC line is unusable.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | AMD Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401` (DCN 4.0.1), `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| NIC | Realtek RTL8125B 2.5 GbE | `r8169` (in-kernel driver, since 7.2) |
| NVMe | Phison E16 PCIe 4.0 | `kyber` (CachyOS `60-ioschedulers.rules`) |
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

- **DCN 4.0.1, not DCN42B.** This GPU is GC IP (12,0,1) → `AMDGPU_FAMILY_GC_12_0_0` → `dcn401_clk_mgr_construct`/`dcn401_create_resource_pool`, and the kernel prints "Display Core ... on DCN 4.0.1". `DCN42B` (and `dcn42`/`dcn42b`/`dcn60` files generally) is instantiated only under
  `AMDGPU_FAMILY_GC_11_5_0` + `DCN_VERSION_4_2B` — Strix-class APUs. A patch touching those files applies and compiles, and does nothing here.
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
  `--set-str` on a symbol that no longer exists, MGLRU under LRU-MARIE (the
  `2131`-`2137` batch, carried for weeks and removed 2026-09-23), and `fair.c`
  under scx full-switch mode are all inert. Confirm the subsystem is actually
  owned by the code you are patching — `lru_gen_enabled()` returns false while
  `lru_marie_enabled()` is true, so the whole MGLRU path is dead here.
  **Note the difference between inert and removable:** `0110`'s `fair.c` hunk
  (base slice 0.4 ms instead of 0.7 ms) is inert because `switch_all=1` puts
  everything on scx, but `0110` also carries live `mm/vmscan.c`,
  `mm/page_alloc.c` and `bus_lock.c` changes — so it stays. An inert *hunk* is
  not an inert *patch*.
- **A patch that applies can still be a duplicate.** When upstream absorbs a
  patch we carry, the cumulative audit still reports `ok`: the hunk's context
  anchor survives, so instead of failing it inserts a **second copy**. `9007`
  made `gfx_v12_0.c` program `DB_RING_CONTROL` twice this way. After a rebase,
  grep the series tree for the register or symbol each patch is named after and
  confirm it appears the expected number of times.
- **Reverse-apply is not authoritative for older commits.** A patch can
  reverse-fail on context drift while its content is plainly present
  (`0b0ff65d3ca1`). Grep for the *identifiers the patch introduces* instead.
- **"Exists in no tree or mirror" ≠ fabricated.** Real patches live in personal
  repos (`kerneltoast/kernel_x86_laptop` held `1158`'s sha). Check GitHub's
  commit search before calling a sha invented.
- **A newer posting is not a supersession.** A *revert* of a carried patch is
  the opposite of superseding it — check for a maintainer objection before
  concluding anything. König defended `1065`/`1066` against exactly such a
  series.
- **Every clone in `repos/` is shallow**, so `git merge-base --is-ancestor`
  lies. Use `git cat-file -e` and content probes. Also **never `git
  format-patch` a lore mirror** (it diffs email headers, not code).
- **`… | head && echo OK` always reports OK** — the exit status is `head`'s.
  It printed "APPLIES CLEANLY" over a `corrupt patch`. Capture exit codes
  directly, never through a pipe.
- **Before proposing a patch as new, grep the series for its subject, its
  author, and the function it changes — then read every hit.** `1064` was
  already carried while three passes called it a candidate. And the fix itself
  can already be carried inside a patch whose *subject* says something else:
  `1227` ("retain immutable autonomous selection") already takes the lock
  before reading `mode_state_machine[][]`, which **is** the amd-pstate TOCTOU
  fix a later candidate proposed. The name grep returned both `1227` and
  `1231`; only the subject match was read, and `1227` was set aside as
  unrelated. A clean standalone dry-run at a large offset, in a subsystem we
  patch heavily, means one of our own patches is in there.
- **A tunable can be set, readable, and still not used.** A patch we carry may
  override it in-kernel. `vm.swappiness = 180` was configured here and had
  never taken effect: LRU-MARIE clamps the effective value to 1
  (`low_swappiness_mode`, default on) *"regardless of the higher values
  vm.swappiness ... have installed"*. `/proc/sys/vm/swappiness` still read 180.
  It is now set to 1, so it agrees with the clamped value. Grep the series for
  the sysctl name before trusting any tuning value — a readable sysctl is not
  evidence that it is consulted.
- **A README claim is not evidence, including ours.** `swap-stack/README.md`
  justified the swap design with "zram never returns that memory when the
  workload shrinks"; zsmalloc has a shrinker and frees a zspage as soon as it
  empties. That claim was load-bearing and false. Verify against source.
- **Disabling a detector is a claim about the detector.** Prove it by showing
  its *inputs* are misread — not by showing that a metric you chose yourself
  looks fine. MARIE's thrash watchdog was switched off as a "false positive" on
  the strength of `MemAvailable: 28.8 GB`, which the watchdog never reads. It
  was right: the machine *was* thrashing, driven by a swappiness change of
  mine, and muting the alarm hid the cause. Re-arm it and measure its own
  inputs instead.
- **A change that makes things worse can be mistaken for the fix.** Clearing
  MARIE's swappiness clamp was credited with fixing the OOM kills while
  actually *creating* the livelock the watchdog was reporting. Both changes
  landed in one window, so credit went to the one that was written down. When
  two changes ship together, attribute by measurement rather than narrative —
  and check whether the "fix" coincides with the symptom getting worse.
- **Build time is ~8 min at `-j16`, longer at the PKGBUILD's capped
  `_jobs=8`** — prefer rebuilding over guessing. The cap exists because 16
  parallel clang jobs peaked at 20-25 GB and froze the desktop; do not raise it
  without checking free RAM with the desktop running.

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
