# Changelog

Notable changes to `linux-sleepy-next`, the only package in this repository. It
targets one machine: an AMD Ryzen 7 7700 (Zen 4) with a Radeon RX 9070 XT
(Navi 48 / RDNA 4).

One entry per released package version, newest first. On the mainline line a
version is `<kernel base>-<pkgrel>-sleepy-next`, which is what `uname -r`
reports. The earlier linux-next preview releases appended their snapshot date,
as in `7.2.0-10-sleepy-next-20260828`. The format follows
[Keep a Changelog](https://keepachangelog.com/).

Two earlier artifacts are summarised at the end under
[Earlier packages](#earlier-packages): the 7.2 `linux-sleepy` package and the
`wannabe-7.3` preview tree. Both were removed from the working tree, and their
full entries remain in git history.

## [7.3.0-rc3-3-sleepy-next]: 2026-09-14

### Added
- **Nineteen fixes from the multi-source sweep**, every one apply-tested against
  the full series before being added. Series: 172 -> 191 patches. Twelve are
  display and GPU core (below), eight are subsystem fixes (further down).
  - **`1159`** drm/amd/display: atomize IRQ register read/modify/write ops. The
    upstream fix for a non-atomic read-modify-write on `OTG_GLOBAL_SYNC_STATUS`
    that can clear `VUPDATE_NO_LOCK_EN`. That is the same mechanism as this
    machine's `flip_done` timeouts and the display artifacts recorded in
    `LESSONS.md`, and it matters most on high-refresh panels.
  - **`1161`** drm/amd/display: guard NULL DDC pins in `dal_ddc_open`, a hard
    wedge when a NULL pin meets `+0x28` (upstream issue #5716).
  - **`1162`** drm/amd/display: check `dc_state_create_copy()` for NULL in
    `dm_suspend`.
  - **`1064`** drm/amdgpu: don't release the fence reference the scheduler
    consumed — a cross-thread use-after-free in `amdgpu_vm_sdma_update()`.
  - **`2403`** drm/sched: do not restore unsaved virtual runtime (Tvrtko
    Ursulin, `Cc: stable`).
  - **`9055`**, **`9056`** drm/amdgpu/userq: a `userq_signal_ioctl` hang inside
    `drm_exec_until_all_locked()`, and filtering idle userqs out of the pending
    signal list.
  - **`9057`** drm/amdgpu: keep freed VM mappings on clear failure (`Cc:
    stable`).
  - **`9058`** drm/amdgpu: hold a runtime PM reference for P2P dma-buf
    attachments (`Cc: stable`).
  - **`9059`**, **`9060`** drm/amdkfd: don't gate userptr cleanup on the owning
    mm, and skip migration when the fault window is already in VRAM.

### Also added — eight subsystem fixes
- **`2009`** fs/buffer: check for a NULL pointer before
  `folio_test_dropbehind()`. The most severe find of the sweep: `bh->b_folio`
  is dereferenced unguarded, and jbd2 submits buffer heads with no folio — a
  NULL-dereference panic on the ext4 journal commit path, which is this
  machine's root filesystem. Crash reported on 7.3.0-rc2-next; the culprit
  commit is in rc3.
- **`2152`** khugepaged: hold `invalidate_lock` across `collapse_file()`
  readahead. A syzbot-reported deadlock between collapse and truncate,
  reachable in about 20 seconds under a collapse/truncate race.
- **`2150`** mm/huge_memory: fix pgtable withdrawal for huge zero PMDs, a NULL
  dereference on `munmap()` (`Cc: stable`).
- **`2154`** mm/page_alloc: apply the per-task GFP context in the bulk
  allocator, so `PF_MEMALLOC_NOIO`/`NOFS`/`PIN` are honoured (`Cc: stable`).
- **`2153`** writeback: report a Tasks-RCU quiescent state per cgwb drain pass.
  Without it any `synchronize_rcu_tasks()` under `PREEMPT_LAZY` can stall for
  minutes and trip the hung-task detector (`Cc: stable`).
- **`2151`** mm/shmem: ignore sysfs configs for forced collapse, restoring the
  documented `MADV_COLLAPSE` behaviour (`Cc: stable`).
- **`2010`** blk-cgroup: save IRQ state in `blkg_tryget_closest()`, where an
  unconditional `spin_unlock_irq()` could re-enable interrupts under a caller
  holding the lock with `spin_lock_irq()`.
- **`2404`** sched_ext: close the pre-enable ops error claim window — a
  use-after-free in `kernel/sched/ext/ext.c` (`Cc: stable`). Worth having
  because this machine actually runs sched-ext (`scx_cake`), and unlike the
  `fair.c` patches this one is **not** inert under full-switch mode.

### Not carried
- **`1160`** drm/amd/display: only allow freesync on a `VRR_ENABLED` crtc. The
  most conceptually interesting find: it addresses the same condition as the
  passive-VRR fix in `pkgrel 2` from the other side, by refusing to let
  VRR-capable sinks set `allow_freesync` while `VRR_ENABLED=0` — the path that
  lets FPO stretch frames during UCLK switches. Three hunks apply; the fourth
  fails because the author's tree has `dc/dml2_wrapper/dml21_wrapper/` while
  rc3 has `dc/dml2_0/dml21/`, and that file's content differs around the hunk
  too. Deferred rather than hand-rebased.
- **`9061`** drm/amdkfd: fix a TCP XNACK scoreboard reset race. It applied
  cleanly but **failed to compile**: its new `gfx_v9_4_2_run_shader()` call
  passes 11 arguments while rc3's definition takes 10, so the patch depends on
  a signature-changing prerequisite that is not in v7.3-rc3. Dropped for that
  reason, not for irrelevance. This is the "applies but does not belong" case
  the cumulative-apply check cannot catch — only a build can.
- **`2155`** mm/zswap: return `-ENOENT` when the swap device is gone. Two hunks
  fail against the current series.
- **sirlucjan's full zstd dev update.** Asked for explicitly, and the answer is
  no: it is a 1.5.7 → 1.6.0 vendored sync whose only x86-relevant deltas are
  already our `2128` and `2143` — and it **conflicts with both**, so carrying it
  would mean dropping them. Its bulk is ARM SVE2 and RISC-V RVV code that
  cannot execute on Zen 4, and its gcc workaround is inert under Clang.
- **CachyOS `sched/fair: do not scan twice in detach_tasks()`.** `fair.c` is
  inert here: sched-ext full-switch mode gates the CFS balance path.
- **CachyOS `finish_task_switch()` always-inline.** Evaluated before and
  rejected: the quoted 34.8% figure is for spectre_v2 retpolines, while this
  machine reports Enhanced/Automatic IBRS, leaving under 0.3% end to end.
- **`mm, swap: extendable swap devices (xswap)`, v2 12-patch series.** Applies
  cleanly, but it is a feature, not a fix, on a subsystem this machine does not
  need extended (zram swap).
- **`nvme: bump genctr when cancelling a request`.** Directly on the Phison E16
  reset path, but v1 with no `Fixes:`, no `Cc: stable` and no acks.
- **maple_tree range64 RCU pointer corruption.** Genuine memory corruption, but
  v1, unreviewed, with no `Fixes:` or `Cc: stable`. Worth re-checking after
  maintainer review.
- `repos/drm-misc` could not be refreshed (every fetch fails with HTTP 503
  during the `acknowledgments` phase), so drm-misc is the one source this sweep
  could not cover.

### Raised for a decision — `1144`
The MAG251RX is **HDMI 2.0 and DP 1.2a**, so `1144` ("Enable HDMI FRL by
default") is inert on the hardware: FRL is an HDMI 2.1 feature. It is
bit-identical to the change CachyOS reverted with no stated reason, and it is
implicated in open upstream work item #5649 (HDMI FRL blanking). Removing a
patch needs explicit approval, so it is left in place and flagged here.

### Open question (not acted on)
- The sweep flagged that `CLAUDE.md` lists `DCN42B` as a Navi 48 identifier and
  claimed it is really GC 11.5.0 with the DCN4A SoC variant B. `DCN_VERSION_4_2B`
  does exist as its own variant in `dal_types.h`, but that mapping could not be
  confirmed from the source here, so the hardware table is left alone and the
  question is recorded rather than resolved.

## [7.3.0-rc3-2-sleepy-next]: 2026-09-14

### Fixed
- **The MSI MAG251RX flicker.** That panel, running 1920x1080 at 240 Hz over
  HDMI, flickered continuously and became close to blank under cursor movement.

  The cause was **passive VRR**. It is the feature that keeps a sink in its
  variable-refresh state during fixed-refresh desktop use, and it is **opt-out**:
  patch `1150` defaults it on for every connector that advertises
  `passive_vrr_capable`, and patch `1151` drives `stream->freesync_on_desktop`
  from the inverse of that flag, so the driver keeps the FreeSync-Active bit set
  on the desktop even when VRR is switched off. The panel was therefore never in
  fixed-refresh mode. Cursor movement makes the compositor repaint, the frame
  interval swings, and the panel follows — which is why idle flicker was mild and
  cursor use was severe.

  It also explains why toggling VRR in COSMIC never helped: that control moves
  `VRR_ENABLED`, which is a different property from `PASSIVE_VRR_DISABLED`.
  Both outputs read `VRR_ENABLED=0  PASSIVE_VRR_DISABLED=0`.

  Fixed by inverting the default: the pristine CRTC state in
  `drm_atomic_helper_crtc_state_init()` now sets `passive_vrr_disabled = true`,
  so passive VRR is opt-in on this machine. The property stays exposed and
  writable, so a userspace that does want desktop passive VRR can still set
  `PASSIVE_VRR_DISABLED=0` on the CRTC.

  This is a deliberate local deviation from the upstream series, recorded in a
  `[sleepy]` block in patch `1150`'s commit message.

## [7.3.0-rc3-1-sleepy-next]: 2026-09-13

### Changed
- **Base moved to Linux 7.3-rc3.** `pkgrel` restarts at 1, and the series drops
  from 176 patches to 169.

### Removed
- **Ten patches that rc3 merges upstream**: `1155`–`1157` and `1153` (the HDMI
  RGB quantization series and its VTEM companion), `2300` and `2301` (kbuild
  `mksysmap`), `2401` and `2402` (the EEVDF fixes), `2501` (AMD MCE threshold
  interrupts) and `2600` (hrtimer). Each was confirmed present in a pristine
  rc3 tree by checking that the lines it adds are already there.
- **`1145`** (the HF-VSDB MCCS FreeSync guard). rc3 rewrites
  `amdgpu_dm_update_freesync_caps()`, so the block the patch guarded no longer
  exists — it cannot be rebased without re-authoring it, and the rc3 code
  supersedes its purpose.

### Added
- **Four memory-management fixes**, each verified to apply on top of the whole
  series:
  - **`2144`** xarray: fix the index jumping backwards in `xas_find()`. A syzbot
    use-after-free: the index moves backwards while a multi-index entry is
    concurrently split, and `filemap_map_pages()` then dereferences a page-table
    page already freed through `tlb_remove_table_rcu()`.
  - **`2145`** mm/vma: unaccount correctly when `mmap_prepare()` fails, which
    otherwise leaks security accounting over the `RLIMIT_AS` budget. The
    regression source is in the base tree.
  - **`2146`** mm/mlock: use the IRQ-safe accessor for `NR_MLOCK` in
    `__munlock_folio()`, where a bio-completion softirq can corrupt the counter.
  - **`2147`** mm/memcg: clear the folio's memcg after updating the per-memcg
    stats, so the swapcache counter stops drifting. This machine swaps
    constantly, so its `memory.stat` was reporting swapcache that had already
    gone.

### Fixed
- **The patch files themselves**, following the provenance audit:
  - the `Cc:` label restored in the 23 kbuild patches, where a stripped field
    name had left a 36-line address list orphaned under `Message-Id`;
  - mail-transport headers stripped from `2138` and `2400` (15 and 63 lines),
    completing an earlier strip that had left debris behind;
  - 43 files had a placeholder or fabricated value in their `From <id> Mon Sep
    17` slot replaced with `nobody`, so no false commit id remains anywhere in
    the series;
  - 28 files gained the `Message-ID` of their original submission, recovered
    from the lore git mirrors;
  - 16 files had their commit-message body restored from the original mail,
    which also restored the `Signed-off-by` they were missing.

### Verified
- The 169-patch series applies to a pristine `v7.3-rc3` tree with 0 failures and
  0 silently skipped patches (cumulative `patch -p1 --forward -F2`).

### Evaluated and not carried
- **`drm/amd/display: Try RGB before YCbCr 4:4:4 in stream validation`**
  (Adrian Betschart, dri-devel 2026-09-11). Its `amdgpu_dm_connector.c` hunk
  applies, but both hunks in the KUnit file fail, and that file is not built
  here. Carrying an extracted subset would mean shipping a behaviour change to
  stream validation — an ordering preference rather than a bug fix — so it is
  deferred rather than forced.
- **`drm/amd/display: invalidate DP CEC state on s3 suspend`** (Dan Himebauch,
  dri-devel 2026-09-12, reported tested on an RX 9070 XT). The mail is
  MIME-encoded and did not survive conversion intact. CEC is not used here, so
  it is deferred.

## [7.3.0-rc2-11-sleepy-next]: 2026-09-13

### Changed
- **`amdgpu.dcdebugmask=0x800` is gone from the built-in command line.** It was
  carried from August to mask a display artifact by disabling DCN4 idle power
  states, on the theory that IPS/DPG pipe-gating made `dc_get_flip_pending_on_otg()`
  misread a pending flip. That theory is disproved: the artifact is a COSMIC
  compositor bug (see `7.3.0-rc2-10`), and it reappeared while the mask was
  still in effect. The mask cost idle power. Re-add it if `flip_done` or vblank
  timeouts appear — the gap Leo Li documents in `f64a9be56536` is real, just not
  this machine's failure mode. The `pcie_aspm=off`, `amdgpu.aspm=0` and
  `amdgpu.runpm=0` stopgaps stay, because the drm/amd !5538 SMU bus-drop is
  still unfixed upstream.
- **The dead `--set-str DEFAULT_IOSCHED "kyber"` line is removed.** The symbol
  no longer exists (it went with the blk-mq rework), so `olddefconfig` discarded
  it silently. The NVMe scheduler is set by udev's
  `60-ioschedulers.rules`.

### Added
- **`2143`** — zstd: fix a DDict hash-set probe index wrap-around. An
  out-of-bounds write in vendored code: `ZSTD_DDictHashSet_emplaceDDict()`
  advances the probe index with `idx &= idxRangeMask; idx++;`, which leaves
  `idx == ddictPtrTableSize` when the probe starts on the last slot. Reachability
  here is low, because the DDict hash set needs multi-dictionary streaming
  decompression while zram and zswap use dictionary-less contexts.
- **The `kernel-verify` skill**, a tiered verification suite: patch hygiene,
  checksums, provenance, documented claims, skill-spec compliance and dangling
  symlinks in the fast tier; the cumulative apply in the series tier;
  `checkpatch`, `sparse`, `coccinelle` and `W=1` in the deep tier. A missing
  tool is reported as a `SKIP` with its reason, never as a silent pass.

### Fixed
- **`2138` and `2400` carried mail-transport headers**: 64 and 43 lines of
  `Return-Path`, `X-Spam-Checker-Version`, `Received` and `ARC-Seal`. Stripped.
  The diff bodies are byte-identical and the `Message-ID` is preserved.

## [7.3.0-rc2-10-sleepy-next]: 2026-09-13

### Added
- **Ten upstream fixes** from the distro-patchset and stable sweep. Eight carry
  `Cc: stable`; two are `mm-new` material.
  - **`1061`** drm/ttm bulk_move — a use-after-free. `ttm_tt_swapout()` returns a
    page count, but `ttm_bo_swapout_cb()` gates its bookkeeping on `if (!ret)`,
    so swapped-out resources never leave their bulk_move range and an endpoint
    is left dangling (`Closes` drm/amd#5387). Carried as the one-hunk original,
    *not* the botched merge `3db7d7d58341`.
  - **`1062`**, **`1063`** dma-fence — a use-after-free in which most amdgpu and
    drm_sched fences lose RCU protection after signalling, plus its doc
    companion.
  - **`2006`**, **`2007`** zram and zsmalloc — convert to the SG-list object read
    API. This machine runs zram-on-zstd swap, so it saves CPU per decompress.
  - **`2008`** io_uring — a single `IORING_ASYNC_CANCEL_ONE` cancelled in both
    the bounded and unbounded accounts, killing an unrelated operation.
  - **`2141`** mm/filemap — retain mapped dropbehind folios. Also fixes a
    sleeping-in-atomic warning on the `fadvise(DONTNEED)` path.
  - **`2142`** mm/vmscan — stop splitting mTHPs when swap is exhausted, that is,
    when zram is full. Splitting cannot make progress and only destroys the huge
    page.
  - **`2501`** x86/MCE/AMD — threshold interrupts were enabled when a storm
    started and disabled when it ended, which is backwards. The culprit commit
    is in rc2.
  - **`2600`** hrtimer — rearming a queued timer with slack left the timerqueue
    mis-sorted, so the next event could fire before the head's hard expiry.
    Mistimed wakeups affect compositor timers, `timerfd` and `poll`/`epoll`,
    that is, frame pacing.

### Changed
- **New patch range `2600–2699`** for time and timers.

### Fixed
- **The display artifact ("the box") is fixed outside the kernel.** The
  rectangular artifact over application windows was misattributed to the kernel
  from August. Three traits identified it as a COSMIC (`cosmic-comp`) bug:
  screenshots never showed it, moving the cursor over it dismissed it, and it
  appeared on whichever monitor last had VRR toggled. The compositor was handing
  fullscreen content to an overlay plane. Either setting below clears it; add
  one to `/etc/environment` and log in again.

  ```
  COSMIC_DISABLE_OVERLAY_SCANOUT=1     # sufficient on its own
  COSMIC_DISABLE_DIRECT_SCANOUT=1      # also works; removes the overlay bit too
  ```

  No kernel change is involved. The `dcdebugmask=0x800` workaround that fixed
  this in August and then stopped working was the signal that the cause had
  changed. The evidence chain is in `LESSONS.md`.

## [7.3.0-rc2-9-sleepy-next]: 2026-09-13

### Added
- **`1158`** — DMCUB busy-wait fix (Sultan Alsawaf, `dfd0e5aa6aad`).
  `dmub_srv_wait_for_idle()` polls with `udelay(1)` in a loop bounded by
  `timeout_us`, and callers pass up to 100000 — as much as 100 ms of CPU
  spinning per call, on the DMCUB path DCN401 uses. Replaced with progressive
  backoff using `usleep_range()` when `preemptible()`, so the CPU can reach
  idle. Out-of-tree, so it will not arrive on a version bump; it is a
  self-contained function, which keeps the carry cost low.

## [7.3.0-rc2-8-sleepy-next]: 2026-09-13

### Added
- **HDMI RGB quantization fix (`1155`–`1157`)** — Satyajit Roy's
  `[PATCH 0/3] drm/amd/display: Fix HDMI RGB quantization updates`. Post-rc2
  upstream work. `resource_build_info_frame()` derives colorimetry and RGB
  quantization from `stream->output_color_space`, but the InfoFrame-update
  predicates did not include `output_color_space`; a commit that changes the
  colour space therefore reprogrammed the output CSC while the sink kept the
  previous AVI InfoFrame range, leaving source and sink disagreeing about RGB
  limited-versus-full range. `1157` adds the missing predicate at the three
  sites in `dc/core/dc.c`. Prompted by drm/amd work item **!5812**, which
  reports on an RX 9070 XT (DCN401) that toggling Adaptive Sync raises or clears
  washed-out colour every time — the same VRR-toggle trigger this machine shows.
  The desync is screen-global, so this is carried as an on-target correctness
  fix, not as a confirmed cure for the artifact.
- **Five upstream fixes** from the MM/PM/sched sweep:
  - **`2139`** mm/vmscan — avoid anon scanning for `GFP_NOIO` with low swapcache.
    Explicitly a zRAM optimisation, and live here: it uses the
    `vmscan_can_reclaim_anon_pages()` wrapper LRU-MARIE adds.
  - **`2140`** mm/page_alloc — avoid direct compaction for costly `__GFP_NORETRY`
    allocations, which removes a cross-CPU drain-IPI storm on the buffered-write
    path. Its regression source is in rc2.
  - **`2401`**, **`2402`** sched/eevdf — fix the augmented `max_slice`, and fix
    rbtree corruption where only one of three augmented fields propagated.
  - **`2500`** x86/mm — a one-line data-loss fix: `pmd_modify()` masked out
    `_PAGE_DIRTY` where `pte_modify()` and `pud_modify()` do not, so pages
    rewritten after `MADV_FREE` on a PMD-mapped THP could be discarded.

## [7.3.0-rc2-7-sleepy-next]: 2026-09-12

### Changed
- **The repository became single-package.** The root 7.2 `linux-sleepy` package
  was dropped, and `linux-sleepy-next` in `sleepy-next/` became the only
  package. Two couplings had to be cut first: its `prepare()` read `../config`,
  and it deliberately did not install `net-tune` because the 7.2 package owned
  it.
- **`linux-sleepy-next` now ships `net-tune`** (CAKE SQM plus low-latency
  ethernet tuning) and enables the service. The shipped template defaults to
  `ENABLE_SQM=yes` at 80/80 Mbit, so an unattended build installs shaping rather
  than silently disabling it. Set your real line rate in `/etc/net-tune.conf`.
- **`/etc/net-tune.conf` is now a pacman backup file.** Without `backup=()`,
  pacman would overwrite local edits on every kernel upgrade, which matters now
  that the service ships enabled with a placeholder line rate.

### Added
- **MGLRU v3 (`2131`–`2137`)** — Barry Song's `mm/mglru: speed up inc_min_seq()
  and fix cold/hot inversions`, from akpm's `mm-unstable`. Batches the per-folio
  work in `inc_min_seq()` and fixes hot/cold inversion by keeping promoted
  folios ahead.
- **`2138`** — memcg: trim the per-cpu charge stock instead of draining it,
  splitting the high watermark from its emptying target.
- **`2400`** — sched: set the need-resched flags before tracing. The unpatched
  order emitted the tracepoint before setting the `TIF` bit, so a BPF tracepoint
  program could recurse through `rcu_read_unlock_special()` into a kernel stack
  overflow. Relevant here, because this package ships `bpftune` and runs
  sched-ext.

### Removed
- **The dangling ADIOS config.** `PKGBUILD` ran `scripts/config -e
  MQ_IOSCHED_ADIOS`, `config` set `CONFIG_MQ_IOSCHED_ADIOS=y`, and `provides=()`
  listed `ADIOS-MODULE`, but no patch adds `block/adios.c`, so `olddefconfig`
  dropped the symbol and the package advertised a module it did not ship.

### Changed
- **New patch range `2400–2499`** for the core scheduler.

## [7.3.0-rc2-6-sleepy-next]: 2026-09-12

### Changed
- **LRU-MARIE updated to the author's official 0.11.1 port for 7.3.** firelzrd
  ships `patches/testing/0001-linux7.3-rc1-lru_marie-0.11.1.patch`, an
  author-written port that applies cleanly to this base. It supersedes the
  hand-rebased 0.11.0, which needed a "legacy writeout" shim to re-provide the
  per-folio swap helpers that 7.3 deleted; the author instead adapts MARIE to
  the native `swap_ops.h` and `swap_io_ctx` path. Two build-artifact sections
  the patch bundled (`localversion`, `scripts/setlocalversion`) were stripped.

## [7.3.0-rc2-5-sleepy-next]: 2026-09-10

### Added
- **The final pieces of AMD's Linux 7.4 HDMI 2.1 pull (`1152`–`1154`).** The
  core was already carried (`0059` HDMI 2.1 FreeSync, `0060` HDMI 2.1 VRR,
  `0061` ALLM, `1144` FRL by default, `1150`/`1151` passive VRR); this adds emit
  VTEM for HF-VSDB VRR on TMDS links, fix HF-VSDB DSC bpc detection to be
  cumulative, and fix a NULL dereference of `new_stream->sink` in the VTEM
  guard.

## [7.3.0-rc2-4-sleepy-next]: 2026-09-09

### Added
- **Passive VRR (`1150`, `1151`)** — Tomasz Pakuła's passive VRR series. Keeps
  the sink in its variable-refresh state during fixed-refresh desktop use,
  avoiding the blanking and flicker HDMI sinks show on VRR entry and exit. Part
  3/3 is the HF-VSDB MCCS fix already carried as `1145`. The author header was
  de-MIME-encoded to the proper UTF-8 name.

## [7.3.0-rc2-3-sleepy-next]: 2026-09-09

### Removed
- **The two DCN4 flip-schedule patches (`9051`, `9052`).** AMD is reverting both
  upstream for causing a regression: `Revert "drm/amd/display: Fix
  CalculateFlipSchedule Calculation"` and `Revert "drm/amd/display: Unify
  CalculateFlipSchedule Logic"`, each stating *"Because it causes some
  regression"*. Both land in `dml2_core_dcn4_calcs.c`, which is DCN4 — this GPU.
  The un-reverted "fix" makes the flip-bandwidth math more conservative, by
  adding `meta_row_bytes` and halving `row_time_budget`, which mis-schedules
  flips.

### Added
- **The kbuild build-speedup series (`2300`–`2322`)** — Lorenzo Stoakes'
  `[PATCH 00/23] kbuild: significantly speed up kernel builds`. Up to 36% faster
  full builds and about 90% faster no-op builds, which matters for this
  project's build loop. All 23 apply cleanly.

### Changed
- **New patch range `2300–2399`** for the build system.

## [7.3.0-rc2-2-sleepy-next]: 2026-09-07

### Changed
- **Moved off the linux-next snapshot line onto Linux 7.3-rc2 (mainline).** The
  post-rc1 linux-next bases (0902 and 0904) carried unfixed upstream RDNA4
  display bugs that froze and panicked this RX 9070 XT: drm/amd work items
  #5722 (`duplicate_state` panic), #5684 (optc `REG_WAIT` hang) and
  #5759/#5763 (MES wedge). rc2 sidesteps the linux-next mm churn and is the
  actual release-candidate line.
- **LRU-MARIE 0.11.0 ported to rc2.** The `mm/lru_marie/` subsystem stays
  byte-identical to firelzrd's 0.11.0, apart from the three earlier one-line
  compile fixes for the base API. The three host-file hooks were re-anchored to
  rc2's renamed and simplified code.
- **Series reconciled for rc2**: 121 patches. Dropped 19 that linux-next 0902 to
  0904 merged upstream, the retry-fault, flip-schedule and userq groups that
  also landed, `1059` (merged in rc2) and `1139` (code changed).
- **VRR fix in `pkgrel 2`.** The local `1137` — a hand-rolled MCCS VCP re-enable
  that force-enabled VRR from the kernel-parsed AMD VSDB — was replaced with
  Fangzhi Zuo's upstream `1145`, which skips the MCCS `freesync_capable` clear
  when the sink advertises HF-VSDB VRR. VRR now engages the way AMD intends
  rather than through a local hack.

### Fixed
- **The recurring freezes and the boot NULL-oops were upstream RDNA4 display
  bugs in the 0902+ linux-next bases**, not this series. Reproduced on a stock
  CachyOS release kernel and matched to open upstream work items.

## [7.3.0-rc1-13-sleepy-next-20260902]: 2026-09-02

### Added
- **LRU-MARIE 0.11.0 carried verbatim**, byte-identical to firelzrd's patch,
  with only two compile-fix lines and a clearly separated legacy-writeout shim
  that re-provides the per-folio swap helpers linux-next deleted.

### Changed
- Base bumped to linux-next `next-20260902`. The series dropped 11 patches
  merged upstream (CLIFF FRL cap and restore, HPD filter, FRL link-training
  timeout, overlay cursor, dw estimate, no-retry PTE, flip-schedule fixes,
  clamp-dcfclk, sched-ext DSQ and unify-flip-schedule), and three were rebased.
  Series: 112 patches.

## [7.3.0-rc1-12-sleepy-next-20260901]: 2026-09-02

### Added
- **LRU-MARIE 0.11.0 ported to the linux-next base**, replacing the version that
  never applied. MARIE is a memory-reclaim accelerator: a per-PFN reclaim-state
  byte array, a SIMD young-bit walker, and a `kcompressd` async-compression
  thread with bio-coalesced swapout and an early-OOM gate. The 7.3-merge mm had
  diverged (memcg soft-limit removal, mglru refactor, `page_io.c` rewritten
  around `swap_io_ctx`, `alloc_context` moved), so the port base-fit those.
- The latest mm, mglru and memcg fixes from `next-20260901`.

### Changed
- **Dropped 20 patches** that target the 7.2-era base and do not apply to the
  7.3-merge tree; the build had been skipping them silently. They were 7.2-only
  CachyOS squashes, SMU14, amd-pstate, ttm and gfx12 backports, early DCN4
  backports the base's newer code supersedes, a zram out-of-bounds fix, and one
  userq fix. Series: 123 patches.

## [7.2.0-10-sleepy-next-20260828]: 2026-08-28

The last release on the linux-next preview line before the move to mainline rc2.

### Fixed
- **Six patches from `-9` were empty no-ops** and are now applied for real: the
  VM-update GPU-hang fix, the GFX12 no-retry PTE fix, the DCN4 flip-schedule
  pair, and the display IRQ guard.

### Changed
- Dropped 76 patches whose content `next-20260828` upstreams. Series: 143
  patches.

## [7.2.0-9-sleepy-next-20260828]: 2026-08-28

### Added
- Eight patches from the amd-staging branch and the mailing lists: a GPU-hang
  fix for the VM page-table update path (`Cc: stable`), GFX12 no-retry PTE
  flags, two DCN4 flip-schedule fixes, a DCN42 idle-power hang fix, HDMI 2.1 FRL
  enabled by default, a user-queue deadlock fix, and a display-IRQ teardown
  guard.

## [7.2.0-8-sleepy-next-20260828]: 2026-08-28

### Changed
- Base bumped from `next-20260827` to `next-20260828`. This snapshot upstreams a
  large batch of AMD driver fixes that were being carried as patches, which made
  roughly 70 of them redundant. The 22 AMD commits in the delta are included.

## [7.2.0-7-sleepy-next-20260827]: 2026-08-27

### Added
- **23 patches** surfaced by a sweep of the lkml archives, the AMD display and
  power-management mailing lists, the AMD bug tracker, and the drm-next,
  amd-staging and drm-misc trees: a 15-patch ACPI CPPC rework that `amd-pstate`
  uses on Zen 4, three zstd BMI2 probe patches, three display robustness fixes,
  a boot-time SR-IOV workaround guard, and a sched-ext allocation cleanup.

## [7.2.0-6-sleepy-next-20260826]: 2026-08-26

### Fixed
- **The "box" artifact was masked in-kernel** by adding
  `amdgpu.dcdebugmask=0x800` to the built-in command line, so it no longer
  depended on a boot argument. Root cause at the time was understood to be
  display idle-power making the driver report an update complete before the
  hardware latched it. This mask was removed in `7.3.0-rc2-11` once the real
  cause turned out to be in the compositor.

## [7.2.0-5-sleepy-next-20260825]: 2026-08-26

### Added
- DCN4 cursor and plane fixes carried from upstream: colour-management state on
  plane recreate, a blend-mode property warning fix, and an overlay-cursor
  fallback.

### Fixed
- **HDMI variable refresh rate** is now offered on the HDMI outputs. The
  firmware path missed FreeSync panels; the driver reads the panel's advertised
  ranges directly.
- The "box" artifact was first worked around with `amdgpu.dcdebugmask=0x800` on
  the boot entry.

## Earlier packages

Both of the following were removed from the working tree. Their `PKGBUILD`,
`patches/` and `config` trees remain in git history, as do their full changelog
entries: `git log --follow CHANGELOG.md`, and
`git show 34e0f98:CHANGELOG.md` for the text as it stood before this file was
consolidated.

### 7.2 `linux-sleepy` (dropped 2026-09-12)

The repository's original package. It was dropped in favour of the single 7.3
package; the `net-tune` service it owned moved to `linux-sleepy-next`.

| Version | Date | Summary |
|---|---|---|
| `7.2.0-2-sleepy` | 2026-08-19 | 17 verified sweep candidates merged; series 157 → 174 patches. |
| `7.2.0-1-sleepy` | 2026-08-19 | Base moved to Linux 7.2 stable; the FAIR revert series dropped as obsolete. |
| `7.2.0-rc7-8-sleepy` | 2026-08-15 | zstd 1.6.0 with the gcc-BMI2 segfault guard. |
| `7.2.0-rc7-7-sleepy` | 2026-08-15 | Six-source sweep; series 179 → 184 patches. |
| `7.2.0-rc7-6-sleepy` | 2026-08-14 | `1053`, an AI-proposed DRM scheduler `min_vruntime` fix. |
| `7.2.0-rc7-5-sleepy` | 2026-08-14 | Seven backports from the `amd-drm-next-7.3-2026-08-12` tag. |
| `7.2.0-rc7-4-sleepy` | 2026-08-12 | Added `amdgpu.aspm=0` and `amdgpu.runpm=0` stopgaps. |
| `7.2.0-rc7-3-sleepy` | 2026-08-12 | Full revert of the DRM scheduler FAIR series; FIFO default restored. |
| `7.2.0-rc7-2-sleepy` | 2026-08-12 | Maintenance sweep; series 151 → 154 patches. |
| `7.2.0-rc7-1-sleepy` | 2026-08-11 | Maintenance sweep; series 140 → 151 patches. |
| `7.2.0-rc7-1-sleepy` | 2026-08-10 | Bump to Linux 7.2-rc7; series 127 → 140 patches. |
| `7.2.0-rc6-7-sleepy` | 2026-08-04 | Bump to Linux 7.2-rc6; 36-patch sweep, `net-tune` introduced. |
| `7.2.0-rc5-1-sleepy` | 2026-08-02 | First maintained release; series renumbered into ranges. |

`7.2.0-rc7-1` was used twice, on 2026-08-10 and 2026-08-11.

### `wannabe-7.3-rc1` (2026-08-26, removed 2026-09-02)

A git-worktree preview built from `next-20260825` ahead of the 7.3-rc1 release,
with its own `wannabe-7.3-patches/` series and `WANNABE-7.3.md`. It was
superseded by the `sleepy-next` package, which carries the same content: the
`mm/gup` batching series (`2120`–`2127`), the HDMI VRR and ALLM patches
(`0059`–`0061`), and the userq and KFD work in the `9000` range.
