---
name: patch-audit
description: Ingest or upgrade a specific kernel patch for sleepy-kernel — add a named patch or commit SHA, swap an existing patch to a newer revision (e.g. a v2-to-v4 swap), or verify a candidate's provenance and eligibility (symbols exist, applies cleanly, hardware-relevant) before it goes in. Use when given a specific patch, commit, or series to bring into the tree, or when asked to audit/verify a patch source or PATCH_SOURCES.md provenance. For the periodic all-source sweep, use the patch-sweep skill instead.
---

# Patch Audit & Ingestion

Never scrape `lore.kernel.org` — its anti-bot protection blocks agents.

## Reference tree

All apply-checks and symbol greps target the **base tree** of the package you
are editing: `repos/linux-7.2@<tag>` for the root `linux-sleepy` package, or a
`git worktree` of `repos/linux-next` at the `_srctag` (e.g. `v7.3-rc2`) for
`sleepy-next`. Create one with
`git -C repos/linux-next worktree add /tmp/ref <tag>`.

## Source access

Per-source fetch commands, archive workarounds, and extraction gotchas:
see [`references/sources.md`](references/sources.md).

## Step-by-Step Ingestion & Validation Workflow

Run these in order. Copy the commands exactly — do not improvise.

1. **Verify Target Hardware**: Confirm candidate patch targets a hardware
   component in `CLAUDE.md`'s target table (Zen 4, RDNA 4/gfx1201/DCN401/SMU14,
   Realtek RTL8125, Phison E16, sched-ext, NAP). Reject all non-target hardware
   (i915, xe, nouveau, Intel WiFi, Bluetooth, laptop audio).

2. **Check Symbol Presence**:
   ```bash
   grep -r "<unique_symbol>" <base-tree>/drivers/gpu/drm/amd/
   ```
   Run this for EVERY function/macro the patch references. If any symbol is
   absent from the clean base tree, the patch depends on staging infrastructure
   and must be DROPPED (see the agd5f staging lesson in `LESSONS.md`).
   **Cover struct members too** (learned 2026-08-10, patch `1025`): a patch can
   apply cleanly yet not compile when it references a `struct` field an
   upstream prerequisite series adds (e.g. `adev->gfx.userq_priv_fault_work` /
   `userq_priv_fault_slots`, added by the gfx11 priv-fault worker in drm-next
   AFTER the base release). For every `adev->xxx.field` / `->member` the patch touches, grep
   that member name in the clean tree's `.h`/`.c` (`grep -rn "userq_priv_fault_work" <base-tree>/drivers/gpu/drm/amd/amdgpu/`). Absent member
   → DROP and defer to the next version move; do not backport the prerequisite
   series during a bump.

3. **Forward apply check** — patch must apply to the clean base tree:
   ```bash
   git -C <base-tree> apply --check "$PWD/<NNNN-short-description.patch>"   # use ABSOLUTE path
   patch -p1 --forward --dry-run < <NNNN-short-description.patch>                  # authoritative — matches prepare()
   ```
   - No output = clean, proceeds to step 4.
   - Error output = context shifted or prereqs missing. Fix hunk offsets,
     regenerate from source, or drop the patch. Do not silently force it.
   - **`git apply --check` can pass while GNU `patch -p1 --forward` rejects**
     (learned 2026-08-03): ambiguous leading context (e.g. `if (r)` appears many
     times in `gfx_v12_0_sw_init`) or a hunk touching a file absent from the base
     (DCN6 `dcn60_resource.c`) both fool `git apply`. ALWAYS confirm with
     `patch -p1 --forward --dry-run`. For a file absent from the base, strip that
     file's hunks + its stats line + fix the "N files changed" summary as a
     documented backport adjustment. Capture git's real exit code —
     `git apply ... > log 2>&1; echo $?` — never `| head && echo OK`.

4. **Already-applied check** — confirm it is NOT already in the tree:
   ```bash
   git -C <base-tree> apply --check -R <NNNN-short-description.patch>
   ```
   - If this REVERSE check passes (no output), the patch is already merged —
     DROP it and report why.
   - If the reverse check also errors, the patch is genuinely new.

   (Lesson in `LESSONS.md`: use `git apply --check` for both — `patch --dry-run`
   reports false "corrupt patch" errors on mbox-format patches.)

   **Reverse-clean means ALREADY IN BASE.** A clean reverse check is
   the most common reason a candidate is useless — record it as
   "already in base" and do not add or force it.

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
   cp <source.patch> patches/<range>/NNNN-short-description.patch
   ```

6. **Document Provenance**: Update `PATCH_SOURCES.md` **BEFORE** modifying
   `PKGBUILD`. Include file name, author, subject, and source URL or commit
   hash. A patch that is in `PKGBUILD` but not in `PATCH_SOURCES.md` is a
   provenance failure. Write the entry in Google doc style — see
   `.claude/style-guides/google-docguide/`.

7. **Update PKGBUILD & Checksums**: Add the patch to the `source=()` array in
   `PKGBUILD` in the correct numeric order (entry is
   `patches/<range>/NNNN-....patch`), then:
   ```bash
   updpkgsums
   ```
   Checksums must match 1:1 — forgetting `updpkgsums` makes makepkg refuse to
   build. `updpkgsums` also recreates the gitignored root symlinks makepkg needs
   to resolve folder-stored patches. After this, hand off to the `kernel-build`
   skill.

---

## Auditing the whole series (is every patch still needed + clean?)

Run this after a base bump or before a release. Work in a **fresh worktree** at
the base tag (`git -C repos/linux-next worktree add .wt-audit <tag>`).

```bash
# Apply the series cumulatively, exactly as prepare() does, classifying each.
# The authoritative test — git apply --check and per-patch dry-runs give false
# negatives, and `patch --forward` exits 0 when it SKIPS a reversed patch.
python3 - <<'PY'
import re, subprocess
ps=[x.strip().strip('"') for x in re.search(r'^source=\((.*?)^\)',
      open('PKGBUILD').read(), re.S|re.M).group(1).split('\n')
      if x.strip().strip('"').endswith('.patch')]
T='repos/linux-next/.wt-audit'; clean=[]; noop=[]; fail=[]
for i,b in enumerate(ps,1):
    d=subprocess.run(['patch','-p1','--forward','--dry-run','-F2'],cwd=T,
        stdin=open(b),capture_output=True,text=True); o=d.stdout+d.stderr
    if 'Reversed (or previously applied)' in o or 'Skipping patch' in o:
        noop.append((i,b)); continue
    if 'FAILED' in o or 'malformed' in o:
        fail.append((i,b,o.strip().split('\n')[0][:70])); continue
    subprocess.run(['patch','-p1','--forward','-F2'],cwd=T,stdin=open(b),capture_output=True)
    clean.append((i,b))
print(f"CLEAN={len(clean)} NO-OP={len(noop)} FAIL={len(noop and 0 or 0)+len(fail)}")
for i,b in noop: print("  NO-OP (drop):", b)
for i,b,d in fail: print("  FAIL:", b, "|", d)
PY
```

- **NO-OP** = already in the base → drop it (a skipped patch is inert).
- **FAIL** = needs rebasing or dropping; check whether the base superseded it.
- After the audit, re-run the full apply and confirm **0 `.rej`** and that the
  key hooks/symbols each patch adds are present.

**Rebasing a large patch (LRU-MARIE)**: see
[`references/marie-rebase.md`](references/marie-rebase.md) — never hand-edit
hunk headers; regenerate the changed file-sections with `diff -u`.

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
git -C <base-tree> apply --check NNNN-short-description.patch
git -C <base-tree> apply --check -R NNNN-short-description.patch

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
