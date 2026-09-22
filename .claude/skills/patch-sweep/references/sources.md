# Sources and access mechanics

Everything the sweep queries, and how to reach each one.

## Contents

- [Source inventory](#source-inventory)
- [Cloning and refreshing](#cloning-and-refreshing)
- [Bare mirrors](#bare-mirrors)
- [lore.kernel.org](#lorekernelorg)
- [Mailing list archives](#mailing-list-archives)
- [drm/amd work items](#drmamd-work-items)
- [Distro and third-party patchsets](#distro-and-third-party-patchsets)
- [Repository health](#repository-health)

## Source inventory

| Source | Where |
|---|---|
| Mainline torvalds | `repos/torvalds` |
| linux-next | `repos/linux-next`, `next-YYYYMMDD` tags |
| drm-next | `repos/drm-next` |
| amd-staging | `repos/agd5f-linux`, `repos/amd-staging-drm-next` |
| drm-misc (TTM/dmemcg/dmabuf) | `repos/drm-misc` |
| linux-pm | `repos/linux-pm` |
| tip | `repos/tip` |
| akpm MM | `repos/akpm-mm`, `mm-everything` / `mm-unstable` / `mm-hotfixes-*` |
| lore mirrors | `repos/lore-<list>` (see below) |
| ML archives | `lists.freedesktop.org` monthly `.txt.gz` |
| drm/amd work items | `gitlab.freedesktop.org` `drm%2Famd` |
| CachyOS | `repos/cachyos-linux`, branches `7.3/base`, `/cachy`, `/fixes`, `/hdmi`, `/xswap` |
| sirlucjan | `repos/sirlucjan-kernel-patches/7.3-rc/` |
| firelzrd | `repos/firelzrd-lru-marie`, `-bore-scheduler`, `-leuo` |
| linux-tkg | `repos/linux-tkg` |

Phoronix is a signal, not a source: it tells you which stone to turn over, then
trace every claim to the actual series.

**Check other branches of akpm's tree, not just the tip.** `mm-unstable` and
`mm-hotfixes-unstable` are regularly fully merged into `master`, so a HEAD-only
diff reads as "nothing new" while `mm-everything` carries dozens of unmerged
commits. The same applies to `agd5f-linux`, which has ~130 branches.

## Cloning and refreshing

`repos/` is user-managed and pruned to save space. **A missing repo is
intentional** — re-clone on demand rather than assuming a broken sweep.

```bash
for r in torvalds linux-next drm-next agd5f-linux amd-staging-drm-next drm-misc \
         linux-pm akpm-mm tip; do
  git -C "repos/$r" fetch --all --prune --quiet &
done
wait
```

- **`--shallow-since` fails** against some repos with
  `fatal: error processing shallow info: 4`. Use `--depth=300` for those.
- **`fetch --all` can exit clean while fetching nothing.** After any fetch,
  verify against the remote:
  ```bash
  git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
      refs/heads/master
  git -C repos/torvalds rev-parse master
  ```
  A two-day stale clone has passed this check's absence before.
- **Shallow clones break ancestry queries.** `git merge-base --is-ancestor`
  returns wrong answers in every repo here. Use
  `git cat-file -e <sha>` to test presence, or range queries, which are
  reliable.
- **`GIT_SHALLOW_FILE=/dev/null` is harmful for range queries.** It suppresses
  grafts whose objects are absent and silently truncates traversal — it turned
  a real 415-commit range into 0. Do not set it.
- **`linux-next`'s `master` ref goes stale** while its tags keep moving. Fetch
  the tag directly: `git -C repos/linux-next fetch origin tag next-YYYYMMDD`.

## Bare mirrors

The lore mirrors are `git clone --mirror` — **bare**, so `repos/lore-x/.git`
does not exist and `[ -d "$r/.git" ]` misreports them as missing. Detect with:

```bash
git -C "repos/$r" rev-parse --git-dir >/dev/null 2>&1
```

Clone with `--mirror`; a plain fetch is enough to refresh. `lore-mirror` (lkml)
and `lore-sched-ext` are small and easy to overlook.

## lore.kernel.org

**Never fetch the web UI** — it is Anubis-gated, a hard block rather than a rate
limit. The **git endpoints are not gated**:

```bash
git clone --mirror https://lore.kernel.org/<list>/<epoch> repos/lore-<name>
```

Epoch `0` is current for most lists. Messages are commits; the raw email is the
blob named `m`.

### Extracting a patch from a mirror

`git show <sha>` diffs the *email*, not the code. Extract the body, and take the
diff from the earliest of `diff --git` **or** `--- a/`:

```python
starts = [m.start() for m in re.finditer(r'^(diff --git |--- a/)', raw, re.M)]
assert starts, "no diff in this mail"
body = raw[min(starts):]
```

Two failure modes, both silent:

1. **Some mailers omit the `diff --git` line.** Anchoring on it alone reports
   "no diff" for patches that plainly contain one.
2. **Cutting at the diff start discards the commit message and every trailer**,
   including the `Signed-off-by` that provenance checking requires. Keep
   everything from the end of the mail headers to the `-- ` signature separator;
   synthesise only `From nobody …` plus `From:`/`Date:`/`Subject:`.

Assert on the extraction: count `Signed-off-by`, `--- a/`, `@@`, and dry-run it.
A patch with correct hunks and no trailer passes `git apply` and fails review.

## Mailing list archives

Only two freedesktop lists matter: **amd-gfx** and **dri-devel**. There is no
separate "drm" or "amdgpu" list. Everything else is reached through lore git
mirrors.

```bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
MONTH=$(date +%Y-%B)
curl -s -A "$UA" "https://lists.freedesktop.org/archives/amd-gfx/${MONTH}.txt.gz" \
     -o /tmp/amd-gfx-${MONTH}.txt.gz
[ -s /tmp/amd-gfx-${MONTH}.txt.gz ] && gunzip -f /tmp/amd-gfx-${MONTH}.txt.gz
```

An empty download or a 403 means the UA was dropped, not that the list is quiet.

For one specific thread, use the thread index — the date/subject/author indexes
are navigation only:

```bash
curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html" \
     -o /tmp/dri-thread.html
rg -o '<LI><A HREF="[0-9]+\.html">[^<]*' /tmp/dri-thread.html \
  | sed -E 's/<LI><A HREF="([0-9]+)\.html">/\1: /'
```

Message ids are bare 6-digit numbers; per-message pages are
`…/${MONTH}/NNNNN.html`.

**Per-message pages are unreliable as raw patches.** Known gotchas:

- **Quoted-printable mboxes** (patchew mirrors): `git am` on a scratch worktree
  decodes them natively; cherry-pick from there.
- **dri-devel pages use U+00A0** for indentation and wrap lines around
  mailing-list links. Normalise before applying:
  `.replace('&nbsp;', ' ').replace('\xa0', ' ')`.
- **Some messages are replies quoting the patch** with broken spacing. Find the
  original `[PATCH]` message through `thread.html` instead.
- **A trailing HTML attachment** may follow the `-- ` diff terminator. Truncate
  at `-- `.
- After extraction, always `git apply --check` and GNU `patch --dry-run`. If a
  hunk is stale against a newer base, port the change deliberately rather than
  forcing fuzz.

**Outlook-mangled diffs.** Mail from Microsoft-hosted addresses arrives with the
leading space stripped from every context line and tabs converted to spaces.
`git apply` says "corrupt patch" and GNU `patch` says "malformed patch". If the
`+`/`-` lines are intact, verify the added content against the base tree, rebuild
the diff body from that ground truth, and confirm content-identical modulo
whitespace before adopting. Record the reconstruction in the ledger with its
Message-ID.

## drm/amd work items

Plain `curl` with **no User-Agent** — a browser UA triggers Anubis.

```bash
# CORRECT way to find what MOVED — filter by update time, not by page:
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?state=opened&updated_after=2026-09-20T00:00:00Z&per_page=100"

# The obvious query — kept only to show why it is wrong:
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?state=opened&per_page=100"
```

`sort=updated_desc&order_by=updated_at` can return a single error object instead
of an array; the unparameterised form above is reliable.

Comments are 401-gated over REST but public over GraphQL:

```bash
curl -s "https://gitlab.freedesktop.org/api/graphql" -H "Content-Type: application/json" \
  --data '{"query":"query { project(fullPath: \"drm/amd\") { issue(iid: \"5868\") { title notes { nodes { createdAt author { username } body } } } } }"}'
```

**Page 1 is not the tracker — it is the newest 100 by CREATION date.** The
project holds **1808** open issues (19 pages), and a plain
`?state=opened&per_page=100` returns only page 1. An issue created months ago
and *updated* yesterday is invisible to it. Measured on 2026-09-22:
`updated_after=2026-09-20` returned **49** issues, of which only **24** were on
page 1 — the other 25 included on-target RX 9070 XT threads (#5718, #5647,
#5511) that a page-1-only sweep had silently missed for several passes.

**Always filter by time, never by page:**

```
?state=opened&updated_after=YYYY-MM-DDT00:00:00Z&per_page=100
```

Check `x-total` against the rows returned; if they differ, you are reading a
page, not the set.

**The GraphQL endpoint caps query complexity at 200.** Asking for
`title description notes { nodes { author { username } body } }` on **15** issues
needs complexity 211 and returns a single error object with **no partial data** —
90 of 100 issues came back empty while the script still reported success. Batch
at **10** with that field set. `notes.nodes.author` is what pushes it over.
Check `d['errors']` and the count of non-null results; never treat an empty
result as "no data".

Enumerating all ~100 issues is worth doing once per sweep rather than trusting a
hand-picked set: it is how `63e19ef3ddab` was found referenced in five separate
issues. Verify each extracted sha with `git cat-file -t` — of 332 hex-looking
tokens across the tracker, 301 were image paths, blob ids and other non-commits.

The tracker is **mostly bug reports**. Most open issues have no referenced fix.
Extract commit shas from comment bodies, but confirm a candidate sha is a commit
(`git cat-file -e`) before citing it — `112d2111f50a…` recurs across issues and
is an image-upload path, not a commit.

Known recurring classes worth grepping each sweep: `SMU`, `lost from bus`,
`black screen`, `IF version`, `Navi 48`, `9070`, `flip_done`, `FRL`, `VRR`.

## Distro and third-party patchsets

- **sirlucjan** — `repos/sirlucjan-kernel-patches/7.3-rc/`, one directory per
  series with `-sep` (separated) and `-all` variants. Version dirs (`-v2`, `-v3`)
  are additive; the newest is the one to read.
- **CachyOS** — `repos/cachyos-linux`, per-branch squashes.
- **linux-tkg, firelzrd, Clear** — check for on-target material only. BORE and
  `-hardened` are not used by this machine (it runs sched-ext), so activity
  there is usually a no-op for us. Say so rather than listing it as a finding.

## Repository health

A corrupt clone answers confidently and wrongly. Before trusting a sweep:

```bash
git -C repos/<r> fsck --no-progress 2>&1 | head
git -C repos/<r> log -1 --format='%ad %h %s' --date=short
git -C repos/<r> log -1 --format='%cd' --date=short    # committer date
```

Nonsense dates (2085, 2077) or a failure to fetch mean the clone is damaged:
re-clone it. Two of these were found in one sweep, and any negative result
recorded against them before that is weaker than it reads.
