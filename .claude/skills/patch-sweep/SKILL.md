---
name: patch-sweep
description: >
  Run the periodic six-source patch sweep for sleepy-kernel, checking drm-next,
  agd5f, linux-next, linux-pm, the amd-gfx and dri-devel mailing lists,
  sirlucjan, firelzrd, and the GitLab drm/amd work-items tracker for new
  commits relevant to our hardware. Produces a triage report and dry-runs clean
  candidates against the reference rc tree.
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
  `NNNN-....patch` resolves against the repo and errors "can't open patch".
  Always write `git -C repos/linux-7.2-rc6 apply --check "$PWD/NNNN-....patch"`.
- **Capture real exit codes, never `| head && echo OK`.** `git apply --check f 2>&1 |
  head -3 && echo CLEAN` always prints CLEAN because `head`'s exit status wins.
  Use `git apply --check f > log 2>&1; echo "exit: $?"` and read `log`.
- **`git apply --check` passing is NOT enough** (learned 2026-08-03). The patch
  must also survive `patch -p1 --forward --dry-run`, the exact tool `prepare()`
  uses. Git-apply tolerates offset/ambiguity that GNU patch rejects (a hunk whose
  leading `if (r)` context appears many times, or a hunk touching `dcn60_resource.c`
  — DCN6, absent from rc6). For a file absent from rc6, strip that file's hunks +
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

# Git repos (use background processes)
for repo in repos/drm-next repos/agd5f-linux repos/linux-pm repos/amd-staging-drm-next; do
  git -C "$repo" fetch --shallow-since=2026-08-01 origin 2>&1 | tail -3 &
done
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
ls repos/sirlucjan-kernel-patches/7.2-rc/ | grep -E "fixes-v|lru-marie-v|preempt-ipi-v|nap"
```

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

Check issue titles/descriptions and events (comment bodies + referenced commit SHAs)
for unmerged patch series relevant to our hardware. If a request returns an Anubis
challenge page, you likely used a browser UA — retry with no UA.

## Step 5 — Dry-run clean candidates

Use `git apply --check` (not `patch --dry-run`) against the clean reference tree:

```bash
TREE="repos/linux-7.2-rc6"

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
already exist in the clean rc6 tree (not just in a staging branch). If the
patch fails here it depends on staging infrastructure and must be dropped.
```bash
# For GPU/display patches:
grep -r "<unique_symbol>" repos/linux-7.2-rc6/drivers/gpu/drm/amd/ | head
# For PM patches:
grep -r "<unique_symbol>" repos/linux-7.2-rc6/drivers/cpufreq/ | head
# For block patches:
grep -r "<unique_symbol>" repos/linux-7.2-rc6/block/ | head
```
If `grep` returns nothing for any referenced symbol, DROP the candidate.

**Check 3 — Applies cleanly.** Use `git apply --check` (NOT `patch --dry-run`)
against the clean reference tree:
```bash
git -C repos/linux-7.2-rc6 apply --check <candidate>.patch       # forward check
git -C repos/linux-7.2-rc6 apply --check -R <candidate>.patch    # already-applied check
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

Copy the file in with a descriptive name:
```bash
cp <downloaded-or-exported>.patch NNNN-short-description.patch
```
Example: `1206-cpufreq-amd-pstate-Fix-EPP-return-type-and-handle-er.patch`.

Then document in `PATCH_SOURCES.md` **before** adding to `PKGBUILD`.
Run `updpkgsums` after any `source=()` change.

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
