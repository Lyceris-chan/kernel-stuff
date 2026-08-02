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
  "https://cdn.kernel.org/pub/linux/kernel/v7.x/testing/linux-7.2-rc5.tar.gz"
  "config"
  # ── 00xx: Handmade local patches (Sleepy/Antigravity) ─────────────────────
  "0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch"
  "0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch"
  "0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch"
  "0004-drm-amd-pm-Disable-deep-sleep-in-PROFILE_PEAK.patch"
  "0005-drm-amd-pm-Disable-SMU14-mode1-reset-for-SR-IOV.patch"
  "0006-drm-amd-pm-Add-bounds-checking-for-SMU14-I2C-command.patch"
  "0007-drm-amd-pm-Remove-redundant-mutex-lock-in-SMU14-I2C-.patch"
  "0008-drm-amd-pm-Fix-SMU14-power-limit-reporting-logic.patch"
  "0010-drm-amdgpu-gfx12-Fix-named-barrier-restore-in-trap-handler.patch"
  # ── 003x: Handmade DCN401 display fixes ───────────────────────────────────
  "0030-drm-amd-display-Proactively-shrink-DET-for-pipes-los.patch"
  "0031-drm-amd-display-Fix-memory-leak-in-DCN20-link-encode.patch"
  "0032-drm-amd-display-Fix-OOB-array-access-for-HPO-FRL-lin.patch"
  "0033-drm-amd-display-Fix-missing-HPO-FRL-link-encoder-reg.patch"
  "0034-drm-amd-display-Prevent-memory-leak-during-IRQ-servi.patch"
  # ── 005x: Upstream AMD FreeSync/EDID/HDMI patches ─────────────────────────
  "0050-drm-edid-Parse-AMD-VSDB-for-FreeSync-refresh-range.patch"
  # Fangzhi Zuo 2/4: HDMI 2.1 gaming caps (ALLM/VRR) from HF-VSDB
  # <20260730171754.704049-2-jerry.zuo@amd.com> — CLEAN on rc5
  "0055-drm-edid-parse-HDMI-2.1-gaming-ALLM-VRR-caps-from-HF-VSDB.patch"
  # Fangzhi Zuo: restore FRL cap on non-destructive HDMI link verify
  # <20260730205047.1016922-1-jerry.zuo@amd.com> — CLEAN on rc5
  "0058-drm-amd-display-restore-FRL-cap-on-non-destructive-HDMI-link.patch"
  # ── 0101-0109: CachyOS branches (squashed to one patch per branch, 2026-08-02) ──
  "0101-cachy-bbr3.patch"
  "0102-cachy-kbuild.patch"
  "0103-cachy-cpu-isa.patch"
  "0104-cachy-cgroup-vram.patch"
  "0105-cachy-fixes.patch"
  # 0106 reverts the off-target hardware patches included in the full fixes branch
  "0106-cachy-drops.patch"
  "0107-cachy-hdmi.patch"
  "0108-cachy-preempt-ipi.patch"
  "0109-cachy-vesa-dsc.patch"
  # NOTE: Zuo 1/4+3/4+4/4 deferred — need amdgpu_dm_connector.c split (not in rc5 yet)
  # Excluded: i915, btusb, rtw89, i2c touchpad, laptop audio, SOF, nouveau
  # 0151 dropped: drm_edid.c + drm_connector.h changes already applied by 0055 (Fangzhi Zuo 2/4)
  # ── 1000-1019: AMDGPU GPU core (GFX12, GMC, SDMA, TTM) ───────────────────
  "1000-drm-amdgpu-gfx12-1-warn-rather-than-bug-for-invalid-sdma-eng.patch"
  "1001-drm-amdgpu-gfx12-warn-rather-than-bug-for-invalid-sdma-engin.patch"
  "1002-drm-amdgpu-allocate-enough-space-for-hpd-info-on-gfx11.patch"
  "1003-drm-amdgpu-gfx12-only-need-to-remap-kcqs-when-reset-via-mmio.patch"
  "1004-drm-amdgpu-gmc9-disallow-gfxoff-around-TLB-flushes.patch"
  "1005-drm-amdgpu-gmc10-disallow-gfxoff-around-TLB-flushes.patch"
  "1006-drm-amdgpu-gmc11-disallow-gfxoff-around-TLB-flushes.patch"
  "1007-drm-amdgpu-gmc12-disallow-gfxoff-around-TLB-flushes.patch"
  "1008-drm-amdgpu-add-an-buffer-funcs-callback-for-TLB-inva.patch"
  "1009-drm-amdgpu-sdma5.0-add-tlb-invalidation-buffer-func-.patch"
  "1010-drm-amdgpu-sdma5.2-add-tlb-invalidation-buffer-func-.patch"
  "1011-drm-amdgpu-sdma6-add-tlb-invalidation-buffer-func-ca.patch"
  "1012-drm-amdgpu-sdma7-add-tlb-invalidation-buffer-func-ca.patch"
  "1013-drm-amdgpu-add-core-helper-to-do-TLB-invalidation-vi.patch"
  "1014-drm-amdgpu-gmc-add-more-gmc-tlb-inv-helpers.patch"
  "1015-drm-amdgpu-gmc10-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1016-drm-amdgpu-gmc11-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1017-drm-amdgpu-gmc12-switch-to-new-gmc-tlb-inv-helpers.patch"
  "1018-drm-amdgpu-Switch-order-of-GC-and-Display-IP-blocks.patch"
  "1019-drm-amdgpu-update-mmhub-4.2.0-client-list.patch"
  "1100-drm-amd-display-enable-psr-and-replay-on-dcn4-variant-and-fi.patch"
  "1101-drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch"
  "1102-drm-amd-display-increase-dcn42b-uclk-value.patch"
  "1103-drm-amd-display-add-dcn42b-specific-SMU-clock-table-.patch"
  "1104-drm-amd-display-Add-MALL-status-readback-support-for.patch"
  "1105-drm-amd-display-Add-DCN42B-VID_CRC_CONTROL-and-HBLAN.patch"
  "1106-drm-amd-display-update-memclk-clock-table-read-for-d.patch"
  "1107-drm-amd-display-enable-hdmistreamclk_rcg-by-default-.patch"
  # ── 1108-1112: DCN401/DCN42 display fixes (drm-next, 2026-07) ─────────────
  "1108-drm-amd-display-Add-MCIF-ARB-programming-structures.patch"
  "1109-drm-amd-display-Add-updated-MCIF-ARB-register-definitions.patch"
  "1110-drm-amd-display-Port-DCN4-MCIF-ARB-programming-to-new-format.patch"
  "1111-drm-amd-display-Fix-dc_stream_remove_writeback.patch"
  # 1112 dropped: dcn401 GPIO lookup tables requires prerequisite GPIO infrastructure patch not in rc5
  "1200-cpufreq-amd-pstate-Document-missing-kernel-doc-mem.patch"
  "1201-cpufreq-amd-pstate-Update-cppc_req_cached-before-w.patch"
  "1202-cpufreq-amd-pstate-Add-per-core-EPP-boost-for-rec.patch"
  "1203-Documentation-amd-pstate-Document-the-epp_boost-pa.patch"
  "1204-cpufreq-amd-pstate-Bail-out-early-if-X86_FEATURE_HW_.patch"
  "1205-cpufreq-amd-pstate-ut-Skip-tests-when-amd-pstate-dri.patch"
  "1206-cpufreq-amd-pstate-Fix-EPP-return-type-and-handle-er.patch"
  "1207-cpufreq-amd-pstate-Toggle-auto_sel-in-active-mode-on.patch"
  "1208-cpufreq-amd-pstate-Cache-the-firmware-programmed-EPP.patch"
  "1209-cpufreq-amd-pstate-handle-missing-policy-in-dynamic-.patch"
  "1210-cpufreq-amd-pstate-Loosen-requirement-on-lowest-nonl.patch"
  # ── 1211-1213: ACPI CPPC / cpufreq-cppc fixes (post-rc5 mainline, 2026-07) ──
  "1211-cpufreq-cppc-Sanitize-lockless-policy-limit-snapshots.patch"
  "1212-ACPI-CPPC-Check-all-controls-for-fast-switching.patch"
  "1213-ACPI-CPPC-Skip-writes-to-unsupported-performance-controls.patch"
  "2000-block-mq-deadline-pass-in-queue-directly-to-dd_inser.patch"
  "2001-block-mq-deadline-skip-expensive-merge-lookups-if-co.patch"
  "2002-block-bfq-pass-in-queue-directly-to-bfq_insert_reque.patch"
  "2003-block-bfq-serialize-request-dispatching.patch"
  "2004-block-bfq-skip-expensive-merge-lookups-if-contended.patch"
  "2100-zstd-7.2-merge-changes-from-dev-tree.patch"
  "2101-mm-7.2-introduce-LRU-MARIE.patch"
  "2200-7.2-nap-v0.5.0.patch"
  "9000-drm-amd-display-Exit-idle-optimizations-before-programming.patch"
  "9001-drm-amdgpu-gfx12-drop-all-BUG-s.patch"
  "9002-drm-amdgpu-gfx12.1-drop-all-BUG-s.patch"
  "9003-drm-amdgpu-psp14-replace-BUG-with-an-error.patch"
  "9004-drm-amd-pm-use-milliwatts-for-GPU-power-sensors.patch"
  "9005-drm-amdgpu-restore-UMD-profile-pstate-after-runtime-resume.patch"
  "9006-drm-amdgpu-ttm-Use-more-optimal-copy-packet-sizes-for-copy-and-fill.patch"
  "9007-drm-gfx12-Program-DB_RING_CONTROL.patch"
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
    if [ -t 0 ] && [ -z "$AUTO_BUILD" ]; then
        echo -e "\nWould you like to enable the CAKE SQM network shaping service to eliminate bufferbloat? (y/N)"
        read -r enable_sqm || enable_sqm="n"
        if [[ "$enable_sqm" =~ ^[Yy]$ ]]; then
            touch "$startdir/src/.enable_sqm"
            echo "Enter your true DOWNLOAD speed in Mbit/s (e.g. 950, or press Enter to set in /etc/sqm-qos.conf later):"
            read -r dl_mbit || dl_mbit=""
            echo "Enter your true UPLOAD speed in Mbit/s (e.g. 950, or press Enter to set in /etc/sqm-qos.conf later):"
            read -r ul_mbit || ul_mbit=""
            cat > "$startdir/src/sqm-qos.conf" << EOF
DOWNLOAD_MBIT="$dl_mbit"
UPLOAD_MBIT="$ul_mbit"
EOF
            if [ -n "$dl_mbit" ] && [ -n "$ul_mbit" ]; then
                echo "SQM QoS configured for ${dl_mbit}Mbps down / ${ul_mbit}Mbps up."
            else
                echo "SQM QoS service enabled. Please specify DOWNLOAD_MBIT and UPLOAD_MBIT in /etc/sqm-qos.conf before starting."
            fi
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
            patch -Np1 --forward < "../$src" -d "${srcdir}/${_nv_open_pkg}"
        else
            patch -Np1 --forward < "../$src"
        fi
    done

    # Patch 1101 (.pstate_enabled = true) causes UCLK switching desyncs and desktop freezes on RDNA4 in auto DPM mode
    patch -Np1 --forward -R -i "$srcdir/1101-drm-amd-display-enable-pstate-for-dcn4-non-emulation-builds.patch"

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
    scripts/config -e LRU_GEN -e LRU_GEN_ENABLED -e LRU_GEN_WALKS_MMU -e LRU_MARIE -e CPU_IDLE_GOV_NAP -e MQ_IOSCHED_ADIOS -e MQ_IOSCHED_KYBER --set-str DEFAULT_IOSCHED "kyber" -m USB_VIDEO_CLASS -m I2C_CHARDEV -d TCP_CONG_BBR -e TCP_CONG_BBR3 -e DEFAULT_BBR3 --set-str DEFAULT_TCP_CONG "bbr3"
    scripts/config -e PCIEASPM_PERFORMANCE -d PCIEASPM_DEFAULT

    scripts/config -d GENERIC_CPU -e MZEN4
    scripts/config -d LTO_NONE -e LTO_CLANG_THIN
    scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE -e CC_OPTIMIZE_FOR_PERFORMANCE_O3
    scripts/config -e CACHY
    scripts/config -e CMDLINE_BOOL --set-str CMDLINE "cpuidle.governor=nap amd_pstate.epp_boost=1 elevator=kyber" -d CMDLINE_OVERRIDE
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
        '23f570909d870d709e9b9f414d8a9f543da492085c0ed457e6896d995e5cd608f7e45f3bdc96a5f09b595fb04e24babd6b9811ed03ea8d9598996aea0e890a9b'
        'a7cefe36f18ea4390b41849e604ad6257cccdbf25c2af380d2353397858cba21f6eb02b0774ebc24ec26639539a8858a29262b02edb60eba5736cd172993480f'
        '458b2cb2413befbbd76c22bd541da17694965d535b486df65fc6b5c470a8b06ddbb0224f25dd966d53210de2d9559da04b7822f688e5f0034ec0094d2f276be8'
        'a6704c51338fc584baa37ccf604ffa6ac5399e73b696404c8d45f521506ccec417207aa6a1665c28efb8b2b2b12e6c436ddb5bb8bd4a36c6e5020541ecef6494'
        '00a418320c6cbcf9c40c88434eb14723b6c97c2a8906586157f993e73aca27000ffa88adbd9dab708405b4c38737c8f72d295a59e4e2cc9da1cf91ef2ba3b751'
        '3e1ebc3b867d8b3a0d25f83987ae83ce20949513fe8fdd923faa0bfc92b607b894cf64e8e1e70fd0b9617477fac3f014e733259519c41a963367ad92e59146d6'
        'ec5bf6d8b50fb282141b72f8446e312170cf2243c1e0a0289a378393ccc014d55c1a0eb39756f955b109ad80344be59b2c148c3e3ebba13227e4a0af467ca26b'
        'f77a07fc6c53ce2862753a110810a7e817b6fec2923132c1fb608e707d769b7719ff912c73c9e72c045155dfc704f02b78e03526ace115c4220b66419764799b'
        'd370e2464a5c2990f9c9f9899b959aa3c2cd55914f06e410446978cb00d632e9691ce0fed3f8288cf63abcf35f16c76e618df754e2194630b164abfa808a70d4'
        '3b714e3460b4d607c120802a2388d121238c87468fd9a733cd3b65c17f20391c0b03147f824aaddefbc4a4a5ce4f22bd65e39c5164f7846c09518f63b54a755d'
        '9d2e7cfd2a8cb089fd3da7be483c293544c5c3bbd40c097c152321f75131057d20616abd712d1a193292ea9977400c1af32d8318c9b0e71de4b838be7176e2e8'
        '12358025d6531fceb1df3dc4a32368be1bd1b528e3685b9b2505027fef898bfab26fe18306bebaab2a8163cd6697e40db487f96766f9631ad8f4be825bb0e1bc'
        '2b7e1ea1ff4592bc8484e97a274c2aac959ccca317cec9523deaf4472be8c91d472567ae4a7029e4afb2dece0b9a934ce94a35ff9da938e26ef0e1d5a1612079'
        '48064b932392d2d8b7c33903a88ec99a5c7d0baf723b58331eeb6bba2e632ec7a38ff1efe8cb022fc95fb50a270f5d57bc075bed0215fe65847c555a7949f706'
        '92148f845b35b0ad77fad1b004fa8625385bfbabd1b83b4a4ba262bb44a51e611473bfc05524cf72db85e3c53838d99175149d035b3ddeea24c3435e1d145e93'
        '57d214236c741a78f0f2b7e0667ffdf8be422aac2d290e03a4e1961cd80a2e444638a044b97fe95b6ef345d3443d6395d522d23ce1ac2be63adee3834304f407'
        'f61685cae107b07fd76a108f80cb0452378c672180a98dd49cf0707a7a6013162f20c1f893f080add632d8ad3fe1e0667db1a4d494f16bd2bd980eee506bbf91'
        'bb8068b44b22abd2316e41425cc250e517bcd76b52885a6ab81de8129f1a82bb93e6f048d521325666cbddb23f32cf74038abc577d1fbe6a20e655dc3f852137'
        '1cb6e0ae6f57e9eca2067594ce83c005c6bc49e6a3d7fb11aa1aeee12204691304da0483e5be3c20b233c132a54831ffa587765599634a5ad123489e99982a58'
        'ee5f2c4aead1f2fc8d8096ae2a953d4c45d4c79de29e0578da543767a2d96664f903f043af36cf481adc13f203e2eca8fb616c26257e6cce5b3cae26b1d46ddf'
        'fdc7fc1d942be4fe8dadcb228b7f9c02273eaec91631ff609a07722b74b1db64828e144856e01a8ffd039762d1970a7ec511a3d240481544c570592914573b69'
        'b6be0eb69eb52e27b8aad11d56e17965a6cddfa480ab665e8d03274bb7fdec1bd6adb943414c8338e2eb19ad3a23f6cc6fa5e7397d193b65ee57b3ab439493d2'
        '3c996978423ed2c0158a621618ff5a065a8627bc2e27b222437178eee10a463b5339175245b9ec11b7802e99f4ecd40d1ba1e35ba11bed74688c00c48bb67104'
        '3f8b82e864524f9a3226c6c1bd04283dd4e23e14bcbe22f842fb989565409a26f7abd285ffe022dfdd1c5b606976a92964eb26ecdeb1a4797934cf3ab7f44f24'
        '7163c9c1549000442721f60b54798fe6e15901285a2f750efb5676a7e81612c3d0bc34e639c9d373d0c6c2f2f805484a51a9e2006e5e1435bd4ae425fa5acd00'
        '1e5978896fe68926133ad6ee291f9b5eb59a550d689118f0dc2bebc793add069785c5b151fb339dbf85213badd790b0383144394217591aeedaab63cd89f3f66'
        '8fa361ac6a9d4b2c8254d4cbd0bbd9bec9d09b633d8bfd0d97f71248194c82714737f6fcbb04db85e727763a000d53d6e0c13c74848dbe21ff2927d33734c221'
        '5f90f7eaef640dec990030967987f44e9f9a429e65edc20789e200b90836c5263b827e9c4c07f18a1c13d167365736489edbdffaef4f4965d1d8bb38cfa6e2ef'
        '9dfb09f65d28ca3cbbe7bcf1c7e064a3c3abf61a6ca3ba4e270fd44123fbfcb5fb919c814926965f1dbdbdcf92cc793103cdf22457ed454c5016b54d2b843eae'
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
        '9882a49729b1030941352cda465deaa36965b288a03acca7030fc9b9f1dd74e7e8257895da29b2ebd38041bf5d89d555335ef5c635379261957c563348d0b1f0'
        '02803704ce3fe311f9bc88e0cdeae545829023a7c3c241a00f4a2bc07ffd27fe5089010b4fc0456c56898bbd09ab93ab3d764cfa97080a5aaf114df1bd91680b'
        '692244e62c6d34c7aca8fda750d18befaefdc02a3be11632aeb6a69327645e6814efb00a4c475bfc407c0dabbce0b5d88c86262acbf32b29111c5e99e2acabd6'
        '9395fc7d168c7cd6cb6b13edbedc2adc58a4a18cd024ae259345034b06bac84e8f9a34334508cd3571aaedb22e85aa2c9a01cd11e5c5336be148e07d63230bd8'
        'd6e8fc6966cc4200e6d322498f6ecb40306c3dab0d1e866987b52799bffeb8cf94251b894671f69ba57592a04910297bb7e75cb034745257b2b5eb5be26c2c62'
        'a0d53c2bdebaa52875cb14d8491e2d051c3ab12529f42cf4a44ace8757876e5a1bf9c7124967e946bfd02a3f171c0e90ae4e22f8a9b77ac8a81c6986271df852'
        '1f97267769ca34e9d1314a19a7b6db66cc1c96fab4e2b65d5732d614655ab198595afa48b2028f34ef381ab5c239d861ab1b36b261916bde5b8511fb059920f7'
        'b7c3d48fffc08d90c434a597623d0b6030c1b40614aa946b92e815852ecb3fca6f8cc7f05aedb57ccff1a2cb64cae6759ffba192a7bcb3f7ec8c2848ee46f17b'
        '34c79642d68eb9a4a04f1d3dde46ef5e96dee8360c478bc62b8c4eb14d7f3bb5655ee40b4ee9f91025871cd095385e5d5554a550c748d2e284bd2fccef674262'
        '6f95ad517c04273b00d2b56858ea3afe7010e88b404df87cd4d32212994e1864c0cebd34a663e1d561acd498ea6c6583d169a27eb6bd2405e1532d56963133a4'
        '166da22fdf4e5d4bff79d16888b55b7290bfa363d3f64a33bdbcebb56cb796d6fa9a6070477ace108947284a4f64ff560f7e85cc1b0abc23f164ec9c7b145d6f'
        'defc3d776fb7ab16215a8df6951b8c2dddaf7f19838cd5123732e6d9e16cc504410b4fdbd0ad547a198cf0164ba513f32c5191273a67ac1b8721a6f7797d95ae'
        '40e7f2df3c07a21af963e0f8dca7a11b4db43b15ea52cbfc42caee01180d5fda91cc4391fa3cc5d84ee42870ae8fa73dd17025b2115691f010af531cdc63c025'
        'aad86c7d3e29956976634971ed46663e67365517b69e35e7cce3e135bcc855c324187dd691630af28a5da7045e6766d52a3b2392726b0bc8587a221f9eedca48'
        'e9d464ebf525cd8d93d48f1cbedea0197bd9d0142085da7d83ec3dfda0174483a0fea4077055fd7d1ad9180563dc6dfb77e4f52f9bcb023b7c7d7c9fb5c39ece'
        '9d3e36dbc5c9c5342d2991c4665278ed075073196251e59280bd12f1d6812a37d31db58f5cb978b926e2dcd0a32365960a414b69d10f463bd8f68cedbb4bb6ae'
        '52fe01328f544e023666eab1fd378ae0a0eb47385d495403a55a933f71beedcf295300767c1e43feb46366915fae8bea3b9137f11d16ed194a1fcf71d95aec0d'
        '3e8a7073870adc34638e6c067051dd7939c61ff7721cda8940e8186cf80890493e660453863a89037f5a4a88f74995dcb5434ae8b9308339ddc4a76f7dac8718'
        '592222f8b84b02cb41b9bbe485aff7a8886a04fee9384241c7f55208792dea6035cd0cd204e040f29e8f095eb16ddfe93f6e8469318591a066a2f4a31ecb0c86'
        '2091f3c722ee0d17fc054d4c08d7c4d918c299dee18d7e46fa4e27684d4674a491e1b2b7112a356411365d1a975866493637d1eb4f8f2f3f601c317c26610441'
        '1bf085acac7b0be9ebe1da858a4ef4900d88208efeceee8d6394a5d28c131bfec8abc1714dccdf4f435e5335e0dc772efbbe8935a8695fc8e85dce6a3501f54b'
        '4633a57fb821830cabf5bbe83c31293037143a0268467c06a18cedd2bdcbe89fccada131d1930adcd1ea64f7b57376c183534ef21cb4d9b9bfb989a3cef8a2bb'
        '086fc64dfdba852d870e776de89b1fb4d9945535dc7d512aba18aa21951f9e152b05762c7a26b4ac4a4a207323e525c4060d7802c0169cd0354d8bf8e80e5d68'
        '8b010822b1dd02b8cabd34740aa6238f7306d9ff203f83ae4a74427a5df77a7ec2b0ffc2aa4b7189a6a95c75e963e68aebb3cf727f908add27889900d9c71a55'
        '10513190fe80eea036dbc1dc399da9fb9ec04703b8d298d73a7952f7de37ae898fa688a39a46ec948e69210d82c3d987f053fa443675b35fb9020e7bd1a4305d'
        '23980ab7fc770fac63d3135b772263bffa72bb68762b33c745770e61400398cc99c5bcb6ed72210ac1f4ef5b7e1fe2f738fb352b295818a4bedf723c8cdcb489'
        'de2ea9470c7925ae9157aa28a7b79cb619f92179b56d75f328625282083aa5215a04b1b875cba9bcfede1be46f38fe3cfa7e88ff4c6ac5d5e2e38967f068259a'
        'c20b3b791715d02756742bfa34f4921bcaebeee62edf079fe15c89afdc11451a2656122f4f21335cd116676ff69c3b7eee80c6adfdcbfe838c0f1e9012ce0428'
        'df68cfd344b37cae25fa446c82c5897510de23c55761570969dc5a6f2a5bf4c11b31e50c1670a18bef1065af6597e72e0ed839e8fdbc0328cf2dcf34484e5758'
        '8bff27696075ec53ca042b0c9e0deae345712e652b3b66bab1da82c4deefdf35533d04c00d59de70cbf968380236131bc819e0eeaa8aa40edfd84df3bd0972ef'
        '48c6c8a299d0d5341475936ea8e1974fc933de81fa710c483c0fa54d7d7a70ccb15c56da1b4cf66bc0c4fe486f78f6b74816b38f602ed219e5dd7f679fba2662'
        '2b9bad240296578ddb6a81629263d046b7e2d9ba063faaae38279c98556749b1b1ae6ccc3036a551fabea3d01ce916cffad1f1e56a65b3eab31faaa37de96211'
        '26a27c3771496e964810ad07ba7f05a84af2a8b469736a0c43b443e5c4160567c70fa294e45ec799f2422086767696683a99c6837295776c78c646517e56326e'
        '78acc6c4a600368561042b3b1a99d295a778699fb76727fcd74107afd8106c134c83f46eea49c9582c9a735e1e6e3d128aaab38e1505ce5beb8f0dc625f84854'
        'dc4e862e8f9fa7e8ead895908459757afd1027c24b960ae3d289a7212e29575bce3ce4627d5fd73edf211ee162dfa545e1642c5b16e8156f3dce50af8ef3c256'
        'bb22d1d9315dc65973e681790b79d32629c27808331fd10c3a41e3f946111365919dcd1413f450f76b2a37973c8b8d8f70df34df9ad37c40e4c1c282537c5e5c'
        '4882cc909f5ee8e4c974f3849e4446656895fb8c5f0c10fa0992e5e7c7ae6ce1ded523326bb51c91ff161d15335968434fabb44cf822cb17fd6364c4d8eb24c5'
        '8a9f7682c746fd53536798e7110836059f982b3daa6b95a767249fe9888a3105d0be3dc9917924aba9bba45f0538436a9e3f67f5d958b63ee9288f391f3507ac'
        'c8c7a6f608eb18b41c771b9fca38f254aaea887f761300494520e9164ac5d695c0f58f6f12702c30e291ef1938384fe7110bbb9f260d354b898b5d1b89465108'
        'be0a2e04920f37363f378667dded58dc6318ed45b7e30712030c82982a2d229a57a81e9647fee48a14b0e93030282794654f3303b6716f3c1ab22b059cffdcb4'
        'da08055b309b8ef540bdc449079a26cc6e3ba9b0592cf87de8a5f38f86fc3a297f2c547509973a48f521ade773e55bcc231aac0042027943dadbc9806ff0de72'
        '270c2bb7cb1e3e2540abf29ff51e0babed092c7eebedcea82805a471c145b1e4ed72f34aec076270ee56ad3743fa4fa0c17f85a0e248cc179d3d4706eee7c717'
        'bdc839d1629f22095c5907e62b7a1a4edfcedebe0cf7e430897ae87aa331cbad28e28cef106ae38c05cafa585fa19ddc019579f1b73fcfaa69d8a8bd40ba8111'
        'SKIP'
        '116ec92181c091e7e57f3c88b159a7080d3f3dfd05ed661da95811dd58209e4b83a69edfc47a57126524c014cdc0bb7b72f9be94294237c24461ac702e2b1206')

if [ "$_use_kernel_org_llvm" = "yes" ]; then
    source+=("https://mirrors.edge.kernel.org/pub/tools/llvm/files/${_kernel_org_llvm_tarball}")
fi
