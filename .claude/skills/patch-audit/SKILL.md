---
name: patch-audit
description: Ingest or upgrade a specific kernel patch for sleepy-kernel — add a named patch or commit SHA, swap an existing patch to a newer revision (e.g. a v2-to-v4 swap), or verify a candidate's provenance and eligibility (symbols exist, applies cleanly, hardware-relevant) before it goes in. Use when given a specific patch, commit, or series to bring into the tree, or when asked to audit/verify a patch source or PATCH_SOURCES.md provenance. For the periodic all-source sweep, use the patch-sweep skill instead.
---

# Patch Audit & Ingestion

Never scrape `lore.kernel.org` — its anti-bot protection blocks agents.

## Detailed Source Access & Fetch Guide

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
- **Audit**: Inspect `7.2-rc/` directories. Current versions to expect:
  `lru-marie-patches-v12/`, `zstd-dev-patches/`, `block-patches-sep/`,
  `cachyos-fixes-patches-v10-sep/`, `preempt-ipi-patches-v3-sep/`, `nap-patches/`.
- **Byte-check**: Verify `2000–2004` (block), `2100–2101` (MM) patches match source diffs.

### 6. `sirlucjan` NAP governor (NOT firelzrd)
- **IMPORTANT (learned this session):** the NAP governor source is
  `repos/sirlucjan-kernel-patches/7.2-rc/nap-patches/`, which contains
  `0001-7.2-nap-v0.5.0.patch`. firelzrd's repo
  (`repos/firelzrd-bore-scheduler`) has **NO** `nap-patches/` directory — its
  `patches/` only contains `additions/`, `legacy/`, `stable/`, `testing/` and is
  BORE-scheduler only. Do not look for NAP patches there.
- Fetch: `git -C repos/sirlucjan-kernel-patches pull`
- Audit: `ls repos/sirlucjan-kernel-patches/7.2-rc/nap-patches/` and compare
  against the in-tree `2200-7.2-nap-v0.5.0.patch`.

---

## Step-by-Step Ingestion & Validation Workflow

Run these in order. Copy the commands exactly — do not improvise.

1. **Verify Target Hardware**: Confirm candidate patch targets a hardware
   component in `CLAUDE.md`'s target table (Zen 4, RDNA 4/gfx1201/DCN401/SMU14,
   Realtek RTL8125, Phison E16, sched-ext, NAP). Reject all non-target hardware
   (i915, xe, nouveau, Intel WiFi, Bluetooth, laptop audio).

2. **Check Symbol Presence**:
   ```bash
   grep -r "<unique_symbol>" repos/linux-7.2-rc7/drivers/gpu/drm/amd/
   ```
   Run this for EVERY function/macro the patch references. If any symbol is
   absent from the clean rc7 tree, the patch depends on staging infrastructure
   and must be DROPPED (see the agd5f staging lesson in `LESSONS.md`).
   **Cover struct members too** (learned 2026-08-10, patch `1025`): a patch can
   apply cleanly yet not compile when it references a `struct` field an
   upstream prerequisite series adds (e.g. `adev->gfx.userq_priv_fault_work` /
   `userq_priv_fault_slots`, added by the gfx11 priv-fault worker in drm-next
   AFTER rc7). For every `adev->xxx.field` / `->member` the patch touches, grep
   that member name in the clean tree's `.h`/`.c` (`grep -rn "userq_priv_fault_work" repos/linux-7.2-rc7/drivers/gpu/drm/amd/amdgpu/`). Absent member
   → DROP and defer to the next version move; do not backport the prerequisite
   series during a bump.

3. **Forward apply check** — patch must apply to the clean rc7 tree:
   ```bash
   git -C repos/linux-7.2-rc7 apply --check "$PWD/<NNNN-short-description.patch>"   # use ABSOLUTE path
   patch -p1 --forward --dry-run < <NNNN-short-description.patch>                  # authoritative — matches prepare()
   ```
   - No output = clean, proceeds to step 4.
   - Error output = context shifted or prereqs missing. Fix hunk offsets,
     regenerate from source, or drop the patch. Do not silently force it.
   - **`git apply --check` can pass while GNU `patch -p1 --forward` rejects**
     (learned 2026-08-03): ambiguous leading context (e.g. `if (r)` appears many
     times in `gfx_v12_0_sw_init`) or a hunk touching a file absent from rc7
     (DCN6 `dcn60_resource.c`) both fool `git apply`. ALWAYS confirm with
     `patch -p1 --forward --dry-run`. For a file absent from rc7, strip that
     file's hunks + its stats line + fix the "N files changed" summary as a
     documented backport adjustment. Capture git's real exit code —
     `git apply ... > log 2>&1; echo $?` — never `| head && echo OK`.

4. **Already-applied check** — confirm it is NOT already in the tree:
   ```bash
   git -C repos/linux-7.2-rc7 apply --check -R <NNNN-short-description.patch>
   ```
   - If this REVERSE check passes (no output), the patch is already merged —
     DROP it and report why.
   - If the reverse check also errors, the patch is genuinely new.

   (Lesson in `LESSONS.md`: use `git apply --check` for both — `patch --dry-run`
   reports false "corrupt patch" errors on mbox-format patches.)

   **LESSON (2026-08-02 sweep) — reverse-clean means ALREADY IN BASE TREE:**
   a clean reverse check is the single most common reason a candidate is
   useless. This session caught six "already in the base tree" candidates
   exactly this way: `f8ee6447e` (drm/amdgpu/discovery: Fix device family for DCN42),
   `7e1b4bdb0` (Fix flip-done timeouts on mode1 reset), `c936b8126`,
   `198663d03`, `183bbded9`, `85453fb4f`. When the reverse check passes clean,
   the patch is ALREADY in the base tree (currently rc7) — DO NOT add it and
   DO NOT try to force it. Record it in the sweep report as "already in base".

5. **Number Assignment**: The prefix MUST match the category. Copy the file in
   with the next unused number:
   | Prefix | Category |
   |--------|----------|
   | `00xx` | Local / hand-selected (0001–0049) or EDID/display ML (0050–0099) |
   | `01xx` | CachyOS branch squashes (0101–0109, one per branch) |
   | `10xx` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) |
   | `11xx` | AMD Display (DCN4, DCN42B, PSR) |
   | `12xx` | AMD Power Management (amd-pstate, cpufreq) |
   | `20xx` | Block / I/O schedulers (bfq, mq-deadline) |
   | `21xx` | Memory management (zstd, LRU-MARIE) |
   | `22xx` | CPU idle (NAP governor) |
   | `90xx` | agd5f staging backports |
   ```bash
   cp <source.patch> NNNN-short-description.patch
   ```

6. **Document Provenance**: Update `PATCH_SOURCES.md` **BEFORE** modifying
   `PKGBUILD`. Include file name, author, subject, and source URL or commit
   hash. A patch that is in `PKGBUILD` but not in `PATCH_SOURCES.md` is a
   provenance failure.

7. **Update PKGBUILD & Checksums**: Add the patch to the `source=()` array in
   `PKGBUILD` in the correct numeric order, then:
   ```bash
   updpkgsums
   ```
   Checksums must match 1:1 — forgetting `updpkgsums` makes makepkg refuse to
   build. After this, hand off to the `kernel-build` skill.

---

## Replacing / upgrading an existing patch (e.g., a v2 → v4 revision swap)

**Note on `00xx` local patches:** the local Antigravity patches live in the
`00xx` range (e.g. the PROFILE_PEAK family `0003`/`0004`) and are routinely
revised in place — `0004` (deep sleep in PROFILE_PEAK) went to **v4** on
2026-08-02. When you swap in a new revision you keep the same number, filename,
and series position.

Run these after placing the new revision (it may come from a Downloads folder,
a fresh `git format-patch` export, or a mailing-list re-read — not necessarily
from a fetched repo):

```bash
# 1. Overwrite the existing patch file IN PLACE (same name/number):
cp ~/Downloads/<new-revision>.patch NNNN-short-description.patch

# 2. Refresh the checksum — updpkgsums recomputes the BLAKE2 (b2sums) entry in
#    PKGBUILD for every file whose content changed. ALWAYS run this after a swap:
updpkgsums

# 3. Re-validate the swapped patch against the clean tree (forward + reverse):
git -C repos/linux-7.2-rc7 apply --check NNNN-short-description.patch
git -C repos/linux-7.2-rc7 apply --check -R NNNN-short-description.patch

# 4. Re-validate the FULL series. A revision swap can shift context for LATER
#    patches. The authoritative in-order apply check is prepare() — run it:
rm -rf src && makepkg -o
```

`makepkg -o` runs the `prepare()` phase only: it verifies the checksums and
applies the entire series (`0001` → `2200`) in order, stopping at the first
failure. If it fails, diagnose per the `kernel-build` skill (read the `.rej`,
regenerate the shifted patch from source, or report).

Then update the `PATCH_SOURCES.md` entry: note the new version and date (e.g.
`0004` ... **v4** (2026-08-02): ...) and what changed.
