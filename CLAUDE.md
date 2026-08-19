# sleepy-kernel

Custom Arch Linux kernel package based on Linux mainline RC releases, built for
a single AMD Zen 4 + RDNA 4 desktop. Uses a sanitized CachyOS patchset as the
base, with additional upstream and local patches filtered to this hardware.

## Target hardware

| Component | Hardware | Kernel identifiers |
|---|---|---|
| CPU | AMD Ryzen 7 7700 (Zen 4) | `MZEN4`, `amd-pstate`, `CPPC`, `k10temp` |
| GPU | AMD Radeon RX 9070 XT (Navi 48, RDNA 4) | `gfx1201`, `DCN401`, `DCN42B`, `SMU14`, `PSP14`, `GC 12.0`, `SDMA 7.0`, `VCN 5.0`, `MMHUB 4.1` |
| NIC | Realtek RTL8125B 2.5 GbE | `r8169` (in-kernel driver, since 7.2) |
| NVMe | Phison E16 PCIe 4.0 | `bfq`, `mq-deadline` |
| Scheduler | sched-ext BPF schedulers | `CONFIG_SCHED_CLASS_EXT=y` |
| CPUIdle | NAP governor | `CONFIG_CPU_IDLE_GOV_NAP=y` |

**If a patch does not target one of these components, it does not go in.**

## Documentation

| File | Purpose |
|---|---|
| `GUIDE.md` | End-user README: target audience, differences from vanilla, build instructions |
| `README.md` | User-facing project doc |
| `CHANGELOG.md` | Per-release summary of what changed, by kernel version + pkgrel |
| `PATCH_SOURCES.md` | Per-patch provenance ledger — authors, commit hashes, source URLs, revisions |
| `LESSONS.md` | Full incident log ("do not repeat") — the durable rules are below; the context is there |

Local Google documentation style guides (committed reference copies, CC-By 3.0
with attribution in `.claude/style-guides/README.md`) live in
`.claude/style-guides/`; the documentation skills consult them before editing
docs.

## Repository layout

| Path | Purpose |
|---|---|
| `PKGBUILD` | Arch build script — version vars, `source=()`, `prepare()` applies the series + config overrides |
| `config` | Base `.config` (from CachyOS) |
| `disable_configs.py` | Strips unwanted driver configs before `olddefconfig` |
| `patches/<range>/NNNN-*.patch` | The patch series, one folder per number range (see Patch numbering). Root-level `NNNN-*.patch` symlinks are auto-created by the PKGBUILD for makepkg 7.1.0 basename resolution and are gitignored. |
| `net-tune/` | Unified CAKE SQM + latency tuning systemd service |
| `repos/` | Cloned upstream git repos for patch extraction (gitignored; never clone into `/tmp`) |
| `src/`, `pkg/` | Build artifacts — never commit |

**Deleted files (do not recreate):** `cake-sqm.sh`, `cake-sqm.service`, `sqm-qos/`, `net-latency/` (replaced by the unified `net-tune/` service).

## Skills — task-specific procedures live in `.claude/skills/`

Each skill owns one full workflow. Invoke it instead of re-deriving the steps; CLAUDE.md records only the durable rules.

| Skill | Use when |
|---|---|
| `kernel-build` | building with makepkg, triaging a build failure, verifying BTF/vmlinux after a build |
| `kernel-version-bump` | bumping to a new Linux RC/release, refreshing the CachyOS `01xx` squashes |
| `patch-audit` | ingesting a **single named patch/commit**, swapping a patch for a newer revision, verifying provenance |
| `patch-sweep` | running the **periodic six-source sweep** for new hardware-relevant patches |
| `patch-cachy-branches` | refreshing the `0101`–`0109` CachyOS branch squashes from sirlucjan |
| `patch-cleanup` | reconciling on-disk patches with `source=()`, removing orphaned patches/artifacts |
| `docs-maintenance` | updating README/PATCH_SOURCES/GUIDE and committing a maintenance result |

## Patch numbering

Each range is a category; use the next unused number in the correct range.

| Range | Category | Source / how to obtain |
|---|---|---|
| `0001–0049` | Handmade local patches (Sleepy/Antigravity) | SMU14, DCN401, GFX12 hand-written fixes for this hardware |
| `0050–0099` | Upstream EDID/display ML patches not yet landed | `b4` mbox or freedesktop archives — verify with `git apply --check` against `repos/linux-7.2-rc7` |
| `0101–0113` | CachyOS branch squashes (0106 = off-target drops; 0110–0113 = CachyOS/linux-fork backports) | sirlucjan `-sep` dirs (see `patch-cachy-branches`); 0110–0113 from CachyOS/linux fork |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | drm-next / agd5f |
| `1100–1199` | AMD Display (DCN4, DCN42B, PSR, Replay, pstate, MCIF ARB) | drm-next |
| `1200–1299` | AMD Power Management (amd-pstate, cpufreq) | linux-pm / sirlucjan |
| `2000–2099` | Block / I/O schedulers (bfq, mq-deadline) | sirlucjan |
| `2100–2199` | Memory management (zstd, LRU-MARIE) | sirlucjan |
| `2200–2299` | CPU idle (NAP governor) | sirlucjan `nap-patches/` (firelzrd's repo is BORE-only) |
| `9000–9099` | agd5f staging backports | `git format-patch` from agd5f/linux — **verify all symbols exist in rc mainline first** |

All sirlucjan directories live under `repos/sirlucjan-kernel-patches/7.2/` (renamed from `7.2-rc/` when 7.2 released, 2026-08-19).
The CachyOS squashes are generated **against the actual series state** (rc7 + the `00xx` local/upstream patches), not a clean rc — the pre-CachyOS patches touch shared files like `drm_edid.c`. Two known conflicts handled inside the squashes: `0151` duplicates `0055`, and `0053` must be dropped when the hdmi branch is present.

## Full maintenance cycle

When asked to "update the kernel", "bump to a new RC", or "check for new patches", run the matching phases in order (a "check for new patches" request is phase 2 alone; a "build it" request is phase 3 alone):

1. **Version bump** — bump `_major`/`_minor`/`_rcver`/`_srcname` in PKGBUILD; rebase every patch; regenerate only the CachyOS squashes that fail `git apply --check`. Report every drop/regeneration with reasons before going further. → `kernel-version-bump`
2. **Patch audit** — check all six sources (drm-next, linux-next, linux-pm, amd-gfx ML, dri-devel ML, sirlucjan) plus the drm/amd work_items tracker for anything new; list candidates with source and priority before adding. → `patch-sweep`
3. **Build and fix** — `rm -rf src pkg && makepkg -f -s -c`; on failure diagnose per the rules below and keep iterating until the build succeeds or a MUST NOT rule blocks you. → `kernel-build`

## YOU MUST

1. Compile with `CC=clang LD=ld.lld LLVM=1 LLVM_IAS=1`. The PKGBUILD downloads a pre-built LLVM toolchain from kernel.org. Never change the toolchain.
2. `rm -rf src pkg` before every build. Old patched files cause false conflicts.
3. `updpkgsums` after any `source=()` change **or any patch-file edit** (checksums must match 1:1).
4. Keep every patch's original `From:`/`Date:`/`Subject:`/`Signed-off-by:` headers intact.
5. `patch --dry-run -Np1 < ../patchfile.patch` (and `git apply --check`) before adding any patch.
6. Resolve conflicts yourself — fix hunk offsets, regenerate from source, or drop the patch. Don't stall waiting on the user.
7. Clone with `--shallow-since="YYYY-MM-DD"` — never `--depth=1`.
8. Document every new patch in `PATCH_SOURCES.md` before adding it to `PKGBUILD`.
9. Verify BTF after every build. Both `CONFIG_TCP_CONG_BBR` (old) and `CONFIG_TCP_CONG_BBR3` define the same BTF kfunc symbol; only one can be built-in. The old BBR must stay disabled.
10. Use `DEBUG_INFO_DWARF5` (not `DWARF_TOOLCHAIN_DEFAULT`) with Clang 23 + pahole 1.31 — the default produces DWARF pahole 1.31 cannot convert to BTF.

## YOU MUST NOT

1. Never use `ld.mold` — crashes on kernel vDSO linker scripts (`fatal: unknown linker script token SECTIONS`).
2. Never access `lore.kernel.org` — anti-bot blocks automated agents. Use git repos or `lists.freedesktop.org` archives. The **drm/amd work items tracker** (`https://gitlab.freedesktop.org/drm/amd/-/work_items`) IS accessible — plain `curl` with **no User-Agent** returns real content (issues + events API; notes API is 401-gated).
3. Never hand-write or fabricate a patch diff. No traceable commit or mailing-list submission → tell the user, don't invent one. **AI-assisted patches ARE allowed** (2026-08-03): a named human author, `Signed-off-by`, an `Assisted-by:` trailer, and traceable provenance are required; fabricated diffs with no source remain forbidden.
4. Never add patches for hardware we don't have (Intel/Nvidia GPUs, ARM/SoC, Apple T2, laptop amps, TV tuners).
5. Never clone into `/tmp` — use `repos/` in the workspace.
6. Never run `make menuconfig`/`nconfig` unless the user explicitly asks.
7. Never remove a patch without explicit user approval, even if it looks irrelevant.
8. Never use `8.8.8.8` in network scripts — use Quad9 (`9.9.9.9`).
9. Never set `LLVM` to a path. `tools/bpf/resolve_btfids/Makefile` checks `ifeq ($(LLVM),1)`; a path value breaks BTF ID resolution. Prepend the LLVM `bin/` to `$PATH` and set `LLVM=1`.

## Kconfig essentials

The `scripts/config` calls below are already in `prepare()`. Full reference (incl. why each exists) is in `kernel-build/reference.md`.

```bash
# CPU + compiler
scripts/config -d GENERIC_CPU -e MZEN4
scripts/config -d LTO_NONE -e LTO_CLANG_THIN
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3
# TCP congestion (BBR3 only — old BBR causes BTF symbol collision)
scripts/config -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 --set-str DEFAULT_TCP_CONG "bbr3"
# Kernel command line (appended to bootloader params, does not override)
# pcie_aspm=off = !5538 SMU bus-drop stopgap; amdgpu.aspm=0/runpm=0 = conservative
# amdgpu-side stopgaps for the silent gaming freeze (SMU IF 0x2e vs 0x33). DPM stays on.
scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1 elevator=kyber pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0" -d CMDLINE_OVERRIDE
# BTF / debug (Clang 23 requires DWARF5)
scripts/config -e DEBUG_KERNEL -d DEBUG_INFO_NONE -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5 -e DEBUG_INFO_BTF
# BPF infrastructure (bpftune, sched-ext)
scripts/config -e BPF_SYSCALL -e BPF_TRACING -e BPF_EVENTS -e BPF_KPROBE_OVERRIDE \
               -e KPROBES -e KPROBE_EVENTS -e UPROBES -e UPROBE_EVENTS \
               -e KALLSYMS -e KALLSYMS_ALL \
               -e FTRACE -e FTRACE_SYSCALLS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER
# Memory management + CPU idle
scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE
scripts/config -e CPU_IDLE_GOV_NAP
# CAKE SQM ingress — NET_SCH_INGRESS is REQUIRED for download shaping; u32 is the classifier
scripts/config -e NET_SCH_INGRESS -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32
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

## net-tune service (CAKE SQM + latency tuning)

`net-tune/` ships one systemd service that applies low-latency ethernet settings
(`ENABLE_LATENCY`) and CAKE SQM shaping (`ENABLE_SQM`), each independently
toggleable in `/etc/net-tune.conf`. The shipped template defaults `ENABLE_SQM=yes`
(80/80 Mbit), so an unattended build installs shaping — it does not silently disable
it. BBR3 is the kernel-compiled default; the SQM part only applies CAKE. The route
probe uses Quad9 (`9.9.9.9`), never `8.8.8.8`.

Ingress shaping requires the `ingress` qdisc (`CONFIG_NET_SCH_INGRESS=y`) and a
**named** `ifb4cake` device (created explicitly with `ip link add ifb4cake type ifb`);
the u32 match-all idiom is used for the ingress redirect. The service verifies both
CAKE halves after applying and logs `net-tune: OK - CAKE shaping active (...)` or an
`ERROR` to journald — a missing ingress is no longer silent. Verify by hand:
`tc qdisc show dev <iface>` (expect root `cake` AND `qdisc ingress ffff:`),
`ip link show ifb4cake` (expect `state UP`, `qdisc cake`), and
`tc filter show dev <iface> ingress` (expect a `mirred` redirect).

## Version string

```bash
echo "-$pkgrel" > localversion.10-pkgrel
echo "-${pkgbase#linux-}" > localversion.20-pkgname
scripts/config --set-str LOCALVERSION ""
```

Result: `uname -r` → `7.2.0-rc7-1-sleepy`.

## Local model routing

When running with a local LLM server (not the hosted Anthropic API), `.claude/settings.json`
sets `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_MODEL`,
`ANTHROPIC_SMALL_FAST_MODEL`, and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` in its `env` block.
`CLAUDE_CODE_AUTO_COMPACT_WINDOW` prevents hard-stops from tokenizer drift between Claude Code
and the local server. On compaction, preserve: the current patch series (number range + subject),
its `PATCH_SOURCES.md` status, and any uncommitted diff. Push heavy one-shot work (cloning repos,
diffing archives) into subagents. Compact deliberately at phase boundaries; treat each version
bump as its own session.
