# Version sweep: bringing carried patches to their latest revision

A sweep that only looks for *new* patches misses that a **carried** patch has
been superseded. This pass compares every patch in the series against what is
currently posted in the mirrors.

One run over 305 carried patches against 13 mirrors found 46 higher-version
postings, of which 4 were real updates.

## Contents

- [Match on the subject, not the index](#match-on-the-subject-not-the-index)
- [Filter 1: already merged upstream](#filter-1-already-merged-upstream)
- [Filter 2: content-identical](#filter-2-content-identical)
- [Filter 3: written against a different base](#filter-3-written-against-a-different-base)
- [Reporting](#reporting)

## Match on the subject, not the index

A posting is identified by its **normalised subject**, and its revision by the
`vN` in `[PATCH vN …]`.

**Ignore the `n/m` denominator.** A resized series renumbers every part while
the subjects stay the same, so keying on `(subject, n, m)` makes a 15-patch
series and its 20-patch successor look like different work. This blind spot is
exactly why an early pass missed ACPI CPPC v7 — `N/15` becoming `N/20` read as
"no match".

```python
def norm(s):                      # strip [PATCH ...] and punctuation
    return re.sub(r'[^a-z0-9]', '', re.sub(r'\[PATCH[^\]]*\]', '', s).strip().lower())

def ver(s):                       # the vN, defaulting to 1
    m = re.search(r'\[PATCH[^\]]*\bv(\d+)\b', s)
    return int(m.group(1)) if m else 1
```

Build an index of the highest-version posting per normalised subject across
every mirror, then report carried patches whose subject has a strictly higher
version. Skip `Re:` replies — they often carry the same subject with no diff.

**The version comparison ignores dates.** A posting can be both higher-numbered
and *older* than what is carried: `1151` showed a "v4" dated months before the
revision in the tree. Check the date before treating a hit as an update.

## Filter 1: already merged upstream

If the carried patch came from a merged commit, the newer mailing-list revision
is **draft history**, not an update. Test by content hash rather than by subject
— the same patch routinely sits in `torvalds` and `linux-next` under different
hashes and subjects.

```bash
git -C repos/torvalds cat-file -e <sha> 2>/dev/null && echo merged
```

This filter removed 3 of the 46 hits in one sweep.

## Filter 2: content-identical

A higher `vN` is often a **resend** — a rebase with no semantic change, or a
repost for review. Compare the changed lines only, as a set:

```python
def lset(t):
    return sorted(l for l in t.split('\n')
                  if l[:1] in '+-' and not l.startswith(('+++', '---')))

delta = set(lset(newer)) - set(lset(ours))
```

**Do not hash the diff body.** Context lines shift with hunk offsets, so equal
patches produce different hashes and a hash comparison reports "all differ". That
misfired on a 20-patch set that was in fact identical.

If `delta` is empty, the newer revision adds nothing not already present — the
version label moved, the content did not. This removed 23 of 46 in one sweep.

If `delta` is non-empty, the candidate is real and moves to Filter 3.

## Filter 3: written against a different base

A genuine content delta does not make a revision adoptable. Test both directions
against the **series-applied** tree, not a clean base:

```bash
[ -d repos/_audit ] || python3 .claude/skills/kernel-build/scripts/audit_series.py --keep
patch -d repos/_audit -R -p1 --batch --forward -F2 --dry-run < cand.patch
patch -d repos/_audit -p1 --batch --forward -F2 --dry-run < cand.patch
```

| Result | Meaning |
|---|---|
| reverse clean | already carried — no action |
| forward clean | adoptable |
| **neither clean** | written against a different base — keep what is carried |

"Neither clean" is the common outcome for a revision posted against a newer
kernel. The delta is usually an adaptation to a post-base API change, so
adopting it would import references the base does not have. Record it as a
7.x-bump item instead.

Never test against a plain copy of the rc source: with no `.git`, `git -C` walks
up to the enclosing repo and patches the wrong tree.

## Reporting

For each hit, record: the carried number, both versions, the posting date and
list, the changed-line delta, and the filter that decided it. A sweep that
reports "46 updates available" without the filters is worse than no sweep —
the number is not actionable and the real four are buried.

Three of the four filters can only be applied with evidence from the trees and
the series tree. State which filter rejected each candidate.
