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
| Snapshot | `next-20261009`, tag `becb95e45ef0` |
| Source | `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git/snapshot/next-20261009.tar.gz` |
| Snapshot tree `Makefile` | `7.3.0-rc6` — the base rc, **deliberately not used in the release name** |
| Kernel release | `2026.10.09-1-sleepy-next` |
| Package | `linux-sleepy-next-2026.10.09-1` |

### Versioning: the snapshot date, not the base rc

`pkgver` is the snapshot date, derived from `_srctag` — `_snapdate=${_srctag#next-}`
(`20261009`) and `_snapver` respells it dotted (`2026.10.09`) — so a bump cannot
move the tag without moving the version.

**The dots are load-bearing, not cosmetic.** Both tools that consume the release
string require it to *begin* with dotted decimal notation:

| Tool | Requirement | Failure without it |
|---|---|---|
| `depmod` (kmod 34.2) | an `N.N` prefix; a bare `20261009-1-sleepy-next` is rejected as `Bad version passed` | post-install depmod hook fails, no module dependencies generated |
| `mkinitcpio` (42.2) | `kver()` validates the release extracted from the image against `^[[:digit:]]+(\.[[:digit:]]+)+` | initramfs build fails — **the kernel is left with no initramfs at all** |

A bare `20261009` therefore cannot be the release name. Dots are legal in
`pkgver`; only `-` is reserved, as the pkgver/pkgrel separator.

`prepare()` rewrites the snapshot's `Makefile` so `KERNELVERSION = 2026.10.09`.
Left alone, the tree composes `KERNELVERSION` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL`/`EXTRAVERSION` and stamps its **base** rc into
the name: `next-20261009` is cut from `v7.3-rc6`, so the kernel announced itself
as `7.3.0-rc6-1-sleepy-next`. That is wrong twice over — stale, because the tree
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

The tree's own `localversion-next` (containing `-next-20261009`) is still
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

| Patch | Role | Applies to `next-20261009`? |
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
