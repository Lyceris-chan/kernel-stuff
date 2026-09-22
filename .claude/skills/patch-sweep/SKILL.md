---
name: patch-sweep
description: >
  Runs the periodic multi-source sweep for new hardware-relevant patches across the upstream kernel trees, mailing lists, distro patchsets, and the drm/amd work-items tracker, then triages and dry-runs the candidates. Use when asked to check for new patches, to sync sources, or to bring carried patches up to their latest revisions.
---

# Multi-source patch sweep

Finds patches worth carrying and brings carried patches up to date. A sweep
produces a **report plus a triage**, not a build; adopting is the follow-up.

Paths are relative to the repo root. Add the `sleepy-next/` prefix for package
files (`PKGBUILD`, `patches/`, `PATCH_SOURCES.md`).

## The three passes

Run all three. Each has caught things the others missed.

1. **New sources** — what landed in the trees, lists, trackers and distro
   patchsets since the last sweep. Steps 1-6 below.
2. **Version sweep** — every *carried* patch checked against its latest posted
   revision. → `references/version-sweep.md`
3. **Branch sweep** — every branch of every repo, not the tips. → Step 2.

Report a source as *unrefreshed* rather than silently skipping it. A stale clone
that answers confidently is worse than a missing one.

## Step 1 — refresh every source

`repos/` is user-managed and pruned; a missing repo is intentional and should be
re-cloned on demand. Full inventory and access mechanics: `references/sources.md`.

Four traps, each of which has produced a wrong "nothing to do" conclusion:

- **`fetch --all` can report success while fetching nothing.** A torvalds clone
  here sat two days stale after a clean-looking fetch. Verify against the remote
  before trusting any scan:
  `git ls-remote <url> refs/heads/master` vs `git -C repos/torvalds rev-parse master`.
- **Lore mirrors are bare** (`git clone --mirror`), so `repos/<r>/.git` does not
  exist and an existence check misreports them as missing. Use
  `git -C repos/<r> rev-parse --git-dir`.
- **`--shallow-since` fails** against some repos with
  `fatal: error processing shallow info: 4`. Use `--depth=N` for those.
- **`linux-next`'s `master` ref is stale** while its `next-YYYYMMDD` tags are
  current. Scan the newest tag, not `master`.
- **Local branches are stale even after a fetch.** `sirlucjan-kernel-patches`
  had local `master` three days behind `origin/master`; the new content was
  invisible until read from the remote ref. **Always scan `origin/<branch>`, and
  check freshness before trusting any result.**
- **Every clone in `repos/` is shallow** (`rev-parse --is-shallow-repository`
  returns true for `linux-next`, `torvalds`, `amd-staging-drm-next`,
  `agd5f-linux`, `drm-next`). So `git merge-base --is-ancestor` is unreliable in
  *all* of them — it reported three 2022–23 commits as absent from rc4. Confirm
  membership with `git cat-file -e` plus a content probe, never with
  `merge-base`.

## Step 2 — scan the trees, every branch

```bash
SINCE="YYYY-MM-DD"   # date of the last sweep

# --all is not optional: a tip-only pass has missed six on-target commits in one
# sweep, two of them wrong-chip traps. See references/triage.md.
KEY='navi48|gfx12|dcn4|dcn401|smu14|smu_v14|psp14|sdma_v7|vcn_v5|amdgpu|amdkfd|
amd_pstate|amd-pstate|cppc|r8169|nvme|phison|zswap|xswap|marie|lru_marie|zstd|
sched_ext|scx|bbr3|bfq|mq-deadline|io_uring|x86/mm|x86/pat|x86/bugs|mce'

for r in torvalds linux-next drm-next agd5f-linux amd-staging-drm-next drm-misc \
         linux-pm akpm-mm tip; do
  git -C "repos/$r" log --all --since="$SINCE" --no-merges \
      --format='%ad %h %s' --date=short -E --grep="$KEY" 2>/dev/null | head -30
done
```

Also check the x86/security line (SRSO, MCE/RAS, KVM) — the GPU pattern misses
it — and each repo's non-`HEAD` refs:

```bash
git -C repos/<r> for-each-ref --sort=-committerdate \
    --format='%(committerdate:short) %(refname:short) %(subject)' refs/remotes | head
```

## Step 3 — mailing lists

Lists without a git mirror are reached through `lists.freedesktop.org` monthly
archives; everything else through its lore git mirror. Mechanics, including the
archive URLs and the mbox parse: `references/sources.md`.

**Extracting a patch from a lore mirror is where this goes wrong.** A mirror
stores each mail as a blob named `m`, and `git show <sha>` diffs the *email*.
Two silent failure modes, both hit in one sweep:

- **Not every mailer emits `diff --git`.** Anchor on the earliest of
  `diff --git` **or** `--- a/`, or four patches report "no diff" while plainly
  containing one.
- **Cutting at the diff start discards the commit message and every trailer** —
  including the `Signed-off-by` that Check 4 requires. Keep the whole body from
  the end of the mail headers to the `-- ` signature separator.

Assert on the result rather than eyeballing hunks: count `Signed-off-by`, count
`--- a/`, count `@@`, and dry-run it.

## Step 4 — drm/amd work items

```bash
# Filter by UPDATE time. The project holds ~1800 open issues and a plain
# per_page=100 fetch returns only page 1 — the newest 100 by CREATION date, so
# an old issue updated yesterday is invisible to it. Measured: updated_after
# returned 49 issues where page 1 held only 24, and the missing 25 included
# on-target RX 9070 XT threads missed for several passes.
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?state=opened&updated_after=YYYY-MM-DDT00:00:00Z&per_page=100"
```

Plain `curl`, **no User-Agent**. Comments are 401-gated over REST but public
over GraphQL; query shape in `references/sources.md`.

The tracker is **mostly bug reports**: most open issues have no referenced fix
yet. Treat each as "track a fix", not "merge". Grep comment bodies for commit
shas, but verify a sha is a commit before citing it — `112d2111f50a…` has been
re-cited across issues and is an image-upload path.

## Step 5 — dry-run the candidates

Two rules, both learned the hard way:

**The reference tree must exist, and "no verdict" must be an error.** A
classifier that branches on `FAILED|ignored` and falls through to "carried"
reports *everything* as carried when the tree is missing — `patch` says
`Can't change to directory …` (matching neither pattern) and **still exits 0**.
Assert the tree exists first:

```bash
[ -d repos/_audit ] || { echo "ABORT: run audit_series.py --keep first"; exit 2; }
```

`audit_series.py` **without** `--keep` consumes the tree it creates.

**Reverse-applicability decides "already carried", not the subject.** A carried
patch does not keep its upstream subject — four candidates were reported absent
in one sweep while all four were carried under shortened names. If `patch -R`
succeeds against the series tree, the change is already in.

```bash
r=$(patch -d repos/_audit -R -p1 --batch --forward -F2 --dry-run < "$cand" 2>&1)
f=$(patch -d repos/_audit -p1 --batch --forward -F2 --dry-run < "$cand" 2>&1)
```

| Reverse | Forward | Verdict |
|---|---|---|
| clean | — | already carried |
| fails | clean | new, adoptable |
| fails | fails | partial — prerequisite missing, or written against a different base |

A forward failure alone cannot distinguish "not carried, context shifted" from
"already carried"; those need opposite responses.

**But reverse-applicability is only authoritative for recent commits.** A patch
older than a few weeks can reverse-fail purely from context drift while its
content is plainly present — `0b0ff65d3ca1` (the stream-validation modeset-hang
fix) reverse-failed on rc4 although every identifier it introduces
(`encoding_order`, `bpc_mask`, `is_hdmi_ep`) was already there. For anything
non-recent, grep the base for **the identifiers the patch introduces** and treat
that as the verdict.

**Before calling a candidate new, grep our own series for its subject and
author.** `1064` was already carried while three separate passes proposed it as
an addition; the giveaway was one `rg` in `sleepy-next/patches/`.

## Step 6 — triage every candidate

All four checks, in order. The trap catalogue — wrong-chip, inert-under-config,
upstream reverts — and the authoritative IP list are in `references/triage.md`.

**Check 0 — reverts and wrong chip.** Grep for `Revert "…"` of anything already
carried. **A revert of carried work is NOT a supersession — it is the opposite,
and it needs a maintainer's blessing before you act.** In one sweep a revert
series was reported as "genuinely superseded"; the maintainer's reply said the
opposite — *"The patches you want to revert actually look correct to me"* — so
adopting it would have swapped working code for a rejected design. Always read
the thread for an objection before concluding. Then confirm the target file
belongs to *this* machine's silicon:
`gfx_v12_0` not `gfx_v12_1`, `dcn401` not `dcn42`/`dcn50`/`dcn60`, `smu_v14_0_0`
not `smu_v14_0_2`, `sdma_v7_0` not `sdma_v7_1`, `vcn_v5_0`. Verify against the
running kernel, not inference:

```bash
sudo dmesg | grep -i 'detected ip block'
```

**Check 1 — hardware relevance.** Target hardware only. Intel/Nvidia, ARM/SoC,
Apple T2, laptop amps, TV tuners, datacenter (MI300 `aqua_vanjaram`/`soc_v1_0`,
CDNA `gfx_v9_4_2`) are rejected before anything else is asked.

**Check 2 — symbol existence.** Every symbol referenced must exist in the base
tree, not just in a staging branch. No symbol → drop.

**Check 3 — applies.** `git apply --check` **and** GNU
`patch -p1 --forward -F2 --dry-run`. git-apply tolerates context GNU patch
rejects. A `Skipping patch` in the dry-run is an inert no-op, not a success.

**Check 4 — provenance.** A named human author and a `Signed-off-by`, with a
traceable commit hash or Message-ID. `Assisted-by:` trailers are allowed. A
fabricated diff is not — report it, do not invent one.

## Step 7 — number and document

Next unused number in the correct range; ranges are in the `patch-audit` skill
table. Document in `sleepy-next/PATCH_SOURCES.md` **before** adding to
`PKGBUILD`, then `updpkgsums`. Never reuse a vacated number — the gap is the
evidence that something was tried.

Record in the ledger: what was adopted, what was rejected, and **why** — the
rejection reasons are the sweep's most reusable output.

## Reporting

State, for each source, whether it was actually queried. Distinguish "no
candidates" from "not checked" from "check failed" — the three are
indistinguishable in a summary that only lists findings.
