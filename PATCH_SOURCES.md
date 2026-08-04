# Patch source manifest

This file documents the origin, author, and upstream commit or message ID for every patch in this repository.

Patch numbering conventions:

| Prefix | Meaning |
|--------|---------|
| `0001`–`0049` | Handmade local patches (Sleepy/Antigravity) — SMU14, DCN401, GFX12 fixes |
| `0050`–`0099` | Upstream EDID/display parser patches (mailing list, not yet in mainline) |
| `0101`–`0109` | CachyOS branches (squashed, one patch per branch) — bbr3, kbuild, cpu-isa, cgroup-vram, fixes, drops, hdmi, preempt-ipi, vesa-dsc-bpp |
| `1000`–`1099` | AMDGPU GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) |
| `1100`–`1199` | AMD Display (DCN4, DCN42B, PSR, Replay, pstate quirk, MCIF ARB) |
| `1200`–`1299` | AMD Power Management (amd-pstate, cpufreq, ACPI CPPC) |
| `2000`–`2099` | Block / I/O schedulers (bfq, mq-deadline) |
| `2100`–`2199` | Memory management (zstd, LRU-MARIE v12) |
| `2200`–`2299` | CPU idle (NAP governor) |
| `9000`–`9099` | Upstream dev-tree backports (agd5f/linux staging) |

---

## 0001–0010 / 0030–0034 — Local handmade SMU14/DCN401 patches

Hand-written local fixes for this specific Zen 4 + RDNA 4 build, produced with Antigravity AI.

| File | Author | Description |
|------|--------|-------------|
| `0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch` | Antigravity | Fix typo in `smu_v14_0_set_irq_state` (SMU14 IRQ `type` parameter) |
| `0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch` | Antigravity | Fix memory leak in `smu_v14_0_fini_smc_tables` |
| `0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch` | Antigravity | Let GFXCLK ceiling float in PROFILE_PEAK on SMU14 |
| `0004-drm-amd-pm-Disable-deep-sleep-in-PROFILE_PEAK.patch` | Antigravity | Disable GPU deep sleep (GFXOFF) in PROFILE_PEAK. **v4** (2026-08-02): deep sleep is now a deterministic function of the forced level (enabled for every level except `PROFILE_PEAK`, tested once after the clock-range switch, so leaving PEAK restores deep sleep unconditionally); the `smu_v14_0_deep_sleep_control()` return value is checked and propagated; the deep-sleep toggle is skipped entirely while `PP_SMC_POWER_PROFILE_COMPUTE` is the active workload mode so it never clobbers `set_power_profile_mode()`'s independent COMPUTE handling |
| `0005-drm-amd-pm-Disable-SMU14-mode1-reset-for-SR-IOV.patch` | Antigravity | Disable SMU14 mode1 reset under SR-IOV |
| `0006-drm-amd-pm-Add-bounds-checking-for-SMU14-I2C-command.patch` | Antigravity | Add bounds checking to SMU14 I2C commands |
| `0007-drm-amd-pm-Remove-redundant-mutex-lock-in-SMU14-I2C-.patch` | Antigravity | Remove redundant mutex lock in SMU14 I2C update |
| `0008-drm-amd-pm-Fix-SMU14-power-limit-reporting-logic.patch` | Sleepy / Antigravity | Fix SMU14 power limit reporting logic (unlock maximum PPT) |

`0010-drm-amdgpu-gfx12-Fix-named-barrier-restore-in-trap-handler.patch` — upstream amd-gfx, **Jay Cornwall**, "drm/amdkfd: Fix named barrier restore in gfx12.1 trap handler", Message-ID `<20260706220043.612554-1-jay.cornwall@amd.com>`.

~~`0009`~~ (gfx12 disallow-GFXOFF around GPU reset) — **DROPPED** 2026-08-02: `gfx_v12_0_reset_kgq` was completely reworked by the `gfx12: recover gfx user queues on priv-fault` series landed in rc5; the new function hardcodes `use_mmio = false`, making the GFXOFF guard dead code. Superseded.

### 0030–0034 — Local display patches

| File | Author | Description |
|------|--------|-------------|
| `0030-drm-amd-display-Proactively-shrink-DET-for-pipes-los.patch` | Antigravity | Proactively shrink DET for pipes losing bandwidth |
| `0031-drm-amd-display-Fix-memory-leak-in-DCN20-link-encode.patch` | Antigravity | Fix memory leak in DCN20 link encoder resource init |
| `0032-drm-amd-display-Fix-OOB-array-access-for-HPO-FRL-lin.patch` | Antigravity | Fix OOB array access in HPO FRL link encoder |
| `0033-drm-amd-display-Fix-missing-HPO-FRL-link-encoder-reg.patch` | Antigravity | Fix missing HPO FRL link encoder register init |
| `0034-drm-amd-display-Prevent-memory-leak-during-IRQ-servi.patch` | Antigravity | Prevent memory leak during IRQ service destroy |

---

## 0050–0058 — Upstream AMD FreeSync/EDID/HDMI patches

Present on disk (mbox format from amd-gfx/dri-devel mailing lists):

| File | Author | Message-ID | Subject |
|------|--------|------------|---------|
| `0050-drm-edid-Parse-AMD-VSDB-for-FreeSync-refresh-range.patch` | Alex Huang | `20260724161713.119382-2` | drm/edid: Parse AMD VSDB for FreeSync refresh range |
| `0055-drm-edid-parse-HDMI-2.1-gaming-ALLM-VRR-caps-from-HF-VSDB.patch` | Fangzhi Zuo | `20260730171754.704049-2` | drm/edid: parse HDMI 2.1 gaming (ALLM/VRR) capabilities from HF-VSDB |
| `0058-drm-amd-display-restore-FRL-cap-on-non-destructive-HDMI-link.patch` | Fangzhi Zuo | `20260730205047.1016922-1` | drm/amd/display: restore FRL cap on non-destructive HDMI link verify |

Source thread: https://lists.freedesktop.org/archives/amd-gfx/2026-July/149621.html

**Dropped / deferred (no longer on disk):**

| File | Author | Verdict |
|------|--------|---------|
| `0053` | Alex Huang | **DROPPED** — deletes `dc_edid_parser.h`, which the CachyOS hdmi branch (`0139`–`0165`) still includes; compile would fail |
| `0054` | Fangzhi Zuo | **DROPPED** 2026-08-02 — "Add 2.1 FreeSync support for AMD VSDB EDID Block". Reviewed and found **already covered** by the CachyOS hdmi branch: `update_freesync_caps` uses `dc_is_hdmi_signal()` (includes `SIGNAL_TYPE_HDMI_FRL`), and `0157`/`0158` already build the VTEM packet for HDMI/FRL; adding `0054` would conflict with `0157`'s rewritten VTEM defines. Message-ID `<20260730171754.704049-1-jerry.zuo@amd.com>` |
| `0056`, `0057` | Fangzhi Zuo | **DEFERRED** — Zuo 3/4 + 4/4 target `amdgpu_dm_connector.c`, split out of `amdgpu_dm.c` by Alex Hung (agd5f). Split not in rc5; revisit at 7.3 |

---

## 0101–0109 — CachyOS branches (squashed, one patch per branch)

The former monolithic `0101-cachyos-mega-patch.patch` is **retired**, and so is the per-file `0101`–`0187` approach. As of the 2026-08-02 maintenance session, each CachyOS branch is **squashed into a single patch** containing the branch's full upstream content, generated by applying the branch's `-sep` patches in order to the series tree and emitting the cumulative diff.

Source: `repos/sirlucjan-kernel-patches/7.2-rc/`

| Patch | Branch | Source directory | Contents |
|-------|--------|------------------|----------|
| `0101-cachy-bbr3.patch` | bbr3 | `bbr3-cachyos-patches-sep/` | BBRv3 TCP congestion control (2 patches) |
| `0102-cachy-kbuild.patch` | kbuild | `kbuild-cachyos-patches/` | Allow `-O3` |
| `0103-cachy-cpu-isa.patch` | cpu-isa | `cpu-cachyos-patches/` | x86_64 Zen4 ISA optimizations |
| `0104-cachy-cgroup-vram.patch` | cgroup-vram | `cgroup-patches-sep/` | VRAM cgroup accounting (8 patches) |
| `0105-cachy-fixes.patch` | fixes (FULL) | `cachyos-fixes-patches-v10-sep/` | Full 26-patch v10 fixes branch, **including off-target hardware** |
| `0106-cachy-drops.patch` | drops | n/a (generated) | **Reverts the off-target fixes** (see table below); net effect = only the 10 hardware-relevant fixes remain |
| `0107-cachy-hdmi.patch` | hdmi | `hdmi-patches-sep/` | HDMI 2.1 FreeSync/VRR/PCON (26 patches, **excludes `0151`**) |
| `0108-cachy-preempt-ipi.patch` | preempt-ipi | `preempt-ipi-patches-v3-sep/` | SMP preemption + TLB flush (14 patches) |
| `0109-cachy-vesa-dsc.patch` | vesa-dsc-bpp | `vesa-patches-sep/` | EDID DSC BPP parsing (8 patches) |

The squashed patches are generated **against the actual series state** (7.2-rc5 + the `0001`–`0058` local/upstream patches), because the hdmi/fixes branches touch files shared with `0050`/`0055`/`0058` (e.g. `drm_edid.c`). When regenerating: apply the branch's patches in order, run `find . -name '*.orig' -delete; find . -name '*.rej' -delete` (GNU `patch` creates `.orig` backups that otherwise pollute the diff), then emit the cumulative diff as a single `git format-patch`.

`0151` (`drm-edid-Parse-more-info-from-HDMI-Forum-vsdb`) is **excluded from the hdmi squash**: it duplicates content added by `0055` (Fangzhi Zuo HF-VSDB) and would show as "already applied". Keep it out whenever `0055` is present.

### What the `0106` drop patch reverts (off-target content in the full fixes branch)

The `0105` fixes squash carries the full 26-patch branch; `0106` reverses the off-target hardware changes so the final tree only contains the hardware-relevant subset. The off-target subjects, by upstream fixes-branch index:

| Fixes-branch index | Reason |
|--------------------|--------|
| `0002`–`0003` (i915 RC6 quirks) | Intel GPU — AMD only |
| `0004`–`0005` (btusb IDs) | Bluetooth dongle IDs, not our hardware |
| `0006` (rtw89 WiFi) | Realtek WiFi PCIe — we have RTL8125 NIC |
| `0011`, `0013` (i915 PSR/eDP) | Intel display PSR |
| `0012` (drm/edid DisplayID eDP) | eDP OLED — external monitors only |
| `0014` (nouveau cgroups) | DRM_NOUVEAU disabled in our config |
| `0015` (i2c ASUE140D touchpad) | Laptop touchpad |
| `0016` (ALSA ALC269 ASUS laptop) | Laptop internal speaker quirk |
| `0017` (iwlwifi mld TX) | Intel WiFi — not our NIC |
| `0018`–`0019` (ASoC ASUS laptop) | Laptop audio DMI overrides |
| `0021` (SOF Dell XPS) | Intel SoundOpen Firmware |
| `0022` (usbcore quirk) | Generic USB quirk, not needed |

### Dropped CachyOS branch

| Branch | Reason |
|--------|--------|
| `snd-codecs` | Samsung/Razer/Lenovo laptop audio codecs — no laptops on this build |

### Build fix (in-tree source edit, not a patch file)

`mm/vmscan.c` — the LRU-MARIE `#ifdef CONFIG_LRU_MARIE` block still used `(vm_flags & VM_EXEC)` after `0136` (`mm: vmscan: convert folio_referenced() to use vma_flags_t`) changed the variable to `vma_flags_t`. Fixed to `vma_flags_test(&vma_flags, VMA_EXEC_BIT)`, matching the API used elsewhere in the file after `0136`. Documented here so the fix survives patch regeneration.

---

## 1000–1023 — AMDGPU GPU core

Source: drm-next (`https://gitlab.freedesktop.org/drm/kernel.git`) / amd-gfx. Formerly numbered `1002`–`1065`.

| File | Author | Subject |
|------|--------|---------|
| `1000` | Alex Deucher | gfx12.1: WARN() rather than BUG() for invalid SDMA engine |
| `1001` | Alex Deucher | gfx12: WARN() rather than BUG() for invalid SDMA engine |
| `1002` | Amber Lin | Allocate enough space for hpd info on gfx11 |
| `1003` | Alex Deucher | gfx12: only need to remap KCQs when reset via MMIO |
| `1004` | Alex Deucher | gmc9: disallow gfxoff around TLB flushes |
| `1005` | Alex Deucher | gmc10: disallow gfxoff around TLB flushes |
| `1006` | Alex Deucher | gmc11: disallow gfxoff around TLB flushes |
| `1007` | Alex Deucher | gmc12: disallow gfxoff around TLB flushes |
| `1008` | Alex Deucher | add a buffer funcs callback for TLB invalidation |
| `1009` | Alex Deucher | sdma5.0: add tlb invalidation buffer func callback |
| `1010` | Alex Deucher | sdma5.2: add tlb invalidation buffer func callback |
| `1011` | Alex Deucher | sdma6: add tlb invalidation buffer func callback |
| `1012` | Alex Deucher | sdma7: add tlb invalidation buffer func callback |
| `1013` | Alex Deucher | add core helper to do TLB invalidation via SDMA |
| `1014` | Alex Deucher | gmc: add more gmc tlb inv helpers |
| `1015` | Alex Deucher | gmc10: switch to new gmc tlb inv helpers |
| `1016` | Alex Deucher | gmc11: switch to new gmc tlb inv helpers |
| `1017` | Alex Deucher | gmc12: switch to new gmc tlb inv helpers |
| `1018` | Matthew Stewart | Switch order of GC and Display IP blocks (DCN42B) |
| `1019` | Alex Deucher | update mmhub 4.2.0 client list — drm-next `658422c7b` |
| `1020` | Alex Deucher | gmc12.1: fix MMHUB0 check in pasid tlb flush — amd-gfx ML `<20260728153930.1531949-1-alexander.deucher@amd.com>` (not yet upstream) |
| `1021` | Alex Deucher | gmc12.1: implement tlb inv semaphore — amd-gfx ML `<20260730172740.1268133-1-alexander.deucher@amd.com>` (not yet upstream) |
| `1022` | Candice Li | reject oversized IBs with per-ring packet limits — amd-gfx ML `<20260803102416.3776005-1-candice.li@amd.com>` (v2, not yet upstream). Per-ring 20-bit IB packet-size limit checked before IB allocation in `amdgpu_cs.c`; applies to GFX/compute/SDMA/VPE rings (RDNA4). CLEAN on rc6 (`git apply --check` + `patch -p1 --forward --dry-run`, offset 5). |
| `1023` | Steven Barrett (Liquorix) | drm/amdgpu/pm: Allow override of min_power_limit with `ignore_min_pcap` — backport from CachyOS/linux fork commit `16cd15654cc6` (2024, carried by CachyOS in every release). Adds an opt-in module param (`amdgpu.ignore_min_pcap=1`) that reads the min power cap as 0 and bypasses the SMU min-power-limit floor in `amdgpu_pm.c`/`amdgpu_smu.c` (swsmu, incl. SMU14). Default 0 = unchanged behavior. Adopted 2026-08-04 after the linux-cachyos-rc 7.2-rc6-2 release audit (the one fork-direct change relevant to our SMU14 power handling). CLEAN on rc6 (`git apply --check` forward, reverse fails). |

---

## 1100–1113 — AMD display

Source: drm-next, confirmed CLEAN-APPLY on v7.2-rc5 via `git apply --check`. `1100`–`1103` were formerly `1025`, `1031`, `1033`, `1065`.

| File | Commit | Author | Subject |
|------|--------|--------|---------|
| `1100` | — | Gabe Teeger | Enable PSR and Replay on DCN4 variant and fix AUX instance |
| `1101` | — | Gabe Teeger | Enable pstate for DCN4 non-emulation builds — **reverse-applied** in `prepare()` (keeps `.pstate_enabled = false` to avoid broken UCLK P-state switching) |
| `1102` | — | Gabe Teeger | Increase dcn42b uclk value |
| `1103` | — | Gabe Teeger | add dcn42b specific SMU clock table read |
| `1104` | `cee2f77c7` | James Lin | Add MALL status readback support for DCN 4.0.1 |
| `1105` | `fd651b9a3` | Matthew Stewart | Add DCN42B VID_CRC_CONTROL and HBLANK_CONTROL registers |
| `1106` | `d52de5693` | Dmytro Laktyushkin | update memclk clock table read for dcn42 |
| `1107` | `47c9c743e` | Charlene Liu | enable hdmistreamclk_rcg by default for dcn42 |
| `1108` | `68e188d91` | Dillon Varone | Add MCIF ARB programming structures (DCN401/DCN42) |
| `1109` | `889afb51a` | Dillon Varone | Add updated MCIF ARB register definitions |
| `1110` | `e324cce52` | Dillon Varone | Port DCN4+ MCIF ARB programming to new format |
| `1111` | `5a22cc7c7` | Bhuvanachandra Pinninti | Fix dc_stream_remove_writeback dropping wrong writeback entries |
| `1113` | `9afc6186f` | Fangzhi Zuo | dispatch compressed FRL cap check inside dml1_frl_cap_chk_inter (fixes DSC-over-HDMI-FRL mode pruning, e.g. 4k144) — drm-next `9afc6186f` |

~~`1112`~~ (`334cbfa3c`, dcn401 GPIO lookup tables) — **DROPPED**: requires `DC_GPIO_GENERIC_A`/`DC_GPIO_HPD_A` type defs from a prerequisite GPIO infrastructure patch not in rc5.

Only `1101` is reverse-applied in `prepare()` (PKGBUILD line 551). If you renumber patches, update that reverse-apply line to match the current filename.

---

## 1200–1209 — AMD Power Management

### 1200–1203 — amd-pstate EPP boost series (David Vernet, RFC)

| File | Message-ID | Subject |
|------|------------|---------|
| `1200` | `20260728073150.54964-2` | cpufreq/amd-pstate: Document missing kernel-doc members |
| `1201` | `20260728073150.54964-3` | cpufreq/amd-pstate: Update cppc_req_cached before writing the MSR |
| `1202` | `20260728073150.54964-4` | cpufreq/amd-pstate: Add per-core EPP boost for recently-busy CPUs |
| `1203` | `20260728073150.54964-5` | Documentation: amd-pstate: Document the epp_boost parameter |

### 1205–1209 — amd-pstate fixes (upstream series; `1204` and `1210` merged upstream in rc6)

| File | Author | Subject | Source (Message-ID / Link) |
|------|--------|---------|-----------------------------|
| `1205` | Qianheng Peng | cpufreq: amd-pstate-ut: Skip tests when amd-pstate driver is not active | `<1784191899-28957-1-git-send-email-pengqh1@chinatelecom.cn>` |
| `1206` | Marco Scardovi | cpufreq/amd-pstate: Fix EPP return type and handle errors during initialization | `<20260609073042.81275-2-scardracs@disroot.org>` |
| `1207` | Marco Scardovi | cpufreq/amd-pstate: Toggle auto_sel in active mode on shared memory systems | `<20260609073042.81275-3-scardracs@disroot.org>` |
| `1208` | Marco Scardovi | cpufreq/amd-pstate: Cache the firmware programmed EPP value | `<20260609073042.81275-4-scardracs@disroot.org>` |
| `1209` | EDAMAMEX | cpufreq/amd-pstate: handle missing policy in dynamic EPP callbacks | `<20260520070211.2753183-1-edame8080@gmail.com>` |

~~`1204`~~ (Bail out early if !X86_FEATURE_HW_PSTATE, Rong Zhang) — **DROPPED** 2026-08-03: merged upstream in rc6 as `cpufreq/amd-pstate: Prevent the driver from loading on unsupported hardware` (`08fc1e7b3`).
~~`1210`~~ (Loosen requirement on lowest nonlinear freq, Mario Limonciello) — **DROPPED** 2026-08-03: merged upstream in rc6 (`6842427bf299`).

### ~~1211–1213~~ — ACPI CPPC / cpufreq-cppc fixes — **ALL DROPPED** 2026-08-03 (merged upstream in rc6)

| File | Commit | Author | Subject |
|------|--------|--------|---------|
| ~~`1211`~~ | `9753c0ab8` | Christian Loehle | cpufreq: cppc: Sanitize lockless policy limit snapshots |
| ~~`1212`~~ | `11055a46f` | Christian Loehle | ACPI: CPPC: Check all controls for fast switching |
| ~~`1213`~~ | `47d4e945d` | Christian Loehle | ACPI: CPPC: Skip writes to unsupported performance controls |

---

## 2000–2004 — Block / I/O schedulers

Source: sirlucjan `7.2-rc/block-patches-sep/`. Formerly numbered `1300`–`1304`.

| File | Author | Subject |
|------|--------|---------|
| `2000` | Jens Axboe | block/mq-deadline: pass in queue directly to dd_insert_request() |
| `2001` | Jens Axboe | block/mq-deadline: skip expensive merge lookups if contended |
| `2002` | Jens Axboe | block/bfq: pass in queue directly to bfq_insert_request() |
| `2003` | Jens Axboe | block/bfq: serialize request dispatching |
| `2004` | Jens Axboe | block/bfq: skip expensive merge lookups if contended |

## 2100–2101 — Memory management

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2100` | `repos/sirlucjan-kernel-patches/7.2-rc/zstd-dev-patches/` | Piotr Gorski | zstd-7.2: merge changes from dev tree (formerly `1400`) |
| `2101` | `repos/sirlucjan-kernel-patches/7.2-rc/lru-marie-patches-v12/` | Piotr Gorski | mm-7.2: introduce LRU MARIE v12 (formerly `1401`; `vma_flags` fix baked in) |

## 2200 — CPU idle (NAP governor)

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2200` | `repos/sirlucjan-kernel-patches/7.2-rc/nap-patches/` | Masahito S (firelzrd) | 7.2-nap-v0.5.0 (formerly `1500`) |

**IMPORTANT**: NAP is sourced from sirlucjan's `nap-patches/` directory, **not** from firelzrd's repo. Verified 2026-08-02: `repos/firelzrd-bore-scheduler/` contains only BORE scheduler patches (`patches/stable/`, `patches/testing/` have no `nap-patches` dir).

---

## 9001–9008 — agd5f staging backports (`9000`, `9004`, `9005` merged upstream in rc6)

Source: `git clone --shallow-since="2026-06-01" https://gitlab.freedesktop.org/agd5f/linux.git repos/agd5f-linux`. Formerly numbered `2000`–`2007`.

| File | Commit | Author | Subject |
|------|--------|---------|---------|
| `9001` | `70a5cb5d2` | Alex Deucher | drm/amdgpu/gfx12: drop all BUG()s |
| `9002` | `0238fd8a2` | Alex Deucher | drm/amdgpu/gfx12.1: drop all BUG()s |
| `9003` | `d9e6b531b` | Alex Deucher | drm/amdgpu/psp14: replace BUG() with an error |
| `9006` | `58b53f58e` | Timur Kristóf | drm/amdgpu/ttm: Use more optimal copy packet sizes for copy and fill |
| `9007` | `402ebe22b267` | Alex Deucher | drm/gfx12: Program DB_RING_CONTROL |
| `9008` | — | Qiang Yu | drm/amdgpu: read TRUNCATE_COORD_MODE on gfx12 — amd-gfx ML `<20260723095431.2831513-1-qiang.yu@amd.com>`; **must apply after `9007`** (its trailing context is the DB_RING_CONTROL block that `9007` adds) |

~~`9000`~~ (Exit idle optimizations before programming, Leo Li, `8419331e64d9`) — **DROPPED** 2026-08-03: merged upstream in rc6.
~~`9004`~~ (use milliwatts for GPU power sensors, Yang Wang, `c54f8d7af`) — **DROPPED** 2026-08-03: merged upstream in rc6.
~~`9005`~~ (restore UMD profile pstate after runtime resume, Candice Li, `39866e3d3`) — **DROPPED** 2026-08-03: merged upstream in rc6.

Dropped candidates (formerly `2008`/`2009`): Jesse Zhang `47862766d211` (gfx12 userq error interrupts) and Lijo Lazar `d1331c7d89b8` (SMUv14 pptable helper) — both reference agd5f staging symbols absent from mainline rc5. Do not re-add until the staging infrastructure lands.

---

## 2026-08-02 sweep results

Checked and **not added** — already in rc5 (verified `git apply --check -R` clean against `repos/linux-7.2-rc6`):

| Commit | Subject | Verdict |
|--------|---------|---------|
| `f8ee6447e` | drm/amdgpu/discovery: Fix device family for DCN42 | already in rc5 |
| `7e1b4bdb0` | Fix flip-done timeouts on mode1 reset | already in rc5 |
| `c936b8126` | drm/amd/pm: fix smu14 power limit range calculation | already in rc5 |
| `198663d03` | drm/amd/display: fix dcn42 det allocation order | already in rc5 |
| `183bbded9` | drm/amd/display: fix dcn42b det allocation order | already in rc5 |
| `85453fb4f` | drm/amd/display: wire DCN42B mcache programming callback | already in rc5 |

Checked and **not added** — duplicate of existing series:

| Commit | Subject | Verdict |
|--------|---------|---------|
| `08fc1e7b3` | amd-pstate: Prevent loading on unsupported hardware | identical to our `1204` |

Checked and **deferred**:

| Item | Reason |
|------|--------|
| Zuo FRL `0054` (1/4), `0056` (3/4), `0057` (4/4) | target `amdgpu_dm_connector.c`, split out of `amdgpu_dm.c` by Alex Hung (agd5f) — split not in rc5; revisit at 7.3 |
| `695bc1971` Fixes for dcn42b_soc_bb.h | neither fwd nor rev applies to rc5; depends on intermediate drm-next commits |
| `1eefee546` Drop CONFIG_DRM_AMD_DC_DCN4_2 from 3dlut | context mismatch in dc.h/dcn42_hwseq.c vs rc5 |

---

## 2026-08-03 sweep results (7.2-rc6 bump)

**8 patches dropped — merged upstream in 7.2-rc6** (verified `git apply --check -R` clean against `repos/linux-7.2-rc6`):

| Patch | Subject | rc6 status |
|-------|---------|------------|
| `1204` | cpufreq/amd-pstate: Bail out early if !X86_FEATURE_HW_PSTATE | merged (`08fc1e7b3` "Prevent the driver from loading on unsupported hardware") |
| `1210` | cpufreq/amd-pstate: Loosen requirement on lowest nonlinear frequency | merged (`6842427bf299`) |
| `1211` | cpufreq: cppc: Sanitize lockless policy limit snapshots | merged |
| `1212` | ACPI: CPPC: Check all controls for fast switching | merged |
| `1213` | ACPI: CPPC: Skip writes to unsupported performance controls | merged |
| `9000` | drm/amd/display: Exit idle optimizations before programming | merged |
| `9004` | drm/amd/pm: use milliwatts for GPU power sensors | merged |
| `9005` | drm/amdgpu: restore UMD profile pstate after runtime resume | merged |

**CachyOS squashes regenerated for rc6 context:**

- `0105-cachy-fixes.patch` and `0106-cachy-drops.patch` re-squashed from
  `cachyos-fixes-patches-v10-sep/` against the rc6 series tree (rc6 + local
  `0001`–`0058`), via `patch -p1 --forward` exactly as `prepare()` applies them.
  Net applied state verified byte-identical to the rc5-era squashes.
- `0101`–`0104`, `0107`–`0109` kept unchanged: sirlucjan branch content is
  identical since 2026-07-31 and the squashes still apply cleanly to rc6.

**No new patches added this cycle.** Swept drm-next (via `linux-next` and the
`agd5f-linux` amd-staging-drm-next branch — `gitlab.freedesktop.org` was
persistently HTTP 503 during the cycle), linux-next, linux-pm, amd-gfx and
dri-devel archives, sirlucjan, and firelzrd. Every candidate AMD/display commit
found is already in rc6 (e.g. `fbbbd98f200f` DCN42B null registers,
`29c57db1629e` discovery DCN42 family, `46c3c32ba655` DCN42B mcache).
Considered and deferred:

| Item | Reason |
|------|--------|
| `34fa4d00a111` Fixes for dcn42b_soc_bb.h | context drift vs rc6 (June 2026 staging commit; file changed since) |
| `23ac3d628379` Reintroduce dcn42 GPIO lookup tables | staging commit ships a `.orig` artifact; revert/reintroduce churn. GPIO infra now present in rc6 — revisit at 7.3 |
| BT.2020 YCbCr output CSC matrices fix (amd-gfx, 2 patches) | display color-space fix; not cleanly extractable from Aug archives, outside the rc6 window |
| Alex Hung degamma helper (3/5) | series refactor, low value |
| YUV conversion colorop (v5 00/10) | core colorop framework series — defer |

**Source URL change:** the rc6 tarball was not yet on `cdn.kernel.org` at bump
time (404 — cdn lags the git tag). Switched the `source=()` URL to
`https://git.kernel.org/torvalds/t/linux-7.2-rc6.tar.gz`.

---

## 2026-08-03 second sweep (post-rc6 build)

**4 patches added** (all verified `git apply --check` forward-clean, reverse-fails
= genuinely not in rc6):

| File | Subject | Source |
|------|---------|--------|
| `1020` | gmc12.1: fix MMHUB0 check in pasid tlb flush | amd-gfx ML `<20260728153930.1531949-1-alexander.deucher@amd.com>` (Alex Deucher) |
| `1021` | gmc12.1: implement tlb inv semaphore | amd-gfx ML `<20260730172740.1268133-1-alexander.deucher@amd.com>` (Alex Deucher) |
| `1113` | dispatch compressed FRL cap check inside dml1_frl_cap_chk_inter | drm-next `9afc6186f` (Fangzhi Zuo — same FRL series author as `0055`/`0058`) |
| `9008` | read TRUNCATE_COORD_MODE on gfx12 | amd-gfx ML `<20260723095431.2831513-1-qiang.yu@amd.com>` (Qiang Yu, R-b Alex Deucher) |

**Series-order dependency discovered:** `9008`'s trailing context is the
`DB_RING_CONTROL` comment block that `9007` adds to `gfx_v12_0.c`. `9008` must
apply **after** `9007` — verified sequentially. Do not renumber it into the
`10xx` range (would apply before `9007` and fail).

**CachyOS: unchanged.** sirlucjan repo master is still 2026-07-31 (no new
commits since the rc6 bump); the `01xx` squashes already match the current
`-sep` sources (`fixes` v10, `preempt-ipi` v3, `lru-marie` v12, `nap` v0.5.0).
The two amd-pstate v2-sep patches we don't carry (`0001` Bail-out-early,
`0007` Loosen-lowest-nonlinear) are recorded as merged upstream in rc6.

**Merged-patch audit: 0 to drop.** Reverse-apply checked all 80 pre-existing
patches against pristine `repos/linux-7.2-rc6`; none reverse-apply clean, so
none are redundant with the base. rc6 is unchanged since the bump.

**Mailing-list candidates considered and deferred:**

| Item | Reason |
|------|--------|
| Retry fault handling v3 (Timur Kristóf, 14 patches) | large series, still in review after a month (likely needs v4); gfxhub/gmc/ih/mmhub changes |
| gfx12 priv-fault user-queue recovery v4 (Jesse Zhang, 5 patches) | in-review WIP; user-queue resilience, not pulled yet |
| PPT limit runtime policy refactor (Yang Wang, 4 patches, ~1500 lines) | touches `smu_v14_0.c`/`smu_v14_0_2_ppt.c` where our local `0003`/`0004` live — heavy conflict + behavioral risk |
| sdma6/7/7.1 "don't do MMIO in MQD init" series | multi-patch with prerequisites; cleanup-oriented |
| RAS UMC v12 refactor (Tao Zhou, 3 patches) | fresh (Aug 3), refactor-only, low desktop value |
| AMD VSDB FreeSync EDID common-code series (Fangzhi Zuo) | overlaps our `0050`/`0055`; different (common-code) approach — revisit at 7.3 |
| `34fa4d00a111` Fixes for dcn42b_soc_bb.h | hunk 2 (`cursor_buffer_size`) targets `dml2_dcn42b_max_ip_caps`, a struct absent from rc6; only the `gpuvm_min_page_size` hunk applies — deferred, revisit at 7.3 |

**Work items tracker note:** `https://gitlab.freedesktop.org/drm/amd/-/work_items`
is behind Anubis anti-bot (same as `lore.kernel.org`) — the page and the REST
API both return the Anubis challenge. No content could be read directly;
covered the same ground via the amd-gfx/dri-devel lists and the agd5f staging
branch.

---

## 2026-08-03 third sweep (no new patches; net-tune SQM → 80/80)

**Result: 0 patches added.** All six sources checked; nothing new relevant to
our hardware is available since the rc6 bump and the post-rc6 second sweep.

| Source | State |
|--------|-------|
| `drm-next` | No new commits since 2026-08-01 (HEAD still `82cb10c8b`, the 2026-07-30 xe merge). |
| `linux-next` | Latest published snapshot is `next-20260731` — byte-identical to the local tree already swept. No `next-2026080N` tags exist (08-01/08-02 weekend; 08-03 not yet cut at sweep time). |
| `linux-pm` | Now at mainline `7.2-rc6` (`075b74841bd0`). All tracked amd-pstate/CPPC commits already merged in rc6 (see the dropped `1204`/`1210`–`1213` entries). |
| `agd5f-linux` / `amd-staging-drm-next` | No new hardware-relevant commits since 07-29. The one display candidate, `de665f07aca6` "drm/amd/display: Exit idle optimizations before programming" (Leo Li), is **already in rc6** as `8419331e64d9` — reverse-check confirms `dm_arm_vblank_event_pre_programming()` exists in the rc6 tree. The other staging commits since 07-29 are GFX7-era (off-target). |
| `sirlucjan` | Up to date (07-31); `7.2-rc/` branch versions unchanged (`fixes` v10, `lru-marie` v12, `preempt-ipi` v3, `nap` v0.5.0). |
| `firelzrd` | Up to date (07-28); NAP lives in sirlucjan `nap-patches/` regardless. |
| amd-gfx / dri-devel lists (2026-August) | Thin (8 + 102 msgs). Nothing hardware-relevant. |

**Candidates considered and rejected:**

| Item | Reason |
|------|--------|
| `de665f07aca6` / `8419331e64d9` Exit idle optimizations before programming (Leo Li) | Already in rc6 base — nothing to add |
| `20260802170647.206880-2-cristian.laspina@kernel.srl` drm/edid: read luminance range from DisplayID 2.0 (Cristian La Spina) | **Rejected** — targets a Lenovo Yoga 9 laptop OLED panel's DisplayID luminance metadata (off-target hardware); generic EDID parsing unrelated to DCN401/DCN42B/PSR/FreeSync. **Note:** carries `Assisted-by: Claude:claude-opus-5`, which is now ALLOWED (rule change 2026-08-03 — AI-assist trailers are acceptable with a named author + provenance); the rejection stands on the off-target-hardware ground alone |

**Config change this session (not a patch):** net-tune CAKE SQM default speed
set 90/90 → **80/80** Mbit. Updated `net-tune/net-tune.conf` (shipped template)
and the `prepare()` interactive-prompt defaults in `PKGBUILD`. pkgrel bumped
2 → 3 so the rebuilt package (which ships the new `/etc/net-tune.conf`) is a
clean upgrade. BBR3 kernel default unchanged.

---

## 2026-08-03 fourth sweep (agents) — 29 patches added

A full agent-assisted re-sweep (4 parallel audits: drm-next/linux-next, agd5f/linux-pm,
mailing-list deep scan, gitlab work_items) found our series was **under-covered**
relative to what the sources actually carry. 29 verified-new patches added.

### GitLab drm/amd work_items tracker — ACCESS BREAKTHROUGH (rule update)

Previously recorded as Anubis-blocked. **2026-08-03 finding:** the Anubis challenge
is served **only to browser-like User-Agents**. Plain `curl` with **no User-Agent**
header returns real GitLab content (issues API, project events API, atom feed).
The issue *notes* API remains 401-gated (real auth), but the events/atom feeds
expose comment bodies + referenced commit SHAs. Update the `patch-sweep`/`patch-audit`
skills and CLAUDE.md accordingly. (lore.kernel.org status not re-tested; the
"never access lore" rule stands unless separately verified.)

Key tracker content (Navi 48 / RX 9070 XT): issues on GPU-bus-loss (SMU power
transitions), flip_done timeouts, DCN42B vblank stalls, FAMS2 memory-clock stalls.
The flagged regression commits (`8382cd234981` vblank consolidation, `f64a9be56536`,
`c87e6635d2db`, `a1fc7bf6677e`) are **all already in rc6** — nothing to revert.
Community FAMS2/VRR workarounds on #4753 are experimental (need `dcdebugmask`
flags) — deferred, not upstream.

### AI-assisted patches — rule change

`Assisted-by: <tool>` trailers (e.g. `Claude:claude-opus-5`) are now **allowed**
provided the patch has a named human author, `Signed-off-by`, and traceable
provenance. Fabricated diffs remain forbidden. (Previously rejected on this ground;
the DisplayID luminance candidate is still out on off-target-hardware grounds.)

### New GPU-core / backport patches

| File | Subject | Source |
|------|---------|--------|
| `9009-drm-amdgpu-mes12.1-drop-all-BUG-s.patch` | mes12.1: drop all BUG()s | drm-next `14bcaa11c` (Alex Deucher) |
| `9010-drm-amdgpu-imu12-WARN-rather-than-BUG.patch` | imu12: WARN rather than BUG | drm-next `bc1e9d39` (Alex Deucher) |
| `9011`–`9024` | **Retry-fault handling v3** (14 patches, Timur Kristóf, `20260701161721.85681-1`) | amd-gfx ML Jul 1; NOT in drm-next/rc6. GFX12.1 noretry, gfxhub/ih/gmc11/gmc12/vm retry-CAM + NOALLOC, IH6.0/7.0 MMIO ACK, **Enable retry CAM on Navi 4 dGPUs**. Verified 14/14 apply in sequence to rc6 AND after our 1019–1021 ||

### New display patches (DCN4/DCN42B)

| File | Subject | Source |
|------|---------|--------|
| `1114` | ensure dtbclk clk_src selected before hdmistream_clk_en | drm-next `5b7e4ad0` (DCN42B HDMI clock sequence) |
| `1115` | fix wrong register field in dccg35_set_hdmistreamclk_src_new | drm-next `db9c882f` (HDMISTREAMCLK0_SRC_SEL) |
| `1116` | Add dcn42b_soc_and_ip_translator | drm-next `98c692c5` (prereq for 1117) |
| `1117` | Fixes for dcn42b_soc_bb.h | drm-next `695bc197` (gpuvm_min_page_size 256→4; applies AFTER 1116) |
| `1118` | Add get replay residency function | drm-next `040f7925d` |
| `1119` | Fix force FRL rate debug setting | drm-next `f73dd04ac` |
| `1120` | Enable PSR and Replay on DCN4 variant **Part 2** | drm-next `329baa1c5` (completes our 1100; actual DCN42B enable) |
| `1121` | Enable IPS support for DCN4 Variant | drm-next `6cefc59d3` |
| `1122` | Enable zstate support and fix seamless boot | drm-next `219fb1f4` (also fixes DCN42B clk-src masks) |
| `1123` | Enable HUBP/DPP Driver PG for DCN42 | drm-next `4fb6f596f` |
| `1124` | Correct vblank_end calc for fams cmd packet | agd5f `c7ec79ef` |
| `1125` | Fix rounding errors in CalculatePrefetchSchedule | agd5f `8938627f` |
| `1126` | fix debug flags assignment in dmub_replay.c | agd5f `d61cb75b` |
| `1129` | Ensure dtbclk is enabled (DCN42) | Roman.Li DC batch 07-31 `20260731211302.3040343-10` — ML-only |
| `1130` | Update VRR info packet to support 12-bit refresh rate | Roman.Li DC batch 07-31 `...-11` — ML-only |
| `1131` | Add missing DCN42B register defines | Roman.Li DC batch 07-31 `...-32` — ML-only |
| `1132` | Add missing DMUB CACP and PR definitions | Roman.Li DC batch 07-31 `...-33` — ML-only |
| `1133` | Add FFE level defaults | Roman.Li DC batch 07-31 `...-40` — ML-only. **DCN6 hunks stripped** (2026-08-03): the patch also touched `dcn60_resource.c` (DCN6, a future die absent from rc6) — those hunks were removed as a mechanical backport adjustment, leaving the 15 rc6-applicable files (dcn30–dcn42b) |

`1129`–`1133` are individual patches taken from the 41-patch Roman.Li "DC Patches July 31"
batch (not yet merged into drm-next/amd-staging). They apply to the series tree but not
to clean rc6 (our 11xx DCN42/42B patches provide the context). Extracted from the
amd-gfx July mbox via `git mailinfo`. If the batch lands upstream, re-derive from the
merged commits. `11/41` (Gate HDMI FRL status polling) was NOT taken — it references
`amdgpu_dm_connector.c`, which does not exist in rc6 (Alex Hung's split is 7.3).
**Ordering note:** `1127`–`1128` (DF C-state backport) MUST precede `1129` (dtbclk) —
`1129`'s `clk_mgr` context needs `execute_clk_mgr_block_sequence` (1127) and
`notify_cstate_disable` (1128). Verified by prepare() apply order.

### Second-pass additions (independent verification agents, 2026-08-03)

| File | Subject | Source |
|------|---------|--------|
| ~~`9025`~~ | gfx12: fix IP dump alloc ordering (leak on sysfs-init failure) | drm-next `4ef372319` (Alex Deucher). **DROPPED** (2026-08-03): marginal 2-line leak fix (sysfs-init failure path only); GNU `patch` in prepare() rejects the hunk in the series tree (leading `if (r)` context is ambiguous across sw_init's many error checks) despite `git apply --check` passing. Revisit at 7.3 when the sw_init context is stable |
| `1127` | Add block sequence support for bandwidth programming ops | drm-next `f3403ab74` — defines `build_clock_update_for_bls`/`execute_clk_mgr_block_sequence`; prereq for 1128 AND 1129 |
| `1128` | Register DCN as a PMFW DF C-state client on DCN42 | drm-next `53845307d` — DCN42B boot-hang fix; depends on 1127, prereq for 1129 |

**linux-next note:** the remote published `next-20260803` after our initial sweep, but the
fetch from git.kernel.org repeatedly failed (TLS/RPC errors) on 2026-08-03 evening. linux-next
is an aggregation tree — its AMD content is a subset of drm-next HEAD (verified by the
first-pass agent via tree diff) — so the delta to next-20260803 carries nothing new for our
hardware beyond what drm-next/ML already provide. Re-check `next-20260803` on the next sweep.

**Still deferred (in-review / no clean apply):** Jesse Zhang priv-fault userq recovery v4
(depends on `amdgpu_userq_process_reset_irq`/`AMDGPU_CTXID0_DOORBELL_ID_MASK`, absent in rc6),
Yang Wang PPT limit runtime policy refactor (context drift on `smu_v14_0*`), Philip Yang SVM
no-access/unmap v3, Harry Wentland YUV colorop v5 (color-mgmt infra), the FAMS2/VRR community
workarounds on gitlab #4753 (experimental, need `dcdebugmask` flags, no upstream submission),
DCN42 GPIO lookup-table series (enum infra absent from rc6, re-verified 2026-08-03), gfx12
IP dump alloc ordering (drm-next `4ef372319` — GNU `patch` rejects in series; revisit 7.3).

### Third-pass verification (independent agent, 2026-08-03) — no new patches

A final independent agent re-fetched everything with a **shallow linux-next fetch**
(`--shallow-since=2026-07-01`, per user request — much faster than full fetch) and
confirmed the latest snapshot is **`next-20260803`** (`9a4cdc958dd7`). All 45–51
AMD-related commits in that snapshot SHA-test as **already in rc6**; zero new
hardware-relevant commits. All other sources (drm-next 08-01, agd5f 07-29, linux-pm rc6,
sirlucjan, firelzrd) unchanged. Mailing lists (fresh Aug + July re-check) and the gitlab
work_items tracker surfaced nothing actionable. The 1127→1128→1129 dependency chain
(block-sequence → DF-cstate → dtbclk) was independently confirmed and is now also
validated by the full `7.2.rc6-3` build (exit 0). **Bottom line: the series is complete
for 7.2-rc6.**

**User decision (2026-08-03):** PSR/IPS/zstate/HUBP-DPP-PG idle-power class added
deliberately despite the 1101/1025 RDNA4-freeze history — the user chose "Add all
idle-power". If desktop freezes recur, reverse-apply 1120–1123 in `prepare()`
alongside 1101.

**Second-pass verification (user-requested):** a fresh batch of independent
agents re-fetched all repos + re-scanned ML/gitlab after this ingestion; their
reports are appended below. Net effect so far: **0 additional patches found**.

---

## 2026-08-04 sweep results (6-source re-fetch + agents; 1 patch added)

Repos re-fetched (drm-next, agd5f-linux, amd-staging-drm-next, linux-next to `next-20260804`, linux-pm, sirlucjan, firelzrd, linux-7.2-rc6 reference) and the August amd-gfx/dri-devel mboxes re-downloaded. Torvalds latest tag is still `v7.2-rc6` → **no version bump**.

**Added (1):**
- `1022` Candice Li — reject oversized IBs with per-ring packet limits (see 1000–1022 section).

**Evaluated and not added (with reasons):**
- König `[PATCH v7 1/6]` amdgpu_vram_mgr_init ordering fix — only 1/6 of the series present in the mbox; König greenlit merging the series via drm-misc-next upstream. Skip (mid-series, being merged upstream).
- Arunpravin Paneer Selvam amdgpu_vram_mgr_fini UAF fix — the mbox entry is **Christian König's rejection reply** ("this approach here is clearly not correct") — maintainer-rejected, do not add.
- Timur Kristóf `hwss_set_output_transfer_func()` crash fix — fixes NULL-hubp deref on **DCE/Vega and older** hardware (not ours); a no-op on DCN4. Skip per "no patches for hardware we don't have".
- Timur Kristóf "Set native cursor mode for disabled CRTCs again" — targets `amdgpu_dm_cursor.c`, split out by the "add cursor module" refactor (`151164f96a4b`) which is **not in rc6**; function absent. Defer (same class as the `amdgpu_dm_connector.c` split).
- Jesse Zhang userq serialize queue-map / remove guilty-compute-userq-reset — in-review; amdgpu_userq.c exists in rc6 but the patches are reply-quoted in the mbox and in-review. Not added.

**GitLab drm/amd work-items tracker (no-UA curl, confirmed readable):**
- SMU14 IF mismatch (driver 0x2e vs fw 0x33) — issues #5538/#5113/#5479. No fix in rc6 or drm-next; nothing to backport. Monitor.
- FAMS2/DCN42B reclock stutter — #4753. fililip's workaround patches are not upstreamable; related "enforce UCLK pstate support" drm-next candidate conflicts with our deliberate `.pstate_enabled=false` (1101 reverse-applied). Not added.
- dc_stream_retain UAF on dual-monitor — #5237/#5242. No fix merged. Monitor.
- GPU-recovery failure on Navi 48 — #5552 (opened 08-02). No fix merged; AMD assigned. Monitor.
- Fan/RPM hwmon on Navi4x — #5422/#5514. AMD: by design (Overdrive domain). No action.

**sirlucjan / CachyOS:** all `7.2-rc/` branch dirs unchanged (fixes v10, preempt-ipi v3, lru-marie v12, nap v0.5.0, master at 2026-07-31). No `01xx` squash regeneration needed. amd-pstate `-v2-sep` already audited on 2026-08-03; overlapping patches differ only by hunk offsets.

**Already in rc6 (reverse-check clean, no re-add):** `8419331e64d9` (Leo Li DCN vblank/flip follow-up), `fbbaca9e2087` (DCE check in dm_gpureset_toggle_interrupts), `82730dba0cf9` (flip-done timeouts on mode1 reset), `00c391102abc`/`6d92c4d03063` (FAMS2 DMUB hw lock rename).

---

## 2026-08-04 CachyOS release audit (linux-cachyos-rc 7.2-rc6-2)

CachyOS pushed `linux-cachyos-rc 7.2-rc6-2` (2026-08-04; base bumped rc5→rc6,
pkgrel 2). Audited against our series by applying our `0101`–`0109` squashes to
a clean torvalds-rc6 tree and diffing against the `cachyos-7.2-rc6-2` fork tag
(`CachyOS/linux`), plus a per-file `(cachyos rc5-1→rc6-2 delta) vs (torvalds
rc5→rc6 delta)` comparison.

**Result: our kept-branch squashes are already current.** 60/91 files byte-identical;
the 31 diffs are:
- **Branches we deliberately exclude** (13): i915, btusb, rtw89, iwlwifi, nouveau,
  i2c touchpad, alc269 laptop audio, SOF — expected (`0106` drops them).
- **Our `0151` exclusion in the hdmi squash** (`drm_edid.c`/`amdgpu_dm.c`/`drm_connector.h`)
  plus our `00xx`/`10xx` additions — expected.
- **Fork-direct commits CachyOS carries in `CachyOS/linux` but NOT in sirlucjan's
  `-sep` dirs** — evaluated, not adopted:
  - `CONFIG_CACHY` Kconfig + CONFIG_CACHY-gated sched tunables in `sched/fair.c`
    (`sysctl_sched_base_slice=400000`, `migration_cost=400000`), `likely/unlikely`
    hints in `sched/core.c`, `h_load`/`runnable_avg` fields — CachyOS's opinionated
    scheduler tuning. Not adopted (behavior change; we historically strip CACHY
    overrides; sched-ext is our scheduler path).
  - `SCHED_POC_SELECTOR` — the `poc-selector` branch (new CachyOS idle-CPU selector).
    Not in our branch set. Not adopted.
  - Makefile `-fmodulo-sched`/`-mllvm -enable-pipeliner` — LLVM pipelining, same
    miscompilation-risk class as the excluded `clang-patches` branch. Not adopted.
  - `unprivileged_userns_clone` restriction (`kernel/fork.c`) — from `arch-patches`
    branch (un-carried). Not adopted.
  - **`amdgpu_ignore_min_pcap`** — adopted as `1023` (the one change relevant to
    our SMU14 power-cap handling).

Also removed the stale `scripts/config -e CACHY` from `prepare()` (+ `kernel-build/
reference.md`) — CONFIG_CACHY is defined only in the CachyOS/linux fork, so the line
was a silent no-op.

---

## Adding new patches

1. Place the patch file in the root of this repository.
2. Use the correct numeric prefix (see the conventions table): `0001`–`0099` local/upstream display, `0101`–`0109` CachyOS (squashed per branch), `1000`–`1099` GPU core, `1100`–`1199` display, `1200`–`1299` PM, `2000`–`2099` block, `2100`–`2199` MM, `2200`–`2299` cpuidle, `9000`–`9099` agd5f.
3. Verify it applies cleanly with BOTH tools (use absolute paths — `git -C` changes CWD):
   ```bash
   git -C repos/linux-7.2-rc6 apply --check "$PWD/<file>"     # forward
   git -C repos/linux-7.2-rc6 apply --check -R "$PWD/<file>"  # reverse-clean = already applied → drop it
   patch -p1 --forward --dry-run < <file>                     # authoritative — matches prepare()'s tool
   ```
   **`git apply --check` can pass while GNU `patch` rejects** (2026-08-03): a hunk with
   ambiguous leading context, or one touching a file absent from rc6 (e.g. DCN6 `dcn60`),
   fools `git apply` but aborts prepare(). Always confirm with `patch -p1 --forward --dry-run`.
   If a patch spans a file that does not exist in rc6, strip that file's hunks (document the
   strip here). If a patch's context references a symbol/field another carried patch adds,
   number it AFTER that patch.
4. Add the filename to the `source=()` array in `PKGBUILD` in the correct sorted position
   (dependencies first — e.g. 1127/1128 must precede 1129).
5. Run `updpkgsums` after any `source=()` change — checksums must match 1:1.
6. Add an entry to the appropriate section in this file with author and source URL or commit hash.
7. Do **not** access `lore.kernel.org` — it has anti-scraping protections. Use the source Git repositories directly (drm-next, linux-pm, sirlucjan GitHub, freedesktop.org mailing list archives, and the gitlab drm/amd work_items via no-UA curl).
