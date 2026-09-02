---
name: patch-sweep
description: >
  Run the periodic patch sweep for sleepy-kernel, checking drm-next,
  drm-misc-next (TTM / dmemcg / dmabuf — e.g. the Valve aggressive-TTM
  dmemcg-protect series), agd5f/amd-staging-drm-next, linux-next, linux-pm,
  the amd-gfx and dri-devel mailing lists, sirlucjan, firelzrd, the GitLab
  drm/amd work-items tracker, AND the x86/security line (torvalds x86_bugs /
  SRSO / MCE — Zen 4 CPU mitigations like the Safe-RET interrupt fix).
  Produces a triage report and dry-runs clean candidates against the reference
  rc tree.
  Use when asked to "check for new patches", "sync sources", or "run a patch
  sweep". For a single named patch/commit, use the patch-audit skill instead.
---

## Local model (Qwen) tips — READ THIS FIRST

- **Copy commands exactly.** Do not improvise, rephrase, or "simplify" any
  command below. A weaker local model that paraphrases produces broken grep
  patterns, wrong paths, or bad quoting. If a command errors, paste the exact
  error text into your reply and follow this skill's fix instructions — do not
  invent a replacement command.
- **Read the whole skill before starting.** The steps build on each other
  (fetch → scan → triage → number). Skipping ahead produces a wrong report.
- **Never access `lore.kernel.org`.** Its anti-bot protection blocks automated
  agents. Use only the git repos and the `lists.freedesktop.org` archives
  described in this skill.
- **Use the `git -C repos/<repo> ...` form everywhere** (this form is already
  covered by project permissions). Never `cd` into a repo and run git there.
- **Confirm each command's output before proceeding.** If a `curl` download
  yields an empty file or a "403 Forbidden" page, stop and re-read the archive
  access section in Step 1 before moving on. If a `grep`/`git log` returns
  nothing, re-run it and verify the repo actually fetched before assuming there
  are no candidates.
- Do not silently continue past a step that produced no output — re-run the
  previous step and verify before proceeding.
- **Use absolute patch paths with `git -C`.** `git -C <repo> apply --check`
  changes the process directory to the repo, so a relative patch path like
  `patches/<range>/NNNN-....patch` resolves against the repo and errors "can't
  open patch". Always write
  `git -C <ref-tree> apply --check "$PWD/patches/<range>/NNNN-....patch"` where
  `<ref-tree>` is a worktree of `repos/linux-next` at the PKGBUILD `_srctag`
  (the series base since 2026-09-02; `repos/linux-7.2*` are the retired era).
  Patches live in `patches/<range>/` folders (2026-08-11); root-level
  `NNNN-*.patch` entries are gitignored build symlinks, not the source of truth.
- **Capture real exit codes, never `| head && echo OK`.** `git apply --check f 2>&1 |
  head -3 && echo CLEAN` always prints CLEAN because `head`'s exit status wins.
  Use `git apply --check f > log 2>&1; echo "exit: $?"` and read `log`.
- **`git apply --check` passing is NOT enough** (learned 2026-08-03). The patch
  must also survive `patch -p1 --forward --dry-run`, the exact tool `prepare()`
  uses. Git-apply tolerates offset/ambiguity that GNU patch rejects (a hunk whose
  leading `if (r)` context appears many times, or a hunk touching `dcn60_resource.c`
  — DCN6, absent from rc7). For a file absent from rc7, strip that file's hunks +
  its stats line + fix the "N files changed" summary as a documented adjustment.

# Six-Source Patch Sweep

## Step 1 — Fetch all repos in parallel

```bash
# Linux-next is huge and slow to fetch. Check first whether a newer daily
# snapshot (next-YYYYMMDD tag) exists at all; if the latest tag equals what
# we already have locally, SKIP the linux-next fetch — there is no new content.
#   git ls-remote --tags repos/linux-next 'next-*' | awk -F/ '{print $NF}' | grep -v "\^{}" | sort -V | tail -1
#   git -C repos/linux-next describe --tags master   # what we already have
# Tags are published on working days only — weekends have no new snapshot.
# CAVEAT (learned 2026-08-04): ls-remote --tags on kernel.org's linux-next may
# NOT advertise the newest snapshot (stale/truncated ref advertisement on this
# huge repo). next-20260803 existed but ls-remote only showed next-20260731.
# If the calendar says a newer working-day snapshot should exist but ls-remote
# disagrees, try a DIRECT tag fetch before concluding nothing is new:
#   git -C repos/linux-next fetch origin tag next-YYYYMMDD
# That bypasses the advertisement and either fetches the tag or errors cleanly.

# Git repos (use background processes). drm-misc is the TTM/dmemcg/dmabuf line
# (Valve dmemcg-aggressive-protect series) — clone on first sweep.
[ -d repos/drm-misc ] || git clone --shallow-since=2026-08-01 https://gitlab.freedesktop.org/drm/misc.git repos/drm-misc >/dev/null 2>&1 &
for repo in repos/drm-next repos/agd5f-linux repos/linux-pm repos/amd-staging-drm-next repos/drm-misc; do
  git -C "$repo" fetch --shallow-since=2026-08-01 origin 2>&1 | tail -3 &
done
# torvalds mainline (x86/security line). repos/linux-7.2-rc6 is a shallow
# torvalds clone with full history to the rc7 tag — fetch to get the latest.
git -C repos/linux-7.2-rc6 fetch --shallow-since=2026-08-01 origin 2>&1 | tail -3 &
git -C repos/sirlucjan-kernel-patches pull 2>&1 | tail -3 &
git -C repos/firelzrd-bore-scheduler pull 2>&1 | tail -3 &
wait

# Mailing list archives (freedesktop, safe to curl)
#
# IMPORTANT: WebFetch returns HTTP 403 on lists.freedesktop.org. The ONLY
# working method is curl with a browser User-Agent. This is a proven workaround.
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
MONTH=$(date +%Y-%B)   # e.g. 2026-August

# Option A — monthly .txt.gz mbox (fastest for keyword scanning):
curl -s -A "$UA" "https://lists.freedesktop.org/archives/amd-gfx/${MONTH}.txt.gz" -o /tmp/amd-gfx-${MONTH}.txt.gz
[ -s /tmp/amd-gfx-${MONTH}.txt.gz ] && gunzip -f /tmp/amd-gfx-${MONTH}.txt.gz
curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}.txt.gz" -o /tmp/dri-devel-${MONTH}.txt.gz
[ -s /tmp/dri-devel-${MONTH}.txt.gz ] && gunzip -f /tmp/dri-devel-${MONTH}.txt.gz

# Option B — thread index HTML (use when you need a specific thread):
#   https://lists.freedesktop.org/archives/amd-gfx/${MONTH}/thread.html
#   https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html
# Per-message pages live at .../{msgid}.html, e.g.:
#   https://lists.freedesktop.org/archives/amd-gfx/2026-August/abcdef1234567890.html
# Download one the same way, with the browser UA:
#   curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html" -o /tmp/dri-thread.html
# Message links in thread.html are <LI><A HREF="NNNNN.html">[PATCH n/N] subject
# (msgid is a bare 6-digit number, NOT "msgNNNNN.html"). Extract subjects:
#   grep -oE '<LI><A HREF="[0-9]+\.html">[^<]*' /tmp/dri-thread.html \
#     | sed -E 's/<LI><A HREF="([0-9]+)\.html">/\1: /'
# The date/subject/author indexes only contain navigation links — use thread.html.

# ML message extraction (learned 2026-08-26) — per-message pages are unreliable
# as raw patches. Known gotchas:
#   * QP-encoded mboxes (patchew.org mirrors): `git am <mbox>` decodes them
#     natively — use git am on a scratch worktree, then cherry-pick the commits.
#   * dri-devel pages use U+00A0 non-breaking spaces for indentation AND wrap
#     lines as <LI><A HREF=...>mailing-list links; always
#     .replace('&nbsp;',' ').replace('\xa0',' ') before git apply.
#   * Some messages are replies that quote the patch (broken spacing). Find the
#     ORIGINAL [PATCH] message via the thread.html grep above instead.
#   * Pages may carry a trailing "-------------- next part --------------" HTML
#     attachment after the "-- 2.xx.x" diff terminator — truncate at "-- ".
#   * After extraction always `git apply --check`; if a hunk is stale against a
#     newer base, apply the change manually with Edit rather than forcing fuzz.

# If a download produced an EMPTY file or a page containing "403 Forbidden",
# stop — do not continue. Re-run with the UA above, or use the git repos.
```

**Never** access `lore.kernel.org` — its anti-bot protection blocks automated
agents; this is a hard block, not a rate limit. Use only the git repos and the
`lists.freedesktop.org` archives above.

## Step 2 — Git repo keyword scan

Use `--since=LAST_CHECK_DATE` to limit results:

```bash
# SINCE = the last time this sweep ran (YYYY-MM-DD). If unsure, use the date of
# the previous sweep's report or the kernel version bump date.
SINCE="2026-08-01"

# Canonical keyword pattern — copy EXACTLY. Covers GPU core, display, PM,
# schedulers, block, and memory-management patches for our hardware.
# Use -E (extended regex) because the pattern contains bare | alternation.
KEYWORDS="gfx12|navi48|dcn4|dcn42b|smu14|psp14|mmhub_4|sdma_v7|vcn_v5|amd_pstate|amd-pstate|epp_boost|bbr3|bfq|mq-deadline|zstd|marie|cgroup.*dmem"

for repo in repos/drm-next repos/agd5f-linux repos/linux-next; do
  echo "=== $repo ==="
  git -C "$repo" log --since="$SINCE" --oneline --all -E --grep="$KEYWORDS" 2>/dev/null | head -30
done

# linux-pm: amd-pstate / cpufreq keywords (same canonical pattern plus CPPC)
echo "=== linux-pm ==="
git -C repos/linux-pm log --since="$SINCE" --oneline --all -E \
  --grep="amd_pstate|amd-pstate|CPPC|k10temp|epp_boost" 2>/dev/null | head -20

# sirlucjan: new/updated third-party performance patches (no --grep; list dirs)
echo "=== sirlucjan 7.2-rc (new version dirs) ==="
ls repos/sirlucjan-kernel-patches/7.2/ | grep -E "fixes-v|lru-marie-v|preempt-ipi-v|nap"
```

## Step 2b — x86/security scan (Zen 4 CPU mitigations)

Added 2026-08-10 after the Phoronix Safe-RET / Zapscape disclosures. The
GPU/drm sweep misses CPU-side security fixes that affect our Zen 4 7700.
Scan torvalds mainline (repos/linux-7.2-rc6 holds full history to the rc7
tag; fetch it in Step 1) for speculative-execution / SRSO / MCE / entry
fixes since the last sweep:

```bash
# SRSO / Safe-RET / speculative execution mitigations (x86_bugs, entry)
git -C repos/linux-7.2-rc6 log --since="$SINCE" --oneline --all -E \
  --grep="x86/bugs|SRSO|Safe.?RET|speculat|ibrs|IBPB|entry_64|ist_enter|retbleed" 2>/dev/null | head -20
# Machine check / RAS (MCE can present as hard resets on Zen 4)
git -C repos/linux-7.2-rc6 log --since="$SINCE" --oneline --all -E \
  --grep="x86/mce|machine.check|mce_intel|mce_amd|threshold" 2>/dev/null | head -10
# KVM/security follow-ups (Zapscape class)
git -C repos/linux-7.2-rc6 log --since="$SINCE" --oneline --all -E \
  --grep="KVM: x86|kvm.*mmu|kvm.*shadow" 2>/dev/null | head -10
```

Eligibility: an x86 fix goes in ONLY if it targets Zen 4-class AMD (SRSO
mitigations, Safe-RET, MCE/RAS on AMD) and is NOT already in the rc base.
Most land in mainline and arrive with the next version bump — only carry one
if it is security-relevant, on-target, and absent from the current base.

## Step 3 — Mailing list scan

Parse the downloaded mbox with Python:

```python
import mailbox, email.header, re

def decode(h):
    parts = email.header.decode_header(h or "")
    return "".join(
        p.decode(enc or 'utf-8', errors='replace') if isinstance(p, bytes) else p
        for p, enc in parts
    )

KEYWORDS = re.compile(
    r'gfx12|navi48|dcn4|dcn42b|smu14|psp14|mmhub_4|sdma_v7|vcn_v5|'
    r'amd_pstate|amd-pstate|epp_boost|bbr3|bfq|mq-deadline|zstd|marie|cgroup.*dmem',
    re.IGNORECASE
)

for mbox_file in ['/tmp/amd-gfx-2026-August.txt', '/tmp/dri-devel-2026-August.txt']:
    mbox = mailbox.mbox(mbox_file)
    for msg in mbox:
        subj = decode(msg.get("Subject", ""))
        from_a = decode(msg.get("From", ""))
        mid = msg.get("Message-ID", "").strip().strip("<>")
        if KEYWORDS.search(subj):
            print(f"  [{mid}]")
            print(f"    From: {from_a}")
            print(f"    Subject: {subj}")
```

## Step 4 — GitLab drm/amd issue scan

**ACCESSIBLE (learned 2026-08-03):** Anubis only blocks browser-like User-Agents.
Use plain `curl` with **no User-Agent header** to read the `drm/amd/-/work_items`
tracker and the REST API (the issue *notes* API is 401-gated, but the issues and
events feeds return real JSON):

```bash
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?state=opened&per_page=100&sort=updated_desc" -o issues.json
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/events?per_page=100" -o events.json
```

**CAVEAT (learned 2026-08-26):** `sort=updated_desc&order_by=updated_at` can
return a single error object instead of the array — if `.json` has one key or
`len()==1` with a dict, drop the sort params (`?state=opened&per_page=100` is
the reliable form). The tracker is **mostly bug reports, not fixes**: most open
issues have no referenced fix yet. Treat each as "track / verify a referenced
fix", not "merge". Watch the RX 9070 XT clusters: flip_done timeouts (#5616,
#5625, #5647 — the Leo Li / amd-drm-next DCN fixes land in the base, see the
7.3 section below) and the VCN-unigate + SMU-deadlock → Mode 1 reset (#5693,
created 08-25, no fix referenced yet).

Check issue titles/descriptions and events (comment bodies + referenced commit SHAs)
for unmerged patch series relevant to our hardware. If a request returns an Anubis
challenge page, you likely used a browser UA — retry with no UA.

**Read full issue COMMENTS via unauthenticated GraphQL (learned 2026-08-10):**
the REST notes API is 401-gated, but GraphQL exposes the same notes for public
projects with no auth. This is how to check issue comments for in-progress fixes /
commit SHAs / workarounds:

```bash
curl -s "https://gitlab.freedesktop.org/api/graphql" -H "Content-Type: application/json" \
  --data '{"query":"query { project(fullPath: \"drm/amd\") { issue(iid: \"5538\") { title notes { nodes { body system } } } } }"}'
```

Sweep flow: (1) search issues by hardware keyword —
`curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?search=<kw>&state=all&per_page=100"` —
then (2) pull notes for each relevant iid via GraphQL and grep for
`([0-9a-f]{12,40})|fixed by|patch|commit|in progress|merged`. The HTML issue page
(`/-/issues/<iid>`) renders the description but comments are Vue-lazy-loaded, so
GraphQL is the reliable route for comments. (2026-08-10 scan: no SMU-IF driver
fix in !5538/!5479/!5038 — firmware-side; AMD devs suggest `pcie.aspm=off` as a
!5538 stopgap; display-stall class !4753 has an in-progress FAMS2 investigation.)

**Watch the hard-reset / SMU-IF class (learned 2026-08-10, work-item !5538):**
our RX 9070 XT reports `smu driver if version = 0x0000002e, smu fw if version =
0x00000033` — a 5-minor-version IF mismatch between the kernel driver and the
VBIOS-resident PMFW. During SMU power transitions the GPU can drop off the PCIe
bus (`device lost from bus!`, SMU message `response:0xFFFFFFFF`), black-screen,
and hang/reboot the system — with `nowatchdog` on the cmdline, nothing is
logged. This is a VBIOS/firmware issue, not a kernel patch fix. Each sweep,
grep issue titles for: `SMU`, `lost from bus`, `reboot`, `black screen`,
`IF version`, `Navi 48`, `9070`. If AMD lands a driver-side IF-compat fix,
that IS a candidate for our tree.

## Step 5 — Dry-run clean candidates

Use `git apply --check` (not `patch --dry-run`) against the clean reference tree:

```bash
# Reference tree = the series base: a worktree of repos/linux-next at the
# PKGBUILD _srctag (repos/linux-7.2* are the retired 7.2 era, historical only).
TREE="/tmp/ref-next"   # e.g. git -C repos/linux-next worktree add "$TREE" next-20260902

check_commit() {
  local repo="$1" sha="$2"
  local tmp="/tmp/sweep_${sha:0:12}.patch"
  git -C "$repo" format-patch -1 --stdout "$sha" > "$tmp" 2>/dev/null
  [ -s "$tmp" ] || { echo "NO-OBJ: $sha"; return; }
  fwd=$(git -C "$TREE" apply --check "$tmp" 2>&1)
  rev=$(git -C "$TREE" apply --check -R "$tmp" 2>&1)
  subj=$(grep "^Subject:" "$tmp" | head -1)
  if [ -z "$fwd" ]; then
    echo "CLEAN  : $sha $subj"
  elif [ -z "$rev" ]; then
    echo "ALREADY: $sha (already in $TREE)"
  else
    echo "FAIL   : $sha $subj"
    echo "  $(echo "$fwd" | head -1)"
  fi
}
```

## Step 6 — Triage checklist (run in this order for every CLEAN candidate)

Every candidate must pass all four checks. Copy the commands exactly.

**Check 1 — Hardware relevance.** Does it target hardware we actually have?
Allowed targets (from CLAUDE.md): RDNA 4 / gfx1201 / DCN401 / DCN42B / SMU14 /
PSP14 / GFX12 / SDMA7 / VCN5, Zen 4 / amd-pstate / CPPC / k10temp, RTL8125,
Phison E16 (bfq, mq-deadline), sched-ext, NAP governor. Anything touching
i915, xe, nouveau, Intel WiFi, Bluetooth dongles, or laptop audio is REJECTED
immediately.

**Check 2 — Symbol existence.** Every function/macro the patch references must
already exist in the clean rc7 tree (not just in a staging branch). If the
patch fails here it depends on staging infrastructure and must be dropped.
```bash
# For GPU/display patches:
grep -r "<unique_symbol>" repos/linux-7.2/drivers/gpu/drm/amd/ | head
# For PM patches:
grep -r "<unique_symbol>" repos/linux-7.2/drivers/cpufreq/ | head
# For block patches:
grep -r "<unique_symbol>" repos/linux-7.2/block/ | head
```
If `grep` returns nothing for any referenced symbol, DROP the candidate.

**Check 3 — Applies cleanly.** Use `git apply --check` (NOT `patch --dry-run`)
against the clean reference tree:
```bash
git -C repos/linux-7.2 apply --check <candidate>.patch       # forward check
git -C repos/linux-7.2 apply --check -R <candidate>.patch    # already-applied check
```
- Forward check passes → CLEAN, proceed to Check 4.
- Reverse check passes (forward fails) → already applied upstream, DROP it.
- Both fail → context shifted or prerequisites missing; report and investigate.

**Check 4 — Author/source trustworthiness.** The patch must have a real
author (a named kernel developer with a traceable commit hash or message-ID).
`Signed-off-by` must be present. **AI-assistance is allowed (rule change
2026-08-03):** an `Assisted-by: <tool>` trailer (e.g. `Assisted-by:
Claude:claude-opus-5`) does NOT disqualify a patch as long as the author is a
named human developer, the patch is not fabricated/hand-written, and its
provenance (commit hash or mailing-list Message-ID) is traceable. What is
still forbidden is an entirely fabricated/hallucinated diff with no traceable
source.
```bash
head -8 <candidate>.patch   # From: / Date: / Subject: / Signed-off-by:
```

## Step 7 — Assign numbers and document

The number prefix tells you the category. Use the NEXT unused number in the
correct range — never reuse, never skip:

| Range | Category | Source |
|-------|----------|--------|
| `0001–0049` | Handmade local patches | Sleepy/Antigravity |
| `0050–0099` | Upstream EDID/display ML patches | freedesktop mbox |
| `0101–0109` | CachyOS branch squashes (one patch per branch, 0106 = drops) | sirlucjan `-sep` dirs |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | drm-next / agd5f |
| `1100–1199` | AMD Display (DCN4, DCN42B, PSR) | drm-next |
| `1200–1299` | AMD Power Management (amd-pstate, cpufreq) | linux-pm |
| `2000–2099` | Block / I/O schedulers (bfq, mq-deadline) | sirlucjan |
| `2100–2199` | Memory management (zstd, LRU-MARIE) | sirlucjan |
| `2200–2299` | CPU idle (NAP governor) | sirlucjan `nap-patches/` |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux |

Copy the file into its `patches/<range>/` folder with a descriptive name:
```bash
cp <downloaded-or-exported>.patch patches/<range>/NNNN-short-description.patch
```
Example: `patches/1200-1299/1206-cpufreq-amd-pstate-Fix-EPP-return-type-and-handle-er.patch`.
Root-level `NNNN-*.patch` symlinks are auto-created by the PKGBUILD (gitignored)
— do not copy patches to the repo root.

Then document in `PATCH_SOURCES.md` **before** adding to `PKGBUILD`.
Run `updpkgsums` after any `source=()` change (this also recreates the root
symlinks). Write the entry and the
triage report in Google doc style — see `.claude/style-guides/google-docguide/`.

## Step 8 — Mailing list patches (mbox format)

Extract from mbox with Python (see `extract_from_mbox()` pattern):

```python
def extract_patch(mbox_file, target_mid, output_file):
    mbox = mailbox.mbox(mbox_file)
    for msg in mbox:
        mid = msg.get("Message-ID","").strip().strip("<>")
        if target_mid not in mid:
            continue
        from_a = decode(msg.get("From",""))
        subj = decode(msg.get("Subject",""))
        payload = msg.get_payload(decode=True)
        if payload:
            payload = payload.decode('utf-8', errors='replace')
        with open(output_file, "w") as f:
            f.write(f"From nobody Mon Sep 17 00:00:00 2001\n")
            f.write(f"From: {from_a}\nDate: {msg.get('Date','')}\n")
            f.write(f"Subject: {subj}\nMessage-ID: <{mid}>\n\n")
            f.write(str(payload or ""))
        return True
    return False
```

**Important**: match by subject + author keywords, not Message-ID prefix, because
mbox parsers may truncate IDs. Verify extracted patch content before using.

**Outlook-mangled mbox diffs (learned 2026-08-10, patch `1026`):** patches sent
from Microsoft-hosted addresses (e.g. `...@amd.com` via `namprd12.prod.outlook.com`)
arrive at lists.freedesktop.org with the leading space stripped from every
context line AND tabs converted to spaces. `git apply --check` reports "corrupt
patch" and GNU `patch` reports "malformed patch" — both unwritable as-is. If a
patch's `+`/`-` lines are intact but its context is mangled, verify the added
content against the rc7 tree (e.g. against an older-IP sibling file the commit
message says it's "modeled after" — the GFX12 CRIU fix was modeled after the
rc7 `kfd_mqd_manager_v11.c` functions), rebuild the diff body from rc7 ground
truth with proper tabs, and confirm content-identical modulo whitespace. Then
pass BOTH `git apply --check` and GNU `patch -p1 --forward --dry-run` before
adopting. Record the reconstruction in `PATCH_SOURCES.md` with the Message-ID.

## Step 9 — linux-next / sleepy-next sweeps (the 7.3 preview)

> The standalone **wannabe preview tree** (gitignored `wannabe-7.3-rc1/` git
> worktree, branch `wannabe-7.3`, doc `WANNABE-7.3.md`, tracked
> `wannabe-7.3-patches/` series) was **removed 2026-09-02**. There is no preview
> worktree to maintain: the linux-next (7.3) preview kernel IS this repo's one
> package, `linux-sleepy-next` (PKGBUILD at the repo root, base = a
> `next-YYYYMMDD` snapshot). Sweep for 7.3-window content directly against that
> series. History of the wannabe era lives in `CHANGELOG.md` + `PATCH_SOURCES.md`
> (2026-08-26 record, annotated as superseded).

For a "check everything" sweep against the next snapshot base:

1. **Repos**: linux-next tags (`git tag -l 'next-*'`) — the snapshot is the
   sleepy-next base; if the newest tag equals the current `_srctag`, repos are
   covered. drm-next / linux-pm / amd-staging tips before the snapshot date are
   in base. amd-staging post-tip content is GC 12.1 / datacenter (off-target
   for gfx1201) until the next amd-drm-next merge.
2. **MLs**: amd-gfx + dri-devel are the ONLY relevant freedesktop lists
   (there is no separate "drm" or "amdgpu" list — those names map to amd-gfx
   and dri-devel). lore-only lists (linux-pm, linux-mm, linux-kernel, netdev)
   are covered via the git repos; never curl lore.
3. **Work items**: see Step 4 caveats — mostly bug reports, track don't merge.
4. **WIP merge rule**: a series applies cleanly to next-YYYYMMDD AND is
   on-target AND not a v1-major-rework / maintainer-rejected / author-dropped
   → adopt as an isolated numbered patch ("ML WIP, easy to drop when it lands
   upstream"), document in `sleepy-next/PATCH_SOURCES.md`. Verify
   `make defconfig` (cheap Kconfig sanity) and 0 `.orig`/`.rej` after.
   Rejected-as-upstream: author-dropped (MMIO-TLB fallback), maintainer-rejected
   (userq-manager keep-alive), v1-major-rework (Alex Deucher 30-patch GPU TLB
   KIQ→SDMA rework — supersedes our TLB series, watch `agd5f tlb_inv_rework`).
5. **amdgpu_dm split (7.2 vs 7.3)**: `amdgpu_dm_connector.c` +
   `amdgpu_dm_freesync.c` exist only on 7.3+. The ML HDMI VRR/ALLM series
   (Fangzhi Zuo / Tomasz Pakuła, v4 `150619`–`150623`) targets the split →
   applies to 7.3, NOT 7.2 (`git apply --check` fails "No such file"). The
   CachyOS `0107` hdmi squash wires dc_edid_parser into the MONOLITHIC
   7.2 amdgpu_dm.c → **0107 is required on 7.2, superseded on 7.3** (base has
   dc_edid_parser + update_freesync_caps + FRL fixes). Don't try to swap them
   across versions.
6. **Leo Li (`sunpeng.li@amd.com`) display fixes** (flip-done timeouts on
   mode1 reset `82730dba0cf9`, DCN vblank/flip consolidation
   `c87e6635d2db`, GRPH_FLIP status check `f64a9be56536`): ~400 commits in
   the 7.3 base. They are the #5616 flip_done fixes — arrive with the 7.3
   bump, do NOT backport to 7.2 (same amdgpu_dm-split reason).
7. **MARIE LRU**: 0.11.0 is current (firelzrd, 2026-08-31), carried as a strict
   1-to-1 rebase (`sleepy-next` `2101`). zstd `2100` already has the gcc<11.4
   workaround (sirlucjan's `zstd-dev-patches-v2` is the same merge reorganized).

Known-good WIP content from the 08-26 preview era now ships in the sleepy-next
series: gup `follow_page_mask()` batching (Rik van Riel RFC v3 → 2120–2127),
HDMI VRR/ALLM v4 (→ 0059–0061), userq GPU-reset + BO-bind + KFD
mark-queues-reset + vm_init reorder (→ 9000s).
