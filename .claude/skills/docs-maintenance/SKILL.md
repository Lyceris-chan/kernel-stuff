---
name: docs-maintenance
description: >
  Update sleepy-kernel documentation and commit the result after a maintenance
  session. Keep the README "Target audience" and "What this kernel adds"
  sections accurate, record provenance for every patch change in
  PATCH_SOURCES.md, write commit-message bodies as Why/How, and commit with a
  clean git state. Use when asked to update README.md / PATCH_SOURCES.md /
  GUIDE.md, write a commit message, or commit a maintenance result.
---

# Docs maintenance & commit

Run this AFTER the patch work (version bump, sweep, or audit) is done and the
build is verified — not before.

## Google developer style — apply to every doc edit

Consult the local Google documentation style guides before editing:
`.claude/style-guides/google-docguide/` (index in
`.claude/style-guides/README.md`). They are committed reference copies (CC-By
3.0, attribution in the index). Read `style.md` (Markdown formatting),
`best_practices.md`, and
`philosophy.md`, and apply them to every README/GUIDE/PATCH_SOURCES edit and
every commit message. Quick rules that always apply:

- **Second person**: "You can build with ..." — never "One can build".
- **Active voice**: "Run `makepkg`" — never "makepkg should be run".
- **Imperative for instructions**: "Run:", "Add:", "Verify:".
- Short sentences; shell commands in fenced blocks, copied exactly.

## 1. Keep README.md sections accurate

The per-patch manifest lives **only** in `PATCH_SOURCES.md` — never duplicate
per-patch rows into README.md or GUIDE.md. Keep the remaining README sections
in sync:

- **"Target audience"** — one machine: Ryzen 7 7700 (Zen 4), RX 9070 XT
  (Navi 48 / RDNA 4), RTL8125B NIC; not a general-purpose distro kernel.
- **"What this kernel adds"** — subsections "Over vanilla Linux 7.2-rcN" and
  "Over stock CachyOS", listing every category the series now carries.

On any patch add/remove/renumber, update `PATCH_SOURCES.md` (mandatory). Touch
README.md / GUIDE.md only when a category range changes (their compact "Patch
series" range tables) or the PROFILE_PEAK behavior section changes.

## 2. Record provenance in PATCH_SOURCES.md

Every changed patch gets a ledger entry BEFORE committing: file name, author,
subject, source URL or commit hash; note revisions (e.g. `0004` ... **v4**
(2026-08-02): ...). Sweep results: list "already in rc5", "duplicate of
existing", and "deferred" candidates.

## 3. Commit message format

- Subject: `type(scope): imperative summary`, under ~72 chars.
- Body: **Why** first (the problem, hardware impact), then **How** (concrete
  change and files touched).

Example:

```
refactor(pm): split PROFILE_PEAK changes into 0003 and 0004

Why: one patch mixing the GFXCLK ceiling float with the deep-sleep toggle was
hard to review and broke the COMPUTE profile path.

How: 0003 floats the GFXCLK ceiling; 0004 guards deep-sleep control to never
touch COMPUTE mode. Updated PKGBUILD/GUIDE.md/README.md/PATCH_SOURCES.md.
```

## 4. Commit the maintenance result

```bash
cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export
# Fresh repo only — DESTRUCTIVE, erases history; only when the user asks:
#   rm -rf .git && git init
#   git config user.name "Sleepy"
#   git config user.email "<email>"
git add -A
git status          # review: only expected .patch renames, docs, PKGBUILD edits
git commit -m "<subject>

<Why/How body>"
```

Never run `rm -rf .git` on a repo whose history must be preserved — ask first.
