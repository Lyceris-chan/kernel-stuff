---
name: kernel-version-bump
description: >
  Bumps sleepy-kernel to a new Linux RC or release and refreshes the CachyOS 01xx squashes that no longer apply. Use when asked to move to a new -rcN or release, or to regenerate the CachyOS branch squashes.
---

> Targets **`sleepy-rc/`** unless a step says otherwise (see `CLAUDE.md` → Two packages).

# Kernel version bump

## 1. Verify the target tag exists

```bash
curl -I -s "https://git.kernel.org/torvalds/t/linux-<X.Y-rcN>.tar.gz"
```

Stop and tell the user if this 404s — don't guess a nearby tag or round to one
that exists.

**This skill targets the mainline-RC package.** `sleepy-rc/` tracks mainline RCs
and is the boot default; `sleepy-next/` is the preview that follows
`next-YYYYMMDD` snapshots. Bumping the RC line never requires touching
`sleepy-next/` — that package moves on its own snapshot cadence (and by default
**skips** patches that no longer apply rather than failing). Never bump to a tag
that does not exist yet.

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
git -C repos/linux-next apply --check <patch>.patch     # forward check
git -C repos/linux-next apply --check -R <patch>.patch  # already-applied check
```

- Reverse check passes (forward fails) → already applied upstream → drop it,
  and note why.
- Fails because context shifted → regenerate from the source repo (see the
  `patch-audit` skill for where each number range's source lives).
- CachyOS `01xx` patches shifted → do NOT hand-rebase; refresh through the
  `patch-cachy-branches` skill instead.
- A squash that still applies cleanly AND whose sirlucjan `-sep` content is
  unchanged can be kept as-is — only the drifted branches need regenerating.
  Verify the content is unchanged against the sirlucjan repo's HEAD date, not
  against a version number remembered from a previous bump.

Report every dropped or regenerated patch, with reasons, before moving to
step 4 — never add or remove a patch silently. Write the report and any
PATCH_SOURCES entries in Google doc style — see
`.claude/style-guides/google-docguide/`.

## 4. Refresh the CachyOS squashes

Do **NOT** regenerate a monolithic mega-patch — that approach was retired. Run
the `patch-cachy-branches` skill: it holds the carried set, the sirlucjan `-sep`
sources, the squash procedure, and the known rebase hazards. Read the branch
versions from the trees there rather than from a value written here.

## 5. Finish

```bash
updpkgsums
```

Hand off to the `kernel-build` skill to build and verify. If this bump is part
of the full maintenance cycle (see CLAUDE.md), continue straight to the
`patch-audit` skill instead of stopping here.

## Don't

- Clone with `--depth=1` anywhere in this process — it kills `git log --grep`
  during rebase. Use `--shallow-since=` (CLAUDE.md YOU MUST 7).
- Drop a patch without saying so, even one that looks obviously superseded —
  that needs explicit user sign-off (CLAUDE.md YOU MUST NOT 8).
