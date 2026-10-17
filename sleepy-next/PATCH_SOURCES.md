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
| Snapshot | `next-20261016`, tag `2efb7a11f1aa` |
| Source | `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git/snapshot/next-20261016.tar.gz` |
| Snapshot tree `Makefile` | `7.3.0-rc7` — the base rc, **deliberately not used in the release name** |
| Kernel release | `2026.10.16-1-sleepy-next` |
| Package | `linux-sleepy-next-2026.10.16-1` |

### Versioning: the snapshot date, not the base rc

`pkgver` is the snapshot date, derived from `_srctag` — `_snapdate=${_srctag#next-}`
(`20261016`) and `_snapver` respells it dotted (`2026.10.16`) — so a bump cannot
move the tag without moving the version.

**The dots are load-bearing, not cosmetic.** Both tools that consume the release
string require it to *begin* with dotted decimal notation:

| Tool | Requirement | Failure without it |
|---|---|---|
| `depmod` (kmod 34.2) | an `N.N` prefix; a bare `20261016-1-sleepy-next` is rejected as `Bad version passed` | post-install depmod hook fails, no module dependencies generated |
| `mkinitcpio` (42.2) | `kver()` validates the release extracted from the image against `^[[:digit:]]+(\.[[:digit:]]+)+` | initramfs build fails — **the kernel is left with no initramfs at all** |

A bare `20261016` therefore cannot be the release name. Dots are legal in
`pkgver`; only `-` is reserved, as the pkgver/pkgrel separator.

`prepare()` rewrites the snapshot's `Makefile` so `KERNELVERSION = 2026.10.09`.
Left alone, the tree composes `KERNELVERSION` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL`/`EXTRAVERSION` and stamps its **base** rc into
the name: `next-20261016` is cut from `v7.3-rc7`, so the kernel announced itself
as `7.3.0-rc7-1-sleepy-next`. That is wrong twice over — stale, because the tree
carries weeks of work past rc6, and easily mistaken for `linux-sleepy-rc`'s
genuine `7.3.0-rc7-1-sleepy-rc`.

Only the release *string* moves. `version.h` derives `LINUX_VERSION_CODE` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL` (`Makefile`: `filechk_version.h`), **not** from
`KERNELVERSION`, so those stay `7`/`3`/`0` and out-of-tree version checks keep
working. `include/generated/utsrelease.h` and every `modules_install` path read
`KERNELRELEASE`, which is regenerated from `KERNELVERSION`, so `uname -r`, the
module directory and the packaged paths all agree.

`prepare()` asserts the rewrite landed and aborts the build if it did not, rather
than shipping a kernel that misreports its own release.

The tree's own `localversion-next` (containing `-next-20261016`) is still
deleted: the date is already `KERNELVERSION`, so keeping it would print it
twice.

## Preview-specific deltas

### 1. Patches that do not apply are SKIPPED, not failed

`prepare()` dry-runs every patch and skips it outright when it does not apply, so
a snapshot that has moved past the series still produces a build. A linux-next
snapshot is not a stable base: it already contains much of what the 7.3-rc6-era
series adds, so a large fraction of the series is skipped.

Skipping is only safe for a **self-contained** patch. A patch that *declares* a
symbol another patch *uses* must not be skipped while its consumer applies —
that yields a compile error rather than a clean miss. Where the series had such
an interdependent group, the whole group is excluded instead (see 2).

### 2. Excluded from `source=()`: the amdgpu TLB-invalidation rework

`1008`, `1012`, `1013`, `1014` and `1017` are **not listed** in the preview
`source=()`. All five are retained in full in `sleepy-rc`.

| Patch | Role | Applies to `next-20261016`? |
|---|---|---|
| `1008` | adds `amdgpu_buffer_funcs::tlb_inv_num_dw` and `amdgpu_emit_tlb_inv()` | no |
| `1012` | sdma7 TLB-invalidation consumer | yes |
| `1013` | core TLB-invalidation helper | yes |
| `1014` | further gmc tlb-inv helpers | yes |
| `1017` | gmc12 TLB-invalidation consumer | yes |

`1008` no longer applies while `1012`/`1013` do — and those consume exactly the
struct member and helper that `1008` introduces. Carrying the group partially
does not compile:

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

### Current shape

| | |
|---|---|
| Files in `patches/` | 279 |
| Entries in `source=()` | 272 |
| Excluded from `source=()` | 7 — `1008`, `1012`, `1013`, `1014`, `1017`, `9060`, `9040` |
| Preview-only adds | `2700`, `2701` (zswap request stack) |
