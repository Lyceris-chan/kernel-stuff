# Triage: what disqualifies a candidate

A patch is not a candidate because it applies. These are the ways a patch that
applies cleanly still does nothing, or does harm.

## Contents

- [This machine's IP blocks](#this-machines-ip-blocks)
- [Wrong-chip traps](#wrong-chip-traps)
- [Inert-under-config](#inert-under-config)
- [Upstream reverts](#upstream-reverts)
- [Provenance](#provenance)
- [Apply checking](#apply-checking)
- [Base mismatch](#base-mismatch)

## This machine's IP blocks

Read from the running kernel, not inferred. Re-check after any hardware or
firmware change:

```bash
sudo dmesg | grep -i 'detected ip block'
```

| Block | This machine | Not this machine |
|---|---|---|
| GPU core | `gfx_v12_0_0` (GC 12.0) | `gfx_v12_1` (GC 12.1), `gfx_v9_4_2` (CDNA) |
| Display | **DCN 4.0.1** (`dcn401`) | `dcn42`/`dcn42b`, `dcn50`, `dcn60`, `dcn30` |
| SMU | `smu_v14_0_0` | `smu_v14_0_2` / `smu_v14_0_3` |
| PSP | `psp_v14_0_0` | — |
| SDMA | `sdma_v7_0_0` | `sdma_v7_1` |
| VCN | `vcn_v5_0_0` | `vcn_v4_*` |
| CPU | Zen 4, `amd-pstate` on CPPC | Intel, ARM/SoC |

Datacenter-only files that appear in broad refactors: `aqua_vanjaram.c`,
`soc_v1_0.c`, `gfx_v9_4_2.c`, `kfd_int_process_v9.c`.

## Wrong-chip traps

**A patch that applies, compiles, and runs on code this machine never
executes.** This is the single most expensive class here: it passes every apply
check, ships, and does nothing.

The failure mode is a shared *filename pattern* with a version that is not ours.

- **`dcn30_apply_idle_power_optimizations()`** is DCN 3.0. DCN 4.0.1 has its own
  `dcn401_apply_idle_power_optimizations()` (`dcn401_init.c`). A MALL-hysteresis
  fix for DCN30 looked like a perfect match for this machine's 240 Hz monitor and
  is dead code here.
- **`smu_v14_0_2_ppt.c`** serves IP versions 14.0.2 and 14.0.3. This machine is
  14.0.0, which takes `smu_v14_0_0_set_ppt_funcs()`. Check the `IP_VERSION`
  switch in `amdgpu_smu.c`, not the filename.
- **`gfx_v12_1.c`** is a different ASIC from `gfx_v12_0.c`.
- **`dcn42_hwseq.c`** is DCN 4.2, instantiated only under
  `AMDGPU_FAMILY_GC_11_5_0` (Strix-class APUs).

Before adopting anything under `drivers/gpu/drm/amd/`, confirm the target file is
in this machine's set:

```bash
rg -n 'IP_VERSION\(12,0|IP_VERSION\(14,0,0' repos/torvalds/drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c
```

**A tip-only sweep hides these.** Branch sweeps have surfaced six on-target
commits a tip-only pass missed, two of them wrong-chip traps that read as
plausible fixes.

## Inert-under-config

A patch can be correct, on-target, and still not execute because the subsystem
is owned by something else here, or the feature is off.

| Subsystem | Status here | Consequence |
|---|---|---|
| `tools/sched_ext/*.bpf.c` | userspace samples; this box runs `cake_1.2.1` from the `scx-scheds` package | any `scx_qmap` change is inert |
| `fair.c` | sched-ext is active via `scx_loader` | core-EEVDF patches are inert; sched-ext patches are not |
| MGLRU | inert under LRU-MARIE (`lru_gen_enabled()` false) | `mm/mglru` patches do nothing |
| xswap writeback | xswap has no backing store | dropbehind/writeback-completion paths unreachable |
| ASPM | `pcie_aspm=off` on the cmdline | ASPM refactors are inert |
| SME | `CONFIG_AMD_MEM_ENCRYPT=y` but SME is not active | `mem_encrypt.c` fixes unreachable |
| `select`ed symbols | — | patching a symbol the config does not enable |
| `--set-str` on a removed symbol | — | silently no-ops |
| `dcn30_*` / `smu_v14_0_2_*` | see above | applies, compiles, never runs |

Confirm the subsystem is owned by the code being patched before adopting.

## Upstream reverts

Grep the lists and trees for a revert of anything already carried:

```bash
git -C repos/torvalds log --all --oneline --grep='Revert' --since=<date>
zcat /tmp/amd-gfx-*.txt.gz 2>/dev/null | rg '^Subject:.*Revert' | sort -u
```

AMD reverting its own patch (*"because it causes some regression"*) means the
carried copy should go too. The DCN4 flip-schedule pair `9051`/`9052` is the
worked example.

## Provenance

Required: a named human author, a `Signed-off-by`, and a traceable commit hash
or Message-ID.

`Assisted-by:` and `Co-developed-by:` trailers do **not** disqualify a patch.
What is forbidden is a fabricated diff with no traceable source — report it
rather than inventing one.

A second `Signed-off-by` from an AMD maintainer (Alex Deucher, Mario
Limonciello) is a strong positive signal that the patch is on its way upstream.

## Apply checking

Both, always:

```bash
git -C <tree> apply --check "$cand"
patch -d <tree> -p1 --forward -F2 --dry-run < "$cand"
```

`git apply` tolerates context GNU `patch` rejects — a context line that gained a
prefix, for example. GNU patch catching it is the point.

Read the *output*, not just the exit status. `Skipping patch` / `Reversed …` is
an inert no-op, not a success. And a missing target directory makes `patch`
print `Can't change to directory …` and **exit 0**, so neither the message
patterns nor `$?` catch it — assert the tree exists before the loop.

For a file absent from the base, strip its hunks and stats line and document
that.

## Base mismatch

A newer revision is not automatically the right one. A patch written against a
kernel newer than this base will fail in **both** directions, and its deltas
often reference APIs the base lacks.

Before adopting a newer revision, test both directions. If neither is clean, the
delta is usually an adaptation to a post-base API change — `gso_segment`
signature changes and `in_nmi()`-based kfunc guards are two seen in one sweep.
Keep the version written for this base and revisit at the next bump.

Conversely, a revision that **reverse-applies** cleanly is already carried; the
higher version label is a resend, not an update.
