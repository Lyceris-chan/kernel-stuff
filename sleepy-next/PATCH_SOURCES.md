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
| Snapshot tree `Makefile` | `7.3.0-rc6` |
| Kernel release | `7.3.0-rc6-1-sleepy-next` |
| Package | `linux-sleepy-next-7.3.0_rc6-1` |

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

### 5. Cmdline

`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is **dropped in the preview only**;
`sleepy-rc` keeps it. The preview exists to exercise the snapshot's display code
with IPS left enabled rather than masked off by the 7.3-era workaround.

```
cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0
```
