---
name: patch-audit
description: Ingest a specific upstream kernel patch, audit third-party (10xx) patches, replace/upgrade an existing patch to a newer revision (e.g. a v2-to-v4 swap), or run the periodic six-source sweep for sleepy-kernel. Use when asked to check for new patches, ingest or add a named patch/commit, swap in a revised version of a patch we already carry, audit patch sources, verify PATCH_SOURCES.md provenance, or review whether a candidate patch belongs in the tree. Covers drm-next, linux-next, linux-pm, amd-gfx, dri-devel, sirlucjan, and firelzrd.
---

# Patch Audit & Ingestion (Six-Source Sweep)

Never scrape `lore.kernel.org` — its anti-bot protection blocks agents.

## Detailed Source Access & Fetch Guide

### 1. `drm-next` (AMD GPU / Display / SMU / RDNA 4)
- **Repository**: `https://gitlab.freedesktop.org/drm/kernel.git` (branch `drm-next`) or `https://gitlab.freedesktop.org/drm/amd.git` (branch `amd-staging-drm-next`)
- **Location**: `repos/drm-next`
- **Fetch**: `cd repos/drm-next && git fetch origin`
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
   grep -r "<unique_symbol>" repos/linux-7.2-rc5/drivers/gpu/drm/amd/
   ```
   Run this for EVERY function/macro the patch references. If any symbol is
   absent from the clean rc5 tree, the patch depends on staging infrastructure
   and must be DROPPED (see the agd5f staging lesson in CLAUDE.md).

3. **Forward apply check** — patch must apply to the clean rc5 tree:
   ```bash
   git -C repos/linux-7.2-rc5 apply --check <NNNN-short-description.patch>
   ```
   - No output = clean, proceeds to step 4.
   - Error output = context shifted or prereqs missing. Fix hunk offsets,
     regenerate from source, or drop the patch. Do not silently force it.

4. **Already-applied check** — confirm it is NOT already in the tree:
   ```bash
   git -C repos/linux-7.2-rc5 apply --check -R <NNNN-short-description.patch>
   ```
   - If this REVERSE check passes (no output), the patch is already merged —
     DROP it and report why.
   - If the reverse check also errors, the patch is genuinely new.

   (Lesson from CLAUDE.md: use `git apply --check` for both — `patch --dry-run`
   reports false "corrupt patch" errors on mbox-format patches.)

   **LESSON (2026-08-02 sweep) — reverse-clean means ALREADY IN BASE TREE:**
   a clean reverse check is the single most common reason a candidate is
   useless. This session caught six "already in rc5" candidates exactly this
   way: `f8ee6447e` (drm/amdgpu/discovery: Fix device family for DCN42),
   `7e1b4bdb0` (Fix flip-done timeouts on mode1 reset), `c936b8126`,
   `198663d03`, `183bbded9`, `85453fb4f`. When the reverse check passes clean,
   the patch is ALREADY in the base tree — DO NOT add it and DO NOT try to
   force it. Record it in the sweep report as "already in rc5".

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
git -C repos/linux-7.2-rc5 apply --check NNNN-short-description.patch
git -C repos/linux-7.2-rc5 apply --check -R NNNN-short-description.patch

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
