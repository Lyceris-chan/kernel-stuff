# AGENT HANDOFF GUIDE: `sleepy-kernel` Build & Maintenance

**Read this entire document before doing anything.** This is the authoritative reference for building, updating, and maintaining the `sleepy-kernel` custom Arch Linux kernel package. It is written so that even a basic local LLM agent can follow it without mistakes.

---

## Table of Contents

1. [What This Project Is](#1-what-this-project-is)
2. [Absolute Rules (DO and DO NOT)](#2-absolute-rules)
3. [Target Hardware](#3-target-hardware)
4. [Repository Layout](#4-repository-layout)
5. [Patch Numbering Convention](#5-patch-numbering-convention)
6. [How to Build the Kernel (Step-by-Step)](#6-how-to-build-the-kernel)
7. [How to Update to a New Kernel Version](#7-how-to-update-to-a-new-kernel-version)
8. [How to Generate the CachyOS Mega-Patch](#8-how-to-generate-the-cachyos-mega-patch)
9. [How to Ingest Upstream Patches](#9-how-to-ingest-upstream-patches)
10. [How to Audit Third-Party Patches](#10-how-to-audit-third-party-patches)
10.5 [Patch Source Integrity and New Patch Checklist](#105-patch-source-integrity-and-new-patch-checklist)
10.6 [bpftune Requirements Verification](#106-bpftune-requirements-verification)
10.7 [Lessons Learned — Mistakes to Avoid](#107-lessons-learned-mistakes-to-avoid)
11. [Kbuild Configuration Reference](#11-kbuild-configuration-reference)
12. [SQM QoS and BBR3 Service](#12-sqm-qos-and-bbr3-service)
13. [Debugging Build Failures](#13-debugging-build-failures)
14. [Common Mistakes to Avoid](#14-common-mistakes-to-avoid)

---

## 1. What This Project Is

This is a custom Arch Linux kernel package (`linux-sleepy`) based on Linux mainline release candidates with:
- A sanitized subset of the CachyOS patchset (community performance patches)
- Bleeding-edge AMD GPU/CPU patches from upstream development trees
- Advanced memory management (LRU-MARIE) and CPU idle (NAP governor) patches
- Aggressive driver pruning to minimize kernel size for a specific desktop PC

The workspace is at: `/home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export/`

---

## 2. Absolute Rules

### YOU MUST:

1. **Use `clang` + `ld.lld` to compile.** The PKGBUILD already sets `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. Do not change this.
2. **Clean `src/` and `pkg/` before every build.** Run `rm -rf src pkg` before `makepkg`.
3. **Run `updpkgsums` if you add, remove, or modify ANY file in the `source=()` array.** This updates SHA256 checksums. If you skip this, `makepkg` will refuse to build.
4. **Keep every patch's original git headers intact.** Every `.patch` file must have its original `From:`, `Date:`, `Subject:`, and `Signed-off-by:` lines from the upstream author.
5. **Test patches with `patch --dry-run -Np1 < ../patchfile.patch`** inside the extracted kernel source tree before adding them to the PKGBUILD.
6. **Resolve patch conflicts yourself.** If a patch fails to apply, you MUST autonomously either fix the hunk offsets, regenerate the patch from its upstream source, or drop the conflicting patch. Do NOT stop and ask the user to fix it. Do NOT stall execution.
7. **Use `--shallow-since` instead of `--depth=1` when cloning repos.** `--depth=1` strips commit history, making `git log --grep` useless for finding patches. Always use `--shallow-since="YYYY-MM-DD"` to preserve enough history for searching.

### YOU MUST NOT:

1. **NEVER use `ld.mold` as the linker.** It crashes on kernel vDSO linker scripts with `fatal: unknown linker script token SECTIONS`. The only supported linker is `ld.lld`.
2. **NEVER access `lore.kernel.org` for any reason.** It has aggressive anti-bot/anti-scraping protections. Requests will be blocked, rate-limited, or return empty/truncated data. Use git repositories instead (see Section 9).
3. **NEVER hand-write, invent, or fabricate patch diffs.** Every patch must come from an actual git commit or mailing list submission by a real kernel developer. If you cannot find a patch for something, tell the user — do not create one.
4. **NEVER apply patches for hardware we don't have.** No Intel GPUs, no Nvidia, no ARM/SoC, no Apple T2, no laptop smart amps, no TV tuners. See Section 3 for our exact hardware.
5. **NEVER use `/tmp` for cloning git repositories.** It fills up on small tmpfs partitions. Use `sleepy-kernel-export/repos/` instead.
6. **NEVER run `make menuconfig` or `make nconfig` unless the user explicitly asks.** The PKGBUILD handles all config via `scripts/config` commands.

---

## 3. Target Hardware

This kernel is built for ONE specific machine. Every config decision and patch selection is based on this hardware:

| Component | Exact Hardware | Kernel Identifiers |
|-----------|---------------|-------------------|
| **CPU** | AMD Ryzen 9 7950X (Zen 4, Family 19h) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| **GPU** | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| **NIC** | Realtek RTL8125 2.5GbE | `r8125` (out-of-tree module in `r8125/` directory) |
| **NVMe** | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline` block schedulers |
| **Scheduler** | sched-ext BPF schedulers | `CONFIG_SCHED_CLASS_EXT=y` |
| **CPUIdle** | NAP governor (Neural Adaptive Predictor) | `CONFIG_CPU_IDLE_GOV_NAP=y`, boot param `cpuidle.governor=nap` |

**If a patch does not target one of the above components, do not include it.**

---

## 4. Repository Layout

Here is what every file and directory in the repository does:

### Core Build Files
| File | Purpose |
|------|---------|
| `PKGBUILD` | The Arch Linux package build script. This is the main file that controls everything. |
| `config` | The base kernel `.config` file (derived from CachyOS). Copied into the source tree during `prepare()`. |
| `disable_configs.py` | Python script that programmatically disables hundreds of unwanted kernel configs (ARM platforms, non-AMD GPUs, etc.). |

### Patch Files (see Section 5 for numbering)
| Prefix | Meaning | Example |
|--------|---------|---------|
| `00xx-*.patch` | Hand-selected upstream fixes specifically for our hardware | `0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch` |
| `01xx-*.patch` | Squashed CachyOS branch patches (bbr3, kbuild, cpu-isa, cgroup-vram, fixes, drops, hdmi, preempt-ipi, vesa-dsc-bpp) | `0101-cachy-bbr3.patch` ... `0109-cachy-vesa-dsc.patch` |
| `10xx-*.patch` | Cherry-picked patches from `sirlucjan`, `firelzrd`, and specific upstream subsystem series | `1083-mm-7.2-introduce-LRU-MARIE.patch` |
| `20xx-*.patch` | Patches extracted directly from upstream git repositories (`drm-next`, `linux-next`, `linux-pm`) | `2017-05-80-drm-amd-display-Enable-IPS-support-for-DCN4-Variant.patch` |

### SQM QoS (Network Shaping)
| File | Purpose |
|------|---------|
| `sqm-qos/sqm-qos.sh` | Bash script that dynamically finds the internet interface, enables BBR3, and applies CAKE qdiscs |
| `sqm-qos/sqm-qos.conf` | User-editable config with `DOWNLOAD_MBIT` and `UPLOAD_MBIT` values |
| `sqm-qos/sqm-qos.service` | systemd oneshot service that runs `sqm-qos.sh` at boot |

### Out-of-Tree Modules
| Directory | Purpose |
|-----------|---------|
| `r8125/` | Realtek RTL8125 2.5GbE out-of-tree driver source |

### Build Artifacts (generated, not committed)
| File/Dir | Purpose |
|----------|---------|
| `src/` | Extracted kernel source tree (created by `makepkg`) |
| `pkg/` | Staged package contents (created by `makepkg`) |
| `linux-sleepy-*.pkg.tar.zst` | The final installable Arch Linux kernel package (~19 MB) |
| `linux-sleepy-headers-*.pkg.tar.zst` | Kernel headers package for building modules (~69 MB) |
| `linux-sleepy-r8125-*.pkg.tar.zst` | RTL8125 out-of-tree driver module package (~124 KB) |
| `repos/` | Cloned upstream git repos used for patch extraction |

### Deleted Legacy Files (do NOT recreate)
The following files previously existed but have been removed:
- `cake-sqm.sh` -- old hardcoded CAKE script, replaced by `sqm-qos/sqm-qos.sh`
- `cake-sqm.service` -- old hardcoded service, replaced by `sqm-qos/sqm-qos.service`

If you see the PKGBUILD referencing `cake-sqm.sh` or `cake-sqm.service`, remove those references.

---

## 5. Patch Numbering Convention

This is critical. Patches are applied in filename sort order by the PKGBUILD. The numbering tells you where each patch came from:

| Range | Category | Source / Description |
|-------|--------|---------------|
| `0001–0049` | **Custom & Handmade Hardware Fixes** | Local stability & power fixes for Zen 4 & RDNA 4 (`0001`–`0013`) |
| `0050–0099` | **Common EDID & Display Parser** | Upstream AMD FreeSync VSDB common parser series (`0050`–`0053`) |
| `0100–0199` | **CachyOS Branch Squashes** | One squashed patch per CachyOS branch (`0101`–`0109`: bbr3, kbuild, cpu-isa, cgroup-vram, fixes, drops, hdmi, preempt-ipi, vesa-dsc-bpp) |
| `1000–1099` | **AMDGPU GPU Core** | GFX12, GMC, SDMA7, PSP, TTM, and TLB invalidation patches |
| `1100–1199` | **AMD Display Features** | DCN4 / DCN42B display, PSR, Replay, and pstate quirks |
| `1200–1299` | **AMD Power Management** | `amd-pstate` per-core boost, EPP caching, and loose bounds |
| `1300–1399` | **I/O Schedulers** | `mq-deadline` and `bfq` queue serialization |
| `1400–1499` | **Memory Management** | `zstd` dev-tree merge & Firelzrd `LRU MARIE` v12 |
| `1500–1599` | **CPU Idle Governors** | Firelzrd `NAP` CPU idle governor v0.5.0 |
| `2000–2099` | **Upstream Dev-Tree Backports** | `drm-next`, `linux-next`, `linux-pm` landed/queued backports |

---

## 6. How to Build the Kernel

This is the exact sequence. Do not skip or reorder steps.

### Prerequisites
```bash
sudo pacman -S base-devel clang llvm lld bpf pahole rust rust-bindgen rust-src xxhash zstd
```
All of these are listed in the PKGBUILD `makedepends`. If any are missing, `makepkg -s` will try to install them, but it's better to have them ready.

### Build Commands
```bash
cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export

# Step 1: Clean previous build artifacts
rm -rf src pkg

# Step 2: Update checksums (ONLY if you changed any source files)
updpkgsums

# Step 3: Build the kernel
# -f = force rebuild, -s = install missing deps, -c = clean after build
makepkg -f -s -c
```

### What Happens During Build
1. `makepkg` downloads the kernel tarball (if not cached) and extracts it to `src/linux-7.2-rc4/`
2. The `prepare()` function runs:
   - Prompts user interactively about SQM QoS setup (download/upload speeds)
   - Sets version strings (`localversion.10-pkgrel`, `localversion.20-pkgname`)
   - Applies ALL `.patch` files from the `source=()` array in order
   - Copies `config` into `.config`
   - Runs `disable_configs.py` to strip unwanted drivers
   - Runs `scripts/config` to set our specific options (Zen4, LTO, MARIE, NAP, etc.)
   - Runs `make olddefconfig` to resolve new config options silently
   - Disables post-olddefconfig auto-enabled configs (CHROMEOS_PRIVACY_SCREEN, etc.)
3. `build()` compiles the kernel with clang+LLD
4. `_package()` installs vmlinuz, modules, and (if user opted in) SQM QoS files
5. `_package-headers()` installs kernel headers
6. The r8125 out-of-tree module is compiled and packaged separately

### Expected Output
```
linux-sleepy-7.2.rc4-1-x86_64.pkg.tar.zst         ~19 MB  (kernel + modules)
linux-sleepy-headers-7.2.rc4-1-x86_64.pkg.tar.zst  ~69 MB  (headers for DKMS)
linux-sleepy-r8125-7.2.rc4-1-x86_64.pkg.tar.zst   ~124 KB  (RTL8125 driver)
```

### Installation
```bash
sudo pacman -U linux-sleepy-*.pkg.tar.zst
```

---

## 7. How to Update to a New Kernel Version

When bumping from e.g. `7.2-rc4` to `7.2-rc5`:

### Step 1: Verify the new release exists
```bash
curl -I -s "https://git.kernel.org/torvalds/t/linux-7.2-rc5.tar.gz" | head -5
```
If you get `404 Not Found`, the release does not exist yet. Stop and tell the user.

### Step 2: Update PKGBUILD variables
Find and change these values in PKGBUILD:
```
_major=7.2
_minor=rc5          # was rc4
_srcname=linux-7.2-rc5
```

### Step 3: Rebase ALL patches
Every single `.patch` file must be tested against the new kernel source:
```bash
# Extract the new kernel source
tar xf linux-7.2-rc5.tar.gz
cd linux-7.2-rc5

# Test each patch
for p in ../*.patch; do
    echo "Testing $p..."
    patch --dry-run -Np1 < "$p"
done
```

Any patch that fails with `HUNK FAILED` needs to be:
1. **Regenerated** from its upstream source (re-extract with `git format-patch` from the relevant repo), OR
2. **Dropped** if it has already been merged into the new release (check with `git log --oneline --grep="<subject>"` in the mainline tree)

### Step 4: Refresh the squashed CachyOS branch patches
See Section 8 (or run the `patch-cachy-branches` skill). CachyOS will likely have updated their patchset for the new kernel version.

### Step 5: Update checksums and build
```bash
updpkgsums
rm -rf src pkg
makepkg -f -s -c
```

---

## 8. Refresh the Squashed CachyOS Branch Patches

The monolithic mega-patch and the per-file `0101`–`0187` approach are **both retired** (2026-08-02). Each CachyOS branch is now **squashed into a single patch** (`0101`–`0109`), so `source=()` has 9 CachyOS files instead of 87. Run the `patch-cachy-branches` skill for the full procedure. Essentials:

1. Pull `repos/sirlucjan-kernel-patches` and pick the latest `-sep` dir per branch (currently `fixes` = `-v10-sep`, `preempt-ipi` = `-v3-sep`, `lru-marie` = `-v12`).
2. For each branch, apply its `-sep` patches **in order to the actual series tree** (rc5 + the `0001`–`0058` local/upstream patches — the pre-CachyOS patches touch shared files like `drm_edid.c`).
3. `find . -name '*.orig' -delete; find . -name '*.rej' -delete` — `patch` leaves `.orig` backups that would pollute the squash (this bit us once).
4. Emit the cumulative diff as one `git format-patch`: `git diff --binary > NNNN-cachy-<branch>.patch`.
5. The `fixes` branch is squashed **in full** (all 26 patches incl. off-target) into `0105-cachy-fixes.patch`, then `0106-cachy-drops.patch` **reverts** the off-target groups (i915, btusb, rtw89, laptop audio, i2c touchpad, iwlwifi, SOF Intel, nouveau, DisplayID eDP) — net effect = only the 10 hardware-relevant fixes.
6. The `hdmi` squash (`0107`) **excludes `0151`** (it duplicates `0055`'s HF-VSDB content).
7. Verify each squash: `git -C repos/linux-7.2-rc5 apply --check NNNN-cachy-*.patch`, then `updpkgsums`.

---

## 9. How to Ingest Upstream Patches

When the user asks you to check for new upstream patches targeting our hardware, here is exactly what to do.

### CRITICAL: Where to Get Patches

| Source | How to Access | DO NOT |
|--------|--------------|--------|
| `drm-next` (AMD GPU patches) | `git clone` from `https://gitlab.freedesktop.org/drm/kernel.git` | DO NOT scrape `lore.kernel.org/dri-devel/` |
| `linux-next` (staging tree) | `git clone` from `https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git` | DO NOT scrape `lore.kernel.org/linux-next/` |
| `linux-pm` (CPU frequency, power) | `git clone` from `https://git.kernel.org/pub/scm/linux/kernel/git/rafael/linux-pm.git` | DO NOT scrape `lore.kernel.org/linux-pm/` |
| `amd-gfx` mailing list | Download monthly thread archive from `https://lists.freedesktop.org/archives/amd-gfx/YYYY-Month/thread.html` | DO NOT use `lore.kernel.org/amd-gfx/` |
| `dri-devel` mailing list | Download monthly thread archive from `https://lists.freedesktop.org/archives/dri-devel/YYYY-Month/thread.html` | DO NOT use `lore.kernel.org/dri-devel/` |
| `sirlucjan` patches | `git clone https://github.com/sirlucjan/kernel-patches.git` | -- |
| `firelzrd` patches | `git clone https://github.com/firelzrd/bore-scheduler.git` | -- |

**WHY NOT lore.kernel.org?** It has aggressive anti-bot protection (CAPTCHAs, rate limiting, empty responses). Automated agents WILL be blocked. Use the git repos and freedesktop.org archives instead.

### Step-by-Step: Clone repos and extract patches

```bash
cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export/repos/

# Clone with shallow history since a recent date to save disk space
# IMPORTANT: Use --shallow-since, NOT --depth=1. --depth=1 strips commit
# history so git log --grep will return nothing. --shallow-since keeps
# enough history for searching.
git clone --no-tags --shallow-since="2026-06-01" https://gitlab.freedesktop.org/drm/kernel.git drm-next
git clone --no-tags --shallow-since="2026-06-01" https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
git clone --no-tags --shallow-since="2026-06-01" https://git.kernel.org/pub/scm/linux/kernel/git/rafael/linux-pm.git
```

### Step-by-Step: Search for relevant commits

Search each repo for our hardware keywords:
```bash
cd drm-next
git log --oneline --grep="gfx12"
git log --oneline --grep="navi48"
git log --oneline --grep="dcn4"
git log --oneline --grep="smu14"
git log --oneline --grep="psp14"
git log --oneline --grep="mmhub_4"
git log --oneline --grep="sdma_v7"
git log --oneline --grep="vcn_v5"

cd ../linux-pm
git log --oneline --grep="amd-pstate"
git log --oneline --grep="amd_pstate"
git log --oneline --grep="CPPC"
git log --oneline --grep="k10temp"
```

### Step-by-Step: Extract patches
```bash
# Example: extract a specific commit as a patch
cd drm-next
git format-patch -1 <commit-hash> -o ../../

# Rename it with the correct 20xx prefix
mv ../../0001-drm-amdgpu-fix-something.patch ../../2040-drm-amdgpu-fix-something.patch
```

### Step-by-Step: Verify the patch is not already applied
Before adding a `20xx` patch, check if its changes already exist:
```bash
cd /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export/src/linux-7.2-rc4/
grep -r "unique_function_or_variable_name" drivers/gpu/drm/amd/
```
If the code already exists in the tree (from mainline or from the CachyOS mega-patch), DO NOT add the patch -- it will cause a conflict.

### WARNING: Known Collision-Prone 20xx Patches
During the 7.2-rc4 build, the following `20xx` patches were extracted from `drm-next` but had to be **removed** because they collided with code already present in the CachyOS mega-patch or the `10xx` cherry-picks:

**Removed patches (DO NOT re-add for 7.2-rc4):** `2003`, `2006`, `2008`, `2011`, `2012`, `2015`, `2016`, `2019`, `2022`, `2024`, `2027`, `2028`, `2029`, `2032`, `2033`, `2034`, `2035`, `2037`, `2038`

The collision pattern is: upstream `drm-next` commits touch the same files/functions that CachyOS already patched (e.g., `gfx_v12_0.c`, `gmc_v12_0.c`, `dcn42b_resource.c`). When checking for new upstream patches on a future kernel version, always `patch --dry-run` first and expect collisions in these subsystems.

### Step-by-Step: Fetching from freedesktop.org Mailing List Archives
When you need to check `amd-gfx` or `dri-devel` mailing lists (not available via git):
```bash
# Download the monthly thread index page
curl -s "https://lists.freedesktop.org/archives/amd-gfx/2026-July/thread.html" -o amd-gfx-july.html
curl -s "https://lists.freedesktop.org/archives/dri-devel/2026-July/thread.html" -o dri-devel-july.html

# Search for hardware-relevant threads
grep -i "gfx12\|navi48\|dcn4\|smu14\|rdna" amd-gfx-july.html

# To download a specific patch email as mbox:
curl -s "https://lists.freedesktop.org/archives/amd-gfx/2026-July/NNNNNN.html" -o patch.html
# Then extract the patch content from the HTML, or use the raw .txt link if available
```
Note: `lists.freedesktop.org` does NOT have anti-bot protection like `lore.kernel.org` and is safe to access programmatically.

### Step-by-Step: Add to PKGBUILD and rebuild
1. Add the new patch filename to the `source=()` array in PKGBUILD
2. Run `updpkgsums`
3. Run `rm -rf src pkg && makepkg -f -s -c`

---

## 10. How to Audit Third-Party Patches

When checking `sirlucjan/kernel-patches` or `firelzrd/bore-scheduler` for updates:

### What We Currently Use (KEEP these)

| Patch Files | Subsystem | Why We Need It |
|-------------|-----------|---------------|
| `1070-1076` | `amd-pstate` CPPC fixes | Zen 4 CPU frequency scaling correctness |
| `1077-1081` | Block I/O spinlock fixes | NVMe performance under high IOPS |
| `1082` | `zstd` dev tree merge | Faster kernel compression |
| `1083` | LRU-MARIE | Multi-Armed Bandit MGLRU page eviction |
| `1084` | NAP governor | Neural Adaptive Predictor for CPU idle |

### What We Reject (DO NOT add these)

| Subsystem | Why We Reject It |
|-----------|-----------------|
| `gaming-sched` | Conflicts with `sched-ext` BPF scheduling |
| `clang-patches` (Polly) | LLVM Polly loop optimizer causes miscompilations |
| `poc-selector` | Legacy scheduler swapper, conflicts with `sched-ext` |
| `t2` / `v4l2loopback` | Apple/laptop hardware we don't have |
| Any ARM/mobile patches | We're x86-64 only |

### How to Check for Updates
```bash
cd repos/
git clone https://github.com/sirlucjan/kernel-patches.git
cd kernel-patches

# Check the branch matching our kernel version
git branch -r | grep 7.2
git checkout master/7.2-rc  # or whatever branch matches

# Look at what's available
ls -la
```

Compare their patch files byte-for-byte against what we have:
```bash
diff repos/kernel-patches/7.2/lru-marie/0001-*.patch 1083-mm-7.2-introduce-LRU-MARIE.patch
```

---

## 10.5 Patch Source Integrity and New Patch Checklist

### Patch Source Manifest

All patch provenance is documented in `PATCH_SOURCES.md`. **Always read this file before adding, removing, or modifying any patch.** It contains:
- The exact source (repo + commit) for every patch
- Verification status (byte-identical check results)
- Pending patches discovered but not yet applied
- Deleted legacy patches and why they were removed

### Verifying Patch Source Integrity

Before any build, verify that every patch still matches its source:

```bash
# 1. Ensure all repos are up to date
cd repos/
for d in drm-next linux-next linux-pm sirlucjan-kernel-patches firelzrd-bore-scheduler; do
    [ -d "$d" ] && cd "$d" && git fetch origin && cd ..
done

# 2. Verify 10xx patches against sirlucjan (byte-identical check)
cd repos/sirlucjan-kernel-patches
diff 7.2-rc/amd-pstate-patches-sep/0001-cpufreq-amd-pstate-Bail-out-early-if-X86_FEATURE_HW_.patch ../../1070-cpufreq-amd-pstate-Bail-out-early-if-X86_FEATURE_HW_.patch && echo "1070: MATCH" || echo "1070: NEEDS UPDATE"
diff 7.2-rc/block-patches-sep/0001-block-mq-deadline-pass-in-queue-directly-to-dd_inser.patch ../../1077-block-mq-deadline-pass-in-queue-directly-to-dd_inser.patch && echo "1077: MATCH" || echo "1077: NEEDS UPDATE"
diff 7.2-rc/lru-marie-patches-v10/0001-mm-7.2-introduce-LRU-MARIE.patch ../../1083-mm-7.2-introduce-LRU-MARIE-v10.patch && echo "1083: MATCH" || echo "1083: NEEDS UPDATE"
diff 7.2-rc/nap-patches/0001-7.2-nap-v0.5.0.patch ../../1084-7.2-nap-v0.5.0.patch && echo "1084: MATCH" || echo "1084: NEEDS UPDATE"
diff 7.2-rc/zstd-dev-patches/0001-zstd-7.2-merge-v1.6.0-into-kernel-tree.patch ../../1082-zstd-7.2-merge-v1.6.0-into-kernel-tree.patch && echo "1082: MATCH" || echo "1082: NEEDS UPDATE"

# 3. Verify 20xx patches retain original git headers
for p in ../20xx-*.patch; do
    head -4 "$p" | grep -q "From [0-9a-f]\{40\}" && echo "$p: git header OK" || echo "$p: MISSING GIT HEADER"
done

# 4. Verify 00xx patches retain original git headers
for p in ../00xx-*.patch; do
    head -4 "$p" | grep -q "From [0-9a-f]\{40\}" && echo "$p: git header OK" || echo "$p: MISSING GIT HEADER"
done
```

### New Patch Checklist (Run Before Every Build)

When checking for new patches from upstream sources, follow this checklist:

**Step 1: Check drm-next for new commits targeting our hardware**
```bash
cd repos/drm-next
git log --oneline --since="LAST_CHECK_DATE" --grep="gfx12\|navi48\|dcn4\|dcn42\|smu14\|psp14\|sdma.*7\|mmhub.*4\|vcn.*5"
```

**Step 2: Check amd-gfx mailing list for new threads**
```bash
curl -s "https://lists.freedesktop.org/archives/amd-gfx/$(date +%Y-%m)/thread.html" | \
    grep -i "gfx12\|navi48\|dcn4\|smu14\|rdna\|dcn42"
```

**Step 3: Check dri-devel mailing list for new threads**
```bash
curl -s "https://lists.freedesktop.org/archives/dri-devel/$(date +%Y-%m)/thread.html" | \
    grep -i "dcn42\|psr.*dcn\|ips.*dcn\|replay.*dcn\|hubp\|dpp.*pg\|hdmistreamclk\|vid.*crc\|hblank\|mcache"
```

**Step 4: Check sirlucjan for updated patches**
```bash
cd repos/sirlucjan-kernel-patches
git fetch origin
# Compare our patches against sirlucjan's (see integrity check above)
# If any differ, decide: update to sirlucjan's version or keep ours with explanation
```

**Step 5: Evaluate new patches against our hardware**
For each new patch found:
1. Does it target one of our components? (Zen 4 CPU, RDNA 4 GPU, RTL8125 NIC, NVMe storage, sched-ext)
2. Does it conflict with any existing patch? (`patch --dry-run -Np1`)
3. Is it already merged into mainline? (if yes, drop it for the next kernel version)
4. Is it from a trustworthy source? (real kernel developer, signed-off-by present)

**Step 6: Document new patches in PATCH_SOURCES.md**
Every new patch MUST be documented in `PATCH_SOURCES.md` before being added to the PKGBUILD.

---

## 10.6 bpftune Requirements Verification

bpftune requires specific kernel configuration options to function. These are **non-negotiable** — if any are missing, bpftune will fail to operate. The PKGBUILD's `prepare()` function sets these via `scripts/config`, but `make olddefconfig` can auto-re-enable them. Always verify AFTER the full prepare() phase.

### Required Kernel Config Options

| Option | Required Value | Purpose |
|--------|---------------|---------|
| `CONFIG_BPF_SYSCALL` | `y` | Allows user-space BPF programs (bpftune core) |
| `CONFIG_DEBUG_INFO_BTF` | `y` | BTF debug info for bpftool/bpftune |
| `CONFIG_DEBUG_INFO_BTF_MODULES` | `y` | BTF info for loadable modules |
| `CONFIG_FTRACE` | `y` | Function tracing (bpftune uses ftrace for runtime tuning) |
| `CONFIG_BPF_EVENTS` | `y` | BPF events for tracing |
| `CONFIG_DYNAMIC_FTRACE` | `y` | Dynamic ftrace support |
| `CONFIG_FUNCTION_TRACER` | `y` | Function tracing infrastructure |
| `CONFIG_KPROBE_EVENTS` | `y` | Kprobes for runtime instrumentation |
| `CONFIG_HAVE_KPROBES_ON_FTRACE` | `y` | kprobes on ftrace targets |

### Build-Time Dependencies

| Package | Purpose |
|---------|---------|
| `pahole` | Generates BTF information from DWARF debug info |
| `bpftool` (in `tools/bpf/bpftool/`) | Built as part of kernel build; provides `bpftune` CLI |

### Verification Script

Run this after `prepare()` completes (inside the kernel source tree):

```bash
# Verify all bpftune-required config options
for opt in BPF_SYSCALL DEBUG_INFO_BTF DEBUG_INFO_BTF_MODULES FTRACE BPF_EVENTS \
           DYNAMIC_FTRACE FUNCTION_TRACER KPROBE_EVENTS HAVE_KPROBES_ON_FTRACE; do
    val=$(scripts/config -g "$opt" 2>/dev/null)
    if [ "$val" = "y" ] || [ "$val" = "m" ]; then
        echo "✓ $opt = $val"
    else
        echo "✗ $opt = $val (REQUIRED: y or m)"
        exit 1
    fi
done

# Verify pahole is available
if command -v pahole &>/dev/null; then
    echo "✓ pahole: $(pahole --version 2>&1 | head -1)"
else
    echo "✗ pahole: NOT INSTALLED (required for BTF generation)"
    exit 1
fi

# Verify BTF was generated in vmlinux
if [ -f vmlinux ] && file vmlinux | grep -q "BTF"; then
    echo "✓ vmlinux contains BTF data"
else
    echo "✗ vmlinux does NOT contain BTF data (check pahole version and DEBUG_INFO_BTF)"
    exit 1
fi
```

### Common bpftune Issues

1. **Missing BTF in vmlinux**: Usually means `pahole` is too old. Arch Linux ships a recent version, but if building on an older system, upgrade `pahole` via `sudo pacman -S pahole`.

2. **FTRACE auto-disabled by `make olddefconfig`**: The `prepare()` function explicitly enables FTRACE and related options AFTER `olddefconfig`. If you run `make olddefconfig` manually without the `scripts/config` overrides, these get reset to defaults.

3. **BTF modules not generated**: Requires `CONFIG_DEBUG_INFO_BTF_MODULES=y` AND a recent `pahole` (≥1.24). Check with `scripts/config -g DEBUG_INFO_BTF_MODULES`.

---

## 10.7 Lessons Learned — Mistakes to Avoid

These are real mistakes made during the 7.2-rc4 build cycle. **Read this section before doing anything.**

### Mistake 1: Dropping 0008 without user approval
**What happened:** Agent removed patch 0008 (DCN20 link encoder memory leak) citing it only affects legacy DCN20. Target hardware uses DCN401/DCN42B, but the DCN20 code path can still be exercised in edge cases (misconfigured HPD sources, certain multi-monitor setups). The patch was harmless and fixed a real bug.
**Rule:** NEVER remove a patch without explicit user approval. If a patch is safe (no conflicts, no side effects), keep it. Document removal reasons in PATCH_SOURCES.md but don't auto-delete.

### Mistake 2: Not checking ALL upstream sources for new patches
**What happened:** Agent checked drm-next git log but missed patches from:
- amd-gfx mailing list (July 2026): SMU14 power limit fix, gfxoff around GPU reset series, IP dump alloc ordering, named barrier restore
- dri-devel mailing list: Named barrier patch (also cross-posted to amd-gfx)
- linux-pm: No new relevant patches this cycle
**Rule:** ALWAYS check ALL sources listed in Section 9 before declaring "no new patches":
1. `drm-next` git log (hardware keywords)
2. `amd-gfx` mailing list thread index (grep hardware keywords)
3. `dri-devel` mailing list thread index (grep DCN42B/PSR/IPS/Replay keywords)
4. `linux-pm` git log (amd-pstate, CPPC, k10temp, LRU-MARIE, zstd)
5. `sirlucjan` repo (byte-identical check against our 10xx patches)
6. `firelzrd` repo (BORE scheduler — usually rejected, but check anyway)

### Mistake 3: Assuming mailing list patches are in drm-next
**What happened:** Agent extracted patches from drm-next but some patches (gfxoff around GPU reset, IP dump alloc ordering, named barrier restore) were only in the mailing list threads, NOT yet merged into drm-next. They must be extracted from `lists.freedesktop.org` HTML archives.
**Rule:** Mailing list patches may not yet be in drm-next. Always check both the git repo AND the mailing list archives. The `git log --since=LAST_CHECK_DATE` in drm-next only shows merged commits.

### Mistake 4: Using wrong context for patches from mailing list HTML
**What happened:** Agent extracted patches from mailing list HTML but used wrong line numbers (from the original commit vs. 7.2-rc4's actual layout). Patches failed with `HUNK FAILED` because the target file structure differs between the upstream commit and our base kernel.
**Rule:** When creating patches from mailing list HTML:
1. Extract the diff content from the HTML `<PRE>` block
2. Reconstruct the patch with correct `--- a/` and `+++ b/` paths
3. **ALWAYS test with `patch --dry-run -Np1` against the extracted 7.2-rc4 source** before adding to PKGBUILD
4. If a patch fails, regenerate it by making the change directly in the extracted source and running `diff -u`

### Mistake 5: Not checking if patches are already in vanilla
**What happened:** Agent added patches for DCN42B mcache callback and SMU14 power limit range calculation that were already merged into Linux 7.2-rc4. These were detected as "Reversed (or previously applied) patch" during testing.
**Rule:** Before adding any patch, verify it's not already in vanilla 7.2-rc4:
```bash
# Check if code change already exists in vanilla
grep -r "unique_function_or_variable" drivers/
# Check if patch hunks match already-modified code
patch --dry-run -Np1 < patchfile.patch  # "Reversed" means already applied
```

### Mistake 6: Forgetting to update b2sums when adding patches
**What happened:** Agent added patches to PKGBUILD source array but forgot to add corresponding b2sums entries. `makepkg` would refuse to build.
**Rule:** Every time you add/remove/modify a file in `source=()`, run `updpkgsums`. The b2sums array must have exactly the same number of entries as the source array, in the same order.

### Mistake 7: Not documenting new patches in PATCH_SOURCES.md
**What happened:** Agent added patches to PKGBUILD but didn't update PATCH_SOURCES.md with their provenance.
**Rule:** Every patch in this repo MUST be documented in PATCH_SOURCES.md before being added to the PKGBUILD. Include: source repo/commit, mailing list URL, author, date, verification status.

### Mistake 8: Writing patches with malformed diff format
**What happened:** Agent created a patch with a malformed second hunk (incorrect line numbers for the `@@` header), causing `patch: **** malformed patch at line 28`.
**Rule:** When hand-crafting patches:
1. Use the exact line numbers from the target file (check with `grep -n`)
2. Include enough context lines (at least 3 lines before and after the change)
3. Use `--- a/` and `+++ b/` format
4. Test immediately with `patch --dry-run`

### Mistake 9: Not verifying bpftune requirements in the final package
**What happened:** bpftune config options were set in PKGBUILD but never verified in the actual built package.
**Rule:** After every build, verify bpftune requirements using the script in Section 10.6. Run it against the extracted kernel source in `src/linux-7.2-rc4/` after prepare() completes.

### Mistake 10: Not checking sirlucjan for updated patches
**What happened:** Agent didn't compare our 10xx patches against sirlucjan's latest versions. Some patches may have been updated upstream.
**Rule:** Always run the byte-identical check against sirlucjan before every build. If patches differ, decide whether to update (sirlucjan's version) or keep ours (with documented reason).

---

## 11. Kbuild Configuration Reference

### Compiler and Linker
The PKGBUILD sets these build flags. DO NOT CHANGE THEM:
```bash
BUILD_FLAGS=(
    CC=clang
    LD=ld.lld
    LLVM=1
    LLVM_IAS=1
)
```

### Key `scripts/config` Commands in `prepare()`
These are already in the PKGBUILD. This is what they do:

```bash
# === CPU Target ===
scripts/config -d GENERIC_CPU -e MZEN4              # Compile for Zen 4 specifically

# === Compiler Optimization ===
scripts/config -d LTO_NONE -e LTO_CLANG_THIN        # Enable ThinLTO
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3  # Use -O3

# === CachyOS Base ===
scripts/config -e CACHY                              # Enable CachyOS config hooks

# === NAP Governor (baked into kernel cmdline) ===
scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap" -d CMDLINE_OVERRIDE
# This means:
#   - CONFIG_CMDLINE_BOOL=y     -> enable built-in command line
#   - CONFIG_CMDLINE="cpuidle.governor=nap"  -> bake nap governor into kernel
#   - CONFIG_CMDLINE_OVERRIDE is NOT set -> bootloader params are APPENDED, not replaced
# Result: NAP governor activates automatically at boot without editing GRUB/systemd-boot

# === BPF and Debug ===
scripts/config -d DEBUG_INFO_NONE -e DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_BTF # Required for bpftune
scripts/config -e BPF_SYSCALL -e FTRACE -e BPF_EVENTS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e KPROBE_EVENTS

# === Memory Management ===
scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE
scripts/config -e CPU_IDLE_GOV_NAP

# === Network (for CAKE SQM) ===
scripts/config -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32

# === Bloat Removal ===
scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU  # No Intel/Nvidia GPUs
scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN    # No industrial/enterprise
scripts/config -d SECURITY_APPARMOR                    # Not needed on desktop
scripts/config -d AUDIT -d AUDITSYSCALL                # Not needed on desktop
```

### Clean Version String
The kernel version string is controlled by:
```bash
echo "-$pkgrel" > localversion.10-pkgrel         # e.g. "-1"
echo "-${pkgbase#linux-}" > localversion.20-pkgname  # e.g. "-sleepy"
scripts/config --set-str LOCALVERSION ""          # Empty -- no extra suffix
```
Result: `uname -r` outputs `7.2.0-rc4-1-sleepy`

---

## 12. SQM QoS and BBR3 Service

The PKGBUILD includes an interactive prompt during `prepare()` that asks the user if they want to enable the SQM QoS service. If they answer yes, the service is baked directly into the kernel package.

### What the Service Does
1. Sets TCP congestion control to `bbr3` system-wide (`sysctl net.ipv4.tcp_congestion_control=bbr3`)
2. Dynamically finds the active internet interface via `ip route get 9.9.9.9`
3. Applies the `cake` qdisc for upload shaping (egress)
4. Creates an `ifb4cake` interface for download shaping (ingress via traffic mirroring)
5. User provides their ISP bandwidth in Mbit/s -- should be set to 90-95% of actual measured speed

### Files
- `sqm-qos/sqm-qos.sh` -> installed to `/usr/local/bin/sqm-qos.sh`
- `sqm-qos/sqm-qos.conf` -> installed to `/etc/sqm-qos.conf` (with user's speed values)
- `sqm-qos/sqm-qos.service` -> installed to `/usr/lib/systemd/system/sqm-qos.service`
- A symlink is created in `/etc/systemd/system/multi-user.target.wants/` to auto-enable the service

### If the User Skips the Prompt
Only BBR3 is set via sysctl. No CAKE shaping is applied. The service files are not packaged.

### For AI Agents Running Non-Interactively (No TTY)
The SQM QoS prompt uses `if [ -t 0 ]` to detect whether a terminal is attached. When `makepkg` is run by an AI agent without a TTY (e.g., via a subprocess), the prompt is silently skipped.

To enable SQM QoS when building non-interactively, pre-seed the config files BEFORE running `makepkg`:
```bash
# Create the config file with the user's bandwidth values
cat > /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export/src/sqm-qos.conf << EOF
DOWNLOAD_MBIT="950"
UPLOAD_MBIT="950"
EOF

# Create the flag file that tells _package() to include SQM files
touch /home/sleepy/Documents/antigravity/bold-rutherford/sleepy-kernel-export/src/.enable_sqm
```
Note: These files go in `src/`, not the repo root. They must be created AFTER `makepkg` extracts the source (i.e., after the `prepare()` phase starts). The simplest approach is to ask the user for their bandwidth values first, then create these files before running `makepkg`.

---

## 13. Debugging Build Failures

### Patch Application Failures
If `makepkg` fails during `prepare()` with a message like:
```
Hunk #3 FAILED at 224.
```

1. Look at the `.rej` file: `cat src/linux-7.2-rc4/path/to/file.c.rej`
2. The `.rej` file shows what the patch expected vs. what was actually in the file
3. Common causes:
   - **Patch already applied** by the CachyOS mega-patch or a previous patch -> REMOVE the conflicting patch
   - **Context lines shifted** due to upstream changes -> regenerate the patch from its source repo
   - **CachyOS modified the same code** (e.g., `vm_swappiness` has a `CONFIG_CACHY` ifdef) -> the patch needs manual rebasing

### Compilation Failures
- If you see `ld.mold` errors -> someone changed the linker. Fix PKGBUILD back to `LD=ld.lld`
- If you see `BTF` errors -> ensure `pahole` is installed: `sudo pacman -S pahole`
- If `Rust` errors appear -> ensure `rust` and `rust-bindgen` are installed

### Package Size Checks
After a successful build:
```bash
ls -lh *.pkg.tar.zst
```
- Core kernel should be ~19-25 MB (if it's >40 MB, bloat removal failed)
- Headers should be ~65-75 MB
- r8125 should be ~100-150 KB

---

## 14. Common Mistakes to Avoid

| Mistake | Why It's Bad | What to Do Instead |
|---------|-------------|-------------------|
| Scraping `lore.kernel.org` | Anti-bot protection blocks you | Clone git repos (Section 9) or use `lists.freedesktop.org` archives |
| Using `ld.mold` | Crashes on vDSO linker scripts | Always use `ld.lld` |
| Forgetting `updpkgsums` | `makepkg` refuses to build due to checksum mismatch | Always run after modifying sources |
| Not cleaning `src/` and `pkg/` | Old patched files persist, causing false conflicts | Always `rm -rf src pkg` before building |

| Adding Intel/Nvidia/ARM patches | Adds bloat, may cause config conflicts | Only add AMD GPU, AMD CPU, or block/mm/net patches |
| Writing patches by hand | Risk of introducing bugs, incorrect diff format | Always use `git format-patch` from real commits |
| Using 8.8.8.8 in network scripts | User preference is Quad9 | Always use `9.9.9.9` |
| Skipping `--dry-run` patch test | You won't know it fails until the full build runs | Always test with `patch --dry-run -Np1` first |
| Cloning repos to `/tmp` | tmpfs can fill up, repos are lost on reboot | Clone to `sleepy-kernel-export/repos/` |
