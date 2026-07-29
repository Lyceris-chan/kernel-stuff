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
: "${_build_r8125:=yes}"

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
    _pkgsuffix="sleepy-lto"
elif ! _is_lto_kernel && [ "$_use_gcc_suffix" = "yes" ]; then
    _pkgsuffix="sleepy-gcc"
else
    _pkgsuffix="sleepy"
fi

pkgbase="linux-$_pkgsuffix"
_major=7.2
_minor=
_rcver=rc5
pkgver=${_major}.${_rcver}
_tagrel=1
pkgrel=1
#_stable=${_major}.${_minor}
#_stable=${_major}
_stable=${_major}-${_rcver}
_srctag=linux-${_major}-${_rcver}
_srcname=${_srctag}
pkgdesc='Linux Clang ThinLTO + AutoFDO  + Cachy Sauce Kernel by CachyOS with other patches and improvements - Release Candidate'
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
  "https://git.kernel.org/torvalds/t/${_srctag}.tar.gz"
  "config"
  "0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch"
  "0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch"
  "0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch"
  "0004-drm-amd-pm-Disable-SMU14-mode1-reset-for-SR-IOV.patch"
  "0005-drm-amd-pm-Add-bounds-checking-for-SMU14-I2C-command.patch"
  "0006-drm-amd-pm-Remove-redundant-mutex-lock-in-SMU14-I2C-.patch"
  "0007-drm-amd-display-Proactively-shrink-DET-for-pipes-los.patch"
  "0008-drm-amd-display-Fix-memory-leak-in-DCN20-link-encode.patch"
  "0009-drm-amd-display-Fix-OOB-array-access-for-HPO-FRL-lin.patch"
  "0010-drm-amd-display-Fix-missing-HPO-FRL-link-encoder-reg.patch"
  "0011-drm-amd-display-Prevent-memory-leak-during-IRQ-servi.patch"
  "0012-drm-amd-pm-Fix-SMU14-power-limit-reporting-logic.patch"
  "0016-cpufreq-amd-pstate-Document-missing-kernel-doc-mem.patch"
  "0017-cpufreq-amd-pstate-Update-cppc_req_cached-before-w.patch"
  "0018-cpufreq-amd-pstate-Add-per-core-EPP-boost-for-rec.patch"
  "0019-Documentation-amd-pstate-Document-the-epp_boost-pa.patch"
  "0020-drm-amd-display-Fix-DCN401-MPCC-OPTC-and-DMCUB-issues.patch"
  "0101-cachyos-mega-patch.patch"
  "1002-drm-amdgpu-gfx12-1-warn-rather-than-bug-for-invalid-sdma-eng.patch"
  "1003-drm-amdgpu-gfx12-warn-rather-than-bug-for-invalid-sdma-engin.patch"
  "1025-drm-amd-display-enable-psr-and-replay-on-dcn4-variant-and-fi.patch"
  "1031-drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch"
  "1033-drm-amd-display-increase-dcn42b-uclk-value.patch"
  "1039-drm-amdgpu-allocate-enough-space-for-hpd-info-on-gfx11.patch"
  "1041-drm-amdgpu-gfx12-only-need-to-remap-kcqs-when-reset-via-mmio.patch"
  "1050-drm-amdgpu-gmc9-disallow-gfxoff-around-TLB-flushes.patch"
  "1051-drm-amdgpu-gmc10-disallow-gfxoff-around-TLB-flushes.patch"
  "1052-drm-amdgpu-gmc11-disallow-gfxoff-around-TLB-flushes.patch"
  "1053-drm-amdgpu-gmc12-disallow-gfxoff-around-TLB-flushes.patch"
  "1054-drm-amdgpu-add-an-buffer-funcs-callback-for-TLB-inva.patch"
  "1055-drm-amdgpu-sdma5.0-add-tlb-invalidation-buffer-func-.patch"
  "1056-drm-amdgpu-sdma5.2-add-tlb-invalidation-buffer-func-.patch"
  "1057-drm-amdgpu-sdma6-add-tlb-invalidation-buffer-func-ca.patch"
  "1058-drm-amdgpu-sdma7-add-tlb-invalidation-buffer-func-ca.patch"
  "1059-drm-amdgpu-add-core-helper-to-do-TLB-invalidation-vi.patch"
  "1060-drm-amdgpu-gmc-add-more-gmc-tlb-inv-helpers.patch"
  "1061-drm-amdgpu-gmc10-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1062-drm-amdgpu-gmc11-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1063-drm-amdgpu-gmc12-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1064-drm-amdgpu-Switch-order-of-GC-and-Display-IP-blocks.patch"
  "1065-drm-amd-display-add-dcn42b-specific-SMU-clock-table-.patch"
  "1070-cpufreq-amd-pstate-Bail-out-early-if-X86_FEATURE_HW_.patch"
  "1071-cpufreq-amd-pstate-ut-Skip-tests-when-amd-pstate-dri.patch"
  "1072-cpufreq-amd-pstate-Fix-EPP-return-type-and-handle-er.patch"
  "1073-cpufreq-amd-pstate-Toggle-auto_sel-in-active-mode-on.patch"
  "1074-cpufreq-amd-pstate-Cache-the-firmware-programmed-EPP.patch"
  "1075-cpufreq-amd-pstate-handle-missing-policy-in-dynamic-.patch"
  "1076-cpufreq-amd-pstate-Loosen-requirement-on-lowest-nonl.patch"
  "1077-block-mq-deadline-pass-in-queue-directly-to-dd_inser.patch"
  "1078-block-mq-deadline-skip-expensive-merge-lookups-if-co.patch"
  "1079-block-bfq-pass-in-queue-directly-to-bfq_insert_reque.patch"
  "1080-block-bfq-serialize-request-dispatching.patch"
  "1081-block-bfq-skip-expensive-merge-lookups-if-contended.patch"
  "1082-zstd-7.2-merge-changes-from-dev-tree.patch"
  "1083-mm-7.2-introduce-LRU-MARIE.patch"
  "1084-7.2-nap-v0.5.0.patch"
  "2000-drm-amd-display-Exit-idle-optimizations-before-programming.patch"
)

validpgpkeys=(
  E18447AC260021D31F3FF6C4C8A2A4774B8B63C4  # Eric Naim <dnaim@cachyos.org>
  E8B9AA39F054E30E8290D492C3C4820857F654FE  # Peter Jung <admin@ptr1337.dev>
)
# Use official Kernel.org pre-built LLVM toolchain (https://mirrors.edge.kernel.org/pub/tools/llvm/)
# Automatically checks for Nathan Chancellor's latest weekly LLVM builds on Wednesday/Thursday
: "${_use_kernel_org_llvm:=yes}"
: "${_auto_fetch_latest_llvm:=yes}"

if [ "$_use_kernel_org_llvm" = "yes" ]; then
    if [ "$_auto_fetch_latest_llvm" = "yes" ]; then
        _latest_tarball=$(curl -s https://mirrors.edge.kernel.org/pub/tools/llvm/files/ | grep -o 'llvm-[^"]*-x86_64\.tar\.\(gz\|xz\)' | sort -u -V | tail -n 1)
        if [ -n "$_latest_tarball" ]; then
            _kernel_org_llvm_tarball="$_latest_tarball"
            _llvm_dir_name="${_latest_tarball%.tar.*}"
        fi
    fi
    : "${_kernel_org_llvm_tarball:=llvm-23.1.0-rc2-x86_64.tar.xz}"
    : "${_llvm_dir_name:=llvm-23.1.0-rc2-x86_64}"
fi

_set_build_flags() {
    if _is_lto_kernel; then
        if [ "$_use_kernel_org_llvm" = "yes" ]; then
            export PATH="${srcdir}/${_llvm_dir_name}/bin:${PATH}"
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
    
    # Interactive SQM QoS Prompt
    if [ -t 0 ]; then
        echo -e "\nWould you like to enable the CAKE SQM network shaping service to eliminate bufferbloat? (y/N)"
        read -r enable_sqm || enable_sqm="n"
        if [[ "$enable_sqm" =~ ^[Yy]$ ]]; then
            touch "$startdir/src/.enable_sqm"
            echo "Enter your true DOWNLOAD speed in Mbit/s (e.g. 950):"
            read -r dl_mbit || dl_mbit="950"
            echo "Enter your true UPLOAD speed in Mbit/s (e.g. 950):"
            read -r ul_mbit || ul_mbit="950"
            cat > "$startdir/src/sqm-qos.conf" << EOF
DOWNLOAD_MBIT="$dl_mbit"
UPLOAD_MBIT="$ul_mbit"
EOF
            echo "SQM QoS configured for ${dl_mbit}Mbps down / ${ul_mbit}Mbps up."
        else
            echo "Skipping SQM QoS service installation."
        fi
    fi
    echo "-$pkgrel" > localversion.10-pkgrel
    echo "-${pkgbase#linux-}" > localversion.20-pkgname
    
    local src
    for patch in "${source[@]}"; do
        patch="${patch%%::*}"
        src="${patch##*/}"
        src="${src%.zst}"
        [[ $src = *.patch ]] || continue
        echo "Applying patch $src..."
        if [[ "$patch" == "${_patchsource}"/misc/nvidia/* ]]; then
            patch -Np1 < "../$src" -d "${srcdir}/${_nv_open_pkg}"
        else
            patch -Np1 < "../$src"
        fi
    done
    
    # causes freezes on rdna4 desktop - 9070xt
    patch -Np1 -R -i "$srcdir/0020-drm-amd-display-Fix-DCN401-MPCC-OPTC-and-DMCUB-issues.patch"
    patch -Np1 -R -i "$srcdir/1025-drm-amd-display-enable-psr-and-replay-on-dcn4-variant-and-fi.patch"
    patch -Np1 -R -i "$srcdir/1031-drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch"
    patch -Np1 -R -i "$srcdir/1033-drm-amd-display-increase-dcn42b-uclk-value.patch"
    patch -Np1 -i "$srcdir/2000-drm-amd-display-Exit-idle-optimizations-before-programming.patch"

    # === CONFIG: Use CachyOS base config, then make olddefconfig to silently resolve new options ===
    echo "Setting config..."
    cp ../config .config
    
    # Apply our minimal overrides BEFORE olddefconfig so they stick
    python3 "${startdir}/disable_configs.py" .config
    scripts/config --set-str LOCALVERSION ""
    scripts/config -d DRM_PRIVACY_SCREEN
    scripts/config -d MEDIA_PLATFORM_SUPPORT -d MEDIA_ANALOG_TV_SUPPORT -d MEDIA_DIGITAL_TV_SUPPORT -d MEDIA_RADIO_SUPPORT -d MEDIA_SDR_SUPPORT -d DVB_CORE
    scripts/config -d IIO -d INFINIBAND -d ISDN -d CAN -d PARPORT -d FIREWIRE -d PCMCIA -d GAMEPORT -d MOST -d GREYBUS -d COMEDI
    scripts/config -d DRM_I915 -d DRM_XE -d DRM_NOUVEAU -d DRM_VGEM -d DRM_VMWGFX -d DRM_GMA500 -d DRM_UDL -d DRM_AST -d DRM_MGAG200 -d DRM_QXL -d DRM_VIRTIO_GPU
    scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE -e CPU_IDLE_GOV_NAP -m V4L2_LOOPBACK -m I2C_CHARDEV -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 --set-str DEFAULT_TCP_CONG "bbr3"
    scripts/config -e PCIEASPM_PERFORMANCE -d PCIEASPM_DEFAULT

    scripts/config -d GENERIC_CPU -e MZEN4
    scripts/config -d LTO_NONE -e LTO_CLANG_THIN
    scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3
    scripts/config -e CACHY
    scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1" -d CMDLINE_OVERRIDE
    scripts/config -e DEBUG_KERNEL -d DEBUG_INFO_NONE -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -e DEBUG_INFO_DWARF5 -e DEBUG_INFO_BTF
    scripts/config -d SECURITY_APPARMOR -d SECURITY_APPARMOR_DEBUG -d SECURITY_APPARMOR_INTROSPECT_POLICY
    scripts/config -d AUDIT -d AUDITSYSCALL -d AUDIT_ARCH -d SLUB_DEBUG
    # Enable BPF, Kprobes, Kallsyms_all, and Tracing infrastructure for bpftune & sched_ext
    scripts/config -e BPF_SYSCALL -e BPF_TRACING -e BPF_EVENTS -e BPF_KPROBE_OVERRIDE \
                   -e KPROBES -e KPROBE_EVENTS -e UPROBES -e UPROBE_EVENTS \
                   -e KALLSYMS -e KALLSYMS_ALL \
                   -e FTRACE -e FTRACE_SYSCALLS -e DYNAMIC_FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER
    # Enable IFB and Mirroring for CAKE SQM Ingress shaping
    scripts/config -e NET_CLS_ACT -m IFB -m NET_ACT_MIRRED -m NET_CLS_U32
    
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

    if [ -f "$startdir/src/.enable_sqm" ]; then
        echo "Installing CAKE SQM network shaping service..."
        install -Dm755 "$startdir/sqm-qos/sqm-qos.sh" -t "$pkgdir/usr/local/bin/"
        install -Dm644 "$startdir/sqm-qos/sqm-qos.service" -t "$pkgdir/usr/lib/systemd/system/"
        if [ -f "$startdir/src/sqm-qos.conf" ]; then
            install -Dm644 "$startdir/src/sqm-qos.conf" -t "$pkgdir/etc/"
        fi
        install -d "$pkgdir/etc/systemd/system/multi-user.target.wants"
        ln -s /usr/lib/systemd/system/sqm-qos.service "$pkgdir/etc/systemd/system/multi-user.target.wants/sqm-qos.service"
    fi

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

b2sums=('46bb6126b1f11442b657f31c6d2025a347c44aa9ce5688bbd678264a9ba9d34ba50c7582580fb20796e73998996588b3aac161a7d36a0db2c2700f6513ed4b14'
        'c5f7991fb1cc8a734264b4430f6cc7c0ebf748da134cd65be61027888dd29f07050d3707fccd3edc546994258176093555ba8ebdfe4e1a018036eccefaf2ab82'
        '2e1adcb9b758c8bfbacf551b668151c505e5bed07790bbd6c16705a14574bd89f3e44215e3cf8fc6a0f12db87fc1eb2e3aa582b02335270f53454aa58dacaa3f'
        '33750094506fee9c45156e65373cfa71365d922da9cc6a423534efad570ff2e28099dc93ade9f85c91be289410289edbf66c1532d40159f26fc116e8e0f45f5c'
        'af0cec1d21fa0034b95b607c36cea87ce88b02a2c4695b2226652bc14906e87200958eaf14779f8b3736cad028cac7cf3b656b30af84fd472dfb58b112e25db8'
        'a6550cb9e602bc3faeb025594c226bc989eccdad4fcffde324829fe7ccd2c7a3732a28be2c5ba0050ffbec1e77c2a335fcc624928bc8600b3d65347cb2f1a263'
        '0c1bc7e706ca8a3b8522fc05d14c1fadaf025426a6812a3fbc2334446f7e970c6e91b63db799147a94eb55c16eed81f0e472f27ed049a8a7d305efcb578d2453'
        'c8ae487d06e2c065f4799f5e66d1e6ee930e647c73c540a53710b0759d7ab39ca1129891e0bfca277ebdb98949913134701a7c10c2ea69b7b7ce2280b8bec102'
        '9d75d086f262c1b55794246526fc55f73849d528697bed34fc949d34741dd5bebdc3cc9330aeb88d69c753d3442332f873958b8fb6b57151f33576d0ca8eb691'
        'a829fe93e802803daeb1978f3a9ae51102943c6e240f849dc2875bb668032b582ec7cbfdc2daecaee7b5bd4b23ad2c5dea85ada9fae3ee97ef2130bab9540618'
        '705790e17ca806c0d47033033c88c024f3a4dba5563561b14f4e537ddc387a5b6fd8ec42d42e8a9c426b04eb996ff6ea279bdd5269bb0fd25dcff74a37b08b74'
        '2755456cf12464ce4173c2bdc26397ccbdedf4ab1ab37191d55711acd5ccfd27764d4a44ce6d69317c7a3f8ba0cf67f7d5eac2a3846e4bd174f49d7be80a068b'
        '6fbec5f5f892fc6835e587d2798dd05dd90ee75dab9d1eedc7735d9022012eb1a9f399dba96e8ffba10024cb0ed1730bb62a8f592c75ab13fe1898a4d89a5a7b'
        '71e73173376279419e605b85d0625834ee2e694258aa355b1c435cdc78eb395ddde5d6c545bc2f1cb4f4e7d7dcb7c29c1d7abc5cf56cafa346718faa76fbf299'
        'aad86c7d3e29956976634971ed46663e67365517b69e35e7cce3e135bcc855c324187dd691630af28a5da7045e6766d52a3b2392726b0bc8587a221f9eedca48'
        'e9d464ebf525cd8d93d48f1cbedea0197bd9d0142085da7d83ec3dfda0174483a0fea4077055fd7d1ad9180563dc6dfb77e4f52f9bcb023b7c7d7c9fb5c39ece'
        '9d3e36dbc5c9c5342d2991c4665278ed075073196251e59280bd12f1d6812a37d31db58f5cb978b926e2dcd0a32365960a414b69d10f463bd8f68cedbb4bb6ae'
        '52fe01328f544e023666eab1fd378ae0a0eb47385d495403a55a933f71beedcf295300767c1e43feb46366915fae8bea3b9137f11d16ed194a1fcf71d95aec0d'
        '13820827f675672c4a41cd19d59517113a27ab607a935074b57026736e2f54bab0e60b82c32ad5e3304e0594059f664bb8463068cd4b8673501f748b9bde268d'
        '4e1d799e10d3e37c4bbc61f9696bb76d4ee9908b63731473d4664c94c12679618c1a4e6ecd028b821e4a840a74a780f477cbb19cbb3b54482373900145406f73'
        '5f90f7eaef640dec990030967987f44e9f9a429e65edc20789e200b90836c5263b827e9c4c07f18a1c13d167365736489edbdffaef4f4965d1d8bb38cfa6e2ef'
        '9dfb09f65d28ca3cbbe7bcf1c7e064a3c3abf61a6ca3ba4e270fd44123fbfcb5fb919c814926965f1dbdbdcf92cc793103cdf22457ed454c5016b54d2b843eae'
        '02803704ce3fe311f9bc88e0cdeae545829023a7c3c241a00f4a2bc07ffd27fe5089010b4fc0456c56898bbd09ab93ab3d764cfa97080a5aaf114df1bd91680b'
        '692244e62c6d34c7aca8fda750d18befaefdc02a3be11632aeb6a69327645e6814efb00a4c475bfc407c0dabbce0b5d88c86262acbf32b29111c5e99e2acabd6'
        '9395fc7d168c7cd6cb6b13edbedc2adc58a4a18cd024ae259345034b06bac84e8f9a34334508cd3571aaedb22e85aa2c9a01cd11e5c5336be148e07d63230bd8'
        '90b8ca8a98554f9e7ca261662756a06de878d95290ca0dff39ba372d3cabf14408f22152a06bb39448317ec4de271d4182fc28ffe4e282bb959e7aadded4a7cd'
        'e0ba03ac5c3025163ab010f1e53ac5600af1ff96bd9ec5aa71a7c6cd021e343cf5468510bd03425d1a8e0f67058771074bfc381885a2d097e57c819932b033fb'
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
        'd6e8fc6966cc4200e6d322498f6ecb40306c3dab0d1e866987b52799bffeb8cf94251b894671f69ba57592a04910297bb7e75cb034745257b2b5eb5be26c2c62'
        '3e8a7073870adc34638e6c067051dd7939c61ff7721cda8940e8186cf80890493e660453863a89037f5a4a88f74995dcb5434ae8b9308339ddc4a76f7dac8718'
        '592222f8b84b02cb41b9bbe485aff7a8886a04fee9384241c7f55208792dea6035cd0cd204e040f29e8f095eb16ddfe93f6e8469318591a066a2f4a31ecb0c86'
        '2091f3c722ee0d17fc054d4c08d7c4d918c299dee18d7e46fa4e27684d4674a491e1b2b7112a356411365d1a975866493637d1eb4f8f2f3f601c317c26610441'
        '1bf085acac7b0be9ebe1da858a4ef4900d88208efeceee8d6394a5d28c131bfec8abc1714dccdf4f435e5335e0dc772efbbe8935a8695fc8e85dce6a3501f54b'
        '4633a57fb821830cabf5bbe83c31293037143a0268467c06a18cedd2bdcbe89fccada131d1930adcd1ea64f7b57376c183534ef21cb4d9b9bfb989a3cef8a2bb'
        '086fc64dfdba852d870e776de89b1fb4d9945535dc7d512aba18aa21951f9e152b05762c7a26b4ac4a4a207323e525c4060d7802c0169cd0354d8bf8e80e5d68'
        '8b010822b1dd02b8cabd34740aa6238f7306d9ff203f83ae4a74427a5df77a7ec2b0ffc2aa4b7189a6a95c75e963e68aebb3cf727f908add27889900d9c71a55'
        'c20b3b791715d02756742bfa34f4921bcaebeee62edf079fe15c89afdc11451a2656122f4f21335cd116676ff69c3b7eee80c6adfdcbfe838c0f1e9012ce0428'
        'df68cfd344b37cae25fa446c82c5897510de23c55761570969dc5a6f2a5bf4c11b31e50c1670a18bef1065af6597e72e0ed839e8fdbc0328cf2dcf34484e5758'
        '8bff27696075ec53ca042b0c9e0deae345712e652b3b66bab1da82c4deefdf35533d04c00d59de70cbf968380236131bc819e0eeaa8aa40edfd84df3bd0972ef'
        '48c6c8a299d0d5341475936ea8e1974fc933de81fa710c483c0fa54d7d7a70ccb15c56da1b4cf66bc0c4fe486f78f6b74816b38f602ed219e5dd7f679fba2662'
        '2b9bad240296578ddb6a81629263d046b7e2d9ba063faaae38279c98556749b1b1ae6ccc3036a551fabea3d01ce916cffad1f1e56a65b3eab31faaa37de96211'
        '26a27c3771496e964810ad07ba7f05a84af2a8b469736a0c43b443e5c4160567c70fa294e45ec799f2422086767696683a99c6837295776c78c646517e56326e'
        '5cce1017a1404ff24b2d45ee5d9d99efd07745b225eb25ee7ddbdc1f742e9ae612adbbac8a5e2d82f013d4c6bf1250c4b804b361e2a4ab0d2b4c30063fd804bc'
        'dc4e862e8f9fa7e8ead895908459757afd1027c24b960ae3d289a7212e29575bce3ce4627d5fd73edf211ee162dfa545e1642c5b16e8156f3dce50af8ef3c256'
        'SKIP'
        '116ec92181c091e7e57f3c88b159a7080d3f3dfd05ed661da95811dd58209e4b83a69edfc47a57126524c014cdc0bb7b72f9be94294237c24461ac702e2b1206'
        'd3f9e4ba02082d133283cc0b90432c33fae70f256c8fc2f469994df95e5ac5beceda8af330ff79c1c5de25412f32d7390cf59f53c0c502335adf9863844c65db')

if [ "$_use_kernel_org_llvm" = "yes" ]; then
    source+=("https://mirrors.edge.kernel.org/pub/tools/llvm/files/${_kernel_org_llvm_tarball}")
fi
