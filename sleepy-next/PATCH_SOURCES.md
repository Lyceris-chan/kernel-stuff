# sleepy-next patch provenance

`sleepy-next` builds `linux-sleepy-next`, the **linux-next snapshot preview**
package. It carries a copy of the same patch series as `sleepy-rc` in its own
`patches/` tree, but applies it to a linux-next daily snapshot instead of a
mainline `-rc` tag.

Per-patch provenance — source, upstream sha, mailing-list link, review status,
drop reasons — lives in **`sleepy-rc/PATCH_SOURCES.md`**, which stays the
authoritative ledger for the series. This file records only what differs in the
preview package. A patch's provenance does not change because the preview base
moved, so the full ledger is not duplicated here.

## Base

| | |
|---|---|
| Snapshot | `next-20261029`, tag `a39c95080621` (tag object `22f566ae1781`) |
| Source | `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git/snapshot/next-20261029.tar.gz` |
| Snapshot tree `Makefile` | `7.3.0` — the base release, **deliberately not used in the release name** |
| Kernel release | `2026.10.29-1-sleepy-next` |
| Package | `linux-sleepy-next-2026.10.29-1` |

### Versioning: the snapshot date, not the base rc

`pkgver` is the snapshot date, derived from `_srctag` — `_snapdate=${_srctag#next-}`
(`20261019`) and `_snapver` respells it dotted (`2026.10.19`) — so a bump cannot
move the tag without moving the version.

**The dots are load-bearing, not cosmetic.** Both tools that consume the release
string require it to *begin* with dotted decimal notation:

| Tool | Requirement | Failure without it |
|---|---|---|
| `depmod` (kmod 34.2) | an `N.N` prefix; a bare `20261019-1-sleepy-next` is rejected as `Bad version passed` | post-install depmod hook fails, no module dependencies generated |
| `mkinitcpio` (42.2) | `kver()` validates the release extracted from the image against `^[[:digit:]]+(\.[[:digit:]]+)+` | initramfs build fails — **the kernel is left with no initramfs at all** |

A bare `20261019` therefore cannot be the release name. Dots are legal in
`pkgver`; only `-` is reserved, as the pkgver/pkgrel separator.

`prepare()` rewrites the snapshot's `Makefile` so `KERNELVERSION = 2026.10.19`.
Left alone, the tree composes `KERNELVERSION` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL`/`EXTRAVERSION` and stamps its **base** release
into the name: `next-20261019` is cut from `v7.3`, so the kernel would announce
itself as `7.3.0-1-sleepy-next` — the same upstream release as
`linux-sleepy-rc`'s genuine `7.3.0-1-sleepy-rc`, colliding with it in tools that
compare only the upstream version.

Only the release *string* moves. `version.h` derives `LINUX_VERSION_CODE` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL` (`Makefile`: `filechk_version.h`), **not** from
`KERNELVERSION`, so those stay `7`/`3`/`0` and out-of-tree version checks keep
working. `include/generated/utsrelease.h` and every `modules_install` path read
`KERNELRELEASE`, which is regenerated from `KERNELVERSION`, so `uname -r`, the
module directory and the packaged paths all agree.

`prepare()` asserts the rewrite landed and aborts the build if it did not, rather
than shipping a kernel that misreports its own release.

The tree's own `localversion-next` (containing `-next-20261019`) is still
deleted: the date is already `KERNELVERSION`, so keeping it would print it
twice.

## Preview-specific deltas

### 1. Patches that do not apply are SKIPPED, not failed

`prepare()` dry-runs every patch and skips it outright when it does not apply, so
a snapshot that has moved past the series still produces a build. The series is
reconciled on every snapshot bump: on `next-20261019`, **139 patches apply in
order** and the absorbed or superseded carries are no longer listed (see *Base
bump to `next-20261019`* at the end of this file). The skip mechanism remains as
a safety net for a snapshot that moves again before the next reconciliation.

Skipping is only safe for a **self-contained** patch. A patch that *declares* a
symbol another patch *uses* must not be skipped while its consumer applies —
that yields a compile error rather than a clean miss. Where the series had such
an interdependent group, the whole group is excluded instead (see 2).

### 2. Excluded from `source=()`: the amdgpu TLB-invalidation rework

`1008`, `1012`, `1013`, `1014` and `1017` are **not listed** in the preview
`source=()`. All five are retained in full in `sleepy-rc`.

| Patch | Role | Applies to `next-20261019`? |
|---|---|---|
| `1008` | adds `amdgpu_buffer_funcs::tlb_inv_num_dw` and `amdgpu_emit_tlb_inv()` | no (1 of 2 hunks fails) |
| `1012` | sdma7 TLB-invalidation consumer | yes |
| `1013` | core TLB-invalidation helper | yes |
| `1014` | further gmc tlb-inv helpers | no (fails both directions) |
| `1017` | gmc12 TLB-invalidation consumer | yes |

`1008` still does not apply, while `1012`/`1013`/`1017` do — and those consume
exactly the struct member and helper that `1008` introduces. Carrying the group
partially does not compile:

```
drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c:2634:42: error: no member named
    'tlb_inv_num_dw' in 'struct amdgpu_buffer_funcs'
drivers/gpu/drm/amd/amdgpu/amdgpu_ttm.c:2641:2: error: call to undeclared
    function 'amdgpu_emit_tlb_inv'
```

Excluding the whole group is the coherent choice — a partially applied rework is
worse than none of it. Checked before excluding: no other carried patch
references `tlb_inv_num_dw`, `amdgpu_emit_tlb_inv` or `gmc_v12_0_tlb_inv*`.

### 3. Excluded from `source=()`: the amdkfd fault-window carry (`9060`)

`9060` ("drm/amdkfd: skip migration when the fault window is already in VRAM") is
**not listed** in the preview `source=()`; `sleepy-rc` retains it.

The snapshot already contains the change, so the patch applied anyway — its
context anchors survived — and inserted a *second* copy of
`svm_range_window_resident()` into `kfd_migrate.c`:

```
drivers/gpu/drm/amd/amdgpu/../amdkfd/kfd_migrate.c:437:1: error:
    redefinition of 'svm_range_window_resident'
```

**This is the "applies, therefore fine" trap.** A clean apply is not evidence
that a patch is still needed: when upstream absorbs a carry, the hunk's context
survives and the patch becomes a duplicate rather than failing. Confirmed by
content, not by subject — the pristine snapshot's `kfd_migrate.c` already
defines the function, and the patched tree ends up with two bodies.

A whole-series check for duplicated function *bodies* — matching a definition
line to a following `{`, so prototypes and macros are not miscounted — flags
`9060` and nothing else among the 100 applied patches.

### 4. `2419` (BORE) rebased for the snapshot's `update_protect_slice()`

One hunk was **added** to the carried BORE patch. This is a rebase of our own
series, not a new patch; it reuses BORE's existing idiom verbatim.

The snapshot gained `update_protect_slice()` (base `kernel/sched/fair.c:1142`),
which reads `normalized_sysctl_sched_base_slice`. BORE wraps the sibling
`set_protect_slice()` in `#ifdef CONFIG_SCHED_BORE` / `#else` and supplies its
own `sysctl_sched_base_slice`; under `CONFIG_SCHED_BORE=y` the `#else` arm is
dead, so `normalized_sysctl_sched_base_slice` is never declared:

```
kernel/sched/fair.c:1174:14: error: use of undeclared identifier
    'normalized_sysctl_sched_base_slice'; did you mean 'sysctl_sched_base_slice'?
```

The added hunk gives `update_protect_slice()` the same wrapper
`set_protect_slice()` already has, so both resolve to BORE's slice under BORE,
and to upstream's normalized slice otherwise. Applying the rebased patch to a
pristine snapshot `fair.c` leaves no `.rej`, and neither remaining
`normalized_sysctl_sched_base_slice` use sits outside an `#else` arm.

### 5. `0101` (BBR3) and `2101` (LRU-MARIE) rebased onto the snapshot

> **Historical — this is the `next-20261009` rebase.** The base has since
> moved to `next-20261016`, where both were rebased again; see *Base bump to
> `next-20261016`* at the end of this file. The method notes here still hold.

Both carries failed to apply to this base and were skipped. Both are now rebased
and apply with **zero failed hunks**. Method for each: reproduce the tree at the
patch's exact position in `source=()` (`0101` is entry 17, `2101` entry 122),
apply, fix the tree so it is *correct*, then regenerate the patch from
`git diff HEAD`. Working at the end state instead reports failures that are not
real — later patches touch the same files, and `2033` also edits
`tcp_output.c`.

**`0101-cachy-bbr3` — 6 failing hunks, all the same change.** Upstream has
already converted the `min_tso_segs` congestion-control callback to
`tso_segs`: `include/net/tcp.h` declares `u32 (*tso_segs)(struct sock *sk, u32
mss_now)` (identical type — `u32` is `unsigned int`), `tcp_output.c`'s
`tcp_tso_segs()` already calls `ca_ops->tso_segs`, and both `tcp_bbr.c` and
`bpf_tcp_ca.c` already register it. So those five hunks are dropped.

The sixth **had to be dropped for a different reason**: it applied, and added a
*second* `bbr_tso_segs()` next to upstream's — two file-scope definitions, the
same redefinition trap as `9060`. It is redundant because `tcp_bbr3.c` is
self-contained: it has its own `bbr_tso_segs()` and its own
`tcp_congestion_ops` named `"bbr3"`.

`tcp_bbr.c` and `bpf_tcp_ca.c` therefore drop out of the patch entirely. But
**one hunk could not simply be deleted**: the `tcp.h` hunk also adds
`skb_marked_lost`, which upstream does *not* have and which `tcp_input.c:1342`
and `tcp_bbr3.c` (definition, registration, `BTF_ID_FLAGS`) all require. It was
rewritten to add only that field.

`bbr_tso_segs` now exists in both `tcp_bbr.c` and `tcp_bbr3.c`, both
`__bpf_kfunc static` — that is the documented BBR/BBR3 kfunc-symbol situation,
and it stays safe only while `CONFIG_TCP_CONG_BBR` is unset, which it is.

**`2101` LRU-MARIE — 5 failing hunks.** Four are context drift:

- `mm/Kconfig` — upstream added `def_bool y` to `LRU_GEN_WALKS_MMU`, so the
  anchor moved. Block re-inserted before `config LOCK_MM_AND_FIND_VMA`.
- `mm/swap.h` — `__swap_writepage()`, the original anchor, no longer exists;
  the `kcompressd()` declaration (definition is `mm/page_io.c:455`) now follows
  `swap_write_submit()`.
- `include/linux/memcontrol.h` — upstream rewrote
  `mem_cgroup_get_zone_lru_size()`: `const` lruvec, `long val`, a
  `WARN_ON_ONCE(val < 0)` guard. MARIE's hook was re-expressed against the new
  body, which required `const`-qualifying `lru_marie_zone_size_read()` and its
  static helper `marie_lruvec_zone_size()` — both read-only.
- `mm/page_alloc.c` — two real merges, not just drift. Upstream added an
  `unsigned int reclaim_order` parameter *and* a `reclaim_order == order`
  term to the progress condition, so MARIE's `bool did_some_progress` ->
  `unsigned long nr_progress` change had to be carried alongside both, and the
  call site updated. MARIE's refault-treadmill accounting and its
  `#ifdef CONFIG_LRU_MARIE` swap-backend-failure OOM trigger are both retained.
  **The refault half is not cosmetic**: an applied hunk already writes
  `ac->last_refaults`, so dropping it would leave the counter written and never
  read — silently disarming the thrash detector, which `LESSONS.md` records
  being wrongly muted once already.
- `mm/vmscan.c` `move_folios_to_lru()` — upstream gained a `do_rotate`
  tail-add: `if (...) lruvec_add_folio_tail(); else lruvec_add_folio();`. That
  axis is orthogonal to MARIE's tracked-vs-orphan axis, and
  `lru_marie_orphan_add()` already takes a `bool tail` (MARIE's own `folio.c`
  passes both `true` and `false`), so the two merge cleanly: an untracked
  orphan takes the tail path through the helper's `@tail`, a tracked folio is
  warned about and handed back to Marie, and the non-Marie path keeps upstream's
  tail behaviour.

### 6. Added — `2700`/`2701`, the zswap request-contention series

`[PATCH v2 0/2] mm: zswap: reduce request contention on loads` (Usama Arif).
Carried in the **preview only**; it does not apply to `v7.3-rc6`, which is why
`sleepy-rc` does not have it.

| | |
|---|---|
| `2700` | *mm: zswap: use separate compression and decompression requests* |
| `2701` | *mm: zswap: use stack requests for synchronous decompression* |

**v2, not v1.** The ledger originally recorded only the v1 posting (2026-10-05,
`<20261006002307.2669023-1-usama.arif@linux.dev>`). Usama Arif posted **v2 on
2026-10-09** (`c98f639a22`, `e9b4a3996d`), with further review from Nhat Pham and
Sergey Senozhatsky on 2026-10-10. Always check for a later revision before
carrying a series.

Provenance: `Signed-off-by: Usama Arif <usama.arif@linux.dev>`; `Acked-by: Nhat
Pham <nphamcs@gmail.com>` on `2701`. Nhat Pham maintains zswap.

The problem, from `2700`'s message: stores and loads serialize on the same
per-CPU acomp request and mutex, so a low-priority store preempted after the
codec drops its stream lock keeps holding the mutex, and a higher-priority load
on that CPU waits. The fix gives compression and decompression their own
request, completion wait and mutex; synchronous codecs then decompress on an
on-stack request. **All in-tree software compressors qualify, and zstd is what
this machine runs.**

**Verified at its real series position, not against a pristine tree.** Eight
carried patches also touch `mm/zswap.c` (`2173`, `2174`, `2177`, `2190`-`2193`,
`2196`), so a pristine-tree test would prove nothing. The tree was rebuilt with
`source=()` indices 0-170 applied, and both patches then pass `git apply
--check` **and** `patch -p1 --forward -F2 --dry-run` with zero failed hunks.
The result carries `struct zswap_comp_ctx` and `MAX_SYNC_COMP_REQSIZE`.

**New range `2700-2799`** (mm/swap: zswap, xswap). `21xx` is full apart from
`2199`, and every other gap in it is a *vacated* number — the dropped MGLRU
batch (`2131`-`2137`), absorbed carries — which must not be reused, since the
gap is the evidence that something was tried. The series opens a new range
rather than splitting across one.

**Also noted in the same thread, not triaged**: `[PATCH v8 14/30] mm: zswap:
reject high-order swap cache allocations backed by zswap` (Usama Arif), and
Baoquan He's xswap v4 series.

### 7. Cmdline

`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is **dropped in the preview only**;
`sleepy-rc` keeps it. The preview exists to exercise the snapshot's display code
with IPS left enabled rather than masked off by the 7.3-era workaround.

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0
```

### 8. sched_ext disabled on `next-20261019`

`CONFIG_SCHED_CLASS_EXT` and `CONFIG_EXT_SUB_SCHED` are disabled in the preview
for this snapshot. The snapshot's sched_ext tree has two merge gaps:

- `free_dsq_irq_workfn()` in `kernel/sched/ext/ext.c` uses `dsq->pcpu`, but the
  field is `pcpu_user` in `include/linux/sched/ext.h`.
- `scx_reenq_wait_dispatching()` is called in `ext.c` but defined nowhere in the
  tree.

BORE is the live scheduler on this machine and sched_ext is unused, so the
preview builds without it; `sleepy-rc` keeps `CONFIG_SCHED_CLASS_EXT=y`.
Re-enable when a later snapshot's sched_ext tree is consistent.

## Base bump to `next-20261016` — 2026-10-17

The move staged on 2026-10-15 and reverted on 2026-10-16 is now done, with the
BORE hunk deletion, the LRU-MARIE rebase and the CachyOS `0101` refresh landed
as one atomic step, as the earlier entry prescribed.

**Measured cost, full series, `patch -p1 --forward --dry-run` at the series
position (the same loop `prepare()` runs): 109 applied, 147 skipped, 0 failed**
— for 256 `source=()` entries. (The 253/145 figures recorded when the bump
landed were re-measured after the cleanup at the end of this file; the applied
count is unchanged because dropping `9040` and adding `1176` cancel out.) The earlier sizing tables (`next-20261009`: 102
applied of 241 carries) were taken before the 13 patches adopted on 2026-10-17,
so the counts are not directly comparable; what matters is `failed=0`, because
`prepare()` skips rather than fails and a silent skip is the failure mode this
ledger exists to catch.

### 1. `0101` (bbr3) regenerated for this base

One hunk or the whole squash fails on `include/linux/tcp.h`: the base gained an
`#ifdef CONFIG_BPF` block (`bpf_tcp_ops_flags`) between `recvmsg_inq : 1` and
`__cacheline_group_end(tcp_sock_read_txrx)`, so the anchor for the
`fast_ack_mode:1` bitfield moved. The bitfield was re-spliced into the new
layout and the squash regenerated from the tree at its series position (the 17
preceding `00xx` entries), per the `patch-cachy-branches` skill.

**Regenerated from this package's own text, not from sirlucjan.** The source
(`bbr3-cachyos-patches-sep`, `9c29aa44556d`, unchanged since 2026-10-15) was
applied fresh at the same position to check, and it reintroduces the
`net/ipv4/tcp_bbr.c` hunks the previous rebase deliberately dropped — the
`min_tso_segs` → `tso_segs` conversion this base already has. Re-squashing from
source would have to re-derive that adaptation; regenerating from the adapted
text does not.

**Dry-run against a *pristine* tree is not a verdict here.** The failing
`include/net/tcp.h` hunk (`Hunk #9 FAILED at 1390`) appears only against a
pristine `next-20261016`; at the real series position the 17 preceding patches
have already changed that region and it applies. This is the skill's "generate
the squash against the actual series state" rule, observed live.

### 2. `2419` (BORE) — hunk #7 deleted

The hunk added on 2026-10-12 (`@@ -1142,5 +1171,9 @@`, wrapping
`normalized_sysctl_sched_base_slice` in `#ifdef CONFIG_SCHED_BORE` inside
`update_protect_slice()`) is **obsolete on this base**: the scheduler rework
landed in the 15→16 window and `update_protect_slice()` no longer reads that
symbol. Verified both directions at `2419`'s position on `next-20261016`:

| Patch | Result |
|---|---|
| preview `2419` (hunk #7 deleted) | **0 rejects**, 0 fuzz |
| `sleepy-rc` `2419` (hunk #7 kept) | **2 rejects** — the hunk has no anchor |

The deletion is still base-specific and must not be copied to `sleepy-rc`:
`v7.3-rc7` keeps the old `update_protect_slice()`, where the wrapper is still
required. **This is a live preview-only delta** — if a later `sleepy-rc` bump
takes the scheduler rework, the same deletion must be applied there.

### 3. `2101` (LRU-MARIE 0.12.0) rebased onto the snapshot — six sites

> **Historical — superseded by §4 (LRU-MARIE 1.0.0-rc1) below.**

The `sleepy-rc` copy (the author's own `0.12.0` for `7.3-rc7`) applies to its
base with zero rejects; this base needs six host hooks re-anchored, exactly the
set diagnosed on 2026-10-16. Applied at its position in a graft tree, fixed,
regenerated with `git diff` against a committed baseline.

| # | Site | What was done |
|---|---|---|
| 1 | `include/linux/memcontrol.h` | **Correction to the earlier diagnosis:** the body is *not* in `mm/folio.c` — the accessor is a `static inline` in the header itself, rewritten upstream to `long val` + `container_of_const()` + a `WARN_ON_ONCE(val < 0)` guard. MARIE's hook was re-expressed against that body |
| 2 | `mm/Kconfig` | `LRU_MARIE` / `LRU_MARIE_DEFAULT_ON` / `LRU_MARIE_DEFRAG` block re-anchored after `config LRU_GEN_WALKS_MMU`'s closing `# }`, before `config LOCK_MM_AND_FIND_VMA` |
| 3 | `mm/page_alloc.c` | `should_reclaim_retry()` — MARIE's `unsigned long nr_progress` + refault-treadmill body merged **with upstream's new `!order_defrag_promoted(order, ac)` term**, which must survive; anchor now at `:4646` |
| 4 | `mm/page_alloc.h` | `unsigned long last_refaults;` added to `struct alloc_context` after the `reclaim_compact_order` field upstream added |
| 5 | `mm/swap.h` | `int kcompressd(void *p);` declared after `__swap_writeout()`; the reject's `__swap_writepage` anchor no longer exists in the tree |
| 6 | `mm/vmscan.c` | `move_folios_to_lru()`'s tail now has the `do_rotate` pair, so **both** branches are wrapped — `lruvec_add_folio_tail()` with `lru_marie_orphan_add(..., true)` and `lruvec_add_folio()` with `..., false` |

**Three more sites only surfaced at compile time, not as rejects.** The
seven-window churn removes symbols the author's `7.3-rc7` text names, and a hunk
that references a removed symbol still *applies* — its context is unchanged.
The build stopped in `mm/page_io.o`; the third would have hit one object later:

| Symbol | Site | Fix |
|---|---|---|
| `__swap_writepage()` | `mm/page_io.c`, in the `do_swapout()` Marie adds | renamed to `__swap_writeout()` |
| `PF_KSWAPD` | `mm/page_io.c`, `kcompressd()`'s flag setup | dropped; upstream's own `kswapd()` now sets only `PF_MEMALLOC` |
| `VM_SPECIAL` | `mm/lru_marie/walker.c` | the composite macro is gone; spelled out as `VM_IO \| VM_DONTEXPAND \| VM_PFNMAP \| VM_MIXEDMAP`, which is exactly what it expanded to (`VMA_SPECIAL_FLAGS` on `v7.3-rc7`) |

The first two are the ones this ledger already recorded as rebase traps; the
previous rebase made the identical changes, so the wording of the `PF_KSWAPD`
comment is reused verbatim. Confirmed by compiling `mm/page_io.o` and the whole
`mm/lru_marie/` directory (including the four SIMD `.S` files) before the full
rebuild, rather than by another seven-minute build cycle.

**And then scan the whole patch for symbols the base no longer has.** Every
function-like identifier the patch's *added* lines call (1014 of them) was
resolved against the applied tree with `rg -w` — none is undefined — which is
the check that would have caught all three of the above before the build did.
Note this must run against the **filesystem**, not `git grep`: the patch creates
`mm/lru_marie/*` as untracked files in a graft tree, and `git grep` cannot see
them.

**Running the previous rebase's diff against the new one is the cheapest way to
find these.** Both the `__swap_writeout` rename and the `PF_KSWAPD` removal were
already solved once in this package's own history; diffing the old and new
`2101` showed them immediately.

**The `memcontrol.h` hook needed a const-qualification, as it did on the last
bump.** The host accessor takes `const struct lruvec *`, MARIE's
`lru_marie_zone_size_read()` takes `struct lruvec *`, so the declaration in
`include/linux/memcontrol.h` and both the helper `marie_lruvec_zone_size()` and
`lru_marie_zone_size_read()` in `mm/lru_marie/core.c` are const-qualified. This
is the standing exception to "`mm/lru_marie/*` stays byte-identical to the
author's" — it is a type adaptation to the host, not a change to Marie's
algorithm, and it has now been applied on two consecutive bumps. `lruvec_pgdat()`
already takes a const pointer, so nothing else in the helper needed changing.

**Git-diff hygiene:** `git diff HEAD` in a graft tree picks up the `.orig` files
GNU patch leaves on an offset. One regeneration came out 156 KB instead of
14 KB with 44 `*.orig` deletions in it. Purge `.orig`/`.rej` **before**
`git add -A`, and if it is already too late, `git diff HEAD -- . ':(exclude)*.orig'`.

### 4. `2101` upgraded to LRU-MARIE 1.0.0-rc1 — nine host sites and three compile fixes

The 0.12.0 carry in §3 is superseded. The author's 1.0.0-rc1 patch (against
7.3-rc7) was applied at the same position — entry 134, 133 preceding — and
rebased against `next-20261016`. `mm/lru_marie/*` stays byte-identical except
the standing const fix; everything else is a host hook.

| # | Site | What was done |
|---|---|---|
| 1 | `include/linux/memcontrol.h` | declaration const-qualified; `lru_marie_zone_size_read()` call re-expressed against the preview's `long val` + `WARN_ON_ONCE()` body |
| 2 | `mm/lru_marie/engine/hooks.c` | `marie_lruvec_zone_size()` and `lru_marie_zone_size_read()` const-qualified (the same one-line fix as 0.12.0; the helper moved from `core.c` to `engine/hooks.c`) |
| 3 | `include/linux/zswap.h` | `zswap_folio_reused()` declaration and `!CONFIG_ZSWAP` stub added around the preview's range-based `zswap_invalidate()` signature |
| 4 | `mm/Kconfig` | `LRU_MARIE` block re-anchored before `config LOCK_MM_AND_FIND_VMA` |
| 5 | `mm/page_alloc.h` | `last_refaults` added to `struct alloc_context` after `reclaim_compact_order` |
| 6 | `mm/swap.h` | `kcompressd()` declared after `__swap_writeout()` (`__swap_writepage` does not exist here) |
| 7 | `mm/page_alloc.c` | `should_reclaim_retry()` takes `unsigned long nr_progress` and keeps the preview's `!order_defrag_promoted(order, ac)` term |
| 8 | `mm/vmscan.c` | both `move_folios_to_lru()` putback arms carry the MARIE orphan/tail split (the §3 block reused verbatim) |
| 9 | `mm/zswap.c` | incompressible-slot logic adapted to the preview's folio-based `zswap_store_page()` and range `zswap_invalidate()`; `zswap_folio_reused()` added after `zswap_store()` |

**Three compile-only fixes, exactly the §3 set.** They apply — the context
matches — but name symbols this base removed; a targeted grep and the
added-line identifier scan found them before a build:

| Symbol | Site | Fix |
|---|---|---|
| `__swap_writepage()` | `mm/page_io.c`, `do_swapout()` | renamed to `__swap_writeout()` |
| `PF_KSWAPD` | `mm/page_io.c`, `kcompressd()` | dropped; the comment reuses §3's wording |
| `VM_SPECIAL` | `mm/lru_marie/engine/walker.c` | spelled out as `VM_IO \| VM_DONTEXPAND \| VM_PFNMAP \| VM_MIXEDMAP` |

**Verified on a fresh `next-20261016` graft:** the 133 preceding entries
applied with prepare semantics (59 applied, 74 skipped as already present),
then `2101` applied with **0 failed hunks and 0 `.rej`**; the three compile
symbols are present in the fixed tree. Hooks checked:
`lru_marie_zone_size_read` in `memcontrol.h`, `kcompressd` in `swap.h` and
`page_io.c`, `nr_swap_write_failed` in `page_io.c`, `include/linux/lru_marie.h`
created. Every function-like identifier on the patch's added lines resolves in
the applied tree.

**Three of the other new carries also skip on this snapshot, for reasons that
are not absorption:**

| Patch | Why it skips here |
|---|---|
| `2046` (nvme clamp revert) | `drivers/nvme/host/pci.c` already calls `dma_max_mapping_size()` — the revert's result is present; only its hunk context drifted, so neither forward nor reverse is clean |
| `2049` | The snapshot's `struct nvme_uring_cmd_pdu` is `{ req, bio }` only; status/result moved to `io_uring_cmd_set_res32()` in `end_io`. The patch's `pdu->status` propagation needs a semantic port, not a rebase |
| `2050` | Same API change: the local-IOPOLL path completes via `__io_uring_cmd_done()` and the pdu carries no status/result. Deferred |

`2047`/`2048` apply here, so the request-freeing half of the copyback series
is live in the preview; the error-propagation half is not.

The zswap range patches `2191`–`2193` are copied from `sleepy-rc`, where they
were rebased around 1.0.0-rc1's zswap changes; here all three are absorbed by
the snapshot and skip.

### 5. Dead carries still in `source=()`

Three patches in this package are now **fully absorbed upstream** and skip on
every build — reverse-applicability confirms the content is in the pristine
`next-20261016` tree:

| Patch | Subject | Evidence |
|---|---|---|
| `1174` | display: Fix direct scanout alpha on some DRM_FORMATs | `amdgpu_dm_plane.c` has `per_pixel_alpha`; reverse-applies |
| `9078` | userq: only accept doorbell BOs as queue doorbell | reverse-applies; the ledger already recorded the content as present |
| `9079` | userq: return the `memdup_user()` error | `mes_userqueue.c` has all three `memdup_user()` calls; reverse-applies |

They are **left in place** — removing a patch needs explicit user approval
(`CLAUDE.md` YOU MUST NOT 8). They cost nothing at build time (they are
skipped) but they are dead weight in the series, and their numbers could not be
reused even if they were removed, since a vacated number is evidence.

## Cleanup 2026-10-17 — three dead carries removed, `9040` excluded

The user authorised dropping what upstream has made irrelevant.

### Removed — `1174` (scanout alpha), `9078`, `9079`

All three were **preview-only** (sleepy-rc never carried any of them), and all
three reverse-apply cleanly against the pristine `next-20261016` tree — the
snapshot already contains the changes. Deleted from `patches/` and `source=()`.
Their numbers are **vacated**: `1174` is the runtime-PM patch in `sleepy-rc`
only, and `9078`/`9079` must not be reused.

### Excluded from `source=()` — `9040`

`9040` (free userptr HMM ranges on the CS error path) is still needed by
`sleepy-rc`, but this snapshot supersedes it: the base's `amdgpu_cs_ioctl()`
already has an `error_free_user_pages:` label that frees the ranges and NULLs
`e->range` before `amdgpu_cs_parser_fini()` runs. Applying `9040` on top adds a
second free loop that always sees NULL — harmless (`amdgpu_hmm_range_free()`
returns on NULL) but redundant. The file stays in `patches/` as part of the
shared series, which is the same treatment `9060` gets.

### Restored — the runtime-PM `1174`

The preview's `1174` was the scanout-alpha patch, a *different* patch from
`sleepy-rc`'s `1174` (the runtime-PM leak fix adopted on 2026-10-16), so the
preview had been **missing** the runtime-PM fix since it was adopted — the two
packages were carrying different files under the same number. With the dead one
deleted, the rc's `1174` now has its own file here and is listed in `source=()`;
it applies cleanly to the pristine snapshot. The number is now consistent across
both packages.

### Everything else stays listed

81 of the preview's carries are already present in the snapshot (see the
matching section in `sleepy-rc/PATCH_SOURCES.md`). They remain in `source=()`
and skip at build time — that is the preview's design, and removing them would
break the shared-series invariant for no runtime gain.

### Fourth pass 2026-10-17 — seven shared additions, six skip here

The seven patches adopted in `sleepy-rc/PATCH_SOURCES.md` (fourth pass) are
copied here per the shared-series invariant. On the `next-20261016` base:

| # | Preview result |
|---|---|
| `1090` | Skipping — the drm_exec fix is already in the snapshot |
| `1091` | **Applies and builds** — the only new code on this base |
| `2802` | Skipping — the swap-readahead change is already in the snapshot |
| `2900` | FAILED context — the snapshot's `copy_fs()` signature already differs; `2901` is detected as applied, so the net change is present |
| `2901` | Skipping — already in the snapshot |
| `9087` | Skipping — already in the snapshot |
| `9088` | FAILED context — the snapshot already has the staging variant of the SDMA padding change; the shared patch's `sdma_v7_0` hunk does not match its `sdma->burst_nop` guard |

`prepare()` skips every non-applying entry, so none of these is a build
failure. The new range `2900–2999` is the shared VFS/core range.

### 2026-10-18 — shared addition `2508`

`2508` (x86/insn-eval: fix shadowed segment index in
`get_seg_reg_override_idx()`, torvalds `32c52ec87d62`) is copied here per the
shared-series invariant. It applies cleanly to the `next-20261016` series tree —
forward clean with both `git apply --check` and GNU `patch`, reverse fails — so
the preview builds it too. It is absent from the snapshot's own `insn.h`.
(`2507` is not used: it belonged to the vacated September x86 PAT group.)

### Current shape

| | |
|---|---|
| Files in `patches/` | 150 |
| Entries in `source=()` | 143 |
| Excluded from `source=()` | 7 — `1008`, `1012`, `1013`, `1014`, `1017`, `9060`, `9040` |
| Preview-only adds | none; the zswap request stack (`2700`/`2701`) is absorbed by this snapshot |
| Preview-only carries | none; the 7.3-bump carries are absorbed and removed (see *Base bump to `next-20261019`*) |

## 2026-10-19 — 7.3 bump: nine preview-only carries, four shared additions, `1084` v2

`sleepy-rc` moved to `Linux 7.3` final and dropped nine patches that the release
absorbed. The preview base is unchanged (`next-20261016`), so those nine stay
in this package. The rc-bump section in `sleepy-rc/PATCH_SOURCES.md` records
their upstream commits.

| # | Result on this base |
|---|---|
| `1086`–`1090` | Already in the snapshot; `prepare()` skips them |
| `2508` | Applies; the snapshot's `insn.h` still lacks the fix |
| `2900` | Context failure; the snapshot's `copy_fs()` already differs |
| `2901` | Detected as applied; the net change is present |
| `9085` | Already in the snapshot; skips |

Four shared additions are copied here:

| # | Result on this base |
|---|---|
| `1092` | Applies after `1082`; both are in `source=()` in numeric order |
| `1178` | Applies |
| `1179` | Applies |
| `9089` | Applies |

`1084` moved from v1 to v2 (Christian König's requested unification). The
snapshot does **not** contain v1, and the v2 patch applies cleanly to the
pristine base, so the preview builds v2 as well. `pkgrel` moves from 2 to 3 to
reflect the new package contents.

`9082` (amdkfd: wait for a GPU reset before freeing a BO) was removed from both
packages on 2026-10-19 after Christian König's NAK. See the governance finding
in `sleepy-rc/PATCH_SOURCES.md`. The number is vacated.

### Retry-fault v1 → v4 (2026-10-19)

The shared series now carries upstream v4 (`9100`–`9110`) in place of the v1
series (`9011`–`9016`, `9018`–`9024`). The preview follows the rc ledger's
replacement section; `prepare()` applies or skips the v4 patches on this
snapshot exactly as it does the rest of the series.

`1093` (the gfxoff debugfs out-of-bounds write) is copied here too; it applies
to the pristine snapshot base. The earlier "already in the base" verdict was
wrong — the `0x7` guard it matched belongs to other gfxoff handlers.

## Base bump to `next-20261019` — 2026-10-19

Linux 7.3 was released on 2026-10-18 and the first post-release snapshot,
`next-20261019`, is cut from `v7.3`. The package moves from `2026.10.16-3` to
`2026.10.19-1`, and the series is reconciled against the new base rather than
left to skip at build time.

### Method

Test every entry in the 275-patch preview series against a pristine
`next-20261019` worktree in both directions with GNU `patch -F2`, then confirm
every apparent absorption with a content probe: the `+` lines a patch introduces
must be present in the base. The final series applies in order: **129/129
clean**.

The reverse test alone is not authoritative. `1093` reverse-applied at a
different `gfxoff` handler, the same wrong-function match that misled the
2026-10-15 sweep; the identifier probe kept it. The content-probe fraction
alone also misclassified it: its added lines (`size & 0x7`, `buf += 8`) exist in
the other `gfxoff` handlers, so the fraction was high while `count_read()` still
had `0x3` and `+= 4`. The function-specific check kept it. `9109`/`9110`
reported `Skipping patch` individually but failed in sequence on the old audit;
the individual content probe showed their merged form in the base, so they are
dropped.

### Dropped — 153 patches

| Group | Count | Reason |
|---|---|---|
| Reverse-applies to the base | 89 | the change is already in `next-20261019` |
| Forward `Skipping patch` | 26 | same; GNU patch detected the post-image |
| Content ≥ 85 % present | 16 | superseded by the base's newer form of the same change |
| Explicit supersession / absorption | 22 | listed below |

The absorbed set includes most of the 7.4 AMD DRM pull (`8e2d7e8d7580`,
`amd-drm-next-7.4-2026-10-08`): the retry-fault v4 `9100`–`9108`, the display
HDMI/VRR set (`0050`, `0055`, `0058`, `0059`, `0061`, `1136`, `1152`, `1154`,
`1165`, `1168`, `1171`, `1172`), and the userq lifecycle fixes. The base's
`pm` tree carries the merged CPPC hardening (`1210`–`1229`); its `mm` tree
carries the zswap rework (`2173`, `2174`, `2177`, `2190`–`2196`, `2700`,
`2701`) and the GUP/khugepaged changes; its `kbuild` tree carries the
toolchain and kallsyms work (`2302`–`2312`). The preview-only absorbed carries
`1086`–`1090`, `2508`, `2700`/`2701`, `2900`/`2901` and `9085` are gone too.

Patches superseded by a newer implementation, rather than absorbed verbatim:
`2009` (`__bh_submit` already has the `bh->b_folio` guard), `2018`
(`io_req_put_file()` unification), `2048`–`2050` (the 7.4 nvme/io_uring
completion API no longer has `pdu->status`/`pdu->result`), `2140` (the base
clears `__GFP_DIRECT_RECLAIM` for costly `__GFP_NORETRY` callers), `2150`
(`has_deposited_pgtable()` is gone), `2182` (`mod_ct++` already present),
`2311`/`2312` (the base has `init/Kconfig.toolchain` and the
`CONFIG_CC_OPT_WNO_*` form), `2400` (the trace placement is already in
`sched/core.c`), `9038` and `9072` (the checks and the SDMA callback moved to
`amdgpu_sdma_types.h`).

### Audit correction — five drops restored

A second pass checked every dropped patch for the change in its **intended
function**, not just for its added lines somewhere in the file. Four patches
had those lines in other functions of the same file and were wrongly classified
as absorbed:

| Patch | Fix that was still missing |
|---|---|
| `0034` | `dcn401_resource_destruct()` destroys the IRQ service inside the plane loop; the fix moves it after the loop. |
| `1018` | `amdgpu_discovery_set_ip_blocks()` still initializes Display before GC; the fix puts GC first. |
| `1142` | The DCE I2C setup-failure path did not close the DDC or clear `dce_i2c_hw->ddc`. |
| `9057` | `amdgpu_vm_clear_freed()` frees the mapping before checking the update result; the fix keeps it on `vm->freed` for a retry. |
| `9071` | `amdgpu_userq_create()` still publishes the queue with `xa_alloc()` without an extra kref, leaving a concurrent free able to race. |

All five apply to the base and are restored. The series is 129 patches.

### Added — seven patches

| # | Subject | Author, source | Evidence |
|---|---|---|---|
| `1094` | sdma7: don't access registers in MQD setup | Alex Deucher, `<20261019190659.2773961-4-alexander.deucher@amd.com>` | On-target SDMA 7.0; applies (2 hunks, offsets +21). The other four parts of the series target SDMA 5/5.2/6/7.1 and are not carried. |
| `1095` | call hw_fini for IP blocks whose hw_init failed (v2) | Leo Liu, `<20261019174039.9771-1-leo.liu@amd.com>` | Applies (4 hunks). Fixes a use-after-free when a block's `hw_init()` fails and its idle work fires after `sw_fini()`. |
| `1096` | Enable SDMA IB processing | Yongqiang Sun, `<20261019175807.970192-1-Yongqiang.Sun@amd.com>` | The thread has `Reviewed-by: Mukul Joshi` (conditional on a commit-message rewrite) and `Acked-by: Alex Deucher`; the carried patch keeps the original message. Partial port of the v12 hunk only (GC 12.0); the v12_1 hunk fails and targets GC 12.1. |
| `2052`–`2055` | cake v7: classifier result, split-GSO iterator, backlog cap, hash before segmenting | Jamal Hadi Salim, cover `<QDISC-BA27.v7.r0.20261019115505@mojatatu.com>` | `Reviewed-by: Victor Nogueira` on all four; `Acked-by: Toke Høiland-Jørgensen` on 2/4. Applies cumulatively in this order. net-next 7.4 content, so this snapshot is the right base. |

Considered and not adopted: `SWITCH_INSIDE_IB` (its own message says the bit is
the hardware default; no-op hardening), the userq engine-reset `13/13` series
(no review yet), and the x86/mce cache-hierarchy patch (Intel/Zhaoxin only).

### Rebased — seven patches

| Patch | Change |
|---|---|
| `1058` | call site now passes `p->adev` and uses `p->vm`/`p->adev` locals; the base's signature already takes `adev`. |
| `1070` | `sdma_v7_0_ring_pad_ib()` now uses `const bool burst_nop`; the pointer-emission rewrite was ported onto it. |
| `1202` | the per-core EPP fields were appended after the new `cpu_type` member of `struct amd_cpudata`. |
| `2036` | `find_tcp_vma()` now uses `vma_start_read_unlocked()` and one check; the `tcp_zc_vma_valid()` replacement was ported. |
| `2037` | `pneigh_queue_purge()` lost the `net` argument; the lock now wraps the base's two-argument call. |
| `2046` | the base uses `dma_max_opt_mapping_size()`; the revert now targets `dma_max_mapping_size()`. |
| `9069` | suspend/resume were rewritten on the base's function bodies with `amdgpu_userq_xa_find()`/`amdgpu_userq_put()`. |

### Compile fixes the apply audit cannot see

Two patches applied cleanly but failed to compile on the new base, the failure
mode an apply-only audit cannot detect:

- `2419` (BORE): the snapshot's new `update_protect_slice()` uses
  `normalized_sysctl_sched_base_slice`, which BORE's `#else` block removes.
  The patch now gives that function the same `CONFIG_SCHED_BORE` branch as
  `set_protect_slice()`.
- `1202` (per-core EPP boost): the base removed `AMD_CPPC_EPP_PERFORMANCE`.
  The patch now writes the CPPC EPP performance value (`0`) directly.

The first build also exposed the snapshot's sched_ext merge gaps (see section
8 above), which the config override handles.

### Still excluded from `source=()`

`1008`, `1012`, `1013`, `1014` and `1017` (the TLB-invalidation rework; `1008`
and `1014` still do not apply), `9040` (the base's `error_free_user_pages` label
already covers it; applying adds a redundant free loop), and `9060` (absorbed
upstream; applying would redefine `svm_range_window_resident()`).

### Reverts and revisions

No `Revert "..."` in `next-20261019` targets a carried patch. The only subject
match is `2046` itself, which is our revert of the nvme-pci clamp and is kept.

A full version re-check over the 16 lore mirrors (postings since 2026-01-01)
found higher-numbered postings for ten kept subjects. All but two are
content-identical resends or comment-only changes: `1175` v4, `1233` v2,
`2037` v2, `2313`/`2315`/`2317` v4 and `9063` V2. `2314` v4's additions
(`add_asm_ksymtab` and the CRC dependency emission) are already present in the
tree; `2316` v4, a 90-line relocation-cache rework, does not apply to this
base; and the `1151` v4 posting is dated 2026-02-16, older than our carried
2026-09-01 revision. No carried patch needs a newer revision.

### Verification

A pristine `next-20261019` worktree with the 129 patches applied in order
reports no failures, no `Skipping patch` and no `Reversed` hunk under GNU
`patch -p1 --forward -F2`. The build follows.

## 2026-10-20 — ten shared carries, CAKE v8, `2057` stays rc-only

The 2026-10-20 sweep adopted the same safe carries as `sleepy-rc`, minus the one
the snapshot already contains, and brought the preview-only CAKE set to v8. The
snapshot does **not** move: `next-20261020` adds no AMD GPU content, and a bump
would need `2046` dropped (absorbed) plus `0101` and `2419` rebased.

### Added — ten shared carries

`1097` (GFXOFF for compute on GFX12), `1098` (CS user fence BO in GTT), `1180`
(VRR inactive vtotal), `1181`/`1182` (drm_crtc fence lifetime), `2056`
(`tcp_wmem_schedule()` clamp), `2058` (blk-mq stale `INACTIVE` flag), `2059`/
`2060` (io_uring schedule points) and `2803` (memcg null-before-put). All apply
to the pristine snapshot. Provenance is in `sleepy-rc/PATCH_SOURCES.md`.

The eleventh rc carry, `2057` (block misaligned-bio iterator), is **not** here:
it reverse-applies cleanly to `next-20261019`, so the snapshot already has it.

### Revised in place

`1084` and `9083` move to their v3 postings, and `9084` to v3 2/2, matching
`sleepy-rc`. The changes are comment-only for `1084`/`9083`; `9084` v3 bounds
SVM ranges by the smallest GPUVM limit.

`2052`–`2055` move from CAKE v7 to **v8** (2026-10-20). v8 is a restructure:
`fq_codel` keeps its original classify shape, and its backlog guard moves inline
into `2054`; `2052` becomes cake-only and the guard sits before
`codel_set_enqueue_time()`. Tested cumulatively on a preview tree with the v7
four removed, then the v8 four applied in order — clean.

`1095` stays. Its maintainer-approved replacement (cancel the idle work in the
`hw_init()` error paths) is still under review and touches `vcn_v5_0_2`, which
this machine does not own.

### 2026-10-21 sweep — two carries and four revision refreshes

`1099` (reject CS chunks too large for `kvmalloc()`) and `1300` (KFD SMI events
only to allowed clients) join both packages. `1084` moves to v4, `9083`/`9084`
to v4 1/2 and 2/2, and `1177` to its 10-21 list posting, matching `sleepy-rc`.
The preview series is now **141** patches, all applying to `next-20261019`
(141/141).

`2804` (page_vma_mapped) and `2805` (THP `MADV_COLD`) are **not** here: both
reverse-apply cleanly to `next-20261019`, so the snapshot already contains them.
Full triage is in the 2026-10-21 sweep in `sleepy-rc/PATCH_SOURCES.md`.

### 2026-10-21 second pass — six carries, `1095` and the r8169 trio retired

`1301`–`1303` (KFD VRAM-page reuse, SVM restore backoff, mmap downgrade),
`1304` (cancel idle work in the `hw_init()` error paths), `1305`/`1306` (gfx12
queue-priority fix) join both packages. `1095` is removed: its `hw_fini`
approach was rejected upstream, and `1304` — now with `Reviewed-by: Alex
Deucher` — is the replacement Alex asked for. `2028`–`2030` (r8169 firmware
error handling) are also removed: the author withdrew the approach after
Andrew Lunn's review and no v2 followed. All four numbers are retired, not
reused.

`1303` depends on `1302` and follows it directly. The preview takes the full
`1304`; the rc copy strips only the `vcn_v5_0_2` hunk (not this IP). The preview
series is now **143** patches and all apply to `next-20261019`.

## Base bump to `next-20261021` — 2026-10-21

`sleepy-next` moves to `next-20261021` (tag `2ca9a319abef`, tip
`9a482184d910`), release `2026.10.21-1-sleepy-next`, `pkgrel=1`. The snapshot
adds **62 non-merge AMD commits** over `next-20261019` and **1066 non-merge
commits overall**. The AMD additions include the reviewed KFD doorbell-race,
GPU-reset BO-free, CWSR-reference and pinned-object-accounting fixes, plus
`set VRR_EN for inactive state`. They are now **base content** and are not
carried as patches.

### Dropped as absorbed

`1063`, `1082`, `1083`, `1085`, `1091`, `1092`, `1176`, `1181`, `1182`, `1233`,
`2046`, `2058`, `2803`. Each reverse-applies cleanly to `next-20261021` or is
present under a superseding commit. `1063`'s RCU documentation is in the base
with different wording; `1082`'s condition is in the base as
`bo_va->base.bo && !bo_va->base.moved` from `22763a52e089` (the absorbed
`1092`); `2046`'s `dma_max_mapping_size()` intent is in the base.

### Rebased

- **`0101` (bbr3):** the base added `obj-$(CONFIG_TCP_CONG_ROCCET) += tcp_roccet.o`
  at the `Makefile` anchor. Regenerated from the carried squash against the
  series state; the BBRv3 content is unchanged.
- **`2419` (BORE 7.0.0):** dropped the `update_protect_slice()` hunk. The new
  base reworked that function around `cfs_rq_min_slice()`, which already uses
  BORE's `se->slice`; forcing the old `#ifdef CONFIG_SCHED_BORE` would override
  the min-slice logic.
- **`1175` (debugfs `memdup_user_nul`):** dropped the `hdmi_automation_enable`
  hunk. The base replaced that handler with `debugfs_create_bool`; the other 18
  hunks, which fix the OOB reads, still apply.

### Added

`1307` — `gpu/buddy: do not pass caller list to __alloc_contig_try_harder()`
(commit `fb26cf4f1df4`, `Reviewed-by: Arunpravin Paneer Selvam`). This is
preview-only: the `v7.3` `drivers/gpu/buddy.c` context differs, so the rc copy
needs a rebase before it can take the patch.

### Verification

At the 2026-10-21 bump the reconciled series was **131 patches** and applied
**131/131** to `next-20261021`. The 2026-10-22 section below records the
current state: **132 patches, 132/132** to `next-20261022`. Build and BTF
results are recorded in `CHANGELOG.md`.

## Sweep 2026-10-22 — `1098` v3 and `1308` adopted; bumped to `next-20261022`

The 2026-10-22 all-source sweep re-ran the cumulative audit against
`next-20261021`: **131/131 clean**. The same-day follow-up added two patches
and bumped the snapshot:

- `1098` was replaced with v3 (Jesse Zhang,
  `<20261022024407.4187271-1-...>`). The CS user-fence BO is now accepted only
  when its preferred or allowed domain is exactly GTT, and userptrs are
  detected with `amdgpu_ttm_tt_is_userptr()`. Christian König's review asks for
  `Cc: stable` in place of the disputed `Fixes:` tag; the file keeps the
  original trailers.
- `1308` was added:
  `drm/amdgpu: don't wait for the SPM VMID's jobs under the VMID manager lock`
  v3 (Jesse Zhang, `<20261022024343.4187095-1-...>`,
  `Reviewed-by: Christian König`, `Fixes: 9b47649cabf4`). Preview-only: the
  snapshot has the `_spm` VMID rework; the rc base does not.

`_srctag` is now `next-20261022` (`bd1ecbb61afe`, cut 10-22 13:26 UTC) and the
series is **132 patches**, applying **132/132** with the cumulative audit. The
1021→1022 delta is 194 non-merge commits; no AMD target file changed. The
target-adjacent changes are the r8169 TX-LPI fix and four `sch_cake` fixes,
both covered in `sleepy-rc/PATCH_SOURCES.md`.
`updpkgsums` was run. Build and BTF results are recorded in `CHANGELOG.md`.

The full triage, including the rejected candidates and the seven orphaned
patch files on disk, is in the 2026-10-22 sweep in
`sleepy-rc/PATCH_SOURCES.md`.

## Sweep 2026-10-23 — bumped to `next-20261023`; `1309`–`1311`

`_srctag` is now `next-20261023` (`20a33c6b6cbe`, tag `77cb3534193b`, cut
10-23 16:23 +0100) and the series is **135 patches**, applying **135/135**
with the cumulative audit. The 1022→1023 delta is 167 non-merge commits
(parisc, tpm, smb, ocfs2, stackdepot, one `nvme-pci` dma-buf change); **no AMD
target file changed**.

Three patches were adopted for both packages in the same session, all from
Jesse Zhang on amd-gfx:

- `1309` — `gfx12: flush the scratch register write in the ring test`,
  `Reviewed-by: Lijo Lazar`. Five lines in `gfx_v12_0.c`; stops a measured
  39/10000 false ring-test failure on Navi 48 that escalates to a full GPU
  reset.
- `1310` — sign extend the addresses `GEM_OP(GET_MAPPING_INFO)` returns.
- `1311` — wait for the `GEM_VA` input fences interruptibly.

The same series' 2/3 (`parse CS IBs at the BO offset their VA mapping starts
at`) is already carried as `9035`; its forward dry-run fails only because the
carried line is `kptr += m->offset + …`, and the identifier probe shows the
change is present.

Preview-specific state is unchanged: `1307` (gpu/buddy) and `1308` (SPM VMID)
remain preview-only. The base already carries AMD's own HDMI FRL timeout pair
(`7f8585e6b79e`, `378e09642326`), so the external 300 ms patch is not carried
here; the rc base lacks both and keeps `1168`.

The full sweep — version pass, rejected candidates, revert scan, tracker and
Phoronix triage — is the 2026-10-23 section in `sleepy-rc/PATCH_SOURCES.md`.

## Sweep 2026-10-26 (second pass) — bumped to `next-20261026`; CAST v0.2.5 ported

`next-20261026` was cut at 13:51 UTC (`f1ac44c32cba`, tag `9269ad8f22bc`),
after the morning pass's 08:30 UTC refresh. `_srctag` is `next-20261026`
(pkgver `2026.10.26`, pkgrel 2), the series is **135 patches** and the
cumulative audit is **135/135**.

The first build of this bump (`2026.10.26-1`) still carried LRU-MARIE, with
`2101` hunk 6 rebased for `81c49e3a6848` — the commit that removed the
`comp_ret = comp_ret ? comp_ret : -EINVAL;` anchor in `zswap_compress()`.
Later the same day the package moved to **lru_cast 0.2.5**, so that rebase is
historical and `2101` is no longer carried here. The tag delta is unchanged:
**722 non-merge commits across 320 files, no AMD or DRM file changed**.

### Version sweep — resends only, again

The normalized-subject pass over all sixteen mirrors found four higher-version
postings, all already triaged in the morning pass and all content-identical or
comment-only: `1179` v2 (resend), `1309` v2 (comment wording only), `2056` v4
(delta empty), `2800` v4 (comment-only). No carried patch has a functional
update waiting.

### New candidates since the morning pass

| Candidate | Source | Verdict |
|---|---|---|
| `drm/amdgpu: reset dGPU on resume if it kept power across s2idle` (Maharshii Patel, 09-24; Mario Limonciello reply 10-26) | amd-gfx | **Inert here.** The machine boots with `mem_sleep_default=deep` and `amdgpu.runpm=0`; the patch targets s2idle-only desktops. Alex's suggested `dgpu_s0i3` branch is the same s2idle runtime-PM class |
| `drm/amdgpu: Fix DC scanout position handling` (Erhan Bilgili, 10-25; Michel Dänzer reply 10-26) | amd-gfx | **Watch, do not carry yet.** Real VRR bug: the 13-bit mask truncates scanout/vblank positions above 8191 lines at high vtotal. The reviewer agrees on the 16-bit DC decode but asked for `lower_16_bits()`/`upper_16_bits()` instead of the posted masks. Wait for v2 |
| `drm/amd/display: Fix logger leak on perf trace allocation failure` (Jackie Liu, 10-26) | amd-gfx | **Watch, no carry.** Two-line error-path leak with `Fixes:` + stable; no review yet and only reachable when `dc_perf_trace_create()` fails |
| `drm/amdkfd: Force perfmon clock on for profiler PMC requests` (Apurv Mishra, 10-26) | amd-gfx | **Rejected — feature + ABI.** 198 lines, bumps `KFD_IOC_PROFILER_VERSION_NUM`; fixes PMCs reading 0 at DPM AUTO, not a regression on this machine |
| `drm/amdkfd: bound SVM migration fence wait and guard with drm_dev_enter` v5 | amd-gfx | **Rejected — NAK.** Christian König: the entity lifetime problem is "essentially unfixable" in drm_sched and the proposed fence workaround would cause data corruption; big NAK on the series |
| `drm/amdgpu: Ensure that harvest information gets set` | amd-gfx | **Watch.** Alex Deucher still asking whether other IP-discovery tables are missed; review open |
| `drm/amd/display: Add null DC check to hpd init` | amd-gfx | **Rejected — test-only.** KUNIT calls `amdgpu_dm_hpd_init()` with `adev->dm.dc == NULL`; production never does |
| `[PATCH 00/49] DC Patches Oct 26 2026` | amd-gfx | **Rejected — 7.5 feature set.** Core 2 BLS scaffolding, staged dcn401 init splits and DCN401 PHY state reading are merge-window work, not stable fixes |
| `PCI: Preserve the initial bus number` 3/3 | amd-gfx/dri-devel | **Rejected — inert.** Only changes `pci=realloc` handling; this machine does not boot with it |
| `drm/amdgpu: Harden against potential deadlock` | amd-gfx | **Rejected — no live bug.** The author states the deadlock cannot occur today because `amdkfd_fence_ops` does not implement `signaled` |

### Tracker and Phoronix, second pass

Fifteen `drm/amd` work items moved after the morning refresh. The on-target
ones remain reports, not fixes: `#5994` (Navi 48 resume MODE1 failure, still
reproducible on 7.3.0-4, VRR path implicated), `#5965` (Navi 48 SMU hang with
hwmon `ENOTSUP`; no fan/clock control is set by the reporter), `#6011` (7.3
display flicker across Navi 3x/7900 XTX, October firmware does not help),
`#6039` (Navi 44 eGPU) and `#6038` (Raphael iGPU s2idle SMU, asking for a 7.3
repro; the dGPU here is on the deep path). No comment cites a new fix commit.

Phoronix through 10-26 15:17 EDT: the only kernel-relevant items are 7.4
merge-window summaries, the Core MM tree split, an EFI improvement, and the
cache-aware-scheduling regression fix for the Zen 5 / Zen 5C Ryzen AI 9 HX 370.
That fix is hybrid-asymmetric-packing-specific and EEVDF-side; this machine is
an eight-core homogeneous Zen 4 running BORE, so it is inert here.

### Reclaim policy — both packages now carry lru_cast 0.2.5

Later on 2026-10-26 the rc package replaced `2101` (LRU-MARIE) with
**`2102` (lru_cast)**, Marie's successor, and the preview followed. The author
shipped **v0.2.5** (`71c94c9`, 2026-10-27 00:18 +0900) while this was in
progress — a substantial update (measured per-device refault cost, anon
write-out cost, loop tie-breaking; the author's QEMU runs now show 0.28×
MGLRU's swap-ins and 12% more throughput) — so both packages carry v0.2.5,
not the v0.2.0 first evaluated.

- **rc**: the author's `0001-7.3-rc7-lru_cast-v0.2.5.patch`, byte-identical,
  zero offsets/fuzz on `v7.3`. `7.3.0-8`, 294 patches, 294/294.
- **preview**: the same patch **ported to `next-20261026`**, 135 patches,
  135/135. The port is recorded below.

### The preview port — 7.3 patch → next-20261026

The preview copy is the author's header plus a diff regenerated against
`next-20261026`, so it applies with zero fuzz. **Every difference from the
author's patch is listed here, with the upstream commit that forced it.** No
CAST logic is added, removed or invented.

| Adaptation | Why | Upstream evidence |
|---|---|---|
| `mm/migrate.c`: move the `lru_cast_migrate()` insertion to the start of `folio_migrate_flags()` | 7.4 replaced the reference-flag copy with `folio_migrate_lru_refs()` | the call is the author's, only its context moved |
| `mm/swap.h`: declaration block next to `__swap_writeout()` | base function renamed | `a6479602b783` (`__swap_writepage` → `__swap_writeout`) |
| `mm/page_io.c`: write-timing hooks after 7.4's dropbehind loop | base function restructured; `bio_associate_blkg_from_page` renamed | `48d54b07157c` (`_from_page` → `_from_folio`) |
| CAST's private helper `__swap_writeout()` renamed `cast_swap_writeout()` | the rename above gave the base function that name; a static helper of the same name with a different signature cannot compile | `a6479602b783` |
| `present_section_nr()` → `valid_section_nr()` | `SECTION_MARKED_PRESENT` removed; "present" folded into "valid" | `da7acb8982ed` |
| `is_vm_hugetlb_page()` → `vma_is_hugetlb()` | renamed | `c911e7ebebf5` |
| `PF_KSWAPD` dropped; `PF_MEMALLOC` kept | the flag was removed; `current_is_kswapd()` now checks the kthread function | `27517f701ff3` |
| augmented rbtree: `RB_DECLARE_CALLBACKS(…, size, compute)` → `RB_AUG_FUNC(oone, size, oadd)` | the macro now declares per-field augmenters and generates the compute; the `1 + left + right` aggregate is expressed by `oone()`/`oadd()` | `c2c620f4345c` |
| `VM_SPECIAL` → `VM_IO \| VM_DONTEXPAND \| VM_PFNMAP \| VM_MIXEDMAP` | the composite macro was eliminated; the explicit set is exactly its old definition | `72a993449cb0` |
| direct `#include`s of `<linux/mm.h>`, `<linux/hugetlb.h>`, `<linux/mmzone.h>` | 7.4 removed transitive includes the 7.3 build happened to rely on | header hygiene, no code change |

`lru_cast_tune_osize()` is kept although the new rbtree macro no longer calls
it: `sim.c` uses it in its own size fix-up. `lru_cast_tune_ocompute()` is
replaced by the macro-generated compute, which implements the same
early-exit-on-unchanged test.

A check for invented code: the port's diff against the author's patch yields
only the rows above; every other added line is byte-identical to the author's
added line. The rc copy is byte-identical to
`0001-7.3-rc7-lru_cast-v0.2.5.patch` (sha256
`288386b09f673d0d8d713d2398bb6c064145c063805946047a4d85bf53093ce3`).
All touched objects (`mm/lru_cast/`, `mm/page_io.o`, `mm/migrate.o`,
`mm/vmscan.o`, `mm/folio.o`, `mm/memory.o`, `mm/huge_memory.o`,
`mm/memcontrol.o`, `mm/shmem.o`, `mm/rmap.o`, `mm/workingset.o`,
`mm/page_alloc.o`, `mm/swapfile.o`, `mm/swap_state.o`, `mm/khugepaged.o`,
`kernel/sched/core.o`) compile on `next-20261026` with the port. The full
package built with Clang 23.1.4 and the installed kernel reports
`lru_cast v0.2.5 by Masahito Suzuki` with `.BTF`/`.BTF_ids`. A line-set diff
of the port against the author's patch yields only the rows above (and the
author's email `-- ` separator, which is not code).

`vm.swappiness` stays **1** in both packages: CAST's file-first promise, not
the measured split. The compatibility evidence and swappiness rationale are
in `sleepy-rc/PATCH_SOURCES.md`.

## Bump to `next-20261027` — 2026-10-27

`next-20261027` was cut at 14:33 UTC on 2026-10-27 (`151a134a4e6e`, tag object
`27e28adce2ba`). `_srctag` is `next-20261027`, pkgver `2026.10.27`, pkgrel 1.
The snapshot delta from `next-20261026` is **460 commits across 196 files**
(5,111 insertions, 11,071 deletions). No `drivers/gpu/drm/amd` file changed;
the touches inside this build's target paths are `block/`, `io_uring/`,
`kernel/sched/ext`, `mm/` (including `mm/migrate.c` and `mm/swapfile.c`),
`net/sched` and `mm/vmalloc.c`.

The series is **136 patches** and the cumulative audit is **136/136** against
`next-20261027`. All 135 pre-existing patches still apply; nothing needed a
rebase for this snapshot. Two additions/changes from the 2026-10-27 sweep:

- **`1312`** — `drm/amdgpu: check amdgpu_vm_ready() in dma-buf move notify`
  (Dariusz Marcinkiewicz, `Reviewed-by` and "Applied!" from Alex Deucher).
  Applies to both bases.
- **`1309` v2** — comment-wording refresh of the gfx12 ring-test flush; the
  code is unchanged and `Reviewed-by: Lijo Lazar` is retained.

### lru_cast v0.2.6 port

The author released **v0.2.6** (`2b1e212`, 2026-10-27 07:31 +0900) on top of
v0.2.5. The only source change is in `mm/lru_cast/policy/balance.c`:
`lru_cast_pick()` reads each type's size from the LRU lists with
`lru_cast_lru_size()` instead of `lruvec_page_state()`, because a memcg's
counters can still read zero for a cgroup new to its limit and leave reclaim
with nothing to scan. `version.h` moves to `0.2.6`.

The preview copy is the v0.2.5 port with exactly that delta — the six-line
comment above `lru_cast_pick()`, the four `lru_cast_lru_size()` calls and the
version string. `mm/lru_cast/policy/balance.c` and `version.h` produced by
applying it are byte-identical to the author's v0.2.6 patch. The ten 7.4
adaptations recorded in the previous section are unchanged: a line-set diff
against the author's v0.2.6 yields only those rows and the author's `-- `
separator. The rc copy is byte-identical to
`0001-7.3-rc7-lru_cast-v0.2.6.patch`.

The port applies cleanly to a pristine `next-20261027` tree with `git apply
--check` and GNU `patch`, and the rc copy applies to `v7.3` the same way. Both
packages built with Clang 23.1.4 and are installed side by side; the integrity
checks are recorded in the rc ledger.

## Bump to `next-20261028` — 2026-10-28

`next-20261028` was cut at 14:40 UTC on 2026-10-28 (`6d0933ae9d46`, tag object
`5fed66a6fde4`). `_srctag` is `next-20261028`, pkgver `2026.10.28`, pkgrel 2
after `1313` was added.
The snapshot delta from `next-20261027` is **613 commits across 355 files**
(12,563 insertions, 16,890 deletions), 143 of the files in this build's target
paths. Unlike the previous snapshots, this delta carries the AMD merge-window
content: nine patches the preview was carrying are now in the base.

The series is **128 patches** and the cumulative audit is **128/128** against
`next-20261028`.

### Absorbed — nine patches dropped

Each patch below failed forward and reverse-applied cleanly against the
pristine snapshot, and its upstream commit is in `next-20261028`:

| Drop | Upstream commit |
|---|---|
| `1084` drop the gang leader reference when freeing gang jobs | `df4d6d404d44` |
| `1096` Enable IB execution for user-mode SDMA queues | `1ac3b84e10d2` |
| `1097` re-enable GFXOFF for compute on GFX12 | `f6d97ecb68b8` |
| `1099` reject CS chunks too large for kvmalloc() | `dab5f5280406` |
| `1174` take a runtime PM reference only when a CRTC turns on | `59ef9a435499` |
| `1300` send SMI process and VM fault events only to allowed clients | `77f5f4eae104` |
| `1308` don't wait for the SPM VMID's jobs under the VMID manager lock | `55ca06a52a09` |
| `9086` validate SRAT subtables before parsing | `d76b655c98e8` |
| `9089` split vram_pages of SVM ranges prefetched without a GPU mapping | `7ca6f3359b55` |

The nine above are removed from `source=()` and from this package's `patches/`
tree only — `sleepy-rc` keeps them, because `v7.3` does not contain the
upstream commits. The preview tree still holds seven files that are not in
`source=()`: `1008`/`1012`/`1013`/`1014`/`1017` (excluded by the PKGBUILD's
own comment) and the retired `9040`/`9060`; they are not part of the series.

### `2152` superseded — dropped

`2152` (Nguyen Ngoc Thang, "khugepaged: hold invalidate_lock across
collapse_file() readahead") is no longer needed. `next-20261028` contains
`f1ce4414a570` ("khugepaged: fix readahead lock inversion in collapse_file()",
Lance Yang, `Reviewed-by: Pedro Falcato`, `Acked-by: David Hildenbrand` and
`Acked-by: Zi Yan`), a different implementation of the same fix that releases
the folio locks and retries after rollback. The two conflict, and the merged
revision is the reviewed one. `sleepy-rc` keeps `2152`: the merged fix does not
apply to `v7.3` (two hunks fail), so the carried form is still the only fix
there.

### `1302` rebased

`next-20261028` contains `266fab831396` ("drm/amdkfd: stop restore retries on
device unplug"), which changes the same `svm_range_restore_work()` reschedule
block and adds the `r != -ENODEV` guard. The preview copy of `1302` is rebased
onto that state: the added `restore_delay_ms` backoff is unchanged, the
reschedule now runs only under the upstream guard, and the debug message
reports the current delay. The changed-line set is identical to the original
posting (no lines added or removed). `sleepy-rc` keeps the original `1302`,
which applies to `v7.3` where the guard does not exist.

### lru_cast v0.2.8 port

The author released v0.2.7 and v0.2.8 on 2026-10-28, after the v0.2.6 carried in
the 2026-10-27 release. The preview copy is the v0.2.6 port plus the author's
v0.2.6 → v0.2.8 delta, applied as a three-way merge; all hunks applied cleanly.
The result differs from the author's v0.2.8 patch only in the same 7.4 API
adaptations recorded for v0.2.6 (rbtree augment macro, `__swap_writeout()`
rename, `valid_section_nr()`, `vma_is_hugetlb()`, expanded `VM_SPECIAL`, and
the `PF_KSWAPD` removal). The rc copy is the author's
`0001-7.3-rc7-lru_cast-v0.2.8.patch` byte-for-byte. Both series audit clean
with it.

The same source check covered the author's NAP governor: **v0.5.1** (stable,
2026-10-11) replaces v0.5.0 in both packages. It applies to this snapshot at
zero fuzz and its delta is recorded in the rc ledger.

### Base churn — `group_cpus` dropped from the 1028 mm tree

`next-20261027` carried `d39303f30314` ("lib/group_cpus: snapshot cluster masks
to keep grouping hotplug invariant", the v1–v4 content) in its mm tree. The
1028 mm tree was rebuilt without it, and `lib/group_cpus.c` is back to the
pre-fix content. The other mm commits that appear in
`next-20261027 ^ next-20261028` are re-hashed copies present in 1028
(`mm/zswap` dlen `9ebe19ab4762`, `mm/vmalloc` `4685a28187f4`, `mm/ksm`
`041b9b7eb14f`, `mm/migrate` `930eec1958e9`, swapoff `b779ef016df0`);
`group_cpus` is the only on-target one lost.

This is the NVMe managed-IRQ affinity fix that `sleepy-rc` carries as `2044`,
and the failure mode is this machine's NVMe across an s2idle cycle, so the
preview now carries **`2044` v5** as well. It applies to the pristine
`next-20261028` tree with zero fuzz and takes the series to 127 patches.

`1313` (`drm/amdkfd: use the queue's process info for the WPTR BO eviction
fence`, Jesse Zhang, `Reviewed-by: Felix Kuehling`) is the one new carry of
this sweep. It fixes a NULL dereference when a WPTR BO exported with
`AMDKFD_IOC_EXPORT_DMABUF` is imported on a second render node, applies to this
base with offsets only, and is carried by both packages. The series is **128
patches**.

`2800` stays rc-only: `next-20261028` already carries its fix
(`sync_with_folio_pmd_zap()` in `mm/internal.h` and `mm/memory.c`).

### Series state

Both packages passed `audit_series.py` after the changes: **295/295** on
`v7.3` and **128/128** on `next-20261028`.

## Sweep 2026-10-29 — `next-20261029`; six new carries, 134 patches

The preview bumps from `next-20261028` to `next-20261029` (`557` commits) and
takes the six patches adopted by the 2026-10-29 sweep: `1234`, `1235`, `1236`,
`2061`, `2062` and `2806`. Five apply byte-for-byte; `2806` is the form
regenerated over `2102`'s lru_cast hooks, shared with the rc series. Their
provenance, sources and review status are recorded once in
`sleepy-rc/PATCH_SOURCES.md` under *Sweep 2026-10-29*.

### Base churn

No carried patch was absorbed by the snapshot: the full 128-patch series
applied unchanged, and a reverse-applicability scan found no real duplicate
(`1093` reverse-matches only through a context accident at offset -745; its
target still has `size & 0x3` in the base).

The new snapshot pulls the `amd-drm-next-fixes-7.4-2026-10-28` merge into its
base. That is merge-window content the preview gets for free; the patches that
also exist in the rc series (for example `1097`, `1099`, `1174`, `1300`,
`9086`, `9089`) remain rc-only because the preview base already provides them.

### Series state

Both packages passed `audit_series.py` after the changes: **302/302** on
`v7.3` and **134/134** on `next-20261029`.
