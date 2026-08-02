import re, sys

config_file = sys.argv[1] if len(sys.argv) > 1 else ".config"

configs_to_disable = [
    # Legacy / Non-x86 CPU vendor support
    "CPU_SUP_INTEL", "CPU_SUP_CENTAUR", "CPU_SUP_ZHAOXIN", "CPU_SUP_HYGON",
    
    # Intel-specific CPU features & Thermal
    "X86_MCE_INTEL", "X86_INTEL_PSTATE", "X86_INTEL_MEMORY_PROTECTION_KEYS", "X86_INTEL_TSX_MODE_AUTO",
    "INTEL_SCU_IPC", "INTEL_SCU", "INTEL_SCU_PCI", "INTEL_HFI_THERMAL", "INTEL_LDMA", "PMIC_OPREGION", "INTEL_RAPL",
    "PINCTRL_BAYTRAIL", "PINCTRL_CHERRYVIEW", "PINCTRL_INTEL", "INTEL_IOMMU", "INTEL_IOMMU_SVM", "DMAR_TABLE", "IOMMU_PT_VTDSS",
    "INTEL_SOC_PMIC", "INTEL_SOC_PMIC_CHTWC",
    
    # Hypervisors (we build for bare-metal Zen 4 desktop)
    "HYPERVISOR_GUEST", "X86_HV_CALLBACK_VECTOR", "PVH", "JAILHOUSE_GUEST", "ACRN_GUEST", "BHYVE_GUEST",
    
    # Non-AMD / Non-Desktop DRM GPUs
    "DRM_I915", "DRM_XE", "DRM_NOUVEAU", "DRM_VGEM", "DRM_VMWGFX", "DRM_GMA500", "DRM_UDL",
    "DRM_AST", "DRM_MGAG200", "DRM_QXL", "DRM_VIRTIO_GPU", "DRM_ETNAVIV", "DRM_HISI", "DRM_LOGICVC",
    "DRM_MXSFB", "DRM_IMX_LCDIF", "DRM_ARCPDU", "DRM_BOCHS", "DRM_CIRRUS", "DRM_GM12U320",
    "DRM_XEN", "DRM_V3D", "DRM_VC4", "DRM_LIMA", "DRM_PANFROST", "DRM_PANTHOR", "DRM_TIDSS",
    
    # DRM Privacy Screen (Laptop hardware e.g. HP Sure View / ThinkPad PrivacyGuard)
    "DRM_PRIVACY_SCREEN",
    
    # Media / TV Tuners / Radio / Embedded Media Platforms (Strips Exynos, Rockchip, Allwinner, TI, etc.)
    "MEDIA_PLATFORM_SUPPORT", "MEDIA_ANALOG_TV_SUPPORT", "MEDIA_DIGITAL_TV_SUPPORT", "MEDIA_RADIO_SUPPORT",
    "MEDIA_SDR_SUPPORT", "MEDIA_TEST_SUPPORT", "DVB_CORE", "DVB_NET", "MEDIA_TUNER",
    "RC_CORE", "LIRC", "BPF_LIRC_MODE2", "RC_DECODERS", "RC_DEVICES",
    
    # Industrial I/O Sensors (Tablets/Phones: accelerometers, gyroscopes, light sensors, compasses)
    "IIO", "IIO_BUFFER", "IIO_TRIGGER",
    
    # Automotive / Enterprise / Legacy Networking Protocols
    "CAN", "NET_CAN", "CAN_VCAN", "CAN_SLCAN", "CAN_DEV",
    "INFINIBAND", "INFINIBAND_USER_MAD", "INFINIBAND_USER_ACCESS", "INFINIBAND_ADDR_TRANS",
    "ISDN", "MISDN", "ATM", "HAMRADIO", "WIMAX", "NFC",
    
    # Legacy Bus & Peripheral Interfaces
    "PARPORT", "PRINTER", "FIREWIRE", "FIREWIRE_OHCI", "PCMCIA", "CARDBUS", "GAMEPORT",
    "MOST", "GREYBUS", "COMEDI", "NTB", "MELLANOX_PLATFORM", "SOC_TI",
    
    # Embedded / Phone PMICs & MFDs
    "MFD_AS3711", "PMIC_ADP5520", "MFD_AAT2870_CORE", "PMIC_DA903X", "PMIC_DA9052", "MFD_DA9052_SPI",
    "MFD_DA9052_I2C", "MFD_DA9055", "MFD_88PM860X", "MFD_MAX77843", "MFD_MAX8925", "MFD_MAX8997",
    "MFD_MAX8998", "MFD_RC5T583", "MFD_LP8788", "MFD_TPS65090", "MFD_TPS6586X", "MFD_TPS65910",
    "TWL4030_CORE", "MFD_TWL4030_AUDIO", "TWL6040_CORE", "MFD_WM8400", "MFD_WM831X_I2C", "MFD_WM831X_SPI",
    "MFD_WM8350_I2C", "MFD_WM831X", "MFD_WM8350",

    # ChromeOS / Lenovo laptop privacy screen drivers (bloat on bare-metal desktop)
    "CHROMEOS_PRIVACY_SCREEN",

    # Virtualization drivers (bare-metal desktop, no VMs)
    "VIRT_DRIVERS", "VIRTIO_FS",

    # Confidential computing TSM (SEV-SNP/TDX guest attestation, bare-metal irrelevant)
    "PCI_TSM", "TSM", "TSM_REPORTS",

    # VM Generation ID (only relevant for VM guests, not bare-metal)
    "VMGENID",

    # Android Binder IPC (only needed for Waydroid/Anbox containers)
    "ANDROID_BINDER_IPC", "ANDROID_BINDERFS",

    # Remote Processor framework (SoC coprocessor firmware loading, irrelevant on x86 desktop)
    "REMOTEPROC", "REMOTEPROC_CDEV",

    # Device-DAX / Persistent Memory (no NVDIMM/Optane in hardware)
    "DEV_DAX", "DEV_DAX_PMEM", "DEV_DAX_HMEM", "DEV_DAX_KMEM",

    # VCAP (video capture FPGA, enterprise hardware)
    "VCAP",

    # Uniwill WMI (laptop-specific)
    "X86_PLATFORM_DRIVERS_UNIWILL",

    # ThinkPad / Laptop platform drivers that select DRM_PRIVACY_SCREEN
    "THINKPAD_ACPI", "THINKPAD_LMI",

    # Intel-specific audio / thermal (AMD board: no Intel NHLT, DPTF, or silent-stream)
    "SND_INTEL_NHLT", "ACPI_NHLT", "SND_HDA_INTEL_HDMI_SILENT_STREAM", "ACPI_DPTF",

    # Debug build hooks (release kernels do not need them)
    "SND_DEBUG", "ACPI_DEBUG", "DM_DEBUG", "PM_DEBUG", "PM_SLEEP_DEBUG",
    "CRYPTO_DEV_CCP_DEBUGFS",

    # Legacy / niche interfaces
    "SND_OSSEMUL",             # OSS sound emulation
    "SND_SPI",                 # SPI sound cards (embedded boards)
    "AUTOFS_FS",               # autofs automount (no NFS in this build)
    "RESCTRL_FS",              # Intel RDT cache allocation (server / data-center)
    "SCSI_DH",                 # multipath device handlers (no SAN)

    # Mobile-flash filesystem (desktop NVMe uses ext4 / vfat / exfat)
    "F2FS_FS", "F2FS_STAT_FS", "F2FS_FS_XATTR", "F2FS_FS_POSIX_ACL", "F2FS_IOSTAT",
]

try:
    with open(config_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    disabled_count = 0
    for line in lines:
        modified = False
        for cfg in configs_to_disable:
            pattern = r"^CONFIG_" + cfg + r"=[ym]$"
            if re.match(pattern, line.strip()):
                new_lines.append(f"# CONFIG_{cfg} is not set\n")
                modified = True
                disabled_count += 1
                break
        if not modified:
            new_lines.append(line)

    with open(config_file, "w") as f:
        f.writelines(new_lines)

    print(f"Disabled {disabled_count} unneeded configurations in {config_file}.")
except Exception as e:
    print(f"disable_configs.py: {e}")
