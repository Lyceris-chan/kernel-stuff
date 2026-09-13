# Configuration and packaging reference

Detail doc for the `kernel-build` skill. Load it when touching `prepare()`,
`scripts/config`, version strings, or the net-tune service.

## Contents

- [`scripts/config` calls in `prepare()`](#scriptsconfig-calls-in-prepare) — and what to re-disable after `olddefconfig`
- [Config traps](#config-traps) — settings that silently do nothing
- [Version string](#version-string)
- [net-tune](#net-tune)
- [Why not `ld.mold`](#why-not-ldmold)

## `scripts/config` calls in `prepare()`

These mirror `sleepy-next/PKGBUILD`. Read the PKGBUILD for the authoritative
list — this is the rationale, not a second source of truth.

```bash
# Memory management and CPU idle
scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE
scripts/config -e CPU_IDLE_GOV_NAP

# TCP congestion. Old BBR and BBR3 define the same BTF kfunc symbol, so only one
# can be built in — BBR3 wins and the old BBR is disabled here AND again after
# olddefconfig (dependency resolution pulls it back).
scripts/config -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 \
               --set-str DEFAULT_TCP_CONG "bbr3"

# I/O scheduler, modules this machine needs, bloat removal
scripts/config -e MQ_IOSCHED_KYBER --set-str DEFAULT_IOSCHED "kyber"
scripts/config -m USB_VIDEO_CLASS -m I2C_CHARDEV -m R8169
scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU -d DRM_VGEM -d DRM_VMWGFX \
               -d DRM_GMA500 -d DRM_UDL -d DRM_AST -d DRM_MGAG200 -d DRM_QXL \
               -d DRM_VIRTIO_GPU
scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN -d PARPORT -d FIREWIRE \
               -d PCMCIA -d GAMEPORT -d MOST -d GREYBUS -d COMEDI \
               -d ANDROID_BINDER_IPC -d ANDROID_BINDERFS -d F2FS_FS
scripts/config -d SECURITY_APPARMOR -d SECURITY_APPARMOR_DEBUG \
               -d SECURITY_APPARMOR_INTROSPECT_POLICY
scripts/config -d AUDIT -d AUDITSYSCALL -d AUDIT_ARCH -d SLUB_DEBUG
scripts/config -d MEDIA_PLATFORM_SUPPORT -d MEDIA_ANALOG_TV_SUPPORT \
               -d MEDIA_DIGITAL_TV_SUPPORT -d DVB_CORE -d DRM_PRIVACY_SCREEN

# CPU target and compiler
scripts/config -d GENERIC_CPU -e MZEN4
scripts/config -d LTO_NONE -e LTO_CLANG_THIN
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3

# Gates the 0110 CachyOS config-hooks backport (watermark_boost_factor=0,
# compaction_proactiveness=0, EEVDF base_slice, THP defer+madvise, split_lock).
scripts/config -e CACHY

# PCIe ASPM: there is no Kconfig "off" choice, so drop the compile-time policy
# and disable ASPM at runtime with pcie_aspm=off on the cmdline.
scripts/config -d PCIEASPM_PERFORMANCE -d PCIEASPM_POWERSAVE -d PCIEASPM_POWER_SUPERSAVE

# Built-in cmdline (appended to bootloader params; CMDLINE_OVERRIDE stays off)
# amdgpu.dcdebugmask=0x800 was dropped in pkgrel 11: it was masking the display
# "box", which is a COSMIC overlay-plane bug, not an IPS one.
scripts/config -e CMDLINE_BOOL \
  --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0" \
  -d CMDLINE_OVERRIDE

# BTF and debug. Clang 23 requires DWARF5 explicitly; the toolchain default
# produces DWARF pahole 1.31 cannot convert to BTF.
scripts/config -e DEBUG_KERNEL -d DEBUG_INFO_NONE \
               -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5 \
               -e DEBUG_INFO_BTF

# BPF infrastructure (bpftune, sched-ext)
scripts/config -e BPF_SYSCALL -e BPF_TRACING -e BPF_EVENTS -e BPF_KPROBE_OVERRIDE \
               -e KPROBES -e KPROBE_EVENTS -e UPROBES -e UPROBE_EVENTS \
               -e KALLSYMS -e KALLSYMS_ALL -e FTRACE -e FTRACE_SYSCALLS \
               -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER

# CAKE SQM ingress. NET_SCH_INGRESS is required for download shaping; u32 is the
# classifier the service uses.
scripts/config -e NET_SCH_INGRESS -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32

# Version string
scripts/config --set-str LOCALVERSION ""
```

### Re-disabled after `olddefconfig`

Dependency resolution turns these back on, so `prepare()` disables them again
after the config is regenerated:

```bash
scripts/config -d TCP_CONG_BBR          # BTF symbol collision with BBR3
scripts/config -d CHROMEOS_PRIVACY_SCREEN
scripts/config -d VIRT_DRIVERS
scripts/config -d PCI_TSM
scripts/config -d VIRTIO_FS
scripts/config -d X86_PLATFORM_DRIVERS_UNIWILL
```

## Config traps

- **`--set-str` on a symbol that no longer exists is silently dropped** by
  `olddefconfig`. Two live examples: `DEFAULT_IOSCHED` (gone since the blk-mq
  rework — the effective NVMe scheduler comes from udev's
  `60-ioschedulers.rules`) and `MQ_IOSCHED_ADIOS` (no patch adds `block/adios.c`).
  Grep the tree for the symbol before trusting a `--set-str` or `-e` line.
- **A `select`ed symbol cannot be disabled.** `RESCTRL_FS` and `SND_INTEL_NHLT`
  come back after `olddefconfig` because another option hard-selects them.
  Disable the selector instead, or accept the bloat — and verify the built
  `.config` afterwards.
- **Editing any `.patch` file changes its BLAKE2 checksum**, even a
  commit-message-only edit. Run `updpkgsums` after any patch change or makepkg
  fails the source-validity check.

## Version string

```bash
echo "-$pkgrel" > localversion.10-pkgrel
echo "-${pkgbase#linux-}" > localversion.20-pkgname
scripts/config --set-str LOCALVERSION ""
```

Resolves to `uname -r` → `<version>-<pkgrel>-sleepy-next`.

## net-tune

See `sleepy-next/net-tune/README.md` for the service, its configuration, and the
manual verification commands.

## Why not `ld.mold`

Crashes on the kernel's vDSO linker scripts (`unknown linker script token`). If a
future patch or config change pulls it in as a dependency or default, force back
to `ld.lld` — never adopt `ld.mold` for this build.
