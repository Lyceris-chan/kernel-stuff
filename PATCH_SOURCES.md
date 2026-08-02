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

Hand-written local fixes for this specific Zen 4 + RDNA 4 build, produced with Antigravity AI. Formerly numbered `ai01`–`ai13`; the mapping is shown below.

| File | Former | Author | Description |
|------|--------|--------|-------------|
| `0001-drm-amd-pm-Fix-typo-in-smu_v14_0_set_irq_state.patch` | `ai01` | Antigravity | Fix typo in `smu_v14_0_set_irq_state` (SMU14 IRQ `type` parameter) |
| `0002-drm-amd-pm-Fix-memory-leaks-in-smu_v14_0_fini_smc_ta.patch` | `ai02` | Antigravity | Fix memory leak in `smu_v14_0_fini_smc_tables` |
| `0003-drm-amd-pm-Allow-PROFILE_PEAK-GFXCLK-ceiling-to-floa.patch` | `ai03` | Antigravity | Let GFXCLK ceiling float in PROFILE_PEAK on SMU14 |
| `0004-drm-amd-pm-Disable-deep-sleep-in-PROFILE_PEAK.patch` | `ai04` | Antigravity | Disable GPU deep sleep (GFXOFF) in PROFILE_PEAK. **v4** (2026-08-02): deep sleep is now a deterministic function of the forced level (enabled for every level except `PROFILE_PEAK`, tested once after the clock-range switch, so leaving PEAK restores deep sleep unconditionally); the `smu_v14_0_deep_sleep_control()` return value is checked and propagated; the deep-sleep toggle is skipped entirely while `PP_SMC_POWER_PROFILE_COMPUTE` is the active workload mode so it never clobbers `set_power_profile_mode()`'s independent COMPUTE handling |
| `0005-drm-amd-pm-Disable-SMU14-mode1-reset-for-SR-IOV.patch` | `ai05` | Antigravity | Disable SMU14 mode1 reset under SR-IOV |
| `0006-drm-amd-pm-Add-bounds-checking-for-SMU14-I2C-command.patch` | `ai06` | Antigravity | Add bounds checking to SMU14 I2C commands |
| `0007-drm-amd-pm-Remove-redundant-mutex-lock-in-SMU14-I2C-.patch` | `ai07` | Antigravity | Remove redundant mutex lock in SMU14 I2C update |
| `0008-drm-amd-pm-Fix-SMU14-power-limit-reporting-logic.patch` | `ai13` | Sleepy / Antigravity | Fix SMU14 power limit reporting logic (unlock maximum PPT) |

`0010-drm-amdgpu-gfx12-Fix-named-barrier-restore-in-trap-handler.patch` — upstream amd-gfx, **Jay Cornwall**, "drm/amdkfd: Fix named barrier restore in gfx12.1 trap handler", Message-ID `<20260706220043.612554-1-jay.cornwall@amd.com>`.

~~`0009`~~ (gfx12 disallow-GFXOFF around GPU reset) — **DROPPED** 2026-08-02: `gfx_v12_0_reset_kgq` was completely reworked by the `gfx12: recover gfx user queues on priv-fault` series landed in rc5; the new function hardcodes `use_mmio = false`, making the GFXOFF guard dead code. Superseded.

### 0030–0034 — Local display patches

| File | Former | Author | Description |
|------|--------|--------|-------------|
| `0030-drm-amd-display-Proactively-shrink-DET-for-pipes-los.patch` | `ai08` | Antigravity | Proactively shrink DET for pipes losing bandwidth |
| `0031-drm-amd-display-Fix-memory-leak-in-DCN20-link-encode.patch` | `ai09` | Antigravity | Fix memory leak in DCN20 link encoder resource init |
| `0032-drm-amd-display-Fix-OOB-array-access-for-HPO-FRL-lin.patch` | `ai10` | Antigravity | Fix OOB array access in HPO FRL link encoder |
| `0033-drm-amd-display-Fix-missing-HPO-FRL-link-encoder-reg.patch` | `ai11` | Antigravity | Fix missing HPO FRL link encoder register init |
| `0034-drm-amd-display-Prevent-memory-leak-during-IRQ-servi.patch` | `ai12` | Antigravity | Prevent memory leak during IRQ service destroy |

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

## 1000–1019 — AMDGPU GPU core

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

---

## 1100–1111 — AMD display

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

~~`1112`~~ (`334cbfa3c`, dcn401 GPIO lookup tables) — **DROPPED**: requires `DC_GPIO_GENERIC_A`/`DC_GPIO_HPD_A` type defs from a prerequisite GPIO infrastructure patch not in rc5.

Only `1101` is reverse-applied in `prepare()` (PKGBUILD line 551). If you renumber patches, update that reverse-apply line to match the current filename.

---

## 1200–1213 — AMD Power Management

### 1200–1203 — amd-pstate EPP boost series (David Vernet, RFC)

| File | Message-ID | Subject |
|------|------------|---------|
| `1200` | `20260728073150.54964-2` | cpufreq/amd-pstate: Document missing kernel-doc members |
| `1201` | `20260728073150.54964-3` | cpufreq/amd-pstate: Update cppc_req_cached before writing the MSR |
| `1202` | `20260728073150.54964-4` | cpufreq/amd-pstate: Add per-core EPP boost for recently-busy CPUs |
| `1203` | `20260728073150.54964-5` | Documentation: amd-pstate: Document the epp_boost parameter |

### 1204–1210 — amd-pstate fixes (upstream series 1/7–7/7)

| File | Author | Subject |
|------|--------|---------|
| `1204` | Rong Zhang | cpufreq/amd-pstate: Bail out early if !X86_FEATURE_HW_PSTATE |
| `1205` | Qianheng Peng | cpufreq: amd-pstate-ut: Skip tests when amd-pstate driver is not active |
| `1206` | Marco Scardovi | cpufreq/amd-pstate: Fix EPP return type and handle errors during initialization |
| `1207` | Marco Scardovi | cpufreq/amd-pstate: Toggle auto_sel in active mode on shared memory systems |
| `1208` | Marco Scardovi | cpufreq/amd-pstate: Cache the firmware programmed EPP value |
| `1209` | EDAMAMEX | cpufreq/amd-pstate: handle missing policy in dynamic EPP callbacks |
| `1210` | Mario Limonciello | cpufreq/amd-pstate: Loosen requirement on lowest nonlinear frequency != min freq |

### 1211–1213 — ACPI CPPC / cpufreq-cppc fixes (backported from post-rc5 mainline, added 2026-08-02)

| File | Commit | Author | Subject |
|------|--------|--------|---------|
| `1211` | `9753c0ab8` | Christian Loehle | cpufreq: cppc: Sanitize lockless policy limit snapshots |
| `1212` | `11055a46f` | Christian Loehle | ACPI: CPPC: Check all controls for fast switching |
| `1213` | `47d4e945d` | Christian Loehle | ACPI: CPPC: Skip writes to unsupported performance controls |

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
| `2100` | `zstd-dev-patches/` | Piotr Gorski | zstd-7.2: merge changes from dev tree (formerly `1400`) |
| `2101` | `lru-marie-patches-v12/` | Piotr Gorski | mm-7.2: introduce LRU MARIE v12 (formerly `1401`; `vma_flags` fix baked in) |

## 2200 — CPU idle (NAP governor)

| File | Source | Author | Subject |
|------|--------|--------|---------|
| `2200` | `repos/sirlucjan-kernel-patches/7.2-rc/nap-patches/` | Masahito S (firelzrd) | 7.2-nap-v0.5.0 (formerly `1500`) |

**IMPORTANT**: NAP is sourced from sirlucjan's `nap-patches/` directory, **not** from firelzrd's repo. Verified 2026-08-02: `repos/firelzrd-bore-scheduler/` contains only BORE scheduler patches (`patches/stable/`, `patches/testing/` have no `nap-patches` dir).

---

## 9000–9007 — agd5f staging backports

Source: `git clone --shallow-since="2026-06-01" https://gitlab.freedesktop.org/agd5f/linux.git repos/agd5f-linux`. Formerly numbered `2000`–`2007`.

| File | Commit | Author | Subject |
|------|--------|--------|---------|
| `9000` | `8419331e64d9` | Leo Li | drm/amd/display: Exit idle optimizations before programming — v2 revision (checkpatch-fixed, `Cc: stable`), applied through the normal patch loop |
| `9001` | `70a5cb5d2` | Alex Deucher | drm/amdgpu/gfx12: drop all BUG()s |
| `9002` | `0238fd8a2` | Alex Deucher | drm/amdgpu/gfx12.1: drop all BUG()s |
| `9003` | `d9e6b531b` | Alex Deucher | drm/amdgpu/psp14: replace BUG() with an error |
| `9004` | `c54f8d7af` | Yang Wang | drm/amd/pm: use milliwatts for GPU power sensors |
| `9005` | `39866e3d3` | Candice Li | drm/amdgpu: restore UMD profile pstate after runtime resume |
| `9006` | `58b53f58e` | Timur Kristóf | drm/amdgpu/ttm: Use more optimal copy packet sizes for copy and fill |
| `9007` | `402ebe22b267` | Alex Deucher | drm/gfx12: Program DB_RING_CONTROL |

Dropped candidates (formerly `2008`/`2009`): Jesse Zhang `47862766d211` (gfx12 userq error interrupts) and Lijo Lazar `d1331c7d89b8` (SMUv14 pptable helper) — both reference agd5f staging symbols absent from mainline rc5. Do not re-add until the staging infrastructure lands.

---

## 2026-08-02 sweep results

Checked and **not added** — already in rc5 (verified `git apply --check -R` clean against `repos/linux-7.2-rc5`):

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

## Adding new patches

1. Place the patch file in the root of this repository.
2. Use the correct numeric prefix (see the conventions table): `0001`–`0099` local/upstream display, `0101`–`0109` CachyOS (squashed per branch), `1000`–`1099` GPU core, `1100`–`1199` display, `1200`–`1299` PM, `2000`–`2099` block, `2100`–`2199` MM, `2200`–`2299` cpuidle, `9000`–`9099` agd5f.
3. Verify it applies cleanly: `git -C repos/linux-7.2-rc5 apply --check <file>`. To test whether a patch is already applied, use the reverse check `git -C repos/linux-7.2-rc5 apply --check -R <file>` (clean output = already applied).
4. Add the filename to the `source=()` array in `PKGBUILD` in the correct sorted position.
5. Run `updpkgsums` after any `source=()` change — checksums must match 1:1.
6. Add an entry to the appropriate section in this file with author and source URL or commit hash.
7. Do **not** access `lore.kernel.org` — it has anti-scraping protections. Use the source Git repositories directly (drm-next, linux-pm, sirlucjan GitHub, freedesktop.org mailing list archives).
