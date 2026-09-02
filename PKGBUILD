# Maintainer: Peter Jung ptr1337 <admin@ptr1337.dev>
# Maintainer: Piotr Gorski <piotrgorski@cachyos.org>
# Maintainer: Vasiliy Stelmachenok <ventureo@cachyos.org>
# Contributor: Jan Alexander Steffens (heftig) <jan.steffens@gmail.com>
# Contributor: Tobias Powalowski <tpowa@archlinux.org>
# Contributor: Thomas Baechler <thomas@archlinux.org>

### BUILD OPTIONS
# Set these variables to ANYTHING that is not null or choose proper variable to enable them

### Selecting CachyOS config
: "${_cachy_config:=no}"

### Selecting the CPU scheduler
# ATTENTION - only one of the following values can be selected:
# 'bore' - select 'Burst-Oriented Response Enhancer'
# 'bmq' - select 'BMQ Scheduler'
# 'hardened' - select 'BORE Scheduler hardened' ## kernel with hardened config and hardening patches with the bore scheduler
# 'cachyos' - select 'CachyOS Default Scheduler (EEVDF)'
# 'eevdf' - select 'EEVDF Scheduler'
# 'rt' - select EEVDF, but includes a series of realtime patches
# 'rt-bore' - select Burst-Oriented Response Enhancer, but includes a series of realtime patches
: "${_cpusched:=cachyos}"

### Tweak kernel options prior to a build via nconfig
: "${_makenconfig:=no}"

### Tweak kernel options prior to a build via xconfig
: "${_makexconfig:=no}"

# Compile ONLY used modules to VASTLYreduce the number of modules built
# and the build time.
#
# To keep track of which modules are needed for your specific system/hardware,
# give module_db script a try: https://aur.archlinux.org/packages/modprobed-db
# This PKGBUILD read the database kept if it exists
#
# More at this wiki page ---> https://wiki.archlinux.org/index.php/Modprobed-db
: "${_localmodcfg:=no}"

# Path to the list of used modules
: "${_localmodcfg_path:="$HOME/.config/modprobed.db"}"

# Use the current kernel's .config file
# Enabling this option will use the .config of the RUNNING kernel rather than
# the ARCH defaults. Useful when the package gets updated and you already went
# through the trouble of customizing your config options.  NOT recommended when
# a new kernel is released, but again, convenient for package bumps.
: "${_use_current:=no}"

### Enable KBUILD_CFLAGS -O3
: "${_cc_harder:=yes}"

### Set performance governor as default
: "${_per_gov:=no}"

### Enable TCP_CONG_BBR3
: "${_tcp_bbr3:=yes}"

### Running with a 1000HZ, 750Hz, 600 Hz, 500Hz, 300Hz, 250Hz and 100Hz tick rate
: "${_HZ_ticks:=1000}"

## Choose between periodic, idle or full
### Full tickless can give higher performances in various cases but, depending on hardware, lower consistency.
: "${_tickrate:=full}"

## Choose between full, lazy or dynamic
# Full: Makes all non-critical kernel code preemptible to reduce latency
# Lazy: Same as full but instead of preempting immediately it waits for signals from the scheduler
#       in an attempt to boost throughput.
#       In practice, this doesn't seem to perform well as both throughput and latency suffer
#       compared to full.
: "${_preempt:=full}"

### Transparent Hugepages
# ATTENTION - one of two predefined values should be selected!
# 'always' - always enable THP
# 'madvise' - madvise, prevent applications from allocating more memory resources than necessary
# More infos here:
# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/performance_tuning_guide/sect-red_hat_enterprise_linux-performance_tuning_guide-configuring_transparent_huge_pages
: "${_hugepage:=always}"

# CPU compiler optimizations - Defaults to native if left empty
# - "native" (use compiler autodetection)
# - "zen4" (Use znver4 compiler optimizations)
# - "generic" (kernel's default - to share the package between machines with different CPU µarch as long as they are x86-64)
: "${_processor_opt:=zen4}"

# Clang LTO mode, only available with the "llvm" compiler - options are "none", "full" or "thin".
# ATTENTION - one of three predefined values should be selected!
# "full: uses 1 thread for Linking, slow and uses more memory, theoretically with the highest performance gains."
# "thin: uses multiple threads, faster and uses less memory, may have a lower runtime performance than Full."
# "thin-dist: Similar to thin, but uses a distributed model rather than in-process: https://discourse.llvm.org/t/rfc-distributed-thinlto-build-for-kernel/85934"
# "none: disable LTO
: "${_use_llvm_lto:=thin}"

# Use suffix -lto only when requested by the user
# yes - enable -lto suffix
# no - disable -lto suffix
# https://github.com/CachyOS/linux-cachyos/issues/36
: "${_use_lto_suffix:=no}"

# Use suffix -gcc when requested by the user
# Enabled by default to show the difference between LTO kernels and GCC kernels
: "${_use_gcc_suffix:=yes}"

# KCFI is a proposed forward-edge control-flow integrity scheme for
# Clang, which is more suitable for kernel use than the existing CFI
# scheme used by CONFIG_CFI_CLANG. kCFI doesn't require LTO, doesn't
# alter function references to point to a jump table, and won't break
# function address equality.
: "${_use_kcfi:=no}"

# Build the zfs module in to the kernel
# WARNING: The ZFS module doesn't build with selected RT sched due to licensing issues.
# If you use ZFS, refrain from building the RT kernel
: "${_build_zfs:=no}"

# Builds the open nvidia module and package it into a own base
# This does replace the requirement of nvidia-open-dkms
# Use this only if you have Turing+ GPU
: "${_build_nvidia_open:=no}"

# Builds the r8125 module and package it into its own package
# Replaces requirement for r8125-dkms
# NOTE: dropped 2026-08-02 — the in-kernel r8169 driver covers the RTL8125B
# NIC; no out-of-tree module needed.
: "${_build_r8125:=no}"

# Build a debug package with non-stripped vmlinux
: "${_build_debug:=no}"

# Enable AUTOFDO_CLANG for the first compilation to create a kernel, which can be used for profiling
# Workflow:
# https://cachyos.org/blog/2411-kernel-autofdo/
# 1. Compile Kernel with _autofdo=yes and _build_debug=yes
# 2. Boot the kernel in QEMU or on your system, see Workload
# 3. Profile the kernel and convert the profile, see Generating the Profile for AutoFDO
# 4. Put the profile into the sourcedir
# 5. Run kernel build again with the _autofdo_profile_name path to profile specified
: "${_autofdo:=no}"

# Name for the AutoFDO profile
: "${_autofdo_profile_name:=}"

# Propeller should be applied, after the kernel is optimized with AutoFDO
# Workflow:
# 1. Proceed with above AutoFDO Optimization, but enable at the final compilation also _propeller
# 2. Boot into the AutoFDO Kernel and profile it
# 3. Convert the profile into the propeller profile, example:
# create_llvm_prof --binary=/usr/src/debug/linux-cachyos-rc/vmlinux --profile=propeller.data --format=propeller --propeller_output_module_name --out=propeller_cc_profile.txt --propeller_symorder=propeller_ld_profile.txt
# 4. Place the propeller_cc_profile.txt and propeller_ld_profile.txt into the srcdir
# 5. Enable _propeller_prefix
: "${_propeller:=no}"

# Enable this after the profiles have been generated
: "${_propeller_profiles:=no}"

# ATTENTION: Do not modify after this line
_is_lto_kernel() {
    [[ "$_use_llvm_lto" = "thin" || "$_use_llvm_lto" = "full"  || "$_use_llvm_lto" = "thin-dist" ]]
    return $?
}

_is_ci_build() {
    [[ -n "$CI" || -n "$GITHUB_RUN_ID" ]]
    return $?
}

if _is_lto_kernel && [ "$_use_lto_suffix" = "yes"  ]; then
    _pkgsuffix="sleepy-next"
elif ! _is_lto_kernel && [ "$_use_gcc_suffix" = "yes" ]; then
    _pkgsuffix="sleepy-next"
else
    _pkgsuffix="sleepy-next"
fi

pkgbase="linux-$_pkgsuffix"
_major=7.2
_minor=0
_rcver=
pkgver=20260902
_tagrel=1
pkgrel=13
#_stable=${_major}.${_minor}
#_stable=${_major}
_stable=${_major}.${_minor}
# linux-next snapshot (the 7.3 merge-window content) for the 7.3 preview
_srctag=next-20260902
_srcname=${_srctag}
pkgdesc='Sleepy-next 7.3 preview kernel: linux-next 20260902 + sleepy hardware merges (CachyOS optimizations included)'
_kernver="$pkgver-$pkgrel"
_kernuname="${pkgver}-${_pkgsuffix}"
arch=('x86_64')
url="https://github.com/CachyOS/linux-cachyos"
license=('GPL-2.0-only')
options=('!strip' '!debug' '!lto')
makedepends=(
  bc
  binutils
  cpio
  gettext
  glibc
  libelf
  libgcc
  openssl
  pahole
  perl
  python
  rust
  rust-bindgen
  rust-src
  tar
  xxhash
  xz
  zlib
  zstd
)

_patchsource="https://raw.githubusercontent.com/cachyos/kernel-patches/master/${_major}"
_nv_ver=610.43.02
_nv_pkg="NVIDIA-Linux-x86_64-${_nv_ver}"
_nv_open_pkg="NVIDIA-kernel-module-source-${_nv_ver}"
source=(
  "https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git/snapshot/next-20260902.tar.gz"
  "config"
  "patches/0001-0049/0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch"
  "patches/0001-0049/0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch"
  "patches/0001-0049/0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch"
  "patches/0001-0049/0004-drm-amd-pm-Disable-deep-sleep-in-PROFILE_PEAK.patch"
  "patches/0001-0049/0005-drm-amd-pm-Disable-SMU14-mode1-reset-for-SR-IOV.patch"
  "patches/0001-0049/0006-drm-amd-pm-Add-bounds-checking-for-SMU14-I2C-command.patch"
  "patches/0001-0049/0007-drm-amd-pm-Remove-redundant-mutex-lock-in-SMU14-I2C-.patch"
  "patches/0001-0049/0010-drm-amdgpu-gfx12-Fix-named-barrier-restore-in-trap-handler.patch"
  "patches/0001-0049/0030-drm-amd-display-Proactively-shrink-DET-for-pipes-los.patch"
  "patches/0001-0049/0031-drm-amd-display-Fix-memory-leak-in-DCN20-link-encode.patch"
  "patches/0001-0049/0032-drm-amd-display-Fix-OOB-array-access-for-HPO-FRL-lin.patch"
  "patches/0001-0049/0033-drm-amd-display-Fix-missing-HPO-FRL-link-encoder-reg.patch"
  "patches/0001-0049/0034-drm-amd-display-Prevent-memory-leak-during-IRQ-servi.patch"
  "patches/0050-0099/0050-drm-edid-Parse-AMD-VSDB-for-FreeSync-refresh-range.patch"
  "patches/0050-0099/0055-drm-edid-parse-HDMI-2.1-gaming-ALLM-VRR-caps-from-HF-VSDB.patch"
  "patches/0050-0099/0059-drm-amd-display-add-2.1-freesync-support-for-amd-vsdb-edid-block.patch"
  "patches/0050-0099/0060-drm-amd-display-add-hdmi-2.1-vrr-support-from-hf-vsdb.patch"
  "patches/0050-0099/0061-drm-amd-display-enable-hdmi-allm-for-gaming-vrr.patch"
  "patches/0101-0113/0101-cachy-bbr3.patch"
  "patches/0101-0113/0102-cachy-kbuild.patch"
  "patches/0101-0113/0103-cachy-cpu-isa.patch"
  "patches/0101-0113/0110-cachy-config-hooks.patch"
  "patches/0101-0113/0111-cachy-acpi-disable-bus-master-check-for-AMD.patch"
  "patches/0101-0113/0112-cachy-amdgpu-avoid-evicting-resources-at-S5.patch"
  "patches/1000-1099/1004-drm-amdgpu-gmc9-disallow-gfxoff-around-TLB-flushes.patch"
  "patches/1000-1099/1005-drm-amdgpu-gmc10-disallow-gfxoff-around-TLB-flushes.patch"
  "patches/1000-1099/1006-drm-amdgpu-gmc11-disallow-gfxoff-around-TLB-flushes.patch"
  "patches/1000-1099/1007-drm-amdgpu-gmc12-disallow-gfxoff-around-TLB-flushes.patch"
  "patches/1000-1099/1008-drm-amdgpu-add-an-buffer-funcs-callback-for-TLB-inva.patch"
  "patches/1000-1099/1009-drm-amdgpu-sdma5.0-add-tlb-invalidation-buffer-func-.patch"
  "patches/1000-1099/1010-drm-amdgpu-sdma5.2-add-tlb-invalidation-buffer-func-.patch"
  "patches/1000-1099/1011-drm-amdgpu-sdma6-add-tlb-invalidation-buffer-func-ca.patch"
  "patches/1000-1099/1012-drm-amdgpu-sdma7-add-tlb-invalidation-buffer-func-ca.patch"
  "patches/1000-1099/1013-drm-amdgpu-add-core-helper-to-do-TLB-invalidation-vi.patch"
  "patches/1000-1099/1014-drm-amdgpu-gmc-add-more-gmc-tlb-inv-helpers.patch"
  "patches/1000-1099/1015-drm-amdgpu-gmc10-switch-to-new-gmc-tlb-inv-helpers.patch"
  "patches/1000-1099/1016-drm-amdgpu-gmc11-switch-to-new-gmc-tlb-inv-helpers.patch"
  "patches/1000-1099/1017-drm-amdgpu-gmc12-switch-to-new-gmc-tlb-inv-helpers.patch"
  "patches/1000-1099/1018-drm-amdgpu-Switch-order-of-GC-and-Display-IP-blocks.patch"
  "patches/1000-1099/1026-drm-amdkfd-fix-NULL-pointer-dereference-in-GFX12-CRIU.patch"
  "patches/1000-1099/1027-drm-amdgpu-force-complete-the-MES-scheduler-ring-fence-on-reset.patch"
  "patches/1000-1099/1055-drm-amd-pm-fix-incorrect-avg-vcn-utilization-in-gpu_metrics.patch"
  "patches/1000-1099/1056-drm-sched-lock-drm_sched_entity_is_idle.patch"
  "patches/1000-1099/1058-drm-amdgpu-track-suboptimal-always-valid-bos.patch"
  "patches/1000-1099/1059-drm-amdgpu-restrict-BAR0-fallback-read-to-SR-IOV-VFs-only.patch"
  "patches/1000-1099/1060-drm-amdgpu-cancel-hang_detect_work-before-taking-userq-mutex.patch"
  "patches/1100-1199/1137-drm-amd-display-fallback-to-drm-core-amd-vsdb-freesync.patch"
  "patches/1100-1199/1138-drm-amd-display-pull-colorops-into-state-when-recreating-a-plane.patch"
  "patches/1100-1199/1139-drm-amd-display-fix-missing-blend-mode-prop-warning.patch"
  "patches/1100-1199/1141-drm-amd-display-skip-receiver-power-control-without-AUX.patch"
  "patches/1100-1199/1142-drm-amd-display-close-DDC-on-I2C-engine-setup-failure.patch"
  "patches/1100-1199/1143-drm-amd-display-fall-back-to-software-I2C-on-hardware-engine-failure.patch"
  "patches/1100-1199/1144-drm-amd-display-enable-HDMI-FRL-by-default.patch"
  "patches/1200-1299/1201-cpufreq-amd-pstate-Update-cppc_req_cached-before-w.patch"
  "patches/1200-1299/1202-cpufreq-amd-pstate-Add-per-core-EPP-boost-for-rec.patch"
  "patches/1200-1299/1203-Documentation-amd-pstate-Document-the-epp_boost-pa.patch"
  "patches/1200-1299/1210-acpi-cppc-validate-the-cpc-package-header.patch"
  "patches/1200-1299/1211-acpi-cppc-validate-cpc-entry-and-control-semantics.patch"
  "patches/1200-1299/1212-acpi-cppc-propagate-performance-control-write-errors.patch"
  "patches/1200-1299/1213-acpi-cppc-use-64-bit-masks-for-register-fields.patch"
  "patches/1200-1299/1214-acpi-cppc-serialize-pcc-single-register-payload-updates.patch"
  "patches/1200-1299/1215-acpi-cppc-serialize-pcc-epp-payload-updates.patch"
  "patches/1200-1299/1216-acpi-cppc-release-cpc-descriptors-through-kobject.patch"
  "patches/1200-1299/1217-acpi-cppc-release-pcc-data-after-probe-failures.patch"
  "patches/1200-1299/1218-acpi-cppc-reject-unsafe-cross-cpu-systemmemory-rmw.patch"
  "patches/1200-1299/1219-acpi-cppc-reject-direct-reads-of-write-only-controls.patch"
  "patches/1200-1299/1220-acpi-cppc-acpi-cppc-validate-and-access-pcc-register-layouts.patch"
  "patches/1200-1299/1221-acpi-cppc-acpi-cppc-validate-systemio-register-layouts.patch"
  "patches/1200-1299/1222-acpi-cppc-acpi-cppc-validate-pcc-overlaps-across-processors.patch"
  "patches/1200-1299/1223-acpi-cppc-acpi-cppc-validate-systemio-overlaps-across-processors.patch"
  "patches/1200-1299/1224-acpi-cppc-acpi-cppc-clear-performance-limited-without-a-stale-read.patch"

  "patches/2000-2099/2000-block-mq-deadline-pass-in-queue-directly-to-dd_inser.patch"
  "patches/2000-2099/2001-block-mq-deadline-skip-expensive-merge-lookups-if-co.patch"
  "patches/2000-2099/2002-block-bfq-pass-in-queue-directly-to-bfq_insert_reque.patch"
  "patches/2000-2099/2003-block-bfq-serialize-request-dispatching.patch"
  "patches/2000-2099/2004-block-bfq-skip-expensive-merge-lookups-if-contended.patch"
  "patches/2100-2199/2100-zstd-7.2-merge-v1.6.0-into-kernel-tree.patch"
  "patches/2100-2199/2101-mm-next-introduce-LRU-MARIE-0.11.0.patch"
  "patches/2100-2199/2120-mm-gup-mm-gup-break-out-gup-fill-pages-helper.patch"
  "patches/2100-2199/2121-mm-gup-mm-gup-convert-follow-page-mask-to-return-a-long.patch"
  "patches/2100-2199/2122-mm-gup-mm-gup-split-follow-page-pte-commit-out-of.patch"
  "patches/2100-2199/2123-mm-gup-mm-gup-break-out-follow-one-pte-helper.patch"
  "patches/2100-2199/2124-mm-gup-mm-gup-fill-the-pages-array-outside-the-pud-pmd-lock.patch"
  "patches/2100-2199/2125-mm-gup-mm-gup-return-a-huge-page-s-full-count-from.patch"
  "patches/2100-2199/2126-mm-gup-mm-gup-walk-multiple-PTEs-per-follow-page-pte-call.patch"
  "patches/2100-2199/2127-mm-gup-mm-gup-batch-contiguous-same-folio-PTEs-into-one.patch"
  "patches/2100-2199/2128-zstd-use-ZSTD_cpuSupportsBmi2-in-ZSTD_initStaticCCtx.patch"
  "patches/2100-2199/2129-zstd-skip-BMI2-probe-when-dynamic-BMI2-dispatch-disabled.patch"
  "patches/2100-2199/2130-zstd-probe-CPU-for-BMI2-support-only-once.patch"
  "patches/2200-2299/2200-7.2-nap-v0.5.0.patch"
  "patches/9000-9099/9007-drm-gfx12-Program-DB_RING_CONTROL.patch"
  "patches/9000-9099/9011-drm-amdgpu-Respect-noretry-flag-for-retry-faults-on-GFX12.1.patch"
  "patches/9000-9099/9012-drm-amdgpu-gfxhub-Enable-retry-fault-interrupts-when-needed.patch"
  "patches/9000-9099/9013-drm-amdgpu-ih-Dont-perturb-HW-registers-when-accessing-soft-IH.patch"
  "patches/9000-9099/9014-drm-amdgpu-ih-Add-retry_cam_ack-IH-function-pointer.patch"
  "patches/9000-9099/9015-drm-amdgpu-ih6.1-Use-IH_SW_RING_SIZE-for-soft-IH-ring.patch"
  "patches/9000-9099/9016-drm-amdgpu-ih7.0-Use-IH_SW_RING_SIZE-for-soft-IH-ring.patch"
  "patches/9000-9099/9017-drm-amdgpu-gmc11-Pass-cam_index-to-retry-fault-handler.patch"
  "patches/9000-9099/9018-drm-amdgpu-gmc12-Pass-cam_index-to-retry-fault-handler.patch"
  "patches/9000-9099/9019-drm-amdgpu-gmc12-Use-AMDGPU_PTE_IS_PTE-flag-for-init_pte_flags.patch"
  "patches/9000-9099/9020-drm-amdgpu-vm-Use-init-PTE-flags-and-NOALLOC-in-handle_fault.patch"
  "patches/9000-9099/9021-drm-amdgpu-ih6.0-Use-MMIO-ACK-for-retry-CAM-on-IH-6.0.patch"
  "patches/9000-9099/9022-drm-amdgpu-ih7.0-Use-MMIO-ACK-instead-of-doorbell-for-retry-CAM.patch"
  "patches/9000-9099/9023-drm-amdgpu-ih6.0-Enable-retry-CAM-on-Navi-3-dGPUs.patch"
  "patches/9000-9099/9024-drm-amdgpu-ih7.0-Enable-retry-CAM-on-Navi-4-dGPUs.patch"
  "patches/9000-9099/9034-drm-amdgpu-fix-VM-update-overrun-on-non-4K-page-kernels.patch"
  "patches/9000-9099/9035-drm-amdgpu-add-the-BO-va-mapping-offset-when-kmapping-an-IB.patch"
  "patches/9000-9099/9038-drm-amdgpu-reject-PRT-mappings-as-user-queue-buffer-VAs.patch"
  "patches/9000-9099/9039-drm-amdgpu-userq-bound-the-eviction-fence-rearm-retry-loop.patch"
  "patches/9000-9099/9040-drm-amdgpu-free-userptr-HMM-ranges-on-the-CS-error-path.patch"
  "patches/9000-9099/9044-drm-amdgpu-userq-skip-unmapped-queues-in-wait_for_signal.patch"
  "patches/9000-9099/9046-amdkfd-fix-integer-overflow-in-queue-ring-buffer-size.patch"
)

# makepkg 7.1.0 resolves local sources by basename in the PKGBUILD directory
# (get_filename strips directory prefixes). The patches live in patches/<range>/
# subfolders for a clean repo view, so create root-level symlinks here — this
# body code runs when makepkg sources the PKGBUILD, before source resolution.
# The symlinks are gitignored (see .gitignore) so the repo root stays clean.
for _sleepy_patch in "${source[@]}"; do
  case "$_sleepy_patch" in
    patches/*.patch)
      _sleepy_base="${_sleepy_patch##*/}"
      [[ -e "$_sleepy_base" ]] || ln -s "$_sleepy_patch" "$_sleepy_base"
      ;;
  esac
done
unset _sleepy_patch _sleepy_base

validpgpkeys=(
  E18447AC260021D31F3FF6C4C8A2A4774B8B63C4  # Eric Naim <dnaim@cachyos.org>
  E8B9AA39F054E30E8290D492C3C4820857F654FE  # Peter Jung <admin@ptr1337.dev>
)
# Pre-built LLVM toolchain: the official GitHub llvm-project release asset
# LLVM-23.1.0-Linux-X64.tar.xz (llvmorg-23.1.0, added to source() below) is the
# toolchain actually used. It links against ICU 70 (Arch ships ICU 78), so the
# libs are bundled via the llvm-icu70-libs source. The kernel.org
# ClangBuiltLinux weekly-rc auto-fetch was dropped 2026-09-02 (legacy
# _kernel_org_llvm_tarball was never added to source()).
: "${_use_kernel_org_llvm:=yes}"
: "${_llvm_dir_name:=LLVM-23.1.0-Linux-X64}"

_set_build_flags() {
    if _is_lto_kernel; then
        if [ "$_use_kernel_org_llvm" = "yes" ]; then
            export PATH="${srcdir}/${_llvm_dir_name}/bin:${PATH}"
            # GitHub LLVM 23.1.0 needs ICU 70 (see llvm-icu70-libs source)
            mkdir -p "${srcdir}/${_llvm_dir_name}/lib"
            tar xzf "$srcdir/llvm-icu70-libs.tar.gz" -C "${srcdir}/${_llvm_dir_name}/lib"
            export LD_LIBRARY_PATH="${srcdir}/${_llvm_dir_name}/lib:${LD_LIBRARY_PATH}"
            BUILD_FLAGS=(
                CC=clang
                LD=ld.lld
                LLVM=1
                LLVM_IAS=1
                PAHOLE=/usr/bin/pahole
            )
        else
            makedepends+=(clang llvm lld)
            BUILD_FLAGS=(
                CC=clang
                LD=ld.lld
                LLVM=1
                LLVM_IAS=1
                PAHOLE=/usr/bin/pahole
            )
        fi
    fi
}

# WARNING The ZFS module doesn't build with selected RT sched due to licensing issues.
if [[ "$_cpusched" = "rt" || "$_cpusched" = "rt-bore" ]]; then
    unset _build_zfs
fi

# ZFS support
if [ "$_build_zfs" = "yes" ]; then
    makedepends+=(git)
    source+=("git+https://github.com/cachyos/zfs.git#commit=c681af76c5a6a15caada25eb13090e41218c7831")
fi


if [ "$_build_nvidia_open" = "yes" ]; then
    source+=("https://download.nvidia.com/XFree86/${_nv_open_pkg%"-$_nv_ver"}/${_nv_open_pkg}.tar.xz")
fi

# Use generated AutoFDO Profile
if [ "$_autofdo" = "yes" ] && [ -n "$_autofdo_profile_name" ]; then
    if [ -e "$_autofdo_profile_name" ]; then
        source+=("$_autofdo_profile_name")
    else
        _die "Failed to find file ${_autofdo_profile_name}"
    fi
fi

# Use generated Propeller Profile
if [ "$_propeller" = "yes" ] && [ "$_propeller_profiles" = "yes" ]; then
    source+=(propeller_cc_profile.txt
             propeller_ld_profile.txt)
fi

if [ "$_build_r8125" = "yes" ]; then
    source+=("git+https://github.com/aravance/r8125.git")
fi

## List of CachyOS schedulers
case "$_cpusched" in
    bore|rt-bore|hardened) # CachyOS Scheduler (BORE)
        # Dropped for sched_ext
        ;;
    bmq) ## Project C Scheduler
        # Dropped for sched_ext
        ;;
    hardened) ## Hardened Patches
        source+=("${_patchsource}/misc/0001-hardened.patch");;
    rt|rt-bore) ## RT patches
        source+=("${_patchsource}/misc/0001-rt-i915.patch");;
esac

export KBUILD_BUILD_HOST="$(hostname)"
export KBUILD_BUILD_USER="$(whoami)"
export KBUILD_BUILD_TIMESTAMP="$(date -Ru${SOURCE_DATE_EPOCH:+d @$SOURCE_DATE_EPOCH})"

_die() { error "$@" ; exit 1; }

prepare() {
    _set_build_flags
    # Ensure clean patch application even if makepkg is re-run on a previously patched tree
    if [ -d "$_srcname" ]; then
        echo "Resetting source tree to ensure clean patch application..."
        rm -rf "$_srcname"
        bsdtar -xf "$srcdir/${_srctag}.tar.gz" -C "$srcdir"
    fi

    cd "$_srcname"

    echo "Setting version..."
    
    # Interactive net-tune prompt (CAKE SQM + latency tuning). Default is now
    # ENABLE_SQM=yes — the shipped net-tune/net-tune.conf template enables SQM,
    # so a skipped prompt (no TTY) or Enter installs shaping by default. An
    # explicit "n" writes a disabled conf so the off path is still honored.
    if [ -t 0 ] && [ -z "$AUTO_BUILD" ]; then
        echo -e "\nEnable CAKE SQM bandwidth shaping (net-tune)? (Y/n)"
        read -r enable_sqm || enable_sqm="y"
        if [[ "$enable_sqm" =~ ^[Yy]$ ]]; then
            touch "$startdir/src/.enable_sqm"
            echo "Enter your true DOWNLOAD speed in Mbit/s [80]:"
            read -r dl_mbit || dl_mbit=""
            dl_mbit="${dl_mbit:-80}"
            echo "Enter your true UPLOAD speed in Mbit/s [80]:"
            read -r ul_mbit || ul_mbit=""
            ul_mbit="${ul_mbit:-80}"
            cat > "$startdir/src/net-tune.conf" << EOF
ENABLE_SQM=yes
DOWNLOAD_MBIT="$dl_mbit"
UPLOAD_MBIT="$ul_mbit"
ENABLE_LATENCY=yes
EOF
            echo "net-tune configured: SQM ${dl_mbit}/${ul_mbit} Mbit + latency tuning."
        else
            echo "Disabling CAKE SQM (latency tuning still applies)."
            cat > "$startdir/src/net-tune.conf" << EOF
ENABLE_SQM=no
ENABLE_LATENCY=yes
EOF
        fi
    fi
    echo "-$pkgrel" > localversion.10-pkgrel
    # kernel identity: sleepy-next-<nextdate> (single 'next'); the linux-next
    # tree's localversion-next would otherwise double it (next-YYYYMMDD).
    echo "-${pkgbase#linux-}-${_srctag#next-}" > localversion.20-pkgname
    rm -f localversion-next
    
    # Apply the 7.2 sleepy series to next-20260828: dry-run first so a patch
    # that does not apply cleanly (e.g. LRU-MARIE 0.10.5, which needs a 7.3
    # port) is SKIPPED entirely instead of leaving a half-applied tree.
    # 0107-cachy-hdmi is not in source=() — the 7.3 base already has the clean
    # upstream HDMI path (dc_edid_parser + update_freesync_caps + FRL fixes).
    local src
    for patch in "${source[@]}"; do
        patch="${patch%%::*}"
        src="${patch##*/}"
        src="${src%.zst}"
        [[ $src = *.patch ]] || continue
        echo "Applying patch $src..."
        if patch -p1 --forward --dry-run -F2 < "../$src" > /tmp/sleepy-patch.log 2>&1; then
            patch -p1 --forward -F2 < "../$src" > /tmp/sleepy-patch.log 2>&1
        else
            echo "  SKIPPED: $(grep -m1 FAILED /tmp/sleepy-patch.log || echo does not apply cleanly)"
        fi
    done
    find . -name "*.rej" -delete

    # === CONFIG: Use CachyOS base config, then make olddefconfig to silently resolve new options ===
    echo "Setting config..."
    cp ../config .config
    
    # Apply our minimal overrides BEFORE olddefconfig so they stick
    python3 "${startdir}/disable_configs.py" .config
    scripts/config --set-str LOCALVERSION ""
    scripts/config -d DRM_PRIVACY_SCREEN
    scripts/config -d MEDIA_PLATFORM_SUPPORT -d MEDIA_ANALOG_TV_SUPPORT -d MEDIA_DIGITAL_TV_SUPPORT -d MEDIA_RADIO_SUPPORT -d MEDIA_SDR_SUPPORT -d DVB_CORE
    scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN -d PARPORT -d FIREWIRE -d PCMCIA -d GAMEPORT -d MOST -d GREYBUS -d COMEDI -d ANDROID_BINDER_IPC -d ANDROID_BINDERFS -d ANDROID_BINDER_DEVICES -d F2FS_FS
    scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU -d DRM_VGEM -d DRM_VMWGFX -d DRM_GMA500 -d DRM_UDL -d DRM_AST -d DRM_MGAG200 -d DRM_QXL -d DRM_VIRTIO_GPU
    scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE -e CPU_IDLE_GOV_NAP -e MQ_IOSCHED_ADIOS -e MQ_IOSCHED_KYBER --set-str DEFAULT_IOSCHED "kyber" -m USB_VIDEO_CLASS -m I2C_CHARDEV -m R8169 -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 --set-str DEFAULT_TCP_CONG "bbr3"
    # ASPM: OFF (was PERFORMANCE). There is no Kconfig "off" policy for PCIe ASPM —
    # the choice is BIOS-default/powersave/powersupersave/performance. The real
    # "off" is the runtime pcie_aspm=off param (the drm/amd !5538 SMU bus-drop
    # stopgap an AMD engineer recommended), passed via the built-in CMDLINE below.
    # We drop the compile-time PERFORMANCE policy so nothing forces a policy;
    # olddefconfig leaves the base PCIEASPM_DEFAULT (BIOS default), and the
    # pcie_aspm=off param overrides it at boot to disable ASPM entirely.
    scripts/config -d PCIEASPM_PERFORMANCE -d PCIEASPM_POWERSAVE -d PCIEASPM_POWER_SUPERSAVE

    scripts/config -d GENERIC_CPU -e MZEN4
    scripts/config -d LTO_NONE -e LTO_CLANG_THIN
    scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3
    scripts/config -e CACHY   # gates the 0110 CachyOS config-hooks backport
    # pcie_aspm=off: disable PCIe ASPM entirely — the !5538 SMU bus-drop stopgap.
    # amdgpu.aspm=0 / amdgpu.runpm=0: conservative amdgpu-side stopgaps for the
    # silent gaming freeze (SMU IF mismatch 0x2e vs 0x33, !5538) — no GPU ASPM or
    # BACO/runtime-PM power transitions. DPM stays on so clocks still downclock.
    # amdgpu.dcdebugmask=0x800 = DC_DISABLE_IPS: disables DCN4 Idle Power States.
    # On DCN401, IPS/DPG pipe-gating makes dc_get_flip_pending_on_otg()'s
    # hubp2_is_flip_pending() read return false (hubp->power_gated) while a flip
    # is still pending, so the VUPDATE_NO_LOCK handler delivers the flip event
    # before HW latches → the compositor re-paints a buffer still being scanned →
    # a fixed content-tracking square over app windows (the sleepy-next "box",
    # matches AMD drm/amd work item #5570 class). Verified fixed 2026-08-26 with
    # dcdebugmask=0x800 (0x20000 FAMS and 0x8 clock-gating did NOT help).
    # Appended to the bootloader params (CMDLINE_OVERRIDE is off); boots this kernel
    # with ASPM off regardless of the platform/BIOS default.
    scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1 pcie_aspm=off amdgpu.aspm=0 amdgpu.runpm=0 amdgpu.dcdebugmask=0x800" -d CMDLINE_OVERRIDE
    scripts/config -e DEBUG_KERNEL -d DEBUG_INFO_NONE -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5 -e DEBUG_INFO_BTF
    scripts/config -d SECURITY_APPARMOR -d SECURITY_APPARMOR_DEBUG -d SECURITY_APPARMOR_INTROSPECT_POLICY
    scripts/config -d AUDIT -d AUDITSYSCALL -d AUDIT_ARCH -d SLUB_DEBUG
    # Enable BPF, Kprobes, Kallsyms_all, and Tracing infrastructure for bpftune & sched_ext
    scripts/config -e BPF_SYSCALL -e BPF_TRACING -e BPF_EVENTS -e BPF_KPROBE_OVERRIDE \
                   -e KPROBES -e KPROBE_EVENTS -e UPROBES -e UPROBE_EVENTS \
                   -e KALLSYMS -e KALLSYMS_ALL \
                   -e FTRACE -e FTRACE_SYSCALLS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER
    # Enable IFB and Mirroring for CAKE SQM Ingress shaping.
    # NET_SCH_INGRESS is REQUIRED — without it the ingress qdisc does not exist
    # and net-tune's download shaping cannot be created at all.
    scripts/config -e NET_SCH_INGRESS -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32
    
    # olddefconfig: silently accepts Torvalds defaults for any NEW 7.2-rc1 options.

    # This is 100% non-interactive and will NEVER prompt or mutate existing config values.
    make "${BUILD_FLAGS[@]}" olddefconfig

    # These MUST be disabled AFTER olddefconfig — olddefconfig can auto-select
    # them (or re-enable them) based on dependency resolution:
    #   CHROMEOS_PRIVACY_SCREEN depends on ACPI+DRM (both y), auto-enabled →
    #   selects DRM_PRIVACY_SCREEN, but we disabled it above → modpost warning
    #   VIRT_DRIVERS selected by FUSE_FS→VIRTIO_FS or explicitly in CachyOS base
    #   PCI_TSM selected by CRYPTO_DEV_SP_PSP (via AMD_IOMMU=y) → also enables TSM
    scripts/config -d CHROMEOS_PRIVACY_SCREEN
    scripts/config -d VIRT_DRIVERS
    scripts/config -d PCI_TSM
    scripts/config -d VIRTIO_FS
    scripts/config -d X86_PLATFORM_DRIVERS_UNIWILL
    # Disable old BBRv1/v2 AFTER olddefconfig — tcp_bbr.c and tcp_bbr3.c both define
    # BTF_KFUNCS_START(tcp_bbr_check_kfunc_ids), causing resolve_btfids to crash with
    # exit 255. Disabling the old BBR removes the duplicate BTF symbol conflict.
    scripts/config -d TCP_CONG_BBR

    ### Prepared version
    make -s kernelrelease > version
    echo "Prepared $pkgbase version $(<version)"

    ### Running make nconfig
    [ "$_makenconfig" = "yes" ] && make "${BUILD_FLAGS[@]}" nconfig

    ### Running make xconfig
    [ "$_makexconfig" = "yes" ] &&  make "${BUILD_FLAGS[@]}" xconfig

    ### Save configuration for later reuse
    echo "Save configuration for later reuse..."
    local basedir="$(dirname "$(readlink "${srcdir}/config")")"
    cat .config > "${basedir}/config-${pkgver}-${pkgrel}${pkgbase#linux}"
}

_sign_modules() {
    msg2 "Signing modules in $1"
    local sign_script="${srcdir}/${_srcname}/scripts/sign-file"
    local sign_key="$(grep -Po 'CONFIG_MODULE_SIG_KEY="\K[^"]*' "${srcdir}/${_srcname}/.config")"
    if [[ ! "$sign_key" =~ ^/ ]]; then
        sign_key="${srcdir}/${_srcname}/${sign_key}"
    fi
    local sign_cert="${srcdir}/${_srcname}/certs/signing_key.x509"
    local hash_algo="$(grep -Po 'CONFIG_MODULE_SIG_HASH="\K[^"]*' "${srcdir}/${_srcname}/.config")"

    if [ "$_use_llvm_lto" != "none" ]; then
        local strip_bin="llvm-strip"
    else
        local strip_bin="strip"
    fi

    find "$1" -type f -name '*.ko' -print \
        -exec "${strip_bin}" --strip-debug '{}' \; \
        -exec "${sign_script}" "${hash_algo}" "${sign_key}" "${sign_cert}" '{}' \;
}

build() {
    _set_build_flags
    cd "$_srcname"
    make "${BUILD_FLAGS[@]}" -j"$(nproc)" all

    if ! _is_ci_build; then
        #make -C tools/bpf/bpftool vmlinux.h feature-clang-bpf-co-re=1
        echo "Skipping bpftool"
    fi

    local MODULE_FLAGS=(
       KERNEL_UNAME="${_kernuname}"
       IGNORE_PREEMPT_RT_PRESENCE=1
       SYSSRC="${srcdir}/${_srcname}"
       SYSOUT="${srcdir}/${_srcname}"
    )

    if [ "$_build_nvidia_open" = "yes" ]; then
        cd "${srcdir}/${_nv_open_pkg}"
        MODULE_FLAGS+=(IGNORE_CC_MISMATCH=yes)
        CFLAGS= CXXFLAGS= LDFLAGS= make "${BUILD_FLAGS[@]}" "${MODULE_FLAGS[@]}" -j"$(nproc)" modules
    fi

    if [ "$_build_zfs" = "yes" ]; then
        cd ${srcdir}/"zfs"

        local CONFIGURE_FLAGS=()
        [ "$_use_llvm_lto" != "none" ] && CONFIGURE_FLAGS+=("KERNEL_LLVM=1")

        ./autogen.sh
        sed -i "s|\$(uname -r)|${_kernuname}|g" configure
        ./configure "${CONFIGURE_FLAGS[@]}" --prefix=/usr --sysconfdir=/etc --sbindir=/usr/bin \
            --libdir=/usr/lib --datadir=/usr/share --includedir=/usr/include \
            --with-udevdir=/lib/udev --libexecdir=/usr/lib/zfs --with-config=kernel \
            --with-linux="${srcdir}/$_srcname"
        make "${BUILD_FLAGS[@]}"
    fi

    if [ "$_build_r8125" = "yes" ]; then
        cd "${srcdir}/r8125"
        make "${BUILD_FLAGS[@]}" KERNELDIR="$srcdir/$_srcname" BASEDIR="$srcdir/$_srcname" modules
    fi

}

_package() {
    pkgdesc="The $pkgdesc kernel and modules"
    depends=('coreutils' 'kmod' 'initramfs')
    optdepends=('wireless-regdb: to set the correct wireless channels of your country'
                'linux-firmware: firmware images needed for some devices'
                'modprobed-db: Keeps track of EVERY kernel module that has ever been probed - useful for those of us who yes "" | make localmodconfig'
                'scx-scheds: to use sched-ext schedulers')
    provides=(VIRTUALBOX-GUEST-MODULES WIREGUARD-MODULE KSMBD-MODULE V4L2LOOPBACK-MODULE NTSYNC-MODULE VHBA-MODULE ADIOS-MODULE)

    cd "$_srcname"

    local modulesdir="$pkgdir/usr/lib/modules/$(<version)"

    echo "Installing boot image..."
    # systemd expects to find the kernel here to allow hibernation
    # https://github.com/systemd/systemd/commit/edda44605f06a41fb86b7ab8128dcf99161d2344
    install -Dm644 "$(make -s image_name)" "$modulesdir/vmlinuz"

    # Used by mkinitcpio to name the kernel
    echo "$pkgbase" | install -Dm644 /dev/stdin "$modulesdir/pkgbase"

    # net-tune: unified CAKE SQM + low-latency ethernet tuning service.
    # (linux-sleepy-next is now the only kernel package; the 7.2 linux-sleepy
    # that previously owned this service was retired 2026-09-02.)
    echo "Installing net-tune service (SQM + latency tuning)..."
    install -Dm755 "$startdir/net-tune/net-tune.sh" -t "$pkgdir/usr/local/bin/"
    install -Dm644 "$startdir/net-tune/net-tune.service" -t "$pkgdir/usr/lib/systemd/system/"
    if [ -f "$startdir/src/net-tune.conf" ]; then
        install -Dm644 "$startdir/src/net-tune.conf" -t "$pkgdir/etc/"
    else
        install -Dm644 "$startdir/net-tune/net-tune.conf" -t "$pkgdir/etc/"
    fi
    install -d "$pkgdir/etc/systemd/system/multi-user.target.wants"
    ln -s /usr/lib/systemd/system/net-tune.service "$pkgdir/etc/systemd/system/multi-user.target.wants/net-tune.service"

    echo "Installing modules..."
    ZSTD_CLEVEL=19 make "${BUILD_FLAGS[@]}" INSTALL_MOD_PATH="$pkgdir/usr" INSTALL_MOD_STRIP=1 \
        DEPMOD=/doesnt/exist  modules_install  # Suppress depmod

    # remove build links
    rm "$modulesdir"/build
}

_package-headers() {
    pkgdesc="Headers and scripts for building modules for the $pkgdesc kernel"
    depends=(binutils
      glibc
      libelf
      libgcc
      openssl
      pahole
      xxhash
      zlib
      zstd
     "${pkgbase}")
    provides=(LINUX-HEADERS)

    if _is_lto_kernel; then
        depends+=(clang llvm lld)
    fi

    cd "${_srcname}"
    local builddir="$pkgdir/usr/lib/modules/$(<version)/build"

    echo "Installing build files..."
    install -Dt "$builddir" -m644 .config Makefile Module.symvers System.map \
        localversion.* version vmlinux

    if ! _is_ci_build; then
        #install -Dt "$builddir" -m644 tools/bpf/bpftool/vmlinux.h
        echo "Skipping bpftool install"
    fi

    install -Dt "$builddir/kernel" -m644 kernel/Makefile
    install -Dt "$builddir/arch/x86" -m644 arch/x86/Makefile
    cp -t "$builddir" -a scripts
    ln -srt "$builddir" "$builddir/scripts/gdb/vmlinux-gdb.py"

    # required when STACK_VALIDATION is enabled
    install -Dt "$builddir/tools/objtool" tools/objtool/objtool

    # required when DEBUG_INFO_BTF_MODULES is enabled
    if [ -f tools/bpf/resolve_btfids/resolve_btfids ]; then
        install -Dt "$builddir/tools/bpf/resolve_btfids" tools/bpf/resolve_btfids/resolve_btfids
    fi

    echo "Installing headers..."
    cp -t "$builddir" -a include
    cp -t "$builddir/arch/x86" -a arch/x86/include
    install -Dt "$builddir/arch/x86/kernel" -m644 arch/x86/kernel/asm-offsets.s

    install -Dt "$builddir/drivers/md" -m644 drivers/md/*.h
    install -Dt "$builddir/net/mac80211" -m644 net/mac80211/*.h

    # https://bugs.archlinux.org/task/13146
    install -Dt "$builddir/drivers/media/i2c" -m644 drivers/media/i2c/msp3400-driver.h

    # https://bugs.archlinux.org/task/20402
    install -Dt "$builddir/drivers/media/usb/dvb-usb" -m644 drivers/media/usb/dvb-usb/*.h
    install -Dt "$builddir/drivers/media/dvb-frontends" -m644 drivers/media/dvb-frontends/*.h
    install -Dt "$builddir/drivers/media/tuners" -m644 drivers/media/tuners/*.h

    # https://bugs.archlinux.org/task/71392
    install -Dt "$builddir/drivers/iio/common/hid-sensors" -m644 drivers/iio/common/hid-sensors/*.h

    echo "Installing KConfig files..."
    find . -name 'Kconfig*' -exec install -Dm644 {} "$builddir/{}" \;

    # Install .rmeta files if they exist
    if compgen -G "rust/*.rmeta" 1>/dev/null; then
        install -Dt "$builddir/rust" -m644 rust/*.rmeta
    fi

    # Install .so files if they exist
    if compgen -G "rust/*.so" 1>/dev/null; then
        install -Dt "$builddir/rust" rust/*.so
    fi

    echo "Installing unstripped VDSO..."
    make INSTALL_MOD_PATH="$pkgdir/usr" vdso_install \
      link=  # Suppress build-id symlinks

    echo "Removing unneeded architectures..."
    local arch
    for arch in "$builddir"/arch/*/; do
        [[ $arch = */x86/ ]] && continue
        echo "Removing $(basename "$arch")"
        rm -r "$arch"
    done

    echo "Removing documentation..."
    rm -r "$builddir/Documentation"

    echo "Removing broken symlinks..."
    find -L "$builddir" -type l -printf 'Removing %P\n' -delete

    echo "Removing loose objects..."
    find "$builddir" -type f -name '*.o' -printf 'Removing %P\n' -delete

    echo "Stripping build tools..."
    local file
    while read -rd '' file; do
        case "$(file -Sib "$file")" in
            application/x-sharedlib\;*)      # Libraries (.so)
                strip -v $STRIP_SHARED "$file" ;;
            application/x-archive\;*)        # Libraries (.a)
                strip -v $STRIP_STATIC "$file" ;;
            application/x-executable\;*)     # Binaries
                strip -v $STRIP_BINARIES "$file" ;;
            application/x-pie-executable\;*) # Relocatable binaries
                strip -v $STRIP_SHARED "$file" ;;
        esac
    done < <(find "$builddir" -type f -perm -u+x ! -name vmlinux -print0)

    echo "Stripping vmlinux..."
    strip -v $STRIP_STATIC "$builddir/vmlinux"

    echo "Adding symlink..."
    mkdir -p "$pkgdir/usr/src"
    ln -sr "$builddir" "$pkgdir/usr/src/$pkgbase"
}

_package-dbg(){
    pkgdesc="Non-stripped vmlinux file for the $pkgdesc kernel"
    depends=("${pkgbase}-headers")

    cd "${_srcname}"
    mkdir -p "$pkgdir/usr/src/debug/${pkgbase}"
    install -Dt "$pkgdir/usr/src/debug/${pkgbase}" -m644 vmlinux
}

_package-zfs(){
    pkgdesc="zfs module for the $pkgdesc kernel"
    depends=('pahole' "${pkgbase}=${_kernver}")
    provides=('ZFS-MODULE')
    license=('CDDL')

    cd "$_srcname"
    local modulesdir="$pkgdir/usr/lib/modules/$(<version)/extramodules"

    cd "${srcdir}/zfs"
    install -dm755 "${modulesdir}"
    install -m644 module/*.ko "${modulesdir}"

    _sign_modules "${modulesdir}"
    find "$pkgdir" -name '*.ko' -exec zstd --rm -19 -T0 {} +
    #  sed -i -e "s/EXTRAMODULES='.*'/EXTRAMODULES='${pkgver}-${pkgbase}'/" "$startdir/zfs.install"
}

_package-nvidia-open(){
    pkgdesc="nvidia open modules of ${_nv_ver} driver for the ${pkgbase} kernel"
    depends=("$pkgbase=$_kernver" "nvidia-utils=${_nv_ver}" "libglvnd")
    provides=('NVIDIA-MODULE')
    conflicts=("$pkgbase-nvidia")
    license=('MIT AND GPL-2.0-only')

    cd "$_srcname"
    local modulesdir="$pkgdir/usr/lib/modules/$(<version)/extramodules"

    cd "${srcdir}/${_nv_open_pkg}"
    install -dm755 "${modulesdir}"
    install -m644 kernel-open/*.ko "${modulesdir}"
    install -Dt "$pkgdir/usr/share/licenses/${pkgname}" -m644 COPYING

    _sign_modules "${modulesdir}"
    find "$pkgdir" -name '*.ko' -exec zstd --rm -19 -T0 {} +
}

_package-r8125() {
    pkgdesc="r8125 modules for the $pkgbase kernel"
    depends=("$pkgbase=$_kernver")
    license=('GPL-2.0-only')

    cd "$_srcname"
    local modulesdir="$pkgdir/usr/lib/modules/$(<version)/extramodules"

    cd "${srcdir}/r8125"
    install -dm755 "${modulesdir}"
    install -m644 src/*.ko "${modulesdir}"

    _sign_modules "${modulesdir}"
    find "$pkgdir" -name '*.ko' -exec zstd --rm -19 -T0 {} +

    # Blacklist r8169 so that r8125 is used instead
    install -dm755 "${pkgdir}/usr/lib/modprobe.d"
    echo "install r8169 /usr/bin/modprobe r8125 || /usr/bin/modprobe --ignore-install r8169" > "${pkgdir}/usr/lib/modprobe.d/${pkgname}.conf"
}

pkgname=("$pkgbase")
[ "$_build_debug" = "yes" ] && pkgname+=("$pkgbase-dbg")
pkgname+=("$pkgbase-headers")
[ "$_build_zfs" = "yes" ] && pkgname+=("$pkgbase-zfs")
[ "$_build_nvidia_open" = "yes" ] && pkgname+=("$pkgbase-nvidia-open")
[ "$_build_r8125" = "yes" ] && pkgname+=("$pkgbase-r8125")
for _p in "${pkgname[@]}"; do
    eval "package_$_p() {
    $(declare -f "_package${_p#$pkgbase}")
    _package${_p#$pkgbase}
    }"
done

b2sums=('aa2a7acfdb5564d40b24f5ab4fadd5890aa6ce212ddcb7c20807f7a0b516f2180c658cddb504fa3e2b09bf93bc9e9213cab1eb7dc77d7b44f4231a74958d5f9f'
        '23f570909d870d709e9b9f414d8a9f543da492085c0ed457e6896d995e5cd608f7e45f3bdc96a5f09b595fb04e24babd6b9811ed03ea8d9598996aea0e890a9b'
        'a7cefe36f18ea4390b41849e604ad6257cccdbf25c2af380d2353397858cba21f6eb02b0774ebc24ec26639539a8858a29262b02edb60eba5736cd172993480f'
        '458b2cb2413befbbd76c22bd541da17694965d535b486df65fc6b5c470a8b06ddbb0224f25dd966d53210de2d9559da04b7822f688e5f0034ec0094d2f276be8'
        'a6704c51338fc584baa37ccf604ffa6ac5399e73b696404c8d45f521506ccec417207aa6a1665c28efb8b2b2b12e6c436ddb5bb8bd4a36c6e5020541ecef6494'
        '00a418320c6cbcf9c40c88434eb14723b6c97c2a8906586157f993e73aca27000ffa88adbd9dab708405b4c38737c8f72d295a59e4e2cc9da1cf91ef2ba3b751'
        '3e1ebc3b867d8b3a0d25f83987ae83ce20949513fe8fdd923faa0bfc92b607b894cf64e8e1e70fd0b9617477fac3f014e733259519c41a963367ad92e59146d6'
        'ec5bf6d8b50fb282141b72f8446e312170cf2243c1e0a0289a378393ccc014d55c1a0eb39756f955b109ad80344be59b2c148c3e3ebba13227e4a0af467ca26b'
        'f77a07fc6c53ce2862753a110810a7e817b6fec2923132c1fb608e707d769b7719ff912c73c9e72c045155dfc704f02b78e03526ace115c4220b66419764799b'
        '4c0ccf168d8c1818bfd5310416b47b7ba6c38bde9aa00a9f577fc043300729fa5949830ed045642472407b0358e4553864fba7629554e26c5e273491bdb1ced8'
        '9d2e7cfd2a8cb089fd3da7be483c293544c5c3bbd40c097c152321f75131057d20616abd712d1a193292ea9977400c1af32d8318c9b0e71de4b838be7176e2e8'
        '12358025d6531fceb1df3dc4a32368be1bd1b528e3685b9b2505027fef898bfab26fe18306bebaab2a8163cd6697e40db487f96766f9631ad8f4be825bb0e1bc'
        '2b7e1ea1ff4592bc8484e97a274c2aac959ccca317cec9523deaf4472be8c91d472567ae4a7029e4afb2dece0b9a934ce94a35ff9da938e26ef0e1d5a1612079'
        '48064b932392d2d8b7c33903a88ec99a5c7d0baf723b58331eeb6bba2e632ec7a38ff1efe8cb022fc95fb50a270f5d57bc075bed0215fe65847c555a7949f706'
        '92148f845b35b0ad77fad1b004fa8625385bfbabd1b83b4a4ba262bb44a51e611473bfc05524cf72db85e3c53838d99175149d035b3ddeea24c3435e1d145e93'
        'b866c2e213614bff04f852e67c2762e6ca28b402dd43142df61192d516bedb7b6d8a7a647870e1121461375735a5e84acae96dc03059347fbf405dddbefd1212'
        'f61685cae107b07fd76a108f80cb0452378c672180a98dd49cf0707a7a6013162f20c1f893f080add632d8ad3fe1e0667db1a4d494f16bd2bd980eee506bbf91'
        'dbae23fc923db3fa3bd04e2d4dcba2774919d2133c031ce728f71f152cd3f4e0b0415054eb98a8768d56f49ac39aef7be13ce62af37785fdea1173d7c8477662'
        'a973cf2388f1a229626656883e741f7a35be2a5d33385e7e694e4c66d9dfa96974f26dca5d74fe6ae1ec093bc0421ca779a1ba68cb920e5d18bed8c37cfc5692'
        '212368b3fce77d1a0704a7a477ca71cee62c5cadd0ed85edfa29fadb8d012f7ea045f1f5be3b985cf559b7451eb54d94f3c872756494871a3527d767aa9b2094'
        '1cb6e0ae6f57e9eca2067594ce83c005c6bc49e6a3d7fb11aa1aeee12204691304da0483e5be3c20b233c132a54831ffa587765599634a5ad123489e99982a58'
        'ee5f2c4aead1f2fc8d8096ae2a953d4c45d4c79de29e0578da543767a2d96664f903f043af36cf481adc13f203e2eca8fb616c26257e6cce5b3cae26b1d46ddf'
        'fdc7fc1d942be4fe8dadcb228b7f9c02273eaec91631ff609a07722b74b1db64828e144856e01a8ffd039762d1970a7ec511a3d240481544c570592914573b69'
        '9e09ebb057ad702b03c3caaaa30660d6f4b1b475002e95f7c1f3fe757980ac3e75a2cead66b01f5ba85bfa2c42bb18b672c316edc3fa645801efee0dfc894e8b'
        '0070a22fe00e90fb691ba892496d9239c81a0bd1242dba1a843a001ae5ee11c81ce3848b763db0d868dba7d366b333cc9ee99f1e29e1963123cb9e49751784e0'
        '2782b795c66d9dd50e04f89f87feb313c0f42f4e64eb4286edcf8a8820eb6157cf88687b64d115a684b38de20b5358ef9a831b645323c1f635357929ec6ca4da'
        '17c7eefbe32074fc2aca66f27513684d35cc2822c0f855d385f7313a099e1b08907fed86fae60ad479cc01679f4f27c24985586c77882193f4ac8e544e57b877'
        'fc807006b62fecaf65da70e5e69d4b49a4d99ff40eec4b841d9701f3ed4e6e1e2470a838cce3fab382f7f79825e8c1aa75b4bed0aa82d12b7d8a495ac1171e3c'
        '7e0b43bb417f1de1308691800cdd5c803bced08d8b30e489646e537103a704354f29370c8b1ac906c7b3132236fa8979675e8e5543e32f8bba33d81a7a984bee'
        '2562671a4574c2bd95b783506fda4045db4f54b14dd8b2f35060979eb1ca930064bd785d16ed797afd06b5c2dbaa9e343da7464a8cffc58162520a1729f7d3b2'
        '1214d2d159179d88f65876092f95d0498cdbaf1bc9bb8e168fb0ea635d8727aa1d60a2c9f72c1a7ede008036616ac0cfe5b81347bb44487900124ca32994bf0d'
        'd3f04c6f6c2ea65f04dffda24fd4993098403ba7201f15824bb16578eb708fe3eb0e0df3ae710f4b7d6db393972f9276ea318ccf7588952a06bb3a880b8e47f5'
        'f9a80bd6c375b7e4116d0c6324fabe0e7e183fde465bed459535d7e618e452e48cdb832d023aaeeea5615fe19cdb091a2c4d8659d1f934aa38a1eeca026f550f'
        '75e19525778f4aa63bcb893b25d83df7889a54e88675d90ae4f1f123fc5ce811bf8c69b454b67f66b7f696b09ebd65650020da348935bdd56f8cb479c13f9e48'
        '6ac08e930e43e78a9aaaa49ddef29164d3d0f1c9bc6e2f75bd04909ba0df3baa1441c9ca245c122915b0675fe8be63ffe1f706376fcc9a2d8940bed846647f4c'
        '80389db520340e3d7463fab193b9c45e959ed3b089843e22c71248bef1d12fa5b2a5269d1a2243171000fd6eae1883ce929ab3a0e474869fd7c52df8d693dab8'
        '403102d5d8ac54bb1bf68db2741950893ca97d6f3311458e58c0ddaa2d37f614a140e0d0f5d3f27db6d289be1079cea774a62cc28d1e8828fadf22f2cb424b75'
        '081c9e49d1f84785569a65a061fd89fe77e5195e6fc0ed52f4571df4c4943609366e9c2219697661070291c40fce441ca4ff082fca2541deae04f65eddba0f6c'
        'dc8f77cc001b2b78696ebd967f14ef2117a10067b30ca4d199809f8057616669aa9ca12a1b14e35ebfe7c33b27152a5c22ef2fc6e7a853e174def0d9a4fbac91'
        '7d10158ac24ec34febf7153b9880592ad46e035c702c91cda424e11722074a5c7590172400d321f1b69f74494591a2fada799a486d5d159e6e8ae57869925379'
        'a47c00f575dc689566a58d4e511f29cc40d642a11aa66b806ffbc5de4659c09ee6a486fdca237c3322336d716d15eb78f794bde7148885b51dfee24a0ad65edd'
        '85028ee0b1271d0bb1f1618a46c28984ef605c9b4f05f3b686f0362ecb10f391712ebec321c47a2220761e1497077869d694c47fce7a74074e5d5270693744b7'
        '9c6b0d66c4d9d73cfb1b8d6902ce2477a8ff59a2ca59eb277489dc28157c1bc8d8b709ad4a0c19abd04ad3dc6171c6ce8644717fe03dbb921769f3aba693a178'
        'eae2d25e806290eb9d55096bc7b9e08077a1d8f1b32da50d3075b1663357995d49796cb45a55175ed2fb2be8809d10d44ecf03a55716c79d045810b51c675790'
        'c2f5bb96636f1a471ec1899249b198335fdd7f19cfb53ec95f4f743e758cfd8f558e83a36536aad6e3f0a3a641a5ac5053998587c898ae26cbde3ce819d5b75f'
        '498ac5d39faa626f9e55902e7b2eb7993937893c2d1a20c9532001983a296cee648460a547c7b57142c9010995b34bfc49d3050e6eac69a6c55a137ce6424fff'
        '6ee4697db2969152e02aefad72a03fdf1bef5e397ae6a64a517554c3712ac7e0e2bc855e2b591eeddbfe03204d62e16c910c402ed4c71f868210509038e6b56f'
        '06727a998555a2c0391a46ff7d6bfca02e43542ce39696881dc1887365df4ed68f633286f07e4e32f08a1931aa9ad911e90e797f207bb3390d5bd2c2d72516f8'
        'abe62b4dadc481d6b1144a579d95c035d8b3d18f0ff5ffaf966c7cd8652242136183c0809210f122220905eda927e6adba524b17138a6e1e3ed785b0d43d62e5'
        'a1442892cc6ed1f8334beeabc418a5532cf1e9a8626f3e0ecbb35792808302b06e4266291849351a6a95b06a5c10aa7ec8787fe096d89688cc9bae30c7498240'
        'eb0169140aa96b826a21b92fc57e2ff222b9f6bd5f33619257ab6e07e48597c54cc01fc5af995b31b2fd5d2698c36ce73b5a4c30ba9a8432a8340c8bbaf046df'
        '0fb08f727791630b6101b8263b23ce433a8b65f895ff757a4d79b282815be449e7b1932a752635e848b3b3ba8235a775a3bf618cfb933bb80d69f3a38f5e5ead'
        'cc08d619b72c0baf6ce3ec997a5a2e381bd6a4c87c395e4d89ba91523369da7a4562a65e837355fa31bce81726abdff717c7b4d70c2f0c02b563ab72b56f2027'
        '05f7335d35933033edcdbdd436dcf8c9fb1f6326cf4cefc34bbc48a1a91d7030536b0e69e48d8ffd4b0a20592f22b5a96895fbd277b776ad860bb2853025d532'
        'fe7fbf83a8f834b103dbfa6f8209d32b62ad4df23683017e0347c03f23372180b331c226baa0ef563dcdc5ad7125f10ef69a072204eb6bf6cdd69f31ffc156b8'
        'e9d464ebf525cd8d93d48f1cbedea0197bd9d0142085da7d83ec3dfda0174483a0fea4077055fd7d1ad9180563dc6dfb77e4f52f9bcb023b7c7d7c9fb5c39ece'
        '9d3e36dbc5c9c5342d2991c4665278ed075073196251e59280bd12f1d6812a37d31db58f5cb978b926e2dcd0a32365960a414b69d10f463bd8f68cedbb4bb6ae'
        '52fe01328f544e023666eab1fd378ae0a0eb47385d495403a55a933f71beedcf295300767c1e43feb46366915fae8bea3b9137f11d16ed194a1fcf71d95aec0d'
        '40ab020af700040e775f56afd544ac121f5391373ddedfcc2e6a6435ac8ee63f2c43b6fea66a78fcb8c3c0803e42fbd0f71d2205505a228a1a6379e0423bcef0'
        'a72a65feedee71dfd2edecdc269aadcd78ccc5622cbb21a879cadb7be2f8f3b3203b2c67423cb6f4f7073e9890a7244f620a547b7f6494befc9599eaf8883c18'
        '39d24bbf092bd519e43371f791b8ea97c6857745c0abe2e3b80ecb6d2d3e26cc11e5fba1741ac4a8f33981cc5168bb0f00d8650f06fb5a666edf6a05c3f8a63c'
        'a1d625c5c923cf3ad4533cc9c007cf91ae44e7d07435457b8f75c4d5dd32aa33424bf1b6cc59cdf076797b09987898f4444e2151452532ba158b504ec27672b7'
        '1ff31d92d71dde6c2c8e32565a3bffe8b8562b6b0af9c5c8ba76648b50fb326af6d07a8f441b72f381660395736bf607a438b96b8eb98b477b71440f420c116b'
        'c03ec8acc871d27f6d827eeed3d6bcdedadb7c662c22b689e84110fc8085849a91c52ca24290ca3b2bfcc73ce4e0b0e15fdd9b97582943f7f018d893f2cea866'
        '78fd1dc2790c18a447fe6fb4d6de2ec835e36085b82d5dacc686b7bca5f0bf28b27fccf75f060b1d352caed53eafcad1e26f2a50d43f737ecce0e377f6ace8d4'
        'b02b85ed477bf89be49272480e49b6a055e5ab8ad11884be158e49ea01bc8f2676bd3019ce4fe03c40cf83f1975f875e4a999b4b690f5d576d8eedccaed5472e'
        '172c070d9f4b1168acf17fd0c5e145fea964dba5175f7ef5e22160b9ff7d7e0c045db0a1ec4ed4536704aa0a5cd6ae19e46753b96982f0f3b934af6fad1b59ec'
        'b3eefbc395d841ba324a13f7f0a647225b8d12012b31f2fe78d1aff220cb9dfbdd449959153f7d66a3a30f6cfb481b82addf0b23cb01b7f0140f8de5312d9929'
        'd3bd197dbceae9b72013acdef50ed7b304dfdcd15a0ee7879b0d506818098a6a625932d5b58455324e22b1b91d87fab8a015455f18db415cc31d80e0edda5afd'
        '1c25bc9976ec6f799bb921eba0b08111e9120eb13486f83f360019c64068c015c4ff7ca58687d969967ec1cae4217125eeaaa02577380eddb24979ce0b12d89b'
        'c45880fc710150cd86b2e0cc1662ecd72d2b9da18700e4808a08dba2d535949d5b0bef9e40175038ff74090fd5728d7370e427b2ea91211be495e391acb92356'
        '6ac07952128eb4edc0120c33ca327f8369820f1ce2ae550955edd01ca982841a1b023c9725cf67c49dcb6aa1fbb2ffe9413aeb755b6a0726ad5c3a8b434ed3f3'
        '8dd8d6ee80d3f7d548c2a08542153bc3ee915403ea3819d0ae30ea2ee6ef80c5c8c4d2a79044111d784bbca8857934deb87447f30561ab3045e06ae4742e0257'
        'c20b3b791715d02756742bfa34f4921bcaebeee62edf079fe15c89afdc11451a2656122f4f21335cd116676ff69c3b7eee80c6adfdcbfe838c0f1e9012ce0428'
        'df68cfd344b37cae25fa446c82c5897510de23c55761570969dc5a6f2a5bf4c11b31e50c1670a18bef1065af6597e72e0ed839e8fdbc0328cf2dcf34484e5758'
        '8bff27696075ec53ca042b0c9e0deae345712e652b3b66bab1da82c4deefdf35533d04c00d59de70cbf968380236131bc819e0eeaa8aa40edfd84df3bd0972ef'
        '48c6c8a299d0d5341475936ea8e1974fc933de81fa710c483c0fa54d7d7a70ccb15c56da1b4cf66bc0c4fe486f78f6b74816b38f602ed219e5dd7f679fba2662'
        '2b9bad240296578ddb6a81629263d046b7e2d9ba063faaae38279c98556749b1b1ae6ccc3036a551fabea3d01ce916cffad1f1e56a65b3eab31faaa37de96211'
        '1d8d63086f1d7ee562047c5e126276b98452daf4cf5146d9a80030abd4832d6fab97c91c01678c301ec9d830a210952715b852c1c9a6783001633ca2f313fa1d'
        '6df3b8a9bc66ea9080f81fd78f346aa773137943db7dd2a7da93d2587073a1321cc753fec5d4d6a4fbdd607c8176790f116c4a958f4768018b5ee145ff2d8c13'
        'a745db752d2586475d373cb29e64b4f42f6e305b4b3e588efbce955491429c73b3d16c426e76118b1499bbfb4a2159192f3950ed06d309064eb28750a1d6e6aa'
        '8820c684d4f21c9c74729a518f187334b817b8059436aa808e423533a67a6b752a93df4e79c200307b29635f0de393f6749aaa52cfc20e28957f759b4adb6ce0'
        '877dc1eebcaec113969ea45471b63e0339066a270da667b5c1aa1578e26aa01c7ec34e1cb4c436565553388e0ba04add10bf3540fe4ba7e11b24aa8a8d8ccc4f'
        '462ac8db18e5755331a47e2c4d8ae24bb2b4042b098bad70f2814ebb97ca10d6c888bc0c75741000a36772c1247b22d5af569b9e756ef7a5558df8c163d5e769'
        '98b30de1e48e6baca5f29d293f2f89e3eedd4882e8091ace78f7b2a1ae9cb2cc2e3189b0e37c5e212e7df4bf97d840130bb1bed812bfb6e978ac48d0bb8019eb'
        'e5330139599a17003bdc3508190e71b3875e354ea6f345d24104ff3449724fab9638f2e431ed0e86c0d987733431da0594bec323271c135e8c6daacf5c7eeb69'
        'a590f6140a02f5cbee18f8ea91ec079e965b5d06a9bdf09c85940f6380fbd6d8a29cb87f846fe05985bb8a256177dd27d3d2a6a1cca9c296cd1c0b3e7ce01985'
        'c91351632390e03d5b874ce5180e07c54c892592180c7d9bf14175e3874762cad385e60f5f77aae24a58bcd1c1a380e40598a52d0dc085fe04f5c63805c68048'
        'c096823c41fb07bd9974ae2189ffeb1f98c31730eb9f8e3ccafe4e3d30b9b9c207b592672698e3f7b5369cdc3baf5375c15f15fc87551fdb27dfbe97e318a66e'
        'eb5b6994b1341e7c05c49ba79336febc87dffe40e5008a81a9afdf931c8d2c00fb69fcf4d70923ba999993dd2e8e9ebf768d5809ee219a22e94f632944553539'
        '5626968774bad1795494928621f43e19945a1ecbd26c4dccd432a329277c26f04fc4ae02fde5560c503aed0fcd9bfda219de5c47e29a226149723fa5a7dbb721'
        'dc4e862e8f9fa7e8ead895908459757afd1027c24b960ae3d289a7212e29575bce3ce4627d5fd73edf211ee162dfa545e1642c5b16e8156f3dce50af8ef3c256'
        'bdc839d1629f22095c5907e62b7a1a4edfcedebe0cf7e430897ae87aa331cbad28e28cef106ae38c05cafa585fa19ddc019579f1b73fcfaa69d8a8bd40ba8111'
        '6eda51715651cc0aa69f046f347171dfcad4606f74b5fdc6e4737a66e86f5e565e8e29c0c67edf1e7bd4f7b3b0312af66369bece36447e78193aafc99107fdb7'
        'fbd6f7b4c4f3a371c17fe6859528aa2ab79e37c04e9191d91eebc4afc15f3145b25148a9c6248d1983ee93360e776ab71dc36896e43260978efd19849c0025e7'
        '7de1cffa679f349533394fdf3f8e36f9037dbb60c91fd31ad586c631c3c033cbba5c90671e5abab36e8129e06cc88f64ea7a785dd80d96d4afa1bf6675dc5f24'
        'e3060e447b03702cd7b2f35129a75c6dd6ec8a85a34bc60639ac93d225dc44c871ec604565231383e9e2a88a1803325355dbb0beaa5dd8287d551d3f85e11799'
        '3e91566e3cd023c22d3b2234f49e31a2906a8d3264c79c16955d1d001a98bb0e064548500a0358d7a05847a3334c56fa37cb5d3d79a123a923cf64398e292703'
        '23459d8b2f37920d2756717d0d6cd5fce78e0ed879ff1ea056ba1bb13a650d7ca5c9a3a65f3323ef7529ab8b14cdccb253fd64c0fcb0e35e67afac3b8ec4ce0a'
        '487e1d98ab4dc7f1fec3ed4bb4de6ab40fc8b96fc99f270f1d99ac2d060a9a33acc4ef6d5dbd429a2b24921e2c91e85982c65fd7f3c663e153753685fcbb7ede'
        '733d5f6843b1a6851c010bdf047f8e72a62185b7c12badcb4fecd125e2607ab85beb9827f1705b0738c1c2e6cc4f4ceb715cb4f63beec50c703e950e78657b7d'
        'e07e591f8add661344ba706231c7c62e863cd966e0a54ceed1a9ad0ce09226159185df26a7833dff30ec8b70a4d7d576db5eea6843bb8a0c1c0d515befac02a9'
        '8ce520754ab5ca577874d6336ec9a8669ec8086c48bae6bb89399ece42c7d3204f59385a191a988c1bc5fdb94544bd420a366946e26c9ce750be83638e09d53a'
        '156a45385d78839a67455a4776edceda28bbc5bea4c5530917c22b48d831917b75d9ee11a54d5b7dff3f8e152df0c68c0327fc995b5e18c7ca3633d2ad51707e'
        '6c0c2e11448f49aa31d9178ab124dd3771b8a625c96511679aaeeec0cf9e61eac8c95f44c93766322db2688d2a41a11a40b254fe45f59fed52817abd833aa54a'
        'e322c8e1dab6618e55e2305005a3bf59080e81bdfd44c446809be59aebe6289027523a246807edf6e21294377b8a8782b547e0a29f0e35d839ebdbc1ed959353'
        'ad3cce7913eb24cb95270e4df78f74c901c268e4d530453744145baa8c4038beaf961bed036dc57d119674fc07e8a059669db1375c6a32d6e208b98d341124ff'
        '0c25491212274500756b31955cafa5f757480985f21d616ab179df8773f1d8a869ab5eb319add233c5f998ec286e12e0fbaf40c1f01cc4f6d577c799cd0a40a7'
        '2f6ecc84e0141cbee5ce379a2959550cb4830e923afa3d5275283d74d69b8e3bba51f84af96df329d1ea30af0a26f320678907833b40172cbff4a751de3682a7'
        '203bd93e310b0795acf2d04a03de10bcfa4ee653b490c5cc3fb2f377119ce373dbf32c4ab4c8674d246ea8d8518d1a26ddd46f8c3dff085aa08022fa28d5144c'
        '21ca802919183021abd12cfc782de48a895daddfa9b401700e4bef50e750537183bc3c7157e723bcae769d2bd72f9efd34e677d80d63d74eaa7344b8205eb1fe'
        'f409b3525bfd04fa1b77adfcafb5d701e28c707619b6d71472d521b34926c40496b47a49b1c2c2404e83333a58a369d1be47517e99df1b1631d5a84a05e102b6'
        '69307106355483e423245a7e6f89c187254c8fd5a2ac8b503fa4fedaafdb8b0795b9ad3a04ff9226e70be267cb662fa8b492357e84b38379b208feabe567a249'
        '4b709d02832578271be2d4a180ba1002eb0dc120a4d4df2a149c2a320224791aea3dc64da520c3af53c4e7ca5ac2b906adae5e5f9ff003b7df3324b95d36b535'
        '2cdec9daf2eb9d4a8e95f33bcc81e603899db1f2e4f55cde68fa29727972238b5bd544e055a06bd0c94569e222666f6d8bf231db9fa8593b6d5f4fe52b26022a'
        'fd97b3f9883167948e21e047733b87535676c305661c12f4a980ba123d08a00c4588a1e2ca8233621b530a743383c1f7cedac01bc142f72bf1c2d3d5b0c05a00')

if [ "$_use_kernel_org_llvm" = "yes" ]; then
    source+=("https://github.com/llvm/llvm-project/releases/download/llvmorg-23.1.0/LLVM-23.1.0-Linux-X64.tar.xz")
# The official GitHub LLVM release links against ICU 70 (Arch has ICU 78). Bundle the libs.
source+=("llvm-icu70-libs.tar.gz")
fi
