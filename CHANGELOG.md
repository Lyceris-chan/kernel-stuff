# Changelog

All notable changes to **sleepy-kernel**, the custom Arch Linux kernel for a
Ryzen 9 7950X (Zen 4) + Radeon RX 9070 XT (RDNA 4 / gfx1201) desktop.

Format follows [Keep a Changelog](https://keepachangelog.com/) and the
[Google developer style guide](https://developers.google.com/style). Versioned
by the running kernel (base + `pkgrel`), e.g. `7.2.0-rc7-1-sleepy`.

---

## [7.2.0-rc7-1-sleepy] — 2026-08-10

Bump to **Linux 7.2-rc7** (tag `linux-7.2-rc7`). The series grew from 127 to
140 patches. Build verified: BTF present for `vmlinux` + modules, `bbr3`
built-in with the old `bbr` disabled, CAKE SQM ingress enabled.

### Fixed

- **GFX12 KFD CRIU-restore NULL-deref panic** (`1026`, amd-gfx ML). On
  gfx1201 the MQD managers leave `restore_mqd`/`checkpoint_mqd` unset, so a
  user holding `CAP_CHECKPOINT_RESTORE` could panic the machine via
  `KFD_IOC_CRIU_OP_RESTORE`. Reconstructed from the mbox (Outlook stripped the
  diff's context whitespace); ML-only, pending an upstream v2.
- **AMDGPU 7.3 backports** (11 total): DCN401 HDR/SDR seamless switch, MST
  `connector->index` bounds check, MST HDCP array resize, DCN42B
  `force_min_dcfclk` clamp, smu_v14_0_0 DPM trio (DCLK metric, DCEFCLK,
  `find_clk_level()`), amdgpu CS/VM correctness (FENCE-chunk leak, VM overrun,
  BO-VA kmap offset), gfx12 userq sub-page VA validation, and the `9037`
  prefer-default-discovery-offset backport.
- **mes12 dropped-dispatches fix** (`1024`): pads the MES queue dispatch so
  concurrent queue oversubscription no longer drops dispatches.
- **DCN42B display fixes**: HPD toggle-filter unit fix (`1135`) and FRL link
  training timeout update (`1136`).
- **LRU-MARIE 0.9.3**: orphaned-L1-bit self-heal — reclaim no longer wedges
  under hot single-type bursts.
- Dropped `1020`/`1021`/`1022` (verified merged upstream in rc7).

### Changed

- **PCIe ASPM off** by default (`pcie_aspm=off` on the built-in command line).
  Stopgap for the drm/amd !5538 SMU bus-drop class — the RX 9070 XT can drop
  off the PCIe bus during SMU power transitions (firmware-side issue; AMD
  engineers suggested ASPM-off).
- **CachyOS fixes branch v11** (`0105`/`0106` regenerated): the branch adds
  the PCI Skip Target Speed quirk (skips 2.5GT/s link-retrain on empty/clamped
  slots, saving ~2s boot) and reworks `mm/mglru`/`mm/vmscan` to the
  `vma_flags_t` API. Net applied effect unchanged except the new quirk.
- `0050` swapped to Alex Huang's v3 (future-VSDB tolerance).

### Deferred (documented, not carried)

- HDMI 2.1 VRR/ALLM v2 (needs the `amdgpu_dm_connector` split not in rc7).
- Valve dmemcg aggressive-protect stack (conflicts with `0104` cgroup-vram).
- gfx12 priv-fault recovery set (needs gfx11 `userq_priv_fault_work` fields).

## [7.2.0-rc6-7-sleepy] — 2026-08-04

Bump to **Linux 7.2-rc6** (tag `linux-7.2-rc6`). Final `pkgrel` of the rc6
line (`rc6-1` … `rc6-7`); `pkgrel` 6 was skipped in git history.

### Fixed

- **36-patch six-source sweep** (biggest single addition): the **retry-fault
  handling v3 series** (`9011`–`9024`, 14 patches — the main RDNA4 stability
  gap), DCN4/DCN42B display fixes including the actual PSR/Replay enable
  (Part 2), IPS/zstate/HUBP-DPP-PG idle-power, the DCN42 DF C-state boot-hang
  backport, and Roman.Li's July-31 DC batch.
- **AMDGPU backports**: gmc12.1 MMHUB0 pasid TLB flush fix, TLB-invalidation
  semaphore, compressed-FRL-cap dispatch fix, gfx12 `TRUNCATE_COORD_MODE` fix,
  mes12.1/imu12 `BUG()`→`WARN()` drops (completes the `9001`–`9003` family),
  oversized-IB rejection (`1022`), and the `ignore_min_pcap` module param
  (`1023`).
- **BT.2020 YCbCr output CSC fix** (`1134`).

### Added

- **`net-tune` systemd service** — unified low-latency ethernet tuning +
  CAKE SQM shaping, replacing the separate `sqm-qos/` scripts. SQM is enabled
  by default at 80/80 Mbit; ingress shaping requires `CONFIG_NET_SCH_INGRESS`
  and a named `ifb4cake` device (fixed across `pkgrel 2–3`).
- **CachyOS fork backports** (`0110`–`0113`): `CONFIG_CACHY` config hooks
  (EEVDF base_slice, THP defrag, lru_gen_min_ttl), ACPI bus-master check
  disable for AMD C3, amdgpu S4/S5 eviction skip, and a micro-opts bundle.
- Dropped custom `r8125` module (in-kernel `r8169` covers the RTL8125B NIC).

### Changed

- Bloat removal: disabled Intel-only audio/thermal, debug hooks, NVMe
  multipath/host-auth, I2C/SPI slave, IPv6 IOAM, and F2FS; kept `autofs`.
- Enabled `uvcvideo` for UVC webcams (replaces the dead `V4L2_LOOPBACK` line).
- Dropped `1204`/`1210`/`1211`/`1212`/`1213`/`9000`/`9004`/`9005` (merged
  upstream in rc6).

## [7.2.0-rc5-1-sleepy] — 2026-08-02

Initial release of sleepy-kernel as a maintained package. Series renumbered
into coherent ranges (`0001`–`9007`), CachyOS squashed to one patch per branch
(`0101`–`0109`, with the off-target `0106` drops), and README/PATCH_SOURCES
rewritten in the Google developer style. Build verified: `linux-sleepy
7.2.rc5-1`, BTF present.

[7.2.0-rc7-1-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc7.tar.gz
[7.2.0-rc6-7-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc6.tar.gz
[7.2.0-rc5-1-sleepy]: https://git.kernel.org/torvalds/t/linux-7.2-rc5.tar.gz
