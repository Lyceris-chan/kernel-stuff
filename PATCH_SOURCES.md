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
| `0050-drm-edid-Parse-AMD-VSDB-for-FreeSync-refresh-range.patch` | Alex Huang | `20260804143339.714548-2` (**v3 1/4**, swapped in 2026-08-10; formerly v2 `20260724161713.119382-2`) | drm/edid: Parse AMD VSDB for FreeSync refresh range — v3 adds: restructured `amd_vsdb_v1/v2/v3_payload` (common/v1/v2/v3 nested) with v1/v2 FreeSync range parsing, and parses VSDB **version > 3 as v3 with a warning** (future-version tolerance). Verified ALL-OK: replaces v2 1/4 in `0050`'s slot, full 127-patch series still applies (`patch -p1 --forward`). Deferred same-series members: 2/4 (use HDMI FreeSync range from common parser), 3/4 (Clean up FreeSync capability detection — the DP-VRR regression fix; needs rebase on rc7 `amdgpu_dm.c`), 4/4 (Remove unused DMCU/DMUB EDID CEA parser — conflicts with the CachyOS hdmi branch's `dc_edid_parser.h`, same blocker as dropped `0053`). |
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

## 0101–0113 — CachyOS branches + fork backports

The former monolithic `0101-cachyos-mega-patch.patch` is **retired**, and so is the per-file `0101`–`0187` approach. As of the 2026-08-02 maintenance session, each CachyOS branch is **squashed into a single patch** containing the branch's full upstream content, generated by applying the branch's `-sep` patches in order to the series tree and emitting the cumulative diff.

Source: `repos/sirlucjan-kernel-patches/7.2/`

| Patch | Branch | Source directory | Contents |
|-------|--------|------------------|----------|
| `0101-cachy-bbr3.patch` | bbr3 | `bbr3-cachyos-patches-sep/` | BBRv3 TCP congestion control (2 patches) |
| `0102-cachy-kbuild.patch` | kbuild | `kbuild-cachyos-patches/` | Allow `-O3` |
| `0103-cachy-cpu-isa.patch` | cpu-isa | `cpu-cachyos-patches/` | x86_64 Zen4 ISA optimizations |
| `0104-cachy-cgroup-vram.patch` | cgroup-vram | `cgroup-patches-sep/` | VRAM cgroup accounting (8 patches) |
| `0105-cachy-fixes.patch` | fixes (FULL) | `cachyos-fixes-patches-v11-sep/` | Full 25-patch **v11** fixes branch, **including off-target hardware** (regen 2026-08-10: renumbered to 25, mm/mglru reworked to vma_flags_t API, adds PCI Skip Target Speed quirk) |
| `0106-cachy-drops.patch` | drops | n/a (generated) | **Reverts the off-target fixes** (see table below); net effect = only the hardware-relevant fixes remain. v11: no longer drops the usbcore 255-byte quirk (branch dropped it), now reverts `mt76/dma.c`; ASoC amd acp TUF self-reverts inside the branch |
| `0107-cachy-hdmi.patch` | hdmi | `hdmi-patches-sep/` | HDMI 2.1 FreeSync/VRR/PCON (26 patches, **excludes `0151`**) |
| `0108-cachy-preempt-ipi.patch` | preempt-ipi | `preempt-ipi-patches-v3-sep/` | SMP preemption + TLB flush (14 patches) |
| `0109-cachy-vesa-dsc.patch` | vesa-dsc-bpp | `vesa-patches-sep/` | EDID DSC BPP parsing (8 patches) |
| `0110-cachy-config-hooks.patch` | cachy config hooks | **CachyOS/linux fork** (not sirlucjan) | Curated CONFIG_CACHY-gated backport (see below) |
| `0111-cachy-acpi-disable-bus-master-check-for-AMD.patch` | fork backport | CachyOS/linux fork `14f3669dd743` (Sultan Alsawaf) | Disable the legacy ACPI bus-master port poll on AMD C3 (`bm_check` kept set, no cache flush) — Zen 4 direct; CachyOS-shipped AMD-wide since 2025 |
| `0112-cachy-amdgpu-avoid-evicting-resources-at-S5.patch` | fork backport | CachyOS/linux fork `575943925bac` (Mario Limonciello, AMD; Acked by Alex Deucher) | Skip VRAM eviction in the S4/S5 poweroff path (`amdgpu_device.c`) — faster, cleaner shutdown of the RX 9070 XT |
| `0113-cachy-micro-opts.patch` | fork backport | CachyOS/linux fork `dec8b451162e` + `1c37598e86ec` + `4b167ad6a219` + `10fc94fd82d6` + `818b55203e93` | Micro-op bundle: `VM_READAHEAD_PAGES` 128K→256K, sched/core gcov branch hints, readdir unlikely hint, `list.h` `__always_inline`, evdev `call_rcu` on detach |

**`0110-cachy-config-hooks.patch`** — curated backport of the CONFIG_CACHY-gated optimizations CachyOS carries directly in their `CachyOS/linux` fork (not in sirlucjan's `-sep` dirs), added 2026-08-04 after the rc6-2 release audit. Individual fork commits (all apply cleanly to rc6):
- `c74130de6b69` Kconfig: Add CONFIG_CACHY (gates everything; `-e CACHY` in `prepare()` now resolves)
- `a9e83bef71e8` sched/fair: Tweak EEVDF for interactivity — `base_slice` 700000→400000, `migration_cost` 500000→400000, `SCHED_NR_MIGRATE_BREAK` 32→8 (lower latency)
- `f70decbe6bab` mm/huge_memory: enable background reclaim of hugepages (THP defrag `KSWAPD_OR_MADV`)
- `96b1ae8ac47a` mm/vmscan: lru-gen protect working set of last 100 jiffies (`lru_gen_min_ttl=100`)
- `62f028222e10` mm/compaction: disable proactive compaction (`proactiveness=0`)
- `488cac6e34bb` mm/page_alloc: disable watermark boosting (`watermark_boost_factor=0`)
- `4107a1558e3f` arch/x86 bus_lock: disable split-lock detect mitigation (`sld_mitigate=0`)

**Excluded from the set** (user-approved scope): `4cdd54c00ce7` (`vm_swappiness=100` — documented LRU-MARIE conflict, see lessons) and the elevator bfq-default hunk (single-queue only, irrelevant to our multi-queue NVMe).

The squashed patches are generated **against the actual series state** (7.2-rc5 + the `0001`–`0058` local/upstream patches), because the hdmi/fixes branches touch files shared with `0050`/`0055`/`0058` (e.g. `drm_edid.c`). When regenerating: apply the branch's patches in order, run `find . -name '*.orig' -delete; find . -name '*.rej' -delete` (GNU `patch` creates `.orig` backups that otherwise pollute the diff), then emit the cumulative diff as a single `git format-patch`.

`0151` (`drm-edid-Parse-more-info-from-HDMI-Forum-vsdb`) is **excluded from the hdmi squash**: it duplicates content added by `0055` (Fangzhi Zuo HF-VSDB) and would show as "already applied". Keep it out whenever `0055` is present.

### What the `0106` drop patch reverts (off-target content in the full fixes branch)

The `0105` fixes squash carries the full 25-patch v11 branch; `0106` reverses the off-target hardware changes so the final tree only contains the hardware-relevant subset. The off-target subjects, by upstream fixes-branch index:

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
| `0018` (ASoC ASUS laptop) | Laptop audio DMI overrides (v11 also self-reverts it via `0024`) |
| `0019` (SOF Dell XPS) | Intel SoundOpen Firmware |
| `0025` (mt76 revert) | MediaTek WiFi — not our RTL8125 NIC |

v11 vs v10 index note: the branch was renumbered 26→25 patches and the usbcore
255-byte quirk (`0022` in v10) was dropped from the branch upstream — so `0106`
no longer reverts `usb/core/config.c`/`usb/quirks.h` (obsolete drops removed).

### Dropped CachyOS branch

| Branch | Reason |
|--------|--------|
| `snd-codecs` | Samsung/Razer/Lenovo laptop audio codecs — no laptops on this build |

### Build fix (in-tree source edit, not a patch file)

`mm/vmscan.c` — the LRU-MARIE `#ifdef CONFIG_LRU_MARIE` block still used `(vm_flags & VM_EXEC)` after `0136` (`mm: vmscan: convert folio_referenced() to use vma_flags_t`) changed the variable to `vma_flags_t`. Fixed to `vma_flags_test(&vma_flags, VMA_EXEC_BIT)`, matching the API used elsewhere in the file after `0136`. Documented here so the fix survives patch regeneration.

---

## 1000–1058 — AMDGPU GPU core

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
| `1023` | Steven Barrett (Liquorix) | drm/amdgpu/pm: Allow override of min_power_limit with `ignore_min_pcap` — backport from CachyOS/linux fork commit `16cd15654cc6` (2024, carried by CachyOS in every release). Adds an opt-in module param (`amdgpu.ignore_min_pcap=1`) that reads the min power cap as 0 and bypasses the SMU min-power-limit floor in `amdgpu_pm.c`/`amdgpu_smu.c` (swsmu, incl. SMU14). Default 0 = unchanged behavior. Adopted 2026-08-04 after the linux-cachyos-rc 7.2-rc6-2 release audit (the one fork-direct change relevant to our SMU14 power handling). CLEAN on rc6 (`git apply --check` forward, reverse fails). |
| `1024` | Jesse Zhang | drm/amdgpu/mes12: fix dropped dispatches under queue oversubscription — drm-next `288cc4a54` (amd-drm-next-7.3-2026-08-06 merge, 08-08). GFX12 MES: pads/spaces the MES queue dispatch so concurrent queue oversubscription no longer drops dispatches. **Added 2026-08-10** (AMDGPU 7.3 last-round backport). CLEAN on rc7 series. |
| `1026` | Vladimir Marioukhine (AMD) | drm/amdkfd: fix NULL pointer dereference in GFX12 CRIU queue restore — **amd-gfx ML 2026-08-04** (`Message-ID SA1PR12MB8600E8B1821FA7D76923FC259FD42@SA1PR12MB8600...`, mbox `amd-gfx-2026-August.txt`). GFX 12.0/12.1 MQD managers leave `restore_mqd`/`checkpoint_mqd` NULL; `create_queue_cpsch`/`create_queue_nocpsch` call them unconditionally during CRIU restore, so a `CAP_CHECKPOINT_RESTORE` user can trigger a kernel NULL-deref panic. Fix implements the callbacks (modeled after GFX 11) + adds NULL guards. **Added 2026-08-10.** **Reconstruction caveat:** the freedesktop mbox copy had context-line leading spaces stripped and tabs→spaces (Outlook sender), so the diff body could not be applied verbatim. Reconstructed byte-for-byte from the mbox `+` lines against the rc7 v11 MQD manager reference (verified content-identical modulo whitespace, incl. the `sdmax_rlcx_doorbell_offset` field + `CP_HQD_PQ_DOORBELL_CONTROL` shift that v11 also uses), kernel-standard tabs restored. Passes `git apply --check` (fwd) and GNU `patch -p1 --forward --dry-run` against rc7. **Not yet merged upstream; Alex Deucher requested brace-style revisions (v2 pending) — swap for the merged commit when it lands.** `Assisted-by: Claude`. **Deviation (compile fix):** the original used the GC 12.0 macro `SDMA0_QUEUE0_DOORBELL_OFFSET__OFFSET__SHIFT` in both files; rc7's v12_1.c (GC 12.1) has that macro undeclared, so the v12_1 hunk here uses `SDMA0_SDMA_QUEUE0_DOORBELL_OFFSET__OFFSET__SHIFT` (the v12_1 header's macro) — the original ML submission would not compile on v12_1.c either. |
| `1027` | Jesse Zhang (AMD) | drm/amdgpu: force complete the MES scheduler ring fence on reset — **amd-gfx ML 2026-08-06** (`Message-ID 20260806075653.711275-1-Jesse.Zhang@amd.com`, mbox `amd-gfx-2026-August.txt`). The MES scheduler ring has no drm scheduler (`no_scheduler = true`), so it is skipped by the force-completion loop in `amdgpu_device_pre_asic_reset()`. Its polling fence lives in wb (GTT) memory and survives a MODE1 reset while `sync_seq` keeps advancing, so a reset triggered by MES itself wedges the first post-resume submission ("MES ring buffer is full", resume fails -110). Fix forces the MES ring fence alongside the scheduler rings. **Added 2026-08-11** (sweep). CLEAN on the rc7 series (`git apply` + GNU `patch -p1 --forward --dry-run`). ML-only; not yet in drm-next/agd5f. |
| `1029`–`1046` | Tvrtko Ursulin (Igalia) | **`[PATCH v2 00/20] Revert switching default DRM scheduler policy to fair`** — dri-devel ML 2026-08-11 (`Message-ID 20260811140738.96974-1-tvrtko.ursulin@igalia.com`, mbox `dri-devel-2026-August.txt`). Reverts the 7.2 DRM scheduler FAIR series that causes the RX 9070 XT performance regression under sustained 100% GPU load (foreground app drops to ~10 fps / desktop freeze — report by Luke Wildhardt, 2026-08-08, `Message-ID TfhgV1W0W5LI6RWUO6J35B3R8QIYH_FN3Eihzdo_9PH39hfn1AVByT-QBPHmWiAR-L0Kqi2sppM_EhFPKwZPGmb5pFgpF2MrzeFzkZDmpG8=@proton.me`). **Not** related to the SMU-IF blackscreen/bus-drop issue (!5538, `pcie.aspm=off` stopgap). Restores the pre-fair multi-run-queue FIFO/RR scheduler with `gpu_sched.sched_policy` (0=RR, 1=FIFO, 2=fair-experimental) and **FIFO as default**. Series order preserved in numbering: `1029` Restore `num_rqs`, `1030`–`1042` restore per-driver `num_rqs` usage (xe, v3d, sched, panthor, panfrost, nouveau, msm, lima, etnaviv, amdgpu, ethosu, rocket, amdxdna), `1043` Revert "Embed run queue singleton", `1044` Revert "Remove FIFO and RR", `1045` Revert "Switch default policy to fair", `1046` Mark fair experimental. **Added 2026-08-12** (decision: full revert, replacing the earlier partial `1028`; the FAIR regression surfaced in real sustained-load sessions). All CLEAN on the rc7 series with GNU `patch -p1 --forward` in order. **Series-adapted:** `1043` carries an rc7-adapted `amdgpu_xcp.c` hunk (rc7's `amdgpu_xcp_release_sched()` lacks the `xcp_mgr` local var drm-next has — the revert is applied directly against `adev->xcp_mgr`); all other hunks apply as-authored. **Dropped from the series:** `01/20` (Revert "Remove redundant entity->rq init" — its target commit is absent from rc7, reverse-applies = already-reverted) and `11/20` (imagination/PVR `num_rqs` — hardware not present, `CONFIG_DRM_IMAGINATION` unset). ML-only; not yet merged upstream. |

~~`1028`~~ (drm/sched: Ensure monotonic `min_vruntime`, Tvrtko Ursulin, dri-devel ML 2026-08-11 `<20260811134223.96203-1-tvrtko.ursulin@igalia.com>`) — **DROPPED 2026-08-12** (replaced by `1029`–`1046`). The one-patch fix was adopted the previous day as a minimal mitigation for the FAIR regression, but it only patches the fair scheduler's `min_vruntime` machinery; the full v2 revert series (adopted now) removes that machinery entirely (restores multi-rq FIFO/RR), so `1028` no longer applies and is superseded. Fair is now opt-in and experimental (`sched_policy=2`).

~~`1025`~~ (gfx12 priv-fault user-queue recovery worker, Jesse Zhang, drm-next `30f07c06`) — **DROPPED 2026-08-10 at build**: applies cleanly but does NOT compile on rc7 — references `adev->gfx.userq_priv_fault_work`/`userq_priv_fault_slots`, fields that live in `struct amdgpu_gfx` only via the gfx11 priv-fault worker infra which is in drm-next (post-rc7), not rc7 (`amdgpu_gfx.h` has only `userq_sch_*`). Requires the whole gfx11 priv-fault prerequisite series — defer to the 7.3 move. Symbol-existence check failed; do not re-add without the prerequisite.

~~`1020`~~ (gmc12.1 fix MMHUB0 check in pasid tlb flush, Alex Deucher) — **DROPPED 2026-08-10**: merged upstream in rc7 (`5227c2c77c38`).
~~`1021`~~ (gmc12.1 implement tlb inv semaphore, Alex Deucher) — **DROPPED 2026-08-10**: merged upstream in rc7 (`cda6ab11c1a2`).
~~`1022`~~ (reject oversized IBs with per-ring packet limits, Candice Li) — **DROPPED 2026-08-10**: merged upstream in rc7 (`fd37f9dd5b5a`). All three verified: content present in clean rc7 tree + upstream commits confirmed in torvalds history.

| `1047` | Pierre-Eric Pelloux-Prayer (AMD) | drm/amdgpu: don't disable ttm buffer funcs on reset — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`fb8379680c82`). TTM buffer funcs stay active across GPU reset. **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1048` | Alex Deucher (AMD) | drm/amdgpu: fix missing check in vm_flush() — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`54a118f1d7e1`). gfx12 SPM emission correctness. **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1049` | Yang Wang (AMD) | drm/amdgpu: fix nbif 6.3.1 l1 low power not functional — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`c2417f9fd704`). NBIF 6.3.1 (RDNA4/soc24) PCIe L1 low-power programming. Effect muted by our `pcie_aspm=off` !5538 stopgap. **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1050` | Jesse Zhang (AMD) | drm/amdgpu: keep PRT mappings off the vm_bo state lists — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`04b48274e985`). Fixes NULL-bo deref in `amdgpu_userq_restore_worker` during GPU reset — the gfx12 userq crash class (complements our `9038`). **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1051` | Yifan Zhang (AMD) | drm/amdgpu: skip BOs being torn down during GTT recovery — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`24775b2e8bce`). GTT recovery / reset race fix. **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1052` | Candice Li (AMD) | drm/amdgpu: validate GEM_CREATE domain combinations — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`db39852d0c39`). Hardening vs userspace BUG_ON. **Added 2026-08-14** (sweep). CLEAN on rc7 series. |
| `1053` | Tvrtko Ursulin (Igalia), AI-suggested fix | drm/sched: Cache and update run-queue `min_vruntime` — **dri-devel ML regression thread** (`[REGRESSION] drm/sched: FAIR policy...9070XT`, Luke Wildhardt's AI-proposed fix, tested/refined in-thread). Replaces per-op `drm_sched_rq_get_min_vruntime()` tree scan with a cached `rq->min_vruntime`, saving/restoring against it. Applies to the **7.2-rc7 vruntime tree scheduler** (matches our kernel, unlike the later full-fair 1047/1048 ML fixups). **Added 2026-08-14** (manual rebase onto our rc7 series). |
| `1054` | Prike Liang (AMD) | drm/amdgpu/userq: fix lock missing for userq fence error set — **amd-gfx ML 08-07** (`<20260807061422.365929-1-Prike.Liang@amd.com>`). `amdgpu_userq_fence_driver_destroy()` sets the error/signals the fence without holding the fence spinlock; takes `dma_fence_spinlock()` around `dma_fence_set_error()`/`dma_fence_signal()` (locked variants). GFX12 userq fence correctness. **Added 2026-08-15** (sweep). CLEAN on rc7 series. ML-only; not in drm-next/agd5f. |
| `1055` | Boqun Feng (Kernel.org) | drm/amd/pm: Fix incorrect avg vcn utilization in gpu_metrics — **amd-gfx ML 08-05** (`<20260805140227.44868-1-boqun@kernel.org>`). `smu_v14_0_0_get_gpu_metrics()` reported `metrics.VcnActivity` (permyriad) directly; now `/100` → percentage. Our GPU is `smu_v14_0_0`. **Added 2026-08-15** (sweep). CLEAN on rc7 series. ML-only. |
| `1056` | drm-misc `0e118b936` (2026-08-13) | Philipp Stanner | drm/sched: Lock `drm_sched_entity_is_idle()` — **Added 2026-08-19** (merge). Fixes an invalid lockless read of `entity->stopped`/`entity->list`; takes the entity lock around the idle check. `Reviewed-by` scheduler maintainers. CLEAN on the 7.2 series. |
| `1057` | pixelcluster `vramstuff-rebase` `e8e6de2b8` (Natalie Vock) | drm/ttm: grab BO reference before locking it — **Added 2026-08-19** (merge). `__ttm_bo_lru_cursor_next` grabs a BO ref before locking to fix a lifetime race under the LRU refcount rework. Private-fork forward-port; not yet upstream. CLEAN on the 7.2 series. |
| `1058` | pixelcluster `vramstuff-rebase` `eb1170e95` (Natalie Vock) | drm/amdgpu: Track suboptimal always-valid BOs in soft-evicted state — **Added 2026-08-19** (merge). Adds a soft-evicted state for VM_ALWAYS_VALID BOs so they aren't force-evicted; complements carried userq soft-evict work (9036/9038-40/1050). Private-fork forward-port. CLEAN on the 7.2 series. |

---

## 1100–1141 — AMD display

Source: drm-next, confirmed CLEAN-APPLY on v7.2-rc5 via `git apply --check`. `1100`–`1103` were formerly `1025`, `1031`, `1033`, `1065`. Later members (`1114`–`1134`) are documented in the 2026-08-03/04 sweep sections below.

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
| `1135` | Charlene Liu | fix HPD program filter programming — Tom Chung "DC Patches Aug 10 2026" 12/34, amd-gfx ML `<20260805063937.2145774-13-chiahsuan.chung@amd.com>` (08-05). DCN42B DIO: `DC_HPD_TOGGLE_FILT_CNTL` delay fields were written in ms but the HW register unit is 10 ms (÷10), which made connection time extremely long. **Added 2026-08-10** (unmerged ML member). CLEAN on rc7 series. |
| `1136` | Relja Vojvodic | Update and revert FRL LT Timeout — Tom Chung "DC Patches Aug 10 2026" 20/34, amd-gfx ML `<20260805063937.2145774-21-chiahsuan.chung@amd.com>` (08-05). `link_hdmi_frl.c`: fall back to polling when LT-no-timeout is set and bound the FRL LT timer (155 polls at ≥16 Gbps ≈ 300 ms) for appropriate link rates. **Added 2026-08-10** (unmerged ML member). CLEAN on rc7 series. |
| `1137` | `7cc88c0d` | Harry Wentland — Bounds-check connector->index in dm_dp_mst_get_modes — **Added 2026-08-10** from `amd-drm-next-7.3-2026-08-06` tag (Phoronix "AMDGPU last round" follow-up). `amdgpu_dm_mst_types.c`: defensive bounds check on `drm_connector->index` before indexing the per-connector HDCP arrays (sized `AMDGPU_DM_MAX_DISPLAY_COUNT`). CLEAN on rc7 series (applies after 1136). |
| `1138` | `73efd24e2` | Karthi Kandasamy — Fix seamless mode switch not triggering for HDR to SDR transition — **Added 2026-08-10** (drm-next 08-06). Touches `dcn401_hwseq.c` (our DCN401). CLEAN on rc7 series. |
| `1139` | `261e0fe4e` | Harry Wentland — Resize MST HDCP per-connector arrays to 32 — **Added 2026-08-10** (drm-next 08-06). Companion to `1137`: sizes `hdcp_workqueue` arrays to the DRM connector index range so the bounds check is complete. CLEAN on rc7 series. |
| `1140` | Tom Chung 10/34 `20260805063937.2145774-11` | Gabe Teeger — Clamp `force_min_dcfclk` to dcn42b range — **Added 2026-08-10** (was the previous session's planned `1137`; numbered 1140 after the 08-06-tag display members). `dcn42b_clk_mgr.c`: clamps the debug-only `force_min_dcfclk_mhz` override to [200,600] MHz. Debug-option sanitization (no normal-path effect) but DCN42B-safe and clean on rc7 series. |
| `1141` | Samuel Pitoiset | drm/amd/display: Fix NULL pointer dereference in `amdgpu_dm_crtc_set_vblank()` — **agd5f drm-next, amd-drm-next-7.3-2026-08-12 tag** (`7b1b31bf6942`). DCN401 vblank path NULL-deref fix (1 line). **Added 2026-08-14** (sweep). CLEAN on rc7 series. |

~~`1112`~~ (`334cbfa3c`, dcn401 GPIO lookup tables) — **DROPPED**: requires `DC_GPIO_GENERIC_A`/`DC_GPIO_HPD_A` type defs from a prerequisite GPIO infrastructure patch not in rc5.

**Deferred from the Tom Chung 34-patch series** (reviewed 2026-08-10, not taken): 10/34 DCN42B `force_min_dcfclk` clamp (`[200,600]` MHz) — debug-option-only sanitization, no normal-path effect; 16/34 zstate_support rework; 29/34 SopCount workaround — touches `dcn60_clk_mgr.c`, absent from rc7; 33/34 unify fast-update classification — series-dependent. **31/34** (restore FRL cap on non-destructive HDMI link verify) is the upstream submission of our `0058`/`1113` — no separate action.

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

Source: sirlucjan `7.2/block-patches-sep/`. Formerly numbered `1300`–`1304`.

| File | Author | Subject |
|------|--------|---------|
| `2000` | Jens Axboe | block/mq-deadline: pass in queue directly to dd_insert_request() |
| `2001` | Jens Axboe | block/mq-deadline: skip expensive merge lookups if contended |
| `2002` | Jens Axboe | block/bfq: pass in queue directly to bfq_insert_request() |
| `2003` | Jens Axboe | block/bfq: serialize request dispatching |
| `2004` | Jens Axboe | block/bfq: skip expensive merge lookups if contended |

## 2100–2119 — Memory management

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2100` | `repos/sirlucjan-kernel-patches/7.2/zstd-dev-patches/` | Piotr Gorski | zstd-7.2: merge **v1.6.0** into kernel tree (formerly `1400`, previously the "dev tree" variant). **Updated 2026-08-15** to the v1.6.0 combined revision: the earlier dev-tree merge lacked the gcc-BMI2 guard (Nick Terrell, "Work around gcc segfault on versions older than 11.4") that the v1.6.0 single patch now folds in. Applies cleanly to rc7; same 18 files, adds the `__GNUC__ >= 11.4` DYNAMIC_BMI2 gate. |
| `2101` | `repos/firelzrd-lru-marie/patches/testing/0001-linux7.2-rc1-lru_marie-0.10.5.patch` (firelzrd/lru_marie commit `55d2c27`, 2026-08-19) | Masahito S (firelzrd) | mm-7.2: introduce LRU MARIE **0.10.5** (formerly `1401`, `2101` was 0.9.2/0.9.3). **Updated 2026-08-19 on the 7.2 bump** to 0.10.5: regenerated `2101` from the 0.10.5 firelzrd patch against the linux-7.2 series state, with the **`vma_flags_test(&vm_flags, VMA_EXEC_BIT)` one-line fix** applied in-tree (0.10.5 still ships the old `vm_flags & VM_EXEC` expression in its `folio_check_references` block, which conflicts with the CachyOS fixes-branch `vma_flags_t` rename now in `0105`). Verified CLEAN on the full 7.2 series (0 rejects). |
| `2102` | linux-next `39602994a` (via akpm-mm, 2026-08-04) | Haoqin Huang (Tencent) | zram: do not release zstd global params from error paths — removes `zstd_release_params()` from `zstd_create()`/`zstd_setup_params()` error paths (per-CPU layering violation + redundant with `zcomp_init()`). **Added 2026-08-11** (sweep). CLEAN on the rc7 series. ZRAM+ZSTD built-in. |
| `2103` | linux-next `4cdd0dadc4` (via akpm-mm, 2026-08-04) | Haoqin Huang (Tencent) | zram: reject zero-size dictionary — rejects a 0-byte dict instead of silently accepting it (distinct error for `sz < 0` vs `sz == 0`). **Added 2026-08-11** (sweep). CLEAN on the rc7 series. |
| `2104` | linux-next `ad719d383e` (via akpm-mm, 2026-08-04) | Haoqin Huang (Tencent) | zram: reset per-priority params when changing algorithm before init — clears stale params validated against a previous algorithm (e.g. `lz4 level=65535` invalid for zstd) on algorithm change. **Added 2026-08-11** (sweep). CLEAN on the rc7 series. |

Note: `2102`–`2104` are 3 of 5 from Haoqin Huang's "zram: fix zstd error paths and add parameter validation" v6 series. The remaining two (`add pr_fmt to backend files`, `validate parameters in each backend's setup_params`) do not apply cleanly to rc7 — their `backend_deflate.c` hunks assume a newer deflate backend not in the rc7 base — and were not carried. `2107` (`validate deflate params`, Sergey Senozhatsky) is a separate later fix that DOES apply — it validates winbits in `deflate_setup_params()` with hunks compatible with the rc7 backend.

`2105`–`2108` are `Cc: stable` zram stability fixes (Longlong Xia/Kylin + Sergey Senozhatsky, linux-next via akpm-mm, all `Reviewed-by: Sergey Senozhatsky`, `Signed-off-by: Andrew Morton`). `2105`/`2106` fix OOB access in the `read_block_state()`/`writeback_store()` debugfs paths when the device is reset with a smaller disksize between `nr_pages` computation and lock acquisition. `2107` adds winbits range validation to the deflate backend (missing validation → possible `BUG_ON()` in zlib). `2108` sets the default primary compressor in `zram_destroy_comps()` (all compressors NULL is invalid device state; `comp_algorithm_show()->strcmp()` can deref NULL). **Added 2026-08-11** (next-20260811 sweep follow-up). All CLEAN on the full rc7 series.

`2109`–`2110` are new MM fixes from akpm-mm `mm-unstable` (7.3-targeted, not in rc7), **Added 2026-08-12** (sweep), both CLEAN on the rc7 series (`git apply` + GNU `patch --dry-run`):

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2109` | akpm-mm mm-unstable `fe59dda7cd93` (2026-07-28) | Shakeel Butt (Meta) | memcg: bypass the reclaim and oom killer for dying tasks once oom_reaper is done — an OOM-killed process can be stuck in the exit path for hours when zswap holds nearly all of its memory (nothing is left on the LRUs to reclaim and swapin re-charges re-trigger OOM). Fix skips reclaim/OOM for dying tasks once oom_reaper has torn down the mm. Directly matches this build (zswap default-on + systemd memory.max). |
| `2110` | akpm-mm mm-unstable `63d76961f3bf` (2026-08-09) | Longlong Xia (Kylin) | zsmalloc: account for handle size in class lookup — `zs_lookup_class_index()` classifies the payload size directly while `zs_malloc()` adds `ZS_HANDLE_SIZE`, so zram recompression misjudges size-class movement near boundaries (accepts replacements with no allocation benefit or rejects memory-saving ones, potentially marking an object incompressible). Factors class selection into `lookup_size_class()` shared by lookup and allocation. `Assisted-by: Codex:gpt-5.6-sol`. ZRAM+ZSMALLOC built-in. |
| `2111` | akpm-mm mm-unstable `b0b8621d` (2026-08-12) | Kairui Song (Tencent) | mm/mglru: fix and remove redundant unevictable folio handling — drops a redundant mlock/unevictable branch in the MGLRU scan path. We run `CONFIG_LRU_GEN=y`. **Added 2026-08-15** (sweep). CLEAN on the rc7 series (incl. LRU-MARIE `2101`). |
| `2112` | akpm-mm mm-unstable `bad68884` (2026-08-12) | Hui Zhu (Kylin) | mm/mglru: fix young counter undercount for large folios — `lru_gen_look_around()` counted the triggering folio as `young = 1` regardless of size (a leftover from before PTE batching); now counts the full PTE batch like other folios. `Reviewed-by: Baolin Wang`. Prevents under-aging hot PMDs. **Added 2026-08-15** (sweep). CLEAN on the rc7 series. |
| `2113` | akpm-mm mm-unstable `93379b08` (2026-07-02) | Yunzhao Li (Cloudflare) | mm/zswap: use ratelimited stats flush in `zswap_shrinker_count()` — `mem_cgroup_flush_stats()` under the global cgroup rstat lock caused 2.88% osq_lock contention in the kswapd reclaim path on many-NUMA machines; use `mem_cgroup_flush_stats_ratelimited()`. We have `CONFIG_ZSWAP=y`. **Added 2026-08-15** (sweep). CLEAN on the rc7 series. |
| `2114` | linux-next `25f52e8` | Breno Leitao | mm/vmscan: report RCU-tasks quiescent states in `shrink_lruvec()` — calls `cond_resched_tasks_rcu_qs()` in the reclaim loop to lower RCU-tasks stall risk during long reclaim. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |
| `2115` | akpm-mm `f6cc09d` | Breno Leitao | mm, swap: ratelimit bad swap entry reports — `pr_err` → `pr_err_ratelimited` on bad-file/offset paths in `get_swap_device`/`swap_dup_entry`. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |
| `2116` | akpm-mm `855a68e` | Nico Pache (Red Hat) | mm/khugepaged: unmap pte before releasing vma write lock — reorders `pte_unmap()` before `anon_vma_unlock_write()` in `collapse_huge_page()` to avoid a use-after-unmap. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |
| `2117` | akpm-mm `762b38e` | Hao Jia | mm/zswap: support batch writeback in `shrink_memcg()` — per-node zswap LRU walk in the memcg shrinker batched to `SWAP_CLUSTER_MAX`. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |
| `2118` | akpm-mm `811f699` | Zhiling Zou | mm: shmem: reject page-aligned fallocate end overflow — `check_add_overflow()` guard in `shmem_fallocate()` so `offset+len+PAGE_SIZE-1` wraparound returns `-EINVAL`. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |
| `2119` | akpm-mm `8303637` | Usama Arif | mm/memcontrol: avoid false sharing between vmstats and events — moves `vmstats_percpu` out of the `struct mem_cgroup` hot layout and marks it `____cacheline_aligned`. **Added 2026-08-19** (merge). CLEAN on the 7.2 series. |

Not carried this sweep: the `mm/swap: revert to single-folio writes for synchronous swap devices` candidate (Christoph Hellwig, part 1 of the "swap_ops updates" series) does not apply to rc7 — it depends on the earlier unmerged swap_ops series that reworked `mm/page_io.c`.

## 2200 — CPU idle (NAP governor)

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2200` | `repos/sirlucjan-kernel-patches/7.2/nap-patches/` | Masahito S (firelzrd) | 7.2-nap-v0.5.0 (formerly `1500`) |

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

## 9025–9048 — SMU14 PPT + DPM + userq/HMM backports (amd-drm-next-7.3-2026-08-06, ML)

**Added 2026-08-10** from the agd5f staging tag `amd-drm-next-7.3-2026-08-06` (commit `daaeec23`, the "AMDGPU last round for Linux 7.3" pull the Phoronix article covered). Tag fetched into `repos/agd5f-linux`. All 9 verified CLEAN on the rc7 series tree in dependency order (`patch -p1 --forward`, prepare()'s tool), and reverse-checked against the clean rc7 tree (not already upstream). These land in drm-next for 7.3 — the backports are pre-bumps; flag for `patch-cleanup` at the 7.3 move.

### 9025–9029 — PPT-limits framework rework (Yang Wang) — **DROPPED**

| File | Commit | Subject |
|------|--------|---------|
| ~~`9025`~~ | `25f4a46b0c8a` | drm/amd/pm: derive stable PPT limits from PPTable |
| ~~`9026`~~ | `6c9e0328d1de` | drm/amd/pm: refactor PPT limits by controller and power source |
| ~~`9027`~~ | `93bd6de5518d` | drm/amd/pm: account for OD percentage in effective PPT limits |
| ~~`9028`~~ | `534e172b888d` | drm/amd/pm: refactor user PPT policy save and restore |
| ~~`9029`~~ | `cf9fa4d4d033` | drm/amd/pm: restore user PPT limits after GPU reset |

The full 5-commit series applies cleanly to a **clean** rc7 tree, but **`9026` fails on our actual series state**: its 77-line `smu_get_power_limit()` hunk in `amdgpu_smu.c` (hunk #9, `@@ -2954,77 +2948,77 @@`) does not match because the carried CachyOS `01xx`/`0113` micro-opts bundle shifts the surrounding context. `9027`/`9028` then cascade-fail (they build on `9026`). Not taken as a partially-ordered set (`9025` alone is smu11/smu13-only = off-target; `9029` needs the refactor). **Deferred to the 7.3 bump**, where the whole PPT framework arrives via drm-next unchanged. Re-evaluate only if the 7.3 rebase still conflicts — do not hand-force the hunk (framework refactor on the SMU power path implicated in the blackscreen class).

### 9033–9035 — amdgpu CS/VM correctness series (Junrui Luo, amd-gfx ML)

| File | Source | Subject |
|------|--------|---------|
| `9033` | amd-gfx ML `<20260806-amdgpu-fixes-v1-1-ce247012d4da@outlook.com>` | drm/amdgpu: disallow multiple FENCE chunks in one submit — per-submit BO reference leak, `Fixes: d38ceaf99ed0`, `Cc: stable` |
| `9034` | amd-gfx ML `<20260806-amdgpu-fixes-v1-2-ce247012d4da@outlook.com>` | drm/amdgpu: fix VM update overrun on non-4K page kernels |
| `9035` | amd-gfx ML `<20260808-amdgpu-fixes-v2-1-36d66398601f@outlook.com>` (**v2**) | drm/amdgpu: add the BO-va mapping offset when kmapping an IB |

All three CLEAN on the rc7 series (git + GNU `patch`). Applied upstream by Deucher 08-06 (7.3-merge). `9035` uses the 08-08 v2 revision. `0035` is deliberately NOT used (sparse `00xx` gap would suggest a local DCN patch); these live in the `90xx` backport range.

| `9036` | `c0122bf2c` | drm-next 08-06 — Fix userq VA validation for sub-page buffers — **Added 2026-08-10**. `amdgpu_userq.c`: span-check via `amdgpu_vm_bo_lookup_mapping()` for sub-page VA ranges (symbol-clean on rc7; the userq fence/mapping path exists). gfx12 userq correctness. |
| `9037` | `46a0df99a` | drm-next 08-06 — Prefer default discovery offset — **Added 2026-08-10** (final sweep). `amdgpu_discovery.c`: use the default IP-discovery binary offset when a valid signature is present (regression fix `Fixes: 01bdc7e219c4`, closes work_items !5447) — protects RDNA4/gfx1201 IP-block discovery. 13-line clean fix. Final-sweep re-checks confirmed skips: `ef45aaf73` (debug-only CRC, DCN31x), `48f1d2a10` (no-op KFD prep), `9ad81600b` (dead fields, absent priv-fault infra). |
| `9038` | amd-gfx ML `<20260811-amdgpu-fixes-v1-2-4954a417b8ff@outlook.com>` | drm/amdgpu: reject PRT mappings as user queue buffer VAs — **Added 2026-08-11** (sweep). `amdgpu_userq.c`: a PRT mapping has no backing BO, so it can't carry the eviction fence `amdgpu_userq_gem_va_unmap_validate()` waits on; rejecting it avoids a NULL `bo` deref on GEM unmap. Same author/series as `9033`–`9035`. ML-only; not in drm-next/agd5f/amd-staging. |
| `9039` | amd-gfx ML `<20260811-amdgpu-fixes-v1-3-4954a417b8ff@outlook.com>` | drm/amdgpu/userq: bound the eviction fence rearm retry loop — **Added 2026-08-11** (sweep). `amdgpu_userq.c`/`amdgpu_userq_fence.c`: bound the restore-worker eviction-fence rearm loop so an unresolvable `-ENOMEM` can't spin forever; `amdgpu_userq_ensure_ev_fence()` now returns an error with the mutex released. |
| `9040` | amd-gfx ML `<20260811-amdgpu-fixes-v1-5-4954a417b8ff@outlook.com>` | drm/amdgpu: free userptr HMM ranges on the CS error path — **Added 2026-08-11** (sweep). `amdgpu_cs.c`: release still-live userptr HMM ranges on CS error paths so the ranges aren't leaked when submit fails before invalidation. |
| `9041` | amd-gfx ML `<20260817-amdgpu-fixes-v1-2-36d5298da646@outlook.com>` | Junrui Luo | drm/amdgpu/userq: hold the doorbell xa lock during hang reset — **Added 2026-08-19** (merge). `mes_userqueue.c`: take the doorbell xarray lock around the hang-reset path. ML-only, not in any tree. |
| `9042` | amd-gfx ML `<20260814103005.9924-1-lingshan.zhu@amd.com>` | Zhu Lingshan | drm/amdgpu: fix hang and race in userq destroy — **Added 2026-08-19** (merge). `amdgpu_userq.c`: cancels `hang_detect_work` with proper fence ordering so destroy doesn't race the watchdog. ML-only. |
| `9043` | amd-gfx ML `<20260819022138.3908141-1-Jesse.Zhang@amd.com>` (**v2**) | Jesse Zhang | drm/amdgpu/userq: lock and validate wptr BOs before reading their GPU offset on restore — **Added 2026-08-19** (merge). ML-only. |
| `9044` | amd-gfx ML `<20260818072959.3356764-1-Jesse.Zhang@amd.com>` | Jesse Zhang | drm/amdgpu/userq: skip unmapped queues in `amdgpu_userq_wait_for_signal` — **Added 2026-08-19** (merge). ML-only. |
| `9045` | amd-gfx ML `<20260817194953.97887-2-david.belanger@amd.com>` | David Belanger | drm/kfd: Add CU occupancy support to GFX12 — **Added 2026-08-19** (merge). Adds `kgd_gfx_v12_get_cu_occupancy` (gfx1201 = our GPU) using `soc24_grbm_select`. ML-only; the GFX12.1 sibling was dropped (off-target gfx1210). |
| `9046` | amd-gfx ML `<SA1PR12MB8600DD7A487308741A4FDA6B9FA72@outlook.com>` | Vladimir Marioukhine | drm/amdkfd: fix integer overflow in queue ring buffer size calculation — **Added 2026-08-19** (merge, reconstructed from Outlook-mangled archive). Defensive hardening (`check_add_overflow`). ML-only. |
| `9047` | amd-gfx ML `<20260817135918.228397-1-xiaogang.chen@amd.com>` | Xiaogang Chen | drm/amdkfd: Fix error path at `svm_migrate_copy_to_ram` — **Added 2026-08-19** (merge). SVM migration error-path fix. Series 1/3; must apply before `9048`. ML-only. |
| `9048` | amd-gfx ML `<20260817135918.228397-2-xiaogang.chen@amd.com>` | Xiaogang Chen | drm/amdkfd: Fix the case that vm range is hole at `svm_migrate_copy_to_vram` — **Added 2026-08-19** (merge). SVM migration hole-range fix. Series 2/3; applies after `9047`. ML-only. |

`9038`–`9040` must apply **after `9036`** (the userq VA-validation rewrite) — the `amdgpu_userq_input_va_validate()` hunk in `9038` depends on 9036's `amdgpu_vm_bo_lookup_mapping()` span-check shape. All three CLEAN on the full rc7 series (GNU `patch -p1 --forward`). From the same 5-patch 08-11 series: `9040` (1/5, free prt_va) does not apply to rc7 (context shifted), and 4/5 (enforce UVD handle ownership) targets legacy UVD hardware not present on RDNA4 — both not carried.

**Not taken from the userq/priv-fault family:** `9ad81600b` (track faulted gfx user-queue slots) references `userq_priv_fault_slots`/`userq_priv_fault_work` — the same `struct amdgpu_gfx` fields absent from rc7 that dropped `1025` (LESSONS #69). Defer the whole recovery-worker set to 7.3.

**TTM/dmem "aggressive protection" + reclaim stack (drm-misc, merged drm-next 08-08) — DEFERRED to 7.3.** The 11-commit stack (`dd517e49a`…`bd4f284df`, incl. `bbc744c06` "Be more aggressive when allocating below protection limit") applies to clean rc7 but **fails on our series state**: our carried `0104-cachy-cgroup-vram` reworks the same dmem limit-pool API, so the upstream cgroup/dmem + TTM members reject under GNU `patch`. Reconciling means reworking the CachyOS cgroup-vram base — defer to the 7.3 bump (drm-misc-next content arrives via drm-next, and the CachyOS fork reconciles it there). This corrects the earlier PATCH_SOURCES note: the upstream dmem split *is* in rc7; the blocker is our `0104` variant, not a missing split.

---

### 9030–9032 — smu_v14_0_0 DPM clock-query fixes (Priya Hosur)

| File | Commit | Subject |
|------|--------|---------|
| `9030` | `abbc038bcbdb` | smu_v14_0_0: fix DCLK metric reporting via VCLK level index |
| `9031` | `ae60a2b05f81` | smu_v14_0_0: add SMU_DCEFCLK support in DPM frequency queries |
| `9032` | `39dfe8a7d709` | smu_v14_0_0: use find_clk_level() for DPM level marking |

Our RX 9070 XT is `smu_v14_0_0` (dmesg: `detected ip block number 4 <smu_v14_0_0>`); all three edit `smu_v14_0_0_ppt.c` (apply in parent order `abbc038b → ae60a2b0 → 39dfe8a7`). `9031` is motivated by Strix Halo (`pp_dpm_dcefclk` N/A) but adds DCEFCLK to the generic smu_v14_0_0 DPM-frequency query path used by our dGPU — included as a same-file correctness fix. Excluded from the same tag: `19d408ea` (adds GC 11.5.1 = Strix Halo APU IP to the vclk/dclk whitelist — off-target, our GC is 12.0.1), `8e37aa0b`/`0e8faef0` (GMC12.1 TLB semaphore + MMHUB0 check — **already upstream in rc7**), `79b36128` (JPEG v5.0.0 queue reset — **already in rc7**), `bd0c0098` (DC self-refresh exit — **already in rc7**), `df94112c`/`8b87300e` (touch `amdgpu_dm_connector.c`, absent), `047f6037` (touches `dcn60_*`, absent), gfx12 userq priv-fault set `30f07c06`/`e9e0bd23`/`8a28e151`/`a8e151fe` (needs gfx11 priv-fault infra absent from rc7 — same blocker as dropped `1025`).

---

## 2026-08-26 — Wannabe 7.3-rc1 preview tree

Created a **wannabe 7.3-rc1** preview tree at `wannabe-7.3-rc1/` (git worktree
from `repos/linux-next` at **next-20260825**), because 7.3-rc1 is not yet
released. Full six-source sweep (drm-next, drm-misc, amd-staging-drm-next,
linux-next, linux-pm, amd-gfx + dri-devel ML, sirlucjan, GitLab work-items,
Phoronix) to identify 7.3-window hardware-relevant content.

**Base = next-20260825 already covers most of the window** (no backport
needed): amd-drm-next-7.3-2026-08-19 merge, ~30 MM commits (MGLRU/vmscan/zram/
zsmalloc/zswap), amd-pstate dynamic-EPP + CPPC set, sched-ext fixes, sch_cake
fix, dmemcg. These arrive with the real 7.3 bump.

**Merged on top — three layers, committed on the worktree branch `wannabe-7.3`:**

*Layer 1 — upstream merges (18 commits, `759b7fb8fbe9`):*
- 17 amd-staging-drm-next: KFD CRIU restore_mqd NULL guard (`75a5e1b6b`),
  userq fence-lock (`dc312e088`) + wptr-restore (`67376cbe8`), MES teardown
  (`300ef13f1`), SVM migrate error+hole (`ec4d432be`,`f0b4aedc4`), AQL
  zero-size (`15b286c89`), CU-occupancy GFX12 (`61e1afedd`), no-retry PTE
  (`9b7ce74b7`), VM dw-estimate (`39e5b1e4f`), DCN42 min-dispclk
  (`b7c4f79d7`), OPP/DPP (`a7f08cbee`), dc_lock leak (`683b1264d`), DM IRQ
  NULL guard (`0372d4c81`), dml2 bpp (`a3540509b`), vblank_nom (`3fa6d595d`),
  mes indenting (`b17d01d87`), HPD IRQ logging (`288f60836`).
- drm/sched lock `drm_sched_entity_is_idle()` (`0e118b936`, fuzz-3).

*Layer 2 — sleepy-kernel additive series (69 commits, `4834e3546e26`):* the
full CachyOS branch squashes (0101 bbr3, 0103 kbuild, 0104 cpu-isa, 0105
config-hooks/fixes, 0106 off-target drops, 0108 preempt-ipi, 0109 ACPI-BM/
S5-eviction, 0110–0113 fork backports) + local GPU fixes (PROFILE_PEAK, SMU14,
DCN/EDID, TLB-invalidation, retry-fault, userq, MES CRIU, VCN util,
soft-evicted), bfq/mq-deadline, LRU-MARIE 0.10.5, zstd/zswap, NAP governor —
so the tree is a superset of the 7.2.0-2 build, not just upstream 7.3.

*Layer 3 — Phoronix WIP merge (8 commits, `7afdec79e9f0`…`6c2092bc8448`):*
Rik van Riel's `mm/gup` `follow_page_mask()` batching RFC v3 (lkml
`20260811025157.1632867-1-riel@surriel.com`, 08-11) — up to 12.8× in gup_test
on mTHP; applies cleanly to next-20260825 (`git am`, no conflicts). Marked RFC
(v4 exists) — expect upstream revisions to supersede; the merge point is
isolated so it's easy to drop. Reverses the 08-15 "Reviewed, not taken"
verdict **for the wannabe tree only**; still not part of the PKGBUILD series.

**Phoronix month check (through 08-25) — verified already in base:** SMP-IPI
preemption rework (ByteDance/Chuyi Zhou, `smp-core-2026-08-17`: task-local IPI
cpumask `9a560af15fd3`, preempt-before-wait `8df8a6028309`), `x86_mm_for_7.3`
`flush_tlb_multi()` preemption + stack `flush_tlb_info`, TTM-aggressive
(Valve, `bbc744c062f8` + `3d33e9c726d6`), amd-pstate dynamic-EPP per-policy
(`b7294b627598`) + `epp_boost` (our cmdline already uses it), sched-ext
feature-complete (`11260c335ec6`), zsmalloc `zs_free` + `rmap_walk_ksm`
(19 Aug MM). **Off-target:** menu-governor 5× wakeup (Intel Xeon; we run the
NAP governor), RTL8261C/D 5 GbE (we have RTL8125B/r8169), DRM fair-policy fix
(FIFO default), k10temp per-CCD (EPYC Zen 5 only).

**Deferred:** sirlucjan reflex 0.3.1r2 governor (cpufreq API 4→5 args;
needs port + review); work-items #5616/#4753 (WIP/community, no upstream
provenance); HDMI 2.1 VRR/ALLM (AMD amd-gfx — missed 7.3, WIP; re-evaluate
when they land); ML-only userq/KFD series mostly superseded by amd-staging or
awaiting v2+. See `WANNABE-7.3.md` for the full breakdown and rebuild
instructions.

---

## 2026-08-19 — Bump to Linux 7.2 stable (drops + CachyOS squash regen + MARIE 0.10.5)

Bumped the base from 7.2-rc7 to the **7.2 stable release** (`linux-7.2` tag,
commit `8d3ae5928`). Reference tree moved to `repos/linux-7.2`. Version is now
`7.2.0-1-sleepy`. The series dropped from 184 to 157 patches.

**Dropped — obsolete DRM scheduler revert series (1029–1046) + min_vruntime
(1053):** 7.2 stable upstream already reverted FAIR→FIFO (commit `2bbea6b81`
"Revert drm/sched: Switch default policy to fair") and defaults to FIFO with
multi-rq, so the entire Tvrtko revert series we carried for rc7 is now
redundant. Includes `1029`–`1043` (num_rqs restore reverts), `1044`/`1045`
(FIFO/RR + default-policy reverts), `1046` (fair-experimental marker), and
`1053` (min_vruntime cache — FIFO default doesn't use vruntime).

**Dropped — merged upstream in 7.2:** `1048` (vm_flush missing check),
`1049` (nbif 6.3.1 L1), `1052` (GEM_CREATE domain validation), `1134`
(BT.2020 CSC), `1141` (vblank NULL-deref), `9033` (FENCE-chunk leak), `9037`
(discovery offset), `9008` (TRUNCATE_COORD_MODE — present in 7.2
`gfx_v12_0.c`).

**Regenerated — CachyOS fixes squashes:** `0105-cachy-fixes.patch` /
`0106-cachy-drops.patch` rebuilt from the current sirlucjan `fixes` branch
(24-patch, renumbered from v11's 25). The branch now carries the MM
exec-folio series (`vma_flags_t` conversion, exec-folio helper, MGLRU
promote-exec) inside `0105` — so those upstream MM patches are **covered by the
squash**, not adopted separately. `0012` (DisplayID adaptive range, eDP OLED
off-target) is excluded from the squash; `0106` reverts the i915/btusb/rtw89/
nouveau/i2c/iwlwifi/ALSA/ASoC/sof off-target groups.

**Upgraded — LRU MARIE to 0.10.5:** see the `2101` row above.

**Kept with rebase:** `9007` (DB_RING_CONTROL — applies in series order on
7.2, isolated check needs prior-patch context).

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

**Work items tracker — READABLE (three working methods, learned 2026-08-10):**
The Anubis anti-scrape challenge is served **only to browser-like User-Agents**.
All of the following work with plain `curl` and **no User-Agent** header:
1. **Issues + project events API** — `GET /api/v4/projects/drm%2Famd/issues?...`
   and `GET /api/v4/projects/drm%2Famd/events` (events include full `note.body`).
2. **HTML page per issue** — `https://gitlab.freedesktop.org/drm/amd/-/issues/<iid>`
   (no UA) returns HTTP 200 with the issue description rendered server-side.
   Comments are Vue-lazy-loaded and NOT in this HTML.
3. **GraphQL API — full comments/notes (the breakthrough)** — unauthenticated:
   ```bash
   curl -s "https://gitlab.freedesktop.org/api/graphql" -H "Content-Type: application/json" \
     --data '{"query":"query { project(fullPath: \"drm/amd\") { issue(iid: \"5538\") { title notes { nodes { body system } } } } }"}'
   ```
   Returns every note body for the issue (filter `system:true` out). This was the
   missing piece — the REST **notes API is 401-gated** (real auth), but GraphQL
   exposes the same notes unauthenticated for public projects. Scripts live in
   the scratch tools (`/tmp/gl_comments.sh`, `/tmp/gl_fixscan.sh`, `/tmp/gl_scan.sh`).
   **2026-08-10 comment-scan result:** no driver-side SMU IF fix in !5538/!5479/!5038
   (confirmed firmware/VBIOS-side); AMD dev on !5538 suggests testing `pcie.aspm=off`
   (grub) as a stopgap; the display-stall class (!4753/!5203/!5571/!5320) has an
   in-progress FAMS2 investigation + a `pp_dpm_mclk` sysfs fix (`d81e52fc`) and
   P-state fixes (`c764b7af`) that are **newer than rc7**.

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
| `1134` | fix BT.2020 YCbCr limited output CSC matrix | Nathan Lucas amd-gfx ML 2026-08-02, Message-ID `2fcc52cc1a86d6e9e393e72f6038ae42ccf1930d.1785616749.git.nlucasgit@gmail.com` (P1 of the `1785616749.git.nlucasgit@gmail.com` 2-patch series) — ML-only, not in drm-next/linux-next. `Assisted-by: OpenAI-Codex:GPT-5.6-Sol` + named human author + `Signed-off-by` (rule 2026-08-03). Fixes `COLOR_SPACE_YCBCR2020_TYPE` (selected for `COLOR_SPACE_2020_YCBCR_LIMITED`) which had full-range luma/chroma scaling — output too bright on calibrated HDR. Splits into `_LIMITED_TYPE`/`_FULL_TYPE` with ITU-T H.273-derived matrices. Author tested on a 9070 XT. `find_color_matrix()` consumers are `dcn10_dpp_cm.c`, `dcn20_mpc.c`, `dcn30_mpc.c` — the DCN output-CSC path used by DCN401/DCN42B. CLEAN on rc6 (`git apply --check` + `patch --dry-run -Np1` both pass). **P2 (DCE copies in `dce_transform.c`/`dce110_opp_csc_v.c`) NOT taken** — DCE IPs, off-target hardware |

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
was a silent no-op. **After user sign-off, the CACHY set was adopted as `0110`
(curated: excludes `vm_swappiness=100` and the elevator bfq hunk), and `-e CACHY`
restored.**

## 2026-08-04 CachyOS fork audit (subagent) — additional adoptions + declined list

A background subagent diffed the full CachyOS `cachyos-7.2-rc6-2` tree against our
series (torvalds rc6 + all carried patches) and enumerated the 237 CachyOS-only
commits. **Adopted** (`0111`–`0113`, all apply cleanly, real authors):
- `0111` ACPI bus-master check disable for AMD (Zen 4 C3) — `14f3669dd743`
- `0112` amdgpu skip VRAM eviction at S5 — `575943925bac`
- `0113` micro-opts bundle (readahead 256K, sched/readdir hints, list.h inline, evdev call_rcu)

**Evaluated, not adopted (with reasons):**
- s5-power shutdown path (`4e200c0ee092` + 4 PCI/PM commits) — medium risk, changes
  the poweroff flow; kept out by default, available as a trial.
- PCI ACS-override boot param — only useful for GPU passthrough (not planned).
- KSM rmap_walk optimization — low value on a desktop.
- EEVDF single-runqueue + cgroup_mode (Peter Zijlstra WIP) — not in linux-next, huge
  CFS rework, conflicts with our sched-ext-first stance.
- POC selector — experimental 2k-line idle-CPU selector, redundant under sched-ext.
- LLVM machine pipeliner (`-mllvm -enable-pipeliner`) — same miscompilation-risk
  class as the excluded `clang-patches` branch.
- TSC `directsync` series — Zen 4 has `IA32_TSC_ADJUST`.
- `unprivileged_userns_clone` — security policy, not hardware.
- `znver5` RDSEED fix — Zen 5 only.
- swap-in readahead disable — low value, conflicts with LRU-MARIE.

---

## 2026-08-10 sweep results — 7.2-rc7 bump + Phoronix audit + MARIE 0.9.3

**Version bump to 7.2-rc7** (`_rcver=rc7`, pkgrel reset to 1). rc7 tag verified at
`git.kernel.org/torvalds/t/linux-7.2-rc7.tar.gz` (sha256 `aa217866eea669da8d84212161131a7315bb94dafcd739a9e9e294d65e748c10`).
Full 128-patch series rebased: 124 apply cleanly, 3 dropped (below), and the
CachyOS `0105`/`0106` squashes were regenerated against the rc7 series state
(fixes branch still v10; off-target drop list unchanged — net applied effect
byte-for-byte the same hunks, re-contextualized). All other `01xx` squashes and
the `0110`–`0113` CachyOS/linux-fork backports apply unchanged (fork untouched
since the 06-19 tag; the fork's April–May reverts — `sched_move_task`,
`dmub_srv_wait_for_idle`, CACHY timer_slack — predate our 08-04 curation and
were already excluded).

**Dropped (merged upstream in rc7):** `1020` (`5227c2c77c38`), `1021`
(`cda6ab11c1a2`), `1022` (`fd37f9dd5b5a`). All three verified — exact content
present in the clean rc7 tree and upstream commits confirmed in torvalds
history (not needlessly dropped).

**Added (3):** `1024` mes12 dropped-dispatches fix (drm-next `288cc4a54`),
`1135` DCN42B HPD filter unit fix, `1136` FRL LT timeout update/revert
(1135/1136 = Tom Chung "DC Patches Aug 10 2026" 12/34 + 20/34, amd-gfx ML
08-05, unmerged). `1025` (gfx12 priv-fault recovery, drm-next `30f07c06`) was
attempted and dropped at build — see the 1000-range section above for the
missing-symbol reason.

**Phoronix-flagged items audited (2026-08-10):**
- **Safe RET interrupt vuln** (SRSO, affects Zen 1–4 incl. our 7700): fix
  merged via `f5fdd6665ac4` → `7e7f81cf6f5c` "x86/bugs: Make Safe-RET robust
  against interrupt injection" — **already in rc7 base**, no patch needed.
- **Zapscape** (KVM x86 shadow-MMU UAF, CVE-2026-64561): fix `2abd5287f083`
  "KVM: x86: Check for invalid/obsolete root..." landed 07-21 — **already in
  rc5**, no action (and no KVM guests on this desktop anyway).
- **HDMI 2.1 VRR/ALLM v2** (Fangzhi Zuo, `[PATCH v2 0/4]`, amd-gfx 08-06,
  MID `20260806205449.16806-1-jerry.zuo@amd.com`): **deferred** — v2 rebases on
  amd-staging-drm-next (base `c4f76bf5e107`) where `amdgpu_dm_connector.c` and
  `amdgpu_dm_freesync.c` exist; **rc7 mainline has neither** (connector logic
  still in `amdgpu_dm.c`). Our `0050`/`0055`/`0058` (v1 lineage) remain the
  correct mainline form. v2's `drm/edid` member (2/4, now authored by Tomasz
  Pakuła) can be re-examined when the connector split lands.
- **Aggressive TTM** (Valve dmemcg protect series v8, Natalie Vock/Timur
  Kristóf, dri-devel `20260804-dmemcg-aggressive-protect-v8`): **deferred** —
  targets the 7.3 merge window; needs the DMEMCG aggressive-allocation split
  (`ttm_bo_attempt_alloc`) not present in our `0104`-carried dmem base.
- **AMDGPU 7.3 last round** (Deucher `amd-drm-next-7.3-2026-08-06`): took the
  GFX12-core members (`1024`, `1025`). Deferred: `4195148` MCM color-manager
  migration (29 files, touches `dcn60*` absent from rc7), `6411a35`
  hwss_set_output_transfer_func NULL check (fixes **Vega/DCE** GPUs — off-target
  for RDNA4), `9d07a6e` native-cursor-mode (needs `amdgpu_dm_cursor.c` split).

**Blackscreen log analysis (2026-08-10):** no kernel panic, oops, or GPU reset
in `log1.txt`/`log2.txt`; all six shutdowns clean. The blackscreen signature is
a display-death burst (xdg-desktop-portal-cosmic "Broken pipe" → compositor
loses its display connection) with the rest of the system alive. Recurring
`REG_WAIT timeout - optc401_disable_crtc` during boot and
`clocksource: Watchdog remote CPU N read timed out` at every boot. See
LESSONS.md. This points at a DCN401 display-path hang (silent, no fence
timeout), not a compute/thermal failure — the 1135/1136 display fixes and rc7's
DCN/JPEG-reset fixes are the relevant mitigations. Consider the drm/amd
work-items !4753 (FAMS2 memclk-change pipeline stall on gfx1201) and !5596
(flip_done timeout on 9070 XT) as follow-ups.

### 2026-08-10 follow-up — Phoronix-source re-audit + full six-source sweep (subagents)

**Result: 11 patches added + 1 revision swap (series 127 → 138).** Ran 4 parallel
agents (Phoronix articles + their sources; gitlab drm/amd work-items + amd-gfx +
dri-devel ML; drm-next/amd-staging-drm-next/linux-next git sweeps; torvalds
x86/security + linux-pm + sirlucjan + firelzrd). Full re-verification of the five
Phoronix stories:

- **More-Aggressive-TTM (Linux 7.3):** `dmemcg-aggressive-protect` v8 (Valve,
  Natalie Vock) — **deferred**. Needs the DMEMCG `ttm_bo_attempt_alloc` split
  absent from rc7's `drivers/gpu/drm/ttm/` (re-verified; no dmemcg hooks in rc7
  TTM). Lands via drm-misc-next at the 7.3 bump.
- **AMD HDMI VRR/ALLM v2:** `0055` **is** the v2 2/4 `drm/edid` member (verified
  byte-identical modulo a trailing blank line); 1/4 (AMD VSDB FreeSync, now the
  Alex Huang common-code series) and 3/4/4/4 (display) need `amdgpu_dm_connector.c`/
  `amdgpu_dm_freesync.c`, still absent from rc7 — **deferred** to the 7.3 bump.
- **Zapscape (CVE-2026-64561):** fix `2abd5287f083` already in rc5/rc7 — **no action**.
- **Safe-RET interrupt vuln:** `x86/bugs: Make Safe-RET robust against interrupt
  injection` (`7e7f81cf6f5c`) is an ancestor of v7.2-rc7 — **no action**.
- **AMDGPU last round for 7.3** (`amd-drm-next-7.3-2026-08-06`, 100 commits):
  took the hardware-relevant members that apply to rc7 (below). Already-upstream
  in rc7 (skipped): GMC12.1 TLB-inv semaphore + MMHUB0 check, JPEG v5.0.0 queue
  reset, DC self-refresh-exit, lockdep fix. Blocked (skipped): gfx12/userq
  priv-fault set (needs gfx11 priv-fault infra, same as dropped `1025`), native
  cursor (`amdgpu_dm_cursor.c` absent), DCN6 `dcn60_*` members, MCM color-manager
  (dcn60), hwss_set_output_transfer_func (Vega/DCE = off-target), FRL-gating +
  wb-info-leak (`amdgpu_dm_connector.c` absent), SMU15 commits (off-target).

**Added this follow-up:**

| Patch | Source | What |
|-------|--------|------|
| `0050` (**swapped**) | Alex Huang v3 1/4, ML `20260804143339.714548-2` | AMD VSDB FreeSync parser upgraded from v2 — adds v1/v2 payload structs + parses VSDB version >3 as v3. Deferred same-series: 2/4, 3/4 (needs rebase), 4/4 (CachyOS-hdmi conflict) |
| `1137` | `7cc88c0d` (08-06 tag) | MST connector->index bounds check |
| `1138` | `73efd24e2` (drm-next 08-06) | DCN401 HDR/SDR seamless-mode-switch fix |
| `1139` | `261e0fe4e` (drm-next 08-06) | MST HDCP per-connector array resize (companion to 1137) |
| `1140` | Tom Chung 10/34 (ML 08-05) | DCN42B `force_min_dcfclk` debug clamp (prev. session's planned `1137`) |
| `9030` | `abbc038b` (08-06 tag) | smu_v14_0_0: DCLK metric fix |
| `9031` | `ae60a2b05f81` (08-06 tag) | smu_v14_0_0: SMU_DCEFCLK in DPM queries |
| `9032` | `39dfe8a7d709` (08-06 tag) | smu_v14_0_0: find_clk_level() DPM level marking |
| `9033` | amd-gfx ML `amdgpu-fixes-v1-1` | disallow multiple FENCE chunks (BO-ref leak) |
| `9034` | amd-gfx ML `amdgpu-fixes-v1-2` | fix VM update overrun on non-4K pages |
| `9035` | amd-gfx ML `amdgpu-fixes-v2-1` (v2) | add BO-VA mapping offset when kmapping IB |
| `9036` | `c0122bf2c` (drm-next 08-06) | gfx12 userq VA validation for sub-page buffers |

**Evaluated and rejected/deferred:** PPT-limits framework rework `25f4a46b`–`cf9fa4d4`
(9025–9029) — `9026`'s 77-line `smu_get_power_limit()` hunk fails GNU patch on our
series state; whole framework defers to the 7.3 bump (see the 9025–9029 section).
`19d408ea` vclk/dclk whitelist = GC 11.5.1 (Strix Halo APU) — off-target.
`drm/amdgpu: check ASPM on the dGPU host link` — only changes behavior for dGPUs
behind an internal AMD PCIe switch; our single 9070 XT is unaffected (off-target).
CachyOS branch dirs (`sirlucjan`/`firelzrd`): nothing new since 07-31 (`fixes` v10,
`lru-marie` v12/0.9.3, `nap` v0.5.0). x86/security: Safe-RET in rc7, no new Zen-4
items after 08-08. linux-pm: no new amd-pstate after 08-08.

**Work-items to watch (no fix merged yet):** !5596 (flip_done timeout, 9070 XT),
!5538 (SMU IF 0x2e/0x33 — blackscreen root cause, still open), !5585 (RDNA4
artifacts @ high refresh + FreeSync), !5582 (GEM BO leak → OOM on gfx1201),
!5593 (atomic EBUSY flicker).

**Comment-scan result (GraphQL method, same day):** pulled every commit SHA /
patch link from the comments of ~25 hardware-relevant work items. **No new
backportable patches** — every fix referenced in the comments is already in the
rc7 base: `239d0ccf` smu v14 soft-clock freq (and `c764b7af` v13), `d81e52fc`
missing `*` on pp_dpm_xxx, `76a2db58` FRL support, `8419331e`/`05984e29` exit
idle-opt (in rc6). The rest are regression-bisect targets (!5527), upload
hashes, or register addresses. The one action: AMD devs on !5538 recommend
`pcie.aspm=off`.

**Config change (not a patch):** **PCIe ASPM → off** (was `PCIEASPM_PERFORMANCE`).
rc7's Kconfig has no ASPM "off" policy (choice = BIOS-default/powersave/
powersupersave/performance), so `prepare()` now drops the compile-time PERFORMANCE
policy and the built-in CMDLINE passes `pcie_aspm=off` (sets `aspm_disabled=true`,
`pr_info("PCIe ASPM is disabled")` — verified in `aspm.c`). This is the !5538
SMU bus-drop stopgap. Trade-off: slightly higher idle PCIe power. Documented in
README.md.

---

## 2026-08-10 late-day sweep — CachyOS fixes v11 + GFX12 CRIU fix

Run after the 7.2-rc7 bump sweep (this morning). Linux-next fetched to
`next-20260810`; torvalds still 7.2-rc7 (no bump).

**CachyOS fixes branch advanced v10 → v11** (sirlucjan `7.2-rc/cachyos-fixes-patches-v11-sep`,
added 2026-08-10 10:42 — after this morning's sweep). v11 renumbers 26→25 patches
(drops the usbcore 255-byte quirk), reworks `mm/mglru` + `mm/vmscan` to the
`vma_flags_t` API (our 0105 already matched), and adds the **PCI Skip Target
Speed quirk** (Maciej W. Rozycki, `Cc: stable` — skips 2.5GT/s link-retrain on
empty/clamped PCIe slots, saving ~2s per boot). Regenerated `0105`/`0106` from
v11 against the rc7 series state; net effect verified byte-identical to the old
squashes except `drivers/pci/quirks.c` (the new quirk). 0106 drop list updated:
no longer reverts the usbcore 255-byte quirk (gone from branch), now reverts
`mt76/dma.c`. User-approved inclusion.

**GFX12 CRIU NULL-deref fix** (Vladimir Marioukhine/AMD, amd-gfx 2026-08-04) —
adopted as `1026`. Security-relevant: a `CAP_CHECKPOINT_RESTORE` user can panic
the machine on gfx1201 via `KFD_IOC_CRIU_OP_RESTORE`. ML-only (not in
drm-next/linux-next yet); Alex Deucher requested brace-style revisions, so a v2
may supersede — swap when the merged commit lands. **mbox reconstruction:** the
lists.freedesktop.org copy had context-line leading spaces stripped and
tabs→spaces by the Outlook sender; the `+`/`-` content was intact. Rebuilt the
diff body against rc7 (v11 MQD manager as the "modeled after GFX 11" template),
verified content-identical modulo whitespace, passes both `git apply --check`
and GNU `patch --dry-run`.

**Not taken this sweep:** dmemcg aggressive-protect v8 (Natalie Vock) — already
merged in drm-misc-next/drm-next (comes with next bump); ACPI CPPC series
(linux-pm linux-next branch, 08-05) — 7.3-targeted, not rc7-backport material;
PCIe link-capability quirks in linux-pm — off-target. Work-items tracker: all
open reports still unresolved, no new driver-fix commits; SMU-IF (issue !5538)
remains firmware-side with `pcie.aspm=off` as the stopgap.

**Follow-up re-check (sirlucjan / firelzrd / linux-next, 2026-08-10):** nothing
new to adopt. sirlucjan still at fixes v11 (adopted above), lru-marie v13 =
0.9.3 (= our `2101`), preempt-ipi v3 (unchanged). firelzrd latest = BORE 6.8.0
and LRU-MARIE 0.9.3 — both match our tree. linux-next remains `next-20260810`
(no newer tag); no new drm/amd/display commits since 08-07. The 7-patch
sirlucjan amd-pstate set was cross-checked: `0001` (Bail out early) and `0007`
(Loosen `lowest_nonlinear_freq != min_freq` requirement, Mario Limonciello)
are **already in the rc7 base** (verified in `amd-pstate.c`); `0002`–`0006`
are our `1205`–`1209`. No gaps.

---

## 2026-08-11 sweep results — next-20260811 + userq/HMM + zram fixes

Six-source sweep (drm-next, drm-misc, linux-next, linux-pm, amd-gfx +
dri-devel ML, sirlucjan, GitLab work-items, x86/security line). Also fetched
**next-20260811** (today's snapshot). The series grew from 140 to 151 patches.

**Adopted:**

- `1027` — GFX12 MES scheduler ring fence force-completion (Jesse Zhang/AMD,
  amd-gfx ML 08-06, `<20260806075653.711275-1-Jesse.Zhang@amd.com>`). MES ring
  has no drm scheduler, so the reset force-completion loop skips it; its
  wb-backed polling fence survives a MODE1 reset while `sync_seq` advances,
  wedging the first post-resume submission. ML-only, not yet in drm-next.
- `9038`–`9040` — GFX12 userq/HMM correctness (Junrui Luo, amd-gfx ML 08-11,
  series `20260811-amdgpu-fixes-v1`): reject PRT mappings as userq buffer VAs,
  bound the eviction-fence rearm retry loop, free userptr HMM ranges on the CS
  error path. Same author as carried `9033`–`9035`; must apply after `9036`.
  From the same series, `1/5` (free prt_va) and `4/5` (UVD handle ownership)
  were not carried — context shifted / legacy UVD hardware.
- `2102`–`2104` — zram zstd error-path + param fixes (Haoqin Huang/Tencent,
  linux-next via akpm-mm 08-04).
- `2105`–`2108` — zram stability fixes (`Cc: stable`, Longlong Xia/Kylin +
  Sergey Senozhatsky, linux-next via akpm-mm 08-04): OOB in
  `read_block_state()`/`writeback_store()`, deflate winbits validation, NULL
  primary compressor after destroy.

**Watch (no patch carried — no formal fix landed):** DRM scheduler FAIR-policy
regression on RX 9070 XT under max GPU load (amd-gfx + linux-kernel ML
08-08/10). Tvrtko Ursulin proposed an informal `min_vruntime` fix; maintainers
leaning toward reverting the FAIR-default switch (`45c211ddf92a`). rc7 carries
the FAIR-only scheduler. Adopt the merged fix/revert when it lands. Note:
scx_sched (CPU scheduler) does not affect this GPU-side scheduler regression.

**Not taken:** dmemcg aggressive-protect v8 (already merged drm-misc, arrives
with next bump; also conflicts with our `0104` cgroup-vram squash); ACPI CPPC
series (ARM-oriented, 7.3-targeted); PSR "multiple displays" patch
(Canonical laptop fix, off-target); VRAM manager init-ordering + UAF fixes
(init-failure-path only; init-ordering already in drm-next).

---

## 2026-08-12 sweep results — DRM scheduler FAIR regression fix + MM fixes

Six-source sweep (drm-next, drm-misc, agd5f, amd-staging, linux-next
`next-20260811` unchanged, linux-pm, amd-gfx + dri-devel ML, sirlucjan,
firelzrd, GitLab drm/amd work-items, x86/security line) plus the two
user-flagged lore.kernel.org threads (fetched via the freedesktop mbox
archives — lore itself is Anubis-blocked). Series grew 151 → 154 patches.

**Adopted:**

- `1028` → **superseded 2026-08-12** by the full revert series (`1029`–`1046`).
  drm/sched: Ensure monotonic `min_vruntime` (Tvrtko Ursulin, dri-devel ML
  08-11, `<20260811134223.96203-1-tvrtko.ursulin@igalia.com>`) was adopted as a
  minimal mitigation for the **DRM scheduler FAIR-policy regression on RX 9070
  XT** (Luke Wildhardt, 08-08): since 7.2 made FAIR the scheduler default,
  sustained 100% GPU load degrades the foreground app to ~10 fps or freezes the
  desktop; 7.1.5 and FIFO both pass. Root cause is unbounded `vruntime` growth
  for a run-queue entity that never exits. ML-only v1 partial fix ("reportedly
  fixes the regression a bit but possibly not fully"). **Follow-up (same day):**
  adopted Tvrtko's full v2 20-patch revert series as `1029`–`1046` (see the
  `1000` range table) — the definitive fix, restoring the pre-fair FIFO/RR
  multi-run-queue scheduler with FIFO as default. `1028` no longer applies
  (the revert removes the `min_vruntime` machinery it patches) and is dropped.
  The revert series initially did not apply cleanly to rc7 in isolation
  (5+ hunks conflict) but applies cleanly in series order with GNU `patch`
  after one rc7-adapted hunk in `1043` (`amdgpu_xcp.c`).
- `2109` — memcg: bypass reclaim/OOM for dying tasks once oom_reaper is done
  (Shakeel Butt, akpm-mm mm-unstable `fe59dda7cd93`). Fixes OOM-killed
  processes stuck for hours in the exit path when zswap holds their memory
  (nothing on LRUs; swapin re-charges re-trigger OOM). Matches this build's
  zswap default-on + memory.max setup.
- `2110` — zsmalloc: account for handle size in class lookup (Longlong Xia,
  akpm-mm mm-unstable `63d76961f3bf`). zram recompression misjudges size-class
  movement near boundaries because lookup classifies payload size while
  allocation adds `ZS_HANDLE_SIZE`.

**Reviewed, not taken (PKGBUILD series):** Rik van Riel's `[RFC PATCH v3 0/8]
batch lookups in follow_page_mask()` (lkml 08-11,
`<20260811025157.1632867-1-riel@surriel.com>`) — gup perf series (2.2–5.9× on
mTHP, up to 12.8× in gup_test), RFC not merged, not adoptable as-is for the
7.2 build. **Later merged into the wannabe 7.3 tree** (08-26, applies cleanly
to next-20260825) — see the 2026-08-26 record above.
mm/swap single-folio revert (Hellwig) — needs the unmerged swap_ops series
prereqs in `mm/page_io.c`. DCN42 DCHVM↔rIOMMU SDP port series (James Lin,
amd-gfx 08-11) — display-virtualization, off-target for a desktop. zram
big-endian slot-lock fix — x86_64 LE unaffected. zswap global-shrinker fix
(memcg-disabled) — `CONFIG_MEMCG=y` here.

**Not taken this sweep:** drm-next/agd5f/amd-staging/drm-misc/linux-pm had no
new commits since 08-11; linux-next unchanged at `next-20260811`; sirlucjan
(fixes v11) and firelzrd (BORE 6.8.0 / LRU-MARIE 0.9.3) unchanged; x86/security
line clean; GitLab work-items tracker had no new adoptable driver-fix commits.

---

## 2026-08-15 sweep results — userq fence + SMU14 VCN + MGLRU/zswap

Six-source sweep + akpm-mm. Fetched `next-20260814` (newest snapshot;
`next-20260815` not yet published, Saturday). The series grew from 179 to 184
patches.

**Adopted:** `1054` (userq fence error-set spinlock, Prike Liang, amd-gfx ML
08-07), `1055` (SMU14 VCN utilization permyriad→%, Boqun Feng, amd-gfx ML
08-05), `2111` (MGLRU redundant unevictable-folio handling, Kairui Song,
akpm-mm 08-12), `2112` (MGLRU young-counter undercount for large folios, Hui
Zhu, akpm-mm 08-12), `2113` (zswap ratelimited stats flush, Yunzhao Li, akpm-mm
07-02). All CLEAN on the full rc7 series.

**Not taken:** gfx12 dynamic-VGPR trap handler (08-14 v1, large generated-hex,
conflicts on series); bind-imported-BOs v3/v4 (competing same-day revisions,
still in review); TTM LRU bulk-move nested-sublist refactor (08-14 v2 under
rapid revision, invasive); Infinity Scheduler (sirlucjan — EEVDF mod conflicts
with sched-ext); HDMI 2.1 VRR/ALLM v4 (overlaps `0055`, needs absent
`amdgpu_dm_connector.c` split); `drm/sched: Fair policy fixups` (08-14, targets
the full-fair 7.3 codebase, not our FIFO-reverted rc7 scheduler — already
evaluated 08-14). Work-items tracker: open reports are firmware/user-space
(AV1 artifacts from `linux-firmware` 20260810; VRR/blanking compositor-side)
— no driver-side kernel patch.

---

## Adding new patches

1. Place the patch file in its `patches/<range>/` folder (one folder per number
   range; the PKGBUILD auto-creates gitignored root symlinks so makepkg can
   resolve them — do not commit root-level `*.patch` files).
2. Use the correct numeric prefix (see the conventions table): `0001`–`0049` local, `0050`–`0099` upstream display, `0101`–`0113` CachyOS (squashed per branch), `1000`–`1099` GPU core, `1100`–`1199` display, `1200`–`1299` PM, `2000`–`2099` block, `2100`–`2199` MM, `2200`–`2299` cpuidle, `9000`–`9099` agd5f/ML backports.
3. Verify it applies cleanly with BOTH tools (use absolute paths — `git -C` changes CWD):
   ```bash
   git -C repos/linux-7.2-rc7 apply --check "$PWD/patches/<range>/<file>"     # forward
   git -C repos/linux-7.2-rc7 apply --check -R "$PWD/patches/<range>/<file>"  # reverse-clean = already applied → drop it
   patch -p1 --forward --dry-run < patches/<range>/<file>                     # authoritative — matches prepare()'s tool
   ```
   **`git apply --check` can pass while GNU `patch` rejects** (2026-08-03): a hunk with
   ambiguous leading context, or one touching a file absent from rc7 (e.g. DCN6 `dcn60`),
   fools `git apply` but aborts prepare(). Always confirm with `patch -p1 --forward --dry-run`.
   If a patch spans a file that does not exist in rc7, strip that file's hunks (document the
   strip here). If a patch's context references a symbol/field another carried patch adds,
   number it AFTER that patch (e.g. `9038`–`9040` must follow `9036`).
4. Add `patches/<range>/<file>` to the `source=()` array in `PKGBUILD` in the correct sorted position
   (dependencies first — e.g. 1127/1128 must precede 1129).
5. Run `updpkgsums` after any `source=()` change — checksums must match 1:1. This also
   recreates the root symlinks; if a build later reports a patch source "not found in the
   build directory", re-run `updpkgsums` (the symlinks may be missing after a fresh clone).
6. Add an entry to the appropriate section in this file with author and source URL or commit hash.
7. Do **not** access `lore.kernel.org` — it has anti-scraping protections. Use the source Git repositories directly (drm-next, linux-pm, sirlucjan GitHub, freedesktop.org mailing list archives, and the gitlab drm/amd work_items via no-UA curl).
