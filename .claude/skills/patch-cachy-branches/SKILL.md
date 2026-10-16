---
name: patch-cachy-branches
description: >
  Refreshes the carried CachyOS squashes (the 01xx range) when a kernel bump breaks one — re-squashing the bbr3, kbuild and cpu-isa branches from sirlucjan's separated patch directories. Use when a CachyOS squash conflicts during a version bump or sirlucjan ships a newer branch version.
---

> Targets **`sleepy-rc/`** unless a step says otherwise (see `CLAUDE.md` → Two packages).

# CachyOS squash refresh

**The carried set is whatever `sleepy-rc/patches/0101-0113/` holds — read the
directory and the ledger, not a list in this file.** Two kinds of patch live
there:

| Kind | Branches | Source | Refresh method |
|---|---|---|---|
| Branch squashes | `bbr3`, `kbuild`, `cpu-isa` | sirlucjan `-sep` directories | re-squash (below) |
| Curated single patches | `CONFIG_CACHY` config hooks, ACPI bus-master check for AMD | the CachyOS/linux fork | re-apply or regenerate by hand — no sirlucjan source exists |

`0104` (sched/core: keep `finish_task_switch()` inline) is a single patch
extracted from sirlucjan's `cachyos-fixes-patches-*` branch, not a squash —
refresh it by re-extracting that one commit from a newer fixes version.

Branches this skill used to carry and no longer does — the `fixes` drops pair,
`hdmi`, `preempt-ipi`, `vesa-dsc-bpp`, `cgroup-vram`, the removed `0112` — and
the machinery that went with them (off-target revert tables, the `0151`/`0055`
and `0053` conflicts, the `vma_flags_t` compile fix) are archived with dates in
[`references/old-patterns.md`](references/old-patterns.md). Read that before
re-adopting any of them.

## Source

`repos/sirlucjan-kernel-patches/<line>/`, one directory per series, with `-sep`
(separated) and `-all` variants. For versioned branches pick the highest version
(`ls -d <dir>-v* | sort -V | tail -1`); for the rest the single `-sep` directory
is canonical.

The clone in `repos/` is shallow and user-managed — a missing or behind
directory is not evidence the branch was withdrawn; re-clone or `git fetch`
before concluding anything.

NAP has no refresh source: it is absent from sirlucjan's `7.3-rc/` line and from
`repos/firelzrd-bore-scheduler` (that repo is BORE-only, no `nap-patches/`). Our
`2200` carry is unaffected; only its recorded source path is historical.

## Squash procedure

Generate the squash against the **actual series state** — the base plus every
patch that precedes it — never against a clean rc: the pre-CachyOS patches touch
shared files such as `drm_edid.c`, and a clean-rc diff silently reverts them.

Do **not** copy each `-sep` file in individually. In a work tree at the correct
series state:

```bash
BASE="repos/sirlucjan-kernel-patches/<line>"
for f in "$BASE"/<branch>-patches*-sep/00*.patch; do
  patch -p1 --forward < "$f" || echo "FAILED: $f"   # apply in order
done
find . -name '*.orig' -delete    # patch leaves .orig/.rej backups — never commit them
find . -name '*.rej' -delete
git diff --binary > /path/to/01NN-cachy-<branch>.patch
```

Build the baseline with `patch -p1 --forward` rather than strict `git apply`:
overlapping local patches like `0003`/`0004` fail strict sequential `git apply`
but apply cleanly under `patch` fuzz — which is what `prepare()` uses.

**Purge `.orig`/`.rej` after every phase and before any `git add`/`git diff`**
— a `.orig` staged into the index lands in the squash as a huge bogus deletion
(one `0105` regeneration ballooned 51 KB → 628 KB this way).

If a branch no longer applies at all, the choice is regenerate, drop, or carry
the individual patch — report the decision with its reason. Removing a patch
needs explicit user approval (`CLAUDE.md` YOU MUST NOT 8).

## After regenerating any `01xx` squash

A changed `01xx` sits mid-series and can shift context for every later patch.
Run the authoritative full-series check — `prepare()` applies everything in
`source=()` order:

```bash
rm -rf src && makepkg -o
```

If it fails, hand off to the `kernel-build` skill for `.rej` triage. Then
`updpkgsums`, and record the change in `PATCH_SOURCES.md` **before** committing.

## Known rebase hazards

- **`0101` (bbr3):** upstream `cb145191e9d3` replaces `min_tso_segs()` with a
  `tso_segs()` CC callback, and our squash performs that same rename itself — so
  `0101` needs regeneration at a bump that takes that commit.
- **`0110` applies only with fuzz:** its `bus_lock.c` hunk carries
  `CONFIG_PROC_SYSCTL` context. `git apply --check` rejects what the build's
  `patch -p1 --forward -F2` accepts — judge it with the cumulative
  `audit_series.py`, never a single-patch dry run.

## Provenance

Squashed `01xx` patches carry one generated header, not the individual upstream
`From:` lines — per-hunk provenance is tracked in `PATCH_SOURCES.md`, which is
the authority for every squash in this range. Write ledger entries in Google doc
style — see `.claude/style-guides/google-docguide/`.
