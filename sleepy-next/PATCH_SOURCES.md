# sleepy-next — patch provenance

## 2026-09-13 — HDMI RGB quantization fix + six verified fixes (165 patches)

**Added — `1158`, DMCUB busy-wait fix.** Sultan Alsawaf (kerneltoast),
`drm/amd/display: Fix high busy wait load in dmub_srv_wait_for_idle()`, commit
`dfd0e5aa6aad` on his `kernel_x86_laptop` tree (branch `v6.16-sultan`,
2025-08-25).

`dmub_srv_wait_for_idle()` polls with `udelay(1)` in a loop bounded by
`timeout_us`, and callers pass up to **100000** — i.e. as much as 100 ms of pure
CPU spinning, per call, in the DMCUB path that **DCN401 uses**
(`dc_dmub_srv.c:165,283`). The patch replaces the fixed 1 µs spin with
progressive backoff: 1 µs for the first 3 iterations, then 10 µs, then 100 µs,
using `usleep_range()` when `preemptible()` so the CPU can actually idle.
Verified live here: `CONFIG_PREEMPT=y` and `CONFIG_PREEMPT_COUNT=y`, so the
sleeping path is taken.

Applies cleanly — `rc=0`, offset 178 only (the hunk header is stale from a 6.16
base; the context is byte-identical in rc2). Out-of-tree, so it will not arrive
on a version bump; it is a self-contained function, which keeps the carry cost
low. Note it fixes `wait_for_idle()` only — `wait_for_pending()` immediately
above it has the same pattern and is untouched.

**Evaluated and not taken from the same tree:**
- The kswapd trio (`1e10be67699e`, `0a28ea9693cb`, `4632bdecee3e` — *Stop kswapd
  early* / *Don't stop kswapd on a per-node basis* / *Increment kswapd_waiters*)
  is a genuinely desktop-targeted series, but it **fails to apply**: 2 of 3 hunks
  in `mm/page_alloc.c` and the `mm/internal.h` hunk are rejected, because LRU-MARIE
  (`2101`) rewrites those same files. It needs a deliberate rebase against the
  series state, not a mechanical fix.
- `47b020a24ae3` (*Revert "cpumask: limit FORCE_NR_CPUS to just the UP case"*) is
  inert unless `CONFIG_NR_CPUS` is exactly 16 **and** `CONFIG_FORCE_NR_CPUS=y`
  (ours is 512 for hotplug headroom). Upstream restricted it to UP precisely
  because a wrong `NR_CPUS` breaks the kernel — **not worth the risk**.
- `e5b7e9d87ace` (*Lower the non-hugetlbpage pageblock size*) is **superseded
  upstream** by `CONFIG_PAGE_BLOCK_MAX_ORDER` (currently 10 in our config), so it
  is a config-only lever — and lowering it with `TRANSPARENT_HUGEPAGE_ALWAYS=y`
  + `HUGETLBFS=y` risks both THP success and 2 MB hugetlb (the Kconfig help says
  so). Not taken.

**Already carried, confirmed at runtime (do not re-add):**
`vm.watermark_boost_factor=0` and `vm.compaction_proactiveness=0` are live via
the CachyOS `0110` config hooks under `CONFIG_CACHY` (which `PKGBUILD` forces on
with `scripts/config -e CACHY` — note `config:43` still reads
`# CONFIG_CACHY is not set`, so the config file alone is misleading here). And
our `0111-cachy-acpi-disable-bus-master-check-for-AMD.patch` **is** kerneltoast's
patch verbatim, re-applied to 7.3 by CachyOS under the same `From:` line — his
work is already partly ingested.

**kdrag0n and tytydraco: nothing applicable.** Every kernel repo of theirs is
Android/ARM/device-specific (kdrag0n's kernel work is device trees plus GKI 6.1
under the GrapheneOS org; tytydraco has no kernel patch repo at all), and all
their generic mainline commits are already ancestors of `v7.3-rc2`.

**Added — five upstream fixes from the MM/PM/sched sweep**, each verified with a
cumulative apply on top of the full series (all clean, small offsets only):

| Patch | Subject / author | Why it is on-target here |
|---|---|---|
| `2139` | `mm: vmscan: avoid anon scanning for GFP_NOIO with low swapcache` — Bo Zhang, 2026-09-08, `09c1d29a3d1e` / `20260908062649.1045883-1-zhangbo56@xiaomi.com` (akpm `mm-unstable`) | The commit message is explicitly about **zRAM** (*"particularly true on systems using zRAM, where swapcache is relatively rare"*): avoids >150 ms `shrink_folio_list()` passes that reclaim nothing. Its `lru_gen_enabled()` guard passes through under Marie, and it uses `vmscan_can_reclaim_anon_pages()` — the wrapper `2101` adds for exactly this — so unlike the MGLRU work this is **live here**. |
| `2140` | `mm/page_alloc: avoid direct compaction for costly __GFP_NORETRY allocations` — Salvatore Dipietro, 2026-09-11, `60adb47f4fa3` / `20260911142102.2294202-1-dipiets@amazon.it` | Suppresses direct compaction and the `drain_all_pages()` cross-CPU IPI storm for costly `__GFP_NORETRY` orders. Its regression source `5d8edfb900d5` (iomap large-folio writes) **is in rc2**. Desktop-stutter class. |
| `2401` | `sched/eevdf: Fix augmented max_slice` — Vincent Guittot, 2026-09-07, `9a8bc9bb4c3f` | 2-line initialisation of `se->max_slice` before `__enqueue_entity()`. rc2 **contains the regression source** `6e3c0a4e1ad1` ("Fix lag clamp"), so we carry the bug today. |
| `2402` | `sched/eevdf: Fix rb augmented with multi fields` — Vincent Guittot, 2026-09-09, `51b0e68cfa0a` | Adds `RB_DECLARE_CALLBACKS_MULTI` so all **three** augmented EEVDF fields propagate on rotate/copy; previously only one did, corrupting the rbtree the scheduler depends on. Applied after `2401` (its ancestor). |
| `2500` | `x86/mm: Fix user-space data loss with MADV_FREE and THP` — Vernon Yang, `f7491d7c81db` | **1-line real data-loss fix**: `pmd_modify()` masks out `_PAGE_DIRTY` (line 809 in rc2) where `pte_modify()`/`pud_modify()` do not, so pages rewritten after `MADV_FREE` on a PMD-mapped THP can be discarded. Needs THP + reclaim pressure + `MADV_FREE` (jemalloc → Firefox/Chrome): all true here. `Cc: stable`, `Reviewed-by` Edgecombe, `Tested-by` Falcato. |

Note on `2500`: the fix was sent twice, and merged into **two** tip trees —
`821eaec4482a` (`[PATCH] x86/mm: Fix pmd_modify() dropping the dirty bit`,
2026-09-03) and `f7491d7c81db` (`[tip: x86/mm] x86/mm: Fix user-space data loss
with MADV_FREE and THP`, 2026-09-08). The hunks are **byte-identical**; we carry
one, under the merged tip subject.

**Not taken from that sweep, deliberately:** the other two commits in
`sched-urgent-2026-09-13` (`c23810313bdf`, `f5741d2b3451`) are *proxy-execution*
work, not standalone fixes; sirlucjan's zstd 7.3 refresh breaks our `2128`/`2130`
BMI2 patches and needs a rebase; the MCE v6 series arrives via Outlook and would
need reconstruction (see `LESSONS.md`); `r8169` LTR is latent only while we boot
`pcie_aspm=off`.

### HDMI RGB quantization fix (`1155`–`1157`)

**Added — the HDMI RGB quantization series (`1155`–`1157`).** Satyajit Roy,
`[PATCH 0/3] drm/amd/display: Fix HDMI RGB quantization updates`, posted
2026-08-30 (`20260830035120.937992-1-edu042sjroy@proton.me`, amd-gfx):

| Patch | Subject |
|---|---|
| `1155` | `drm/amd/display: Propagate HDMI RGB quantization selectability` |
| `1156` | `drm/amd/display: Honor Broadcast RGB for BT.2020 RGB output` |
| `1157` | `drm/amd/display: Rebuild InfoFrames on output color space changes` |

**Why.** drm/amd work item **!5812** (2026-09-12) reports that on an RX 9070 XT
(DCN401) *"toggling Adaptive Sync between 'Never' and 'Automatic'/'Always'
reproduces or clears [raised black levels / washed out colours] immediately,
every time"*. The mechanism: `resource_build_info_frame()` derives colorimetry
and RGB quantization from `stream->output_color_space`, but the InfoFrame-update
predicates did not include `output_color_space` — so a commit that changes the
colour space (which is what a VRR toggle is) reprograms the output CSC while the
sink keeps the **previous AVI InfoFrame range**. Source and sink then disagree
about RGB limited-vs-full range. `1157` is the fix: it adds
`stream_update->output_color_space ||` to the three predicates in
`dc/core/dc.c` (`check_update_surfaces_for_stream`,
`commit_planes_do_stream_update_sequence`, `commit_planes_do_stream_update`).
Verified after applying: all three insertions landed in the intended
predicates.

**Provenance / status.** Post-rc2 — `merge-base --is-ancestor` confirms
`bdcd0411d7d1` (`Propagate HDMI RGB quantization selectability`, linux-next
20260911) and `a56a5007452c` (amd-staging) are **not** in `v7.3-rc2`, so our
HDMI path does not have the fix. The series is in linux-next and
`amd-staging-drm-next`, i.e. accepted AMD work. We carry `6eb4c13a3845`
("Support 'Broadcast RGB' drm property") in the rc2 base, so the property itself
already exists.

**Extraction note.** The mails are **quoted-printable** encoded; they must be
decoded with a MIME parser before applying, or every hunk fails
(`=09` is a tab). Decoded here with Python's `email` module, headers preserved.
Production payload is small: 1 line in `amdgpu_dm_helpers.c`, the connector
colour-space handling in `amdgpu_dm_connector.c`, and the 3 lines in `dc.c`.
`1156` also touches the KUnit file `amdgpu_dm/tests/amdgpu_dm_connector_test.c`,
which is not built (`CONFIG_KUNIT` is unset on this machine).

**Caveat recorded honestly:** a quantization-range desync is *screen-global*, so
this does not by itself explain a rectangular "box" artifact. It is carried as a
real, on-target correctness fix whose trigger (a VRR-toggle atomic commit on
DCN401 over HDMI) matches the user's trigger exactly.

**Audit.** The full **159-patch series applies to pristine v7.3-rc2 with 0
failures** (cumulative `patch -Np1 --forward`).

## 2026-09-12 — MM/sched optimizations + ADIOS cleanup (156 patches, pkgrel 7)

Six-source sweep (linux-mm, akpm `mm-unstable`, linux-pm, sched-ext/lkml,
block/net/fs, sirlucjan). Nine patches added; all nine were verified by
**cumulative apply against a pristine v7.3-rc2 worktree on top of the full
147-patch series** — the whole 156-patch series now applies with 0 failures and
0 `SKIPPED` (the runner dry-run-gates and prints `SKIPPED:` for any miss).

**Added — MGLRU v3 (`2131`–`2137`).** Barry Song (Xiaomi), `mm/mglru: speed up
inc_min_seq() and fix cold/hot inversions`, v3 posted 2026-09-02
(`20260901232421.40157-1-baohua@kernel.org`), in akpm `mm-unstable` as
`54e9345e4563`, `521a7c952c89`, `3384a49a865e`, `e25d6c041ca0`, `efac6d51d1d6`,
`81cb06a097b3`, `64fff1e3d929` (extracted with `git format-patch`). Batches the
per-folio work in MGLRU `inc_min_seq()` — `nr_pages` update, gen→gen moves, an
inlined prefetch helper — and fixes hot/cold inversion by keeping promoted
folios ahead. Reviewed (`R-b` Kairui Song, Baolin Wang, Lian Wang, Ridong Chen;
`Tested-by`), heading for 7.4. MGLRU ages on every reclaim here
(`CONFIG_LRU_GEN=y`), so this cuts sys time in the memory-pressure window that
causes desktop/game stutter. Applies mm/vmscan.c with offsets only; `2135` takes
1 hunk at fuzz 1.

**Added — `2138`, memcg per-cpu charge stock.** Shakeel Butt,
`memcg: trim the per-cpu charge stock instead of draining it`, v2
(`20260820012010.2016086-1-shakeel.butt@linux.dev`), `Acked-by: Michal Hocko`,
in `mm-unstable`. Splits the percpu-stock high watermark from its emptying
target (the page-allocator `pcp->batch` idiom) instead of thrashing the stock;
measured 44.6–57% of CPU in charge/uncharge for request/response patterns.

**Added — `2400`, need-resched ordering fix.** Andrea Righi (NVIDIA),
`sched: Set need-resched flags before tracing`
(`20260911213300.1305763-1-arighi@nvidia.com`). Sets the TIF bit *before*
emitting `sched_set_need_resched_tp`, in both `set_tsk_need_resched()` and
`__resched_curr()`. rc2 still traces first, and the unfixed order lets a BPF
tracepoint program recurse through `rcu_read_unlock_special()` until kernel
stack overflow — live risk here because we ship bpftune and run sched-ext. Clean
apply; no other patch in the series touches `kernel/sched/core.c`.

**New range:** `2400–2499` = core scheduler (non-CachyOS). Chosen because the
existing ranges cover block/IO schedulers (`2000`), memory (`2100`), CPU idle
(`2200`) and kbuild (`2300`), but not sched core / EEVDF.

**Removed — the dangling ADIOS config (both packages).** `PKGBUILD` ran
`scripts/config -e MQ_IOSCHED_ADIOS`, `config` set
`CONFIG_MQ_IOSCHED_ADIOS=y`, and `provides=()` listed `ADIOS-MODULE`, but **no
patch in either tree adds `block/adios.c`** — so `olddefconfig` silently dropped
the symbol and the package advertised a module it did not ship. Confirmed on the
running kernel: `/sys/block/nvme0n1/queue/scheduler` → `none mq-deadline
[kyber] bfq` (no `adios`). The dead config line, the `-e MQ_IOSCHED_ADIOS` flag
and the `ADIOS-MODULE` provides entry are removed from both `PKGBUILD`s and both
`config` files. `DEFAULT_IOSCHED=kyber` was already in effect and is unchanged.
sirlucjan's ADIOS 3.3.0 patch is available (`block/adios.c`, 2062 lines) if we
ever want the scheduler itself.

**Considered and not taken:** the Reflex cpufreq governor (`0.3.1r2`, verifies
clean — the 7.2-era "cpufreq API 4→5" deferral is obsolete, and it shares no
files with our series) and the nvme-pci adaptive-interrupt-polling v2 series
(patch 1 applies, patch 2 needs a rebase — 1 of 20 hunks). Also rejected:
hrtick repick v2 (needs rebase, collides with `0105`/`0113` regions),
sched_ext lazy preemption (inert — `CONFIG_PREEMPT_LAZY` unset), Hugh Dickins'
26-patch fbatch (needs two `mm-hotfixes-stable` prereqs, perf unproven), Jan
Kara's deferred inode reclaim (still in review), CPPC v6 (hardening, not perf).

## 2026-09-09 — full series audit (142 patches)

Base moved from linux-next snapshots to mainline **Linux 7.3-rc2** (the
linux-next 0902+ bases carried unfixed RDNA4 display bugs — see CHANGELOG).
Full audit of the series against a pristine v7.3-rc2 tree:

- **All 142 patches apply cleanly** (`patch -p1 --forward -F2`, cumulative), 0
  rejected, 0 silently skipped/inert.
- **Dropped this cycle:** `9051`/`9052` (DCN4 flip-schedule — AMD is reverting
  both upstream, *"causes some regression"*, in `dml2_core_dcn4_calcs.c`);
  `1059` (BAR0, merged in rc2); `1137` (local MCCS hack, replaced by the
  upstream `1145`); `1139` (blend-mode, already in rc2 base); 19 patches merged
  by linux-next 0902–0904.
- **Added:** `1145` (upstream HF-VSDB MCCS FreeSync fix, Fangzhi Zuo) and the
  23-patch **kbuild build-speedup series** `2300`–`2322` (Lorenzo Stoakes,
  rust-for-linux 2026-09-08, `20260908-build-speedup-v1-0-5dc1ac01672d@kernel.org`).
- **New range:** `2300–2399` = build system / kbuild.

### Handmade patches (0001–0007, 0030–0034) — reviewed 2026-09-09

All 12 are small, single-purpose fixes (1–17 added lines each), verified
against the rc2 source:

| Patch | Fix | Verified |
|---|---|---|
| `0001` | typo `tyep`→`type` in `smu_v14_0_set_irq_state` | cosmetic |
| `0002` | free `user_overdrive_table` in `fini_smc_tables` (separate kzalloc — real leak) | correct |
| `0003` | PROFILE_PEAK GFXCLK ceiling floats (firmware boost >3.0 GHz) | correct |
| `0004` | deep sleep off while PROFILE_PEAK/COMPUTE active | correct |
| `0005` | `is_mode1_reset_supported`: false for SR-IOV VF | correct |
| `0006` | bounds-check `SwI2cCmds[c]` against `MAX_SW_I2C_COMMANDS` | correct |
| `0007` | drop redundant `adev->pm.mutex` around `smu_cmn_update_table` (self-deadlock hazard) | correct |
| `0030` | proactively shrink DET for pipes losing space | correct |
| `0031` | free `enc20` before the hpd_source bounds return (leak) | correct |
| `0032`/`0033` | `hpo_frl_link_enc_regs[1]`→`[2]` + second `reg_list(1)` (OOB) | correct |
| `0034` | move `dal_irq_service_destroy` out of the per-pipe loop (double-destroy) | correct |

Headers normalised to upstream quality: author `Sleepy <sleepy@localhost>`,
matching `Signed-off-by`, `Assisted-by: Claude <noreply@anthropic.com>`, and
leftover `[PATCH n/36]` series numbering stripped.

`linux-sleepy-next` builds the **wannabe 7.3-next preview** kernel from the
linux-next **next-20260825** snapshot + the sleepy 7.2 patch series (the same
patches the `linux-sleepy` 7.2 build uses) + the clean upstream HDMI VRR/ALLM
patches. See `../PATCH_SOURCES.md` (the 7.2 ledger) for the 173 shared patches
— every one is the identical, traceable 7.2 series file (CachyOS squashes,
upstream ML patches, agd5f backports, local patches).

## Base

- `next-20260825` snapshot (the 7.3 merge-window content).
- Toolchain: official **LLVM 23.1.0** release from the llvm-project GitHub
  release (the prebuilt binary links ICU 70; Arch ships ICU 78, so the ICU 70
  libs are bundled via `llvm-icu70-libs.tar.gz`).

## Excluded from the 7.2 series

- **`0107-cachy-hdmi`** — the CachyOS HDMI branch. The 7.3 base already has the
  clean upstream HDMI path (`dc_edid_parser` + `amdgpu_dm_update_freesync_caps`
  in the split connector file + FRL fixes). Shipping it would conflict.
- **LRU-MARIE (`2101`)** — 0.10.5 does not port to 7.3 (12+ hunks fail across
  huge_memory/rmap/vmscan/page_io). Skipped cleanly by `patch --forward`;
  re-evaluate when a 7.3 port exists.

## Added (clean upstream, vanilla)

The HDMI 2.1 VRR + ALLM v4 series (amdgpu-side, amd-gfx ML 2026-08), replacing
the earlier squash — each is the original submission:

| Patch | Author | ML Message-ID | Content |
|---|---|---|---|
| `0059` | Fangzhi Zuo | `150622` (lists.freedesktop.org amd-gfx 2026-August) | Add 2.1 FreeSync support for AMD VSDB EDID Block — `SIGNAL_TYPE_HDMI_FRL` FreeSync + VTEM info packet |
| `0060` | Fangzhi Zuo | `150623` | Add HDMI 2.1 VRR support from HF-VSDB — VRR-range fallback when the AMD VSDB has none |
| `0061` | Fangzhi Zuo | `150621` | Enable HDMI ALLM for Gaming-VRR — `ALLM_Mode` in the HF-VSIF |

The drm/edid part of the series (`150619`, HF-VSDB gaming caps) is already
present as `0055` (the 7.2 series' Fangzhi Zuo HF-VSDB patch).

## Verification

Every patch is applied with `patch -p1 --forward -F2` and a dry-run check:
patches that do not apply cleanly to next-20260825 (e.g. MARIE) are skipped
entirely, never half-applied. The VRR/ALLM series is verified to apply on
next-20260825 + the 0050s, with the HF-VSDB VRR fallback and
`drm_connector_attach_vrr_capable_property` present in the built kernel.

## Added (Phoronix 08-11 WIP — RFC, 7.4-target)

The `mm/gup` follow_page_mask() batching series (Rik van Riel, Meta; RFC v3,
lkml `20260811025157.1632867-1-riel@surriel.com`) — up to 12.8× in gup_test on
mTHP paths (GPU userptr, io_uring, VMA walkers). Phoronix 08-11 "Up To 12.8x
Improvement Observed For gup_test". Not in next-20260825 (targets 7.4);
applies cleanly. 8 patches, `2120`–`2127`, each with the original
From:/Signed-off-by: (Rik van Riel) preserved. Marked RFC — re-evaluate when
it lands upstream (7.4).

## Added (local fix, 2026-08-26)

- **`0040`** — drm/amd/display: fall back to DRM-core AMD VSDB FreeSync info.
  The amdgpu-side `parse_hdmi_amd_vsdb()` relies on the DMUB/DMCU firmware to
  report the AMD VSDB; on RDNA4 the firmware does not detect it, leaving
  `vrr_capable=0` even for displays that advertise FreeSync via the AMD VSDB
  (verified: modetest `vrr_capable: 0` on an HDMI display whose EDID has AMD
  VSDB v2, Feature Caps 0x09, 48-120 Hz). `drm_edid.c` (patch `0050`) already
  parses the AMD VSDB kernel-side into `connector->display_info.amd_vsdb`
  (`freesync_supported`, `min/max_frame_rate`) for v1/v2/v3 — use it as a
  fallback in `amdgpu_dm_update_freesync_caps()` when the firmware path found
  nothing. Local fix (Sleepy + Claude-assisted), applies on top of the
  VRR/ALLM series.

## Fixed (cmdline, 2026-08-26) — DCN401 "box/square" artifact

Not a patch: `amdgpu.dcdebugmask=0x800` (`DC_DISABLE_IPS`) added to the
built-in CMDLINE in `PKGBUILD`. On DCN401, IPS/DPG pipe-gating sets
`hubp->power_gated`, making `hubp2_is_flip_pending()` return `false` while a
flip is still pending → the VUPDATE_NO_LOCK flip-event handler delivers the
completion before HW latches → the compositor re-paints a buffer still being
scanned → a fixed content-tracking square over app windows (the sleepy-next
"box", absent from compositor screenshots). Matches AMD drm/amd work item
#5570 class. A/B verified 2026-08-26: `0x20000` (FAMS) and `0x8` (clock
gating) did not help; `0x800` (IPS off) fixed it. Re-evaluate when a proper
DCN401 flip-pending fix lands upstream.

## Added (2026-08-27) — zstd BMI2 probe series (Usama Arif, Meta)

`2128`–`2130`, "zstd: probe the CPU for BMI2 support once, not per context"
(lkml `20260826122558.2662013-1-usama.arif@linux.dev`, via the lkml
public-inbox git mirror — lore.kernel.org web is Anubis-blocked, the
`repos/lore-mirror` epoch-20 clone is the working access path). Three patches
on `lib/zstd`:
- `2128` — `ZSTD_initStaticCCtx()` routes its BMI2 probe through
  `ZSTD_cpuSupportsBmi2()` (requires BMI1+BMI2, matching the dynamic-dispatch
  bodies; latent inconsistency, no field-visible change).
- `2129` — `ZSTD_cpuSupportsBmi2()` returns 0 when `DYNAMIC_BMI2` is unset
  (nothing reads the flag in static dispatch).
- `2130` — probe the CPU once and cache the result with READ_ONCE/WRITE_ONCE
  instead of re-probing per context.

Relevant: this kernel ships `CONFIG_ZSTD_COMMON/COMPRESS/DECOMPRESS=y` (zram/
zswap use zstd). Original `From:`/`Date:`/`Subject:`/`Signed-off-by:` headers
kept intact (mailing-list noise headers trimmed). Applies cleanly to
next-20260827 with `patch -p1 --forward -F2` (cumulative order 2128→2129→2130).

## Added (2026-08-27 sweep — 20 patches)

Fresh 08-26/27 ML submissions found in the lkml public-inbox mirror
(`repos/lore-mirror`) and the amd-gfx/dri-devel August archives. All apply
cleanly to next-20260827 with `patch -p1 --forward -F2` (verified in series
order) and keep original headers/Signed-off-by.

- **`1210`–`1224` — ACPI: CPPC v5 (15 patches)**, Christian Loehle (arm.com),
  lkml `2026082711…`. Reworks the CPPC control path amd-pstate runs on Zen 4:
  validate `_CPC` packages, propagate control-write errors, serialize PCC
  payload updates (single-reg + EPP), 64-bit register masks, reject unsafe
  cross-CPU SystemMemory RMW, lifetime-leak fixes. High value for our
  `amd_pstate.epp_boost=1` setup.
- **`1141`–`1143` — drm/amd/display** (NepNep7601, amd-gfx ML 08-27): skip
  receiver power control without AUX; close DDC on I2C engine setup failure;
  fall back to software I2C on hardware engine failure. Display-link power
  sequencing + DDC/I2C robustness on the shared path.
- **`1059` — drm/amdgpu: restrict BAR0 fallback read to SR-IOV VFs only**
  (Mario Limonciello, amd-gfx 08-26, `Cc: stable`). Early-init boot-path
  regression fix (`Fixes: ea8ac194077d`).
- **`2005` — sched_ext: skip per-CPU data allocation for built-in DSQs**
  (Qiurong Fang, lkml 08-27). Relevant to `CONFIG_SCHED_CLASS_EXT=y`.

Deferred (tracked, not merged): the 30-patch Alex Deucher **TLB-invalidation
v2** upgrade of `1004`–`1017` (under review; swap in a dedicated session);
gfx12 mes_dbgext; job-based IB refactor; blend-mode v4 (drm-helper piece).

## Added (2026-08-28 — second sweep window, 8 patches)

Fresh 08-27/28 finds from the amd-staging-drm-next branch (agd5f) and the
amd-gfx ML. All verified `patch -p1 --forward -F2` against next-20260828.

- **`9049` — drm/amdgpu: recompute dw estimate after allocating a new VM
  update job** (YuBiao Wang, `Cc: stable`). Stale free-dw count after job
  realloc can encode a 1 GB copy inside the IB pool → GART fault + ring hang.
  Coexists with our `9034` (same file, no hunk overlap).
- **`9050` — drm/amdgpu: Update no-retry PTE flags for GFX12** (RDNA4 gfx12.0).
- **`9051`/`9052` — DCN4 flip-schedule pair** (Unify + Fix CalculateFlipSchedule):
  flip-path bandwidth calc; relevant to the VUPDATE_NO_LOCK "box" class.
- **`9053` — DCN42 IPS1 rIOMMU hang fix** (DCHVM↔rIOMMU SDP port disconnect).
- **`9054` — Guard amdgpu_dm_irq_schedule_work against NULL irq_wq** (teardown race).
- **`1144` — drm/amd/display: Enable HDMI FRL by default** (Jerry Zuo, v2,
  `20260827155409.1426730-1`, Reviewed-by Harry Wentland). Adds `DC_FRL_MASK`
  to the default `amdgpu_dc_feature_mask` so HDMI 2.1 FRL is on.
- **`1060` — drm/amdgpu: cancel hang_detect_work before taking userq_mutex**
  (Vitaly Prosyak, `20260827222531.127950-1`, Reviewed-by Christian Koenig).
  Deadlock fix on the gfx12 userq path.

Note: next-20260828 upstreams ~18 more amd-staging commits (the ones we had
backported as `1054`, `9043`, `9045`, `9047`, `9048` are now redundant; `1026`
needs a rebase to drop the duplicate guard while keeping the CRIU callbacks).
The remaining pending amd-staging content is off-target (GC12.1/datacenter,
SMU15, DCN5/6) or refactor — nothing else worth carrying this window.

## Cleanup (2026-08-28, pkgrel 10)

Dropped **76 patches** whose content next-20260828 now upstreams (verified by
`patch -p1 --forward -F2 -R` reverse-apply against the base): `1000`-`1002`,
`1019`, `1024`, `1047`, `1050`, `1051`, `1101`-`1104`, `1106`-`1111`,
`1113`-`1115`, `1117`-`1126`, `1129`-`1133`, `1137`-`1139`, `1200`, `1205`,
`1207`, `1208`, `2102`-`2105`, `2108`-`2119`, `9001`-`9003`, `9006`, `9009`,
`9010`, `9030`, `9031`, `9032`, `9036`, `9042`, `9043`, `9048`, plus the
superseded `1054`, `9045`, `9047` (base has refined revisions) and `9053`
(DCN42 rIOMMU — already in base). `1026` (GFX12 CRIU callbacks) applies
cleanly and is kept. Fixed the six `9049`-`9054` amd-staging patches that were
accidentally empty (re-extracted via `git format-patch` from agd5f; `9053`
dropped as redundant). `source=()` now matches on-disk exactly (143 patches).

## Sweep 2026-09-02 — base bump to next-20260901, no new fixes worth carrying

Full source re-check (linux-next next-20260901 fetched; amd-gfx + dri-devel
2026-September archives; lkml mirror; drm/amd work-items tracker; CachyOS /
sirlucjan / firelzrd; x86/security line). Findings, all **deferred/not carried**
with reasons:

- **LRU-MARIE 0.11.0** (firelzrd, 2026-08-31) — fetched. Does NOT port to the
  7.3-merge-window base (both 0.10.5 and 0.11.0 fail `patch` against
  next-20260828/0901: the mm memcg soft-limit removal shifted
  memcontrol.h/vmscan.c). Our carried 2101 (0.10.5) is itself skipped by the
  build for the same reason. Needs a dedicated 7.3 port before it can land.
- **"passive VRR" series** (Jerry Zuo / Fangzhi Zuo + Tomasz Pakuła, v1
  2026-09-01, `20260901191251.2653684-1`, dri-devel) — a NEW feature (keeps
  sinks in their variable-refresh state during desktop/fixed-refresh use to
  avoid HDMI blanking flicker), not a fix; touches DRM core + the 7.3 split
  amdgpu_dm files; not in next-20260901. V1 unreviewed; our VRR already works
  (HF-VSDB freesync_capable via 0059-0061/0063). pvr-01/pvr-03 apply clean,
  pvr-02 needs a manual rebase. Deferred — re-evaluate on a v2/review.
- **drm/amd/display cursor-disable w/ horizontal split planes** (yulingli,
  08-31) — cursor fix; targets horizontal-split (ultrawide/ODM) configs, not
  our 1920x1080 layout; not carried.
- **Work items**: #5709 (HDMI FRL link-training fail on DPMS wake), #5717
  (NAVI48/RX 9070 XT evicted-surface corruption) — open, no landed fix
  referenced; track. #5616/#5705 flip_done class still open (no new fix).
- CachyOS fixes v5 = cosmetic (HID touchpad); cachyos-linux/build forks stale.
- x86/security: nothing new for Zen 4 since 08-01.

Net: no new AMD fixes worth carrying this window; bumped base to
`next-20260901` for the current mm/mglru + 7.3-rc1 content.

## Dropped (2026-09-02) — 20 non-applying patches removed from sleepy-next

These 20 patches target the vanilla-7.2 / 7.2-era base and do NOT apply to the
7.3-merge linux-next base (the build was skipping them — verified: each fails
`patch -p1 --forward` and does NOT reverse-apply). Removed from source=() and
disk so the series only carries patches that actually apply:
`0008` (SMU14 power-limit), CachyOS `0104`-`0113` 7.2-only squashes that don't
port (cgroup-vram, fixes, drops, preempt-ipi, vesa-dsc, micro-opts), `1003`
(gfx12 KCQ remap), `1023` (min_power_limit), `1057` (ttm BO ref), `1100`/
`1105`/`1116`/`1127`/`1128` (DCN4/42b backports the base's newer DCN4 code
supersedes), `1206`/`1209` (amd-pstate EPP — base CPPC v4+ path differs),
`2106`/`2107` (zram OOB — base zram rewritten), `9041` (userq doorbell xa-lock
— base userq evolved). `2101` (MARIE 0.10.5) retained pending the 0.11.0 port.
Series now 123 patches.

## Ported (2026-09-02) — LRU-MARIE 0.11.0 onto next-20260901 (replaces 2101 0.10.5)

`2101` is now the **ultracode-ported LRU-MARIE 0.11.0** for the linux-next
7.3-merge base (firelzrd's vanilla-7.2 patch does NOT apply to next-20260901;
a multi-agent recon/port/verify pass base-fit it). The 7.3 base diverged:
`mm/swap.c` content moved to `mm/folio.c`, `struct alloc_context` moved to
`mm/page_alloc.h`, `page_io.c` was rewritten around `struct swap_io_ctx`
(the old `swap_iocb**` per-folio path is gone), vma_flags became
`vma_flags_t`, and the memcg soft-limit rbtree was removed. Port notes:
- swapout batching delivered via the base's native ctx/bio coalescing (not
  MARIE's removed `do_swapout_batch`); kcompressd kthread + store/drain +
  nr_swap_write_failed early-OOM gate all present.
- `FOLIOREF_RECLAIM_CLEAN` enum restored (base removed it); `vm_flags & VM_EXEC`
  fixed to the base's `is_exec_file_folio`/vma_flags_t API.
- 3 compile fixes applied: `#include "../swap.h"` (state_reclaim.c, for
  mem_cgroup_swappiness), `#include "../page_alloc.h"` (defrag.c, for
  buddy_order/post_alloc_hook), and 4-arg `post_alloc_hook(..., ALLOC_DEFAULT)`
  in defrag_compat.h. Verified: applies clean (`patch -p1 --forward`, 0 rejects)
  and the mm/ subtree builds (gcc) with these fixes.
- Runtime invariants (kcompressd folio_get/drain balance, queued-folio locking
  across the keep path) match base semantics but need real boot testing.
