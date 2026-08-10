---
name: patch-cleanup
description: >
  Clean up the sleepy-kernel workspace after a maintenance session: cross-check
  patch files on disk against the PKGBUILD source=() array, delete dropped or
  deferred patch files only after confirming they are unreferenced, and remove
  scratch scripts and build artifacts. Use when asked to clean up, remove
  leftover/orphaned patch files, delete scratch or build artifacts, or reconcile
  the patch tree with the PKGBUILD.
---

# Patch Cleanup (post-maintenance-session workspace hygiene)

Run this at the END of a maintenance session (version bump, patch audit, or
patch sweep). It removes orphaned patch files and build artifacts so the
workspace matches `PKGBUILD` exactly. This is the workflow used in the session
that renamed old `0013–0015`/`ai0x` patches into the numbered scheme and dropped
deferred patches.

## Rules (read first)

- **Never delete a patch that IS in `PKGBUILD`'s `source=()`.** Only files that
  are NOT referenced there may be removed. Deleting an active patch breaks the
  build.
- **Never remove a patch from `source=()` yourself** — dropping a patch from the
  build requires explicit user approval (see CLAUDE.md YOU MUST NOT #7). This
  skill only deletes files whose removal decision was already made.
- Work from the repository root:
  ```bash
  cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export
  ```
- Confirm every command's output before running the next step.

## Step 1 — Build the two lists

Extract every patch filename that `PKGBUILD` references, and list every `.patch`
file on disk. (Files must be `sort`-ed for the diff below.)

```bash
# 1a. Patch paths referenced by PKGBUILD source=() (patches/<range>/<file>)
grep -oE 'patches/[0-9]+-[0-9]+/[^"]+\.patch' PKGBUILD | sort -u > /tmp/pkgsrc.txt

# 1b. Patch files physically present under patches/
find patches -name '*.patch' 2>/dev/null | sort -u > /tmp/ondisk.txt

# 1c. Show both for review
echo "=== in PKGBUILD source=() ==="; cat /tmp/pkgsrc.txt
echo "=== on disk ==="; cat /tmp/ondisk.txt
```

If `1a` printed nothing, the regex did not match — inspect the actual `source=()`
format first (patch entries look like `patches/<range>/NNNN-...patch`; the array
spans ~lines 227–419 of PKGBUILD) before continuing.

## Step 2 — Find orphaned patches (on disk, NOT in source=())

```bash
echo "=== ON DISK but NOT in PKGBUILD (candidates for deletion) ==="
comm -23 /tmp/ondisk.txt /tmp/pkgsrc.txt
```

For each candidate, CONFIRM it is truly unreferenced before deleting. Check the
PKGBUILD (must be 0 hits) and the PATCH_SOURCES.md ledger (a patch listed there
as "dropped"/"deferred" is safe to remove the file; an active entry means
investigate):

```bash
grep -c "<candidate>" PKGBUILD               # full patches/<range>/<file> path — must print 0
grep -n "<candidate-file>" PATCH_SOURCES.md  # read the context line (ledger uses the bare filename)
```

Examples of candidates that legitimately appear here: files using an old naming
scheme (`0013-...`, `0014-...`, `0015-...`), a deferred/never-applied upstream
patch, or a patch you regenerated under a new number leaving the old copy behind.

## Step 3 — Delete orphaned patches (only the confirmed ones)

```bash
# One file at a time — never a wildcard that could hit an active patch:
rm <candidate1> <candidate2>    # each candidate is a patches/<range>/<file> path
```

After deleting, regenerate both lists and confirm no active patch was removed:

```bash
find patches -name '*.patch' 2>/dev/null | sort -u > /tmp/ondisk2.txt
echo "=== still orphaned (should now be empty) ==="
comm -23 /tmp/ondisk2.txt /tmp/pkgsrc.txt
```

If a file you deleted still shows in `comm -13` output (see Step 5) it means it
was actually referenced — restore it immediately from git: `git checkout -- <candidate>`.

## Step 4 — Remove scratch scripts and build artifacts

```bash
# Build directories / extracted source
rm -rf src pkg tmp_build usr

# Build outputs
rm -f *.log *.pkg.tar.zst *.tar.gz

# Patch-reject / backup leftovers from apply conflicts
find . -maxdepth 1 -type f \( -name "*.rej" -o -name "*.orig" \) -delete

# One-off helper scripts created during the session (list them first!)
ls *_helper.sh extract_*.py sweep_notes.sh 2>/dev/null
rm -f <scratch-script>   # only files you confirmed are scratch, not repo tooling
```

Never delete `disable_configs.py`, `PKGBUILD`, `config`, the `net-tune/`,
`sqm-qos/` (legacy), or `repos/` directories. Only build artifacts and your own
scratch files go.

## Step 5 — Final verification (both directions)

```bash
find patches -name '*.patch' 2>/dev/null | sort -u > /tmp/ondisk2.txt

echo "=== patches on disk MISSING from PKGBUILD (must be EMPTY) ==="
comm -23 /tmp/ondisk2.txt /tmp/pkgsrc.txt

echo "=== patches in PKGBUILD MISSING on disk (must be EMPTY) ==="
comm -13 /tmp/ondisk2.txt /tmp/pkgsrc.txt
```

Both directions must be empty. If either prints a file:
- "on disk missing from PKGBUILD" → you have an orphan left; repeat Steps 2–3.
- "in PKGBUILD missing on disk" → you deleted an active patch; restore with
  `git checkout -- <candidate>` (the full `patches/<range>/<file>` path).

## Step 6 — Wrap up

```bash
# If and only if source=() itself changed during the session:
updpkgsums

git status   # review the final diff; every deletion should be a *.patch / artifact
```

`git status` is the last word: every `D` (deleted) entry must be either an
orphaned patch you confirmed in Step 2 or a build artifact. If any deletion
looks wrong, restore it with `git checkout -- <file>` and re-run Step 5.
