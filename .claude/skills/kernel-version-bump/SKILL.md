---
name: kernel-version-bump
description: Bump sleepy-kernel to a new Linux RC or release version, and refresh the squashed CachyOS branch patches. Use when asked to update or bump the kernel version, move to a new -rcN, or regenerate the CachyOS 01xx branch squashes. Also covers editing PKGBUILD's _major/_minor/_srcname and the resulting version string.
---

# Kernel version bump

## 1. Verify the target tag exists

```bash
curl -I -s "https://git.kernel.org/torvalds/t/linux-<X.Y-rcN>.tar.gz"
```

Stop and tell the user if this 404s — don't guess a nearby tag or round to one
that exists.

**Bumping linux-sleepy-next (the linux-next preview, learned 2026-08-26):**
this repo's one package (`linux-sleepy-next`, promoted to the repo root on
2026-09-02) is built from a `next-YYYYMMDD` snapshot. A version bump moves
`_srctag` to the newest snapshot and runs the patch-sweep Step-9 linux-next
sweep; it is not a `linux-7.2`-family RC bump (that era is retired). The
earlier wannabe preview worktree (branch `wannabe-7.3`, doc `WANNABE-7.3.md`)
was removed 2026-09-02 — do not recreate it; its content lives in this series.

**Tarball source URL:** the `cdn.kernel.org/pub/linux/kernel/v7.x/testing/`
URL 404s right after a tag is cut (the cdn mirrors RC tarballs late). Point
`source=()` at `https://git.kernel.org/torvalds/t/linux-<tag>.tar.gz` instead
(seen on the 7.2-rc6 bump).

## 2. Bump PKGBUILD

Update `_major`/`_minor`/`_srcname` to match the verified tag. Don't touch
anything else yet.

## 3. Rebase every patch

Extract the new source, then for each patch in numeric order, test it against
the clean tree (use `git apply --check`, NOT `patch --dry-run` — it reports
false "corrupt patch" errors on mbox-format files):

```bash
git -C repos/linux-7.2-rcN apply --check <patch>.patch     # forward check
git -C repos/linux-7.2-rcN apply --check -R <patch>.patch  # already-applied check
```

- Reverse check passes (forward fails) → already applied upstream → drop it,
  and note why.
- Fails because context shifted → regenerate from the source repo (see the
  `patch-audit` skill for where each number range's source lives).
- CachyOS per-branch patches (01xx) shifted → do NOT hand-rebase; refresh the
  whole branch set in step 4 instead.
- A branch's squash that still applies cleanly (forward check passes) AND whose
  sirlucjan `-sep` content is unchanged can be kept as-is — only the drifted
  branches need regenerating (on 7.2-rc6 only `0105`/`0106` needed it). Verify
  content is unchanged with the sirlucjan repo's HEAD date.

Report every dropped or regenerated patch, with reasons, before moving to
step 4 — never add or remove a patch silently. Write the report and any
PATCH_SOURCES entries in Google doc style — see
`.claude/style-guides/google-docguide/`.

## 4. Refresh CachyOS per-branch patches

Do **NOT** regenerate a monolithic mega-patch — that approach was retired. The
CachyOS set is now sourced as individual per-branch `-sep` files. Run the
`patch-cachy-branches` skill now. It covers: identifying the latest `-sep`
directories (current: `fixes` = v10, `preempt-ipi` = v3, `lru-marie` = v12),
the off-target skip list, numbering, and the two known conflicts (`0151` vs
`0055`, `0053` vs hdmi).

If the `fixes` branch added `0136` (vma_flags_t) alongside `2101` (LRU-MARIE),
apply the one-line in-tree fix to `mm/vmscan.c` per the `patch-cachy-branches`
skill's Step 8 — that is a source edit, not a patch file.

## 5. Finish

```bash
updpkgsums
```

Hand off to the `kernel-build` skill to build and verify. If this bump is part
of the full maintenance cycle (see CLAUDE.md), continue straight to the
`patch-audit` skill instead of stopping here.

## Don't

- Clone with `--depth=1` anywhere in this process — it kills `git log --grep`
  during rebase. Use `--shallow-since=` (see CLAUDE.md YOU MUST #7).
- Drop a patch without saying so, even one that looks obviously superseded —
  that needs explicit user sign-off (see CLAUDE.md YOU MUST NOT #7).
