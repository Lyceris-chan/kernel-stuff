# Changelog

Notable changes to the `linux-sleepy-rc` and `linux-sleepy-next` packages. They
target one machine: an AMD Ryzen 7 7700 (Zen 4) with a Radeon RX 9070 XT
(Navi 48 / RDNA 4).

One entry per released package version, newest first. A version is what
`uname -r` reports. `sleepy-rc` uses `<kernel base>-<pkgrel>-sleepy-rc`, as in
`7.3.0-1-sleepy-rc`. `sleepy-next` uses
`<snapshot date>-<pkgrel>-sleepy-next`, as in `2026.10.09-1-sleepy-next` — the
snapshot's own date, never the mainline `-rc` it happened to be cut from. The
date is dotted because `depmod` and `mkinitcpio` both reject a release that does
not begin with dotted decimal notation. The format follows
[Keep a Changelog](https://keepachangelog.com/).

Two earlier artifacts are summarised at the end under
[Earlier packages](#earlier-packages): the 7.2 `linux-sleepy` package and the
`wannabe-7.3` preview tree. Both were removed from the working tree, and their
full entries remain in git history.

## [2026.10.27-1-sleepy-next (linux-next `next-20261027`)]: 2026-10-27

Preview bump from `next-20261026` to `next-20261027` — 460 commits across 196
files, with no `drivers/gpu/drm/amd` file changed — plus **lru_cast v0.2.6**,
the reviewed `1312` dma-buf hang fix and the `1309` v2 comment refresh. The
series is **136 patches** and the cumulative audit is **136/136**.

### Changed

- **lru_cast 0.2.6** — `lru_cast_pick()` reads each type's size from the LRU
  lists with `lru_cast_lru_size()` instead of the periodically summed memcg
  counters. A cgroup new to its limit could report zero pages, leaving reclaim
  with nothing to scan and the charge OOM. The rc copy is the author's
  `0001-7.3-rc7-lru_cast-v0.2.6.patch` byte-for-byte; the preview copy is the
  v0.2.5 port plus the same six-line comment, four call-site changes and
  version string.
- **`1312`** — `drm/amdgpu: check amdgpu_vm_ready() in dma-buf move notify`
  (Dariusz Marcinkiewicz, `Reviewed-by` and "Applied!" from Alex Deucher). A
  SIGKILLed process's stopped VM entities are no longer used to clear PTEs
  while imported dma-bufs are torn down; without it the task hangs.
- **`1309` v2** — comment-only refresh of the gfx12 ring-test flush; the
  `RREG32(scratch)` and the `Reviewed-by: Lijo Lazar` are unchanged.

### Sweep

All source classes were queried: every branch of the eight kernel trees, the
lore mirrors, both freedesktop October archives, the drm/amd work-item tracker
by update time, and Phoronix. The version sweep found seven higher-version
postings: three content-identical resends, two reviewer replies quoting the
patch, one already the carried revision, and only `1309` v2 was real. No
carried patch was reverted upstream. No carried preview patch is absorbed by
the new snapshot; `1093` reverse-applies only to the wrong function and the
base still has the bug.

New candidates were triaged, not merged. `1312` was adopted. The DC
scanout-position mask fix, the MES timeout report, the DC logger leak, the
discovery harvest fix and the GPU-reset ordering series are watch items with
open review requests. The dGPU s2idle reset was redirected to the runtime-PM
`dgpu_s0i3` branch. The ATOM underflow fix was dropped upstream after an
atombios regression. The in-base `vupdate_no_lock` consolidation has a
three-patch revert posted for gfx1201 multi-monitor corruption but no
maintainer reply, so it stays a watch item.

### Verification

Cumulative audit **136/136** against `next-20261027`. Package
`linux-sleepy-next-2026.10.27-1` (23.1 MB) and headers (34.8 MB) built with
**ClangBuiltLinux clang 23.1.4**. The extracted `vmlinux` carries `.BTF` and
`.BTF_ids`, reports `lru_cast v0.2.6 by Masahito Suzuki`, has
`CONFIG_TCP_CONG_BBR3=y` with old `tcp_bbr` absent, and the built-in cmdline is
`cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0`.
Installed side by side with the rc package; no reboot or shutdown.

## [7.3.0-9-sleepy-rc (Linux 7.3)]: 2026-10-27

lru_cast v0.2.6, the reviewed `1312` dma-buf fix and the `1309` v2 refresh. The
base stays `v7.3`; the series moves to **295 patches** and audits **295/295**.

### Verification

Package `linux-sleepy-rc-7.3.0-9` (22.8 MB) and headers (34.5 MB) built with
Clang 23.1.4. The extracted `vmlinux` carries `.BTF` and `.BTF_ids`, reports
`lru_cast v0.2.6 by Masahito Suzuki`, has `CONFIG_TCP_CONG_BBR3=y` with old
`tcp_bbr` absent, and the built-in cmdline still has `amdgpu.dcdebugmask=0x800`.
The rc patch is byte-identical to the author's (sha256 `aeae9c32…`). Installed
side by side with the preview; no reboot.

## [2026.10.26-2-sleepy-next (linux-next `next-20261026`)]: 2026-10-26

Reclaim-policy update: the preview replaces LRU-MARIE with **lru_cast 0.2.5
(CAST)**, ported to this base, as patch `2102`. The rc package moved to the
same release in `7.3.0-8`; both packages now run one policy. The snapshot and
the 135-patch series are unchanged, and the cumulative audit is **135/135**.

### Ported — the author's 7.3 patch applied to next-20261026

The 7.3 patch does not apply as-is to the 7.4-merge-window code. Every change
is a mechanical adaptation, each forced by a traceable upstream commit; an
automated line-set diff against the author's patch shows no other differences:

- `mm/migrate.c` — `lru_cast_migrate()` moves to the start of
  `folio_migrate_flags()`, before 7.4's `folio_migrate_lru_refs()` call.
- `mm/swap.h` — the handoff/kcompressd declarations move next to the renamed
  `__swap_writeout()` (`a6479602b783`).
- `mm/page_io.c` — the write-timing hooks go after 7.4's dropbehind loop;
  `bio_associate_blkg_from_page()` became `…_from_folio()` (`48d54b07157c`).
- CAST's private helper `__swap_writeout()` is renamed
  `cast_swap_writeout()` because the 7.4 rename (`a6479602b783`) gave the base
  function that name.
- `present_section_nr()` → `valid_section_nr()` (`da7acb8982ed` — "present"
  folded into "valid").
- `is_vm_hugetlb_page()` → `vma_is_hugetlb()` (`c911e7ebebf5`).
- `PF_KSWAPD` dropped from `kcompressd` (removed by `27517f701ff3`; the flag's
  Intel-GPU workaround does not apply, and `current_is_kswapd()` now checks
  the kthread function instead).
- Augmented rbtree: the old `RB_DECLARE_CALLBACKS(…, size, compute)` becomes
  `RB_AUG_FUNC(oone, size, oadd)` for the new per-field API
  (`c2c620f4345c`); the generated compute keeps the same early-exit test.
- `VM_SPECIAL` → `VM_IO | VM_DONTEXPAND | VM_PFNMAP | VM_MIXEDMAP`
  (`72a993449cb0` — exactly the old macro's definition).
- Direct `<linux/mm.h>`, `<linux/hugetlb.h>`, `<linux/mmzone.h>` includes,
  because 7.4 removed transitive includes the 7.3 build relied on.

The preview copy is the author's header plus a diff regenerated against
`next-20261026`; it applies with zero fuzz and passes `git apply --check` and
GNU `patch`. The rc copy is the author's patch byte-identical
(sha256 `288386b09f673…`).

### Toolchain — Clang 23.1.4 from kernel.org

Both packages now use the kernel.org ClangBuiltLinux
`llvm-23.1.4-x86_64.tar.xz`. 23.1.4 is the newest release on both
`mirrors.edge.kernel.org/pub/tools/llvm/` and the llvm-project GitHub
releases (published 2026-10-20). It is a multicall build (`clang`, `ld.lld`
and the `llvm-*` tools are symlinks to one `llvm` binary), links only the
system `libz`/`libzstd`/`libstdc++`, and needs no bundled ICU libs — so the
GitHub `LLVM-23.1.0-Linux-X64` tarball and `llvm-icu70-libs.tar.gz` are gone.

### Verification

Cumulative audit **135/135** against `next-20261026`. Package
`linux-sleepy-next-2026.10.26-2` (22.8 MB) and headers (34.8 MB) built with
**ClangBuiltLinux clang 23.1.4** (`CONFIG_CC_VERSION_TEXT` in the image). The
extracted `vmlinux` carries `.BTF` and `.BTF_ids`, reports
`lru_cast v0.2.5 by Masahito Suzuki`, has `CONFIG_LRU_CAST=y` (no
`LRU_MARIE` symbol) and `CONFIG_TCP_CONG_BBR3=y` with old `tcp_bbr` absent
from `modules.builtin`. The built-in cmdline matches this package's PKGBUILD
(no rc-only `dcdebugmask`). The port passes `git apply --check` and GNU
`patch` with zero fuzz; a line-set diff against the author's patch yields only
the adaptations listed above and nothing else. Installed; initramfs rebuilt;
the running kernel remains `2026.10.23-1` until the next reboot (none was
performed).

## [7.3.0-8-sleepy-rc (Linux 7.3)]: 2026-10-26

lru_cast upgraded from v0.2.0 to **v0.2.5**, released the same day. The new
revision measures per-device refault queues and anon write-out cost, adds a
decay floor and hash tie-breaking for looped working sets, and reports 0.28×
MGLRU's swap-ins with 12% more throughput in the author's QEMU runs. The
patch is the author's byte-identical
`0001-7.3-rc7-lru_cast-v0.2.5.patch`; the series stays at 294 patches and
audits **294/294**. `vm.swappiness` stays 1 (CAST's file-first promise).

### Toolchain — Clang 23.1.4 from kernel.org

Both packages now use the kernel.org ClangBuiltLinux
`llvm-23.1.4-x86_64.tar.xz` — the newest on both the kernel.org mirror and
the llvm-project GitHub releases. It is a multicall build with no ICU
dependency, so the GitHub 23.1.0 tarball and `llvm-icu70-libs.tar.gz` are
dropped. See the 2026.10.26-2 entry for the full note.

### Verification

Cumulative audit **294/294** against `v7.3`. Package
`linux-sleepy-rc-7.3.0-8` (22.6 MB) and headers (34.5 MB) built with
**ClangBuiltLinux clang 23.1.4**. The extracted `vmlinux` carries `.BTF` and
`.BTF_ids`, reports `lru_cast v0.2.5 by Masahito Suzuki`, has
`CONFIG_LRU_CAST=y` (no `LRU_MARIE`), `CONFIG_TCP_CONG_BBR3=y` with old
`tcp_bbr` absent, and the built-in cmdline still has `amdgpu.dcdebugmask=0x800`.
The rc patch is byte-identical to the author's (sha256 `288386b0…`). Installed
side by side with the preview, both initramfs images rebuilt, systemd-boot
default unchanged. No reboot was performed.

## [7.3.0-7-sleepy-rc (Linux 7.3)]: 2026-10-26

Reclaim-policy refresh: the rc package replaces **LRU-MARIE 1.0.0-rc1** with
**lru_cast 0.2.0 (CAST)**, Marie's designated successor, carried as patch
`2102`. The preview keeps Marie because CAST does not apply to the linux-next
base. The base stays at `v7.3`; the series stays at 294 patches and the
package is rebuilt at `pkgrel=7`.

### Changed — MARIE → CAST in the rc package

CAST keeps every Marie mechanism this machine uses — the flat per-PFN 32-bit
state array, SIMD PTE walker, rmap-fed bloom filter, look-around, two-stage
prefetch, `kcompressd` and `clean_min_ratio` — and replaces the eight-
generation ring with a measured, self-tuning LRFU ranking. It adds per-lruvec
reclaim (so `memory.max` is enforced through the active policy) and a runtime
switch at `/sys/kernel/mm/lru_cast/enabled`.

Compatibility decided the split:

| Test | `v7.3` (rc) | `next-20261026` (preview) |
|---|---|---|
| `git apply --check` | pass | fail |
| `patch -p1 -F2 --dry-run` | pass, zero offsets/fuzz | `mm/migrate.c` and `mm/swap.h` hunks fail; `mm/page_io.c` needs fuzz 2 |

The preview cannot take it without hand-porting 324 KB of third-party MM code
across the 7.4 merge window, so it stays on Marie until the author publishes a
7.4-compatible revision.

Kefeng Wang's zswap series (`2191`–`2193`) had been rebased onto Marie's
`zswap_store()` and stopped applying without it. They were regenerated from
the upstream commits (`0bdbe1ccedd9`, `50eb352dcd30`, `81a798cf85e9`) with the
author and trailers intact.

### Swappiness unchanged

`vm.swappiness` stays **1**: under CAST that is its file-first promise (file
down to the clean-file floor, then anon), not the start of the measured split.
That preserves the measured-correct policy for this workload — ~27 GB of
largely-cold page cache against ~2.3 GB of live anonymous memory. `60` would
enable CAST's measured split; that is a user decision.

### Verification

Cumulative audit **294/294** against `v7.3`. Package
`linux-sleepy-rc-7.3.0-7` (22.6 MB) and headers (34.5 MB) built. The extracted
`vmlinux` carries `.BTF` and `.BTF_ids`; `CONFIG_LRU_CAST=y` with no
`CONFIG_LRU_MARIE` symbol, `CONFIG_TCP_CONG_BBR3=y` and the old `tcp_bbr`
absent from `modules.builtin`; the built-in cmdline still has
`amdgpu.dcdebugmask=0x800`. Installed side by side with the preview, both
initramfs images rebuilt, and the systemd-boot default
(`linux-sleepy-next.conf`) unchanged. No reboot was performed.

## [2026.10.26-1-sleepy-next (linux-next `next-20261026`)]: 2026-10-26

Preview bump from `next-20261023` to `next-20261026`, the tag that landed after
the morning sweep's 08:30 UTC refresh. The 1023→1026 delta is 722 non-merge
commits across 320 files and changes **no AMD or DRM target file** —
`drivers/gpu/drm/amd`, `ttm` and `scheduler` are identical between the two
tags. The content is dominated by perf tooling, selftests, platform/x86, net,
md, scsi and time; the target-relevant edits are in `mm/zswap.c`,
`mm/vmscan.c`, `kernel/sched/fair.c` and `drivers/nvme/host/pci.c`.

### Changed — `2101` rebased for the new zswap code

`81c49e3a6848` ("mm/zswap: validate dlen and normalize comp_ret on compression
success") removed the `comp_ret = comp_ret ? comp_ret : -EINVAL;` line that
MARIE's zswap hunk anchored on. The preview copy of `2101` drops that context
line. This is the only preview-only delta. No patch was dropped or skipped; the
series remains 135 patches and audits 135/135 against `next-20261026`. (Later
the same day the rc package removed `2101` altogether in favour of lru_cast —
see the 7.3.0-7 entry.)

### Sweep — no new carries

The second pass of 2026-10-26 found four higher-version postings, all resends
with no functional delta (`1179` v2, `1309` v2, `2056` v4, `2800` v4), and no
revert of carried work. The new on-target material is watch-only: the DC
scanout-position fix (VRR 13-bit truncation, awaiting v2 after review), the DC
logger error-path leak, the harvest-information fix (review open), and the
s2idle dGPU-reset series (inert here: `mem_sleep_default=deep`,
`amdgpu.runpm=0`). The KFD SVM-migration fence series is NAKed upstream. Full
triage in `sleepy-next/PATCH_SOURCES.md`.

### Verification

Cumulative audit **135/135** against `next-20261026`. Package
`linux-sleepy-next-2026.10.26-1` (23.0 MB) and headers (34.9 MB) built. The
extracted `vmlinux` carries `.BTF` and `.BTF_ids`; `CONFIG_LRU_MARIE=y`,
`CONFIG_TCP_CONG_BBR3=y`, and the old `tcp_bbr` absent from
`modules.builtin`. The built-in cmdline matches this package's PKGBUILD
(it deliberately omits the rc-only `amdgpu.dcdebugmask=0x800`). Installed;
initramfs rebuilt; the running kernel remains `2026.10.23-1` until the next
reboot (none was performed).

## [7.3.0-6-sleepy-rc (Linux 7.3)]: 2026-10-26

A patch-only refresh; the base stays at `v7.3`. The series moves from 293 to
294 patches and the package is rebuilt at `pkgrel=6`.

### Added — chipset temperature sensors (`3000`)

`3000` adds the AMD 600-series PCI IDs to `xhci-pci-prom21`
(`29381088ac50`, Stephen Horvath, `Tested-by` from an X670 board with the same
`1022:43f7` DID this B650 board has). The Promontory 21 glue publishes the
auxiliary device that `prom21-xhci.ko` turns into chipset temperature sensors;
the merged 7.2 driver listed only the 800-series IDs.

The IDs alone do nothing while `CONFIG_SENSORS_PROM21_XHCI` is unset, so both
packages now select `-m SENSORS_PROM21_XHCI` in `prepare()`. That also flips
the hidden `USB_XHCI_PCI_PROM21` to `y`, which compiles the glue.

### Verification

Cumulative audit **294/294** against `v7.3`. Package
`linux-sleepy-rc-7.3.0-6` (22 MB) and headers (33 MB) built. The extracted
`vmlinux` carries `.BTF` and `.BTF_ids`; `tcp_bbr3` is built and the old
`tcp_bbr` is not; `prom21-xhci.ko` is in the package and the built-in cmdline
still has `amdgpu.dcdebugmask=0x800`. Installed side by side with the preview
and a rebuilt initramfs. No reboot was performed.

The 2026-10-26 sweep found no functional update to a carried patch. It flagged
`lru_cast` v0.2.0 (Marie's successor) as a user decision, and kept the ATOM
calltable underflow, the single-NAPI io_uring busy-poll change and the TCP MSS
revert on the watch list; the triage is in `sleepy-rc/PATCH_SOURCES.md`.

## [2026.10.23-1-sleepy-next (linux-next `next-20261023`)]: 2026-10-23

Preview bump from `next-20261022` to `next-20261023`, one day of linux-next.
The 167-commit delta is parisc, tpm, smb, ocfs2, stackdepot and one `nvme-pci`
dma-buf change. It changes no AMD target file, so no carried patch was absorbed
or rebased.

### Changed — series moves to 135 patches

Three amd-gfx fixes from Jesse Zhang are added to both packages:

- `1309` — `gfx12: flush the scratch register write in the ring test`
  (`Reviewed-by: Lijo Lazar`). The posted `0xCAFEDEAD` write can lose the race
  with the CP's `0xDEADBEEF`; measured 39/10000 false ring-test failures on
  Navi 48, each escalating recovery to a full GPU reset.
- `1310` — sign extend the addresses `GEM_OP(GET_MAPPING_INFO)` returns.
- `1311` — wait for the `GEM_VA` input fences interruptibly.

The same series' 2/3 is already carried as `9035`. The sweep's rejected and
deferred candidates are in `sleepy-rc/PATCH_SOURCES.md`.

### Verification

Cumulative audit **135/135** against `next-20261023`. Package
`linux-sleepy-next-2026.10.23-1` (22 MB) and headers (34 MB) built. The
extracted `vmlinux` carries `.BTF` and `.BTF_ids`; `tcp_bbr3` is built and the
old `tcp_bbr` is not. Installed with a rebuilt initramfs; the systemd-boot
default entry `linux-sleepy-next.conf` points at it.

## [7.3.0-5-sleepy-rc (Linux 7.3)]: 2026-10-23

A patch-only refresh; the base stays at `v7.3`. The series moves from 290 to
293 patches and the package is rebuilt at `pkgrel=5`.

### Added — `1309`–`1311`

The same three amd-gfx fixes as the preview: the gfx12 ring-test MMIO
read-back (`Reviewed-by: Lijo Lazar`), the `GEM_OP` mapping-address sign
extension, and the interruptible `GEM_VA` fence wait.

### Verification

Cumulative audit **293/293** against `v7.3`. Package
`linux-sleepy-rc-7.3.0-5` (22 MB) and headers (33 MB) built. `.BTF` and
`.BTF_ids` are present; `tcp_bbr3` is built and the old `tcp_bbr` is not. The
built-in cmdline keeps `amdgpu.dcdebugmask=0x800`. Installed side by side with
the preview and a rebuilt initramfs.

## [2026.10.22-1-sleepy-next (linux-next `next-20261022`)]: 2026-10-22

Preview bump from `next-20261021` to `next-20261022`, one day of linux-next.
The 194-commit delta is networking, Hyper-V, RISC-V KVM, `x86/uaccess` and
APIC. It changes no AMD target file, so no carried patch was absorbed or
rebased.

### Changed — series moves to 132 patches

`1098` moves to v3: the CS user-fence BO is accepted only when its preferred
or allowed domain is exactly GTT, and userptrs are detected with
`amdgpu_ttm_tt_is_userptr()`. Christian König reviewed it and asked for a
`Cc: stable` tag in place of the disputed `Fixes:` tag.

### Added — `1308`

`drm/amdgpu: don't wait for the SPM VMID's jobs under the VMID manager lock`
v3 (Jesse Zhang, `Reviewed-by: Christian König`). Preview-only: the snapshot
has the `_spm` VMID rework; `sleepy-rc`'s 7.3 base still uses
`amdgpu_vmid_{alloc,free}_reserved()`, so the bug and the patch do not apply
there.

### Verification

Cumulative audit **132/132** against `next-20261022`. Package
`linux-sleepy-next-2026.10.22-1` (23 MB) and headers (34 MB) built. `vmlinux`
carries `.BTF` and `.BTF_ids`, and the `amdgpu` module carries `.BTF`;
`CONFIG_TCP_CONG_BBR3=y`, `CONFIG_DEFAULT_BBR3=y`, old `CONFIG_TCP_CONG_BBR`
off, `DEBUG_INFO_DWARF5` and `DEBUG_INFO_BTF` on. The built-in cmdline keeps
the preview's deliberate omission of `amdgpu.dcdebugmask=0x800`. Installed
with a rebuilt initramfs; the default systemd-boot entry
`linux-sleepy-next.conf` points at it.

## [7.3.0-4-sleepy-rc (Linux 7.3)]: 2026-10-22

A patch-only refresh; the base stays at `v7.3`. The series moves from 289 to
290 patches and the package is rebuilt at `pkgrel=4`.

### Added — `2322`

`sorttable: parse nm output correctly` (Lorenzo Stoakes, merged
`4719513c0fa2`). Without it, a size-less `nm` entry can be misparsed and
swallow the next symbol once `2305` stops sorting `nm` output, losing function
names.

### Changed — `1098` v3

As above: the rework replaces the v1 special case in
`amdgpu_cs_bo_validate()`.

### Verification

Cumulative audit **290/290** against `v7.3`. Package
`linux-sleepy-rc-7.3.0-4` (22 MB) and headers (33 MB) built and installed.
`vmlinux` carries `.BTF` and `.BTF_ids`; `CONFIG_TCP_CONG_BBR3=y`,
`CONFIG_DEFAULT_BBR3=y`, old `CONFIG_TCP_CONG_BBR` off, `DEBUG_INFO_DWARF5`
and `DEBUG_INFO_BTF` on. The built-in cmdline, including
`amdgpu.dcdebugmask=0x800`, is unchanged. The initramfs was rebuilt for
`7.3.0-4-sleepy-rc`.

## [2026.10.21-1-sleepy-next (linux-next `next-20261021`)]: 2026-10-21

Preview bump from `next-20261019` to `next-20261021`. The snapshot adds 62
non-merge AMD commits and 1066 non-merge commits overall. The reviewed KFD
doorbell-race, GPU-reset BO-free, CWSR-reference and pinned-object-accounting
fixes, and `set VRR_EN for inactive state`, are now **base content**.

### Changed — series reconciled to 131 patches

Dropped as absorbed: `1063`, `1082`, `1083`, `1085`, `1091`, `1092`, `1176`,
`1181`, `1182`, `1233`, `2046`, `2058`, `2803`. Rebased: `0101` (bbr3;
`Makefile` now has `tcp_roccet.o` at the anchor), `2419` (BORE 7.0.0; dropped
the obsolete `update_protect_slice()` hunk because the new base's
`cfs_rq_min_slice()` already uses BORE's `se->slice`), and `1175` (dropped the
`hdmi_automation_enable` hunk; the base replaced the handler with
`debugfs_create_bool`).

### Added — `1307`

`gpu/buddy: do not pass caller list to __alloc_contig_try_harder()`
(`fb26cf4f1df4`, `Reviewed-by: Arunpravin Paneer Selvam`). Preview-only until
the rc copy is rebased over the `v7.3` `drivers/gpu/buddy.c` context.

### Verification

Cumulative audit **131/131** against `next-20261021`. Package
`linux-sleepy-next-2026.10.21-1` (22.9 MB) and headers (35.0 MB) built and
installed. `vmlinux` carries a `.BTF` section; `CONFIG_TCP_CONG_BBR3=y`,
`CONFIG_DEFAULT_BBR3=y`, old `CONFIG_TCP_CONG_BBR` off, `DEBUG_INFO_DWARF5` and
`DEBUG_INFO_BTF` on. The built-in cmdline is unchanged. The initramfs was
rebuilt for `2026.10.21-1-sleepy-next` and the default systemd-boot entry
`linux-sleepy-next.conf` now points at it.

## [7.3.0-3-sleepy-rc (Linux 7.3)]: 2026-10-21

A patch-only refresh; the base stays at `v7.3`. The series moves from 282 to
289 patches and the package is rebuilt at `pkgrel=3`. BTF is present in
`vmlinux` and the modules, `TCP_CONG_BBR3` is on with the old BBR off, and the
built-in cmdline is unchanged.

### Added — ten patches

GPU and KFD: `1099` rejects CS chunks too large for `kvmalloc()` before the
copy, closing a render-node-triggered warning; `1300` restores the
per-process/privileged filter on KFD SMI PROCESS_START/END and VMFAULT events
and matches clients by global TGID; `1301` stops SVM migration from reusing a
VRAM page that a CPU fault still references; `1302` backs off the SVM restore
retry to 128 ms and `1303` downgrades the mmap lock before validating ranges,
so a failing restore no longer starves the process locks; `1304` cancels the
VCN/UVD/VCE/JPEG idle work in each `hw_init()` error path; `1305` and `1306`
give high-priority kernel queues a longer quantum instead of a higher queue
priority, which was starving lower-priority queues on GFX12.

Memory: `2804` keeps `page_vma_mapped_walk()` going past a nonmatching huge PMD
after an unaligned `mremap()`, and `2805` clears the young bit atomically on THP
`MADV_COLD`; both are rc-only because `next-20261019` already contains them.

### Changed — four revisions

`1084` moves to v4 (frees the remaining IBs through `amdgpu_job_free_resources()`
and takes the gang-leader reference before cleanup); `9083` to v4 1/2 (message
only) and `9084` to v4 2/2 (bounds ranges at creation plus a backstop);
`1177` moves from the tracker upload to Melissa Wen's list posting.

### Dropped

`1095` is retired. Its `hw_fini` approach was rejected upstream; `1304`, with
Alex Deucher's `Reviewed-by`, is the replacement he asked for.

`2028`–`2030` (r8169 PHY/firmware error propagation and firmware release) are
retired. Andrew Lunn challenged the fatal-error approach, the author agreed the
TODO is stale and proposed failing `rtl_open()` instead, and no v2 followed;
none of the three is in any upstream tree. The numbers become gaps.

### Not adopted

The `dma-fence` signaled-bit ordering pair is rejected: Christian König
objected that the signaling bit must be visible before the callbacks run.
`memcg` cacheline contention is a performance rework that does not apply here;
the TTM suspend-OOM change is xe-only; the PAT/WB fix needs an SEV guest.

## [2026.10.19-3-sleepy-next (linux-next `next-20261019`)]: 2026-10-21

A patch-only refresh; the snapshot stays at `next-20261019`. The series moves
from 139 to 143 patches: eight added, `1095` and the r8169 trio dropped. The
package is rebuilt at `pkgrel=3`; BTF is present in `vmlinux` and the modules.

### Added

`1099`, `1300`–`1306`, the same carries as `7.3.0-3-sleepy-rc`. `2804` and
`2805` are omitted because the snapshot already contains them.

### Dropped

`1095`, replaced by `1304` as in the rc package.

## [7.3.0-2-sleepy-rc (Linux 7.3)]: 2026-10-20

A patch-only refresh; the base stays at `v7.3`. The series moves from 271 to
282 patches.

### Added — eleven patches

GPU: `1097` re-enables GFXOFF for compute on GFX12 because the MES workaround
that disabled it is no longer needed; `1098` keeps the CS user-fence BO in GTT
so the GART address handed to the GPU is valid. Display: `1180` keeps the
nominal vtotal while VRR is inactive, avoiding the integer-refresh round trip
that can shift the vblank rate; `1181` and `1182` fix `drm_crtc` fence lifetime
and the `::get_driver_name()` race.

Block, I/O and network: `2056` clamps `tcp_wmem_schedule()` to non-negative;
`2057` restores the iterator when a misaligned bio is rejected; `2058` clears a
stale `BLK_MQ_S_INACTIVE` flag when an hctx is reused; `2059` and `2060` add
schedule points to the io_uring completion-freeing loops. Memory: `2803`
publishes the null memcg stock pointer before dropping its reference.

### Changed — three revisions

`1084` moves to v3 (drops the review comments; no code change), `9083` to v3 1/2
(comment cleanup) and `9084` to v3 2/2 (bounds SVM ranges by the smallest GPUVM
limit).

### Not adopted

`1095` stays until Leo Liu's reviewed cancel-idle replacement settles. The CS
SPM VMID patch, the KFD SVM restore pair and the EEVDF idle-group fix are
watched, not carried; the CPPC v6 ordering series does not apply to this base.

## [2026.10.19-2-sleepy-next (linux-next `next-20261019`)]: 2026-10-20

A patch-only refresh; the snapshot stays at `next-20261019` because
`next-20261020` adds no AMD GPU content and would need one drop and two
rebases. The series moves from 129 to 139 patches.

### Added — ten shared patches

`1097`, `1098`, `1180`, `1181`, `1182`, `2056`, `2058`, `2059`, `2060` and
`2803`, the same carries as `7.3.0-2-sleepy-rc`. `2057` is omitted because the
snapshot already contains the block fix.

### Changed

`1084`, `9083` and `9084` move to their v3 postings. CAKE moves v7 → v8:
`2052` becomes cake-only, `fq_codel` keeps its original classify shape, and the
backlog guard moves inline into `2054`.

## [7.3.0-1-sleepy-rc (Linux 7.3 final)]: 2026-10-19

The base moves from `v7.3-rc7` to the 7.3 release (`v7.3`,
`c03c1a14507d`). `pkgrel` resets to 1 and the series moves from 278 to 271
patches.

### Dropped — nine patches the release absorbed

`1086`–`1090` (amdgpu eviction fence, runtime PM, GEM leak, sched entity leak,
drm_exec prelocked object), `2508` (UMIP segment index), `2900`/`2901` (idle
threads sharing `init_fs`) and `9085` (userq BO validation). Each
reverse-applies to `v7.3`; the upstream commits are recorded in
`PATCH_SOURCES.md`.

### Added — four patches

`1092` keeps PRT mappings off the VM update lists; it fixes the NULL
dereference introduced by our `1082`. `1178` adds the missing NULL check in
`dcn401_update_clocks_update_dtb_dto()`. `1179` sets `allow_freesync` before
stream validation. `9089` fixes SVM VRAM accounting after a prefetch. `1093`
fixes the gfxoff debugfs out-of-bounds write: the handler stores a u64 with
`put_user()` but advanced the buffer by 4 bytes. The earlier sweep wrongly
marked it as already upstream; the `0x7` guard it matched belongs to other
gfxoff handlers.

### Changed

`1084` moves to v2: `amdgpu_job_free()` and `_free_cb()` are unified, as
Christian König asked on the v1 review.

The retry-fault series moves from our v1 carry to upstream **v4**: `9011`–`9016`
and `9018`–`9024` are removed and replaced by `9100`–`9110` in a new `91xx`
range. v4 drops the MMIO-ACK design (`9014`, `9021`, `9022`), adds the gmc11
`cam_index` handler, and replaces the `9020` `NOALLOC` hunk. It applies cleanly
after the other 259 patches.

### Dropped after review

`9082` (amdkfd: wait for a GPU reset before freeing a BO) is removed from both
packages. Christian König NAK'd the exact v5 approach as "horribly racy" and
pointed at the misplaced trylock as the root cause. The number is vacated.

### Version check

A content-based sweep over every carried subject found one real update
(`1084` v2). The kbuild v4 and zswap v4 series remain deferred on base
mismatches; the retry-fault v1 → v4 redesign remains approval-gated. The
`9082` NAK is recorded in `PATCH_SOURCES.md` and stays in place pending
explicit approval to remove it.

## [2026.10.19-1-sleepy-next (linux-next `next-20261019`)]: 2026-10-19

The preview moves to the first post-7.3 snapshot. `next-20261019` is cut from
v7.3 final and carries the opening of the 7.4 merge window, including the
`amd-drm-next-7.4-2026-10-08` pull. Instead of leaving the series to skip at
build time, every entry was tested against the new base in both directions and
confirmed with a content probe. The series drops from 275 to 129 patches; all
129 apply in order with no skips.

### Dropped — 153 patches the snapshot absorbed or superseded

Of these, 115 reverse-apply or report `Skipping patch` against the pristine
base, and 38 are superseded by a newer implementation or explicitly absorbed:
the CPPC hardening (`1210`–`1229`), the zswap rework (`2173`–`2196`,
`2700`/`2701`), the kbuild toolchain moves (`2302`–`2312`), the display
FRL/VRR set (`0050`–`0061`, `1136`–`1172`), the retry-fault v4 series
(`9100`–`9108`), the io_uring set, and the nvme copyback/API work (`2018`,
`2048`–`2050`).

### Added — seven ready patches

`1094` (SDMA 7.0 MQD setup without register reads), `1095` (call `hw_fini()`
for IP blocks whose `hw_init()` failed), `1096` (amdkfd SDMA IB processing;
`Reviewed-by`/`Acked-by`, partial port of the v12 hunk) and `2052`–`2055`
(CAKE v7: classifier result, split-GSO iterator, backlog cap, hash before
segmenting).

### Rebased — seven patches for the new base

`1058`, `1070`, `1202`, `2036`, `2037`, `2046` and `9069`. The details and the
full drop list are in `PATCH_SOURCES.md`. Two patches needed compile fixes the
apply audit cannot see: `2419` (BORE) now branches in the snapshot's new
`update_protect_slice()`, and `1202` uses the CPPC performance value directly
because the base removed `AMD_CPPC_EPP_PERFORMANCE`.

A post-build audit restored five patches whose added lines also occur in other
functions of the same file: `0034`, `1018`, `1142`, `9057` and `9071`. Their
intended fixes were still missing from the base, and all five apply; the series
is 129 patches.

### Changed — sched_ext disabled for this snapshot

`CONFIG_SCHED_CLASS_EXT` and `CONFIG_EXT_SUB_SCHED` are off in the preview:
next-20261019's sched_ext tree calls an undefined
`scx_reenq_wait_dispatching()` and uses the pre-rename `dsq->pcpu`. BORE is the
live scheduler and sched_ext is unused; the RC package keeps it enabled.

### Still excluded

The TLB-invalidation group (`1008`, `1012`, `1013`, `1014`, `1017`), `9040` and
`9060`; the reasons are unchanged.

## [2026.10.16-3-sleepy-next (linux-next `next-20261016`)]: 2026-10-19

`pkgrel` 2 -> 3. The snapshot base is unchanged. This rebuild carries the four
2026-10-19 shared additions (`1092`, `1178`, `1179`, `9089`) and the `1084` v2
update. It also keeps the nine patches that `sleepy-rc` dropped at the 7.3
bump: `1086`–`1090` and `9085` are already in the snapshot and skip, `2508`
still applies, and `2900` fails context because `2901` is already present.
`9082` is removed from the preview as well, after Christian König's NAK.
The retry-fault series follows the rc tree to upstream v4 (`9100`–`9110`).
`1093` (gfxoff debugfs out-of-bounds write) is copied as well.

## [2026.10.16-2-sleepy-next (linux-next `next-20261016`)]: 2026-10-18

`pkgrel` 1 -> 2. The snapshot base is unchanged: linux-next published no
weekend tag, so `next-20261016` is still the newest. This rebuild installs the
shared carries added after the 2026.10.16-1 build and the UMIP fix.

### Added — nine shared carries that apply on this base

`1091` (wait for pending page-table updates before `amdgpu_vm_make_compute()`;
the SDMA-clear race that takes a MODE1 reset with VRAM loss on gfx1201),
`1177` (PQ in the FreeSync infopacket for DP HDR), `2047`/`2048` (nvme
passthrough copyback), `2051` (nvme volatile write cache state), the preview's
rebased `2101` (LRU-MARIE 1.0.0-rc1), `2506`/`9086` (SRAT bounds checks) and
`2508` (x86/insn-eval UMIP segment-index spin).

The rest of the 2026-10-17 shared additions are already in the snapshot and
skip (`1090`, `2046`, `2802`, `2901`, `9087`), or their hunk context has
drifted and `prepare()` skips them (`2049`, `2050`, `2900`, `9088`). Full
accounting in `PATCH_SOURCES.md`.

## [7.3.0-rc7-3-sleepy-rc]: 2026-10-18

`pkgrel` 2 -> 3. Series is 278 patches (was 261 in the rc7-2 build). This is
the first release that installs the 16 patches adopted on 2026-10-17 after
that morning's build, plus one merged mainline fix.

### Added — the 2026-10-17 carries

The rc7-2 and 2026.10.16-1 packages installed at 10:55 on 10-17 came from
10:43/10:49 builds; the nine third-pass and seven fourth-pass carries were
added later that day and never reached an installed kernel. They ship here:

- **GPU/VM:** `1090` drm_exec prelocked-object fix; `1091` waits for pending
  page-table updates before switching a VM to CPU updates (closes the
  SDMA-clear race that takes a MODE1 reset with VRAM loss on gfx1201);
  `9087` returns copy errors from `AMDGPU_INFO_UQ_FW_AREAS`; `9088` memset32
  SDMA padding.
- **NVMe:** `2046` reverts the `max_hw_sectors` DMA clamp (up to 15% on large
  transfers); `2047`-`2050` passthrough copyback fixes; `2051` volatile write
  cache state.
- **Memory/VFS:** `2802` submits the last swap-readahead batch before
  unplugging; `2900`/`2901` stop idle threads pinning the initramfs
  superblock (70-150 MB).
- **Hardening and other:** `2506`/`9086` SRAT bounds checks; `1177` PQ in the
  FreeSync infopacket for DP HDR; `2101` LRU-MARIE 1.0.0-rc1.

### Added — `2508`, the UMIP segment-index fix

`32c52ec87d62` x86/insn-eval: a CS-prefixed SGDT/SIDT/SMSW takes the UMIP `#GP`
path and spins in the kernel, with a SIGKILL that is never delivered; FS/GS
overrides write the emulated result to the wrong address. Merged by Linus on
2026-10-16 with Peter Zijlstra's and Borislav Petkov's `Acked-by`. It applies
cleanly to `v7.3-rc7` and to both series trees. `CONFIG_X86_UMIP=y` here.

### Note — the previous artifacts were built but never installed

`PATCH_SOURCES.md`'s fourth-pass "Verification" paragraph describes the 16:49
build correctly, but that build was never installed. The installed kernels
remained the morning ones: the packaged `amdgpu.ko` from 16:49 calls
`dma_fence_wait_timeout` (the `1091` form) while the installed module calls
`amdgpu_bo_sync_wait`. This release supersedes both installed packages.

## [2026.10.16-1-sleepy-next (linux-next `next-20261016`)]: 2026-10-17

### Changed — the preview moves to `next-20261016`

The bump staged on 2026-10-15 and reverted on 2026-10-16 is done. It was worth
taking for one reason: **all of the GPU payload of that week arrived in the
15→16 window** — 172 amdgpu/amdkfd files, the SPM VMID series and the removal of
the legacy CP programming in `gfx_v12_0.c`. Every earlier window in the same run
(`09→12`, `12→13`, `13→14`, `14→15`) carried **zero** amdgpu files. The base also
moves `rc6` → `rc7`, so the two packages finally agree on the base rc.

Cost, measured as the full series applied at its position: **109 applied, 147
skipped, 0 failed** of 256 entries. Three things had to move with it:

- **`2419` (BORE):** the `update_protect_slice()` wrapper hunk added on
  2026-10-12 is obsolete — the scheduler rework in this window made that
  function stop reading `normalized_sysctl_sched_base_slice`. The hunk is
  deleted **in the preview only**; `v7.3-rc7` still needs it, so the two copies
  of `2419` now differ deliberately.
- **`2101` (LRU-MARIE 0.12.0):** rebased onto the snapshot at six host hooks
  (`memcontrol.h`, `mm/Kconfig`, `page_alloc.c`, `page_alloc.h`, `swap.h`,
  `vmscan.c`), including a const-qualification of Marie's zone-size helper to
  match the host accessor's new `const struct lruvec *`.
- **`0101` (bbr3):** regenerated — the `fast_ack_mode` bitfield's anchor moved
  behind a new `#ifdef CONFIG_BPF` block in `struct tcp_sock`.

### Removed — preview-only dead carries, and `9040` from the build list

`1174` (direct-scanout alpha), `9078` and `9079` were preview-only and their
changes are already in `next-20261016`; all three are deleted (numbers vacated).
`9040` is excluded from `source=()` — the snapshot's own
`error_free_user_pages` label supersedes it — but `sleepy-rc` still needs it, so
the file stays part of the shared series.

81 other carries are also fully present in the snapshot, measured for the first
time by reverse-applying the whole series. They stay listed: a skipped patch
contributes nothing to the build, and keeping the shared series intact is what
the preview is for.

### Added — 13 patches

| | |
|---|---|
| `1081` | allow dispatch tunneling on GFX12 — our `gfx_v12_0.c` hard-coded it off |
| `1082`,`1083` | the `amdgpu_vm_bo_insert_map()` pair Christian König asked for on the seq64 thread |
| `1084` | drop the gang-leader fence reference when freeing a gang job (leak on every GFX+COMPUTE gang) |
| `1085` | reject ANONONLY userptrs that span multiple VMAs (restores a check lost in the HMM move) |
| `1175` | `memdup_user_nul` in the display debugfs handlers (out-of-bounds read) |
| `1233` | reapply UMD profile state after GPU recovery |
| `2800` | `mm: memory:` truncation removing mapped folios (a `VM_BUG_ON_FOLIO` on shmem/tmpfs) |
| `2801` | `mm/swap:` recheck the swap-table slot in `swap_cache_get_folio()` |
| `9081` | userq: commit the seq64 BO mapping for userqueue-only clients |
| `9082` | amdkfd: wait for a GPU reset before freeing a BO |
| `9083`,`9084` | amdkfd: bound SVM mappings by the GPU address limits (`Cc: stable`) |

Range `2800–2899` is new: `2100–2199` is exhausted and every gap in it is a
vacated number.

### Changed — LRU-MARIE 0.11.1r2 → 0.12.0, both packages

`2101` is now the **author's own 0.12.0 patch for Linux 7.3-rc7** (Masahito S,
2026-10-12) rather than a repackage of sirlucjan's copy. It needs no hand-rebase
on `sleepy-rc`'s base at all — zero failed hunks, zero fuzz. The preview carries
the same file rebased for its snapshot, as it always has.

## [2026.10.09-1-sleepy-next (linux-next `next-20261009`)]: 2026-10-12

### Changed — the preview is versioned by its snapshot date

No patch changed; only the way the package names itself.

`sleepy-next` was reporting itself as `7.3.0-rc6-1-sleepy-next`, because the
snapshot's `Makefile` composes the release from its own base rc — `next-20261009`
is cut from `v7.3-rc6`. That name was wrong twice over: it was **stale**, since
the tree carries weeks of work past rc6, and it was **easily confused with
`sleepy-rc`**, whose `7.3.0-rc7-1-sleepy-rc` is a genuine mainline rc.

The release is now the **snapshot date**:

| | Before | After |
|---|---|---|
| `pkgver` | `7.3.0_rc6` | `2026.10.09` |
| Package | `linux-sleepy-next-7.3.0_rc6-1` | `linux-sleepy-next-2026.10.09-1` |
| `uname -r` | `7.3.0-rc6-1-sleepy-next` | `2026.10.09-1-sleepy-next` |
| Module dir | `/usr/lib/modules/7.3.0-rc6-1-sleepy-next` | `/usr/lib/modules/2026.10.09-1-sleepy-next` |

### Why the date is dotted

The obvious form — `20261009-1-sleepy-next` — **does not work**, and the first
attempt at this change shipped it and broke the install. Both tools that consume
the release string require it to *begin* with dotted decimal notation:

| Tool | Rule | What broke |
|---|---|---|
| `depmod` (kmod 34.2) | needs an `N.N` prefix | `depmod: ERROR: Bad version passed 20261009-1-sleepy-next`; the post-install hook failed and no module dependencies were generated |
| `mkinitcpio` (42.2) | `kver()` matches `^[[:digit:]]+(\.[[:digit:]]+)+` against the release extracted from the image | `ERROR: invalid kernel specified`; pacman's pre-transaction hook had already deleted the old initramfs, so the kernel was left with **no initramfs at all** |

`2026.10.09` satisfies both. The dots are load-bearing, not decoration.

`prepare()` rewrites `KERNELVERSION` in the snapshot's `Makefile`, and `pkgver`
is derived from `_srctag` — so a bump cannot move the tag without moving the
version, and the two can never drift apart.

Only the release *string* moves. `version.h` derives `LINUX_VERSION_CODE` from
`VERSION`/`PATCHLEVEL`/`SUBLEVEL`, not from `KERNELVERSION`, so those stay
`7`/`3`/`0` and out-of-tree module version checks are unaffected. The build
asserts the rewrite landed and aborts if it did not.

### Fixed — package descriptions

Both packages described themselves as *"Sleepy-next kernel: Linux 7.3-rc4"* —
stale on the version, and wrong about which package it was. `sleepy-rc` now
reads *"Sleepy-rc kernel: Linux 7.3.0-rc7"* and `sleepy-next` reads
*"Sleepy-next kernel: linux-next 20261009 snapshot"*, each derived from its own
variables rather than a hardcoded string.

## [7.3.0-rc7-2-sleepy-rc]: 2026-10-17

`pkgrel` 1 -> 2. Series is 261 patches (was 242).

### Added — 13 patches, and LRU-MARIE 0.11.1r2 -> 0.12.0

Full provenance, review state, and the rejection reasons for everything else the
sweep considered are in `PATCH_SOURCES.md`.

- **GPU core:** `1081` dispatch tunneling on GFX12 (our `gfx_v12_0.c` hard-coded
  `TUNNEL_DISPATCH, 0` while GFX10/11 pass `prop->allow_tunneling`), `1082`/`1083`
  the `amdgpu_vm_bo_insert_map()` pair Christian Koenig asked for on the seq64
  thread, `1084` a gang-leader fence reference leaked on every gang submission,
  `1085` an ANONONLY userptr check lost in the move to HMM.
- **Display:** `1175` `memdup_user_nul` in the debugfs handlers (out-of-bounds
  reads); 1/2 only - 2/2 does not apply to this base.
- **PM:** `1233` reapply the UMD profile state after a GPU recovery.
- **Memory:** `2800` truncation removing mapped folios (`VM_BUG_ON_FOLIO` on
  shmem/tmpfs), `2801` a recheck in `swap_cache_get_folio()` that prevents
  touching a folio that left the swap cache. New range `2800-2899`: `2100-2199`
  is exhausted and every gap in it is a vacated number.
- **KFD/userq:** `9081` commit the seq64 BO mapping for userqueue-only clients,
  `9082` wait for a GPU reset before freeing a BO, `9083`/`9084` bound SVM
  mappings by the GPU address limits.
- **LRU-MARIE 0.11.1r2 -> 0.12.0**, now the author's own patch for `7.3-rc7`
  instead of a repackage - it needs no hand-rebase on this base.
- **Six fixes from the rc8 window**, taken the same day because they are on
  this machine's user-queue and VM paths: `1086` keep the eviction fence
  until the last handle closes, `9085` validate userq BOs (evicted-list
  BOs never got an eviction-fence rearm), `1087` a runtime-PM double-drop
  in the debugfs GPR read, `1088`/`1089` GEM and sched-entity leaks on
  error paths, and `1176` a one-line `median3()` bug in DSC rate control
  (`median3(2,3,1)` returned 3).

### Not carried, with reasons

`01b3f957` (MES 64-bit register reads) applies cleanly but its only consumer is
a GFX12.1 VF path this machine never runs; `e57b299800` needs
`debug_guardpage_minorder`; `ce2f3b80de` needs memory hot-add; `0d5c18f2` lands
in the preview's new snapshot anyway; `34fa31c8` is a GC-12.1 dispatch path. The
v6 KFD wedged-teardown series is deferred, not rejected.

## [7.3.0-rc7-1-sleepy-rc]: 2026-10-12

### Changed — rebased to mainline `v7.3-rc7`

Tag `24a19b953e2a`. The whole series was re-applied to a clean rc7 worktree:
**242 of 245 applied.**

**`245` -> `242` patches. Three carries absorbed upstream**, each user-approved
and each verified **by content** rather than by reverse-apply, which has given
false positives and negatives repeatedly:

| Patch | Landed as |
|---|---|
| `1174` direct-scanout alpha | `amdgpu_dm_plane.c:115` already has the `format->has_alpha` form; the old `alpha_formats[]` table is gone |
| `9078` userq doorbell BO check | all 6 added lines present in `amdgpu_userq.c` |
| `9079` userq `memdup_user()` error | all 3 added lines present in `mes_userqueue.c` |

No CachyOS branch needed regenerating — all `01xx` applied cleanly, and
sirlucjan has nothing newer (repo current at `753c3849ce8d`; its newest `7.3-rc`
material is 2026-09-18).

### Verified

`242` entries, **0 skipped, 0 errors**, `EXIT=0`. `.BTF` and `.BTF_ids` present;
banner `Linux version 7.3.0-rc7-1-sleepy-rc`. `CONFIG_TCP_CONG_BBR3=y`,
`CONFIG_LRU_MARIE=y`, `CONFIG_SCHED_BORE=y`, `CONFIG_DEBUG_INFO_DWARF5=y`, and
`CONFIG_TCP_CONG_BBR` unset as required.

`sleepy-next` is **unchanged** at `next-20261009` — no newer snapshot exists.
The two kernel releases are now `7.3.0-rc7-1-sleepy-rc` and
`7.3.0-rc6-1-sleepy-next`.

## [7.3.0-rc6-1-sleepy-next (linux-next `next-20261009`)]: 2026-10-11

The repository is now **two packages**. `sleepy-next/` became **`sleepy-rc/`** by
`git mv` — same series, same patch numbers, renamed package — and `sleepy-next/`
was recreated as the **linux-next snapshot preview**. Each sets its own
`_pkgsuffix`, which drives both `pkgbase` and the kernel release, so the two
install side by side: distinct module directories, distinct boot artefacts,
distinct pacman packages.

> **Version caveat.** The preview's kernel release is
> `7.3.0-rc6-1-sleepy-next` — byte-identical to the rc6 build's, because
> `localversion.20-pkgname` deliberately strips the snapshot date and
> `_pkgsuffix` no longer carries it. The two are indistinguishable by `uname -r`.
> Not changed this session, deliberately: kernel identity is not worth editing
> untested. Recorded as a recommendation.

### Added — the preview package

| | |
|---|---|
| Base | linux-next `next-20261009`, tag `becb95e45ef0` |
| Tree `Makefile` | `7.3.0-rc6` |
| Package | `linux-sleepy-next-7.3.0_rc6-1` |

`prepare()` **skips** patches that no longer apply rather than failing, so an
unstable base still yields a build. Of **239** `source=()` entries, **99 applied
and 140 were skipped**.

### Excluded from `source=()` — two groups that cannot be carried partially

- **`1008`/`1012`/`1013`/`1014`/`1017`** (amdgpu TLB-invalidation rework).
  `1008`, which declares `tlb_inv_num_dw` and `amdgpu_emit_tlb_inv()`, no longer
  applies, while `1012`/`1013` consume exactly those. A partially applied rework
  does not compile.
- **`9060`** (amdkfd fault-window skip). Upstream already has
  `svm_range_window_resident()` in this snapshot, so the patch applied *and*
  inserted a second definition — `error: redefinition`. This is the trap where a
  clean apply proves nothing: an absorbed carry re-applies rather than failing.

`sleepy-rc` retains all six. `sleepy-next/PATCH_SOURCES.md` records the detail.

### Regenerated — `2419` (BORE) rebased

The snapshot added `update_protect_slice()`, which reads
`normalized_sysctl_sched_base_slice`. BORE wraps the sibling
`set_protect_slice()` in `#ifdef CONFIG_SCHED_BORE` and supplies its own slice,
so under BORE that symbol is never declared. One hunk was added, giving
`update_protect_slice()` the wrapper BORE already uses. Reuses BORE's own idiom
verbatim; no `.rej`, and no `normalized_…` use remains outside an `#else` arm.

### Rebased — `0101` (BBR3) and `2101` (LRU-MARIE) now apply

Both carries originally failed against this base and were skipped, leaving the
preview with no BBR3 and no LRU-MARIE. Both are now rebased and apply with
**zero failed hunks**, so `CONFIG_TCP_CONG_BBR3=y` and `CONFIG_LRU_MARIE=y` are
back. Neither has an upstream version for this base (CachyOS's newest branch is
`7.3`, sirlucjan's newest tree is `7.3-rc`, firelzrd's newest MARIE is the
`v0.11.1r2 for Linux 7.3` we already carry), so both were ported by hand.

The method matters: each patch was rebased against the tree at *its own
position* in `source=()` (`0101` is entry 17, `2101` entry 122), then
regenerated from `git diff`. Working at the end state reports failures that are
not real — later patches touch the same files, and `2033` also edits
`tcp_output.c`.

**BBR3** — six failing hunks were all the same change. Upstream has already
converted the `min_tso_segs` congestion-control callback to `tso_segs`, so five
are dropped. The sixth **applied and added a second `bbr_tso_segs()`** beside
upstream's — the same redefinition trap as `9060` — and is redundant because
`tcp_bbr3.c` is self-contained, carrying its own helper and its own
`"bbr3"` ops. But the `tcp.h` hunk also adds `skb_marked_lost`, which upstream
lacks and which `tcp_input.c` and `tcp_bbr3.c` both require, so that hunk was
rewritten rather than deleted.

**LRU-MARIE** — five failing hunks. Three were pure context drift: `mm/Kconfig`
gained `def_bool y`, `__swap_writepage()` (the `mm/swap.h` anchor) is gone, and
`mem_cgroup_get_zone_lru_size()` was rewritten upstream with a `const` lruvec,
which required `const`-qualifying MARIE's read helper. Two were real merges:
`page_alloc.c` had to combine upstream's new `reclaim_order` parameter *and* its
`reclaim_order == order` term with MARIE's `nr_progress` accounting and its
swap-backend-failure OOM trigger; and `vmscan.c`'s `move_folios_to_lru()` gained
an upstream `do_rotate` tail-add that had to be merged with MARIE's
tracked-vs-orphan axis — clean, because `lru_marie_orphan_add()` already takes a
`@tail` flag.

The `page_alloc.c` refault half could not simply be dropped: an applied hunk
already writes `ac->last_refaults`, so omitting the read side would have left
the counter written and never read — silently disarming MARIE's thrash
detector, which `LESSONS.md` records being wrongly muted once already.

Full detail is in `sleepy-next/PATCH_SOURCES.md`.

### Cmdline

`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is dropped in the preview only, so
the snapshot's display code runs with IPS enabled. `sleepy-rc` keeps it.

### Verified

Built with Clang/ThinLTO as usual. `.BTF` (section 16) and `.BTF_ids`
(section 17) present in the extracted vmlinux. `CONFIG_SCHED_BORE=y`,
`CONFIG_CPU_IDLE_GOV_NAP=y`, `CONFIG_DEBUG_INFO_BTF=y`,
`CONFIG_DEBUG_INFO_DWARF5=y` (not `DWARF_TOOLCHAIN_DEFAULT`), and
`CONFIG_LOCALVERSION=""`.

With the two rebases landed, `CONFIG_TCP_CONG_BBR3=y`, `CONFIG_LRU_MARIE=y` and
`CONFIG_LRU_MARIE_DEFRAG=y`. `CONFIG_TCP_CONG_BBR` stays **not set**: `bbr_tso_segs`
is a `__bpf_kfunc` in both `tcp_bbr.c` and `tcp_bbr3.c`, so building BBR would
collide on the BTF kfunc symbol — the documented BBR/BBR3 rule, unchanged.

### net-tune is owned by `linux-sleepy-rc` only

The two packages install side by side, and pacman has no notion of shared file
ownership, so both shipping `net-tune` is a hard conflict — `/usr/local/bin/net-tune.sh`,
`/etc/net-tune.conf`, both units and both `.wants` symlinks. `sleepy-next` now
builds the service's config but does not install it (`_ship_net_tune=no` in its
PKGBUILD); `linux-sleepy-rc` owns it. Installing the preview alone therefore
leaves net-tune unmanaged until `linux-sleepy-rc` is present.

Also checked against the snapshot, since they were candidates: the HDMI FRL fix
`495606b324cd` is **already upstream** in `next-20261009`
(`amdgpu_dm_connector.c` carries the `link_active` guard, and the commit
reverse-applies cleanly), so it needs no carry.

## [7.3.0-rc6-1-sleepy-next]: 2026-10-05

### Changed — rebased to mainline `v7.3-rc6`

Series rebased from `v7.3-rc5` to `v7.3-rc6` (`4eeccbed21e`, tagged 2026-10-04).
The cumulative audit reports **all 245 patches applying cleanly**.

**`255` -> `245` patches.**

### Removed — ten carries absorbed upstream

Each was confirmed by content, not by subject: the added lines are present in
rc6, and for the amdgpu pair, independently by a named entry in Alex Deucher's
`drm-fixes-7.3` pull of 2026-10-01.

| Patch | Landed as |
|---|---|
| `1074` amdgpu SDMA DCC workaround | agd5f `c1702ed0d64a` |
| `1162` display `dc_state_create_copy()` NULL check | `drm-fixes-7.3` pull |
| `2010` blk-cgroup IRQ state in `blkg_tryget_closest` | upstream |
| `2016` nvme-multipath ANA log bounds | upstream |
| `2041` net GSO recursive ip-in-ip limit | upstream |
| `2046` blk-mq set `RQF_USE_SCHED` | `ab6c756f28c` |
| `2047` blk-mq cached requests for flush ops | upstream |
| `2048` io_uring BPF-loop task context | `a3bdf68feec` |
| `2049` io_uring SQPOLL task-work RCU | upstream — *code identical to rc6, only the comments differ* |
| `2151` mm shmem forced-collapse sysfs | upstream |

### Regenerated — four carries rebased onto rc6

`1007` and `1017` (gmc12 TLB-invalidation rework) needed a one-token context
rebase: the 7.3 fixes pull changed `gmc_v12_0_flush_vm_hub(..., 0)` to
`flush_type`. `2311` (kbuild toolchain checks) was rebuilt because rc6 added a
`CC_OPT_INLINE_MEMSET` block inside the region it rewrites. `2049` was inspected
and found already upstream rather than regenerated.

### Verified

A duplicate audit across the whole series found **no silent duplicates** against
rc6 — no patch applies cleanly while its content is already present. Built with
Clang/ThinLTO as usual; `.BTF` and `.BTF_ids` present in the vmlinux,
`CONFIG_TCP_CONG_BBR` **not set** (so the BBR/BBR3 kfunc collision is avoided),
`CONFIG_TCP_CONG_BBR3=y`, `CONFIG_SCHED_BORE=y`, `CONFIG_LRU_MARIE=y`, and the
baked-in cmdline unchanged.

## [7.3.0-rc5-3-sleepy-next]: 2026-09-30

### Changed — the scheduler is now BORE, not sched-ext

`scx_loader` and `scx_cake` are gone; this kernel runs **BORE**
(Burst-Oriented Response Enhancer). BORE makes the EEVDF task selection in
`kernel/sched/fair.c` burst-aware, favouring tasks that run less bursty.
`scx_loader.service` is disabled and stopped, so `fair.c` is the live
scheduler.

**`257` -> `252` patches.**

### Added

- **`2419` BORE 7.0.0** (Piotr Gorski). Adds `CONFIG_SCHED_BORE` and
  `CONFIG_MIN_BASE_SLICE_NS` (left at its 2000000 default), and two new files
  (`kernel/sched/bore.c`, `include/linux/sched/bore.h`).
- **`2420` `sched/fair: do not scan twice in detach_tasks()`** (Huang Shijie).
  This is a patch an earlier sweep rejected *specifically* because `fair.c` was
  inert under scx full-switch mode. BORE makes it live, and it carries
  `Reviewed-by: Vincent Guittot` and `Reviewed-by: Valentin Schneider`. It
  computes `env.loop_max` under the RQ lock from `cfs.h_nr_queued` instead of
  guessing from `nr_running` without the lock, which could walk the same tasks
  twice.

### Removed — the seven sched_ext carries

`2005`, `2413`-`2418`, all targeting `kernel/sched/ext/`. They are dropped
because the machine no longer runs the subsystem, **not because upstream
superseded them** — this is the first removal of its kind here. If sched-ext is
ever re-enabled, they must come back with it: they fix a NULL sub-sched
dereference raised from NMI and a CPU-hotplug hang.

### Modified — `0110` lost its `fair.c` hunk

BORE and `0110` write the same lines of `fair.c`; the CACHY base-slice block
would land in BORE's dead `#else` branch and never compile. Stripped for exactly
that reason. `0110`'s other seven hunks (`mm/vmscan.c`, `mm/page_alloc.c`,
`bus_lock.c`, ...) remain live, so the patch stays.

### Note for future maintenance

`fair.c` was inert here from the sched-ext era until 2026-09-30 and is now the
**live** scheduler — while `kernel/sched/ext/` is the inert side. **Every
"inert under scx" verdict recorded before that date needs re-reading rather than
trusting.** `2420` is the case where the basis changed and the verdict flipped.

### Verified

- Cumulative audit: all 252 patches apply cleanly to `v7.3-rc5`.
- `CONFIG_SCHED_BORE` confirmed **in the built image**: the decompressed vmlinux
  contains `kernel/sched/bore.c` and the full BORE sysctl set
  (`sched_burst_penalty_scale`, `sched_burst_smoothness`,
  `sched_burst_cache_lifetime`, `sched_burst_protect_slice_lv`,
  `sched_burst_inherit_type`, `sched_burst_penalty_offset`) — checked by
  decompressing rather than by `strings` on the compressed bzImage.

## [7.3.0-rc5-2-sleepy-next]: 2026-09-28

### Updated

- **`2045` -> v4** — `net/sched: sch_cake: prevent shaper corruption and stall
  in cake_overhead()` (Yuchao Zhang). CAKE is this machine's SQM, run by
  `sleepy-next/net-tune/` on the RTL8125B path, so both defects it fixes are
  live here rather than theoretical.

  v4 is a **real code change**, unlike the v3 assessed earlier the same day
  (which was a packaging-only split of the v2 — byte-identical content). Patch 2
  consolidates the three early `return cake_calc_overhead(q, len, off)` fallback
  exits into a single `err:` label at the end of the function, per review from
  **Toke Hoiland-Jorgensen**, the CAKE maintainer, who also adds his
  `Acked-by` to patch 1. That review is what moves this past the adoption bar
  the v2 and v3 did not meet.

  Carried as the single patch `2045` with the combined content of upstream 1/2
  and 2/2; both `Fixes:` tags are preserved in the commit message. The upstream
  split exists for stable backport granularity, which this repo does not use.

  Verified by building the combined patch from a throwaway worktree at
  `v7.3-rc5` (applying 1/2 then 2/2, then `git diff`) and confirming the written
  patch reproduces that tree byte-for-byte, passes `git apply --check` and GNU
  `patch --dry-run` with no fuzz, and that the cumulative audit still reports
  all 257 patches clean.

### Not adopted

A full all-source sweep found nothing else worth carrying. Notable rejections,
recorded in full in `sleepy-next/PATCH_SOURCES.md`: the kbuild build-speedups
**v4** (does not apply to rc5 — built on three unmerged dependency series), the
`r8169` RSS series (**RTL8127**, not this machine's RTL8125B), `zram` short
reads (zram is not in use here), a USB string-descriptor sanitizer (the defect
does not occur on this machine's devices), and `sched/fair` `detach_tasks`
(inert: `switch_all=1`, so CFS load balancing never runs).

### Fixed

- **CHANGELOG ordering** — `[7.3.0-rc4-18]` had been inserted above
  `[7.3.0-rc5-1]` despite being older. Reordered to keep the file newest-first
  as its own header specifies.

257 patches.

## [7.3.0-rc5-1-sleepy-next]: 2026-09-27

### Changed

- **Rebased onto mainline `v7.3-rc5`** (`72d3fcf802c`, cut 2026-09-27).
  `pkgver` `7.3.0_rc4` -> `7.3.0_rc5`; `pkgrel` reset to 1.

### Removed — 11 patches now upstream in rc5 (268 -> 257)

The cumulative audit flagged 11 as `Skipping patch` against the new base. Each
was verified as genuinely present in rc5 before removal:

- `1076`-`1080`, `1174`, `9079`, `9080` — the eight fixes adopted on 2026-09-26
  *from* the rc5 DRM pull, so rc5 necessarily contains them.
- `2040` (net/sched idr error pointers), `2043` (fs `evict_inodes`), `2153`
  (writeback Tasks-RCU) — merged upstream in the rc4→rc5 window.

`9080` and `2043` reverse-applied cleanly to rc5 while being absent from it, and
two others failed the reverse check while being present. Both directions of the
apply check were wrong at least once; every one of the eleven was settled by
probing the identifiers the patch introduces.

### CachyOS branches

No `01xx` regeneration needed: the audit passes unchanged, and sirlucjan's
sources for the branches we carry have zero changed files since 2026-09-18.
Their new commits add an `hdmi-patches-v2` rebundle (already assessed as work we
carry) and a POC scheduler selector (not used here).

257 patches.

## [7.3.0-rc4-18-sleepy-next]: 2026-09-26

### Updated

- **`2032` → v3** — `tcp: preserve timestamps across receive queue collapse`
  (Jason Xing). One line our carried v2 lacked: clear
  `TCP_SKB_CB(nskb)->has_rxtstamp` before the `cb` memcpy, because that memcpy
  inherits the flag from a source skb that may contribute no bytes (a
  fully-covered skb left in the ofo tree). Without it the new skb can advertise
  an RX timestamp it does not have. v3's changelog attributes the corner case
  to **Eric Dumazet**. It scored NEITHER on a plain dry-run — forward fails on
  hunk 2 (carried), reverse fails on hunk 1 (not carried) — which is the
  *partial* signature; verified by reverting to base and applying v3 at that
  series position.

### Version sweep

All 268 carried patches checked against 11 lore mirrors. Ten had a
higher-version posting; **seven were resends** with byte-identical changed
lines, one was **older** than what we carry (`1151`: the "v4" is from February,
ours from September), and one (`2415`) is superseded by our own `2414`+`2415`
pair against the newer `kernel/sched/ext/` layout.

### Not adopted — already carried

`#5870` reports an `amdgpu_sync_add_later` use-after-free on RX 9070 XT, and a
commenter points at Donggeun Yoo's *"don't release the fence reference consumed
by the scheduler"*. The bug is real — `drm_sched_job_add_dependency()` consumes
the reference on every path, so the callers' `dma_fence_put()` on error is a
double put, still present in `next-20260925` — but **we already carry it as
`1064`**, across the same three files.

## [7.3.0-rc4-17-sleepy-next]: 2026-09-26

### Added — the 7.3-rc5 DRM fixes (8)

Sourced from `[git pull] drm fixes for 7.3-rc5` (Dave Airlie, merged as
`6812ce4e4379`). These are fixes for the kernel this machine runs: the base is
rc4, they are the rc5 fixes.

- `1076` amdgpu: vmid_wait fence leak in `amdgpu_ring_init()`
- `1077` amdgpu: last_update fence leak in `amdgpu_vm_init()`
- `1078` amdgpu: runtime PM leak in `amdgpu_debugfs_test_ib_show()`
- `1079` amdgpu: acpi device leak in `amdgpu_acpi_enumerate_xcc()`
- `1080` amdkfd: use-after-free and multi-container gap in `kfd_dev_mapping`
- `1174` display: dc stream excess put in `dm_update_crtc_state()`
- `9079` amdgpu/userq: double jiffies conversion in hang detect timeout
- `9080` amdgpu: move userq fence wait out of signalling section — **rebased**;
  one context line had drifted because our own series changed
  `amdgpu_userq_ensure_ev_fence()` from `void` to `int`

### Added — io_uring SQPOLL UAF (`2049`)

`io_uring/sqpoll: protect task-work publication with RCU` (Jérémy Jean,
`Fixes: af5d68f8892f`). A KASAN-confirmed slab-use-after-free that **is present
in rc4**: `io_uring/tw.c:226` reads `tctx->task` after `mpscq_push()`, and
SQPOLL can consume the request and free `ctx`/`tctx` underneath it. The v2
implements the fix **Jens Axboe prescribed on the list** (a `guard(rcu)()` in
`io_req_normal_work_add()` plus widening the `synchronize_rcu()` in
`io_ring_exit_work()` to include `IORING_SETUP_SQPOLL`) after he rejected the
v1 `get_task_struct()` approach. The two halves only work together.

### Added — SLUB (`2197`)

`mm/slub: refill prefilled sheaves from the barn` (Hao Li, `Reviewed-by:
Vlastimil Babka`). Fixes the barn's full list saturating, which forced every
`kfree_rcu()` sheaf to be flushed to slabs. Only caller is `lib/maple_tree.c`,
so the path is live here; +24.2% on the author's will-it-scale `maple_node`
benchmark. **An optimization without a `Fixes:` tag and not yet through a full
-rc cycle — drop it first if anything unexplained appears.** No other carried
patch touches `mm/slub.c`.

268 patches.

### Rejected, with reasons

- **DML frame-warning-limit family** (`15814c01ac5`, `18779dd8451`,
  `0fd5e9ddf36`) — they exist to stop the DML build *failing* under
  `CONFIG_WERROR`/`CONFIG_UBSAN`. We set neither, and our `dc/dml/Makefile`
  sits at `frame_warn_limit := 2048` against `CONFIG_FRAME_WARN=2048`, so the
  flag is not even emitted. Inert — and it would *remove* a real signal about
  a 2512-byte stack frame.
- **`vcn5.0.1` / `vcn4.0.3` video_timeout unit mismatch** — real bugs (~2 s
  intended wait actually lasting microseconds), but wrong chip: discovery maps
  `IP_VERSION(5,0,0) -> vcn_v5_0_0.c` and the running kernel reports
  `vcn_v5_0_0`. Checked for a latent equivalent rather than stopping at the
  filename: the unconverted pattern exists in exactly two files, neither ours,
  and our `vcn_v5_0_0.c`/`jpeg_v5_0_0.c` have zero occurrences.
- **`next-20260925`** — 1520 commits, all on-target hits are 7.4 `mm/sparse`,
  `mm/damon`, `mm/hugetlb` refactors. `e74db71a3530` (IOMMU PerfOpt) is
  iGPU-only by its own admission (`AMD_IS_APU`); we are a discrete GPU.

### Confirmed

`1074` **is** the v2 SDMA-DCC workaround and remains current: `pepp`'s
2026-09-25 tracker comment links the very patch we carry as the one "going to
be merged soon", after noting the earlier `e = 0` form "doesn't fix it
completely". The issue is a **Navi 4x SDMA hardware bug** on this exact GPU and
the fix is an acknowledged interim workaround.

## [7.3.0-rc4-14-sleepy-next]: 2026-09-24

### Added

Three patches from `[PATCH 00/34] DC Patches September 22th, 2026`, the AMD
display pull request posted to `lore-amdgfx` on 2026-09-24. All three sit on
paths this machine runs; the rest of the batch is DCN60/DCN42/DCN30/DCE and
cannot execute on DCN 4.0.1.

- **`1171` — Serialize HDMI FRL status polling against link detect**
  (`Reviewed-by: Harry Wentland`). `hdmi_frl_status_polling_work()` now takes
  `dm->dc_lock` with `mutex_trylock()` around the whole link walk rather than
  only around `dc_link_detect()`, so the poll can no longer race a link detect
  after an unplug/replug.
- **`1172` — Skip HDMI FRL status polling while link is down**
  (`Reviewed-by: Harry Wentland`). Stops a poll-driven retrain landing on a
  link whose PHY was just torn down — per the mail, that wedges DMCUB and the
  sink's SCDC then reads back version 0, leaving the display dark.
- **`1173` — avoid to write signal specific for tmds**
  (`Reviewed-by: Michael Strauss`). Threads `is_frl` into `write_scdc_data()`
  so a TMDS transition stops writing signal-specific SCDC state, which on some
  panels provokes a spurious HPD.

`1172`'s hunk against `amdgpu_dm_connector_test.c` was dropped — it edits test
additions from the September 16th batch, which is not carried. The code hunk
is unaffected and was verified in series order after `1171`.

258 patches.

### Not adopted, with reasons

- **`24/34` "Fix HDMI2.2 LT timeout duration"** — applies cleanly and rewrites
  the polling loop in `hdmi_frl_perform_link_training()`, the same function as
  our `1136`+`1168`. Rejected: it sets a 200 ms timeout and raises it to 300 ms
  **only at ≥ 16 Gbps**, but this machine's MAG251RX link is FRL6, below that
  threshold — the exact reason `1168` makes the budget unconditional. Taking it
  would cut this link's budget from ~310 ms to 200 ms, less than it had before
  `1136`. Revisit with `1136`/`1168` at the 7.4 bump, not alone.
- **`6f742bc837f1` "Restore FreeSync VCP code check for HDMI/PCON sinks"** —
  its `Fixes:` names the very commit our `1164` reverts, so it looks like a
  swap. It is not: it restores only the `!freesync_vcp_code` half (which our
  unconditional clear already covers), and it has no HF-VSDB VRR guard, so
  adopting it would undo `1163` and re-clear `freesync_capable` for HDMI Forum
  VRR sinks — the change that stopped the rc3 flicker. Recorded as a standing
  divergence.
- **Wrong chip**, verified rather than assumed: `f35aa5c77f5f` (powerplay
  `polaris10`/`vegam` only), `a24db07159cd` and `b2adbdf861e3` (GFX 12.**1**),
  `473b54b63504` (DCN42B), `228200f695c0` (**Zen5** TLB sizes).

### Verified already carried

On-target commits since 2026-09-08 in `agd5f` `drm-next`/`amd-staging-drm-next`
were reverse-tested *and* identifier-probed: `aee05c455ad3` (carried as `1072`,
`bios_size` guards confirmed in `atom.c`), `a2a27745350c`, `5e6b21bce9d9`,
`636139603b99`, `04de4007d323`.

## [7.3.0-rc4-13-sleepy-next]: 2026-09-24

### Added

- **`1075` — drm/amdgpu: don't leak bo_va when `gem_object_open` fails**
  (Xiang Liu). `Reviewed-by: Felix Kuehling`, `Acked-by: Alex Deucher`. A real
  leak in `amdgpu_gem.c` — an unchecked `amdgpu_vm_bo_add` and a missing
  `amdgpu_vm_bo_del` on the error path, reachable because
  `amdgpu_evf_mgr_attach_fence` can fail via `ttm_bo_validate`.
- **`2418` — sched_ext: Place `dsq_vtime` next to `dsq_priq`** (Usama Arif,
  applied by Tejun Heo to `sched_ext/for-7.4`). Puts the two fields rbtree
  insertion touches on one cache line. This machine runs scx full-switch.
  Note it changes `struct sched_ext_entity` layout — out-of-tree scx schedulers
  built against an older `vmlinux.h` need a rebuild; CO-RE consumers do not.

255 patches.

### Not adopted, with reasons

- **ATOM parameter-space bounds pair** — the analysis is sound (external callers
  pass bytes while `atom.c` treats `ps_size` as an element count, so the bound is
  4x too permissive), but there is **no review on either patch**, the author
  posted v2 and v3 within a day, and adopting it would shrink the
  `ATOM_CMD_INIT` window at `atom.c:1669` — a call that passes `16` for a
  **64-byte** buffer, which is inconsistent under the patch's own bytes model.
  This is the VBIOS parser every AMD GPU here depends on. Revisit with review.
- **io_uring CQE32/CQE_MIXED refill** — Jens told the author he had already done
  the work and split it into 7.3 and 7.4 sets. His `io_uring-7.3` head is
  `a3bdf68feecc`, **exactly the commit we carry as `2048`** — so the 7.3 half is
  already ours and the rest is on `for-7.4/io_uring`.

## [7.3.0-rc4-12-sleepy-next]: 2026-09-24

### Changed

- **`1073` replaced by `1074` — the upstream, reviewed version of the same fix.**
  `1073` was adopted from drm/amd work item #5663 with provenance already flagged
  as weak: a GitLab handle with no `Signed-off-by` and a diff that was
  space-indented and truncated, so its hunk body had to be rebuilt by hand.

  The mailing-list pass found the proper `[PATCH v2]` posting: same issue,
  authored by **Pierre-Eric Pelloux-Prayer (AMD)** with
  **`Reviewed-by: Alex Deucher`** and **`Reviewed-by: Christian König`**, and
  `Fixes: 3a6f6eeb3db5`.

  It also fixes it better — device-level (`num_move_entities = 1` for
  `IP_VERSION(7,0,0) || IP_VERSION(7,0,1)`) rather than per-blit, which
  **subsumes** `1073`'s effect, since a single move entity makes the round-robin
  index 0 for every blit rather than only DCC ones. `1073`'s number is left
  vacant rather than reused.

### Fixed

- **`2416` was corrupt and had been built and installed.** My mail decoder,
  Python's `quopri.decodestring`, silently eats one `=` from a bare `==`:
  `quopri.decodestring(b'if (x == y)')` returns `b'if (x = y)'`. Tejun Heo's
  sched_ext hotplug fix therefore shipped as
  `if (p->scx.dsq = &rq->scx.local_dsq)` — an assignment in a condition, always
  true — instead of `==`.

  **Neither the build nor the series audit can catch that**: it compiles without
  `-Werror`, and the audit only proves a patch *applies*. BTF and provenance
  checks are blind to it too. Found by re-decoding every mail-sourced patch
  adopted that day with a safe decoder (expand `=XX` and soft breaks only) and
  diffing the bodies — of six patches, exactly one differed. Then whole-series
  scans for assignment-in-condition (5 hits, 4 benign) and for `=XX` decoding
  artifacts via non-ASCII bytes (23 hits, all author names or em-dashes).

  Fixed, re-audited, rebuilt, reinstalled. `LESSONS.md` and the `patch-sweep`
  skill now carry the safe decoder and the rule.

## [7.3.0-rc4-11-sleepy-next]: 2026-09-24

### Added

- **`2417` — sched_ext: Avoid relocking DSQ during remote DSQ moves**
  (Usama Arif, `Suggested-by`/`Signed-off-by: Tejun Heo`). `move_task_between_dsqs()`
  drops `src_dsq->lock` while `p->scx.dsq` is still set, so the following
  `deactivate_task()` reacquires that lock only to unlink the task and clear the
  pointer. Calling `dispatch_dequeue_locked()` before the unlock takes the
  `!dsq` path and avoids the redundant acquisition. This machine runs sched-ext
  full-switch, so this is live code. One line in `kernel/sched/ext/ext.c`.

  Found in the `next-20260924` delta — the only on-target commit in the day's
  sweep. 252 -> **253**.

### Notes

- The `mm-unstable` zswap series reappeared in `next-20260924` with **different
  shas**: that is linux-next rebasing its branches, not new content.
- `sirlucjan`'s `zstd-dev-patches-v5` is **content-identical** to our `2100`
  (zero changed-line delta, byte-identical), so no update was due.
- Work items `#5036`/`#5035` name "RDNA 4" in the title but their bodies say
  **Navi 44 / RX 9060** — not this machine.

## [7.3.0-rc4-10-sleepy-next]: 2026-09-24

### Added

- **`1169` — drm/amd/display: Fix null deref of link_enc in
  `dce110_enable_tmds_link_output`** (Srinivasan Shanmugam). On-target because
  `dcn401_init.c:97` assigns `.enable_tmds_link_output =
  dce110_enable_tmds_link_output` — that *is* DCN 4.0.1's TMDS/HDMI hook.
  Smatch-reported by Dan Carpenter, `Fixes:` tagged, two `Reviewed-by`s.
- **`1170` — drm/amd/display: Fix LSDMA divide by zero** (Alex Hung).
  `element_size_to_bytes_per_pixel()` in **DML21** returned 0 for element sizes
  above 4, and an unexpected size divides by it. `dcn401_resource.c` sets
  `using_dml21 = true`, so DML21 is this machine's display mode library.

Both came from an **all-branches** sweep of `agd5f-linux` (132 remote refs) —
the tip-only scan showed neither. 250 -> **252**.

### Notes

- `cb546fdd2cd1` (clamp cursor hotspot at the register write) is genuinely
  dcn401 but **fails to apply**: it depends on a cursor refactor chain that is
  not carried, and the bug needs the ODM/MPC slice case two 1080p outputs do
  not reach. Recorded, not taken.
- The `Revert "request DMUB HW cursor offload"` is **DCN42-only** by its own
  rationale, and we do not carry the reverted commit.

## [7.3.0-rc4-9-sleepy-next]: 2026-09-24

### Added

Eight patches adopted after a full multi-source sweep, each verified with a
named author + `Signed-off-by`, symbol existence in the base, and **both**
`git apply --check` and GNU `patch --forward -F2 --dry-run` — and then the whole
series re-verified by cumulative apply in order. 243 -> **250**.

- **`2046` + `2047` — blk-mq `RQF_USE_SCHED`** (Keith Busch). **Kyber is this
  machine's io scheduler**, and `Fixes: 4b6a5d9cea91` is present in rc4, so the
  leaked domain token and stalled queue are live here. Both carry
  `Reviewed-by: Christoph Hellwig` and were applied upstream as `ab6c756f28c7`
  and `9d2c70986bb7`.
- **`2048` — io_uring: initialize task context before the BPF loop** (Yao Kai).
  A NULL deref in `io_submit_sqes()` reachable through `bpf_io_uring_submit_sqes`.
  Applied upstream as `a3bdf68feecc`.
- **`2416` — sched_ext: Fix CPU hotplug hang** (Tejun Heo). Marked
  **`for-7.3-fixes`** with `Cc: stable`; this machine runs scx full-switch.
- **`0104` — sched/core: keep `finish_task_switch()` inline** (Xie Yuanbin,
  CachyOS `fixes` branch). Its premise holds here: `spectre_v2` reads
  *"Enhanced / Automatic IBRS; IBPB: conditional; STIBP: always-on"*, so
  mitigations are on, and this is core code scx does not bypass.
- **`9077` — drm/amdgpu/userq: fix reading the WPTR at a non-zero BO offset**
  (Jesse Zhang) — wrong fence seqno.
- **`1073` — drm/amdgpu: keep GFX12 DCC blits off the SDMA move entity**, from
  drm/amd work item **#5663**, reporter-confirmed on **RX 9070 XT (gfx1201)** to
  fix artifacts after S3 suspend. See the provenance note below.

### Changed

- **`2041` — net: gso: limit recursive IP-in-IP segmentation, updated v4 -> v6**
  (Zihan Xi). A genuine rework: it replaces v4's `GSO_MAX_HEADER` headroom test
  with a per-skb `recursion_counter` in `SKB_GSO_CB`.

### Notes

- **`9078` was adopted and then dropped.** It references
  `amdgpu_userq_input_trap_params_validate()`, which does not exist in rc4 — it
  is written against a newer base. The cumulative audit caught it, along with
  two others that needed rebasing (`2047`, `1073`). Applying to a pristine tree
  is not enough; the series-order test is what finds these.
- **`1073` has weaker provenance than the rest**: its source is a GitLab issue
  note, not a list posting or merged commit, and the author is a handle with no
  real name or `Signed-off-by`. The note's diff is also space-indented where the
  tree uses tabs and is truncated, so the hunk body was rebuilt from the tree
  with the added lines kept verbatim. It forces `e = 0` for `GFX12_DCC` blits
  into VRAM, which is not a no-op here (`num_move_entities` is greater than 1 on
  Navi 48). **Drop it first if blit behaviour or display artifacts regress.**

## [7.3.0-rc4-8-sleepy-next]: 2026-09-23

### Fixed

- **Kernel builds froze the desktop.** On rc4-7 a build window produced **6
  watchdog firings and 114 reclaim-retry firings in ~10 minutes**, with the OOM
  killer repeatedly taking desktop processes (`steamwebhelper`, `electron`),
  and the machine was unusable. This entry originally blamed the build's
  parallelism; **that was wrong** — see below.

  **This entry originally claimed `-j16` was the cause. That was wrong, and it
  was corrected the same day.** Two problems with the attribution:

  1. The measurement was taken on `rc4-7` — the release that had MARIE's
     swappiness clamp *cleared*. That alone produced 192M anon refaults and PSI
     `memory full` at 16%, so the machine was already thrashing before the build
     started. Any job count would have looked catastrophic on top of it.
  2. The three OOM kills originally blamed on build parallelism were in the
     **patch phase** (`prepare()`), before a single `.o` was compiled.
     Compilation parallelism cannot cause a kill there.

  Re-measured against the fixed reclaim policy, at `-j16`, with a watcher that
  would kill the build if `MemAvailable` fell below 2 GB: **minimum 19 GB
  available** on a 30 GB machine, never aborted. Had 16 clang jobs really held
  the 20-25 GB the old note claimed, availability would have fallen near 5 GB.
  That figure most likely counted `buff/cache` growth, which is reclaimable and
  was never memory pressure.

  So `_jobs` is **16**, not 8 — but not because it is faster. Build wall-clock
  is dominated by the serial stages (extract, patch, vmlinux link, BTF,
  kallsyms, packaging), and the measured difference is small:

  | | wall clock |
  |---|---|
  | `-j8` | 6m22s |
  | `-j16` | 6m03s |

  About 20 seconds. The cap is gone because its rationale was refuted, not
  because raising it buys much.

  Note on the diagnosis: the console loglevel here is 3, *below* WARNING(4), so
  the `pr_warn` messages never reached the console. The volume of logging was
  not the problem; the thrash was.

- **MARIE's swappiness clamp is restored, and its thrash watchdog re-armed.**
  `rc4-7` cleared the clamp so the configured `vm.swappiness = 180` would reach
  the reclaim picker. That was backwards: the clamp is what made reclaim
  file-first, which is correct for this workload (~27 GB of largely-cold page
  cache against ~2.3 GB of live desktop working set). Clearing it made MARIE
  reclaim anon almost exclusively — 201M anon steals against 3.5M file, with
  192M anon refaults — and drove PSI `memory full` to 16%, meaning every task
  was stalled on memory a sixth of the time. That was the sluggishness.

  The OOM kills credited to the clamp were MARIE's thrash watchdog correctly
  detecting the livelock the clamp change had *created*. It was briefly
  disabled on the false theory that it was spurious; re-armed and measured
  across a full kernel compile it now reports a refault:steal ratio of **0.303**
  with **0 firings**, against ~0.95 and three kills in three minutes before.

  `vm.swappiness` is now **1**, matching the clamped value, so the sysctl
  reports what the machine actually does. See `swap-stack/README.md`.

### Removed

- **The 7 MGLRU patches (`2131`-`2137`).** They sit behind `lru_gen_enabled()`,
  which LRU-MARIE masks to false while `lru_marie_enabled()` is true, so the
  whole MGLRU aging path is unreachable here. `CONFIG_LRU_GEN=y` and
  `LRU_GEN_ENABLED=y` stay set — MARIE owns reclaim regardless. Verified seven
  ways, including that the functions they change (`folio_update_gen`,
  `folio_inc_gen`, `inc_min_seq`) appear zero times in MARIE's own patch.

- **12 patches for IP blocks this machine never instantiates.** The kernel
  reports `<gmc_v12_0_0>`, `<gfx_v12_0_0>`, `<sdma_v7_0_0>` and DCN 4.0.1 at
  boot, and `lspci` shows a single display device, so gmc_v9/10/11, gfx_v11,
  sdma_v5/6 and dcn42 code cannot run here. Each removed patch is the unused
  sibling of a per-chip series whose ours-chip member stays. Two candidates
  were kept after checking: `1142`/`1143` touch `dce_i2c`, which `dcn401` uses.

  Patch count: **262 -> 243**.

### Added

- **`1168` — `drm/amd/display: Allow 300 ms for HDMI FRL link training at every
  rate`** (David Janice, 2026-09-19). It builds directly on our `1136` — the
  patch's diff context *is* 1136's post-image — and makes the 300 ms budget
  unconditional rather than applying it only above 16 Gbps.

  On-target here for a specific reason: this machine drives the MAG251RX at
  1920x1080@240Hz over HDMI on **FRL6 (~14 Gbps), which is below 1136's
  16 Gbps threshold**, so our link never received the larger budget. Carried
  alongside `1136` also protects it, since both touch the same hunk at
  `link_hdmi_frl.c:528` and a future rebase of 1136 alone would drop it.

  Recorded uncertainty: the reporter's evidence is an LG C2 on a DP-HDMI PCON,
  and no FRL link-training failure has been observed in this machine's logs.
  It is carried because it is a strict widening on the path we use, at a rate
  class our existing fix misses — not because a failure was reproduced here.

## [7.3.0-rc4-7-sleepy-next]: 2026-09-22

### Changed

- **Swap is now zswap in front of a 16 GiB swapfile**, replacing the xswap
  device. The deciding property is that **zswap's drain works automatically**:
  the shrinker calls `zswap_writeback_entry()`, which writes back to the
  entry's *own* swap device, so a real file behind the pool means the pool can
  always be emptied and anonymous pages stay reclaimable. Everything involved
  is upstream — no local patch series.

- **MARIE's swappiness clamp was cleared** so `vm.swappiness = 180` would reach
  the reclaim picker. That was wrong and it was reverted on 2026-09-23 — see
  below. It is kept in this list because it is what the release *did*; it is
  not a recommendation.

### Corrected after release

Two claims in this entry's original revision were wrong. Both are recorded
rather than edited away, because the reversal is the useful part.

**1. Clearing the clamp did not fix anything — it caused the sluggishness.**
The original reasoning: this machine's swap is compressed RAM, so an evicted
anonymous page is cheap (decompress) while an evicted file page costs an NVMe
re-read. Therefore reclaim should be anon-first. That reasoning ignores the
shape of the workload — ~27 GB of page cache against ~2.3 GB of anonymous
memory, where the anon *is* the live desktop working set and the 27 GB is
largely cold.

With the clamp cleared and `vm.swappiness = 180`, MARIE's proportional bias
controller picked anon almost exclusively (an anon reclaim advances the bias
by 180 per page; a file reclaim only -20). Measured over one boot:

| | |
|---|---|
| `pgsteal_anon` | 201,545,880 |
| `pgsteal_file` | 3,537,572 |
| `workingset_refault_anon` | 192,572,097 |
| PSI `memory full avg10` | 16.05 |

57× more anon than file, and 192 million anon refaults — every reclaimed page
faulted straight back. PSI `full` at 16% means *every task* was stalled on
memory a sixth of the time. Restoring the clamp dropped `full` to 0.02 within
60 seconds, with anon reclaim stopping dead (+120 pages).

**2. The OOM kills were the thrash watchdog correctly detecting that thrash.**
The original entry credited the clamp with fixing the kills and treated the
watchdog as a secondary, possibly-spurious factor. The order was the other way
round: the clamp change *created* a real reclaim livelock, and the watchdog
fired because the machine genuinely was thrashing. Its counter is
`WORKINGSET_REFAULT_ANON + WORKINGSET_REFAULT_FILE`, which the 192M anon
refaults drove. Re-arming it and rebuilding measured **0 firings, 0 kills, and
a refault:steal ratio of 0.155** against ~0.95 before. See `LESSONS.md`,
"CORRECTION: the watchdog was right".

`vm.swappiness` is now **1**, matching the clamped value, so the sysctl reports
what the machine actually does.
## [7.3.0-rc4-6-sleepy-next]: 2026-09-22

### Added

Four fixes, all targeting code this machine runs, all verified to apply in
series order against the fully-applied tree.

- **`2045` — CAKE shaper corruption and stall.** CAKE *is* this machine's SQM
  (`net-tune` runs it on the RTL8125B path), and `cake_overhead()` carried three
  real defects: `hdr_len` was `unsigned int`, so a negative transport offset
  wrapped; the `segs == 1` test missed `segs == 0`, underflowing the shaper
  interval; and an unset transport header returned the `~0U` sentinel, inflating
  the computed length to ~66 KB. `sch_cake.c` is otherwise untouched by the
  series, so this is purely additive.
- **`1231` — amd-pstate could be left with no driver at all.**
  `amd_pstate_change_driver_mode()` unregisters the active driver *before*
  registering the requested one, so a failed registration returned the error and
  left the system with **no cpufreq scaling driver** until a mode was manually
  re-selected. It now re-registers the previous mode and still reports the
  original failure.
- **`1232` — silent auto_sel failures.** `amd_pstate_change_mode_without_dvr_change()`
  discarded `cppc_set_auto_sel()`'s return value, so a firmware rejection was
  recorded as a successful transition while the hardware stayed in its previous
  state — software and hardware disagreeing about autonomous selection.
- **`9076` — amdgpu IP discovery table validation.** Missing `&& table_size` /
  `&& size` guards in `check_table`, `get_mall_info` and `get_vcn_info` —
  the tables Navi 48 walks to enumerate every IP block. Carries
  `Reviewed-by: Frank Min` and `Signed-off-by: Alex Deucher`.

### Verified

- Cumulative audit after all four: **275/275 clean, exit 0**. Each passes both
  `git apply --check` and `patch -p1 --dry-run -N` against pristine `v7.3-rc4`,
  and each applies cleanly **in series order** — the check that caught the
  earlier `1231` redundancy.
- Evaluated and not carried: two io_uring fixes (unreviewed, or with a
  reviewer-requested change pending) and a `page_alloc` reserve pair still under
  active review.

`pkgrel` 5 -> 6. Series is 275 patches.

## [7.3.0-rc4-5-sleepy-next]: 2026-09-22

### Changed

- **`2041` (net GSO IP-in-IP) swapped from our v2 to upstream's v4** — and it is
  a strict simplification. v2 drove the limit through a `gso_header_len_add()`
  helper plus a `skb_gso_segment_cb()` wrapper with checks at ~14 call sites
  (10 files, 83 added lines). v4 replaces all of it with
  `#define GSO_MAX_HEADER 256` and a `gso_header_len_exceeded()` inline checked
  only at the two IP GSO entry points — **3 files, 15 added lines**. Same fix,
  far less surface. Verified: both mandated checks pass against pristine rc4,
  the cumulative audit is 271/271 clean after the swap, and the old helper API
  appears **zero** times in the resulting tree.
  The earlier deferral of this patch to the 7.4 bump was based on v3, which
  predated rc4; v4 is written against rc4 and applies directly.

### Verified

- Full-source sweep for 2026-09-22: every kernel tree, all lore mailing-list
  mirrors, the drm/amd work-items tracker (all 49 issues updated since 09-20),
  and every carried patch against its latest revision. **`2041` was the only
  carried patch with a genuinely newer revision.**
- **Nothing else was carried, and several candidates were rejected on
  evidence:** the six `sched/cache` fixes on `tip`'s `sched/urgent` are inert
  here (single L3 domain disables the static branch; `CONFIG_NUMA` is off so the
  `exit.c` path is an empty stub; sched-ext full-switch means `fair.c` balancing
  never runs); a blk-mq **kyber token-leak** fix and an io_uring NULL-deref fix
  both have reviewer-requested revisions pending; an amd-pstate TOCTOU fix was
  admitted and then **removed again** because our own `1227` already makes the
  same fix — caught by the cumulative audit, not by the standalone checks.
- Confirmed the sched-ext hashtable-comparison patches recommended on 09-21 are
  **now merged upstream**, so they are not carried and will arrive by
  themselves; our CPPC series is landing likewise.

### Known for the next bump

- Upstream renames `__swap_writepage()` → `__swap_writeout()`; **three carried
  patches use the old name** (`2199`, `2155`, `2101`) and will need it applied.
- r8169 will **enable EEE by default** at probe. This machine deliberately
  disables EEE (toggling it restarts auto-negotiation and drops the link ~3 s,
  which broke DNS ~11 s after login), so our `net-tune-eee.service` needs a
  measurement then.
- `1056`/`1060` are already upstream and belong on the 7.4 drop list alongside
  `2005`/`2413`/`2414`/`2415`.

`pkgrel` 4 -> 5. Series is 271 patches.

## [7.3.0-rc4-4-sleepy-next]: 2026-09-21

### Removed

- **`1027` (`force complete the MES scheduler ring fence on reset`) — the second
  dead carry, and a different kind from `9007`.** Here the added code was *not*
  in rc4 verbatim; instead rc4 carries a **superseding** implementation. Its
  `AMDGPU_MAX_MES_INST_PIPES` loop realigns the polling fence on **every** MES
  instance pipe (one per XCC), plus an equivalent KIQ loop. Our patch realigned
  only `mes.ring[0]`, so it was redundant work on top of a loop that already
  covered that ring. `mes.ring[0]` read **0** in rc4 and **3** in our tree.
  Five checks were run before removal — standalone failure, cumulative apply,
  superseding code present, count comparison, and function preserved after
  removal — all passed.

### Verified

- A systematic sweep for the first kind (`9007`'s: a patch whose added code is
  already in rc4 verbatim) found **five candidates, all cleared**. Three
  (`1136`, `2033`, `2307`) apply cleanly to pristine rc4, so their content is
  *not* in rc4; `1219` fails only because its series predecessor `1218` also
  fails, which is series dependency rather than duplication. **No further
  literal duplicates remain.**
- The detector used for that sweep was validated against the known positive
  (reconstructed `9007`) rather than trusted blind — an earlier version failed
  to find it and was discarded.

`pkgrel` 3 -> 4. Series is 271 patches.

## [7.3.0-rc4-3-sleepy-next]: 2026-09-21

### Removed

- **`9007` (`drm/gfx12: Program DB_RING_CONTROL`) — a carry that was installing
  a duplicate.** The `v7.3-rc4` rebase absorbed this change upstream, so the
  patch was no longer doing anything. It did not fail, though: its hunk context
  is the lines *before* the block, which rc4 still has, so `git apply` found a
  valid anchor and inserted a **second** byte-identical copy. The series tree
  programmed `DB_RING_CONTROL` twice (`gfx_v12_0.c:1836-1844` and `1851-1859`),
  against once in rc4. This is the one failure mode the cumulative audit cannot
  see — it reports `ok`, because it measures whether a hunk lands, not whether
  the change is wanted.
- **`0112` (`cachy: avoid evicting resources at S5`) — reverted by CachyOS, and
  redundant.** CachyOS reverted its own change (`bd3b950c5b0f`, 2026-08-17,
  reverting the whole `7.2/s5-power` branch merge), and the revert removes
  exactly our four-line hunk. This one was checked carefully before removal
  because, unlike `9007`, it changes behaviour: neither rc4 **nor upstream
  `linux-next`** carries a `SYSTEM_HALT` term here — both have only the
  `SYSTEM_POWER_OFF` early return — so our patch added a case upstream
  deliberately does not have.

### Verified

- Cumulative audit after both removals: **272/272 apply cleanly, exit 0**, no
  skips, reversals or fuzz. The verification suite's fast tier passes.
- `DB_RING_CONTROL` now appears **once** in the series tree (it read twice
  before), and `SYSTEM_HALT` is absent from `amdgpu_device.c`.

`pkgrel` 2 -> 3. Series is 272 patches.

## [7.3.0-rc4-2-sleepy-next]: 2026-09-21

### Removed

- **`1140` (`clamp force_min_dcfclk to dcn42b range`) — inert on this
  hardware.** It patched a single file, `dc/clk_mgr/dcn42b/dcn42b_clk_mgr.c`,
  and the series is gated on `ctx->dce_version == DCN_VERSION_4_2B`
  (`clk_mgr.c:343`, `:454`). This machine reports **DCN 4.0.1**. The Makefile
  compiles the file unconditionally, so it built — it never ran. It was also
  already merged upstream, making it doubly redundant.

`pkgrel` 1 -> 2. Series is 274 patches.

## [7.3.0-rc4-1-sleepy-next]: 2026-09-21

### Changed

- **Rebased the series onto `v7.3-rc4`** (was `v7.3-rc3`). The rc3..rc4 window is
  1038 commits (916 non-merge), and **39 carried patches were absorbed
  upstream** and dropped — every one a merged commit rather than a rejection.
  See `PATCH_SOURCES.md` for the full list and for the three (`1159`, `2408`,
  `2503`) that failed a strict reverse-check while being genuinely upstream.
- **`2101` (LRU-MARIE)** needed one real rebase: rc4 added
  `#include <linux/kvm_types.h>` to `mm/folio.c`, so the include hunk lost its
  context and was regenerated.
- **`2032` (TCP timestamp preservation)** replaced with the upstream v2.

### Fixed

- **The display "box" fix is in this base.** `63e19ef3ddab` ("Atomize IRQ
  register read/modify/write ops", Leo Li) closes the `VUPDATE_NO_LOCK`
  read-modify-write race. AMD's Mario Limonciello directs users to that exact
  commit for RX 9070 XT pageflip-timeout reports in drm/amd `#5872`, `#5843`
  and `#5846`. We had carried it as `1159`; rc4 absorbed it, so it is now
  native to the base.

`pkgrel` resets to 1. Series is 275 patches.

## [7.3.0-rc3-26-sleepy-next]: 2026-09-20

### Fixed

- **A NULL-mempool panic in the swap-out path that killed `kswapd0` and
  `kcompressd0`.** `do_swapout()`, added by the LRU-MARIE patch (`2101`), calls
  `__swap_writepage()` directly. The `SWP_XSWAP` guard that keeps an xswap folio
  in memory lives in `swap_writeout()`, one level above, so that path walked
  around it. It matters because an xswap device is created through
  `/sys/kernel/mm/xswap/create` rather than `swapon()`, so `setup_swap_extents()`
  never runs and `sio_pool` — whose only initialiser lives there — is never
  allocated. On a machine whose only swap is xswap, `swap_add_folio()` then
  reached `mempool_alloc(NULL, GFP_NOIO)`. `2101` applies before `2155`, so
  neither patch's author could see the other's entry point.
  Carried as `2199`; see `PATCH_SOURCES.md` for the full analysis and for why
  the guard belongs at the shared choke point in the long run.

### Verified

- Upstream has **not** fixed this, checked the same day. The newest xswap
  posting (v3, 2026-09-16) is byte-identical to the carried v2 in every affected
  file. A new RFC (patchwork series `1169641`, 2026-09-20) does touch the same
  guard and its commit message describes the identical condition, but it is a
  feature adding a physical backend for xswap, not a fix.

`pkgrel` 25 -> 26. Series is 314 patches.

## [7.3.0-rc3-25-sleepy-next]: 2026-09-20

### Changed

- Replace the ACPI CPPC series with **v7** (`1210`-`1229`, 20 patches; was
  `1210`-`1224`, 15). This is live code — `amd-pstate` is built on ACPI CPPC and
  this machine is Zen 4 with CPPC. Beyond the renumber, v7 changes real content
  in patches 4-14 and adds six: Performance Limited clearing on NVIDIA T41,
  FFH register-field validation before hardware access, cross-CPU FFH error
  propagation, immutable autonomous selection requests, per-CPU
  frequency-invariance callback selection, and FIE worker creation before PCC
  callbacks are published. Verified by substitution: all 14 v6 patches reverse
  cleanly, all 20 v7 patches apply, and no later patch is disturbed.
- Replace `2005` with its **v2**.
- `pkgrel` 23 -> 25. Series is 313 patches; the cumulative audit applies all of
  them to `v7.3-rc3`.

### Removed

- `1213` `ACPI: CPPC: Use 64-bit masks for register fields`, dropped by the
  series author between v6 and v7. The v7 cover letter gives the reason: *"All
  supported CPPC configurations are already 64-bit, so this is only a cleanup
  I'll submit later on."* Its removal was approved before this update.

### Added

- `1071` — `drm/amdgpu: More compact VCN IB emission` (Tvrtko Ursulin,
  2026-09-18). Part of the same 18-patch series `1070` came from, and on-target:
  this machine enumerates `vcn_v5_0_0` and the patch touches the shared
  `amdgpu_vcn.c`. Unlike `1070` it needs no adaptation and applies cleanly to
  both pristine `v7.3-rc3` and the series-applied tree.
- `1230` — `cpufreq/amd-pstate: Skip auto_sel write when it already matches the
  mode` v3 (Wentao Guan, 2026-09-18). Avoids a redundant firmware write on a
  driver this machine depends on.
- `1072` — `drm/amdgpu/atom: bound the VBIOS date, part number, version and build
  getters` (Hari Mishal, 2026-09-15; `Signed-off-by` also from Alex Deucher).
  Closes four out-of-bounds reads in VBIOS string parsing: a 14-byte read at a
  fixed offset that `check_atom_bios()`'s 0x49 minimum does not cover, an
  unchecked image-supplied string offset, a fixed 18-byte advance whose copy had
  no image bound, and a config-string walk from an image-supplied offset. All
  four are now checked against `ctx->bios_size`. This is the VBIOS of the GPU in
  this machine, parsed at every driver load. Found by sweeping amd-staging
  *branches* rather than tips.

### Verified

- A version sweep over all 305 carried patches against 13 lore mirrors found 46
  higher-version postings. Three were adopted. The rest were rejected on
  evidence: three are written against a base newer than `v7.3-rc3` and apply in
  neither direction (`2041` v3, `2415` v3, `2158` v3 — their deltas adapt to
  post-rc3 API changes), three already match by content despite a higher version
  label (`2144`, `2168`, `2185`), three are already-merged upstream commits whose
  higher mailing-list versions are draft history (`2141`, `2412`, `2506`), and
  one is simply older than what is carried (`1151`).
- `1070` was checked against its parent series and is already the correct
  adaptation: the series' hunk 4 expects a `burst_nop` hoist this base lacks,
  which `1070`'s own commit message documents.

### Not carried

- The io_uring `[SECURITY]` posts of 2026-09-16 are vulnerability **reports**,
  not patches — the mails carry no diff bodies and the maintainer has replied.
- `2ac2fe765` "fix MALL hysteresis timer underflow at high refresh rates"
  patches `dcn30_apply_idle_power_optimizations()`; DCN 4.0.1 has its own
  `dcn401_apply_idle_power_optimizations()`, so the patched code never executes
  here. `9413959fa` "report energy accumulator for smu 14.0.3" patches
  `smu_v14_0_2_ppt.c`; this machine enumerates `smu_v14_0_0`. Both were rejected
  on the hardware's own IP discovery rather than on inference.

## [7.3.0-rc3-23-sleepy-next]: 2026-09-18

### Changed

- Replace `2100` with sirlucjan's zstd **v5** (`zstd-dev-patches-v5`,
  2026-09-18; ours was the 2026-09-14 revision). The delta is 14 added and 7
  removed lines: a tightened `longOffsets` assertion, and FSE state updates in
  `zstd_decompress_block.c` that pass `DInfo` directly instead of copying
  `nextState`/`nbBits` into locals. zstd is this machine's zswap compressor.
  The file name is unchanged, so this is a byte-level replacement rather than a
  renumber. Verified by substitution against the series tree, including the four
  zstd dependents that follow it, and again by the full build: 305 patches
  applied, zero skipped.

### Added

- `2045` — `tcp: Don't call skb_clone_and_charge_r() for close()d listener in
  tcp_v6_do_rcv()` (Kuniyuki Iwashima, 2026-09-14). The IPv6 receive path
  charged an skb to a listener that had already closed.
- `2198` — `mm: filemap: move lruvec accounting outside the xarray lock` (Usama
  Arif, 2026-09-16). Moves `NR_FILE_PAGES`/`NR_FILE_THPS` accounting past
  `xas_unlock_irq()`, shortening the xarray critical section on the page-cache
  add path. Taken from `akpm-mm` `mm-everything` and absent from linux-next, so
  a version bump would not bring it.

`2045` sits in the `v7.3-rc3`..`master` window that drains into rc4, so carrying
it shortens the wait rather than adding anything rc4 will not have. `2198` is
not in that window and is the only part of this release that a bump would not
reproduce.

### Fixed

- Correct the duplicate test used during sweeps. Comparing an upstream commit
  subject against the carried patches reported `1587d3394`, `e14a34548`,
  `93d88ac4a` and `9a0b159ff` as absent; all four are carried (`2507`, `2146`,
  `2405`, `2410`) under shortened subjects. Reverse-applicability against the
  series-applied tree is the authoritative test.

## [7.3.0-rc3-22-sleepy-next]: 2026-09-18

### Changed

- Replace the kbuild build-speedup series with **v3** (`2302`-`2321`, 20 patches;
  was `2302`-`2322`). Verified by substitution: all 21 carried patches reverse
  cleanly, all 20 v3 patches apply, zero rejects, and no later patch touches any
  of the 49 files v3 modifies.
- Export `KRUSTFLAGS="-Zthreads=8"`. v3 drops the rustc front-end threading
  patch; its cover letter states the flag restores the same behaviour. This
  build has `CONFIG_RUST=y`, so the flag preserves the parallelism the dropped
  patch provided.
- Adopt v3's other fixes: the relocation hash is dropped in favour of building
  one section at a time incrementally with a linear-scan fallback;
  parallelisation is limited to the `--link` step; pigz uses the make job server
  through a new `KPGZIP` variable; `modules_prepare` no longer duplicates a
  `rust/` build; and `.module-common.o` is built only by the top-level make.
- Replace the ACPI CPPC series with **v6** (`1210`-`1224`, 15 patches). Ours were
  v5, three days older. This is live code: `amd-pstate` is built on ACPI CPPC.
- Replace `2041` (net GSO recursion limit) with its **v2**, posted four days
  after the v1 carried.
- Replace `2147` (memcg clear folio memcg) with its **v5**; ours was four
  revisions behind.

- Add `1070`, a locally adapted **SDMA 7.0 compact IB emission** patch from
  Tvrtko Ursulin's `[PATCH 17/18]` (2026-09-18). It replaces repeated
  `ib->ptr[ib->length_dw++]` stores with a register pointer written back once,
  and skips the padding loop when `pad_count` is zero. Only `17/18` of that
  series targets Navi 48; the rest are GFX8/9, SI, CIK, UVD, VCE and SDMA 2.4-6.0.
- Adapt hunk 4 rather than reject it. It is written against a tree carrying a
  prerequisite refactor this base lacks — it expects
  `const bool burst_nop = sdma->burst_nop;` hoisted out of the loop and the
  `sdma &&` NULL check dropped. The port applies that hunk's delta (the early
  `return`, the register pointer, the single `ib->length_dw += pad_count`) to the
  rc3 form of `sdma_v7_0_ring_pad_ib()` and changes nothing else. The diff body
  was regenerated with `git diff`; the only textual difference from the original
  is one spacing fix, `*ptr++=` to `*ptr++ =`, matching the sibling branch in the
  same hunk. Verification: applies cleanly to clean v7.3-rc3 under both
  `git apply --check` and GNU `patch -p1 --forward -F2 --dry-run`, and the
  cumulative audit applies all 303 patches.

### Fixed

- **Re-clone `repos/torvalds` and `repos/drm-next`.** Both were corrupt — 394 and
  144 filesystem-check issues, and neither could fetch. `torvalds` now reaches
  2026-09-18. Any GPU or mainline negative result recorded before this re-clone
  was less trustworthy than it read.

### Changed
- `pkgrel` 20 -> 22. Series is 303 patches.

## [7.3.0-rc3-20-sleepy-next]: 2026-09-16

### Changed

- Replace the xswap series with the current upstream revision. The 12-patch
  `v2/12` posting (`2155`-`2166`) is superseded by the 14-patch
  `xswap-patches-v2-sep`, carried as `2155`-`2168`. The `2167`-`2195` block
  moves to `2169`-`2197` so the series keeps its position in `source=()`; the
  119 later patches were verified against that position. All 14 patches apply,
  and all 119 subsequent patches apply on top.
- Add `2166`, which caps xswap growth at `nr_clusters`, and `2168`, which
  shrinks the device to the ceiling when the ceiling drops. Together they make
  `type<N>/limit` a hard cap; the previous revision read it only in the
  shrinker, so a limit below current usage caused unmap-and-remap churn.
- Revise the remaining carried patches. `2158` replaces `READ_ONCE()` with
  `smp_load_acquire()` and `smp_store_release()` in the cluster grow/unmap
  protocol. `2167` makes `si->pages` mutable at runtime and adds kobject
  add/del helpers.
- Mark the swap-stack runtime verification `NOT YET RE-VERIFIED`. The 4.4x
  forced swap cycle, the 262,144-page round trip and the five-cycle leak check
  measured the superseded revision. Re-run them on a kernel carrying v2.

### Fixed

- Correct the nvme `genctr` sha in `PATCH_SOURCES.md`. The entry recorded
  `7f607455c3b9`, which resolves in `torvalds` to a 2010 OMAP merge commit.

### Rejected

- BBR3: no newer revision exists. `bbr3-cachyos-patches` and its `-sep` variant
  date to 2026-08-31, and the newest CachyOS commits that touch `tcp_bbr3.c`
  are `7235d70addc6` (2026-06-27) and `af253e921d6f` (2026-04-27). Carried
  `0101` has provenance `55d248b79ea6` (2026-09-02).

### Known issues

- BBR3 needs a rebase for the 7.4 bump. `cb145191e9d3` replaces
  `min_tso_segs()` with a `tso_segs()` CC callback, which rewrites
  `include/net/tcp.h`, `tcp_output.c` and `bpf_tcp_ca.c`. Every BBR3 variant in
  the tree still references `min_tso_segs`, so none is adapted.
- `8a3c76523e44` (r8169 phylink conversion) is not inert. It rewrites shared
  PHY/EEE plumbing and touches `rtl_is_8125()` and `RTL_GIGA_MAC_VER_61/63/70/80`.

### Changed
- `pkgrel` 19 -> 20. Series is now 303 patches.

## [7.3.0-rc3-19-sleepy-next]: 2026-09-16

Add 59 patches (242 -> 301) from a five-lane sweep: mailing lists, the drm/amd
work-items tracker, the `v7.3-rc3..origin/master` window, the repos merged into
linux-next, and the distro patchsets. Each patch is verified with
`patch -p1 --forward --dry-run -F2` against a worktree carrying the full series.

### Added

- GPU (`1065`-`1069`, `1167`): reserve the amdgpu eviction-fence slot at the
  WPTR caller, which stops a `BUG_ON` in `amdgpu_userq_restore_worker()`, and
  its root-PD companion; skip the KFD mapping clear before init (NULL deref on
  reset, Cc stable); report GPU PCIe link capability; unmap rmmio on device
  removal; restore the native-cursor early return for disabled CRTCs.
- Memory and swap (`2181`-`2197`): `cead15891dad`, which is patch 4/4 of the
  series carried as `2167`-`2169`; a `#DE` divide error in
  `effective_protection()` (Cc stable); an off-by-one out-of-bounds read in the
  swap-cache replace check; the stuck `FLUSHING_CACHED_CHARGE` bit (Cc stable);
  `setup_swap_clusters_info()` ordering, which affects xswap device creation;
  the three-patch `zswap_invalidate()` range conversion, which replaces a
  per-slot loop of up to 512 iterations on PMD folios; `mm->locked_vm`
  accounting for `MREMAP_DONTUNMAP`; root memcg charging from
  `obj_cgroup_charge_pages()`.
- Block, I/O, network and filesystems (`2014`-`2044`): the ten-patch io_uring
  ring-close cancel series and the io-wq exit-bit ordering (Cc stable); blk-mq
  cached passthrough state; nvme `genctr` and ANA underflow; the r8169
  error-propagation trio; seven TCP fixes; three net/sched fixes; GSO recursion
  and `pskb_carve()` header staleness; `lib/group_cpus` cluster-mask
  snapshotting (Cc stable), which affects the managed-IRQ affinity spread for
  multi-queue NVMe.
- Scheduler (`2412`-`2415`): the cgroup dying-task use-after-free (Cc stable)
  and the sched-ext NMI trio.
- Time (`2603`-`2605`): the sysctl ms-to-jiffies range and truncation fixes,
  which cover ARP/neighbour, route-gc and IPv6 timers.

### Rejected

- Already carried: `6cc27d821963` and `e14a34548064` are `2145`/`2146`;
  `848d2ce2fce1` is `2141`; `63a68656e48b` and `656581d1d349` are
  `2169`/`2170`; `6795913f` is `1159`.
- Inert by configuration: `5a5d26f2cfe1` (CFI FineIBT; `CONFIG_CFI_CLANG`
  unset), `f65d38155aef` (div64; compile-only constraint fix),
  `7891fbb9512f` (`CONFIG_KVM` unset), `932cfb25e7ce` (no
  `cgroup.memory=nokmem`), `e384abeb559d` (`huge_pfnmap` absent from rc3),
  `228200f695c0` (Zen 5).
- Does not apply: the mm/truncate data-loss series (`aa226fc0` is 2/3),
  `48b0789dec0a`, `c93496f5133e`, and the amd-pstate EPP trio (`1201`/`1202`
  rework the same code).
- Out of scope: the rc4 window is 32 SUNRPC/NFS commits under `net/`, 28 RDMA
  commits under `drivers/`, and 127 nfsd plus 10 lockd commits under `fs/`.
- Needs the whole stack: the pixelcluster amdgpu set, which collides with
  `1058`/`1061`/`9055`.

### Fixed

- `2176` is vacated. `848d2ce2fce1` was reported absent from the base
  but was already carried as `2141`; it was staged as `2176`, then skipped by
  the build. The number is not reused, matching the gaps at
  `2401`/`2402`/`2501`.
- `2401`, `2402`, `2501` and `2600` are indexed in
  `PATCH_SOURCES.md` but are absent from `source=()` and from disk. The sysctl
  trio is numbered `2603`-`2605` to avoid the `2600` collision.
- Carried patch `2155` applies with fuzz. Its `mm/zswap.c` hunk
  expects `return -ENOENT`, but the base has `return -EEXIST`, which is why
  `c93496f5133e` cannot apply.

### Changed
- `pkgrel` 18 -> 19. Series is now 301 patches.

## [7.3.0-rc3-18-sleepy-next]: 2026-09-16

### Added

- Add `2405`-`2411`, the `sched_ext-for-7.3-rc3-fixes` pull (`9b87fdc9af2f`,
  Tejun Heo). These are live on this machine because `scx_loader` runs
  `cake_1.2.1`; the `fair.c` items in `2400`-`2402` are inert under it. The pull
  fixes a use-after-free, where an error raised before the scheduler finished
  enabling was consumed by the disable path's pre-enable shortcut and left a
  running scheduler that could not be disabled, and a NULL scheduler
  dereference in two compat kfuncs (`2407`).
- Add `2171`-`2175` and `2177`-`2180`, all `Fixes:`-tagged and absent from the
  base:
  - `2171` publishes the initial zswap pool with `list_add_rcu()`.
  - `2172` enables `zswap_ever_enabled` in `zswap_pool_create()`. Without it, a
    failed boot-time pool creation left the key off, and a pool created later
    through `zswap.compressor` stored through zswap while the swapin path
    skipped it, returning zeroed pages.
  - `2173` fixes the `SWAP_USAGE_OFFLIST_BIT` collision.
  - `2174` fixes a NULL dereference when a sleep-table allocation is retried.
  - `2175` stops a large-folio swapin from returning `VM_FAULT_SIGBUS` for a
    range that is not in zswap.
  - `2177` validates the in-memory LZ4 chunk length. This runs on every boot;
    `/etc/mkinitcpio.conf` sets `COMPRESSION="lz4"`.
  - `2178` fixes `plist_requeue()` order corruption in `rtmutex`/`futex`.
  - `2179` fixes access after wake in `klist_remove()`.
  - `2180` fixes the `mod_ct` value in `dynamic_debug_init()`.
- Add `2503`-`2507`, the x86 PAT group: `init_mm` read and write locking around
  attribute changes and collapse, the effective-RW computation in
  `lookup_address()`, split page tables allocated as kernel page tables, and
  alternatives text poking excluded from a concurrent `change_page_attr`.

### Rejected

- `a0d356696f87`, `63b4ff622244` and `89ff16f07139` touch only
  `tools/sched_ext/scx_qmap.bpf.c` and `scx_qmap.h`. The PKGBUILD does not build
  `tools/`, so they change nothing in the shipped kernel.
- `c7a1c6e8004a` is carried as `2404`.
- `392dee2b81f4` and `8679598143f2` (bootconfig): `/proc/bootconfig` is empty
  and the command line enables nothing.
- `c922c000d06e` (bunzip2 run-length bound) guards an initramfs compressor this
  machine does not build.
- `364e520095b2` and `4cf50332b538` (`crypto: rsassa-pkcs1`): `MODULE_SIG_FORCE`
  is unset, so an unsigned module loads regardless, and the parser only sees
  signatures this machine produced.

### Changed
- `pkgrel` 17 -> 18. Series is now 242 patches. Correct the per-range table in
  `PATCH_SOURCES.md` for `9000`-`9099` (41 recorded, 45 present).

## [7.3.0-rc3-17-sleepy-next]: 2026-09-16

### Added

- Add `9072`-`9075`, Jesse Zhang's SDMA hung-queue detection and recovery series
  (amd-staging `972a8cd8fba1`, `994dea375802`, `ba07df579939`, `10a6760a1a64`;
  linux-next `4a3ef2809c88`, `17bd3e9f404e`, `6537bd210878`, `4a263bc34083`):

  | # | Patch |
  |---|---|
  | `9072` | `drm/amdgpu/sdma: add detect_hung_queue callback` — a new `amdgpu_sdma_funcs` hook |
  | `9073` | `drm/amdgpu/sdma6: implement detect_hung_queue` |
  | `9074` | `drm/amdgpu/sdma7: implement detect_hung_queue` |
  | `9075` | `drm/amdgpu/userq: reset a hung SDMA user queue over MMIO` |

  `9074` walks the per-queue doorbell-offset registers
  (`SDMA0_QUEUE0_DOORBELL_OFFSET + q * SDMA_V7_0_QUEUE_REG_STRIDE`) to find the
  hardware slot whose doorbell matches the stuck one. SDMA 7.0 is the Navi 48
  SDMA block. `9075` recovers the queue over MMIO instead of taking a full GPU
  reset. This covers the SDMA hang class in drm/amd #5663 and #5693.
- Apply on two subsystems this machine runs: SDMA7, and the userq path where the
  kref series (`9062`-`9071`) is already carried. `9075` touches
  `mes_userqueue.c`, which `9067` also modifies.
- Verify all four against a clean `v7.3-rc3` worktree and against the
  series-applied tree, under both `git apply --check` and
  `patch -p1 --forward -F2 --dry-run`. Each carries `Signed-off-by` and a
  `Reviewed-by` or `Acked-by`.

### Rejected

- `0251963afd22` (`gpu/buddy: Fix use-after-free in split_block() call sites`):
  a genuine use-after-free and rbtree corruption, but the base already has the
  fix. `__gpu_buddy_undo_splits()` (`drivers/gpu/buddy.c:737`) calls
  `rbtree_remove()` before `__gpu_buddy_free()`, which is the ordering the patch
  introduces; the patch targets the pre-refactor shape of the four `err_undo`
  sites.
- `dml2_core_dcn4_calcs.c` (+172 lines): DCN4, but the churn is in
  `max_flip_time`, `lb_flip_bw` and `iflip_enable`, the area AMD reverted for
  causing regressions (`c010ccac1358`, `04009276da2d`).
- HDMI RGB quantization (Alex Hung): selects `COLOR_SPACE_2020_RGB_LIMITEDRANGE`
  in `amdgpu_dm_connector.c`. 7.4 content; noted as a rebase point.
- The September DC patchsets (`00/40`, `00/66`): of 106 patches, three are
  carried (`1154`, `1159`, `1166`). The rest is DCN6, DCN35, DCN42B, DCN50,
  DCN60 and DML2.1.

### Changed
- `pkgrel` 16 -> 17. Series is now 221 patches.

## [7.3.0-rc3-16-sleepy-next]: 2026-09-15

### Changed

- Move `net-tune.service` and `blocky.service` under `network-online.target`.
  Both carried `WantedBy=multi-user.target` with `After=network-online.target`,
  which made `multi-user.target` wait for DHCP: `NetworkManager-wait-online`
  took 12.346s and held `graphical.target` to 14.751s. `net-tune` moves in the
  package, including its `WantedBy`, enable symlink and install step. `blocky`
  uses an explicit `network-online.target.wants` symlink, because
  `systemctl enable` reads `[Install]` from the unit file and ignores a
  drop-in's `WantedBy`. Both still start when the link comes up.
- Build `R8169` and `REALTEK_PHY` in rather than as modules. As modules, udev
  loaded them after the root switch, so driver probe and the approximately 3s
  of autonegotiation ran after most of boot. The PHY driver must be built in as
  well, or the carrier waits for it to load.
- Raise `vm.swappiness` from 150 to 180. The 150 was CachyOS's zram udev-rule
  default, kept for continuity. `Documentation/admin-guide/sysctl/vm.rst`
  defines swappiness as a relative IO cost over 0-200 in which 100 means equal
  cost, and states that in-memory swap can go beyond 100. The Arch Wiki's Zram
  article recommends 180 together with `watermark_boost_factor = 0`,
  `watermark_scale_factor = 125` and `page-cluster = 0`; the other three are
  already set in `/etc/sysctl.d/99-custom-tweaks.conf`. Documented in
  `sleepy-next/swap-stack/99-xswap-swappiness.conf`.
- Drop the dead `vm.swappiness` line from
  `/etc/sysctl.d/99-custom-tweaks.conf`. It also set 180, so the 150 won by
  lexicographic filename order.

### Fixed

- Remove `After=local-fs.target` from `xswap-create.service`. It formed an
  ordering cycle (`tmp.mount -> swap.target -> xswap-create ->
  local-fs.target -> tmp.mount`) that systemd broke by deleting the `tmp.mount`
  job at every boot. The root filesystem is mounted by the initramfs, so
  `Before=swap.target` is sufficient.

### Removed

- Disable `system76-power-monitor.service`. It is hand-written, owned by no
  package, ordered `After=com.system76.PowerDaemon.service` which does not
  exist, and runs a polling loop for a binary that is not installed. The unit
  and script remain on disk.

### Verified

Measured on `7.3.0-rc3-16` after reboot:

- The DHCP gate is gone. `graphical.target` is reached after 2.083s of
  userspace, down from 14.751s. Total boot is 29.5s to 24.9s, and 17.2s from
  power-on to a usable desktop. `NetworkManager-wait-online.service` still
  takes 7.666s but runs behind the desktop.
- `r8169` probes at 0.663s, down from 7.211s. Carrier moved from 10.13s to
  9.79s, because PHY attach and link-up are now gated by userspace, with udev
  renames at 6.4s and approximately 2.9s of autonegotiation.
- Stage timings: firmware 9.835s, kernel 2.100s, initrd 2.717s, userspace
  2.083s.

### Known issues

- `mem_cgroup_update_lru_size()` underflows on every boot (`lru_size -2522`),
  from `lru_reparent_memcg()` through `mem_cgroup_css_offline()`. LRU-MARIE's
  own comments document the cause: a folio entering MARIE receives a legacy
  debit that MARIE never credits, so the per-memcg counter drifts downward. It
  fires on every `sleepy-next` boot from rc3-6 and on no `cachyos-rc` boot.
  LRU-MARIE 0.11.1r2 is the newest revision and retains at least one such path.
  `WARN_ONCE` makes one occurrence per boot a lower bound. `CONFIG_DEBUG_VM` is
  off, so the adjacent `VM_BUG_ON(1)` is inert; with it enabled this would be a
  `BUG()`.
- `network-online.target` is not reached until approximately 12s into boot, so
  `net-tune` (CAKE) and `blocky` (DNS) are inactive until then. Nothing waits
  for the target, so this is a functional gap rather than a boot-time one.
  Closing it requires triggering both from the interface coming up;
  `net-tune.sh` exits 1 when no interface is up.
- A 725ms gap inside the initrd, between fsck finishing at 2.730555 and
  `/sysroot` mounting at 3.478237. Only USB enumeration appears in the log, and
  `systemd-udev-settle` is not in the initramfs.
- Dead configuration prints errors every boot. All of it is owned by CachyOS
  packages under `/usr/lib`, so the fix belongs upstream: amdgpu
  `si_support=1 cik_support=1`, which are GCN-era options that do not exist for
  Navi 48; `70-cachyos-settings.conf` writing `kernel/nmi_watchdog` and
  `kernel/unprivileged_userns_clone`, neither of which this kernel has; and a
  `sp5100_tco` blacklist for a driver that is not built.
- `nowatchdog` on the command line is inert. The kernel reports `Unknown kernel
  command line parameters "nowatchdog"`, and `CONFIG_SOFTLOCKUP_DETECTOR` and
  `CONFIG_HARDLOCKUP_DETECTOR` are both unset. `CONFIG_CLOCKSOURCE_WATCHDOG=y`
  is running and was never controlled by it.

### Rejected

- `kexec` reboots. They skip the 9.835s POST but re-initialise the GPU from a
  running kernel, which is not appropriate while the display path is under A/B.
- Dropping the `kms` hook. It saves approximately 245ms of the 485ms ESP read
  but changes when the display modesets.
- Dropping the `base` hook. It provides the recovery shell, and the presets
  build no fallback image.
- `MODULES_DECOMPRESS="yes"` with `xz -9e`. It trades an approximately 250ms
  ESP read for single-threaded decompression.
- Trimming the 54.5 MB initramfs. It unpacks in 25ms, so there is nothing to
  win. The bulk is approximately 29 MiB of amdgpu firmware that mkinitcpio
  moves into the early CPIO to avoid double compression.
- Clearing `After=` on `cachyos-rate-mirrors.timer` through a drop-in. It was
  measured to change nothing, because an empty `After=` in a drop-in does not
  reset the ordering list. Its `Wants=` is load-bearing and stays.
- `libahci.ignore_sss=1`. It is applicable, but nothing on the critical path
  waits for the MX500, which is `x-systemd.automount`.
- Silent-boot console flags. The console is the GPU framebuffer, so they touch
  the display path.
- Disabling `bpftune`. This package builds `-d TCP_CONG_BBR -e
  TCP_CONG_BBR3`, so CachyOS's bpftune looks for a congestion control named
  `bbr` that cannot exist here, then rewrites
  `net.ipv4.tcp_allowed_congestion_control` three times per boot chasing it,
  and counts the failures as successes. `net-tune` sets that key regardless.
  Working tuning tool with a broken edge; left enabled.

### Changed
- `pkgrel` 15 -> 16.

The six-source sweep that ran alongside this release is recorded in
`PATCH_SOURCES.md` under *Sweep 2026-09-16*.

## [7.3.0-rc3-15-sleepy-next]: 2026-09-15

### Added
- **`1166`** — "drm/amd/display: Return success status from check_mode_supported"
  (Alvin Lee, `Reviewed-by: Wenjing Liu`, DC 3.2.398 patch 59/66,
  `<20260908113338.2433445-60-chen-yu.chen@amd.com>`). `dml2_top_utm_check_mode_supported()`
  logged DML2's verdict and then returned a hardcoded `true`, so a mode the
  display mode library had rejected was still programmed. The fix returns
  `status == DML2_STATUS_OK`; it is the patch AMD recommends in the reports of
  **#5834** — a NULL pointer dereference in `update_config` that hits roughly 30%
  of the time when waking from screen-off (plain DPMS, not suspend) on a 9070 XT,
  leaving a blank screen and no usable tty. DPMS cycling is daily use here, and
  the same series' patch 58 is already carried as `1159`.
  *Watch on the first boot:* this makes mode validation authoritative, so a mode
  DML2 rejects is now refused instead of programmed. 1920x1080@240 and 1080p are
  ordinary modes for DCN 4.0.1 and unlikely to be rejected, but if the display
  comes up at the wrong mode after rebooting, drop `1166` (or boot the
  cachyos-rc entry) — that is the revert, and the changelog is the record.

### Verified after the reboot (2026-09-15 22:29, running `7.3.0-rc3-15`)

- **xswap is live**: `zswap/enabled=Y`, `compressor=zstd`, `/proc/swaps` shows a
  single `xswap0` of 30.9G at priority 100 with pages already in it (83 MB
  compressed holding 268 MB, ~3.2x), `/sys/kernel/mm/xswap/{create,destroy,type0}`
  present, and `xswap-create.service` exited 0. No zram swap anywhere; the
  leftover `zram0` node is size 0 and its setup unit is dead. `vm.swappiness`
  is 150 from the sysctl drop-in, replacing what the masked udev rule used to set.
- **The flicker fix holds**: `vrr_capable=0` and `passive_vrr_capable=0` on both
  HDMI connectors, `VRR_ENABLED=0`, `PASSIVE_VRR_DISABLED=1` — the same state the
  clean cachyos-rc kernel showed.
- **`1166` did not reject the mode**: CRTC 438 is driving 1920x1080 at
  **239.96 Hz** as before. This was the one item to watch after making DML2 mode
  validation authoritative, and it is the outcome that mattered.
- One `amdgpu` message appears (`Failed to setup vendor infoframe on connector
  HDMI-A-2: -22`); it is present with the **same count in the previous boot**, so
  it predates this series and belongs to the second monitor's sink, not to any
  patch here.

### Changed
- `pkgrel` 14 → 15. Series is now 217 patches.

## [7.3.0-rc3-14-sleepy-next]: 2026-09-15

### Added
- **`2170`** — "mm: vmalloc: fix `vmap_purge_lock` livelock under memory
  pressure" (Ye Liu, `6c06fec56a63d`, `Fixes: 7679ba6b36db`,
  `Reviewed-by: Uladzislau Rezki (Sony)`, in akpm's tree). `__purge_vmap_area_lazy()`
  holds `vmap_purge_lock` across a `flush_work()` while `vmap_node_shrink_scan()`
  can block on that same lock from direct reclaim — a circular wait that
  deadlocks the whole system under memory pressure. The fix takes the lock with
  `mutex_trylock()` in both reclaim-reachable paths and reports
  `SHRINK_STOP`; skipping a pool decay is harmless. `mm/vmalloc.c` is not
  touched by any other patch in the series.

### Changed
- **Renumbered for order.** `1165` now sits after `1164` instead of back at the
  `1140` slot it kept when it was renamed from `1140`, and `2142` became
  **`2169`** so the three parts of its series read `2167`, `2168`, `2169`.
  `source=()` is now sorted ascending end to end. No patch content changed.
- `pkgrel` 13 → 14. Series is now 216 patches.

### Ledger repair
- `PATCH_SOURCES.md` had a stale index row for `9061` (evaluated and dropped
  for a compile failure, never carried) and **no row at all for `0055`**, which
  is carried. Both fixed; `0055`'s row now names its real provenance (a
  `[sleepy]`-stripped version of Fangzhi Zuo's submission, not the
  `150619` archive id the prose implied). Every remaining row without a file is
  an intentional "Dropped" record.

## [7.3.0-rc3-13-sleepy-next]: 2026-09-15

### Fixed
- **`2142` was an incomplete series, and incomplete made it wrong.** It is
  patch 3/4 of Xueyuan Chen's "[PATCH v7 0/4] mm: avoid large folio splits when
  swap is unavailable"; only 3/4 was carried. It gates the large-folio split
  fallback in `shrink_folio_list()` on `ret != -E2BIG`, and **nothing in the
  tree returned `-E2BIG`** — 2/4 is what introduces that classification — so
  every `folio_alloc_swap()` failure took the "do not split" branch. The THP /
  mTHP swapout fallback was unreachable dead code, the exact opposite of the
  patch's intent, and it made large anon folios that could not get swap get
  reactivated instead of split. Added **`2167`** (1/4, `page_counter_margin()`)
  and **`2168`** (2/4, the `0`/`-E2BIG`/`-ENOSPC`/`-ENOMEM` classification,
  `Acked-by: David Hildenbrand`), which restores the intended behaviour: split
  only when splitting might help, skip the pointless split when swap is
  exhausted. Patch 4/4 (shmem) is not carried and not needed for correctness.
  This is the failure mode the "a patch that applies can still do nothing" rule
  warns about, in the opposite direction: the patch did something, and the
  something was wrong.

### Deep sweep results not adopted
- **Work items**: `dc66/59` ("Return success status from check_mode_supported",
  Alvin Lee, AMD) is the one AMD recommends in #5834's NULL-deref reports and
  it applies cleanly to the series. Not adopted yet **because of what it
  changes**: it makes DML2 mode validation actually return failure instead of a
  hardcoded `true`. If DML2 dislikes 1920x1080@240 it would now be rejected, and
  this display just got fixed. It arrives with the DC 3.2.398 drop in the next
  drm merge, where AMD tests the set together — re-evaluate then.
- Wentland's RGBA8888 surface-format enablement (#5339, field-tested on Navi 48)
  is skipped on evidence: this machine logs **zero** "Unsupported screen format"
  messages in dmesg and the journal, so it is not hit here.
- superm1's EDID-override pair (#5779) only matters if an override is in use.
  Correcting an earlier note: it does **not** collide with `1143` (different
  files entirely).
- MM: Kefeng Wang's zswap invalidate/store v3 has **no measured claim** in its
  cover letter ("eliminate redundant per-slot lookups"), and it shares
  `swap_range_free()` with the xswap series — still deferred for that reason.
  Usama Arif's PMD-level swap v7 does not apply as posted (needs `f078c72e5ca2`
  + `94edc3c732625` for 12/29 and a hugetlb patch absent from rc3 for 14/29).
  Hugh Dickins' fbatch v2 collides with LRU-MARIE in `mm/folio.c` (436 changed
  lines) and its author expects "some disappointments".
- The Ghiti zswap-writeback fixes fail on the series state at `mm/zswap.c:1001`
  — exactly where xswap's `2155` rewrites the store/writeback path. They are
  accounting fixes, and there is no writeback target (no disk swap).

### Changed
- `pkgrel` 12 → 13. Series is now 215 patches.

## [7.3.0-rc3-12-sleepy-next]: 2026-09-15

### Added

- Add `2012`-`2013`, Zhenxian Ma's "block: avoid redundant flushes for O_DSYNC
  direct writes" pair (linux-next `bec7d36a6514`, `0d492f40c4ad`).
  `blkdev_write_iter()` called `generic_write_sync()` unconditionally, so an
  `O_DIRECT|O_DSYNC` write paid a `REQ_PREFLUSH` on top of the `REQ_FUA` the
  direct path had already set. The author measured 4 KiB `O_DIRECT|O_DSYNC`
  writes on a Seagate ST20000NM007D going from 119.7 to 7497 IOPS. The Phison
  E16 reports `fua=1`, so `2013` is inert here; `2012` removes the redundant
  flush.
- Regenerate `2100` from sirlucjan's 2026-09-14 `zstd-7.3` cut (`e0f9795534f4`,
  2741 lines across 25 files, up from 20). The newer cut carries additional
  upstream zstd work, including a BMI2 dispatch refactor
  (`lib/zstd/common/bmi2.h`). zstd is load-bearing for the swap stack, not only
  for btrfs.

### Removed

- Remove `2128` (use `ZSTD_cpuSupportsBmi2()` in `ZSTD_initStaticCCtx()`) and
  `2143` (DDict hash-set probe wrap-around). Both are now inside the
  regenerated `2100`; its hunk reports already-applied and `2143` is skipped as
  present. The code remains in the tree through `2100`.

### Changed
- `pkgrel` 11 -> 12.

The three parallel sweeps that ran alongside this release, and the deep
GPU/display pass that followed, are recorded in `PATCH_SOURCES.md` under
*Sweeps 2026-09-15*.


## [7.3.0-rc3-11-sleepy-next]: 2026-09-15

### Added
- **`2155`–`2166`** — Baoquan He's **v2 xswap series**, "mm, swap: extendable
  swap devices" (linux-mm, 2026-09-13,
  `<20260913075014.1732524-2..13-hebaoquan@kylinos.cn>`), 12 patches: the
  `XSWAP` Kconfig option, a sparse-vmalloc `cluster_info[]`, grow and shrink
  triggers driven by allocation and free, the `sysfs create` interface, a
  workqueue-deferred shrink, `xswap_destroy`, the zswap requirement, and a
  per-device size limit. An xswap device has no backing store — swapped pages
  live in zswap — and its metadata is mapped lazily, so it starts at 1xRAM and
  costs nothing until used. CachyOS carries the same series in its `7.3/xswap`
  branch. `CONFIG_XSWAP=y` is set. Upstream work in review: drop it when it
  lands, and check for a v3 before rebasing.
- **Swap stack switched from zram to zswap + xswap** on this machine. zram
  allocated a fixed 30.9 GB compressed block device and never gave the memory
  back; xswap grows and shrinks with use. The kernel side is the series above;
  the userspace side is `/etc/systemd/system/xswap-create.service` (creates one
  device at priority 100), `/etc/systemd/zram-generator.conf` and
  `/etc/udev/rules.d/30-zram.rules` symlinked to `/dev/null`, and
  `zswap.enabled=0` removed from `LINUX_OPTIONS` in `/etc/sdboot-manage.conf`
  so the built-in `CONFIG_ZSWAP_DEFAULT_ON=y` takes effect. Masking the udev
  rule matters: it forces `zswap/parameters/enabled` to `N` whenever a zram
  device appears, which would make `xswap/create` return `-EOPNOTSUPP`.
  `vm.swappiness=150` moves to `/etc/sysctl.d/99-xswap-swappiness.conf`; the
  masked udev rule used to set it.




### Changed
- **`2101`** now carries LRU-MARIE **0.11.1r2** from the author's repository
  (<https://github.com/firelzrd/lru_marie>). The r2 revision is 0.11.1 minus
  the `localversion` file creation (the `-marie` version suffix), which this
  repository had already stripped. It also restores the author's
  `scripts/setlocalversion` change — an `echo "+"` commented out — which is
  inert here because the kernel is built from a tarball and that branch only
  runs inside a git tree. The built version string is unchanged.
- `pkgrel` 10 → 11. Series is now 213 patches.

### Reviewed and not included: cachymod
[cachymod](https://github.com/marioroy/cachymod) is a CachyOS kernel
customization toolkit (TUI, build configs, and a patch set). Reviewed on
2026-09-15; nothing was adopted:
- `0280-prefer-idle-core` was **reverted by CachyOS itself**
  (`a4808133047d`), and its author calls it trial-and-error EEVDF tuning
  measured on a Threadripper 3970X (many CCDs) — this machine has one CCD.
- `0000-revert-prop-newidle-bal` reverts mainline `9fe89f022c05` ("More
  complex proportional newidle balance"), which is present in rc3, and it
  applies cleanly. Not adopted: the supporting measurement is a 6.18.5-era
  easyWave regression ("persists with 7.1-rc, though not as bad"), and
  upstream has since reworked that area (`b3a2dfa8b42e`, `c095741713d1`).
  Reverting it would be a permanent divergence from the scheduler mainline.
- `0300-x86-prevent-avx2-vector` adds `-mno-avx2 -fno-tree-vectorize
  -mpopcnt`. Not adopted: `CONFIG_MZEN4` selects `-march=znver4` and the
  kernel appends `-mno-sse -mno-avx` after it, and an audit of the linked
  vmlinux (disassembled, mapped through `/proc/kallsyms`) found all 3,089
  `ymm`/`zmm` instructions confined to 27 deliberate vector functions — the
  x86 crypto assembly (poly1305, chacha, sha1/sha256/sha512, crc32/crc64
  AVX2 and AVX-512) and the NAP governor's AVX2 neural-network predictor.
  None appear in compiler-generated generic code. cachymod's own configs
  leave the option off by default too (`_prevent_avx2:=no`).
- `0200-clearlinux-extras` is the Clear Linux patch set. Several entries are
  Intel-only (`itmt_epb`, `itmt2` ADL fixes, `epp-retune`); the rest are
  generic micro-optimizations with no target here. Modern CachyOS does not
  carry them either (its `clearlinux-5.18` branch was reverted).
- The remaining patches revert CachyOS scheduler modifications that this
  series never carried (`gaming-sched`, POC, `sched/fair` tunings), or belong
  to cachymod's own build framework (gnu17 switch, DKMS clang, 800 Hz tick
  option — this kernel runs `CONFIG_HZ=1000`).
- Config comparison: this kernel already matches or exceeds cachymod's
  defaults — THP `always`, `CONFIG_PREEMPT=y`, `CONFIG_HZ=1000`, plus BBR3.

### Sweep 2026-09-15 (evening)
- Nothing new in agd5f, drm-next, linux-pm, or the CachyOS branches today.
- **`next-20260915`**: its tree diff against `next-20260914` is 737 files
  (+42k/-12k). Nothing in it needs adding. Two commits checked by content:
  `aa55d949bf9f` is byte-identical to `f7491d7c81db`, the fix already carried
  as `2500` (same author, same date, identical diff), and `eddf1f80667e` is
  `2151`. *Method note:* `git log A..B` between two linux-next tags returns
  **1.47 million** commits, because the tags are rebased onto fresh bases daily
  — the commit list is meaningless. Use `git diff` for content and the tag's own
  merge commits for attribution; `git log` between tags produces a confident,
  wrong "delta". The hugetlb subpool accounting fix
  (`1ff1504af83d`) is unreachable here — `HugePages_Total` is 0, so nothing
  allocates from a hugetlbfs subpool. `228200f695c0` fixes Zen 5 TLB size
  reporting (a CPUID bit Zen 4 does not set). The block delta is entirely
  zoned-storage work, which this NVMe does not use.
- xswap had no v3 and no review replies at the time of the check.

### Housekeeping
- Removed the accumulated `*.pacnew` / `*.pacsave` files (13 of them, some
  from January) after diffing each against its live config; they are archived
  at `~/etc-pacnew-pacsave-20260915.tar.gz`. The live configs were the
  deliberate ones in every case (for example `resolved.conf` sets `FallbackDNS=`
  empty and `MulticastDNS=no`; `system.conf` sets `DefaultTimeoutStartSec=0s`).
- Removed four dangling systemd-boot entries (`linux-cachyos-cacule`,
  `linux-cachyos`, `linux-next`, `linux-sleepy`) whose kernels no longer exist
  on disk, via `sdboot-manage remove`. Three valid entries remain.
- `xswap-create.service` needed `DefaultDependencies=no` + `After=local-fs.target`:
  `systemd-analyze verify` found an ordering cycle (swap.target is ordered
  before sysinit.target, so a default-dependency service that is `Before=swap.target`
  deadlocks the graph and systemd deletes the swap.target job to break it —
  which would have silently skipped the unit at boot).

## [7.3.0-rc3-10-sleepy-next]: 2026-09-15

### Added
- **`9062`–`9071`** — Zhu Lingshan's "secure userq lifecycle by its kref"
  series (10 patches, amd-gfx, RESEND 2026-09-14,
  `<20260914130724.130794-2..11-lingshan.zhu@amd.com>`). A doorbell lookup
  helper that holds the queue kref, userq-manager lifetime tied to its
  queues, kref held in the gfx11/gfx12 private fault workers (this chip is
  the gfx12 one), asynchronous userq destruction, kref held across MES
  reset / isolation scheduling / suspend-resume, and create-path UAF fixes.
  Hardens the user-queue submission path that the 9000s backports ship.
  Still under review (the author pinged AMD on 2026-09-14); drop or refresh
  when the series lands in agd5f. Two of the ten patches apply only against
  the series-applied tree, not clean rc3 — the context comes from the
  existing userq backports.

### Sweep 2026-09-15
- **Upstream now — drop at the next bump**: `2148`/`2149` (crypto zstd
  init dedup) are in linux-next for 7.4 (`0db478c2e26f`, `57818119c9eb`);
  `2500` (x86/mm MADV_FREE-THP data loss) is in mainline x86_urgent
  (`f7491d7c81db`) and arrives with rc4.
- **Watch for 7.4**: amd-pstate per-SoC EPP tunings (linux-pm pull,
  2026-09-14) — the override table is empty for non-hybrid platforms, so
  Zen 4 keeps the legacy defaults; a no-op here, skip. The mqd_prop
  modify-flag series (v4, amd-gfx) depends on agd5f CU-mask work. Alex
  Hung's 66-patch DC series (KUnit tests, dcn42b power gating, MALL
  removal) heads for amd-staging. Jens Axboe's io_uring rsrc prefill and
  thread-identity RFCs. sirlucjan's zstd-dev-patches v3 (2026-09-14) —
  regenerate `2100` from it at the next bump instead of churning now.
- **Work items tracked, no fix referenced yet**: RX 9070 XT hard
  hang/reset deadlock (#5821), SMU bus loss (#5820), vblank-wait timeout
  (#5800), VRR black level over DisplayPort (#5812), HDMI FRL after
  standby (#5780).
- **Skipped**: ESMTP guest hardening (EPYC/SEV, not this machine), EROFS
  LZ4 rollback (not this filesystem), jitterentropy hardware mixer (watch
  only), Zen6 EPP tunings (wrong CPU).

### Changed
- `pkgrel` 9 → 10. Series is now 201 patches.

### Handmade-patch audit (0001–0049)
All 12 patches in the handmade range were checked against rc3 upstream code:
every one is still valid (applies and compiles in rc3-10) and still needed —
none of the fixes has an upstream equivalent yet. Notably `0001`'s `unsigned
tyep` typo and `0005`'s `// TODO` mode1-reset stub are both still in rc3
verbatim, and the `0031`/`0034` resource leaks are still present in rc3's
dcn401 code. `0055` (the local `drm_hdmi_vrr_cap` struct) stays: rc3 does not
define the field anywhere, and `1163`'s guard reads it.

## [7.3.0-rc3-9-sleepy-next]: 2026-09-15

### Fixed
- **VRR advertisement regression — the MAG251RX flicker bisect ends here.**
  The clean CachyOS 7.3 rc kernel (rc2-based) reports `vrr_capable=0` and
  `passive_vrr_capable=0` on both HDMI ports and does not flicker; this rc3
  line reported 1/1 and flickered at 240 Hz. Bisecting the diff between the
  two trees: the MSI MAG251RX EDID has an AMD VSDB **v1** (48–240 Hz, MCCS
  flag) and no HF-VSDB VRR block (`hdmi.vrr_cap.supported=0`), so the only
  path to `freesync_capable=true` is the AMD-VSDB parse plus the MCCS gate.
  Upstream `cfdcf5571c31` ("Consult MCCS FreeSync cap only if requested &
  supported", merged for rc3) moved the MCCS clear inside `if (do_mccs)`; the
  later `do_mccs=false` pass from `amdgpu_dm_connector_ddc_get_modes()` then
  re-advertises VRR on HDMI sinks whose MCCS VCP does not answer. rc2 (and
  cachy) cleared unconditionally and stayed at 0.
- **`1164`** reverts `cfdcf5571c31` (adapted to the 1163 form in the series),
  restoring the unconditional clear with the HF-VSDB VRR exemption kept.
  Result: `vrr_capable=0` + `passive_vrr_capable=0` on both HDMI ports, the
  VRR option disappears from cosmic-settings, and the runtime state matches
  the cachy kernel verified clean on this monitor.
- Box bug: the rc2→rc3 window carried zero DCN401/HUBP/clock-manager changes
  (verified by log), and CachyOS carries no extra DCN401 fix — the baked
  `amdgpu.dcdebugmask=0x800` (IPS power states off) remains the documented
  mitigation for the HUBP flip-pending artifact, unchanged in this release.

### Changed
- `pkgrel` 8 → 9. Series is now 191 patches.

## [7.3.0-rc3-8-sleepy-next]: 2026-09-14

### Added
- **`2011`** r8169: don't enable chip LTR when the platform has not enabled
  LTR (Yogesh Gaur, `[PATCH net v4]`,
  `<20260914130050.304-1-yogeshgaur.83@gmail.com>`). This machine's NIC.
  rc3's `rtl_hw_aspm_clkreq_enable()` calls `rtl_enable_ltr()` on every ASPM
  enable, gated only on `tp->aspm_manageable`, which says nothing about LTR;
  the PCI core's `pci_dev->ltr_path` verdict is never consulted. On platforms
  where LTR is not end-to-end the chip still programmes ALDPS_LTR_EN and can
  trigger L1.2 — the reported symptom class is link flaps and downshifts.
  Applies clean.

### From the sweep, deferred with reasons
- sched_ext lazy preemption v3 (Righi, for-7.4): a feature for the next
  window, not a fix for this base.
- MGLRU rejected-folios v3 (Baolin Wang): inert here — LRU-MARIE owns
  reclaim — and it needs a rebase past the eight `mm/vmscan.c` patches.
- Seven post-rc3 mm fixes (`12e9ac7bc5b2` SWAP_USAGE_OFFLIST_BIT,
  `6e673d0879ef` root-memcg charging, `397432cab17b` mremap locked_vm,
  `e384abeb559d` THP tuneables, `932cfb25e7ce` shrinker nokmem, plus two
  inert): all apply-tested clean upstream but arrive with the rc4 bump — no
  point carrying them for a day.
- amd-pstate 7.4 pull: a no-op for this machine — the `epp_soc_ids[]` table
  is empty and non-hybrid Zen 4 keeps the legacy defaults.

### Drop-list data for the next bump
- `2141`, `2145`, `2146` are now upstream in rc4.
- `2140`, `2144`, `2150`–`2154` are still akpm-only.
- `2500` is upstream in rc4 (`f7491d7c81db` via `x86_urgent_for_7.3-rc4`).

## [7.3.0-rc3-7-sleepy-next]: 2026-09-14

### Removed
- **`0055` and `0060`** — `0055` (drm/edid: parse HDMI 2.1 gaming ALLM/VRR capabilities from
  HF-VSDB). The decisive bisect step for the 240 Hz flicker, and the first one
  grounded in a value difference, not a guess.

  Captured from the flicker-free cachyos-rc kernel at runtime: `vrr_capable=0`
  and `passive_vrr_capable=0` on **every** connector, so cosmic-settings offers
  no VRR option at all. Ours advertised `vrr_capable=1` on both HDMI outputs.
  `0055` is the patch that creates that advertisement: its
  `drm_parse_hdmi_gaming_info()` sets `vrr_cap.supported=true` from the
  HF-VSDB VRR range in the MAG251RX's EDID. CachyOS's tree carries the
  `drm_hdmi_vrr_cap` struct but never sets the flag.

  The chain that follows from the advertisement: `0060` (dropped in the same build) had a fallback that set
  `freesync_capable=true`, the driver sends FreeSync signalling to a G-Sync
  Compatible panel whose scalar then sits in a half-negotiated VRR state —
  flicker at 240 Hz where content changes (cursor movement), and the box, whose
  old symptom was that it moved to whichever monitor last had VRR toggled.

  Without `0055`, the advertisement is gone, `0060`'s fallback becomes inert,
  and the whole chain matches the known-good kernel. VRR over HDMI disappears
  as a feature; that is the accepted trade for this machine, and it matches
  the stock kernel's behaviour exactly.

  *Correction (rc3-9):* this hypothesis was wrong — dropping `0055`/`0060`
  did not zero the chain (`vrr_capable` stayed 1). The actual cause was
  upstream `cfdcf5571c31`, fixed by `1164`; see the rc3-9 entry.

### Added
- **`1163`** drm/amd/display: keep `freesync_capable` for HF-VSDB VRR sinks in
  the MCCS fallback. A rebase of Fangzhi Zuo's upstream submission
  `<20260901191251.2653684-4-jerry.zuo@amd.com>`, which this series carried as
  patch `1145` until the rc3 rebase dropped it on the assumption that rc3's
  rewrite of `amdgpu_dm_update_freesync_caps()` superseded its purpose.

  The rewrite restructured the function but kept the MCCS clear without the
  `vrr_cap.supported` term — and the kernel-to-kernel diff against the
  flicker-free CachyOS `7.3/base` tree shows they carry exactly that guarded
  version. The user's test on `pkgrel 6` exonerated both `1144` and `0030`, and
  this is the next bisect step with the strongest evidence yet:

  - The MAG251RX is a G-Sync Compatible panel: its EDID carries a FreeSync VCP
    code and an HF-VSDB VRR range. Its MCCS does not answer the AMD VCP read.
  - Without the guard, the rc3 code clears `freesync_capable` for exactly this
    sink, so the driver stops FreeSync signalling while the monitor's
    Adaptive-Sync OSD stays on — the panel sits in a half-negotiated state that
    flickers, worst where content changes (cursor movement) and worst at
    240 Hz timing.
  - The guard skips the clear for `vrr_cap.supported` sinks, keeping the
    HF-VSDB fallback alive.

### The bisect record
- `pkgrel 6` was tested: **`1144` and `0030` are exonerated** — the flicker
  persists with both dropped. Recorded rather than quietly extended.

## [7.3.0-rc3-6-sleepy-next]: 2026-09-14

### Removed
- **`0030`** (handmade: proactively shrink DET for pipes losing space). The
  second bisect step for the 240 Hz flicker, dropped in the same build as
  `1144`. `0030` patches `dcn401_prepare_bandwidth()` — the DCN401
  bandwidth-transition function that programs watermarks, the arbiter, compbuf
  and DET before a clock update — and immediately programs a smaller DET size
  for pipes that are losing space, *before* the pipe stops scanning at its old
  requirements. That transient can underflow the pipe's DET buffer and the
  shared CRB: visible at 240 Hz timing margins, invisible at 144 Hz, and
  triggered exactly by cursor-driven surface updates, which set the
  `det_size` update flag on pipes. CachyOS does not carry it.

  The identification came from the kernel-to-kernel diff the bisect demanded:
  the applied display tree against CachyOS `7.3/base` shows 32 differing
  files, and the DCN401 hardware-sequencer difference is this patch alone —
  everything else in `dcn401_hwseq.c` is identical between the two trees.

  Two variables are changed in this build (`1144` and `0030`). If the flicker
  is gone, a follow-up build can re-add one of them to isolate; if it
  persists, both are exonerated and the next suspect is the baked command line
  (`cpuidle.governor=nap`).

### Changed
- **The kbuild build-speedup series is upgraded from v1 to v2**
  (`20260914-build-speedup-v2-0-39817ec5db23@kernel.org`, 21 patches,
  replacing the v1 content on the same numbers `2302`–`2322`). v2 drops two v1
  patches (the modpost srcversion hashing and its source-per-file companion),
  adds two (the toolchain checks moved into `init/Kconfig.toolchain`, and
  objtool sizing its instruction hash to the text), and refreshes the rest with
  the review feedback from the v1 thread. Renumbered in v2 order. The whole
  189-patch series still applies cleanly, and this is build-time only, so the
  runtime behaviour is unchanged from `pkgrel 5`.

### Noted, nothing to add
- **The Vernon Yang link** (`20260903031608.1194238-1-vernon2gm`) is a reply on
  the thread of `2500` (x86/mm `pmd_modify()` dropping the dirty bit) — it
  just accepts the `Reported-by:` trailer Andrew Morton added. No new patch.
- **linux-next `next-20260914` is out**, and it is the 7.4 merge-window preview
  (455 display files changed, 33k insertions; mm +5.4k lines). Per this
  project's policy linux-next is a preview base, not a patch source mid-RC.
  The only delta in `crypto/zstd.c` is the workspace series already carried as
  `2148`/`2149`. Nothing worth backporting onto 7.3-rc3.

## [7.3.0-rc3-5-sleepy-next]: 2026-09-14

### Removed
- **`1144`** (drm/amd/display: Enable HDMI FRL by default). This is a bisect
  step aimed at the MSI MAG251RX 240 Hz flicker, not a value judgement on the
  patch itself.

  The evidence chain that made it the first variable to test:

  - The user A/B-tested: the cachyos-rc kernel (rc2-based) is flicker-free at
    240 Hz, this kernel flickers, and 144 Hz works. Something in this kernel's
    delta is the cause.
  - Captured from the good kernel: `amdgpu.dcfeaturemask=2`. Ours was `0x402`.
    The extra bit is `DC_FRL_MASK`, added by this patch.
  - CachyOS reverted the same change twice in their 7.3 branches
    (`cc29db585c84`, `143e44f57bf8`), both by their maintainer with no reason
    stated, and the change is implicated in open upstream work item #5649
    (HDMI FRL blanking).

  Ruled out before this move: rc3's display commits versus rc2 (all benign), the
  FRL status-polling workqueue (inert without a trained FRL link), FBC (off on
  both kernels), the display driver configuration (identical between the two
  kernels apart from the command line and the NAP governor), and passive VRR
  (the good kernel has it *on* and is fine, so it cannot be the cause).

  Dropping the patch restores the upstream default mask of exactly 2, the
  known-good value. If the flicker persists on this build, the next suspect is
  the baked command line (`cpuidle.governor=nap`).

## [7.3.0-rc3-4-sleepy-next]: 2026-09-14

### Changed
- **`amdgpu.dcdebugmask=0x800` (DC_DISABLE_IPS) is back in the baked command
  line.** It was removed in `pkgrel 11` because the display "box" turned out to
  be a COSMIC overlay-plane bug rather than an IPS one. That is still true of the
  box — but the IPS gap is a separate, real artifact, and this machine shows it.

  `dc_get_flip_pending_on_otg()` reads `hubp2_is_flip_pending()`, which returns
  false while the HUBP is clock-gated, so flip completion can be delivered
  before the hardware latches and the compositor repaints a buffer that is still
  being scanned. Leo Li's own comment in `f64a9be56536` concedes it: *"DCN HUBP
  may be clock-gated, so the flip-pending status may be undefined"*.

  The MSI MAG251RX flickers exactly where that bites. Cursor movement is the
  most frequent source of flips, which is why the artifact is severe under the
  cursor and mild when idle, and why it is **independent of VRR** — every VRR
  knob, including disabling passive VRR, changed nothing. `1159` fixed the
  software half of the race (the non-atomic read-modify-write that clears
  `VUPDATE_NO_LOCK_EN`); this mask covers the clock-gating half, which is
  hardware. It costs idle power, and should be dropped again if a proper DCN4
  flip-pending fix lands.

  **This is a hypothesis under test, not a proven fix.** The passive-VRR
  diagnosis in `pkgrel 2` was wrong: the fix applied cleanly — both CRTCs read
  `PASSIVE_VRR_DISABLED=1` — and the flicker persisted. Two related things were
  established while re-diagnosing: the MSI runs 1920x1080@239.96Hz at a 571 MHz
  pixel clock on HDMI-A-2 (legal against HDMI 2.0's 600 MHz TMDS ceiling, but
  near the top of it), and the kernel logs **no runtime display errors at all**.
  The only complaints are at boot: a `REG_WAIT` timeout in
  `optc401_disable_crtc`, and an InfoFrame failure on HDMI-A-1 — the *other*
  monitor, not the MSI.

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
  already `2128` and `2143` — and it **conflicts with both**, so carrying it
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

### Decision recorded — `1144` is kept
The MAG251RX is **HDMI 2.0 and DP 1.2a**, so `1144` ("Enable HDMI FRL by
default") is inert on the hardware: FRL is an HDMI 2.1 feature. It is
bit-identical to the change CachyOS reverted with no stated reason, and it is
implicated in open upstream work item #5649 (HDMI FRL blanking). Removing it
was considered and **declined on 2026-09-14**: being inert, removing it buys
nothing measurable today, and the 7.4 bump replaces this area with drm-next's
reworked VSDB/FRL handling anyway. Revisit then rather than re-arguing it.

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
