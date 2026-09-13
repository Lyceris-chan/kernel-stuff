---
name: kernel-verify
description: >
  Runs the sleepy-kernel verification suite — patch hygiene, checksums, provenance, documented claims, skill-spec compliance, the cumulative apply, plus checkpatch and sparse in the deep tier. Use before committing or releasing, when asked to verify the series or the packaging, or when a change to patches, PKGBUILD, or docs needs checking.
---

> **Package location (2026-09-12).** The repo is single-package: everything this
> skill touches lives in `sleepy-next/`. Unless a step says otherwise, `cd
> sleepy-next` first so paths like `PKGBUILD`, `patches/...`, `config`,
> `net-tune/` and `PATCH_SOURCES.md` resolve. From the repo root, prefix them
> with `sleepy-next/`.

# Verify the series and the packaging

One entry point:

```bash
python3 .claude/skills/kernel-verify/scripts/verify.py            # fast tier
python3 .claude/skills/kernel-verify/scripts/verify.py --tier series
python3 .claude/skills/kernel-verify/scripts/verify.py --tier deep --tree <prepared-tree>
python3 .claude/skills/kernel-verify/scripts/verify.py --tier all --tree <tree>
```

Exit status is `0` when every check passed, `1` when one failed, and `2` when
the environment is unusable (no PKGBUILD, bad `--tree`). `--json` emits the
results for a hook or CI to consume.

## What the tiers cost and cover

| Tier | Cost | Needs | Checks |
|---|---|---|---|
| `fast` | seconds | nothing | `source=()` files exist; no two patches share a number; `b2sums` current; patch headers intact and no `[PATCH n/N]`; every patch number documented in `PATCH_SOURCES.md`; documented patch count and base version match the PKGBUILD; skills satisfy the Agent Skills spec; no dangling symlinks |
| `series` | ~1–2 min | `repos/linux-next` | the whole series applies cumulatively to the base tag |
| `deep` | minutes | a prepared kernel tree | `checkpatch.pl --strict` on the patches we authored; `sparse` (`make C=1`) over the directories the series touches |

**A missing tool is a `SKIP` with the reason, never a silent pass** — that is
the point of the tiering. `--tier all` without `--tree` runs the sparse check as
a skip and says why.

## The wrong tools, and why

Do not reach for `cppcheck` here. It cannot parse kernel headers or the macro
soup in `linux/`, and no kernel developer runs it on the tree — it produces
thousands of false positives and hides real findings. The kernel's own tooling
is strictly better and is what this suite uses:

| Tool | Role | Availability here |
|---|---|---|
| `checkpatch.pl` | style and commit-message conformance | ships in the kernel source; the script extracts it from the source tarball into `/tmp/kverify` |
| `sparse` | the kernel's semantic checker (`make C=1`) | installed; `pacman -S sparse` elsewhere |
| `scan-build` | clang static analyzer | installed |
| `coccinelle` (`spatch`) | semantic patching and its `scripts/coccinelle/` checks | not installed; `pacman -S coccinelle` |
| `smatch` | the kernel's deeper analyzer | a separate build; run it at smatch.kernel.org instead |

## Where each check comes from

Each check exists because this project has actually got it wrong:

- **`b2sums` current** — forgetting `updpkgsums` after a patch edit is the
  single most common cause of a build that refuses to start.
- **Patch numbers documented** — a patch in `source=()` but absent from
  `PATCH_SOURCES.md` is a provenance failure.
- **No duplicate patch numbers** — every other check works on *sets* of numbers,
  so a collision comes out one short and stays invisible; only a check that
  keeps the full list can see it. Two different DCN4 patches both shipped as
  `1140`, which made "patch 1140" ambiguous in the ledger and the changelog.
- **Documented claims** — `docs/README.md` has twice claimed a stale patch count
  and base version while `PKGBUILD` moved on.
- **Dangling symlinks** — dropped patches leave their `NNNN-*.patch` symlink
  behind, which misleads the next audit.
- **Cumulative apply** — neither `git apply --check` nor a single-patch dry-run
  is sufficient; see the `kernel-build` skill.
- **checkpatch on our own patches only** — `0001`–`0049` are the ones we wrote,
  so upstream style applies to them. Backports are reviewed upstream already,
  and running checkpatch over 130 of them buries the signal.

## Deep tier needs a prepared tree

`--tree` must point at a kernel tree that has been configured and built — sparse
compiles through `make`, so it needs the generated headers and `.config`:

```bash
cd sleepy-next && rm -rf src pkg && makepkg -o     # prepare only, keeps src/
python3 .claude/skills/kernel-verify/scripts/verify.py --tier deep --tree sleepy-next/src/linux-7.3-rc2
```

Run `--tier all` before a release; run the `fast` tier before every commit (the
repository's commit hook does this automatically).
