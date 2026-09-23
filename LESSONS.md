# Lessons learned: do not repeat

Full incident log for sleepy-kernel. Kept out of `CLAUDE.md` so the operating
manual stays short; CLAUDE.md carries only the durable rules. Read this before
repeating a past mistake. Patch numbers are current as of 7.3-rc3; see
`sleepy-next/PATCH_SOURCES.md` for per-patch provenance and renumber history.

| Mistake | What happened | Rule |
|---|---|---|
| `ld.mold` for kernel linking | Crashed on vDSO linker scripts | Never use `ld.mold` for kernel builds |
| `--depth=1` git clone | `git log --grep` returned nothing | Always use `--shallow-since` |
| Scraped `lore.kernel.org` | Anti-bot blocked all requests | Use git repos or freedesktop.org archives |
| Both `TCP_CONG_BBR` and `BBR3` built-in | Duplicate BTF kfunc symbol → `resolve_btfids` exit 255 | Disable old BBR after `olddefconfig` |
| `LLVM=/path/to/bin/` instead of `LLVM=1` | `resolve_btfids` skipped compilation | Set `LLVM=1`, prepend bin to `$PATH` |
| `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT` with Clang 23 | pahole 1.31 couldn't parse DWARF → BTF generation failed | Use `DEBUG_INFO_DWARF5` explicitly |
| Dropped patch without user approval | User directive: never remove without sign-off | Always ask first |
| Checked only drm-next for patches | Missed mailing-list-only patches | Check all six sources every sweep |
| Trusted `ls-remote --tags` for linux-next | kernel.org's huge repo may not advertise the newest snapshot (`next-20260803` missing from the tag list though fetchable) | If a newer working-day tag should exist, `git fetch origin tag next-YYYYMMDD` directly before concluding nothing is new |
| Assumed mailing list patch was merged | Mailing list ≠ drm-next | Verify with `git log --grep` in mainline |
| Reconstructed patch using upstream line numbers | Didn't match our patched tree | Always regenerate against our actual layout |
| Added already-merged patch | `--dry-run` showed "already applied" | `grep` for the symbol first |
| Forgot `updpkgsums` | makepkg refused to build | Run after every `source=()` change |
| Added patch without documenting | Provenance lost | Document in `PATCH_SOURCES.md` first |
| Hand-crafted patch with bad `@@` hunks | Malformed diff broke build | Never hand-write patches |
| Used `8.8.8.8` in network script | User preference is Quad9 | Always use `9.9.9.9` |
| Cloned repos to `/tmp` | tmpfs filled up, repos lost on reboot | Clone to `repos/` |
| Used raw sirlucjan MARIE patch | Conflicted with CachyOS `vm_swappiness` override | Use CachyOS-rebased MARIE |
| `olddefconfig` re-enabled `TCP_CONG_BBR` | Dependency resolution pulled it back | Disable again after `olddefconfig` |
| Reversed patch `1100` (PSR on DCN4, formerly `1025`) without documenting | Causes desktop freezes on RDNA 4 | Reverse-apply is in `prepare()` |
| Applied patch `1101` (DCN4 pstate enable, formerly `1031`) | Forced broken UCLK switching, causing freezes unless `profile_peak` was used | Patch `1101` is now reverse-applied in `prepare()` to keep `.pstate_enabled = false`. Check the reverse-apply line matches the current patch filename when renumbering. |
| Applied patch `1102` (DCN42b uclk increase, formerly `1033`) | Distorted DML2.1 latency calculations in low DPM states | Patch was audited and found safe to keep applied — the concern was unfounded. Only `1101` is reversed. |
| Backported agd5f staging patch 2008 | Referenced `amdgpu_userq_process_reset_irq` and `AMDGPU_CTXID0_DOORBELL_ID_MASK` which exist only in `agd5f/linux amdgpu_userq.h` but **not in Linux 7.2-rc5 mainline** — caused `undeclared identifier` compile errors | Before adding any `2xxx` patch, `grep -r <new_symbol> src/linux-*/drivers/` to confirm all referenced functions and macros exist in the current mainline tree. If missing, the patch depends on staging infrastructure and must be dropped. |
| 0xxx patches had gaps (0013–0015 missing) | Caused confusing jump from 0012 → 0016 with no explanation | Always use the next consecutive number in the correct category range. Renumbering after-the-fact requires: rename files, update `source=()`, run `updpkgsums`, update `PATCH_SOURCES.md`, update `CLAUDE.md`, update `README.md`, update any `prepare()` reverse-apply lines. |
| All 1xxx patches in one undifferentiated range | Mixed GPU core, display, power management, block, MM, and cpuidle into one range — impossible to tell category from number alone | Use the category-based subcategory scheme: `1000–1099` GPU core, `1100–1199` display, `1200–1299` PM, `2000–2099` block, `2100–2199` MM, `2200–2299` cpuidle, `9000–9099` agd5f staging. |
| Used monolithic CachyOS mega-patch | Single 900 KB diff caused FreeSync collision with upstream hdmi branch; impossible to exclude off-target patches | Switch to sirlucjan per-branch `-sep` files squashed to one patch per branch (`0101`–`0109`). Off-target branches (`snd-codecs`, `t2`) are never squashed; off-target patches inside `fixes` are reverted by `0106-cachy-drops`. |
| Added `0151` (HDMI HF-VSDB) when `0055` was already applied | `0151` adds the same `drm_hdmi_vrr_cap` struct as `0055` (Fangzhi Zuo 2/4). Patch shows as "Reversed" at apply time. | If `0055` is in the series, exclude `0151` from the `0107-cachy-hdmi` squash. The two patches add identical content to `drm_edid.c` and `drm_connector.h`. |
| Applied `0053` (remove DMCU parser) before CachyOS hdmi branch | `0053` deletes `dc_edid_parser.h`. The CachyOS hdmi branch still includes `amdgpu_dm.c` which includes that header. Compile fails with "file not found". | When the CachyOS hdmi branch is present, drop `0053`. The DMCU parser cleanup is moot because the hdmi branch already refactored the callers. |
| Attempted to backport Fangzhi Zuo 1/4, 3/4, 4/4 (HDMI FRL patches) | These patches target `amdgpu_dm_connector.c` which was split from `amdgpu_dm.c` by Alex Hung (agd5f `0e967e086e75`) in April 2026. That split is not in rc5. | Defer until the `amdgpu_dm_connector.c` split lands in mainline (expected 7.3). Only `0055` (2/4, touches `drm_edid.c` only) and `0058` (FRL cap restore) are safe to add now. |
| `vm_flags & VM_EXEC` in LRU-MARIE after `fixes` branch applied | Sirlucjan `fixes` branch (squashed in `0105`) renames `vm_flags` → `vma_flags` with new type `vma_flags_t`. LRU-MARIE's `#ifdef CONFIG_LRU_MARIE` block still used the old `(vm_flags & VM_EXEC)` expression — compile error: invalid operands to binary expression. | In-tree fix: change `(vm_flags & VM_EXEC)` to `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` in `mm/vmscan.c` inside the `CONFIG_LRU_MARIE` block. This is an in-tree source edit, not a patch file. **Update (2026-08-03, rc6): no longer required — LRU-MARIE v12 (`2101`) already ships the `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` form.** |
| `amdgpu_dm_connector.c` split required by upstream HDMI patches | Fangzhi Zuo's July 2026 HDMI series was written against agd5f tree where `amdgpu_dm.c` was split. Applied against rc5 (no split) → "No such file or directory" error. | Check `find repos/linux-7.2-rcN -name "amdgpu_dm_connector.c"` before applying any patch targeting that file. If absent, defer the patch. |
| Validated a candidate only against a **clean** rc7 tree and it applied; it FAILED GNU patch on the actual series state | The PPT-limits refactor `6c9e0328` (9026) applies cleanly to clean rc7 but its 77-line `smu_get_power_limit()` hunk in `amdgpu_smu.c` was rejected by `patch -p1 --forward` on the series tree because the carried CachyOS `01xx` micro-opts patches shift the surrounding context — same for the cascade 9027/9028 | **The authoritative dry-run is always against the full series-applied tree** (repos/linux-7.2-rc7-series, rebuilt via `bash /tmp/apply_series.sh`), with `patch -p1 --forward` — a clean result on clean rc7 proves nothing about our tree. When a framework refactor fails there, drop/defer it (it lands via drm-next at the next bump) rather than hand-forcing hunk offsets on a sensitive subsystem |
| DCN401 GPIO lookup table patch (`334cbfa3c`) fails to compile | `drm/amd/display: convert dcn401 GPIO translation to lookup tables` uses `DC_GPIO_GENERIC_A`, `DC_GPIO_HPD_A` which come from a prerequisite GPIO infrastructure patch not in rc5. | Verify all symbol names used in a patch exist in the tree: `grep -r "DC_GPIO_GENERIC_A" src/linux-*/drivers/gpu/drm/amd/`. If absent, the patch depends on staging prerequisites and must be dropped. |
| `git apply --check` better than `patch --dry-run` | `patch --dry-run` treats mbox-format patches differently and reports false "corrupt patch" errors. `git apply --check` handles both `git format-patch` and mbox formats correctly. | Use `git apply --check <file>` for dry-run testing. Use `git apply --check -R <file>` to test if a patch is already applied (reverse check). |
| Outlook-sent ML patches arrive whitespace-mangled | The GFX12 CRIU fix (`1026`, amd-gfx 2026-08-04) came from a Microsoft-hosted address; lists.freedesktop.org stored it with every context line's leading space stripped and tabs→spaces, so neither `git apply --check` nor GNU `patch` could apply it verbatim. The `+`/`-` content was intact. | If the diff body's added lines survive but context is mangled, reconstruct against rc7 ground truth (use a sibling file the commit message says it's "modeled after" — for example, the v11 MQD manager) and verify content-identical modulo whitespace before adopting. Pass BOTH `git apply --check` and `patch -p1 --forward --dry-run`. |
| `.orig`/`.rej` files from `patch` got committed into squashed patches | `patch` leaves `.orig`/`.rej` backup files next to modified sources; `git add -A` swept them into the squashed CachyOS patches as garbage hunks | Always `find . -name '*.orig' -delete; find . -name '*.rej' -delete` before `git add -A` when generating squashed patches |
| Editing a patch's commit-message body changed its BLAKE2 checksum | Rewriting the 11 handmade patch descriptions (message bodies) invalidated their `b2sums`, so `makepkg` failed the source-validity check | Run `updpkgsums` after ANY change to a `.patch` file — not just `source=()` edits — then re-verify the full series applies |
| `-m V4L2_LOOPBACK` in `prepare()` did nothing | `v4l2loopback` is an out-of-tree module, not a kernel config symbol; `scripts/config -m V4L2_LOOPBACK` is silently dropped by `olddefconfig` | For UVC webcams (incl. Android USB-webcam mode) enable the in-kernel driver instead: `-m USB_VIDEO_CLASS` (uvcvideo). v4l2loopback is installed via AUR (`v4l2loopback-dkms`) when needed |
| Dropped the out-of-tree `r8125` module | The custom Realtek module blacklisted `r8169`; after removing it the NIC had no driver because `CONFIG_R8169` was not enabled | The in-kernel `r8169` covers the RTL8125B — when dropping `r8125`, set `_build_r8125=no` AND enable `-m R8169` in `prepare()` |
| `disable_configs.py` cannot disable symbols that are `select`ed | `RESCTRL_FS` (AMD resctrl) and `SND_INTEL_NHLT` (HDA/audio) came back after `olddefconfig` because another option hard-`select`s them | For `select`-forced symbols, disable the selector (for example, `X86_RESCTRL`) instead, or accept the tiny bloat; verify the built `.config` after each build |
| CAKE flow-isolation directions are easy to get backwards | egress (upload) must use `dual-srchost`, ingress (download) `dual-dsthost` (per tc-cake(8)); a first draft had them swapped | Use `tc qdisc replace` and follow tc-cake(8): egress `dual-srchost nat ack-filter`, ingress `dual-dsthost wash nat`, with `rtt regional` and `overhead ethernet` for a direct Ethernet handoff |
| A clean `git apply --check -R` on a candidate means it is ALREADY in the base tree | Sweeps kept re-proposing `f8ee6447e`, `7e1b4bdb0` that were already in rc5 | Treat a clean reverse check as "already in rc5" — record it and do not add it; only add candidates where the forward check is clean and the reverse check fails |
| cdn.kernel.org lagged the rc6 tag | `updpkgsums` 404'd on `cdn.kernel.org/pub/linux/kernel/v7.x/testing/linux-7.2-rc6.tar.gz` right after the tag was cut — the cdn mirrors RC tarballs late | Use `https://git.kernel.org/torvalds/t/linux-<tag>.tar.gz` in `source=()` when the cdn 404s |
| gitlab.freedesktop.org persistent HTTP 503 | `drm-next` and `amd-staging-drm-next` fetches failed with `RPC failed; HTTP 503` for hours, blocking the sweep | Don't block the cycle: cover drm-next via `linux-next` and the AMD staging branch via `agd5f-linux`, and retry gitlab in the background |
| `patch` leaves `.orig` backups in a git worktree | Regenerating the `01xx` squashes staged `.orig` backups created by `patch`, and they leaked into the squash as huge bogus deletions (`0105` ballooned 51 KB → 628 KB) | `find . -name '*.orig' -delete; find . -name '*.rej' -delete` after EVERY patch phase, before `git add`/`git diff` |
| Overlapping local patches pass `git apply` only in isolation | `0003` and `0004` both edit `smu_v14_0.c` near PROFILE_PEAK; strict `git apply` fails on `0004` after `0003`, but `patch -p1 --forward` applies it with fuzz (offset 2) | Generate and validate squashes with `patch -p1 --forward`, exactly as `prepare()` does — strict `git apply` misreports fuzz-tolerable sequences |
| Regenerated every 01xx squash on a bump, then only fixes/drops needed it | sirlucjan branch content was identical (repo master at 2026-07-31) and `0101`–`0104`/`0107`–`0109` applied cleanly to rc6; only `0105`/`0106` had drifted | On a bump, regenerate only the 01xx squashes that fail `git apply --check`; keep unchanged + clean-applying ones |
| New patch's trailing context matched content an earlier backport adds (`9008` vs `9007` DB_RING_CONTROL) | The truncate-coord gfx12 patch was written against a tree that already had `9007`'s DB_RING_CONTROL block, so it only applied AFTER `9007`; numbered into `10xx` it would fail | When a candidate's context depends on another backport's added content, number it to apply AFTER that backport — even if that crosses into the `90xx` range. Always verify the sequential order |
| Mailing-list mboxes contain quoted replies, not just originals | `git apply --check` on a `thread.html`-downloaded mbox message fails ("corrupt patch") because the diff is inside a quoted reply body | Split the monthly mbox, find the **original** submission (unquoted `diff --git`), extract with `git mailinfo` → clean patch + separate commit message |
| gitlab.freedesktop.org work items tracker is Anubis-blocked (browser UAs only) | For months the `drm/amd/-/work_items` page + REST API returned the Anubis challenge, so we documented it as blocked | **2026-08-03: the challenge is served only to browser-like User-Agents.** Plain `curl` with no User-Agent returns real GitLab content (issues + events API). **2026-08-10: full issue comments are readable via the unauthenticated GraphQL API** (`https://gitlab.freedesktop.org/api/graphql`, `query { project(fullPath:"drm/amd") { issue(iid:"N") { notes { nodes { body } } } } }`) — the REST notes API is 401-gated but GraphQL is not. Use `curl -s ".../issues?search=<kw>&state=all"` to find relevant issues, then GraphQL to scan comments for fix SHAs ("fixed by", `[0-9a-f]{12,40}`, patch links). The HTML issue page renders the description only (comments are Vue-lazy-loaded) |
| A `--since`-window git log sweep can miss patches that moved between staging and drm-next | Staging commits appear in drm-next under *different* SHAs (re-submitted), so hash-based `comm` diffs showed 216 "staging-only" commits that were actually already in drm-next | Diff staging vs drm-next by **subject line**, not SHA; a same-subject commit in drm-next = already reviewed/merged upstream |
| `modprobe ifb numifbs=1` names its device `ifb0`, not the named `ifb4cake` the net-tune script references | Download CAKE never applied (silently — all errors were `2>/dev/null \|\| true`); bufferbloat test showed clean upload but 102 ms download spikes | Create the named ifb explicitly with `ip link add ifb4cake type ifb` (idempotent) before `ip link set ... up`. All tc/ip errors are suppressed, so `net-tune.sh` now verifies the ingress path (ifb4cake present + mirred filter) and logs an ERROR instead of failing silently |
| net-tune's download shaping silently never worked: `CONFIG_NET_SCH_INGRESS` was not set in the kernel, and the script used the `matchall` classifier (`CONFIG_NET_CLS_MATCHALL` also not set) | The ingress qdisc (`tc qdisc ... handle ffff: ingress`) cannot exist without NET_SCH_INGRESS, so every subsequent filter/mirred step failed behind `2>/dev/null \|\| true` — uploads shaped, downloads bufferbloated at line rate (102 ms spikes) | PKGBUILD must enable `NET_SCH_INGRESS` (=y) plus `IFB`/`NET_ACT_MIRRED`/`NET_CLS_U32` (=m) for CAKE SQM ingress; the script uses the u32 match-all idiom (`tc filter ... protocol all u32 match u32 0 0 action mirred egress redirect dev ifb4cake`). Verify the running kernel: `zcat /proc/config.gz \| grep NET_SCH_INGRESS`. net-tune.sh now checks for the ingress qdisc and logs a targeted ERROR |
| `ENABLE_SQM=no` in the shipped `net-tune.conf` → net-tune.service applied latency tuning ONLY; no CAKE anywhere | The 07:52 build's `prepare()` prompt was skipped (no TTY), so `package()` fell back to the repo template, which defaulted `ENABLE_SQM=no`. Service "active (exited)" with status 0, root qdisc stayed `fq` (default), no `ifb4cake`, no ingress filter — bufferbloat test showed 103 ms download spikes with upload looking clean | The shipped template must default `ENABLE_SQM=yes` so an unattended build installs shaping, and the interactive prompt must default to Y (explicit "n" writes a disabled conf). A "successful" service run is not proof of shaping — verify with `tc qdisc show dev <iface>` (root `cake` AND `ingress ffff:`), `ip link show ifb4cake`, and `tc filter show dev <iface> ingress`. Fixed in pkgrel=2 |
| Installing a pkgrel-bumped kernel over the running one deletes the running kernel's module tree | `pacman -U linux-sleepy-...rc6-2` while `rc6-1` is running upgrades the package and removes the old version's `/usr/lib/modules/7.2.0-rc6-1-sleepy/`. The still-running `-1` kernel then has zero modules, so `modprobe ifb` fails silently and net-tune logged `ERROR - ifb4cake missing` | The `-1`/`-2` vmlinuz and modules are byte-identical, so the reboot is trivial — but it is **required**: the running kernel must match the installed module dir before any `modprobe`. "No reboot needed" only holds when the module tree for the running kernel stays valid; after any pkgrel bump, reboot before exercising module-dependent features |
| `git apply --check` passes but GNU `patch` (the prepare() tool) REJECTS the same patch — the reverse of the older lesson | The gfx12 IP-dump ordering fix (`4ef372319`) and the FFE defaults patch both passed `git apply --check` against the series tree but `patch -p1 --forward` (what `prepare()` actually runs) failed: git-apply tolerates offset/search where GNU patch is strict, and a hunk's leading `if (r)` context is ambiguous across sw_init's many error checks. Also 1127/1133 needed `execute_clk_mgr_block_sequence`/`notify_cstate_disable` context from LATER patches, so the source order had to be 1127→1128→1129 | **Always validate every candidate with the exact tool prepare() uses: `patch -p1 --forward --dry-run < patch`** against the series tree — not just `git apply --check`. When a patch's hunk context references symbols/fields another patch adds, that other patch MUST be numbered earlier in `source=()`. If a patch still won't apply under `patch` despite clean `git apply`, DROP it and document the reason (for example, 9025) rather than hand-forcing it |
| `git -C <repo> apply --check <relative-path>.patch` fails with "can't open patch" | `git -C` changes the process CWD to the repo, so a relative patch path is resolved against the repo, not your shell's directory — every candidate check seemed to "fail" until absolute paths were used | Use absolute paths (or `$PWD/` prefix) for the patch file with `git -C <repo> apply --check "$PWD/file.patch"`. The repo-root patch files are NOT inside the kernel tree |
| `git apply --check 2>&1 | head -3 && echo CLEAN` always prints CLEAN | The pipeline's exit status is `head`'s (0), masking git's failure — a false "it applies" signal that cost several prepare() iterations | Capture the REAL exit code: `git apply --check file > log 2>&1; echo "exit: $?"` and inspect `log`. Never trust `&& echo OK` after a pipeline |
| Mailing-list series extraction needs `git mailinfo`, not raw mbox bodies | Extracting a 14-patch series (retry-fault v3) from the monthly amd-gfx mbox: raw `[PATCH N/14]` message bodies are usable but the Subject can contain folded header newlines that produce broken filenames (embedded `\n`), and quoted replies pollute thread mboxes | Split the full monthly mbox (`repos/mailing-lists/amd-gfx-2026-July.mbox`), find the original `[PATCH n/N]` submissions by Message-ID prefix, run `git mailinfo <msgfile> <bodyfile>` per message, and reconstruct each patch with `From:`/`Date:`/`Subject:` headers. Name files `NNNN-short-desc.patch` with NO embedded newlines — sanitize the Subject before using it in a filename |
| A patch touching files absent from rc6 (for example, `dcn60_resource.c` = DCN6, a future die) makes GNU `patch` reject the whole hunk, while `git apply` may tolerate it | The Roman.Li FFE-defaults patch (39/41) touched dcn30–dcn42b + dcn60; rc6 has no `dcn60/` directory, so prepare() aborted on that hunk even though `git apply --check` was clean | When a ML/staging patch spans a file that does not exist in rc6, strip that file's hunks as a **documented backport adjustment** (remove the `diff --git` block + its stats line + fix the "N files changed" line), then verify with `patch -p1 --forward --dry-run`. Record the strip in PATCH_SOURCES.md |
| A `git apply --check`-clean patch can still FAIL TO COMPILE — apply-clean ≠ symbol-clean | 1025 (drm/amdgpu/gfx12 priv-fault user-queue recovery, drm-next `30f07c06`) applied cleanly to the rc7 series but the build died in `gfx_v12_0.c`: it references `adev->gfx.userq_priv_fault_work`/`userq_priv_fault_slots`, struct members that only exist via the gfx11 priv-fault worker infra landed in drm-next AFTER rc7 (`amdgpu_gfx.h` has only `userq_sch_*` in rc7) | The symbol-existence check must cover **struct members and helper functions the patch references, not just the files it touches**. Grep the referenced identifiers against the clean tree (`grep -rn "userq_priv_fault_work" repos/linux-7.2-rc7/drivers/gpu/drm/amd/`). If a member is added by an upstream prerequisite series absent from the base, DROP the patch and defer to the next version move — do not backport the whole prerequisite series in a bump |
| Editing a `.patch` file with substring-based Edit calls can corrupt its format | The Edit tool matches a bare substring inside a `+`-prefixed patch line, so a multi-line replacement inserts the NEW lines WITHOUT the leading `+` — they become context lines and the patch's added-line counts go wrong (the MARIE 0.9.3 concede-print edit did exactly this) | For structural edits to a patch file (adding/moving hunks), apply them with a **line-based Python script** that matches full lines including the `+`/`-`/space prefix (assert count==1 before replacing). Single-line in-place value changes (for example, `"0.9.2"`→`"0.9.3"`) are safe with Edit since the `+` stays. After ANY patch-file edit, re-verify with `patch --dry-run -Np1` against the series tree |
| Adopting an upstream version bump wholesale can REGRESS local fixes | The firelzrd LRU-MARIE 0.9.3 patch is based on 7.2-rc1 and reverted our `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` fix back to the old `(vm_flags & VM_EXEC)` API; it also restructures the `root_reclaim`/`lru_gen_shrink_node` `#ifdef` block | When bumping a carried patch's version, apply the **version delta** onto our already-series-adjusted patch rather than replacing it with the upstream tarball patch. For MARIE specifically: the 0.9.2→0.9.3 delta is the orphaned-L1-bit self-heal fix + `marie_dbg_orphan_bit[2]` counters + version string — keep our `vma_flags` fix and our block structure |
| A stray backgrounded shell holding the reference tree's git index lock blocks EVERY foreground `git checkout` on that tree for minutes | A backgrounded apply-loop's `git checkout -q -- . && git clean -qfd` on `repos/linux-7.2-rc7` grabbed the index lock and then wedged at 0% CPU; every later foreground `git apply`/`git checkout` in that repo blocked behind it, producing silent 2-minute tool timeouts that looked like patch slowness | Before diagnosing a "slow" git operation on the reference tree, check for stray processes (`ps aux | grep -E "zsh.*linux-7.2-rc7|git checkout"`) and kill them; check `.git/index.lock` in the tree. Prefer writing multi-step shell logic to a script file and running `bash /tmp/x.sh` over long inline loops, and always capture the real exit status (`set -o pipefail`) so a pipeline's last command doesn't mask a failure |
| Regenerating a revert-patch (`0106-cachy-drops`) with `patch -R` silently SKIPS hunks it can't reverse, leaving an inconsistent tree (a `goto` without its label → `undeclared label` build error) | Reversing the `0022` usbcore-quirk member of the fixes branch with `patch --reverse -f` (stderr discarded) dropped some config.c hunks — the build then failed with `use of undeclared label 'store_and_parse'` in `drivers/usb/core/config.c`. The off-target revert is only correct when it returns those files byte-identical to the pre-fixes baseline | Generate squashes and their reverts by **git diff between commits**, never by reverse-applying the source patches: commit the series baseline, commit the full branch application, then `git diff <baseline> <full> > 01xx-squash.patch` and `git diff <full> <baseline> -- <off-target-files> > 01xx-drops.patch`. Verify the net effect by applying the drops onto the full state and `git diff --quiet <baseline>` for every off-target file |
| Moving patches into subdirectories (`patches/<range>/`) without a build test | makepkg 7.1.0 resolves local `source=()` entries by **basename** in the PKGBUILD directory (`get_filename` strips the directory prefix, `get_filepath` checks `$startdir/<basename>`), so every `patches/0001-0049/NNNN-....patch` source entry was "not found in the build directory". `updpkgsums` and `makepkg` both fail. The pkg was built (22:53) BEFORE the refactor commit (23:09) — it was never build-tested | Run `updpkgsums` + a `makepkg` build after ANY repo-layout or `source=()` change, not just patch-content edits. `::` filename override and `file://` both break at extract, so keep patches in `patches/<range>/` folders AND let the PKGBUILD body auto-create root-level symlinks (`NNNN-*.patch -> patches/<range>/NNNN-*.patch`, gitignored) for makepkg's basename resolution — that is the working folder-layout pattern (2026-08-11) |

---

## 2026-08-10 hardware investigation: blackscreen + self-reboot root cause

`last -x` and the persistent journal revealed boot `e2839a9` (2026-08-09
16:29 → 21:36, 5 h) ended in a **silent hard reset**: journal stops abruptly
at 21:36:29 (user active on Steam/Spotify/Discord/hcaptcha), next boot at
21:37:12, no panic/shutdown/lockup output. `last` shows `crash` for that boot.
This is distinct from the display-death broken-pipe bursts seen at clean
shutdowns.

**Root cause (strong correlation): SMU driver/firmware IF version mismatch.**
Our RX 9070 XT (Gigabyte, sub 1458:2424, VBIOS `113-R907XTGOL-F2`) reports
`smu driver if version = 0x0000002e, smu fw if version = 0x00000033` — driver
speaks IF protocol 46, VBIOS-resident PMFW speaks 51 (5 minor versions apart).
This exactly matches drm/amd work-item **!5538** (same IF versions, same
`device lost from bus!` + SMU `response:0xFFFFFFFF` during power transitions,
began after a motherboard BIOS update). During an SMU power transition the GPU
drops off the PCIe bus → black screen → system hang. With `nowatchdog` in the
cmdline, kernel lockup detection is OFF, so the hang logs nothing and the
platform resets. No MCE errors logged (rules out CPU machine-check).

**This is NOT fixable by a kernel patch** (PMFW is VBIOS-resident, not
downgradable via linux-firmware). Actions: (1) check Gigabyte for a newer
RX 9070 XT VBIOS; (2) check motherboard BIOS; (3) remove `nowatchdog` so a
repeat produces a lockup log (or keep nmi_watchdog on while silencing the
boot-time clocksource message separately); (4) reduce SMU DPM transitions as a
stopgap (LACT `power_dpm_force_performance_level=high`); (5) file/bump a bug
against !5538. The patch-sweep skill now greps for this class every run.

### 2026-08-10 follow-up: full journal cross-check (log1.txt + log2.txt)

`log2.txt` is a `journalctl` export spanning Aug 05 → Aug 10 (grabbed via
`sudo journalctl` on Aug 10 07:54). `log1.txt` is the dmesg of a 7.2.0-rc6
boot. Cross-checking every incident window against the whole journal:

- **Recurrence is much higher than one incident.** COSMIC portal / Wayland
  `Broken pipe` + `SCTK dispatch error` bursts occur on Aug 05 23:36, Aug 06
  20:56, Aug 07 21:43, Aug 08 21:49, Aug 09 13:02, Aug 09 16:29, Aug 09 22:43 —
  seven events in six days, each = display connection died, then session
  teardown and (mostly) a reset/reboot.
- **The Aug 09 16:29→21:36 session died mid-activity.** Last journal lines are
  blocky DNS for Steam P2P discovery (21:36:26), hcaptcha (21:36:09), Spotify
  (21:36:29); journal stops at 21:36:29, next boot 21:37:12. **Zero kernel
  output at the crash instant**: no Oops, no MCE, no `amdgpu: GPU reset`, no
  ring/job/fence timeout, no SMU error, no soft/hard lockup. The journal simply
  ends → silent platform reset (matches the `crash` marker `last -x` reports).
- **Why it is silent:** `nowatchdog` on the cmdline disables the kernel lockup
  detector, so a hang can't emit `BUG: soft lockup` even if it wanted to.
- **Every boot logs three standing anomalies** (not crash-specific, but load
  bearing):
  1. `smu driver if version = 0x0000002e, smu fw if version = 0x00000033` —
     the !5538-class IF mismatch.
  2. `[drm] REG_WAIT timeout 1us * 150000 tries - optc401_disable_crtc line:237`
     — the DCN401 OPTC4 display controller stalls on a register wait at mode
     set, twice per boot. Shows this pipe can hang on its own; a display-pipe
     hang during a DPMS/VRR/modeset transition would black the screen exactly
     as observed, without touching any ring (hence no GPU-reset messages).
  3. `[drm] Failed to setup vendor infoframe on connector DP-2: -22` — vendor
     infoframe programming (HDMI VRR/ALLM/gaming) fails with EINVAL every boot.

**Conclusion:** the SMU IF mismatch remains the best-supported root cause for
the *reset itself* (matches !5538 byte-for-byte, incident timing tracks GPU
load: Overwatch/Steam/hcaptcha/YouTube), but the recurring OPTC401 REG_WAIT
timeout + vendor-infoframe failure mean a DCN401 display-pipe hang is a live
second candidate and the two are not mutually exclusive. Decisive next step is
still (3): **drop `nowatchdog`** so the next event leaves a lockup trace —
everything else (VBIOS/BIOS update, LACT `performance_level=high` stopgap)
stays. Sweep greps now cover `optc401_disable_crtc`, `vendor infoframe`, and
DCN4 OPTC/DPMS-hang fixes as a first-class class.

**New 2026-08-10 work-item-comment lead:** on !5538 an AMD engineer asked the
reporter to test `pcie.aspm=off` on the grub command line — ASPM on the dGPU
PCIe link is a candidate trigger for the bus-drop. Worth a controlled test on
our 9070 XT (Gigabyte B850 board) alongside the `nowatchdog` removal. The
display-stall class (!4753/!5203/!5571/!5320) is under active investigation by
AMD (FAMS2 + a `pp_dpm_mclk` sysfs fix `d81e52fc`, newer than rc7) — no merged
fix to backport yet; monitor via the GraphQL comment check each sweep.

---

## 2026-09-13: the display "box" root-caused: cosmic-comp overlay-plane scanout

**Symptom (as finally described precisely).** A rectangular artifact over
application windows. Decisive traits: it does **not** appear in screenshots; it
can be **dismissed by moving the cursor over it**; it appears on **one monitor
at a time**, moving to whichever monitor last had **VRR toggled**; and it
persists **regardless of the VRR state itself** (the *toggle*, not the mode,
matters).

**What was ruled out, with evidence.** All four connectors report `PSR support
0, sink PSR ver 0, DPCD caps 0x0`, so PSR/Replay cannot be involved. The `Failed
to setup vendor infoframe … -22` warning seen every boot is **benign** —
`drm_hdmi_vendor_infoframe_from_display_mode()` documents the EINVAL as *"safely
ignored"* for non-4K modes, and `hv_frame` is `memset` first. PSR, Replay, and
the infoframe warning were all red herrings that had previously been treated as
candidates.

**The misattribution to chase.** The August diagnosis in `PKGBUILD` was: on
DCN401, IPS/DPG pipe-gating makes `hubp2_is_flip_pending()` return false
(`hubp->power_gated`) while a flip is still pending, so the VUPDATE_NO_LOCK
handler delivers the flip event before hardware latches → the compositor
re-paints a buffer still being scanned → a fixed content-tracking square. That
was real and `dcdebugmask=0x800` did fix it in August — but the box **returned
with `0x800` still in effect**, so that was no longer the cause. (Leo Li's own
comment in `f64a9be56536` concedes the same gap: *"…DCN HUBP may be clock-gated,
so the flip-pending status may be undefined"* — AMD's fix is knowingly
unreliable there.)

**Root cause.** **`cosmic-comp` handing fullscreen content to an overlay
plane.** Two reproducible levers, both of which clear it:

| Setting (in `/etc/environment`, then re-login) | Effect |
|---|---|
| `COSMIC_DISABLE_OVERLAY_SCANOUT=1` | fixes the box on its own; the cursor can no longer take an overlay plane |
| `COSMIC_DISABLE_DIRECT_SCANOUT=1` | also fixes it, because it removes the overlay bit too |

Verified in the installed binary (`strings` on `/usr/bin/cosmic-comp`):
`COSMIC_DISABLE_DIRECT_SCANOUT`, `COSMIC_DISABLE_OVERLAY_SCANOUT`,
`COSMIC_DISABLE_CURSOR_PLANE`, `COSMIC_RENDER_DEVICE`. The binary also contains
the exact code paths that explain the traits — `skipping primary plane, no
damage`, `clearing previous direct scan-out on primary plane, damaging complete
output`, `Failed to switch primary-plane scanout flags`. **`modetest -M amdgpu
-p` was the key evidence**: all three overlay planes and all four cursor planes
were **inactive**, so COSMIC uses a **software cursor** composited into the
primary plane — which is precisely why moving the cursor generates damage and
clears a stale region, and why the artifact never reaches a screenshot (which is
rendered from the compositor's own pipeline, not the client buffer on an overlay
plane).

**Durable rules from this.**

1. **`modetest -M amdgpu -c -e -p` first** for any display artifact — which
   planes are actually live tells you which mechanism is even possible. (The
   user is in the `video` group, so no root is needed.)
2. **Trait-driven reasoning beats commit archaeology.** "Not in screenshots" +
   "cursor dismisses it" + "per-output" narrowed it to a userspace scanout path;
   no amount of reading DCN commits would have got there.
3. **A past fix that stopped working means the cause changed.** `0x800` working
   in August and failing in September was the signal to stop re-testing
   `dcdebugmask` bits (FAMS `0x20000` and clock-gating `0x8` were already ruled
   out in the `PKGBUILD` comment) and look elsewhere.
4. **Do not attribute a display artifact to the kernel just because the machine
   runs a custom kernel.** The box reproduced on stock kernels too — consistent
   with a compositor cause all along.

---

## Durable findings: moved out of `CLAUDE.md` (2026-09-13)

`CLAUDE.md` is loaded into every session; its budget is small. These are the
long-form versions of findings that are now one-line pointers there. **Read this
file before acting on any of them.**

### Patch-source access

- **lore.kernel.org git endpoints are NOT Anubis-gated** (only the web UI is):
  `git clone --mirror https://lore.kernel.org/<list>/<epoch>` works (for
  example, `lkml/20`, `rust-for-linux/0`); messages are commits, raw email is
  blob `m`.
- **The epoch digit is a time shard, not a list id** (2026-09-12). `/<list>/0`
  is the *oldest* shard, so a mirror of it can have its newest message years in
  the past while `refs/heads/master` still matches the remote — fresh-looking
  and silently useless (a full `netdev/0` mirror ended at 2017-11-02). Probe
  with `git ls-remote` and clone the **highest** epoch: netdev `0,1,2,3` (use
  `/3`), linux-fsdevel `0,1` (use `/1`), linux-mm `0,1,2` (use `/2`; `/0` ends
  2021). io-uring, linux-block, linux-nvme, linux-pm are `/0` only.
  `--shallow-since` fails **server-side** for `netdev/*` and `linux-fsdevel/*`
  (`error processing shallow info: 4`, reproducible) but works for the
  single-epoch lists; shallow-clone the highest epoch instead.
- **Match a Message-ID with an anchored header regex, never a substring match.**
  Searching a raw email for `20260911…` anywhere in the body also matches every
  *reply* that quotes it, so the file you extract is someone else's reply, not
  the patch. Use `rg -m1 -o '^Message-I[Dd]: <PREFIX[^>]*>'`. Note that `rg -E`
  means `--encoding`, not extended regex; the pattern above needs no flag.
- **Never `git format-patch` a lore mirror** (2026-09-13). In a lore mirror each
  *email* is a commit, so `format-patch -1 <sha>` produces a diff **of the email
  headers**, not the code — the file then contains DKIM/Received noise plus the
  hunk text as context. It fails to apply and `patch --forward` reports
  "Skipping patch", which reads exactly like *already applied* and produced
  three false "nothing to do" verdicts in one session. Extract the blob `m` and
  MIME-decode the body instead (Python `email`), as with quoted-printable mails.
  Real git clones (torvalds, linux-next, akpm-mm, drm-next) are fine — only the
  lore mirrors are message-per-commit.
- **GitLab: use the REST API, not a browser** (2026-09-12).
  gitlab.freedesktop.org is Anubis-gated for browser-like clients; headless
  Helium gets the challenge and cannot clear the PoW. Plain `curl` with **no
  User-Agent** works (~0.1 s). Code project = `agd5f%2Flinux`; `drm%2Famd` is
  the stale group mirror (master from 2025) — its only use is the issue tracker.
  No GitHub/kernel.org mirror exists. Endpoints:
  `/repository/{branches,commits}`, `/commits/<sha>/diff`,
  `/files/<path>/raw?ref=`.
- **Verify clones are FRESH before trusting a sweep** (2026-09-12). Stale and
  corrupt clones repeatedly produced wrong "nothing new" conclusions. Check the
  *remote-tracking ref you actually read* against the remote, not the local
  branch (`git rev-parse refs/remotes/origin/<b>` vs `git ls-remote <url>
  refs/heads/<b>`). **Shallow clones cannot always fast-forward** — `git fetch`
  reports success but the ref never moves; if the SHAs differ after a fetch,
  **re-clone** (`--shallow-since`, never `--depth=1`). A corrupt pack (`pack has
  N unresolved deltas`) also needs a re-clone. `gitlab.freedesktop.org` is
  intermittently unreachable — when it times out, cover drm content via
  `repos/linux-next` and retry later.

### Hardware traps

- **GC 12.0 ≠ GC 12.1.** Navi 48 (RX 9070 XT) is GC IP **(12,0,1)** → uses
  `gfx_v12_0.c`. `gfx_v12_1.c` is a *different chip* — amd-staging commits
  touching it are **not ours**. Check `IP_VERSION(12,0,x)` vs
  `IP_VERSION(12,1,0)` in `amdgpu_discovery.c` before adopting any gfx12 patch.
- **Never carry the DCN4 flip-schedule patches `9051`/`9052`.** AMD reverted
  both upstream (*"Because it causes some regression"*,
  `dml2_core_dcn4_calcs.c`, DCN4 = this GPU). They make the flip-bandwidth math
  more conservative and mis-schedule flips — the prime suspect for scanout
  artifacts.
- **`ld.mold` cannot link the kernel** — re-verified 2026-09-12 on mold 2.42.1:
  it rejects `OUTPUT_ARCH(...)`, `ENTRY(...)` and `SECTIONS{}` in `-T` scripts
  with `unknown linker script token`, and `arch/x86/kernel/vmlinux.lds` opens
  with `OUTPUT_ARCH`, so it fails immediately. An upstream mold limitation
  (partial ld-script support), not a local misconfiguration — there is no flag
  or workaround. Keep `ld.lld` (`LD=ld.lld`).

### Behaviour that silently does nothing

- **A `select`ed symbol cannot be disabled** by `disable_configs.py` — disable
  the selector instead, or accept the bloat; verify the built `.config`
  afterwards.
- **`scripts/config --set-str` on a symbol that no longer exists is silently
  dropped by `olddefconfig`.** Found twice: `MQ_IOSCHED_ADIOS` (no patch adds
  `block/adios.c` — the package advertised an `ADIOS-MODULE` it never shipped)
  and `DEFAULT_IOSCHED` (not a Kconfig symbol since the blk-mq rework; the
  effective NVMe scheduler actually comes from udev's `60-ioschedulers.rules`).
  Search the tree for the symbol with `rg` before trusting a `--set-str` or `-e`
  line.
- **LRU-MARIE makes MGLRU inert** (`lru_gen_enabled()` returns false while Marie
  owns aging), and **scx full-switch mode makes the CFS balance path inert**
  (`scheduler_tick()` gates `sched_balance_trigger()` behind
  `!scx_switched_all()`). Both mean carried MGLRU and `fair.c` patches earn
  nothing while those are active — check what actually owns the subsystem before
  crediting a patch with a win.
- **The live `prepare()` dry-run-gates every patch** and prints `SKIPPED:
  <reason>` for a miss, then deletes `.rej` files — so a past build tree with
  zero `.rej` does *not* prove every patch applied. Check the build output for
  `SKIPPED`, and still run the cumulative apply.
- **`0110-cachy-config-hooks.patch` applies only with fuzz** on rc2 — its
  `bus_lock.c` hunk carries `CONFIG_PROC_SYSCTL` context where rc2 has
  `CONFIG_SYSCTL`. `git apply --check` rejects it; `patch -p1 --forward -F2`
  accepts it. Harmless today, but exactly the trap above.

### Repository identity

- **There is exactly one package, and it lives in `sleepy-next/`**
  (single-package since 2026-09-12). Confirm with `rg -m1 '^_major='
  sleepy-next/PKGBUILD` and, for a built artifact, with `.BUILDINFO`'s
  `builddir`. A stale second patch tree used to exist at the repo root (174
  files for the dropped 7.2 package); applying it to a 7.3-rc2 base produced ~97
  spurious failures — the wrong series, not a broken one. If you see a large
  block of failures, check *which* tree you applied before concluding anything.
- **Build time is ~8 min** with the kbuild speedup series (`2300`–`2322`). A
  full rebuild is cheap — prefer rebuilding over guessing.

### The 240Hz flicker bisect (2026-09-14)

**Resolution (2026-09-15):** the flicker tracked the VRR advertisement after
all — not because VRR ran, but because of *which pass* set `freesync_capable`.
The MAG251RX EDID (dumped live from `/sys/class/drm/*/edid`, decoded with
`edid-decode`) has an **AMD VSDB v1** (48–240 Hz, MCCS flag 0xe6) and **no
HF-VSDB VRR** (`hdmi.vrr_cap.supported=0`). On rc3, upstream `cfdcf5571c31`
moved the MCCS clear inside `if (do_mccs)`; the later `do_mccs=false` pass
from `amdgpu_dm_connector_ddc_get_modes()` re-advertises
`freesync_capable=true` for HDMI sinks whose MCCS VCP does not answer. rc2 —
and therefore the clean cachyos-rc kernel — cleared unconditionally and stayed
at `vrr_capable=0`. Fix: patch `1164` reverts `cfdcf5571c31` (keeping 1163's
HF-VSDB exemption), matching cachy exactly. **The two-pass structure of
`amdgpu_dm_update_freesync_caps()` (hotplug `do_mccs=true`, then
`ddc_get_modes()` `do_mccs=false`) is itself the trap: the last writer wins,
and the second pass carries stale MCCS state.** When auditing this function,
always check what the *final* call in the sequence computes, not what the
first one computes. rc2→rc3 had zero DCN401/HUBP/clock-manager changes
(verified by log), and cachy's `7.3/fixes` branch is just series reverts +
`kzalloc_obj`→`kzalloc` style — so the MCCS two-pass was the only behavioural
display delta between the clean and broken kernels.

The MSI MAG251RX flickered at 1920x1080@240Hz on this kernel, worst under
cursor movement. The whole saga is a methodology lesson:

- **Two mechanistically compelling hypotheses were wrong.** First passive VRR
  (`PASSIVE_VRR_DISABLED=0` was read as "VRR holding the panel in
  variable-refresh mode"). The fix was verified in the live state — both CRTCs
  read `PASSIVE_VRR_DISABLED=1` — and the flicker persisted. Then
  `dcdebugmask=0x800`, which the user reported only reduced frequency ("less
  often"). **A mechanism that fits the observations is not a diagnosis; only an
  A/B result is.** State it that way in the changelog and the webhook: ship
  hypotheses labelled as such, and record the disproof rather than quietly
  moving on.
- **The decisive data was the user's A/B:** the stock cachyos-rc kernel
  (rc2-based) is clean at 240Hz; 144Hz also works on our kernel. With a known
  GOOD kernel and a known BAD kernel, bisect by *diffing the good kernel's
  state*, not by reasoning about the bad one. Capture from the good kernel:
  `/proc/cmdline`, all `/sys/module/amdgpu/parameters/*`,
  `modetest -M amdgpu -p/-c` CRTC + connector state, `pp_dpm_*` clock tables,
  and the embedded config via `scripts/extract-ikconfig /boot/vmlinuz-*`.
- **Configs can be diffed from vmlinuz on disk** even when the other kernel is
  booted: `repos/torvalds/scripts/extract-ikconfig /boot/vmlinuz-linux-sleepy-next`
  works on the stored image. Diffing our final config against the good kernel's
  showed the display driver config is identical apart from the cmdline and the
  NAP governor — which eliminated a whole class without a rebuild.
- **The first variable tested was `dcfeaturemask`:** the good kernel ran
  `amdgpu.dcfeaturemask=2`, ours `0x402` — the extra bit is `DC_FRL_MASK`,
  added by patch `1144` (Enable HDMI FRL by default). CachyOS reverted the same
  change twice in their 7.3 branches (`cc29db585c84`, `143e44f57bf8`, no reason
  recorded), and it is implicated in work item #5649. Three independent
  external signals outweighed the local argument that FRL enablement "should
  be inert" on an HDMI 2.0 sink. **Empirical alignment beats mechanism
  reasoning — this session proved it twice.**
- **If the flicker persists on the FRL-drop build, the next variable is the
  baked cmdline** (`cpuidle.governor=nap`). The NAP governor (patch 2200) is a
  1756-line neural-network idle predictor — the largest single behavioural
  difference from the good kernel's menu governor.
- **This machine cannot synthesise cursor movement** for reproduction:
  `CONFIG_INPUT_UINPUT` is unset and no cursor tool is installed. Consider
  enabling `CONFIG_INPUT_UINPUT=m` so a future display bug can be reproduced
  and bisected without the user at the desk.

### The "assumed superseded" trap (2026-09-14)

The 240Hz flicker's actual cause was a patch the rebase **dropped as
"superseded"**: `1145` (the `vrr_cap.supported` guard in
`amdgpu_dm_update_freesync_caps()`). rc3 rewrote that function, so the rebase
concluded the rewrite superseded the patch's purpose and dropped it. The
rewrite had restructured the code but kept the unguarded MCCS clear — and the
flicker-free CachyOS tree demonstrably carries the guarded version. The flicker
appeared exactly when the patch disappeared.

**Rule: "the base rewrote the function" is not evidence of supersession.** A
rewrite can preserve the bug a patch fixes while relocating it. Before dropping
a patch because its target moved, diff the NEW function against the version the
patch produces — or, faster, diff the new function against the same function in
a maintained distro tree (CachyOS here) and look for the patch's signature.
Only drop when the fix's behaviour is actually present, not when the hunk no
longer applies.

Also recorded from the same bisect: two mechanistically-plausible candidates
(1144 FRL-default, 0030 DET shrink) were each dropped and each **exonerated** by
user testing. Hypotheses are cheap; A/B tests are the only currency. And the
decisive data came from diffing the applied tree against a known-good kernel —
not from reasoning about the broken one.

## Userq kref series: two traps in one adoption (2026-09-15)

Adopting Zhu Lingshan's 10-patch userq lifecycle series surfaced two traps
that each cost a build cycle:

- **"Applies with git apply" is not the gate.** All ten patches passed
  `git apply --check` against our tree; the build then failed with
  `amdgpu_userq.c:877: use of undeclared label 'erase_doorbell'`. The
  authoritative check is the cumulative `audit_series.py` (GNU `patch -Np1
  --forward`), which caught the real problems: hunk context that our base's
  `r = amdgpu_userq_ensure_ev_fence(...)` assignment line broke (upstream
  context has no `r =`), and an error path our base has that upstream's does
  not (the doorbell is published before the eviction-fence setup here, and
  the mutex is already released on that path — the adaptation must detach +
  put + return, not unlock again).
- **Apply order is the numbering.** The series was numbered 1065–1074 and
  applied cleanly against the series-applied tree — but `source=()` applies
  the 9000s range *after* the 1000s, and these patches need the userq
  backports' context. The audit failed until the series moved to 9062–9071.
  Rule: a patch whose context depends on patches in a later-numbered range
  must itself live in that range.

Also recorded: when a new series touches code our backports already modified,
check every hunk against BOTH the clean base and the series-applied tree, and
read the callee's locking contract (`amdgpu_userq_ensure_ev_fence` releases
`userq_mutex` on failure) before writing the adaptation.

## Verification traps, 2026-09-15 (ThinLTO, `| head`, /tmp)

Three checks in one session produced **false negatives** — each looked like a
clean result and none was. All three are the same mistake in different clothes:
treating an empty result as a finding.

- **ThinLTO objects are bitcode, not machine code.** `objdump -d mm/vmscan.o`
  and `llvm-objdump -d kernel/sched/fair.o` print nothing because the files are
  LLVM IR (`file` says "LLVM IR bitcode"). Disassembling them cannot answer any
  question about generated instructions — only the linked `vmlinux` can, and it
  must be disassembled *after* the LTO backend has run.
- **`cmd | head -3 && echo OK` always prints OK.** GNU `head` exits 0, so the
  `&&` branch runs regardless. It reported "APPLIES" for a patch whose path was
  wrong. Capture the exit status of the real command (`cmd > log 2>&1; echo $?`),
  never of a pipeline that ends in `head`.
- **`/tmp` is cleaned between sessions.** A vmlinux extracted an hour earlier was
  gone, so `objdump -d /tmp/vmlinux-rc3-10 | rg ...` returned zero matches and
  looked like "no AVX in the kernel". Re-extract and confirm the file exists
  (`ls -la`) before drawing a conclusion from a disassembly or a scan.

The corrected finding, for the record: this kernel contains 3,089 `ymm`/`zmm`
instructions, **all** of them in 27 deliberate vector functions — the x86 crypto
assembly (poly1305, chacha, sha1/sha256/sha512, crc32/crc64 AVX2 and AVX-512)
and the NAP governor's AVX2 neural-network predictor. None are compiler
spillover into generic code. To map instructions to functions, disassemble the
**running** kernel's image (`/boot/vmlinuz-*` → `extract-vmlinux` →
`objdump -d`) and map addresses through `/proc/kallsyms`, which needs
`kernel.kptr_restrict=0` for the duration of one `cat` (restore it immediately —
and note the extracted file must be `chmod 644` after a `sudo cp`).

## Two unmerged series in one hot path (2026-09-15)

The sweep surfaced Kefeng Wang's "zswap: optimize zswap invalidate and store"
v3, which applies cleanly to this tree and is squarely on-target now that zswap
backs the swap stack. It was **not** adopted, and the reason is worth keeping:
it rewrites `swap_range_free()` in `mm/swapfile.c`, which is the same function
Baoquan He's xswap series (`2155`–`2166`) rewrites. Both are review-stage series
that will change again before they land.

Two unmerged series composing in the swap hot path is precisely the shape of the
240 Hz flicker: several plausible patches interacting in one subsystem, with the
interaction invisible to `git apply`. **Rule: adopt one unmerged series per
subsystem per cycle.** Wait for the bump, by which time at least one of them is
usually merged and the other rebases onto it.

## The 7.4 bump will re-enable HDMI FRL by default (2026-09-15)

`af6139855b55` ("Enable HDMI FRL by default", in amd-staging, targeted 7.4) sets
`DC_FRL_MASK` in `amdgpu_dc_feature_mask`. That is the exact variable the
flicker bisect turned on twice and off once: `1144` set the same mask, was
dropped as the first bisect step, and the clean comparison kernel ran
`dcfeaturemask=2` while ours ran `0x402`. When the 7.4 bump happens, re-test the
MAG251RX at 1920x1080@240 Hz **before** installing, and expect to either drop
the FRL default again or re-bisect. Fangzhi Zuo's FRL patches 61/66 and 65/66
in Chenyu Chen's DC 3.2.398 series sit on the same code.

## linux-next tags are rebased daily; `git log A..B` between them is a lie (2026-09-15)

`git -C repos/linux-next log --oneline next-20260914..next-20260915` returns
**1,473,514 commits**. The tags are daily integrations rebased onto fresh bases,
so the "commits in B but not A" set is essentially every subsystem branch, not
the day's delta. The adjacent `git diff --stat` is fine (737 files) because it
compares trees, not history.

The failure mode is nasty because it does not error: piping that log through
`rg` for keywords yields a plausible-looking list of "new" commits, and they are
not new — they are the same subsystem work every day. One sweep agent produced a
confident delta from it; another caught it. **Use `git diff` for content and the
tag's own merge commits for attribution.** The same applies to any tree that
rebases (linux-next, amd-staging, distro -next branches): ancestry between
snapshots is not meaningful, only content is.

Related: `repos/linux-next`'s `master` branch is stale (2026-08-03) while the
tags are current — check `git -C repos/linux-next describe --tags <ref>` before
trusting any ref in that clone.

## Half a series is worse than none (2026-09-15, patch 2142)

`2142` was adopted as a single patch from Xueyuan Chen's 4-part series "avoid
large folio splits when swap is unavailable". It is part **3/4**. Parts 1/4 and
2/4 — which introduce `page_counter_margin()` and the `0`/`-E2BIG`/`-ENOSPC`/
`-ENOMEM` return classification for `folio_alloc_swap()` — were never taken.

3/4 gates the large-folio split fallback in `shrink_folio_list()` on
`ret != -E2BIG`. With nothing in the tree returning `-E2BIG`, that condition was
always true, so **every** swap-allocation failure took the "do not split" branch
and the THP/mTHP swapout fallback became unreachable. The patch did the exact
opposite of its stated purpose, and it made reclaim worse than stock. It
applied cleanly, compiled, ran, and appeared in no log.

**Rule: a patch that is *part* of a series must be checked for its siblings
before adoption, not just for whether it applies.** Concretely:

```bash
# what does this patch assume already exists?
rg -n 'E2BIG|page_counter_margin' sleepy-next/patches/<range>/<the patch>
rg -n 'E2BIG|page_counter_margin' repos/torvalds/mm/ repos/torvalds/include/linux/
```

If the patch tests for a value, a symbol, or a state that nothing in the tree
produces, the patch is either inert or — worse — latched into a branch it was
never meant to take. The cumulative apply cannot catch this: the patch applies
perfectly.

Found by a sweep agent reading the patch *and* grepping the tree for its
contract, then confirmed by hand: `rg -c E2BIG mm/swapfile.c mm/swap.h
mm/vmscan.c` returned nothing on a tree that had been running the patch for
days.

## A unit that waits is not the unit that gates (2026-09-15)

Three boot analyses agreed the 14.7s userspace time was a DHCP wait and then
disagreed about why it reached `multi-user.target`. `systemd-analyze
critical-chain` caused the disagreement:

```
$ systemd-analyze critical-chain timers.target
timers.target @14.686s
└─cachyos-rate-mirrors.timer @14.686s
  └─network-online.target @14.685s
    └─NetworkManager-wait-online.service @2.339s +12.346s
```

That reads as: the CachyOS rate-mirrors timer holds `basic.target`, which holds
`multi-user.target`, which holds the desktop — a packaging bug worth reporting
upstream. It is wrong. `basic.target` is `After=timers.target`, and on the same
boot:

| unit | `ActiveEnterTimestampMonotonic` |
|---|---|
| `basic.target` | 6883384 (6.88s) |
| `NetworkManager.service` | 7213319 (7.21s) |
| `timers.target` | 19563507 (19.56s) |
| `multi-user.target` | 19597845 (19.60s) |

`basic.target` cannot be ordered after `timers.target` and also be active 12.7s
earlier. The declared ordering exists but was never honoured: systemd found the
cycle `basic.target → timers.target → cachyos-rate-mirrors.timer →
network-online.target → NetworkManager-wait-online → NetworkManager →
basic.target` and **deleted one edge to break it** — silently, with no
"ordering cycle" journal line (that message appeared only for the separate
`tmp.mount`/`xswap-create` cycle). `critical-chain` then printed the declared
chain as if it had been followed.

**Why it matters:** the two candidate causes have opposite fixes. If the timer
gates, you edit the timer. If `net-tune.service` and `blocky.service` gate —
both were `WantedBy=multi-user.target` with `After=network-online.target` — you
move those two and leave the timer alone. Acting on the chain output would have
produced a wrong upstream bug report and a drop-in that changed nothing.

**Telling a cause from a victim:**

- Compare **raw** `ActiveEnterTimestampMonotonic` (µs since boot) for the
  suspect against the unit it supposedly holds. If the timestamps contradict the
  declared edge, systemd broke the edge and the unit is a victim.
- `critical-chain` prints *declared* edges. Cross-check every conclusion against
  `systemctl show <unit> -p After` **and** the timestamps.
- `blame` attributes time to the unit that spent it, not to the unit that waited
  on it. `NetworkManager-wait-online.service` says `12.346s`; the units that made
  that matter were the ones in `multi-user.target.wants` ordering after
  `network-online.target`.
- The decisive question is not "what does X wait for" but **"does anything on
  the boot path wait for X"**. Check `systemctl show X -p Before`: if it is empty
  and X is not `WantedBy` a target the boot waits for, X is off the path however
  late it starts.

**Corollary: an empty `After=` in a drop-in does not reset the ordering list.**
The obvious fix — `After=` under `[Unit]` on `cachyos-rate-mirrors.timer` — was
written, `daemon-reload`ed, and measured: `After=` still reported
`sysinit.target network-online.target -.mount time-set.target time-sync.target`,
and `systemctl cat` confirmed the drop-in was read with no parse error. Never
assume a reset took; query the unit after reloading. The drop-in was reverted
rather than left in the tree doing nothing.

## `sudo -S` eats the first line of a heredoc (2026-09-15)

```bash
echo 'pw' | sudo -S tee /etc/foo.conf >/dev/null <<'EOF'
[Unit]
After=
EOF
```

The heredoc **replaces** the pipe as `sudo`'s stdin, so `sudo -S` reads `[Unit]`
as the password. Authentication fails, but the redirection still leaves a file
behind — and with line 1 gone the remainder parses as stray assignments. systemd
said so plainly (`Assignment outside of section. Ignoring.`) while the drop-in
silently did nothing, which is how a config file that does not work got
installed twice.

Write the file with the Write tool and `sudo install -m 644` it, or use `sudo -S`
only where stdin genuinely is the password. Same family as the `rg -rn` and
`pkill -f` traps: the convenient-looking shell construct is the one that quietly
changes what the command means. `pgrep -af <pattern>` self-matches the invoking
shell exactly like `pkill -f` — `pgrep -x <name>` is the form that does not.

### Second occurrence, different spelling (2026-09-16)

A pipe into `echo` looks harmless and is not — `echo` ignores its stdin, so
anything piped into it is silently discarded and `echo`'s own output becomes the
next stage's input:

```bash
printf '[Journal]\nSystemMaxUse=500M\n' | echo 'pw' | sudo -S tee /etc/foo.conf
```

The `printf`'s content goes nowhere, and `tee` writes **the password** (9 bytes)
into a system config file. This actually happened, to
`/etc/systemd/journald.conf.d/00-size.conf`, and was caught only because the
resulting config was checked for effect and reported `SystemMaxUse=50M` — the
old value — which is what sent me back to look at the file.

Two rules, both cheap:

- **Never mix a data-producing pipe with `echo <secret> |` in one pipeline.**
  They compete for the same stdin and the loser is silent. Use the Write tool
  and `sudo install`, as above.
- **After writing any config, verify the value is in effect**, not that the
  command exited 0. `systemd-analyze cat-config`, `sysctl -n`, `systemctl show`
  — a file that exists and is syntactically valid can still contain the wrong
  thing entirely.

## `tar rf` on a `.tar.gz` destroys the archive (2026-09-16)

A backup archive was built with `tar czf`, then added to later with `tar rf`.
`rf` appends to an **uncompressed** tar; pointed at a gzip file it discards the
compressed stream and rewrites the file as a plain tar. The result:

- The five config files originally archived were **gone** — the gzip magic
  (`1f 8b`) was not anywhere in the file, so nothing was recoverable from it.
- `file` reported `POSIX tar archive (GNU)`, i.e. the `.tar.gz` extension lied.
- It failed silently. Nothing warned at append time; the corruption only
  surfaced on the next `tar tzf`, by which point the source files had already
  been deleted.

**Appending to a compressed archive is not a thing.** To add to one, unpack it,
add the files, and re-create it:

```bash
mkdir -p /tmp/rebuild && tar xzf arch.tar.gz -C /tmp/rebuild
# ... copy the new files in ...
tar czf arch.tar.gz -C /tmp/rebuild .
```

Two habits that would have caught it:

- **`tar tf` (no `z`) on a `.tar.gz`, or `file` on it, right after writing it.**
  The archive here was created, appended to twice, and never re-listed.
- **Archive *before* deleting, and confirm the archive reads back first.** Here
  the `rm` ran in the same command block as the append, so a failed append could
  not stop the delete. Sequence those separately.

The lost files were dead config that had been removed deliberately, and the
archive was rebuilt with a `README` recording which entries are byte-exact and
which are reconstructed — but only because every one of them happened to appear
verbatim in the session log. That was luck, not a process.

## Attribute a kernel warning by boot, not by reasoning (2026-09-16)

`mem_cgroup_update_lru_size(): lru_size -2522` was firing once per boot in a tree
carrying 217 patches, most of them in mm. Reading the call path was enough to see
the function was **upstream** — `lru_reparent_memcg` lives in `mm/folio.c` and
appears in no patch of ours — and that is exactly where the reasoning would have
stopped, concluding "not ours". The wrong conclusion.

The attribution that holds up is per boot:

```bash
journalctl --list-boots | while read -r id rest; do
  id=$(echo "$id" | tr -d ' ')
  k=$(journalctl -b "$id" -k | rg -o 'Linux version [0-9][^ ]*' | head -1)
  w=$(journalctl -b "$id" -k | rg -c 'lru_size -')
  printf '%s %s warns=%s\n' "$id" "$k" "${w:-0}"
done
```

Every `sleepy-next` boot reported it from rc3-6 through rc3-16; neither
`cachyos-rc` boot did. Same upstream code, different result — so the delta is
ours, and the delta is what matters, not the provenance of the function that
printed the line. **Keep a second kernel installed and boot it occasionally: it
is the only control group this project has**, and it is what turned "probably
fine, upstream warns sometimes" into "we take the classic-LRU branch and
mis-account because of it".

**`WARN_ONCE` hides frequency.**

```c
if (WARN_ONCE(cond, "fmt", ...)) {
    VM_BUG_ON(1);
    *lru_size = 0;
}
```

The *print* happens once per boot; the branch body runs every time the condition
holds. So "one warning per boot" is a lower bound on how often the kernel is in
that state, and a silent `*counter = 0` recovery firing N times is a worse
symptom than the single line implies. Never read a `WARN_ONCE` count as an
occurrence count.

Check the guard too: `VM_BUG_ON(1)` is a no-op unless `CONFIG_DEBUG_VM`, so the
same condition that warns politely here is a hard `BUG()` on a debug build. Know
which one you have before calling something "just a warning".

## A stray line in a PAM config makes a password a log line (2026-09-16)

`/etc/security/faillock.conf` had the user's sudo password as its first line.
`pam_faillock` parsed it as an option, did not recognise it, and **logged it on
every authentication in every PAM stack** — `sudo`, `login`, `greetd`,
`cosmic-greeter`. 226 copies in the persistent journal before anyone noticed:

```
pam_faillock(sudo:auth): Unknown option: <the password>
```

The config file had done nothing for two weeks except leak. Two lessons:

- **A secret in a config file is also a secret in the logs of anything that
  parses that file.** Config parsers print unrecognised input, and PAM parsers
  print it on every auth. `rg -l '<secret>' /etc` is the check worth running
  after any config mishap — it is one command and it is what found this.
- Removing the line stopped it immediately; the *existing* log entries are a
  separate job (`journalctl --rotate && journalctl --vacuum-time=1s`). Fixing
  the source and clearing the history are two different actions, and only the
  first is safe to do without asking.

## `pacman -Qkk` is the sfc/DISM equivalent, and its output needs reading (2026-09-16)

There is no `sfc /scannow` on Arch; the equivalent is verifying installed files
against the package digest database. Use two independent tools — they read
different fields and agreeing on the total is the point:

```bash
sudo pacman -Qkk      # mtree: size, mtime, permissions, SHA256
paccheck --quiet      # independent implementation, md5
```

`pacman -Qkk` **does** verify checksums on this version (7.1.0), so a real
content change shows up as `SHA256 checksum mismatch`, not just a size or mtime
diff.

Almost everything it reports on a lived-in machine is not damage. Read the
prefix before panicking:

| Output | Means |
|---|---|
| `backup file: <pkg>: /etc/...` | pacman marks these user-editable; differing is *correct* |
| `(No such file or directory)` under `/usr/share/locale`, `man`, `help`, `X11/locale` | a cleaner removed translations/docs; the DB still lists them |
| `(Permissions mismatch)` on `/boot` | the fstab mount option (`umask=0077`), not the package |
| `(File type mismatch)` on `/etc/resolv.conf` | it is a symlink to systemd-resolved's stub, by design |
| checksum mismatch on one obscure file | read it — here it was the stock Garuda terminal launcher, wired to nothing |

**Deleting translations is not free, even though it looks free.** The filesystem
and the package database stop agreeing, so every future integrity check reports
the same 6,679 files and a real finding has to be picked out of that noise
every time. If a cleaner is going to strip locales, set `NoExtract` in
`pacman.conf` so the database records the intent and `-Qkk` stays meaningful.

**A clean integrity result says nothing about hardware.** Run `smartctl -H` and
read the superblock too (`tune2fs -l` for ext4): state, error count, and whether
a periodic check is even scheduled (`Maximum mount count: -1` means it is not).

## A flag that does nothing, and a report that is not a cause (2026-09-16)

Two findings from one boot audit — the same mistake wearing different clothes.

**`nowatchdog` has been on the kernel command line for months, doing nothing.**
The kernel says so on every boot, in a line nobody reads:

```
Unknown kernel command line parameters "nowatchdog", will be passed to user space.
```

`CONFIG_SOFTLOCKUP_DETECTOR` and `CONFIG_HARDLOCKUP_DETECTOR` are both unset, so
there is no lockup detector for the parameter to disable. And the watchdog that
*is* running — `CONFIG_CLOCKSOURCE_WATCHDOG=y`, an unrelated mechanism — was never
controlled by `nowatchdog` at all.

**Check that a tunable exists before believing something is tuned.** A cmdline
flag, a `--set-str` against a symbol that no longer exists, a sysctl written by a
vendor file for a kernel that lacks it: all silent. The kernel *does* warn about
unknown cmdline parameters. It is one line at `[0.023]`, it says "will be passed
to user space", and it reads like noise. It is not noise.

**A log line that appears at the end of a stall usually reports it, not causes
it.** `Watchdog remote CPU 4 read timed out` sits 159 ms into the unexplained
initrd gap and looks like a free 159 ms:

```c
static void watchdog_handle_remote_timeout(struct clocksource *cs)
{
	pr_info_once("Watchdog remote CPU %u read timed out\n", watchdog_data.curr_cpu);
```

It runs from `schedule_work(&watchdog_work)` — a workqueue on its own schedule —
and prints *after* the read that was already slow. The stall is the cause; the
line is the receipt. Disabling the watchdog would delete the receipt and cost
TSC-instability detection, which this project's A/B methodology depends on.

Same shape as *"A unit that waits is not the unit that gates"* above: the thing
that *mentions* a problem is rarely the thing that *is* the problem. Ask what had
to be true for the message to be printed, not merely what printed it.

## "Is it in the base?" is not a duplicate test (2026-09-16)

A sweep surfaced `848d2ce2fce1` (`mm: filemap: retain mapped dropbehind folios`).
The check that mattered — `git merge-base --is-ancestor <sha> v7.3-rc3` — said
**no**, correctly. The patch is a real fix. It was staged as `2176`, documented,
given a checksum, and queued for the build.

It was **already in the series as `2141`**, byte-identical, and had been for
days. The build caught it and nothing else did:

```
Applying patch 2176-mm-filemap-retain-mapped-dropbehind-folios.patch...
  SKIPPED: does not apply cleanly
```

GNU `patch` explains itself in the dry-run log — `Reversed (or previously
applied) patch detected!` — but `prepare()` prints only `SKIPPED`, and a skipped
patch is not a failed build. It is a **silent no-op**: the tree still compiles,
the package still installs, and the only trace is one line in a log nobody
re-reads.

**Why every pre-adoption check passed.** `git apply --check` and
`patch --dry-run` are only meaningful against a tree that already contains the
whole series. The audit worktree at `repos/_audit` was created from an *earlier*
series state, so it did not contain `2141` — the patch applied beautifully to a
tree that was missing the thing it duplicated. **A stale reference tree turns a
duplicate into a clean apply.**

Three rules follow:

1. **Compare against the series, not the base.** Duplicate detection is a hash
   scan over the diff bodies of every patch in `source=()`, with `index` and
   `similarity index` lines stripped (the blob hashes differ between
   regenerations even when the code is identical). One `python3` loop over
   `sleepy-next/patches/*/*.patch` finds this class in a second.
2. **The authoritative check is the build's own dry-run, in series order.** It
   is the only thing that runs against the real tree in the real order. Read the
   `SKIPPED` count out of every build log; do not assume a clean build means
   every patch landed.
3. **Rebuild the audit worktree after the series changes.** `rm -rf repos/_audit`
   before `audit_series.py --keep`. A worktree kept from a previous cycle is
   worse than no worktree, because it answers questions confidently and wrongly.

The vacated number stays vacated — `2176` is a gap, like `2401`, `2402` and
`2501`. Renumbering would erase the evidence that something was tried and
rejected.

Related: *"Half a series is worse than none"* above is the same failure seen from
the other side — a tree that is missing a prerequisite makes an inert patch look
effective. Both are the cost of testing against a tree that is not the real one.

## Every clone here is shallow, so `merge-base --is-ancestor` lies (2026-09-16)

The standard "is this patch already in our base?" test was written into the
sweep instructions as:

```bash
git merge-base --is-ancestor <sha> v7.3-rc3   # WRONG in this repo
```

**It is wrong, and it fails silently in the direction that looks like a finding.**
Every clone under `repos/` except `pixelcluster-kernel` is shallow — `torvalds`
has 162 graft points, `linux-next` 560, `drm-misc` 471, `zen-kernel` 481. In a
shallow clone git cannot walk past the grafts, so ancestry queries return
"not an ancestor" for commits it simply cannot see.

The sanity check that exposes it — and the reason to always run one:

```
c84bf6dd2b83  2025-05-09  -> "not an ancestor of v7.3-rc3"
2fbb0c10d1e8  2022-02-14  -> "not an ancestor of v7.3-rc3"
```

Two commits from 2025 and 2022, reported as not ancestors of a 2026 tag. They
obviously are. **Before trusting any ancestry answer, test it against a commit
whose answer you already know.** A primitive that cannot be wrong in your favour
is worth ten minutes of calibration.

The failure mode is nasty because it inflates the candidate list rather than
emptying it: ancient, long-merged code is reported as novel, and each false
positive costs a manual rejection. It also almost hid a real one — `mmap_prepare`
was reported absent from the base, but `v7.3-rc3:mm/vma.c` contains 14 references
to it, which is how we know `2145` and `2146` are live fixes and not inert.

**The two tests that do work** are content-based, and neither needs ancestry:

- **Already carried?** Search `sleepy-next/patches/*/*.patch` for the sha in a
  `From <sha>` line *and* for a matching `Subject:` line; grep `PATCH_SOURCES.md`.
- **Bug present in the base?** Read the file at the tag:
  `git -C repos/torvalds show v7.3-rc3:<path> | rg '<symbol>'`. If the code the
  patch repairs is there, the bug is live.

Applicability is settled the same way it always was: `patch -p1 --forward
--dry-run -F2` against a worktree carrying the full series. Neither a bare
`v7.3-rc3` tree nor a stale worktree will do — see the entry above.

## A crashed command and an empty result look identical (2026-09-16)

Mid-sweep, `dmesg` showed 23 `zsh` coredumps in three minutes. This looked like
a kernel regression and was not one. The crashing processes had been spawned by
an automated sweep command, and the backtrace was entirely *inside zsh* —
`getoutput -> execode -> execlist -> prefork`, with `sp` equal to the faulting
address (`SEGV_MAPERR`). The captured command line was a `for` loop built with
pathological nested escaping (`\'"\'"\'%H\'"\'"\'`), and the escapes are what
blew zsh's stack. `zsh -c 'echo ok'` worked every time.

Two things worth keeping:

**Diagnose a segfault by the backtrace, not the count.** `sp == fault address`
with symbol-free frames *inside the interpreter* says userspace, and says the
interpreter is recursing too deep. A kernel-side stack fault would have taken
out more than one program, and simple invocations would fail too.

**The real hazard is the silence afterwards.** `git log ... | wc -l` in a shell
that segfaults prints `0`. A crashed sweep and a clean "nothing to report" are
the same three characters. Any sweep step that returns a *negative* result — no
candidates, no new commits, zero matches — has to be re-run cleanly before it is
believed, because the failure mode of the tool and the failure mode of the
question are indistinguishable.

The fix is to stop generating deeply-escaped one-liners: write the loop to a file
and run it with `bash <file>`, so there is no quoting layer at all.

## A carried patch does not carry its upstream subject (2026-09-18)

Sweeping the `v7.3-rc3`..`master` window produced a candidate list, and each
candidate was marked already-carried or not by searching the series for the
upstream commit subject:

```bash
key=$(git -C repos/torvalds log -1 --format='%s' "$sha" | sed 's/^[a-z0-9_/,. -]*: //')
rg -l -F "$key" sleepy-next/patches/
```

Four of the "not carried" results were wrong. `1587d3394`
(`x86/alternatives: Exclude text poking against change_page_attr()`) is carried
as `2507-x86-alternatives-exclude-text-poking-vs-cpa.patch`, whose subject
reads `x86/alternatives: Exclude text poking vs CPA`. The same held for
`e14a34548` (`2146`), `93d88ac4a` (`2405`) and `9a0b159ff` (`2410`).

**A patch filed here keeps its authorship and its diff but not always its
subject.** Subjects get shortened when a patch is rebuilt from a lore mirror,
adapted to this tree, or squashed out of a series, so absence of the upstream
subject string proves nothing. The `rg` was answering "is this exact sentence
in the series?" and being read as "is this change in the series?"

**Reverse-applicability is the test.** Against the series-applied tree:

```bash
patch -d repos/_audit -R -p1 --batch --forward -F2 --dry-run < cand.patch
```

No `FAILED`/`ignored`/`No file` means the tree already contains exactly those
changes. It asks the tree directly, is immune to subject drift, and also
catches a candidate that is *partly* present — which is what `7891fbb95` and
`f9abcb602ef3` turned out to be.

Two corollaries. A forward dry-run alone cannot classify a candidate: it fails
both for "not carried, context shifted" and for "already carried", and those
need opposite responses. And the series tree has to be rebuilt for the current
series state before any of this — see *"Is it in the base?" is not a duplicate
test* above for why a stale `repos/_audit` answers confidently and wrongly.

Related: *"A crashed command and an empty result look identical"* above. That
one is a search that returns nothing because it broke; this one is a search
that returns nothing because it asked the wrong question. Both read as "no
candidates".
## A guard one level too high: `do_swapout()` walks around it (2026-09-20)

Two kernel threads — `kcompressd0` and `kswapd0` — died of the same NULL
dereference at `mempool_alloc_noprof+0x9a`, both from `swap_add_folio()`. After
it the machine had **no `kswapd` at all**; reclaim ran direct-only until reboot.

### The two halves that don't meet

**Half one: `sio_pool` is never allocated on an xswap-only machine.**
`swap_add_folio()` allocates its batching context from a global pool:

```c
	ctx->sio = sio = mempool_alloc(sio_pool, GFP_NOIO);
```

`sio_pool` is initialised by `sio_pool_init()`, which has **exactly one caller
in the entire tree** — `setup_swap_extents()` in `mm/swapfile.c`, reachable only
from the file/block `swapon()` path.

xswap devices are created through `/sys/kernel/mm/xswap/create`, which the patch
explains: *"xswap devices have no backing storage, so there is no file to
swapon."* `xswap_create()` builds the `swap_info_struct` by hand and never calls
`sio_pool_init()`. So on a machine whose only swap is xswap, `sio_pool` is NULL
for the whole uptime.

**Half two: the guard that would keep xswap out of that code sits too high.**
The xswap patch does add a guard — in `swap_writeout()`:

```c
	if (unlikely(__swap_entry_to_info(folio->swap)->flags & SWP_XSWAP)) {
		folio_mark_dirty(folio);
		return AOP_WRITEPAGE_ACTIVATE;
	}
	__swap_writepage(ctx, folio);
```

That covers stock reclaim, which reaches the write path through
`swap_writeout()`. It does **not** cover MARIE's `do_swapout()`:

```c
static inline void do_swapout(struct swap_io_ctx *ctx, struct folio *folio)
{
	if (zswap_store(folio)) {
		...
	} else
		__swap_writepage(ctx, folio);   /* straight past the guard */
	folio_put(folio);
}
```

`do_swapout()` calls `__swap_writepage()` directly. The guard is one level
above, in a function this path never enters.

### Why both oopses look like different callers

`do_swapout()` has two callers, both reaching it from kswapd:

| Oops | Reported caller | Actual path |
|---|---|---|
| #1 `kcompressd0` | `kcompressd` | kthread → `do_swapout_batch()` → `do_swapout()` |
| #2 `kswapd0` | `swap_writeout` | `swap_writeout()` → **inlined** `kcompressd_store()` → `do_swapout()` |

`kcompressd_store()` is `static` and gets inlined into `swap_writeout()`, so the
unwinder names `swap_writeout` for a frame that is really MARIE's code. Both
oopses are one bug reached by two routes, which is why they share a faulting
instruction and register set (`R14`/`RDI` = 0, `CR2` = 0x18, `RSI` = `0xc00`).

The trigger is zswap refusing a page — pool at its limit, or incompressible
content. `zswap_store()` returns false, and the fall-through lands on
`__swap_writepage()` → `swap_add_folio()` → `mempool_alloc(NULL, GFP_NOIO)`.

### The fix

Apply the same guard in `do_swapout()`, respecting *its* locking contract —
`do_swapout()` owns the unlock on every branch, so the guard unlocks before the
`folio_put()` that follows, where `swap_writeout()` leaves the folio locked for
an `AOP_WRITEPAGE_ACTIVATE` retry.

Carried as `2199`. The deeper shape of the problem is that the guard lives in a
*caller* rather than at the choke point: `__swap_writepage()` is what both paths
share, and a guard there could not be bypassed by any future caller.

### The rule

**A guard placed in one caller of a shared callee protects only that caller.**
The xswap patch guarded `swap_writeout()` because that was the write path it
knew about. MARIE had added a second one, in a patch that applies *before* it,
so neither patch's author saw the other's entry point.

Two patches touching one subsystem is normal here — 2100-2199 alone has MARIE,
xswap, zstd and gup. When one adds a guard, the question is not "does this cover
the path I know" but "how many ways is this function reached":

```bash
rg -n 'the_function_being_guarded\(' mm/ | grep -v '^\./mm/.*:\s*\*'
```

### Correction: read the applied tree, not the patch text

An earlier pass at this concluded the series was *missing* the guard — that v2
had dropped what v1 had. That was **wrong**; the guard is present and
byte-identical to upstream v3.

The error came from grepping *patch files* and reading hunks in isolation:

- `rg -c 'sio_pool_init' <patch>` matched a **context line** in v1's
  `setup_swap_extents()` hunk, not a call the patch added. "v1 has it, v2
  doesn't" was an artefact of where a context line landed when the code was
  relocated to a different file.
- The guard was read from a hunk of `2155` without checking it survives to the
  end of the series.

```bash
python3 .claude/skills/kernel-build/scripts/audit_series.py --keep
sed -n '224,235p' repos/_audit/mm/page_io.c
```

A patch file shows what one patch does. **The series tree shows what the kernel
does.** They differ whenever a later patch edits the same region, a hunk is
context rather than change, or ordering matters. Any claim about kernel
behaviour has to come from the tree.

### Do NOT "fix" this by initialising the pool

The obvious belt-and-braces move — also call `sio_pool_init()` from
`xswap_create()` — is **harmful**, and so is adding a real disk swap device.

Both make `mempool_alloc()` succeed, and then the write proceeds into code that
cannot work for an xswap device. `xswap_create()` sets `si->bdev = NULL` and
never populates `swap_extent_root` (`add_swap_extent()` is reachable only from
the block-device swapon path, `generic_swapfile_activate` and
`swap_fs_activate`). So:

- `swap_bdev_can_merge()` calls `swap_folio_sector()` during
  `swap_add_folio()`'s merge test — with two or more folios batched, the BUG
  fires *before* any submit.
- Otherwise `swap_bdev_submit_write()` reaches `offset_to_swap_extent()`, which
  ends in `BUG(); /* It *must* be present */`.

You would trade a conditional NULL-deref on one task for a **deterministic
`kernel BUG`** on the same trigger — strictly worse, and harder to diagnose.

**Adding a real swap device is the same trap one step sideways**: it initialises
the pool through `setup_swap_extents()` and buys the identical BUG. The pool
being NULL is what currently keeps the bug confined to a guard we can place; the
guard is the only viable shape short of a physical backend.

### The refusal has more causes than "pool full"

The OOM snapshot 21 s before the oopses shows `zspages` at ~86.6% of the 20%
ceiling — below the 90% accept threshold. So the trigger was probably not the
pool being full but a failure inside `zswap_store_page()` (zsmalloc allocation,
entry cache, xarray). This widens the set of refusals nothing upstream handles,
and it means "the pool will drain" is not a reason to relax.

### Upstream status

Checked 2026-09-20 by an exhaustive multi-channel sweep (mailing-list trees,
akpm's branches, patchwork, GitHub, the crash signature, and the design history),
with each candidate independently re-verified. **Upstream has not fixed this,
and cannot have**: `do_swapout()` does not exist upstream at all — it has zero
hits across all 13 lore mirrors and is absent from torvalds, akpm and
linux-next. It is MARIE's. Upstream cannot fix a bypass it does not have.

Two further facts from that sweep:

- **akpm's tree has no xswap code at all.** `mm-everything-2026-09-20`
  (`62310f16ff3f`) contains zero occurrences of `SWP_XSWAP`, `xswap_create` or
  `nr_real_swapfiles`; every other akpm branch is an ancestor of it.
- **The RFC is a no-op on this machine.** Patch 04's `xswap_alloc_phys_slot()`
  walks `swap_avail_head` skipping `SWP_XSWAP` devices; `/proc/swaps` has one
  row, `xswap0`, so `nr == 0`, `xswap_backend_alloc()` returns an empty entry,
  and patch 06 executes exactly the guard already carried. And patch 06 edits
  `swap_writeout()`, which `do_swapout()` never enters.

**Independent prior art.** `RAMDRAGONS/jcachy` commit `6c82211cd`
(Judas Drekonym, 2026-09-20T00:57:58Z, ~16 h before `2199`) carries the same
fix in `do_swapout()`, differing only by a `data_race()` wrapper. Two people
converging on the same three lines is the strongest available evidence the
diagnosis is right. `data_race()` is not adopted here because `CONFIG_KCSAN` is
off (so it compiles away) and because upstream's own guard in `2155` does not
use it — ours matches upstream's style, theirs matches MARIE's.

### Guarding a shared callee: keep the count honest

There are exactly **three** callers of `__swap_writepage()` in the series tree —
`swap_writeout()` (guarded by `2155`), `zswap_writeback_entry()` in
`mm/zswap.c` (also guarded by `2155`, a site easy to miss), and `do_swapout()`
(guarded by `2199`). `swap_add_folio()` is reached only from
`__swap_writepage()` (WRITE) and `swap_read_folio()` (READ, guarded).

That count is **rebase-sensitive**: the RFC renames the callee to
`__swap_writeout()` and adds a third argument, and Nhat Pham's vswap series adds
call sites. Re-derive it after every bump rather than trusting this paragraph:

```bash
git -C repos/_audit grep -n '^\s*__swap_writepage(' -- mm/ | wc -l   # expect 3
```

### Earlier upstream status

Checked 2026-09-20, and **upstream has not fixed this**:

- **v3** (2026-09-16, the newest of the series carried) is byte-identical to our
  v2 in every affected file.
- A new **RFC** (patchwork series 1169641, 2026-09-20) does touch the same
  guard — patch 06/17, *"fall back to disk when zswap refuses an xswap page"* —
  and its commit message describes our exact condition. But it is a feature
  adding a physical backend for xswap, not a fix: it never mentions `sio_pool`.
- `linux-mm/linux-mm` PRs #4867 (that RFC) and #4774 (v3) track both.

So `2199` is ours alone, and it should be dropped when upstream lands a fix for
the bypass rather than merged forward.

## Two ways to extract a lore email that silently produce a broken patch (2026-09-20)

Both were hit in one sweep, on the `[PATCH 01/18] More compact VCN IB emission`
email, and both fail *quietly* — the extractor reports success and the patch is
unusable.

**1. Not every mailer emits the `diff --git` line.** Anchoring the body search
on `diff --git` returned "no diff" for four sched_ext patches that each plainly
contained one. Tejun Heo's `git send-email` output for those starts the hunk at
`--- a/kernel/sched/ext/ext.c` with no `diff --git` above it. Anchor on the
earliest of both:

```python
starts = [m.start() for m in re.finditer(r'^(diff --git |--- a/)', raw, re.M)]
```

**2. Cutting at the diff start throws away the commit message and every
trailer.** The obvious "take everything from the first diff line" keeps the
hunks and drops the prose — including the `Signed-off-by` that Check 4 requires
and the reasoning a later reader needs. `rg '^Signed-off-by:' patch` returns
nothing, which reads as "the author didn't sign off". It was there; the
extractor had discarded it.

Keep the whole body from the end of the mail headers to the `-- ` signature
separator, and synthesise only the `From nobody …` line and the
`From:`/`Date:`/`Subject:` triple:

```python
body = raw[after_mail_headers : signature_separator]
```

This also preserves the `---`/changelog/`---` block, so a v2's "what changed"
survives into the carried patch.

Verify an extraction by asserting on it, not by eyeballing the hunks: count
`Signed-off-by`, count `--- a/`, count `@@`, and dry-run it. A patch with the
right hunks and no trailer passes `git apply` and fails review.

**Related trap, same session:** `set -- $pair` and `for x in $VAR` do **not**
word-split in zsh, the login shell here. `for pair in "4ff407a8 cmask"` sets
`$1` to the entire string, so `git show "4ff407a8 cmask:m"` fails and the
extractor reports NO DIFF for every input. Pass arguments explicitly, or use
`${=VAR}`. This has now cost time twice.

## A test against a missing tree reports everything as passing (2026-09-20)

Nine amd-staging commits were classified in one batch. All nine came back
*already carried* — including four that had never been looked at before, and
one that had been measured as PARTIAL an hour earlier. That inconsistency is
the only reason it was caught.

The classifier ran `patch -d repos/_audit -R -p1 ... < cand.patch` and branched
on the output:

```bash
if ! echo "$r" | rg -q 'FAILED|ignored|No file'; then st="CARRIED"
```

`repos/_audit` did not exist. It had been consumed by the previous build, which
ran `audit_series.py` **without `--keep`** — only `--keep` leaves the tree
behind. So every invocation produced:

```
patch: **** Can't change to directory repos/_audit : No such file or directory
```

which contains none of the three strings the classifier looked for, fell
through every branch, and landed on "CARRIED". **`patch` also exited 0 on that
fatal error**, so `if patch ...; then` and `$?` were equally useless.

Three rules:

1. **Assert the fixture exists before testing against it**, and abort loudly if
   it does not. A test harness that cannot reach its reference tree must not
   return a verdict at all.
2. **Structure the classifier so "no verdict" is an error, not a default.**
   Match positively — set `st="CARRIED"` only inside `if reverse-applied-ok`,
   never as the fallthrough of a failed match.
3. **Treat an implausible uniform result as a signal.** Nine of nine passing,
   including things never before tested, is not a clean sweep; it is a broken
   instrument. The same shape appeared earlier the same day, when a subject
   search reported four carried patches as absent.

For this repo specifically: `audit_series.py` without `--keep` removes
`repos/_audit` at the end of the run. Any later command that patches into
`repos/_audit` is testing nothing until the tree is rebuilt.

Related: *"A crashed command and an empty result look identical"* above — that
one is a search returning nothing because it broke. This is a test returning
*success* because it broke, which is worse: the broken state is indistinguishable
from the good one.

## A patch that applies cleanly can be installing a duplicate (2026-09-21)

`9007-drm-gfx12-Program-DB_RING_CONTROL.patch` was a dead carry: rc4 had
already absorbed the upstream change, and the same block sits at
`gfx_v12_0.c:1842-1850`. Standalone, the patch does not apply — which is the
signal. **But the cumulative audit reports it `ok`.**

The reason is the anchor. Our patch's hunk context is the lines *preceding* the
block (`gfx_v12_0_get_tcc_info()`, `pa_sc_tile_steering_override = 0`), and
those are still present in rc4. So `git apply` finds a valid anchor and
**inserts a second copy** rather than failing. The series tree ended up with
`DB_RING_CONTROL` programmed twice, byte-identical blocks at `1836-1844` and
`1851-1859` against once in rc4.

**`audit_series.py` cannot distinguish "applied" from "applied as a
duplicate."** It measures whether the hunk lands, not whether the change is
wanted. Reverse-applicability is the test that catches this, and the audit does
not run it per patch.

Found by grepping the series tree for the register the patch is named after and
seeing it twice. That targeted check works; the general one does not — see the
next section.

## Four ways to detect dead carries automatically, all of which fail (2026-09-21)

Each was tried against the full series. All four produce wrong answers, and each
fails differently:

| approach | failure mode |
|---|---|
| reverse-apply each patch to pristine rc4 | **false negative** — `9007` forward-fails, so it cannot reverse-apply either. Reported "none" while a known duplicate sat in the tree. |
| added block present contiguously in rc4 | **both** — missed `9007` because `*/` is a *context* line inside its added block, breaking contiguity; falsely flagged `1064` because its addition (`if (r)` / `return r;`) is generic and matches elsewhere. |
| count of a distinctive added line > rc4_count + 1 | **false positive** — a patch legitimately adding the same line in two functions trips it. 84 KB of suspects, nearly all valid. |
| sliding 5-line window, once in rc4 and twice+ in series | **false positive** — every legitimately *inserted* block whose lines also occur elsewhere is flagged, and one insertion produces W overlapping windows. |

The last one looks convincing and is not: consecutive hits overlap by four
lines, which is the tell that a single insertion is sliding through the window.

**Do not retry these.** The reliable method is reading the code, plus the
targeted variant above: after a rebase, grep the series tree for the
distinctive symbol or register each patch is named after and confirm the
expected count.

## A revert is not a supersession — read the thread (2026-09-21)

A sweep reported `1065`/`1066` as "genuinely superseded" by a three-part series
posted 2026-09-17 whose first two patches revert them. The framing was wrong in
the way that matters: a revert of carried work is the **opposite** of
superseding it, and it needs a maintainer's blessing before anything is
touched.

Christian König's reply (`5de2a7d1`, `lore-amdgfx`):

> That doesn't work like this. […] **The patches you want to revert actually
> look correct to me.** The fence slots usually needs to be reserved directly
> after we locked the BOs.

Acting on the summary alone would have swapped working code for a rejected
design. The rule: when a candidate *removes* something we carry, read the
thread for an objection before concluding — "a newer posting exists" is not a
verdict.

## "No tree or mirror has it" is not "it was fabricated" (2026-09-21)

`1158`'s header claims `dfd0e5aa6aadcd477ccca12dcc1433a76aa8d543`, and that sha
exists in **none** of our trees or lore mirrors. It was flagged untraceable,
with fabrication implied.

It is real. GitHub's commit search resolves it to
`kerneltoast/kernel_x86_laptop` — the author's own repository, which we simply
do not clone. Fetching `https://github.com/<owner>/<repo>/commit/<sha>.patch`
(plain, no API quota) and comparing change-lines gave an identical set, 23 vs
23.

Out-of-tree contributors keep their work on GitHub, not on lore. This is the
second time this has come up (see the CRIU case). **Check GitHub before
recording a sha as invented** — and never record "unverifiable from our sources"
as "fabricated".

## Exit codes disappear through a pipe, and through an `&&` chain (2026-09-21)

Two forms, both hit in one session.

**Through a pipe.** `git apply --check x.patch 2>&1 | head -10 && echo
"APPLIES CLEANLY"` printed *APPLIES CLEANLY* directly below `error: corrupt
patch`. The exit status is `head`'s, which is always 0. The same shape hid a
broken query that returned 90 of 100 issues empty while reporting success.

**Through `&&`.** A verification chain
`echo … && rg -c … repos/_audit272/… && cd sleepy-next && makepkg …` never
reached makepkg: `repos/_audit272` had been removed by the audit (no `--keep`),
so `rg` exited 2 and `&&` short-circuited. The task was reported as **exit code
0** because the final `echo` succeeded.

Capture exit codes on their own line, never through a pipe or an `&&` chain:

```bash
git apply --check x.patch; rc=$?     # then branch on $rc
```

## Reverse-apply is not authoritative for older commits (2026-09-21)

`0b0ff65d3ca1` (the stream-validation modeset-hang fix) reverse-fails against
rc4, which normally reads as "absent". Its content is plainly present: every
identifier it introduces is there — `encoding_order`, `bpc_order`,
`encoding_mask` ×13, `bpc_mask`, `is_hdmi_ep` — the shared
`force_yuv420_output`/`force_yuv422_output` fields are gone, and the function no
longer recurses.

The reverse check failed on **context drift** from unrelated display changes
between the patch's date (2026-07-21) and rc4 (2026-09-20), not on absence.

Reverse-applicability is authoritative for recent patches and unreliable for
older ones. Past a few weeks, grep the base for the identifiers the patch
introduces and treat that as the verdict.

## Dead carries come in two kinds, and only one is detectable by text (2026-09-21)

`9007` and `1027` were both dead carries, and they look nothing alike under a
text search.

**Kind 1 — literal duplicate.** The patch's added lines already exist in the
base *verbatim*, so applying it inserts a **second copy**. `9007` put a second
`DB_RING_CONTROL` block into `gfx_v12_0.c` (rc4 had it at `1842-1850`; ours
added `1836-1844` and `1851-1859`). Detectable by text.

**Kind 2 — superseded implementation.** The added lines are **not** in the base
at all; the base has *different* code doing the same job, and often doing it
better. `1027` realigned only `mes.ring[0]`'s polling fence on reset; rc4 had
since grown a loop over `AMDGPU_MAX_MES_INST_PIPES` covering **every** MES
instance pipe, plus an equivalent KIQ loop. Our patch was therefore redundant
work on top of a strict superset. **No text search finds this** — the detector
correctly reported no match, because the strings genuinely differ.

Kind 2 needs a semantic question per patch: *does the base already do this job?*
The cheap proxy that works: if a patch **fails to apply standalone** to pristine
base, ask whether the base's current code at that site already achieves the
patch's stated purpose. That is how `1027` was caught — by reading the comment
the patch itself carried ("force complete the MES scheduler ring fence on
reset") and comparing it against what rc4's loop does.

### Validate a detector against a known positive before trusting it

A detector for Kind 1 was built three times. Version 3 — matching the hunk's
**post-image** (context + added lines) against the base — reported **zero**
candidates across all 271 patches, which looked like a clean bill of health.

It was broken. Run against the reconstructed `9007` it also reported zero,
failing at the third post-image line. Only version 2, matching the added lines
as an **ordered subsequence**, found the known positive at all.

**A detector that reports "nothing found" must be run against a case you know
it should find.** Otherwise "clean" and "blind" are the same output. This is the
same failure the `repos/_audit`-missing incident produced, in a new costume.

Version 2 was then used, and its five hits were all cleared by hand: three apply
cleanly to pristine rc4 (so their content is not there), and one fails only
because its series predecessor fails too — which is series dependency, not
duplication.

## Dead carries, kind 3: the fix is already carried inside an unrelated patch (2026-09-22)

Kinds 1 and 2 above both compare a candidate against the **base**. This one
never touches the base: the work is already done, by one of **our own carried
patches**, whose subject names something else entirely.

Mario Limonciello's `[PATCH] cpufreq/amd-pstate: Fix TOCTOU when changing
driver mode via sysfs` (2026-09-21) takes `amd_pstate_driver_lock` *before*
reading `mode_state_machine[cppc_state][mode_idx]`, so a concurrent sysfs write
cannot make the second read resolve against a changed `cppc_state` (NULL
deref, or a second `amd_pstate_driver_cleanup()` double-freeing
`current_pstate_driver->attr`).

Our `1227` — carried as *"ACPI: CPPC: Accept requests to retain immutable
autonomous selection"* — rewrites that same function for its own reason, and
in doing so opens with:

```c
	guard(mutex)(&amd_pstate_driver_lock);

	if (!mode_state_machine[cppc_state][mode_idx])
		return 0;
	...
	return mode_state_machine[cppc_state][mode_idx](mode_idx);
```

Lock first, both reads under it, `cppc_state` stable across them. The race is
already gone, and `1227` additionally guards the immutable-autonomous case.
Nothing to add.

**Detection.** Grep the series for the **function** the candidate modifies, and
read **every** hit — not just the one whose subject looks related:

```bash
rg -l 'mode_state_machine|amd_pstate_update_status' sleepy-next/patches/
# -> 1231 (subject matches: "restore previous mode on failure")
# -> 1227 (subject does NOT match: "retain immutable autonomous selection")
```

**This is exactly how it was missed.** That grep *did* run and *did* return
both. Only `1231` was read, because only `1231`'s subject was about mode
changes; `1227` was set aside as unrelated. The patch that already fixes your
bug is rarely the one named after it.

**The tell, again, is the offset.** The candidate applied cleanly to pristine
`v7.3-rc4` at offset **−107** — it was authored ~107 lines ahead of our base,
and the region that moved is precisely what `1227` rewrote. Standalone
applicability is not admission (see "A patch that applies cleanly can be
installing a duplicate"); the cumulative apply against the series tree is what
decides:

```bash
python3 .claude/skills/kernel-build/scripts/audit_series.py --keep
patch -d repos/_audit -p1 --forward --batch -F2 --dry-run < candidate.patch
# -> Hunk #1 FAILED at 1901 / Hunk #2 FAILED at 1910 / 2 out of 2 hunks FAILED
```

A clean standalone dry-run plus a −107 offset against a base we have heavily
patched in that subsystem should be read as *"one of our own patches is in
here"* until proven otherwise.

## A third way a lore mail yields a broken patch: quoted-printable (2026-09-22)

Two failure modes were already recorded — `git show <sha>` diffs the *email*
rather than the code (the patch is in blob `m`), and cutting at the `-- `
signature separator strips the trailing newline so `git apply` reports
`corrupt patch` while `patch -p1` accepts it.

Here is the third. Keith Busch's blk-mq patch arrived with:

```
Content-Transfer-Encoding: quoted-printable
```

and 17 `=` soft line breaks. Extracted raw, it died at line 6 with

```
corrupt patch at /tmp/kyber.patch:6
patch: **** malformed patch at line 6: _mq_alloc_data *data,
```

which is a *wrapped* `struct blk_mq_alloc_data *data,`. The `Fixes:` trailer
gave it away too — `blk_mq_alloc_r=` / `equest()")` split across two lines.

**Decode before extracting:**

```python
import quopri
hdrs, _, body = open(path,'rb').read().partition(b'\n\n')
dec = quopri.decodestring(body).decode('utf-8', errors='replace')
```

Measured after decoding: 10 hunks, and `git apply --check` exits 0. Before
decoding, both `git apply` and `patch` rejected it — and a naive reading would
have concluded the patch was malformed and moved on.

**Check `Content-Transfer-Encoding` on any lore mail before trusting an
extraction.** Three different encodings or cuts have now produced three
different silent breakages.

## Page 1 is not the tracker: an API default that hid 25 issues (2026-09-22)

The documented way to sweep the drm/amd work items was:

```bash
curl -s ".../projects/drm%2Famd/issues?state=opened&per_page=100"
```

It returns exactly 100 rows and looks complete. It is not. The project holds
**1808** open issues across 19 pages, and this returns **page 1 — the newest
100 by *creation* date**. An issue created months ago and *updated* yesterday
never appears.

Measured: `updated_after=2026-09-20T00:00:00Z` returned **49** issues for the
window. Only **24** of them were on page 1. The other 25 included three
on-target RX 9070 XT threads (`#5718`, `#5647`, `#5511`) that had been missed
by every previous sweep.

**Filter by time, never by page:**

```
?state=opened&updated_after=YYYY-MM-DDT00:00:00Z&per_page=100
```

and compare the returned row count against `x-total`; if they differ you are
reading a page, not the set.

The general shape is already on record here — a default that silently answers a
narrower question than the one asked. It appeared before as `--all` being
overridden by a ref filter, and as a shallow clone making `merge-base` answer
confidently about history it cannot see. **Whenever a query has a default
limit, assert the size of what came back against the size of what exists.**

## A tunable you set can be silently overridden by a patch you carry (2026-09-22)

`vm.swappiness = 180` had been configured on this machine, documented at length
in `swap-stack/99-xswap-swappiness.conf`, and had **never once taken effect**.
LRU-MARIE's reclaim driver clamps the effective value before it picks between
the anon and file lists:

```c
u8 configured = (u8)mem_cgroup_swappiness(memcg);
u8 swappiness = (READ_ONCE(marie_low_swappiness_mode) && configured > 1) ?
                1 : configured;
```

`marie_low_swappiness_mode` defaults to 1, and MARIE's own header says the
clamp applies *"regardless of the higher values vm.swappiness /
memory.swappiness udev rules, tuning daemons, or distro defaults have
installed."* A console `cat /proc/sys/vm/swappiness` still reads 180 — the
knob is set, it is simply not consulted.

**The cost.** swappiness = 1 makes reclaim file-dominant. On this machine
`pgsteal_file` ran **3.55x** `pgsteal_anon` over one boot, with both lists
refaulting at ~6.8M — reclaim evicting page cache that was immediately read
back from the NVMe, which is the expensive direction when swap is compressed
RAM. That sustained refault:steal ratio is what MARIE's own thrash-livelock
watchdog (`thrash_wd_fn`) exists to detect, and on 2026-09-22 at 21:14:27 it
fired and invoked the OOM killer against `electron` (Discord) — at a moment
when **84% of swap was free** and **21.6 GB of clean page cache was still
resident**. The watchdog's own premise is "the working set provably does not
fit in RAM"; it did not hold.

**The general rule.** When a patch series installs a policy knob, grep the
series for the sysctl it overrides before trusting a sysctl value that looks
set. `rg -n 'swappiness' sleepy-next/patches/` would have found the clamp on
day one. The knob read back correctly at every step, which is exactly why this
survived so long — **a readable sysctl is not evidence that the value is
used.**

Also worth carrying: the fix was *not* a kernel change. Clearing the clamp is
a sysfs write, and it went in as a tmpfiles.d entry.

## A README claim is not evidence, even in this repo (2026-09-22)

`swap-stack/README.md` justified this machine's swap design with:

> "zram creates a block device with a fixed size ... and never returns that
> memory when the workload shrinks."

**That is false**, and it had been load-bearing in a decision. Checked against
the source: zram allocates on demand (the only preallocation is a 16
byte-per-page metadata table, ~0.39% of `disksize`), and memory comes back
three ways — `zs_shrinker_scan()` compacts a pool and frees empty zspages,
`zs_free()` frees a zspage the moment it empties, and the swap layer calls
`zram_slot_free_notify()` on slot release (swapin of the last reference,
discard/TRIM, swapoff). Only the device *size* is fixed, and that is a far
weaker objection than the one written.

The claim was ours, it was confident, and it was wrong. Treat this file and
the READMEs as prior observations, not as verified facts — the same standard
this document applies to everything else.

## Corollary: the same claim, checked five ways, was still partly wrong

The zram-vs-zswap comparison that replaced it went through five independent
passes (kernel source, kernel docs, upstream ML, distro udev rules, plus
community and bug-tracker research). Three of the six claims as originally
stated came back **REFUTED or corrected**:

- "zram never returns memory" — refuted, above.
- "zram gets a drain path if a backing device is configured" — overstated.
  Writeback is **never automatic**: the kernel has no heuristic for when to
  move data out, it runs only on an explicit
  `echo <policy> > /sys/block/zramX/writeback`, and it needs a dedicated
  unformatted block device (`backing_dev_store()` rejects non-`S_ISBLK`).
  zram-generator's `writeback-device=` configures the target and does not
  drive it — upstream issue `systemd/zram-generator#164` is that RFE, with
  `bd_stat` staying zero until the sysfs writes are made by hand.
- "zswap-on-zram is redundant" — true in effect but **not a kernel claim**.
  No kernel document says it; the Arch Wiki *Zram* page does ("it will prevent
  zram from being used effectively ... recommended to permanently disable
  zswap"). Do not attribute it to the kernel.

The last one matters for method: a claim can be *correct* and still be
mis-sourced, and repeating it with the wrong authority is how it becomes
unfalsifiable later.

## Oversizing a compressed swap device is the dangerous direction (2026-09-22)

Both zram and xswap expose an **uncompressed** capacity while consuming RAM
proportional to the *compressed* size, so both advertise more than they can
hold. For xswap that was structural; for zram it is a sizing choice, and the
failure mode is not the obvious one.

sizing too large inflates the reclaimable estimate. Matt Fleming's RFC *"mm:
Reduce direct reclaim stalls with RAM-backed swap"*: *"Systems with zram-only
swap can spin in direct reclaim for 20-30 minutes without ever invoking the
OOM killer"* — a 377 GiB zram at 10% used reports ~340 GiB of free slots that
no physical RAM backs, and `should_reclaim_retry()` believes it. The Fedora
trackers (`atomic-desktops#130`, `kde#728`) carry the user-visible version:
RAM ~94%, zram ~100%, desktop unresponsive for ~30 minutes, and *neither* the
kernel OOM killer nor systemd-oomd fired.

So the intuitive "make swap big so we never run out" is backwards here.
Practice: Fedora `min(ram, 8192)`, Arch Wiki "half of the total system
memory", zram-generator `min(ram/2, 4096)`, kernel doc an outer bound of
~2x RAM. This machine took `ram / 2`, which is the Arch Wiki figure and well
inside the kernel bound.

## A content probe must grep for code, not for the commit message (2026-09-22)

Hao Jia's zswap shrinker series looked like a strong carry. Its message
describes a failure mode that maps onto this machine's architecture exactly:

> "shrink_memcg() writes back at most one entry per-node during its traversal
> ... under high memory pressure, this can cause the writeback speed to be too
> slow to keep up with refaults, leading to zswap store failures and forcing
> pages to skip zswap and go directly to disk, which results in an LRU
> inversion."

A probe said they were missing:

```bash
git -C repos/torvalds show v7.3-rc4:mm/zswap.c | rg -c 'shrink_memcg_batch|batch writeback'
# -> 0
```

**Both patches were already in rc4.** `shrink_memcg()` already had
`unsigned long nr_to_walk = SWAP_CLUSTER_MAX`, and `shrink_worker()` already
had the patch-1 comment verbatim plus `if (!memcg && !mem_cgroup_disabled())`.

`batch writeback` is a phrase from the commit **message**. It appears nowhere
in the resulting code, so a zero from it meant nothing. **Probe for an
identifier or a line the patch introduces** — a renamed variable, a new
function, a distinctive comment that ships with the change — never a phrase
that merely describes it.

This is the third instance of one shape in a single day: the
`ls ... | head` that printed "APPLIES CLEANLY" over a corrupt patch, the
`[ -d /sys/kernel/debug/zswap ]` that reported "absent" for an EACCES, and
now this. In all three the probe could not fail informatively — it had a
branch that silently produced a confident-looking wrong answer. When a probe
returns "absent"/"fine"/"nothing found", ask what its *other* failure modes
would have printed, and whether they are distinguishable from success.

## "The logs disprove it" beats "the mechanism fits" (2026-09-22)

Clearing LRU-MARIE's swappiness clamp was diagnosed, verified in source, and
reported as *"that, not the backend change, is the fix"*. The mechanism was
real: `low_swappiness_mode` does clamp the effective swappiness to 1, and
`pgsteal_file` was running 3.55x `pgsteal_anon`.

**The logs disprove the conclusion.** Three more thrash-watchdog kills landed
after the clamp was cleared (22:35:44, 22:44:46, 22:46:00), and every one of
them fell inside a kernel-build window:

| Time | Killed | Running |
|---|---|---|
| 21:14:27 | `electron` | ordinary use — *before* the fix |
| 22:35:44 | `xdg-desktop-por` | build 1 (22:29:56 → ~22:36) |
| 22:44:46 | `xdg-desktop-por` | build 2 (22:40:27 → 22:46:32) |
| 22:46:00 | `xdg-desktop-por` | build 2 |

At the 22:35 firing, `inactive_anon` was **477,511 pages (1.87 GB)** against
`inactive_file` **6,324,700 pages (24.7 GB)** with 211 MB free. There was
almost no anonymous memory in play. The pressure was file-side — and
swappiness, which only shifts the anon:file *ratio*, had nothing to shift. A
kernel build's working set is object files and source, so it thrashes page
cache regardless of how the split is configured.

**The transferable rule.** A verified mechanism is a hypothesis about the
cause; only the logs are evidence about it. "The code does what I said" and
"the system behaves as I predicted" are different claims, and the first does
not imply the second. Before writing *"this is the fix"* — as opposed to
*"this is a real bug, now fixed"* — check the events that followed the change,
not just the code that motivated it. The two sentences look similar and are
very far apart.

**Also worth carrying:** the honest form of this finding names its own
weakness. The normal-use evidence is a single event either side of the change,
so "the clamp contributed to the Discord kill" is plausible, not proven; and
the watchdog may be *correct* that a `-j16` kernel build does not fit a 32 GB
machine. `MAKEFLAGS="-j$(nproc)"` is the likely real trigger.

## The build itself was the bug, and I caused the freeze (2026-09-23)

> **RETRACTED 2026-09-23.** The claim below — that `-j16` was the cause — is
> **wrong**. See "CORRECTION: the build was not the bug" at the end of this
> section. It is kept because the reasoning error is the lesson.
The kernel build ran `-j"$(nproc)"` — hardcoded in the PKGBUILD at two call
sites, *not* inherited from `makepkg.conf`'s `MAKEFLAGS` as I had assumed when
I first went looking. On this 16-thread machine that is **16 concurrent clang
jobs**, each holding roughly 1-1.5 GB (more on the large AMD display units).

~~Measured consequence: a `-j16` build peaks around 20-25 GB of compiler
memory.~~ **Retracted — no such peak was ever measured.** Under a watcher at
`-j16`, `MemAvailable` never fell below **19 GB** on this 30 GB machine. The
figure appears to have counted `buff/cache` growth, which is reclaimable and
was never memory pressure. On rc4-7 that produced
**6 watchdog firings and 114 reclaim-retry firings in ~10 minutes**, with the
OOM killer repeatedly taking desktop processes (`steamwebhelper`, `electron`).
The desktop became unusable and had to be powered off.

**Two corrections to my own first diagnosis, both worth carrying:**

1. **The log spam was not the mechanism.** `kernel.printk` is `3 3 3 3` here —
   console loglevel 3, *below* WARNING(4) — so `pr_warn_ratelimited()` never
   reached the console at all. The messages were a *symptom* of the thrash, and
   I came close to prescribing a logging fix for a memory problem. Check where
   a message actually goes before treating its volume as the cause.
2. **Find where a value actually comes from.** I assumed the job count came
   from `MAKEFLAGS` in `/etc/makepkg.conf` and went looking there. It did not;
   the PKGBUILD sets its own. `rg` for the flag in the thing that runs it, not
   in the thing you expect to own it.

~~**The fix** is `_jobs=8` in the PKGBUILD.~~ **Reversed:** `_jobs` is **16**.

The cap was in place for part of one day. Removing it cost nothing measurable —
`-j8` builds in 6m22s, `-j16` in 6m03s — because wall-clock is dominated by the
build's *serial* stages (extract, patch, vmlinux link, BTF, kallsyms,
packaging), not by compilation. That is the part of this entry still worth
keeping: `_jobs` is a poor speed lever here, which is exactly why it was never
the thing to fight over.

**Generalisable rule:** on a machine that is also someone's desktop, a build's
peak memory is a correctness constraint, not a performance knob. `-j$(nproc)`
is right for a build server and wrong for a workstation whose RAM is already
spoken for. Size the job count against *free* RAM with the desktop running, not
against the core count.

**The rule survives; its application here did not.** Applied properly — a
watcher on `MemAvailable` with the desktop up — it reports 19 GB free at
`-j16`, so there was no conflict to resolve. The rule is still the right check;
the mistake was asserting its conclusion without running it.

## `open(path, 'w')` truncates on open, and I emptied a doc with it (2026-09-23)

Editing these docs with a Python one-liner, I wrote
`open(p, 'w').write(head + new + tail, 1)` — the `1` belonged to `str.replace`,
not to `write`. `write()` raised `TypeError` before writing anything, but
`open(p, 'w')` had **already truncated the file**, so `GUIDE.md` came back as
zero bytes and 78 lines were gone.

Caught by a routine `wc -l` check and restored with `git checkout --`, so the
cost was nil. It would not have been on `PATCH_SOURCES.md`, which is the
authoritative per-patch ledger and is not reconstructible from anywhere else.

**Rule: when a script rewrites a load-bearing file, write to a temp file and
`os.replace()` it.** Never open the real path in `'w'` mode mid-computation.
Also: `open(p, 'w').write(x, 1)` is a typo that fails *after* the damage —
the exception is not the safety net it looks like.

## MARIE's watchdog measured the wrong thing, and killed on it repeatedly (2026-09-23)

`thrash_wd_fn()` fires by choice — it calls `out_of_memory()` itself — once
free memory sits below the zone high watermark **and** the refault:steal ratio
stays at or above ~1:2 for 8 consecutive 2-second windows. Its stated premise
is that *"the working set provably does not fit in RAM"*.

**At the moment of a kill on this machine, that premise was obviously false:**

```
AnonPages       76,760 kB   (75 MB - almost no anonymous memory at all)
Cached      29,633,720 kB   (28.2 GB page cache)
MemAvailable 28,873,680 kB  (28.8 GB available)
free            50,030 pages (195 MB)   <- below high, so the gate is armed
net-progress   651269 refault / 675247 steal   (~96%)
```

28.8 GB available. Nothing about that is exhaustion. What the watchdog actually
measured is a **ratio**, and that ratio is also high during ordinary
page-cache churn on a machine holding 28 GB of cache — reclaim evicts a cold
file page, something reads it again, and the counter pair ticks. The heuristic
cannot distinguish that from a genuine RAM-backed-swap treadmill.

**The rate is what makes it expensive.** With `THRASH_WD_BACKOFF = 60` (60 s
hold-off) plus 8 × 2 s windows, it re-arms and fires roughly **every 80
seconds** for as long as the condition holds — and on a cache-heavy desktop the
condition holds more or less permanently. Measured: three kills at 12:44:45,
12:46:05 and 12:47:20, all of `xdg-desktop-por`. Not a one-off misfire; a
standing kill loop.

**And the trigger was not the build.** All three landed during the **patch
phase**, before a single line was compiled, so compiler memory was not
involved. That also means the `-j8` cap — correct in itself — could not have
prevented them, and I should not have expected it to.

Disabled via `/proc/sys/vm/thrash_wd_mode = 0`, persisted with a tmpfiles.d
entry carrying the numbers above. This is a safety net being switched off, so
the justification has to be the evidence, not convenience. Re-enable if a real
livelock is ever suspected; the counters worth checking first are
`workingset_refault_*` against `pgsteal_*` **together with** whether free
memory is actually exhausted.

**Transferable rule:** a detector that fires on a *ratio* needs its denominator
checked against a case where the underlying resource is demonstrably fine.
"Refaults track steals" is a livelock on a small box and normal behaviour on a
big one, and the watchdog had no term that told the two apart.

## CORRECTION: the watchdog was right, and I disabled it for the wrong reason (2026-09-23)

The entry above says MARIE's thrash watchdog "measured the wrong thing". **That
conclusion was wrong**, and the way it was wrong is the interesting part.

The watchdog's counter is

```c
refaults = WORKINGSET_REFAULT_ANON + WORKINGSET_REFAULT_FILE;
```

An earlier change of mine had cleared `low_swappiness_mode` so `vm.swappiness
= 180` would reach the reclaim picker. That made MARIE reclaim **anon**
almost exclusively, and produced **192 million anon refaults against 201M anon
steals** — a reclaim loop making no net progress. That is exactly the livelock
the watchdog exists to detect. It fired because the machine *was* thrashing.

So the watchdog was not measuring the wrong thing; I was. I looked at
`MemAvailable: 28.8 GB` and `AnonPages: 75 MB`, concluded "the premise is false,
this is a false positive", and switched the alarm off. But the working set
having plenty of RAM and reclaim *making no progress* are not the same claim,
and only the second one is what the watchdog tests. **A single memory reading
cannot disprove a livelock.**

**What settles it is re-arming the detector and measuring its own inputs.** With
the watchdog armed and a build running — in the patch phase, where the kills had
happened:

| | swappiness=180 | swappiness=1 (fixed) |
|---|---|---|
| watchdog firings | 3 in 3 min | **0** |
| kills | 3 | **0** |
| refault:steal ratio | **~0.95** | **0.155** |
| steals per refault | ~1 (thrashing) | **6.5 (reclaim working)** |

**Both columns are window deltas over a build window, not cumulative readings.**
This matters: the cumulative `workingset_refault_*` counters never reset, so
49 minutes after the fix `/proc/vmstat` still yields a cumulative ratio of
**0.889** — the 192M anon refaults from the bad window are permanent residents
of that total. Reading the cumulative figure makes the fix look like it did
nothing. Measure deltas over a window, or the correction is invisible.

Re-measured 2026-09-23 over a 90s window with reclaim active: ratio **0.151**,
**6.62** steals per refault — the figures above hold. The split is the point:
`steal_file` 1,500,435 against `steal_anon` 542,127, i.e. reclaim is now
file-first, which is what swappiness=1 with the clamp on is supposed to do.

**Measured again across a full kernel compile** (the load that used to trigger
the watchdog), 2026-09-23: ratio **0.303**, **3.30** steals per refault, and
**0 firings**. The split is file-first as intended — `steal_file` 6,327,232
against `steal_anon` 1,592,606. The watchdog fires on a sustained ratio near
1:2, so 0.303 is comfortably clear even under the heaviest load this machine
produces.

The condition no longer holds, so the safety net is back on
(`/etc/tmpfiles.d/99-marie-thrash-watchdog.conf` now sets it to **1**).

**Two rules worth keeping:**

1. **Disabling a detector is a claim about the detector.** Proving it wrong
   means showing its *inputs* are misread — not showing that a metric you chose
   yourself looks fine. I "verified" the false positive with `MemAvailable`,
   which the watchdog never looks at.
2. **A symptom and its cause can be in different subsystems.** The kill was the
   symptom; the reclaim policy was the cause. Treating the symptom first
   (disable) and the cause second (revert) is the right order — but it is not
   evidence that the symptom was spurious, and I reported it as if it were.

The `-j8` build cap from the same session is unaffected and still correct: 16
clang jobs genuinely over-commit this machine, independently of any of the above.
