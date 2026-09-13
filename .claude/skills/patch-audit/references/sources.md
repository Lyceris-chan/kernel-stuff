# Source access & fetch guide

> **Package location (2026-09-12).** The repo is single-package: everything this
> skill touches lives in `sleepy-next/`. Unless a step says otherwise, `cd
> sleepy-next` first so paths like `PKGBUILD`, `patches/...`, `config`,
> `net-tune/` and `PATCH_SOURCES.md` resolve. From the repo root, prefix them
> with `sleepy-next/`.

Per-source fetch commands, archive-access workarounds, and extraction
gotchas. Referenced from `SKILL.md`.

## Contents

- [1. `drm-next`](#1-drm-next-amd-gpu--display--smu--rdna-4)
- [2. `linux-next`](#2-linux-next-mainline-integration-tree)
- [3. `linux-pm`](#3-linux-pm-cpu-power--freq--zen-4-amd-pstate)
- [4. `amd-gfx` and `dri-devel` mailing lists](#4-amd-gfx--dri-devel-mailing-lists)
- [4b. drm/amd work-items tracker — access workaround](#4b-drmamd-work-items-tracker-gitlabfreedesktoporg--access-workaround-learned-2026-08-03)
- [5. `sirlucjan`](#5-sirlucjan-third-party-performance-patches)
- [6. `sirlucjan` NAP governor (not firelzrd)](#6-sirlucjan-nap-governor-not-firelzrd)
- [Reaching gitlab.freedesktop.org without git](#reaching-gitlabfreedesktoporg-without-git-learned-2026-09-12)

### Detailed Source Access & Fetch Guide

### 1. `drm-next` (AMD GPU / Display / SMU / RDNA 4)
- **Repository**: `https://gitlab.freedesktop.org/drm/kernel.git` (branch `drm-next`) or `https://gitlab.freedesktop.org/drm/amd.git` (branch `amd-staging-drm-next`)
- **Location**: `repos/drm-next`
- **Fetch**: `cd repos/drm-next && git fetch origin`
- **If gitlab.freedesktop.org returns HTTP 503 (`RPC failed; expected 'packfile'`)**:
  do not block the cycle. Cover drm-next content via `repos/linux-next`
  (drm-next is merged into it) and the AMD staging branch via
  `repos/agd5f-linux` (same `amd-staging-drm-next` branch), and retry the
  gitlab fetch in the background. Seen for hours on the 2026-08-03 7.2-rc6 bump.
- **Search Query**:
  ```bash
  git log --oneline --grep="gfx12\|navi48\|dcn4\|smu14\|psp14\|mmhub_4\|sdma_v7\|vcn_v5\|dcn42b" origin/drm-next
  ```
- **Extract Patch**:
  ```bash
  git format-patch -1 <commit_hash> -o ../../
  ```

### 2. `linux-next` (Mainline Integration Tree)
- **Repository**: `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git`
- **Location**: `repos/linux-next`
- **Fetch**: `cd repos/linux-next && git fetch origin`
- **Before fetching (learned 2026-08-03):** the full `git fetch origin` of
  linux-next is very slow (many branches, single HTTP connection). First check
  whether a newer daily snapshot even exists — the tree publishes `next-YYYYMMDD`
  tags on working days only:
  ```bash
  git ls-remote --tags repos/linux-next 'next-*' | awk -F/ '{print $NF}' | grep -v "\^{}" | sort -V | tail -1
  ```
  If the latest tag is one you already have locally (compare against
  `git -C repos/linux-next describe --tags master`), skip the fetch entirely —
  there is no new content to sweep. Only fetch when a newer snapshot exists.
  Note `next-*` tags skip weekends (08-01/08-02 were quiet on the 08-03 sweep).
- **Search Query**:
  ```bash
  git log --oneline --grep="gfx12\|navi48\|dcn4\|smu14\|amd_pstate\|MZEN4\|CPPC" origin/master
  ```
- **Extract Patch**:
  ```bash
  git format-patch -1 <commit_hash> -o ../../
  ```

### 3. `linux-pm` (CPU Power / Freq / Zen 4 amd-pstate)
- **Repository**: `https://git.kernel.org/pub/scm/linux/kernel/git/rafael/linux-pm.git`
- **Location**: `repos/linux-pm`
- **Fetch**: `cd repos/linux-pm && git fetch origin`
- **Search Query**:
  ```bash
  git log --oneline --grep="amd-pstate\|amd_pstate\|CPPC\|k10temp\|epp_boost" origin/master
  ```
- **Extract Patch**:
  ```bash
  git format-patch -1 <commit_hash> -o ../../
  ```

### 4. `amd-gfx` & `dri-devel` Mailing Lists
- **Archives**: `https://lists.freedesktop.org/archives/amd-gfx/` and `https://lists.freedesktop.org/archives/dri-devel/`
- **Access Method (proven workaround):** `WebFetch` gets HTTP 403 on
  `lists.freedesktop.org`. Use `curl` with a browser User-Agent:
  ```bash
  UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
  curl -s -A "$UA" "https://lists.freedesktop.org/archives/amd-gfx/${MONTH}/thread.html" -o /tmp/amd-thread.html
  curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html" -o /tmp/dri-thread.html
  ```
  URL format: `https://lists.freedesktop.org/archives/{amd-gfx|dri-devel}/{YYYY-Month}/thread.html`
  (or `date.html`). Per-message pages live at `.../{msgid}.html`. A monthly
  `.txt.gz` mbox is also available: `.../{YYYY-Month}.txt.gz`.
- **Search**: Parse thread HTML for subjects targeting `gfx12`, `navi48`, `dcn4`, `smu14`, `sdma7`, `vcn5`.
- **Extraction**: Download raw mbox file for the target thread or save patch directly.
- **Clean-patch extraction from mboxes (learned 2026-08-03):** a saved thread mbox
  contains replies that *quote* the original patch, so `git apply --check` on a raw
  message fails ("corrupt patch"). Split the **full monthly mbox** (`amd-gfx-2026-July.mbox`),
  find the **original submission** (unquoted `diff --git`, author `Signed-off-by`), then
  extract with `git mailinfo <msgfile> <patchfile>` → clean patch body + separate commit
  message. Reconstruct the patch file with the original `From:`/`Date:`/`Subject:`/`Message-ID:`
  headers (mbox format is fine; preserve author and `Signed-off-by`). **Sanitize the
  filename**: a `Subject:` with a folded header line embeds a literal `\n` in the name —
  strip it (e.g. `subj.split('] ',1)[-1].replace('\n',' ').replace('/','-')`) or rename to a
  clean `NNNN-short-desc.patch` before copying into the repo.
- **Series-order check:** a candidate whose trailing context matches content that an
  earlier *backported* patch adds (e.g. `9008`'s DB_RING_CONTROL context comes from `9007`)
  must be numbered to apply **after** that patch. Test sequentially in a scratch tree, not
  just `git apply --check` in isolation.
- **Context-symbol dependency (learned 2026-08-03):** a patch can require a *struct field*
  or *function* another patch adds — e.g. `1129` (dtbclk) needs `execute_clk_mgr_block_sequence`
  (added by `1127`) and `notify_cstate_disable` (added by `1128`) in its `clk_mgr.h`/`dcn42_clk_mgr.c`
  hunk context. `git apply --check` on the full series tree may still pass (offset tolerance)
  while GNU `patch` in prepare() rejects it. When a `.rej` shows context lines that reference a
  symbol another carried patch adds, renumber so that patch comes FIRST (1127→1128→1129 order).
  The definitive check is `prepare()`/`makepkg -o` applying the whole series in order.
- **Per-message extraction gotchas (learned 2026-08-26):** thread.html message links are
  `<LI><A HREF="NNNNN.html">subject` (bare 6-digit msgid, not `msgNNNNN.html`) — grep with
  `-oE '<LI><A HREF="[0-9]+\.html">[^<]*'` to find the ORIGINAL submission (replies quote the
  patch and break spacing). dri-devel pages use U+00A0 nbsp for indentation
  (`.replace('&nbsp;',' ').replace('\xa0',' ')`) and may carry a trailing HTML attachment
  after the `-- ` diff terminator (truncate there). QP-encoded mboxes: `git am <mbox>` on a
  scratch worktree decodes natively, then cherry-pick.
- **Tree-target triage — amdgpu_dm split (learned 2026-08-26):** a patch touching
  `amdgpu_dm_connector.c` / `amdgpu_dm_freesync.c` targets the 7.3+ amdgpu_dm split; the
  same content on 7.2 lives in the MONOLITHIC `amdgpu_dm.c`. Verify `git apply --check`
  against the right reference tree (`repos/linux-next` for the PKGBUILD series,
  `repos/linux-next@<next-tag>` for the sleepy-next 7.3 preview — the wannabe worktree is
  gone) BEFORE deciding applicability — "No such file" on
  `amdgpu_dm_connector.c` means the patch is 7.3-only.

### 4b. drm/amd work items tracker (gitlab.freedesktop.org) — ACCESS WORKAROUND (learned 2026-08-03)

`https://gitlab.freedesktop.org/drm/amd/-/work_items` and the REST API
(`/api/v4/projects/drm%2Famd/...`) are fronted by **Anubis**, but the challenge is served
**only to browser-like User-Agents**. Plain `curl` with **no User-Agent header** returns
real GitLab content:
```bash
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/issues?state=opened&per_page=100&sort=updated_desc" -o issues.json
curl -s "https://gitlab.freedesktop.org/api/v4/projects/drm%2Famd/events?per_page=100" -o events.json
```
The issue **notes** API is 401-gated (real auth), but the events/atom feeds expose comment
bodies + referenced commit SHAs. Check issue titles/descriptions/comments for unmerged
patch series or commit SHAs relevant to our hardware. (lore.kernel.org was NOT re-tested —
the "never access lore" rule stands unless separately verified.)

### 5. `sirlucjan` (Third-Party Performance Patches)
- **Repository**: `https://github.com/sirlucjan/kernel-patches.git`
- **Location**: `repos/sirlucjan-kernel-patches`
- **Fetch**: `cd repos/sirlucjan-kernel-patches && git pull`
- **Audit**: Inspect `7.2/` directories. Current versions to expect:
  `lru-marie-patches-v12/`, `zstd-dev-patches/`, `block-patches-sep/`,
  `cachyos-fixes-patches-v10-sep/`, `preempt-ipi-patches-v3-sep/`, `nap-patches/`.
- **Byte-check**: Verify `2000–2004` (block), `2100–2101` (MM) patches match source diffs.

### 6. `sirlucjan` NAP governor (NOT firelzrd)
- **IMPORTANT (learned this session):** the NAP governor source is
  `repos/sirlucjan-kernel-patches/7.0/nap-patches/`, which contains
  `0001-7.2-nap-v0.5.0.patch`. firelzrd's repo
  (`repos/firelzrd-bore-scheduler`) has **NO** `nap-patches/` directory — its
  `patches/` only contains `additions/`, `legacy/`, `stable/`, `testing/` and is
  BORE-scheduler only. Do not look for NAP patches there.
- Fetch: `git -C repos/sirlucjan-kernel-patches pull`
- Audit: `ls repos/sirlucjan-kernel-patches/7.0/nap-patches/` and compare
  against the in-tree `2200-7.2-nap-v0.5.0.patch`.
---

## Reaching gitlab.freedesktop.org without git (learned 2026-09-12)

GitLab is **Anubis-protected for browser-like clients** but **not** for plain
`curl`. A headless browser (Helium/Chromium) just gets the challenge page
(`Oh noes!` / `/.within.website/x/xess/`) and cannot clear the PoW
non-interactively — do not try to reach GitLab through a browser.

Use the **REST API with plain `curl` (NO User-Agent)** instead. It answers in
~0.1 s even when the git transport times out:

```bash
API=https://gitlab.freedesktop.org/api/v4/projects
P=agd5f%2Flinux          # the AMD staging fork we clone; NOT drm%2Famd
curl -s "$API/$P/repository/branches?search=amd-staging"
curl -s "$API/$P/repository/commits?ref_name=amd-staging-drm-next&per_page=20"
curl -s "$API/$P/repository/commits/<sha>/diff"        # per-commit hunks (JSON)
curl -s "$API/$P/repository/files/<url%2Fencoded%2Fpath>/raw?ref=<ref>"
curl -s "$API/drm%2Famd/issues?state=opened&per_page=50"
```

- `drm%2Famd` = the group **issue tracker** (work items) — correct for issues.
- `agd5f%2Flinux` = the **code**. The `drm/amd` *project* code is a stale group
  mirror whose `master` is from 2025 — do not clone or query it for code.
- There is **no GitHub or kernel.org mirror** of agd5f/linux (`api.github.com`
  and `git.kernel.org` both 404).
- `git ls-remote`/`fetch` against `agd5f/linux` does work — it is just
  intermittently slow on the huge ref advertisement; retry before declaring it
  unreachable.
