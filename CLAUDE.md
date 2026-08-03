# sleepy-kernel

Custom Arch Linux kernel package based on Linux mainline RC releases, built for
a single AMD Zen 4 + RDNA 4 desktop. Uses a sanitized CachyOS patchset as the
base, with additional upstream and local patches filtered to this hardware.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | AMD Ryzen 9 7950X (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| NIC | Realtek RTL8125B 2.5 GbE | `r8169` (in-kernel driver, since 7.2) |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline` |
| Scheduler | sched-ext BPF schedulers | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

**If a patch does not target one of these components, it does not go in.**

## Documentation

| File | Purpose |
|---|---|
| `GUIDE.md` | End-user README: target audience, differences from vanilla, build instructions, PROFILE_PEAK explanation |
| `PATCH_SOURCES.md` | Per-patch provenance ledger with authors, commit hashes, and source URLs |

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch Linux build script |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `00xx-*.patch` | Handmade local patches (Sleepy/Antigravity) and upstream ML patches not yet landed |
| `0101-cachy-bbr3.patch` | CachyOS `bbr3` — BBR3 TCP congestion control (squashed) |
| `0102-cachy-kbuild.patch` | CachyOS `cachy` — kbuild `-O3` (squashed) |
| `0103-cachy-cpu-isa.patch` | CachyOS `cachy` — x86\_64 ISA/Zen4 optimizations (squashed) |
| `0104-cachy-cgroup-vram.patch` | CachyOS `cgroup-vram` — VRAM cgroup accounting (drm/ttm) (squashed) |
| `0105-cachy-fixes.patch` | CachyOS `fixes` — full 26-patch branch, incl. off-target hardware (squashed) |
| `0106-cachy-drops.patch` | Reverts off-target `fixes` (i915, btusb, rtw89, touchpad, laptop audio, SOF, iwlwifi, nouveau, DisplayID eDP) |
| `0107-cachy-hdmi.patch` | CachyOS `hdmi` — HDMI 2.1 FreeSync/VRR/PCON refactor, excl. `0151` (squashed) |
| `0108-cachy-preempt-ipi.patch` | CachyOS `preempt-ipi` v3 — SMP preemption + TLB flush (squashed) |
| `0109-cachy-vesa-dsc.patch` | CachyOS `vesa-dsc-bpp` — EDID DSC BPP parsing + AMD consumer (squashed) |
| `10xx-*.patch` | AMDGPU GPU core: GFX12, GMC, SDMA, PSP, TTM, TLB |
| `11xx-*.patch` | AMD Display: DCN4, DCN42B, PSR, pstate quirk, MCIF ARB |
| `12xx-*.patch` | AMD Power Management: amd-pstate, cpufreq |
| `20xx-*.patch` | Block / I/O schedulers: bfq, mq-deadline |
| `21xx-*.patch` | Memory management: zstd, LRU-MARIE |
| `22xx-*.patch` | CPU idle: NAP governor |
| `90xx-*.patch` | Upstream dev-tree backports from agd5f/linux |
| `net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `repos/` | Cloned upstream git repos for patch extraction |
| `src/`, `pkg/` | Build artifacts — never commit |

**Deleted files (do not recreate):** `cake-sqm.sh`, `cake-sqm.service`, `sqm-qos/`, `net-latency/` (replaced by the unified `net-tune/` service).

## Patch numbering

| Range | Category | Source / How to obtain |
|---|---|---|
| `0001–0049` | Handmade local patches (Sleepy/Antigravity) | SMU14, DCN401, GFX12 hand-written fixes for this hardware |
| `0050–0099` | Upstream EDID/display ML patches not yet landed | `b4` mbox or mbox from freedesktop archives — verify with `git apply --check` against the current clean tree (`repos/linux-7.2-rc6`) |
| `0101` | CachyOS `bbr3` (squashed) | Apply `bbr3-cachyos-patches-sep/` in order, emit cumulative `git diff` |
| `0102` | CachyOS `cachy` kbuild (squashed) | `kbuild-cachyos-patches/` |
| `0103` | CachyOS `cachy` cpu-isa (squashed) | `cpu-cachyos-patches/` |
| `0104` | CachyOS `cgroup-vram` (squashed) | `cgroup-patches-sep/` |
| `0105` | CachyOS `fixes` (squashed, full branch incl. off-target) | `cachyos-fixes-patches-vN-sep/` |
| `0106` | CachyOS `drops` (reverts off-target `fixes` groups) | Reverse diff of the off-target hunk groups in `0105` |
| `0107` | CachyOS `hdmi` (squashed, excl. `0151`) | `hdmi-patches-sep/` — exclude `0151` (HF-VSDB conflicts with `0055`) |
| `0108` | CachyOS `preempt-ipi` (squashed) | `preempt-ipi-patches-v3-sep/` |
| `0109` | CachyOS `vesa-dsc-bpp` (squashed) | `vesa-patches-sep/` |
| `1000–1099` | AMDGPU GPU core | GFX12, GMC, SDMA, PSP, TTM, TLB from agd5f/linux or drm-next |
| `1100–1199` | AMD Display | DCN4, DCN42B, PSR, Replay, pstate quirk, MCIF ARB from drm-next |
| `1200–1299` | AMD Power Management | amd-pstate, cpufreq from linux-pm or sirlucjan |
| `2000–2099` | Block / I/O schedulers | bfq, mq-deadline from sirlucjan `block-patches-sep/` |
| `2100–2199` | Memory management | zstd, LRU-MARIE from sirlucjan |
| `2200–2299` | CPU idle | NAP governor from sirlucjan `nap-patches/` (firelzrd's repo is BORE-only) |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux — **verify all symbols exist in rc mainline first** |

All sirlucjan directories are under `repos/sirlucjan-kernel-patches/7.2-rc/`.

**CachyOS branch workflow** (use `patch-cachy-branches` skill):
1. Identify the latest `-sep` subdirectory for each branch in `repos/sirlucjan-kernel-patches/7.2-rc/`
2. For the `fixes` branch: squash the FULL branch into `0105-cachy-fixes.patch`, then revert the off-target groups (i915, btusb, rtw89, laptop audio, i2c touchpad, iwlwifi, SOF Intel, nouveau, DisplayID eDP) in `0106-cachy-drops.patch`. Net effect = only the 10 hardware-relevant fixes remain. See the skills file for the full off-target list.
3. Squash each branch: apply its `-sep` patches **in order to the actual series tree** (rc6 + the `0001`–`0058` local/upstream patches, since those touch shared files like `drm_edid.c`), delete `.orig`/`.rej` leftovers, then emit the cumulative `git diff` as one `format-patch` per branch.
4. The CachyOS `hdmi` branch (squashed as `0107`) replaces the old `0051`/`0052` FreeSync patches — do not add both.
5. The `hdmi` squash **excludes `0151`** (`drm-edid-Parse-more-info-from-HDMI-Forum-vsdb`): if `0055` (Fangzhi Zuo HF-VSDB) is in the series, `0151` adds identical content to `drm_edid.c`/`drm_connector.h` and shows as "already applied" — drop it before squashing.

Workflow: identify category → next unused number in that range → `NNNN-short-description.patch`
→ `git apply --check` against `repos/linux-7.2-rc5` (clean tree) → add to `source=()` → `updpkgsums` → document in `PATCH_SOURCES.md`.

---

## Full maintenance cycle

When asked to update the kernel ("update to 7.3-rc1", "bump to the latest RC"),
run all three phases in order without waiting for the user to ask for each one:

1. **Version bump** — update `_major`, `_minor`, `_rcver`, `_srcname` in PKGBUILD.
   Rebase every patch with `patch --dry-run`. Regenerate the CachyOS squashed branch patches (`0101`–`0109`) from latest sirlucjan `-sep` directories
   (keep a branch's squash unchanged when its content is identical and it still applies cleanly — only `fixes`/`drops` usually drift).
   Report every patch dropped or regenerated, and why, before going further.
2. **Patch audit** — check all six sources (drm-next, linux-next, linux-pm,
   amd-gfx mailing list, dri-devel mailing list, sirlucjan) for anything new.
   List candidates with source and priority before adding any.
3. **Build and fix** — `rm -rf src pkg && makepkg -f -s -c`. On failure, diagnose
   and fix per the rules below. Keep iterating until the build succeeds or a
   MUST NOT rule blocks you.

A request for "check for new patches" is phase 2 alone.
A request for "build it" is phase 3 alone.

---

## YOU MUST

1. **Compile with `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`.** The PKGBUILD downloads
   a pre-built LLVM toolchain from kernel.org. Never change the toolchain.
2. **`rm -rf src pkg` before every build.** Old patched files cause false conflicts.
3. **`updpkgsums` after any `source=()` change.** Checksums must match 1:1.
4. **Keep every patch's original `From:`/`Date:`/`Subject:`/`Signed-off-by:` headers intact.**
5. **`patch --dry-run -Np1 < ../patchfile.patch` before adding any patch.**
6. **Resolve conflicts yourself** — fix hunk offsets, regenerate from source, or drop
   the patch. Don't stall waiting on the user.
7. **Clone with `--shallow-since="YYYY-MM-DD"` — never `--depth=1`.** `--depth=1` strips
   commit history, making `git log --grep` useless.
8. **Document every new patch in `PATCH_SOURCES.md` before adding it to `PKGBUILD`.**
9. **Verify BTF after every build.** Both `CONFIG_TCP_CONG_BBR` (old) and `CONFIG_TCP_CONG_BBR3`
   define the same BTF kfunc symbol. Only one can be built-in. The old BBR must stay disabled.
10. **Use `DEBUG_INFO_DWARF5` (not `DWARF_TOOLCHAIN_DEFAULT`) with Clang 23 + pahole 1.31.**
    `DWARF_TOOLCHAIN_DEFAULT` with Clang 23 produces DWARF output that pahole 1.31 cannot
    convert to BTF, causing `Failed to generate BTF for vmlinux`.

## YOU MUST NOT

1. **Never use `ld.mold`** — crashes on kernel vDSO linker scripts (`fatal: unknown linker script token SECTIONS`).
2. **Never access `lore.kernel.org`** — anti-bot protection blocks automated agents. Use git
   repos or `lists.freedesktop.org` archives instead.
3. **Never hand-write or fabricate a patch diff.** No traceable commit or mailing list
   submission → tell the user, don't invent one.
4. **Never add patches for hardware we don't have** (Intel/Nvidia GPUs, ARM/SoC, Apple T2,
   laptop amps, TV tuners).
5. **Never clone into `/tmp`** — use `repos/` in the workspace.
6. **Never run `make menuconfig`/`nconfig`** unless the user explicitly asks.
7. **Never remove a patch** without explicit user approval, even if it looks irrelevant.
8. **Never use `8.8.8.8`** in network scripts — use Quad9 (`9.9.9.9`).
9. **Never set `LLVM` to a path** (e.g. `LLVM=/path/to/bin/`). The kernel's
   `tools/bpf/resolve_btfids/Makefile` checks `ifeq ($(LLVM),1)`. A path value
   breaks BTF ID resolution. Instead, prepend the LLVM `bin/` to `$PATH` and set `LLVM=1`.

---

## Build failure triage

### BTF failures (`Failed to generate BTF for vmlinux`)

This is the most common failure. Check in this order:

1. **Duplicate BTF kfunc symbol**: Both `tcp_bbr.c` and `tcp_bbr3.c` define
   `BTF_KFUNCS_START(tcp_bbr_check_kfunc_ids)`. If both are built-in,
   `resolve_btfids` exits 255 silently. Fix: `scripts/config -d TCP_CONG_BBR`
   **after** `olddefconfig` (which can re-enable it via dependency resolution).
2. **DWARF format mismatch**: Clang 23 with `DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT`
   produces DWARF output that pahole 1.31 cannot parse. Fix:
   `scripts/config -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5`.
3. **LLVM path vs boolean**: If `LLVM` is set to a directory path instead of `1`,
   `resolve_btfids` skips compilation. Fix: set `LLVM=1` and prepend LLVM bin to `$PATH`.
4. **Missing pahole**: `sudo pacman -S pahole` (package name: `dwarves`).

### Patch application failures

1. Read the `.rej` file: `cat src/linux-*/path/to/file.c.rej`
2. Already applied by a CachyOS branch squash (`01xx`) or a `10xx` patch → remove the conflicting patch.
3. Context lines shifted → regenerate from source repo with `git format-patch`.
4. `vm_swappiness` collision → strip the `CONFIG_CACHY` override from the relevant CachyOS branch squash (see below).

### Linker failures

- `ld.mold` error → force back to `ld.lld` in PKGBUILD.
- `ld.lld: error: undefined symbol` in vDSO → ensure the custom LLVM bin is on `$PATH`.

---

## CachyOS per-branch patch refresh

**Do not use the old mega-patch approach.** Use the `patch-cachy-branches` skill instead.

The CachyOS patchset is now sourced as individual per-branch `-sep` files from sirlucjan's repo, then **squashed to one patch per branch** (`0101`–`0109`, plus `0106-cachy-drops` as the off-target filter). Squashing keeps `source=()` short (9 files instead of 87) while still allowing per-branch exclusion.

### Branch selection (7.2-rc)

| Branch | sirlucjan directory | Squash patch | Keep? | Notes |
|--------|---------------------|--------------|-------|-------|
| `bbr3` | `bbr3-cachyos-patches-sep/` | `0101` | ✅ | Always |
| `cachy` | `kbuild-cachyos-patches/` + `cpu-cachyos-patches/` | `0102` + `0103` | ✅ | O3 + Zen4 |
| `cgroup-vram` | `cgroup-patches-sep/` | `0104` | ✅ | VRAM cgroups for RDNA4 |
| `fixes` | `cachyos-fixes-patches-vN-sep/` | `0105` + `0106` | ✅ | `0105` = full 26-patch branch; `0106` reverts off-target (i915, btusb, rtw89, laptop audio, i2c touchpad, iwlwifi, SOF Intel, nouveau, DisplayID eDP) |
| `hdmi` | `hdmi-patches-sep/` | `0107` | ✅ | Full HDMI VRR/FreeSync series, excl. `0151` |
| `preempt-ipi` | `preempt-ipi-patches-v3-sep/` | `0108` | ✅ | SMP/TLB quality |
| `vesa-dsc-bpp` | `vesa-patches-sep/` | `0109` | ✅ | DSC BPP for our monitors |
| `snd-codecs` | any | — | ❌ | Samsung/Razer/Lenovo laptop audio — we have no laptops |
| `t2` | any | — | ❌ | Apple T2 Mac |
| `adios-iosched-default-on` | any | — | ❌ | Conflicts with sched-ext |
| `gaming-sched` | any | — | ❌ | Conflicts with sched-ext |
| `clang-patches` | any | — | ❌ | LLVM Polly — miscompilation risk |

### Squash workflow (one patch per branch)

Each `0101`–`0109` patch is the cumulative `git diff` of one branch's `-sep` patches applied **in order to the actual series tree** (rc6 + the `0001`–`0058` local/upstream patches). The pre-CachyOS patches matter — e.g. `0055` modifies `drm_edid.c` before the `hdmi` branch is applied, so each squash must be generated against that tree state, not a clean rc6.

```bash
# From a tree at the correct series state (rc6 + 0001–0058):
for f in "$BASE/cachyos-fixes-patches-vN-sep"/*.patch; do
  patch -p1 --forward < "$f"          # apply branch patches in order
done
find . -name '*.orig' -delete         # patch leaves .orig/.rej backups — never commit them
find . -name '*.rej' -delete
git diff --binary > 0105-cachy-fixes.patch   # cumulative diff = the squash
```

Verify each squash with `git apply --check 01xx-cachy-*.patch` against a clean `repos/linux-7.2-rc5`. `0106-cachy-drops.patch` is the reverse diff of the off-target hunk groups from `0105`; its net effect is that only the 10 hardware-relevant fixes remain applied.

### Conflict check when building the hdmi squash

The `hdmi` branch (squashed as `0107`) modifies `drm_edid.c` and `drm_connector.h`. If the Fangzhi Zuo HF-VSDB patch (`0055`) was applied first, the `0151` `drm-edid-Parse-more-info-from-HDMI-Forum-vsdb` patch shows as "Reversed (already applied)" — **exclude `0151` from the `0107` squash**.

### vm_swappiness / LRU-MARIE conflict

The CachyOS `cachy` branch no longer contains a `vm_swappiness` override (removed upstream). If it reappears in a future version, strip the `mm/vmscan.c` hunk touching `vm_swappiness` before applying.

### vma_flags_t / VM_EXEC compile error

Sirlucjan's `fixes` branch (squashed into `0105-cachy-fixes.patch`; `mm: vmscan: convert folio_referenced() to use vma_flags_t`) renames `vm_flags` → `vma_flags` with type `vma_flags_t`. The LRU-MARIE patch (`2101`) contains a `#ifdef CONFIG_LRU_MARIE` block that still used the old `(vm_flags & VM_EXEC)` pattern. Fix the one line at the conflict site:

```c
// WRONG after the fixes squash (0105):
if (referenced_ptes > 0 && (vm_flags & VM_EXEC) && folio_is_file_lru(folio))

// CORRECT:
if (referenced_ptes > 0 && vma_flags_test(&vma_flags, VMA_EXEC_BIT) && folio_is_file_lru(folio))
```

This is an in-tree source edit to `mm/vmscan.c`, **not** a new patch file. Document it in PATCH_SOURCES.md under "Build fixes".

---

## Upstream patch sources (Detailed Fetch Guide)

Never scrape `lore.kernel.org` — its anti-bot protection blocks automated access.

### 1. `drm-next` (AMD GPU / Display / SMU / RDNA 4)
- **Repo**: `https://gitlab.freedesktop.org/drm/kernel.git` (branch `drm-next`)
- **Fetch & Search**:
  ```bash
  cd repos/drm-next && git fetch origin
  git log --oneline --grep="gfx12\|navi48\|dcn4\|smu14\|psp14\|mmhub_4\|sdma_v7\|vcn_v5\|dcn42b" origin/drm-next
  ```
- **Extract**: `git format-patch -1 <commit_hash> -o ../../` (save as `20xx-*.patch`)

### 2. `linux-next` (Mainline Integration Tree)
- **Repo**: `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git`
- **Fetch & Search**:
  ```bash
  cd repos/linux-next && git fetch origin
  git log --oneline --grep="gfx12\|navi48\|dcn4\|smu14\|amd_pstate\|MZEN4\|CPPC" origin/master
  ```
- **Extract**: `git format-patch -1 <commit_hash> -o ../../` (save as `20xx-*.patch`)

### 3. `linux-pm` (CPU Freq / Power / Zen 4 amd-pstate)
- **Repo**: `https://git.kernel.org/pub/scm/linux/kernel/git/rafael/linux-pm.git`
- **Fetch & Search**:
  ```bash
  cd repos/linux-pm && git fetch origin
  git log --oneline --grep="amd-pstate\|amd_pstate\|CPPC\|k10temp\|epp_boost" origin/master
  ```
- **Extract**: `git format-patch -1 <commit_hash> -o ../../` (save as `20xx-*.patch`)

### 4. `amd-gfx` & `dri-devel` Mailing Lists
- **Archives**: `https://lists.freedesktop.org/archives/amd-gfx/` and `https://lists.freedesktop.org/archives/dri-devel/`
- **Fetch & Search**: Parse monthly thread HTML (`YYYY-Month/thread.html`) for subject keywords. Download target thread mbox.

### 5. `sirlucjan` (Third-Party Performance Patches)
- **Repo**: `https://github.com/sirlucjan/kernel-patches.git`
- **Fetch**: `cd repos/sirlucjan-kernel-patches && git pull`
- **Audit**: Inspect `7.2-rc/` directories (`lru-marie-patches-v10/`, `zstd-dev-patches/`, `block-patches-sep/`).

### 6. `firelzrd` (BORE / NAP Governor Patches)
- **Repo**: `https://github.com/firelzrd/bore-scheduler.git`
- **Fetch**: `cd repos/firelzrd-bore-scheduler && git pull`
- **Audit**: Inspect `nap-patches/` for `1084-7.2-nap-v0.5.0.patch` updates.

---

## Kconfig reference

Key `scripts/config` calls in `prepare()` (already in the PKGBUILD):

```bash
# CPU
scripts/config -d GENERIC_CPU -e MZEN4

# Compiler
scripts/config -d LTO_NONE -e LTO_CLANG_THIN
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3

# TCP congestion (BBR3 only — old BBR causes BTF symbol collision)
scripts/config -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 --set-str DEFAULT_TCP_CONG "bbr3"

# Kernel command line (appended to bootloader params, does not override)
scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1 elevator=kyber" -d CMDLINE_OVERRIDE

# BTF / debug (Clang 23 requires DWARF5, not DWARF_TOOLCHAIN_DEFAULT)
scripts/config -e DEBUG_KERNEL -d DEBUG_INFO_NONE -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5 -e DEBUG_INFO_BTF

# BPF infrastructure (bpftune, sched-ext)
scripts/config -e BPF_SYSCALL -e BPF_TRACING -e BPF_EVENTS -e BPF_KPROBE_OVERRIDE \
               -e KPROBES -e KPROBE_EVENTS -e UPROBES -e UPROBE_EVENTS \
               -e KALLSYMS -e KALLSYMS_ALL \
               -e FTRACE -e FTRACE_SYSCALLS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER

# Memory management
scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE
scripts/config -e CPU_IDLE_GOV_NAP

# CAKE SQM ingress
scripts/config -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32

# Bloat removal
scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU
scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN
scripts/config -d SECURITY_APPARMOR -d AUDIT -d AUDITSYSCALL
```

After `olddefconfig`, disable these again (dependency resolution re-enables them):
```bash
scripts/config -d TCP_CONG_BBR       # BTF symbol collision with BBR3
scripts/config -d CHROMEOS_PRIVACY_SCREEN
scripts/config -d VIRT_DRIVERS
scripts/config -d PCI_TSM
scripts/config -d VIRTIO_FS
scripts/config -d X86_PLATFORM_DRIVERS_UNIWILL
```

---

## net-tune service (CAKE SQM + latency tuning)

`net-tune/` ships one systemd service that applies low-latency ethernet
settings (`ENABLE_LATENCY`) and, optionally, CAKE SQM shaping (`ENABLE_SQM`),
each independently toggleable in `/etc/net-tune.conf`. BBR3 is the
kernel-compiled default (`CONFIG_DEFAULT_TCP_CONG="bbr3"`); the SQM part does
**not** set BBR3 via sysctl — it only applies CAKE traffic shaping.

The PKGBUILD prompts interactively during `prepare()`. When no TTY is attached
(CI, piped input), it silently skips. To pre-seed non-interactively (before
running makepkg, after `mkdir -p src`):

```bash
mkdir -p src
cat > src/net-tune.conf << EOF
ENABLE_SQM=yes
DOWNLOAD_MBIT="80"
UPLOAD_MBIT="85"
ENABLE_LATENCY=yes
EOF
touch src/.enable_sqm
```

The route-detection probe uses Quad9 (`9.9.9.9`), never `8.8.8.8`.

---

## Lessons learned — do not repeat

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
| Reversed patch 1025 (PSR on DCN4) without documenting | Causes desktop freezes on RDNA 4 | Reverse-apply is in `prepare()` |
| Applied patch 1031 (DCN4 pstate enable) | Forced broken UCLK switching, causing freezes unless `profile_peak` was used | Patch `1101` is now reverse-applied in `prepare()` to keep `.pstate_enabled = false`. Check the reverse-apply line matches the current patch filename when renumbering. |
| Applied patch 1033 (DCN42b uclk increase) | Distorted DML2.1 latency calculations in low DPM states | Patch was audited and found safe to keep applied — the concern was unfounded. Only `1101` is reversed. |
| Backported agd5f staging patch 2008 | Referenced `amdgpu_userq_process_reset_irq` and `AMDGPU_CTXID0_DOORBELL_ID_MASK` which exist only in `agd5f/linux amdgpu_userq.h` but **not in Linux 7.2-rc5 mainline** — caused `undeclared identifier` compile errors | Before adding any `2xxx` patch, `grep -r <new_symbol> src/linux-*/drivers/` to confirm all referenced functions and macros exist in the current mainline tree. If missing, the patch depends on staging infrastructure and must be dropped. |
| 0xxx patches had gaps (0013–0015 missing) | Caused confusing jump from 0012 → 0016 with no explanation | Always use the next consecutive number in the correct category range. Renumbering after-the-fact requires: rename files, update `source=()`, run `updpkgsums`, update `PATCH_SOURCES.md`, update `CLAUDE.md`, update `README.md`, update any `prepare()` reverse-apply lines. |
| All 1xxx patches in one undifferentiated range | Mixed GPU core, display, power management, block, MM, and cpuidle into one range — impossible to tell category from number alone | Use the category-based subcategory scheme: `1000–1099` GPU core, `1100–1199` display, `1200–1299` PM, `2000–2099` block, `2100–2199` MM, `2200–2299` cpuidle, `9000–9099` agd5f staging. |
| Used monolithic CachyOS mega-patch | Single 900 KB diff caused FreeSync collision with upstream hdmi branch; impossible to exclude off-target patches | Switch to sirlucjan per-branch `-sep` files squashed to one patch per branch (`0101`–`0109`). Off-target branches (`snd-codecs`, `t2`, etc.) are never squashed; off-target patches inside `fixes` are reverted by `0106-cachy-drops`. |
| Added `0151` (HDMI HF-VSDB) when `0055` was already applied | `0151` adds the same `drm_hdmi_vrr_cap` struct as `0055` (Fangzhi Zuo 2/4). Patch shows as "Reversed" at apply time. | If `0055` is in the series, exclude `0151` from the `0107-cachy-hdmi` squash. The two patches add identical content to `drm_edid.c` and `drm_connector.h`. |
| Applied `0053` (remove DMCU parser) before CachyOS hdmi branch | `0053` deletes `dc_edid_parser.h`. The CachyOS hdmi branch still includes `amdgpu_dm.c` which includes that header. Compile fails with "file not found". | When the CachyOS hdmi branch is present, drop `0053`. The DMCU parser cleanup is moot because the hdmi branch already refactored the callers. |
| Attempted to backport Fangzhi Zuo 1/4, 3/4, 4/4 (HDMI FRL patches) | These patches target `amdgpu_dm_connector.c` which was split from `amdgpu_dm.c` by Alex Hung (agd5f `0e967e086e75`) in April 2026. That split is not in rc5. | Defer until the `amdgpu_dm_connector.c` split lands in mainline (expected 7.3). Only `0055` (2/4, touches `drm_edid.c` only) and `0058` (FRL cap restore) are safe to add now. |
| `vm_flags & VM_EXEC` in LRU-MARIE after `fixes` branch applied | Sirlucjan `fixes` branch (squashed in `0105`) renames `vm_flags` → `vma_flags` with new type `vma_flags_t`. LRU-MARIE's `#ifdef CONFIG_LRU_MARIE` block still used the old `(vm_flags & VM_EXEC)` expression — compile error: invalid operands to binary expression. | In-tree fix: change `(vm_flags & VM_EXEC)` to `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` in `mm/vmscan.c` inside the `CONFIG_LRU_MARIE` block. This is an in-tree source edit, not a patch file. **Update (2026-08-03, rc6): no longer required — LRU-MARIE v12 (`2101`) already ships the `vma_flags_test(&vma_flags, VMA_EXEC_BIT)` form.** |
| `amdgpu_dm_connector.c` split required by upstream HDMI patches | Fangzhi Zuo's July 2026 HDMI series was written against agd5f tree where `amdgpu_dm.c` was split. Applied against rc5 (no split) → "No such file or directory" error. | Check `find repos/linux-7.2-rcN -name "amdgpu_dm_connector.c"` before applying any patch targeting that file. If absent, defer the patch. |
| DCN401 GPIO lookup table patch (`334cbfa3c`) fails to compile | `drm/amd/display: convert dcn401 GPIO translation to lookup tables` uses `DC_GPIO_GENERIC_A`, `DC_GPIO_HPD_A`, etc. which come from a prerequisite GPIO infrastructure patch not in rc5. | Verify all symbol names used in a patch exist in the tree: `grep -r "DC_GPIO_GENERIC_A" src/linux-*/drivers/gpu/drm/amd/`. If absent, the patch depends on staging prerequisites and must be dropped. |
| `git apply --check` better than `patch --dry-run` | `patch --dry-run` treats mbox-format patches differently and reports false "corrupt patch" errors. `git apply --check` handles both `git format-patch` and mbox formats correctly. | Use `git apply --check <file>` for dry-run testing. Use `git apply --check -R <file>` to test if a patch is already applied (reverse check). |
| `.orig`/`.rej` files from `patch` got committed into squashed patches | `patch` leaves `.orig`/`.rej` backup files next to modified sources; `git add -A` swept them into the squashed CachyOS patches as garbage hunks | Always `find . -name '*.orig' -delete; find . -name '*.rej' -delete` before `git add -A` when generating squashed patches |
| Editing a patch's commit-message body changed its BLAKE2 checksum | Rewriting the 11 handmade patch descriptions (message bodies) invalidated their `b2sums`, so `makepkg` failed the source-validity check | Run `updpkgsums` after ANY change to a `.patch` file — not just `source=()` edits — then re-verify the full series applies |
| `-m V4L2_LOOPBACK` in `prepare()` did nothing | `v4l2loopback` is an out-of-tree module, not a kernel config symbol; `scripts/config -m V4L2_LOOPBACK` is silently dropped by `olddefconfig` | For UVC webcams (incl. Android USB-webcam mode) enable the in-kernel driver instead: `-m USB_VIDEO_CLASS` (uvcvideo). v4l2loopback is installed via AUR (`v4l2loopback-dkms`) when needed |
| Dropped the out-of-tree `r8125` module | The custom Realtek module blacklisted `r8169`; after removing it the NIC had no driver because `CONFIG_R8169` was not enabled | The in-kernel `r8169` covers the RTL8125B — when dropping `r8125`, set `_build_r8125=no` AND enable `-m R8169` in `prepare()` |
| `disable_configs.py` cannot disable symbols that are `select`ed | `RESCTRL_FS` (AMD resctrl) and `SND_INTEL_NHLT` (HDA/audio) came back after `olddefconfig` because another option hard-`select`s them | For `select`-forced symbols, disable the selector (e.g. `X86_RESCTRL`) instead, or accept the tiny bloat; verify the built `.config` after each build |
| CAKE flow-isolation directions are easy to get backwards | egress (upload) must use `dual-srchost`, ingress (download) `dual-dsthost` (per tc-cake(8)); a first draft had them swapped | Use `tc qdisc replace` and follow tc-cake(8): egress `dual-srchost nat ack-filter`, ingress `dual-dsthost wash nat`, with `rtt regional` and `overhead ethernet` for a direct Ethernet handoff |
| A clean `git apply --check -R` on a candidate means it is ALREADY in the base tree | Sweeps kept re-proposing `f8ee6447e`, `7e1b4bdb0`, etc. that were already in rc5 | Treat a clean reverse check as "already in rc5" — record it and do not add it; only add candidates where the forward check is clean and the reverse check fails |
| cdn.kernel.org lagged the rc6 tag | `updpkgsums` 404'd on `cdn.kernel.org/pub/linux/kernel/v7.x/testing/linux-7.2-rc6.tar.gz` right after the tag was cut — the cdn mirrors RC tarballs late | Use `https://git.kernel.org/torvalds/t/linux-<tag>.tar.gz` in `source=()` when the cdn 404s |
| gitlab.freedesktop.org persistent HTTP 503 | `drm-next` and `amd-staging-drm-next` fetches failed with `RPC failed; HTTP 503` for hours, blocking the sweep | Don't block the cycle: cover drm-next via `linux-next` and the AMD staging branch via `agd5f-linux`, and retry gitlab in the background |
| `patch` leaves `.orig` backups in a git worktree | Regenerating the `01xx` squashes staged `.orig` backups created by `patch`, and they leaked into the squash as huge bogus deletions (`0105` ballooned 51 KB → 628 KB) | `find . -name '*.orig' -delete; find . -name '*.rej' -delete` after EVERY patch phase, before `git add`/`git diff` |
| Overlapping local patches pass `git apply` only in isolation | `0003` and `0004` both edit `smu_v14_0.c` near PROFILE_PEAK; strict `git apply` fails on `0004` after `0003`, but `patch -p1 --forward` applies it with fuzz (offset 2) | Generate and validate squashes with `patch -p1 --forward`, exactly as `prepare()` does — strict `git apply` misreports fuzz-tolerable sequences |
| Regenerated every 01xx squash on a bump, then only fixes/drops needed it | sirlucjan branch content was identical (repo master at 2026-07-31) and `0101`–`0104`/`0107`–`0109` applied cleanly to rc6; only `0105`/`0106` had drifted | On a bump, regenerate only the 01xx squashes that fail `git apply --check`; keep unchanged + clean-applying ones |

---

## Version string

```bash
echo "-$pkgrel" > localversion.10-pkgrel
echo "-${pkgbase#linux-}" > localversion.20-pkgname
scripts/config --set-str LOCALVERSION ""
```

Result: `uname -r` → `7.2.0-rc6-1-sleepy`

## Local model routing

When running with a local LLM server (not the hosted Anthropic API):

- `.claude/settings.json` sets `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`,
  `ANTHROPIC_MODEL`, `ANTHROPIC_SMALL_FAST_MODEL`, and
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` in its `env` block.
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` prevents hard-stops from tokenizer drift
  between Claude Code and the local server.
- On compaction, preserve: the current patch series (number range + subject),
  its `PATCH_SOURCES.md` status, and any uncommitted diff.
- Push heavy one-shot work (cloning repos, diffing archives) into subagents.
- Compact deliberately at phase boundaries. Treat each version bump as its own session.
