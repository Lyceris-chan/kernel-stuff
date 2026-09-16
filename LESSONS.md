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
