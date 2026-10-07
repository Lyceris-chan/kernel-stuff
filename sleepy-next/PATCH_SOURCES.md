# sleepy-next: patch provenance

Provenance for every patch in `source=()` of `sleepy-next/PKGBUILD`.

- **Base:** Linux `v7.3-rc3`
- **Series:** 217 patches
- **Companion documents:** `../CHANGELOG.md` records what changed in each
  release. `../LESSONS.md` records the traps. The authoritative range-to-source
  table is in the `patch-audit` skill.

The patch index is generated from the patch headers. Where a patch came from a
git branch the identifier is a commit hash; where it came from a mailing list it
is the submission `Message-ID`. Patches whose own header carried no usable
identifier had their original submission recovered from the lore git mirrors and
are supplied by the generator instead, so every row below has a source.

## Series at a glance

| Range | Category | Patches |
|---|---|---|
| `0001–0049` | Handmade local | 12 |
| `0050–0099` | EDID and display mailing-list patches | 5 |
| `0101–0113` | CachyOS branch squashes | 5 |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | 18 |
| `1100–1199` | AMD display (DCN4, colorops) | 18 |
| `1200–1299` | AMD power management (amd-pstate, CPPC) | 26 |
| `2000–2099` | Block, I/O, buffers and network (bfq, mq-deadline, zram, io_uring, r8169) | 41 |
| `2100–2199` | Memory management and swap (zstd, LRU-MARIE, gup, zswap) | 51 |
| `2200–2299` | CPU idle (NAP governor) | 1 |
| `2300–2399` | Build system and kbuild | 20 |
| `2400–2499` | Core scheduler and sched-ext | 4 |
| `2500–2599` | x86 and arch core | 1 |
| `2600–2699` | Time and timers | 0 |
| `9000–9099` | agd5f staging + userq lifecycle backports | 41 |

**A resolved numbering collision:** two patches used to share the number
`1140` — Tom Chung's clamp of `force_min_dcfclk` to the dcn42b range (still
`1140`) and James Lin's fallback to an overlay cursor on dcn4x, which was
renumbered to `1165` in the rc3-9 cycle (2026-09-15).

## Patch index
| Patch | Subject | Author | Date | Upstream id |
|---|---|---|---|---|
| `0001` | drm/amd/pm: Fix typo in smu_v14_0_set_irq_state | Sleepy | 2026-07-01 | `b0f38302d5be` |
| `0002` | drm/amd/pm: Fix memory leaks in smu_v14_0_fini_smc_tables | Sleepy | 2026-07-01 | `f80ef62e0eec` |
| `0003` | drm/amd/pm: let GFXCLK ceiling float in PROFILE_PEAK on SMU14 | Sleepy | 2026-07-30 | `860bc6db0fcb` |
| `0004` | drm/amd/pm: Disable deep sleep in PROFILE_PEAK | Sleepy | 2026-07-30 | `3c8e4d101234` |
| `0005` | drm/amd/pm: Disable SMU14 mode1 reset for SR-IOV | Sleepy | 2026-07-01 | `680124f219d2` |
| `0006` | drm/amd/pm: Add bounds checking for SMU14 I2C commands | Sleepy | 2026-07-01 | `882e8148ae7e` |
| `0007` | drm/amd/pm: Remove redundant mutex lock in SMU14 I2C update | Sleepy | 2026-07-01 | `7ceb7ab7c86f` |
| `0010` | drm/amdkfd: Fix named barrier restore in gfx12.1 trap handler | Jay Cornwall | 2026-07-06 | `20260706220043.612554-1-jay.cornwall@amd.com` |
| `0031` | drm/amd/display: Fix memory leak in DCN20 link encoder creation | Sleepy | 2026-07-01 | `42f8da1167d8` |
| `0032` | drm/amd/display: Fix OOB array access for HPO FRL link encoder | Sleepy | 2026-07-01 | `d8aa0fbd0493` |
| `0033` | drm/amd/display: Fix missing HPO FRL link encoder register init | Sleepy | 2026-07-01 | `a4d4d2c0a220` |
| `0034` | drm/amd/display: Prevent memory leak during IRQ service destroy | Sleepy | 2026-07-01 | `33a065acb38a` |
| `0050` | drm/edid: Parse AMD VSDB for FreeSync refresh range | Alex Huang | 2026-08-04 | `20260804143339.714548-2-Alex.Huang2@amd.com` |
| `0055` | drm/edid: add the HDMI VRR capability struct without enabling the parse | Fangzhi Zuo (struct-only strip by Sleepy) | 2026-07-30 | `20260730171754.704049-2-jerry.zuo@amd.com` |
| `0058` | drm/amd/display: restore FRL cap on non-destructive HDMI link verify | Fangzhi Zuo | 2026-07-30 | `20260730205047.1016922-1-jerry.zuo@amd.com` |
| `0059` | drm/amd/display: Add 2.1 FreeSync support for AMD VSDB EDID Block | Fangzhi Zuo | 2026-08-26 | `150622@lists.freedesktop.org` |
| `0061` | drm/amd/display: Enable HDMI ALLM for Gaming-VRR | Fangzhi Zuo | 2026-08-26 | `150621@lists.freedesktop.org` |
| `0101` | cachyos-bbr3: BBRv3 TCP congestion control (2 patches) | squash | 2026-08-02 | `55d248b79ea1` |
| `0102` | cachyos-kbuild: Allow -O3 (kbuild branch) | squash | 2026-08-02 | `35f22c56b3f3` |
| `0103` | cachyos-cpu-isa: x86_64 Zen4 ISA optimizations | squash | 2026-08-02 | `0a24926402c8` |
| `0110` | cachy: CONFIG_CACHY config hooks (curated backport) | Eric Naim | 2026-03-25 | `16cd15654cc6` |
| `0111` | ACPI: processor: Disable bus master check for AMD | Sultan Alsawaf | 2025-08-26 | `14f3669dd743` |
| `0112` | drm/amd: Avoid evicting resources at S5 | "Mario Limonciello (AMD)" <superm1@kernel.org> | 2025-09-09 | `575943925bac` |
| `1004` | drm/amdgpu/gmc9: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `043453a07452` — **REMOVED 2026-09-23** |
| `1005` | drm/amdgpu/gmc10: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `ebfc4cbbb580` — **REMOVED 2026-09-23** |
| `1006` | drm/amdgpu/gmc11: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `a1efda0bc2ee` — **REMOVED 2026-09-23** |
| `1007` | drm/amdgpu/gmc12: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `48026ef6756e` |
| `1008` | drm/amdgpu: add an buffer funcs callback for TLB invalidation | Alex Deucher | 2026-07-13 | `7b5120c066ad` |
| `1009` | drm/amdgpu/sdma5.0: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `c7a9aad03f6c` — **REMOVED 2026-09-23** |
| `1010` | drm/amdgpu/sdma5.2: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `a461b17a3fec` — **REMOVED 2026-09-23** |
| `1011` | drm/amdgpu/sdma6: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `748c1927ec4e` — **REMOVED 2026-09-23** |
| `1012` | drm/amdgpu/sdma7: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `4481ee06e2a3` |
| `1013` | drm/amdgpu: add core helper to do TLB invalidation via SDMA | Alex Deucher | 2026-07-13 | `1d5a9fb3dc8c` |
| `1014` | drm/amdgpu/gmc: add more gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `14a0ecfb5c9d` |
| `1015` | drm/amdgpu/gmc10: switch to new gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `497621ee93de` — **REMOVED 2026-09-23** |
| `1016` | drm/amdgpu/gmc11: switch to new gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `2ba771d6669d` — **REMOVED 2026-09-23** |
| `1017` | drm/amdgpu/gmc12: switch to new gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `929f98010c17` |
| `1018` | drm/amdgpu: Switch order of GC and Display IP blocks | Matthew Stewart | 2026-07-16 | `efc5353500f1` |
| `1026` | drm/amdkfd: fix NULL pointer dereference in GFX12 CRIU queue restore | Vladimir Marioukhine | 2026-08-04 | `SA1PR12MB8600E8B1821FA7D76923FC259FD42@SA1PR12MB8600.namprd12.prod.outlook.com` |
| `1027` | drm/amdgpu: force complete the MES scheduler ring fence on reset | Jesse Zhang | 2026-08-06 | `20260806075653.711275-1-Jesse.Zhang@amd.com` |
| `1055` | drm/amd/pm: Fix incorrect avg vcn utilization in gpu_metrics | Boqun Feng | 2026-08-05 | `20260805140227.44868-1-boqun@kernel.org` |
| `1056` | drm/sched: Lock drm_sched_entity_is_idle() | Philipp Stanner | 2026-08-13 | `0e118b936dc5` |
| `1058` | drm/amdgpu: Track suboptimal always-valid BOs in soft-evicted state | Natalie Vock | 2026-04-14 | `eb1170e956c4` |
| `1060` | drm/amdgpu: cancel hang_detect_work before taking userq_mutex | vitaly.prosyak at amd.com | 2026-08-27 | `20260827222531.127950-1-vitaly.prosyak@amd.com` |
| `1061` | drm/ttm: fix swapped-out resources never leaving their bulk_move range | Vadim Nikitushkin | 2026-09-09 | `20260909205028.13799-1-bub4z0r@gmail.com` |
| `1062` | dma-buf/dma-fence: fix checking signaling bit for timeline and driver name | Christian König | 2026-09-09 | `20260909131808.2201-2-christian.koenig@amd.com` |
| `1063` | drm/sched: document the RCU dependency | Christian König | 2026-09-09 | `20260909131808.2201-3-christian.koenig@amd.com` |
| `1064` | drm/amdgpu: don't release the fence reference consumed by the scheduler | Donggeun Yoo | 2026-09-10 | `20260910054551.634054-1-donggeunyoo.kernel@gmail.com` |
| `9062` | drm/amdgpu: introduce amdgpu_lookup_queue_by_doorbell | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-2-lingshan.zhu@amd.com` |
| `9063` | drm/amdgpu: keep the userq manager alive as long as its queues | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-3-lingshan.zhu@amd.com` |
| `9064` | drm/amdgpu/gfx11: hold userq refs in private fault worker | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-4-lingshan.zhu@amd.com` — **REMOVED 2026-09-23** |
| `9065` | drm/amdgpu/gfx12: hold userq refs in private fault worker | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-5-lingshan.zhu@amd.com` |
| `9066` | drm/amdgpu: implement asynchronous userq destruction routine | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-6-lingshan.zhu@amd.com` |
| `9067` | drm/amdgpu: hold userq kref in MES reset | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-7-lingshan.zhu@amd.com` |
| `9068` | drm/amdgpu: hold userq kref during isolation scheduling | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-8-lingshan.zhu@amd.com` |
| `9069` | drm/amdgpu: hold userq kref during suspend and resume | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-9-lingshan.zhu@amd.com` |
| `9070` | drm/amdgpu: free userq by kref_put when fails to create | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-10-lingshan.zhu@amd.com` |
| `9071` | drm/amdgpu: take queue kref in userq_create to avoid UAF | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-11-lingshan.zhu@amd.com` |
| `9072` | drm/amdgpu/sdma: add detect_hung_queue callback | Jesse Zhang | 2026-09-03 | `972a8cd8fba1` |
| `9073` | drm/amdgpu/sdma6: implement detect_hung_queue | Jesse Zhang | 2026-09-03 | `994dea375802` — **REMOVED 2026-09-23** |
| `9074` | drm/amdgpu/sdma7: implement detect_hung_queue | Jesse Zhang | 2026-09-03 | `ba07df579939` |
| `9075` | drm/amdgpu/userq: reset a hung SDMA user queue over MMIO | Jesse Zhang | 2026-09-03 | `10a6760a1a64` |
| `1135` | drm/amd/display: fix HPD program filter programming | Charlene Liu | 2026-08-05 | `20260805063937.2145774-13-chiahsuan.chung@amd.com` — **REMOVED 2026-09-23** |
| `1136` | drm/amd/display: Update and revert FRL LT Timeout | Relja Vojvodic | 2026-08-05 | `20260805063937.2145774-21-chiahsuan.chung@amd.com` |
| `1138` | drm/amd/display: pull colorops into state when recreating a plane | Harry Wentland | — | `20260825153539.213495-1-harry.wentland@amd.com` |
| `1140` | drm/amd/display: clamp force_min_dcfclk to dcn42b range | Tom Chung | 2026-08-05 | `20260805063937.2145774-11-chiahsuan.chung@amd.com` |
| `1165` | drm/amd/display: fall back to overlay cursor on dcn4x when top plane doesn't fill CRTC | James Lin | — | `20260818202139.4172592-2-IVAN.LIPSKI@amd.com` |
| `1166` | drm/amd/display: Return success status from check_mode_supported | Alvin Lee (DC 3.2.398, posted by Chenyu Chen) | 2026-09-08 | `20260908113338.2433445-60-chen-yu.chen@amd.com` |
| `1141` | drm/amd/display: skip receiver power control without AUX | "NepNep7601" | 2026-08-27 | `20260826204457.4666-1-neptune@imm0nv1nhtv.is-a.dev` |
| `1142` | drm/amd/display: close DDC on I2C engine setup failure | "NepNep7601" | 2026-08-27 | `20260826204457.4666-2-neptune@imm0nv1nhtv.is-a.dev` |
| `1143` | drm/amd/display: fall back to software I2C on hardware engine failure | "NepNep7601" | 2026-08-27 | `20260826170549.21985-1-neptune@imm0nv1nhtv.is-a.dev` |
| `1150` | drm: Add passive_vrr properties for passive/desktop VRR | Tomasz Pakuła | 2026-09-01 | `21311d5b6fd4` |
| `1151` | drm/amd/display: Use passive_vrr properties in amdgpu | Tomasz Pakuła | 2026-09-01 | `1508cfd62df5` |
| `1152` | drm/amd/display: Emit VTEM for HF-VSDB VRR on TMDS links | Fangzhi Zuo | 2026-08-20 | `fabf2169cb45` |
| `1154` | drm/amd/display: Fix NULL deref of new_stream->sink in VTEM guard | Fangzhi Zuo | 2026-08-31 | `a69d7c8a99b4` |
| `1158` | drm/amd/display: Fix high busy wait load in dmub_srv_wait_for_idle() | Sultan Alsawaf | 2025-08-25 | `dfd0e5aa6aad` |
| `1159` | drm/amd/display: Atomize IRQ register read/modify/write ops | Chenyu Chen | 2026-09-08 | `20260908113338.2433445-59-chen-yu.chen@amd.com` |
| `1161` | drm/amd/display: Guard NULL DDC pins in dal_ddc_open | Dennis Thomsen | 2026-08-31 | `20260831194926.274044-1-dennis.fich.thomsen@gmail.com` |
| `1162` | drm/amd/display: check dc_state_create_copy() for NULL in dm_suspend | Jiangshan Yi | 2026-09-04 | `20260904091817.578894-1-yijiangshan@kylinos.cn` |
| `1163` | drm/amd/display: keep freesync_capable for HF-VSDB VRR sinks in MCCS fallback | Fangzhi Zuo | 2026-09-01 | `20260901191251.2653684-4-jerry.zuo@amd.com` |
| `1164` | Revert "drm/amd/display: Consult MCCS FreeSync cap only if requested & supported" | Sleepy (revert of upstream cfdcf5571c31, orig. Michel Dänzer) | 2026-09-15 | upstream commit `cfdcf5571c3107bf636002fc0c16ce93c19bd671` |
| `1201` | cpufreq/amd-pstate: Update cppc_req_cached before writing the MSR | David Vernet | 2026-07-28 | `20260728073150.54964-3-void@manifault.com` |
| `1202` | cpufreq/amd-pstate: Add per-core EPP boost for recently-busy CPUs | David Vernet | 2026-07-28 | `20260728073150.54964-4-void@manifault.com` |
| `1203` | Documentation: amd-pstate: Document the epp_boost parameter | David Vernet | 2026-07-28 | `20260728073150.54964-5-void@manifault.com` |
| `1210` | ACPI: CPPC: Validate the _CPC package header | Christian Loehle | 2026-08-27 | `20260827063100.2741066-2-christian.loehle@arm.com` |
| `1211` | ACPI: CPPC: Validate _CPC entry and control semantics | Christian Loehle | 2026-08-27 | `20260827063100.2741066-3-christian.loehle@arm.com` |
| `1212` | ACPI: CPPC: Propagate performance-control write errors | Christian Loehle | 2026-08-27 | `20260827063100.2741066-4-christian.loehle@arm.com` |
| `1213` | ACPI: CPPC: Use 64-bit masks for register fields | Christian Loehle | 2026-08-27 | `20260827063100.2741066-5-christian.loehle@arm.com` |
| `1214` | ACPI: CPPC: Serialize PCC single-register payload updates | Christian Loehle | 2026-08-27 | `20260827063100.2741066-6-christian.loehle@arm.com` |
| `1215` | ACPI: CPPC: Serialize PCC EPP payload updates | Christian Loehle | 2026-08-27 | `20260827063100.2741066-7-christian.loehle@arm.com` |
| `1216` | ACPI: CPPC: Release CPC descriptors through kobject | Christian Loehle | 2026-08-27 | `20260827063100.2741066-8-christian.loehle@arm.com` |
| `1217` | ACPI: CPPC: Release PCC data after probe failures | Christian Loehle | 2026-08-27 | `20260827063100.2741066-9-christian.loehle@arm.com` |
| `1218` | ACPI: CPPC: Reject unsafe cross-CPU SystemMemory RMW | Christian Loehle | 2026-08-27 | `20260827063100.2741066-10-christian.loehle@arm.com` |
| `1219` | ACPI: CPPC: Reject direct reads of write-only controls | Christian Loehle | 2026-08-27 | `20260827063100.2741066-11-christian.loehle@arm.com` |
| `1220` | ACPI: CPPC: Validate and access PCC register layouts | Christian Loehle | 2026-08-27 | `20260827063100.2741066-12-christian.loehle@arm.com` |
| `1221` | ACPI: CPPC: Validate SystemIO register layouts | Christian Loehle | 2026-08-27 | `20260827063100.2741066-13-christian.loehle@arm.com` |
| `1222` | ACPI: CPPC: Validate PCC overlaps across processors | Christian Loehle | 2026-08-27 | `20260827063100.2741066-14-christian.loehle@arm.com` |
| `1223` | ACPI: CPPC: Validate SystemIO overlaps across processors | Christian Loehle | 2026-08-27 | `20260827063100.2741066-15-christian.loehle@arm.com` |
| `1224` | ACPI: CPPC: Clear Performance Limited without a stale read | Christian Loehle | 2026-08-27 | `20260827063100.2741066-16-christian.loehle@arm.com` |
| `2000` | block/mq-deadline: pass in queue directly to dd_insert_request() | Jens Axboe | 2024-01-19 | `57c8b2fceb33` |
| `2001` | block/mq-deadline: skip expensive merge lookups if contended | Jens Axboe | 2024-01-19 | `580f9800f5ea` |
| `2002` | block/bfq: pass in queue directly to bfq_insert_request() | Jens Axboe | 2024-01-20 | `c1c6f8f174e1` |
| `2003` | block/bfq: serialize request dispatching | Jens Axboe | 2024-01-20 | `a0ec4351418e` |
| `2004` | block/bfq: skip expensive merge lookups if contended | Jens Axboe | 2024-01-20 | `e6a57788416f` |
| `2005` | sched_ext: Skip per-CPU data allocation for built-in DSQs | Qiurong Fang | 2026-08-27 | `20260827082329.3368255-1-fangqiurong@kylinos.cn` |
| `2006` | zram: convert to SG-list zsmalloc object read API | Sergey Senozhatsky | 2026-09-07 | `abaa6b12ca8a` |
| `2007` | zsmalloc: remove old object read API | Sergey Senozhatsky | 2026-09-07 | `f2ae543ebcc5` |
| `2008` | io_uring/io-wq: stop a single cancel after one running match | Mark Amirkan via B4 Relay | 2026-09-13 | `20260913-b4-send-io-wq-cancel-v1-1-dcfe47275c6e@gmail.com` |
| `2009` | fs/buffer: check for NULL pointer before folio_test_dropbehind() | Zhaoyu Liu | 2026-09-13 | `pfk6l6lsgecie4xwy5njrgtzpave4uayxbl4lkz3iekcdds7fg@bpihjzlnz7m2` |
| `2010` | blk-cgroup: save IRQ state in blkg_tryget_closest() | Hao Zhang | 2026-09-12 | `aqQmqb1k57PXj8Ef@192.168.1.215` |
| `2011` | r8169: don't enable chip LTR when the platform has not enabled LTR | Yogesh Gaur | 2026-09-14 | `20260914130050.304-1-yogeshgaur.83@gmail.com` |
| `2012` | block: skip redundant flush for O_DSYNC direct writes | Zhenxian Ma | 2026-08-15 | `bec7d36a6514` |
| `2013` | block: only use REQ_FUA for direct writes if the device supports it | Zhenxian Ma | 2026-08-15 | `0d492f40c4ad` |
| `2100` | zstd-7.3: merge v1.6.0 into kernel tree | Piotr Gorski | 2026-09-14 | `e0f9795534f4` |
| `2101` | linux7.3-rc1-lru_marie-0.11.1r2 | Masahito S | 2026-09-15 | `10c0c0872c91` |
| `2120` | mm/gup: break out gup_fill_pages() helper | Rik van Riel | 2026-08-10 | `7afdec79e9f0` |
| `2121` | mm/gup: convert follow_page_mask() to return a long | Rik van Riel | 2026-08-10 | `b283884f04a2` |
| `2122` | mm/gup: split follow_page_pte_commit() out of follow_page_pte() | Rik van Riel | 2026-08-10 | `9fbdbf16c239` |
| `2123` | mm/gup: break out follow_one_pte() helper | Rik van Riel | 2026-08-10 | `d71a0f5b585f` |
| `2124` | mm/gup: fill the pages array outside the pud/pmd lock | Rik van Riel | 2026-08-10 | `d317aafdbc4a` |
| `2125` | mm/gup: return a huge page's full count from follow_page_mask() | Rik van Riel | 2026-08-10 | `ef7d0a878a6e` |
| `2126` | mm/gup: walk multiple PTEs per follow_page_pte() call | Rik van Riel | 2026-08-10 | `053ce5bc0ed8` |
| `2127` | mm/gup: batch contiguous same-folio PTEs into one refcount grab | Rik van Riel | 2026-08-10 | `6c2092bc8448` |
| `2129` | zstd: skip the BMI2 probe when dynamic BMI2 dispatch is disabled | Usama Arif | 2026-08-26 | `20260826122558.2662013-3-usama.arif@linux.dev` |
| `2130` | zstd: probe the CPU for BMI2 support only once | Usama Arif | 2026-08-26 | `20260826122558.2662013-4-usama.arif@linux.dev` |
| `2131` | mm/mglru: separate folio generation update from LRU accounting | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `54e9345e4563` — **REMOVED 2026-09-23** |
| `2132` | mm/mglru: batch update lrugen->nr_pages in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `521a7c952c89` — **REMOVED 2026-09-23** |
| `2133` | mm/mglru: enhance cold/hot inversion handling in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `3384a49a865e` — **REMOVED 2026-09-23** |
| `2134` | mm/mglru: exclude folios promoted by aging from protected in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `e25d6c041ca0` — **REMOVED 2026-09-23** |
| `2135` | mm/mglru: make LRU folio prefetch helper an inline function | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `efac6d51d1d6` — **REMOVED 2026-09-23** |
| `2136` | mm/mglru: move folios from oldest gen to second-oldest gen from head to tail | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `81cb06a097b3` — **REMOVED 2026-09-23** |
| `2137` | mm/mglru: batch move folios to the second-oldest gen's LRU | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `64fff1e3d929` — **REMOVED 2026-09-23** |
| `2138` | memcg: trim the per-cpu charge stock instead of draining it | Shakeel Butt | 2026-08-19 | `20260820012010.2016086-1-shakeel.butt@linux.dev` |
| `2139` | mm: vmscan: avoid anon scanning for GFP_NOIO with low swapcache | Bo Zhang | 2026-09-08 | `09c1d29a3d1e` |
| `2140` | mm/page_alloc: avoid direct compaction for costly __GFP_NORETRY allocations | Salvatore Dipietro | 2026-09-11 | `60adb47f4fa3` |
| `2141` | mm: filemap: retain mapped dropbehind folios | Wenjie Qi | 2026-08-30 | `848d2ce2fce1` |
| `2171` | mm/vmscan: avoid pointless large folio splits without swap | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-08-30 | `bd7fcb0dea86` |
| `2172` | mm: vmalloc: fix vmap_purge_lock livelock under memory pressure | Ye Liu | 2026-08-28 | `6c06fec56a63d` |
| `2144` | xarray: fix index jumping backwards in xas_find() | Krystian Kaniewski | 2026-09-04 | `5fe684a7cd8e` |
| `2145` | mm/vma: correctly unaccount on mmap_prepare() failure | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-02 | `6cc27d821963` |
| `2146` | mm/mlock: use the IRQ-safe accessor for NR_MLOCK in __munlock_folio() | Shakeel Butt | 2026-09-01 | `e14a34548064` |
| `2147` | mm/memcg: clear folio memcg after changing per memcg stats | Bingfang Guo | 2026-09-10 | `f245cf82e158` |
| `2148` | crypto: zstd - Avoid redundant cstream initialization | Usama Arif | 2026-08-25 | `20260825220616.3842633-2-usama.arif@linux.dev` |
| `2149` | crypto: zstd - Avoid redundant dstream initialization | Usama Arif | 2026-08-25 | `20260825220616.3842633-3-usama.arif@linux.dev` |
| `2150` | mm/huge_memory: fix pgtable withdrawal for huge zero PMDs | Lance Yang | 2026-09-13 | `ac63e1b4d2a2` |
| `2151` | mm: shmem: ignore sysfs configs for shmem forced collapse | Baolin Wang | 2026-09-14 | `1538a25f38cf` |
| `2152` | khugepaged: hold invalidate_lock across collapse_file() readahead | Nguyen Ngoc Thang | 2026-09-13 | `1be399d378b7` |
| `2153` | writeback: report a Tasks-RCU quiescent state per cgwb drain pass | Josef Bacik | 2026-09-09 | `6495bf0e43d6` |
| `2154` | mm/page_alloc: apply per-task GFP context in bulk allocator | Qiqi Liu | 2026-09-14 | `afd44a6aa48e` |
| `2155` | mm: xswap support for zswap | Chris Li | 2026-09-16 | `xswap-patches-v2-sep/0001` |
| `2156` | mm, swap: add CONFIG_XSWAP and xswap fields to | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0002` |
| `2157` | mm, swap: refactor free_swap_cluster_info to take | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0003` |
| `2158` | mm, swap: add xswap cluster grow via VM_SPARSE vmalloc | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0004` |
| `2159` | mm, swap: add sysfs create interface for xswap | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0005` |
| `2160` | mm, swap: add xswap grow trigger on cluster allocation | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0006` |
| `2161` | mm, swap: add xswap_try_shrink and shrink trigger on | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0007` |
| `2162` | mm, swap: free backing pages in xswap_unmap_clusters | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0008` |
| `2163` | mm, swap: defer xswap shrink to workqueue to avoid lock | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0009` |
| `2164` | mm, swap: refactor swapoff and add xswap_destroy | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0010` |
| `2165` | mm, swap: require zswap for xswap devices | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0011` |
| `2166` | mm, swap: cap xswap growth at nr_clusters | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0012` |
| `2167` | mm, swap: add sysfs per-device size limit for xswap | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0013` |
| `2168` | mm, swap: shrink xswap to the ceiling when it drops | Baoquan He | 2026-09-16 | `xswap-patches-v2-sep/0014` |
| `2170` | mm: distinguish large folio swap allocation failures | Xueyuan Chen | 2026-08-30 | `20260830042920.2280454-3-xueyuan.chen21@gmail.com` |
| `2200` | 7.2-nap-v0.5.0 | Masahito S | 2026-06-05 | `04aef34448bb` |
| `2303.patch` | kallsyms: index symbols by token to speed up table compression | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-2-39817ec5db23@kernel.org` |
| `2304.patch` | kallsyms: output binary data to speed output and kallsyms assembly | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-3-39817ec5db23@kernel.org` |
| `2305.patch` | kbuild: do not sort nm output where the order is irrelevant | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-4-39817ec5db23@kernel.org` |
| `2306.patch` | kbuild: only emit vmlinux relocations when required | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-5-39817ec5db23@kernel.org` |
| `2307.patch` | elf-parse: add section flags, symbol binding and a read-only mapping | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-6-39817ec5db23@kernel.org` |
| `2308.patch` | kallsyms: reimplement mksysmap in C | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-7-39817ec5db23@kernel.org` |
| `2309.patch` | kbuild: cache list, composite object state per object | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-8-39817ec5db23@kernel.org` |
| `2310.patch` | kbuild: implement and use depcheck to check dependency timestamps | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-9-39817ec5db23@kernel.org` |
| `2311.patch` | kbuild: move the toolchain checks into init/Kconfig.toolchain | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-10-39817ec5db23@kernel.org` |
| `2312.patch` | kbuild: avoid re-running compiler and linker probes | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-11-39817ec5db23@kernel.org` |
| `2313.patch` | modpost: cache section relocation mismatch state | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-12-39817ec5db23@kernel.org` |
| `2314.patch` | modpost: emit module descriptors as assembly | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-13-39817ec5db23@kernel.org` |
| `2315.patch` | kbuild: batch module finalisation | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-14-39817ec5db23@kernel.org` |
| `2316.patch` | objtool: cache relocations, do less work | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-15-39817ec5db23@kernel.org` |
| `2317.patch` | objtool: size the instruction hash to the text | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-16-39817ec5db23@kernel.org` |
| `2318.patch` | objtool: decode instructions and resolve branch targets in parallel | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-17-39817ec5db23@kernel.org` |
| `2319.patch` | kbuild: rust: optionally parallelise rustc front end | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-18-39817ec5db23@kernel.org` |
| `2320.patch` | rust: make exports.o depend on the headers generated for it | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-19-39817ec5db23@kernel.org` |
| `2321.patch` | kbuild: build rust crates in parallel with the rest of the build | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-20-39817ec5db23@kernel.org` |
| `2322.patch` | kbuild: use pigz for gzip compression if available | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-21-39817ec5db23@kernel.org` |
| `2302` | kbuild: do not allocate .modinfo in vmlinux | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-1-39817ec5db23@kernel.org` |
| `2303` | kallsyms: index symbols by token to speed up table compression | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-2-39817ec5db23@kernel.org` |
| `2304` | kallsyms: output binary data to speed output and kallsyms assembly | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-3-39817ec5db23@kernel.org` |
| `2305` | kbuild: do not sort nm output where the order is irrelevant | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-4-39817ec5db23@kernel.org` |
| `2306` | kbuild: only emit vmlinux relocations when required | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-5-39817ec5db23@kernel.org` |
| `2307` | elf-parse: add section flags, symbol binding and a read-only mapping | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-6-39817ec5db23@kernel.org` |
| `2308` | kallsyms: reimplement mksysmap in C | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-7-39817ec5db23@kernel.org` |
| `2309` | kbuild: cache list, composite object state per object | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-8-39817ec5db23@kernel.org` |
| `2310` | kbuild: implement and use depcheck to check dependency timestamps | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-9-39817ec5db23@kernel.org` |
| `2311` | kbuild: move the toolchain checks into init/Kconfig.toolchain | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-10-39817ec5db23@kernel.org` |
| `2312` | kbuild: avoid re-running compiler and linker probes | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-11-39817ec5db23@kernel.org` |
| `2313` | modpost: cache section relocation mismatch state | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-12-39817ec5db23@kernel.org` |
| `2314` | modpost: emit module descriptors as assembly | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-13-39817ec5db23@kernel.org` |
| `2315` | kbuild: batch module finalisation | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-14-39817ec5db23@kernel.org` |
| `2316` | objtool: cache relocations, do less work | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-15-39817ec5db23@kernel.org` |
| `2317` | objtool: size the instruction hash to the text | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-16-39817ec5db23@kernel.org` |
| `2318` | objtool: decode instructions and resolve branch targets in parallel | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-17-39817ec5db23@kernel.org` |
| `2319` | kbuild: rust: optionally parallelise rustc front end | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-18-39817ec5db23@kernel.org` |
| `2320` | rust: make exports.o depend on the headers generated for it | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-19-39817ec5db23@kernel.org` |
| `2321` | kbuild: build rust crates in parallel with the rest of the build | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-20-39817ec5db23@kernel.org` |
| `2322` | kbuild: use pigz for gzip compression if available | "Lorenzo Stoakes (ARM)" <ljs@kernel.org> | 2026-09-14 | `20260914-build-speedup-v2-21-39817ec5db23@kernel.org` |
| `2400` | sched: Set need-resched flags before tracing | Andrea Righi | 2026-09-11 | `20260911213300.1305763-1-arighi@nvidia.com` |
| `2403` | drm/sched: Do not restore unsaved virtual runtime | Tvrtko Ursulin | 2026-09-07 | `20260907130527.52530-1-tvrtko.ursulin@igalia.com` |
| `2404` | sched_ext: Close the pre-enable ops error claim window | Qiurong Fang | 2026-09-12 | `20260912131518.3428032-1-fangqiurong@kylinos.cn` |
| `2500` | x86/mm: Fix user-space data loss with MADV_FREE and THP | Vernon Yang | 2026-09-03 | `f7491d7c81db` |
| `2502` | x86/amd_node: Fix PCI device reference counting in amd_smn_init() | Yazen Ghannam | 2026-09-03 | `27600805e62f` |
| `9007` | drm/gfx12: Program DB_RING_CONTROL | Alex Deucher | 2026-06-26 | `402ebe22b267` |
| `9011` | drm/amdgpu: Respect noretry flag for retry faults on GFX12.1 | Timur Kristóf | 2026-07-01 | `20260701161721.85681-2-timur.kristof@gmail.com` |
| `9012` | drm/amdgpu/gfxhub: Enable retry fault interrupts when needed | Timur Kristóf | 2026-07-01 | `20260701161721.85681-3-timur.kristof@gmail.com` |
| `9013` | drm/amdgpu/ih: Don't perturb HW registers when accessing soft IH ring | Timur Kristóf | 2026-07-01 | `20260701161721.85681-4-timur.kristof@gmail.com` |
| `9014` | drm/amdgpu/ih: Add retry_cam_ack IH function pointer | Timur Kristóf | 2026-07-01 | `20260701161721.85681-5-timur.kristof@gmail.com` |
| `9015` | drm/amdgpu/ih6.1: Use IH_SW_RING_SIZE for soft IH ring instead of PAGE_SIZE | Timur Kristóf | 2026-07-01 | `20260701161721.85681-6-timur.kristof@gmail.com` |
| `9016` | drm/amdgpu/ih7.0: Use IH_SW_RING_SIZE for soft IH ring instead of PAGE_SIZE | Timur Kristóf | 2026-07-01 | `20260701161721.85681-7-timur.kristof@gmail.com` |
| `9017` | drm/amdgpu/gmc11: Pass cam_index to retry fault handler | Timur Kristóf | 2026-07-01 | `20260701161721.85681-8-timur.kristof@gmail.com` — **REMOVED 2026-09-23** |
| `9018` | drm/amdgpu/gmc12: Pass cam_index to retry fault handler | Timur Kristóf | 2026-07-01 | `20260701161721.85681-9-timur.kristof@gmail.com` |
| `9019` | drm/amdgpu/gmc12: Use AMDGPU_PTE_IS_PTE flag for init_pte_flags on GFX12.0 | Timur Kristóf | 2026-07-01 | `20260701161721.85681-10-timur.kristof@gmail.com` |
| `9020` | drm/amdgpu/vm: Use init PTE flags and NOALLOC in amdgpu_vm_handle_fault() | Timur Kristóf | 2026-07-01 | `20260701161721.85681-11-timur.kristof@gmail.com` |
| `9021` | drm/amdgpu/ih6.0: Use MMIO ACK for retry CAM on IH 6.0 | Timur Kristóf | 2026-07-01 | `20260701161721.85681-12-timur.kristof@gmail.com` |
| `9022` | drm/amdgpu/ih7.0: Use MMIO ACK instead of doorbell for retry CAM on IH 7.0 | Timur Kristóf | 2026-07-01 | `20260701161721.85681-13-timur.kristof@gmail.com` |
| `9023` | drm/amdgpu/ih6.0: Enable retry CAM on Navi 3 dGPUs | Timur Kristóf | 2026-07-01 | `20260701161721.85681-14-timur.kristof@gmail.com` |
| `9024` | drm/amdgpu/ih7.0: Enable retry CAM on Navi 4 dGPUs | Timur Kristóf | 2026-07-01 | `20260701161721.85681-15-timur.kristof@gmail.com` |
| `9034` | drm/amdgpu: fix VM update overrun on non-4K page kernels | Junrui Luo via B4 Relay | 2026-08-06 | `20260806-amdgpu-fixes-v1-2-ce247012d4da@outlook.com` |
| `9035` | drm/amdgpu: add the BO-va mapping offset when kmapping an IB | Junrui Luo via B4 Relay | 2026-08-08 | `20260808-amdgpu-fixes-v2-1-36d66398601f@outlook.com` |
| `9038` | drm/amdgpu: reject PRT mappings as user queue buffer VAs | Junrui Luo via B4 Relay | 2026-08-11 | `20260811-amdgpu-fixes-v1-2-4954a417b8ff@outlook.com` |
| `9039` | drm/amdgpu/userq: bound the eviction fence rearm retry loop | Junrui Luo via B4 Relay | 2026-08-11 | `20260811-amdgpu-fixes-v1-3-4954a417b8ff@outlook.com` |
| `9040` | drm/amdgpu: free userptr HMM ranges on the CS error path | Junrui Luo via B4 Relay | 2026-08-11 | `20260811-amdgpu-fixes-v1-5-4954a417b8ff@outlook.com` |
| `9044` | drm/amdgpu/userq: skip unmapped queues in amdgpu_userq_wait_for_signal | Jesse Zhang | 2026-08-18 | `20260818072959.3356764-1-Jesse.Zhang@amd.com` |
| `9046` | drm/amdkfd: fix integer overflow in queue ring buffer size calculation | Vladimir Marioukhine | 2026-08-17 | `SA1PR12MB8600EE73548498C578990CF49FDC2@SA1PR12MB8600.namprd12.prod.outlook.com` |
| `9049` | drm/amdgpu: recompute the dw estimate after allocating a new VM update job | YuBiao Wang | 2026-07-29 | `39e5b1e4f4b3` |
| `9050` | drm/amdgpu: Update no-retry PTE flags for GFX12 | Mukul Joshi | 2025-12-04 | `9b7ce74b7867` |
| `9054` | drm/amd/display: Guard amdgpu_dm_irq_schedule_work against NULL irq_wq | Ivan Lipski | 2026-08-18 | `0372d4c817bc` |
| `9055` | drm/amdgpu/userq: fix userq_signal_ioctl stuck in drm_exec_until_all_locked() | Yogesh Mohan Marimuthu | 2026-09-07 | `20260907084719.3972-1-yogesh.mohanmarimuthu@amd.com` |
| `9056` | drm/amdgpu/userq: filter out idle userqs from pending signal list | Prike Liang | 2026-09-07 | `20260907125343.647133-1-Prike.Liang@amd.com` |
| `9057` | drm/amdgpu: keep freed VM mappings on clear failure | oushinnyo | 2026-09-05 | `20260905023151.90699-1-oushinnyo@163.com` |
| `9058` | drm/amdgpu: hold a runtime PM reference for P2P dma-buf attachments | Mike Lothian | 2026-09-12 | `20260911232908.1056738-1-mike@fireburn.co.uk` |
| `9059` | drm/amdkfd: don't gate userptr cleanup on the owning mm | Perry Yuan | 2026-09-02 | `20260902024715.696381-1-perry.yuan@amd.com` |
| `9060` | drm/amdkfd: skip migration when the fault window is already in VRAM | William Palacek | 2026-09-01 | `20260901165400.16262-1-William.Palacek@amd.com` |

## The v7.3-rc3 bump (2026-09-13)

### Dropped — merged upstream in rc3

Each was confirmed present in a pristine rc3 tree by checking that the lines it
adds are already there, not merely that `patch` reported it applied.

| Patch | Subject |
|---|---|
| `1153` | drm/amd/display: Fix HF-VSDB DSC bpc detection to be cumulative |
| `1155` | drm/amd/display: Propagate HDMI RGB quantization selectability |
| `1156` | drm/amd/display: Honor Broadcast RGB for BT.2020 RGB output |
| `1157` | drm/amd/display: Rebuild InfoFrames on output color space changes |
| `2300` | scripts/mksysmap: drop the MODULE_INFO() symbols from kallsyms |
| `2301` | scripts/mksysmap: fix escape of `$` in the `__pi_` pattern |
| `2401` | sched/eevdf: Fix augmented max_slice |
| `2402` | sched/eevdf: Fix rb augmented with multi fields |
| `2501` | x86/MCE/AMD: Fix inverted interrupt enablement during storm handling |
| `2600` | hrtimer: Use hard expiry when updating timers on the same base |

### Dropped — superseded
- **`2128`** (zstd: use `ZSTD_cpuSupportsBmi2()` in `ZSTD_initStaticCCtx()`) and
  **`2143`** (zstd: fix DDict hash-set probe index wrap-around). The
  `2100` merge was updated on 2026-09-15 to sirlucjan's 2026-09-14
  `zstd-7.3` cut, which already contains both changes: `2128`'s hunk reports
  "already applied" and `2143` is skipped as present. Removed with the user's
  approval; nothing is lost, the code is in the tree via `2100`.

- **`1145`** (drm/amd/display: Keep FreeSync for HF-VSDB VRR sinks in MCCS
  fallback). rc3 rewrites `amdgpu_dm_update_freesync_caps()`; the block the patch
  guarded no longer exists, so it cannot be rebased without re-authoring it. The
  rc3 code supersedes its purpose.

### Added

| Patch | Source | Subject |
|---|---|---|
| `2144` | akpm-mm `5fe684a7cd8e1` | xarray: fix index jumping backwards in `xas_find()` |
| `2145` | akpm-mm `6cc27d8219638` | mm/vma: correctly unaccount on `mmap_prepare()` failure |
| `2146` | akpm-mm `e14a345480646` | mm/mlock: use the IRQ-safe accessor for `NR_MLOCK` |
| `2147` | akpm-mm `f245cf82e158d` | mm/memcg: clear folio memcg after changing per memcg stats |
| `2148` | crypto ML `<20260825220616.3842633-1-usama.arif@linux.dev>` | crypto: zstd — avoid redundant cstream initialization |
| `2149` | crypto ML, same series | crypto: zstd — avoid redundant dstream initialization |
| `2502` | torvalds `27600805e62f` | x86/amd_node: fix PCI device reference counting in `amd_smn_init()` |

`2148` and `2149` were applied by Herbert Xu on 2026-09-11 for 7.4; they touch
`crypto/zstd.c` and do not conflict with `2128`–`2130`, which are `lib/zstd`.

## Header repairs (2026-09-13)

The provenance audit found defects in the patch files themselves. All are now
repaired. None of them affected whether a patch applies — the build never reads
the header block — but each made a patch harder to trace.

| Defect | Patches | Repair |
|---|---|---|
| `Cc:` label stripped, orphaning a 36-line address list under `Message-Id` | 23 (`2300`–`2322`) | label restored; the address list itself was intact |
| mail-transport headers left behind by an earlier partial strip | `2138`, `2400` (15 and 63 lines) | stripped with a field whitelist, continuations included |
| placeholder or fabricated value in the `From <id>` slot | 43 | replaced with `nobody`; no false commit id remains |
| no `Message-ID` anywhere in the file | 28 | the original submission's `Message-ID` inserted, recovered from the lore mirrors |
| no commit-message body, and therefore no `Signed-off-by` | 16 | body restored from the original mail |

The fabricated values deserve naming: `1135` and `1136` carried sequential
placeholders (`f000…0001`, `f000…0002`), `2300`–`2322` carried the all-zeros
object name, and `1145` carried a 41-character string that cannot be a commit id
at all. Absence from the local clones proves nothing on its own — `repos/` holds
shallow, pruned clones — so each was judged on the shape of the value.

Five generated squashes (`0101`–`0103`, `2101`, `2200`) still have no
`Signed-off-by`. They are our own condensations of other people's branches
rather than submissions, so a single DCO line on them would not mean anything.

### Evaluated and not carried this cycle

- **`drm/amd/display: Try RGB before YCbCr 4:4:4 in stream validation`**
  (Adrian Betschart, dri-devel 2026-09-11). The `amdgpu_dm_connector.c` hunks
  apply; both KUnit-file hunks fail, and that file is not built here. Carrying an
  extracted subset would ship a change to stream-validation ordering, so it is
  deferred rather than forced.
- **`drm/amd/display: Default HDMI RGB output to limited range on CTA
  modes` v2** (same author, 2026-09-10). Same shape: the working hunks apply,
  3 of 10 fail,
  all in the KUnit file. It changes the default colour range, and the symptom it
  targets is already addressed by the upstream `1155`–`1157` now in rc3.
- **`drm/amd/display: invalidate DP CEC state on s3 suspend`** (Dan Himebauch,
  2026-09-12, reported tested on an RX 9070 XT). The mail is MIME-encoded and did
  not survive conversion intact. CEC is not used here.

### Watch items

- **CachyOS reverted `Enable HDMI FRL by default`** (`cc29db585c84` on
  `7.3/base`, `143e44f57bf8` on `7.3/fixes`, both by their maintainer with no
  reason recorded). This series carried the same change as `1144` until
  2026-09-14, when it was dropped as the first bisect step for the 240 Hz
  flicker: the flicker-free cachyos-rc kernel runs `dcfeaturemask=2` while ours
  ran `0x402`, and the extra `DC_FRL_MASK` bit is exactly what this patch adds.
  See the rc3-5 changelog entry for the full evidence chain.
- **drm/amd work item !5663** (RX 9070 XT, 2026-09-13) reports post-resume
  artifacts caused by the ttm/all-SDMA-schedulers change, which **is** in the rc3
  base. No upstream fix is named yet.


## Per-patch notes

Notes for the patches whose index row does not explain itself, and for the
traps that travel with them.

### Handmade local patches (0001–0007, 0010, 0030–0034)

All 13 are small, single-purpose fixes, between 1 and 17 added lines each,
reviewed against the rc2 source on 2026-09-09:

| Patch | Fix | Verdict |
|---|---|---|
| `0001` | typo `tyep` into `type` in `smu_v14_0_set_irq_state` | cosmetic |
| `0002` | free `user_overdrive_table` in `fini_smc_tables`; separate `kzalloc`, real leak | correct |
| `0003` | let the PROFILE_PEAK GFXCLK ceiling float instead of pinning it to the DPM peak entry, which blocked firmware boost above about 2.0 GHz on a part capable of more | correct |
| `0004` | disable deep sleep while PROFILE_PEAK or COMPUTE is active | correct |
| `0005` | `is_mode1_reset_supported` returns false for an SR-IOV VF | correct |
| `0006` | bounds-check `SwI2cCmds[c]` against `MAX_SW_I2C_COMMANDS` | correct |
| `0007` | drop a redundant `adev->pm.mutex` around `smu_cmn_update_table`, a self-deadlock hazard | correct |
| `0010` | named barrier restore in the gfx12.1 trap handler | reviewed for rc2 |
| `0031` | free `enc20` before the `hpd_source` bounds return; leak | correct |
| `0032`, `0033` | `hpo_frl_link_enc_regs[1]` into `[2]` and a second `reg_list(1)`; out-of-bounds | correct |
| `0034` | move `dal_irq_service_destroy` out of the per-pipe loop; double-destroy | correct |

Headers are normalised to upstream quality: author `Sleepy <sleepy@localhost>`,
a matching `Signed-off-by:`, an `Assisted-by: Claude <noreply@anthropic.com>`
trailer, and no leftover `[PATCH n/N]` series numbering.

### HDMI and EDID (0050–0061)

`0050` is Alex Huang's v3, which tolerates future VSDB revisions. `0055` is a
Sleepy [sleepy]-stripped version of Fangzhi Zuo's HF-VSDB gaming-caps patch (the full submission is `20260730171754.704049-2-jerry.zuo@amd.com`, 2026-07-30;
the series also appeared as `150619` in the lists.freedesktop.org amd-gfx
2026-August archive). `0059`, `0060` and `0061`
are the amdgpu side of the same series from that archive, as `150622`, `150623`
and `150621`. Together these give HDMI 2.1 FreeSync over `SIGNAL_TYPE_HDMI_FRL`,
the HF-VSDB VRR-range fallback, and ALLM for Gaming-VRR.

VRR and VSDB parsing live upstream now. Do not re-introduce a local
force-enable: the old local MCCS hack (`1137`) was replaced by the upstream
`1145`.

### GPU core (1000–1099)

`1004`–`1018` are the TLB-invalidation series from agd5f. A 30-patch v2 upgrade
was under review upstream; swap it in as a dedicated session rather than
piecemeal.

`1026` is the GFX12 KFD CRIU-restore NULL dereference: on gfx1201 the MQD
managers leave `restore_mqd` and `checkpoint_mqd` unset, so a process holding
`CAP_CHECKPOINT_RESTORE` could panic the machine through
`KFD_IOC_CRIU_OP_RESTORE`. It was reconstructed from the mailing-list copy,
because Outlook had stripped the whitespace in the diff context.

`1027` force-completes the MES scheduler ring fence on reset. The MES ring has
no DRM scheduler, so the reset loop skipped it, and its writeback-backed polling
fence survived a MODE1 reset while `sync_seq` kept advancing, which wedged the
first post-resume submission.

`1055` fixes VCN utilization in `gpu_metrics`, which reported raw permyriad
instead of a percentage; this GPU is `smu_v14_0_0`. `1056` locks
`drm_sched_entity_is_idle()`. `1058` tracks suboptimal always-valid BOs in the
soft-evicted state. `1060` cancels `hang_detect_work` before taking
`userq_mutex`, a deadlock on the gfx12 user-queue path.

`1061`–`1063` are the TTM and dma-fence use-after-free pair described under
`7.3.0-rc2-10` in the changelog. **One trap:** the same TTM fix was merged
upstream *botched* as `3db7d7d58341`, with the wrong hunk. Carry only the
one-hunk original, which is what the series does.

### AMD display (1100–1199)

`1135` and `1136` carry **synthetic commit ids** — `f000…0001` and `f000…0002`,
sequential placeholders rather than real hashes. Their provenance is Tom Chung's
34-patch amd-gfx series whose cover is
`20260805063937.2145774-1-chiahsuan.chung@amd.com`; the timestamps match the
clamp patch below to the second. The placeholder should be replaced with the
real hash, or removed, the next time these two are touched.

`1138` pulls colorops into the plane state when recreating a plane.

`1140` is Tom Chung's clamp of `force_min_dcfclk`
into the dcn42b range, from the series above. It used to share its number with
James Lin's fallback to an overlay cursor on dcn4x when the top plane does not
fill the CRTC — that one is now `1165` (renumbered in the rc3-9 cycle).

`1141`–`1143` are display robustness fixes: skip receiver power control when
there is no AUX, close DDC when I2C engine setup fails, and fall back to
software I2C when the hardware engine fails. (`1144`, which enabled HDMI FRL by
default, was dropped 2026-09-14 — see the rc3-5 changelog entry.) `1145` is
Fangzhi Zuo's HF-VSDB MCCS fix, which skips the MCCS `freesync_capable` clear
when the sink advertises HF-VSDB VRR; it replaced the local `1137`.

`1150` and `1151` are passive VRR. `1152`–`1154` finish AMD's Linux 7.4 HDMI
2.1 pull. `1155`–`1157` are the HDMI RGB quantization series: the mailing-list
copies are quoted-printable and must be MIME-decoded before applying, or every
hunk fails because `=09` is a tab. `1158` is the DMCUB busy-wait fix.

### AMD power management (1200–1299)

`1201` and `1202` update `cppc_req_cached` before writing the MSR, and add
per-core EPP boost for recently-busy CPUs — the latter is what the
`amd_pstate.epp_boost=1` command-line parameter drives. `1203` documents the
parameter.

`1210`–`1224` are Christian Loehle's 15-patch CPPC v5 rework of the control
path `amd-pstate` runs on Zen 4: validate the `_CPC` packages, propagate
control-write errors instead of dropping them, serialize PCC payload updates,
use 64-bit register masks, reject unsafe cross-CPU SystemMemory
read-modify-write, and fix lifetime leaks.

### Block and I/O (2000–2099)

`2000`–`2004` are Jens Axboe's insert-path micro-optimisations for `mq-deadline`
and `bfq`: pass the queue directly instead of rederiving it, and skip expensive
merge lookups under contention. `2005` skips per-CPU data allocation for
built-in sched-ext DSQs. `2006` and `2007` move zram and zsmalloc to the SG-list
object read API, which saves CPU per decompress on this machine's zram-on-zstd
swap. `2008` stops a single `IORING_ASYNC_CANCEL_ONE` from cancelling in both
the bounded and unbounded accounts.

### Memory management and compression (2100–2199)

`2100` merges zstd 1.6.0 into the kernel tree, including the dynamic-BMI2 guard
that avoids a `HUF_compress1X_usingCTable_internal_body` crash on gcc older than
11.4.

`2101` is LRU-MARIE, now the author's official 0.11.1 port for 7.3. Earlier
carries needed a hand-rebase and a legacy-writeout shim; the author's port
adapts MARIE to the native `swap_ops.h` and `swap_io_ctx` path instead. Two
build-artifact sections the patch bundled (`localversion`,
`scripts/setlocalversion`) were stripped.

**`2131`–`2137` (the MGLRU batch) were REMOVED 2026-09-23** — they were
inert, and this note is why. `lru_gen_enabled()` returns false while
`lru_marie_enabled()` is true, so every MGLRU patch was dead weight here.
`CONFIG_LRU_GEN=y` and `LRU_GEN_ENABLED=y` remain set, but MARIE owns reclaim,
so the MGLRU aging path never runs. Confirm which of the two owns the subsystem
before crediting either with a result.

Verified 6 ways before removal: (1) `2101` masks `lru_gen_enabled()` to false
when MARIE owns aging, stated in its own comment; (2) runtime
`lru_marie/enabled=1`, `CONFIG_LRU_MARIE_DEFAULT_ON=y`, and the boot log prints
"lru_marie: currently enabled"; (3) the functions they change
(`folio_update_gen`, `folio_inc_gen`, `inc_min_seq`) appear **zero** times in
`2101`, so MARIE neither uses nor modifies them — they are pure MGLRU internals;
(4) every reference to those functions in the whole series lives inside the
`2131`–`2137` set itself, so no other carried patch depends on them; (5) `2135`
is a semantic no-op (macro to `static inline`, same `flags` field); (6) this
note, written 2026-09-02, had independently reached the same conclusion.
Confirmed by cumulative apply after removal.

`2120`–`2127` are Rik van Riel's `mm/gup` batching series, RFC v3 at the time of
carrying, worth up to 12.8× in `gup_test` on mTHP paths. Marked RFC, so expect
an upstream revision to supersede it.

`2128`–`2130` probe the CPU for BMI2 once and cache the result, instead of
re-probing per compression context.

`2139`–`2143` are the vmscan, page_alloc and zstd fixes described under
`7.3.0-rc2-10` and `7.3.0-rc2-11` in the changelog. `2143` is an **extracted
subset** of sirlucjan's `7.3-rc/zstd-dev-patches` merge, not an independent
submission; the rest of that merge was not taken, because it refactors the
`bmi2` field into `ZSTD_*Ctx_get_bmi2()` accessors that `2128`–`2130` depend on.

`2173`–`2182` are the 2026-09-16 sweep's mm and lib picks, all `Fixes:`-tagged
and absent from the rc3 base. **Two of them touch the same `zswap_setup()`
region, so the order in `source=()` is a dependency, not a preference** —
`2173` must precede `2174`. Reversing them makes `2174` fail its context check
and be silently skipped by `patch --forward`.

- `2173` publishes the initial zswap pool with `list_add_rcu()`, so a concurrent
  reader cannot observe a half-linked pool.
- `2174` moves `static_branch_enable(&zswap_ever_enabled)` from `zswap_setup()`
  into `zswap_pool_create()`. Without it, a boot where the default-on pool
  creation fails leaves the static key off; a pool created later by writing
  `zswap.compressor` then stores through zswap while the swapin path skips it,
  and pages read back **zeroed**. The reporter measured 131072/131072 zeroed
  pages under fault injection. `Cc: stable`.
- `2175` fixes `SWAP_USAGE_OFFLIST_BIT` colliding with a real usage count.
  `Cc: stable`, one line. Unreachable below 4 TiB of swap, so prophylactic here.
- `2176` fixes a NULL dereference when a sleep-table allocation is retried.
  Directly relevant: this machine swaps through xswap continuously.
- `2177` stops a large-folio swapin from failing when only part of the range is
  in zswap. It replaces an unconditional `WARN_ON_ONCE` + `-EINVAL` for every
  large folio with a range scan: `-EIO` only if a slot really is in zswap, and
  `-ENOENT` otherwise. **Checked against our own swap stack before adopting,
  because a new `-ENOENT` return could send a swapin to a backing device that
  xswap does not have.** It cannot: `2155` already guards exactly this in
  `swap_read_folio()` — `if (unlikely(sis->flags & SWP_XSWAP)) { folio_unlock();
  goto finish; }` sits immediately after the `zswap_load() != -ENOENT` test — so
  on an xswap device the new path stops there instead of reading. No corruption
  path is opened, and the spurious `WARN_ON_ONCE` on our setup goes away.
- `2179` validates the in-memory LZ4 chunk length. **Live on every boot here**:
  `/etc/mkinitcpio.conf` sets `COMPRESSION="lz4"`.
- `2180` fixes `plist_requeue()` corrupting order in the last node. `plist` is
  live in `rtmutex`/`futex` (`Cc: stable`).
- `2181` avoids accesses after waking `klist_remove()` — driver core
  (`Cc: stable`).
- `2182` fixes an incorrect `mod_ct` in `dynamic_debug_init()`;
  `CONFIG_DYNAMIC_DEBUG=y`.

**`2178` was vacated, and the reason is worth recording.** It was `848d2ce2fce1`
(`mm: filemap: retain mapped dropbehind folios`), which the sweep reported as
absent from the base — true, but it was **already carried here as `2141`**. The
diff bodies are byte-identical. It passed every pre-adoption check (`git apply
--check` and GNU `patch --dry-run` on the audit worktree) and was then **silently
skipped in the real build**: the build log reads

```
Applying patch 2176-mm-filemap-retain-mapped-dropbehind-folios.patch...
  SKIPPED: does not apply cleanly
```

against `Reversed (or previously applied) patch detected!`. The audit worktree
had been built from an earlier series state, so it did not contain `2141`.

**The durable lesson: an "is it in base?" test is not a duplicate test.** The
authoritative check is `patch --forward --dry-run` run in series order against
the real tree, which is exactly what `prepare()` does and what
`audit_series.py` reports as `Skipping patch`. A hash scan over the whole series
(body of each patch, `index`/`similarity` lines stripped) now shows `2141`≡`2178`
as the only duplicate pair; the gap at `2178` is left in place rather than
renumbering, matching `2401`/`2402`/`2501`.

**Three further candidates were rejected as inert, not as wrong.**
`392dee2b81f4` and `8679598143f2` (bootconfig) touch a subsystem this machine
does not use — `/proc/bootconfig` is empty and nothing on the command line
enables it. `c922c000d06e` (bunzip2 run-length bound) guards an initramfs
compressor we do not build.

### CPU idle (2200–2299)

`2200` is the NAP governor, firelzrd's `7.2-nap-v0.5.0`. sirlucjan's `7.3-rc/`
tree has no `nap-patches` directory, so the documented source path is stale;
NAP survives only under their `7.0/` and `6.19/` trees. The patch itself is
unaffected.

### kbuild (2300–2399)

`2302`–`2322` are Lorenzo Stoakes' kbuild build-speedup series. **The carried
files are the v3 posting** (`[PATCH v3 NN/20]`, 2026-09-17) — v3 superseded the
v2 posting (`20260914-build-speedup-v2-0-39817ec5db23@kernel.org`, 21 patches,
2026-09-14), which in turn superseded v1. (An earlier revision of this paragraph
said v2; the patch headers say v3, and the headers win.) v2 dropped the modpost
srcversion hashing pair and added the toolchain-checks move into
`init/Kconfig.toolchain` and an objtool instruction-hash sizing patch.

A **v4** posting exists (2026-09-23, 22 parts) and is **not adopted** — see the
2026-10-02 sweep below for the verified reason. This is why a full rebuild here
takes about 8 minutes. Build-time only — nothing here changes runtime
behaviour.

### Scheduler (2400–2499)

`2400` sets the need-resched flags before tracing. `2401` and `2402` are Vincent
Guittot's EEVDF fixes for the augmented `max_slice` and for rbtree corruption
where only one of three augmented fields propagated.

**The EEVDF fixes are largely inert here.** `scx_loader` runs `scx_cake` (live:
`state=enabled`, `ops=cake_1.2.1`), and rc2 gates `sched_balance_trigger()`
behind `if (!scx_switched_all())` in `scheduler_tick()`. The CFS
load-balancing half is therefore bypassed on this machine, which makes `2401`,
`2402` and every other `fair.c` patchset item inert or partly inert while
scx_cake is loaded. They remain correct if sched-ext is ever not loaded.

`2405`–`2411` are `sched_ext-for-7.3-rc3-fixes` (pull `9b87fdc9af2f`, Tejun
Heo), the fixes batch for the 7.3-rc3 sched-ext rework. **These are not inert
here the way the `fair.c` items above are** — `scx_loader` runs `cake_1.2.1`,
so this *is* the live scheduler. The pull's own description names two real
bugs: a use-after-free where an error raised by a BPF program *before* the
scheduler finished enabling was consumed by the disable path's pre-enable
shortcut, leaving a running scheduler that could not be disabled and was later
freed while in use; and two compat kfuncs dereferencing a NULL scheduler when
handed an exited or idle task, oopsing the kernel (`2407`).

`2405` passes the initial `cpu.idle` state in, `2406` stops delivering duplicate
`ops.cgroup_set_idle()` for the same ctx, `2407` fixes the NULL sub-sched
deref, `2408` renames `sch` to `root_sch` in `dispatch_one()`, `2409` uses
`@prev`'s scheduler for the keep decisions, `2410` restores unused idle claims
and `2411` maintains an online `cid` mask in the scheduler arena.

**Three commits of that pull are deliberately not carried.** `a0d356696f87`,
`63b4ff622244` and `89ff16f07139` touch only `tools/sched_ext/scx_qmap.bpf.c`
and `scx_qmap.h`. This PKGBUILD does not build `tools/` (the only reference is
a commented-out `bpftool` line), so they would apply cleanly and change nothing
in the shipped kernel. The eleventh commit in the pull, `c7a1c6e8004a`, is
**already ours as `2404`** — the code is byte-identical and only a comment is
worded differently, because ours is the v1 mailing-list version.

### x86, arch and timers (2500–2600)

`2500` is a one-line data-loss fix: `pmd_modify()` masked out `_PAGE_DIRTY`
where `pte_modify()` and `pud_modify()` do not, so pages rewritten after
`MADV_FREE` on a PMD-mapped THP could be discarded. It was sent twice and merged
into two tip trees, `821eaec4482a` and `f7491d7c81db`; the hunks are
byte-identical and the series carries one, under the merged tip subject.

`2501` fixes inverted AMD MCE threshold-interrupt enablement. `2600` makes
`hrtimer` use the hard expiry when updating timers on the same base.

`2503`–`2507` are the 2026-09-16 sweep's x86 picks, all `Fixes:`-tagged and
absent from the rc3 base. They are one group: `2503` and `2504` take
`init_mm`'s read lock around attribute changes and its write lock around
collapse, so a concurrent `change_page_attr` cannot race `lookup_address`;
`2505` fixes the effective-RW computation in `lookup_address`; `2506` allocates
split page tables as kernel page tables; `2507` excludes alternatives text
poking from racing a concurrent `change_page_attr`. `CONFIG_X86_PAT=y`, and PAT
is per-CPU and on the hot path of every `ioremap`/`set_memory_*` caller, so
this is live code rather than a latent corner.

### agd5f staging backports (9000–9099)

`9007` programs `DB_RING_CONTROL` for gfx12.

`9011`–`9024` are Timur Kristóf's retry-fault handling v3 series, the main
RDNA4 stability gap: respect the noretry flag, enable retry-fault interrupts
when needed, stop perturbing hardware registers when accessing the IH ring,
add the `retry_cam_ack` function pointer, use `IH_SW_RING_SIZE` for the soft IH
ring, pass `cam_index` to the retry-fault handler, use `AMDGPU_PTE_IS_PTE` for
init PTE flags, and use MMIO ACK rather than a doorbell for retry CAM.

`9034`, `9035`, `9038`, `9039` and `9040` are Junrui Luo's amdgpu fixes: a VM
update overrun on non-4K page kernels, the BO-VA mapping offset when kmapping an
IB, rejecting PRT mappings as user-queue buffer VAs, bounding the eviction-fence
rearm retry loop, and freeing userptr HMM ranges on the CS error path.

`9044` skips unmapped queues in `amdgpu_userq_wait_for_signal`. `9046` fixes an
integer overflow in the amdkfd queue ring-buffer size calculation. `9049`
recomputes the dw estimate after allocating a new VM update job, where a stale
free-dw count could encode a 1 GB copy inside the IB pool and hang the ring.
`9050` updates the no-retry PTE flags for GFX12. `9054` guards
`amdgpu_dm_irq_schedule_work` against a NULL `irq_wq`.

**Do not re-add `9051` and `9052`.** They were the DCN4 flip-schedule pair,
dropped because AMD is reverting both upstream.

### The 2026-09-16 second sweep — 59 patches (`1065`–`1069`, `1167`, `2014`–`2044`, `2183`–`2197`, `2412`–`2415`, `2603`–`2605`)

Adopted after the five-lane sweep below. Every one was verified with
`patch -p1 --forward --dry-run -F2` against a worktree carrying the **full
series** (`repos/_sweep-full`), never against a bare rc3 tree and never against
a worktree whose HEAD is the base tag. Series order matters for three groups:
`eabd297f77a2` -> `1808dccdef42` -> `9ffd38b0f610`, `422d8f12c09c` -> `3e2f847821dd`,
and the ten io_uring ring-close patches in posting order.

- **`1065`** — `1065-amdgpu-reserve-eviction-fence-slot-at-wptr-caller.patch`
- **`1066`** — `1066-amdgpu-reserve-root-pd-fence-slots-userq-rearm.patch`
- **`1067`** — `1067-amdgpu-skip-kfd-mapping-clear-before-init.patch`
- **`1068`** — `1068-amdgpu-fix-pcie-link-capability-reporting.patch`
- **`1069`** — `1069-amdgpu-fix-rmmio-iounmap-skipped-on-removal.patch`
- **`1167`** — `1167-dm-restore-native-cursor-early-return-disabled-crtc.patch`
- **`2014`** — `2014-blk-mq-check-passthrough-before-cached-request.patch`
- **`2015`** — `2015-nvme-bump-genctr-when-cancelling-a-request.patch`
- **`2016`** — `2016-nvme-multipath-fix-ana-log-bounds-underflow.patch`
- **`2017`** — `2017-io-wq-order-exit-bit-against-worker-creation.patch`
- **`2018`** — `2018-io_uring-put-request-file-before-completion.patch`
- **`2019`** — `2019-io_uring-post-io-wq-completions-last-reference.patch`
- **`2020`** — `2020-io_uring-rw-dont-reap-iopoll-while-io-wq-ref.patch`
- **`2021`** — `2021-io_uring-put-request-files-before-completions.patch`
- **`2022`** — `2022-io_uring-uring_cmd-cancel-only-given-task.patch`
- **`2023`** — `2023-io_uring-notif-count-zerocopy-per-ring.patch`
- **`2024`** — `2024-io_uring-cancel-wait-all-requests-on-exit.patch`
- **`2025`** — `2025-io_uring-run-cancelations-sync-on-release.patch`
- **`2026`** — `2026-io_uring-drop-files-buffers-at-release.patch`
- **`2027`** — `2027-io_uring-wait-inflight-requests-on-release.patch`
- **`2028`** — `2028-r8169-propagate-errors-from-phy-write.patch`
- **`2029`** — `2029-r8169-propagate-firmware-access-errors.patch`
- **`2030`** — `2030-r8169-release-firmware-on-application-failure.patch`
- **`2031`** — `2031-tcp-exclude-old-acks-from-fast-path.patch`
- **`2032`** — `2032-tcp-preserve-timestamps-across-recv-collapse.patch`
- **`2033`** — `2033-tcp-init-skb-tx-timestamp-key-before-clone.patch`
- **`2034`** — `2034-tcp-do-not-let-tcp_rmem-go-below-4096.patch`
- **`2035`** — `2035-net-lock-socket-in-sock_gettstamp.patch`
- **`2036`** — `2036-net-tcp-account-zerocopy-receive-vma-memory.patch`
- **`2037`** — `2037-net-neighbour-serialize-proxy-timer-teardown.patch`
- **`2038`** — `2038-net-sched-codel-bound-drop-loop-per-dequeue.patch`
- **`2039`** — `2039-net-sched-avoid-quadratic-qdisc_alloc_handle.patch`
- **`2040`** — `2040-net-sched-reject-idr-error-pointers-act-api.patch`
- **`2041`** — `2041-net-gso-limit-recursive-ip-in-ip-segmentation.patch`
- **`2042`** — `2042-net-skbuff-no-stale-headers-after-pskb_carve.patch`
- **`2043`** — `2043-fs-avoid-repeated-scans-in-evict_inodes.patch`
- **`2044`** — `2044-lib-group_cpus-snapshot-cluster-masks-hotplug.patch`
- **`2183`** — `2181-mm-shmem-split-large-folios-only-on-e2big.patch`
- **`2184`** — `2182-mm-page_counter-avoid-overflow-effective-protection.patch`
- **`2185`** — `2183-mm-swap-cache-replace-fix-off-by-one.patch`
- **`2186`** — `2184-memcg-fix-stuck-flushing-cached-charge-bit.patch`
- **`2187`** — `2185-memcg-clear-flushing-cached-charge-cpu-offline.patch`
- **`2188`** — `2186-mm-swap-clusters-info-after-solidstate-init.patch`
- **`2189`** — `2187-mm-huge_memory-zap-deposited-tables-after-rcu.patch`
- **`2190`** — `2188-mm-zswap-release-retired-pools-queue-rcu-work.patch`
- **`2191`** — `2189-mm-zswap-invalidate-takes-a-range.patch`
- **`2192`** — `2190-mm-zswap-skip-xarray-walk-when-unused.patch`
- **`2193`** — `2191-mm-zswap-reuse-invalidate-in-zswap_store.patch`
- **`2194`** — `2192-mm-swap-drop-unneeded-swap_extend_table_try_free.patch`
- **`2195`** — `2193-mm-swap-return-early-from-swap_extend_table_try_free.patch`
- **`2196`** — `2194-memcg-avoid-charging-root-memcg-obj-cgroup.patch`
- **`2197`** — `2195-mm-mremap-account-locked_vm-mremap-dontunmap.patch`
- **`2412`** — `2412-cgroup-avoid-iterating-dying-tasks-zero-refcount.patch`
- **`2413`** — `2413-sched_ext-protect-idle-search-nodemask-irqsave.patch`
- **`2414`** — `2414-sched_ext-scx_locked_rq-return-null-from-nmi.patch`
- **`2415`** — `2415-sched_ext-reject-nmi-calls-lock-taking-kfuncs.patch`
- **`2603`** — `2603-sysctl-check-range-proc_dointvec_ms_jiffies_minmax.patch`
- **`2604`** — `2604-sysctl-check-range-do_proc_ulong_conv_ms_jiffies.patch`
- **`2605`** — `2605-sysctl-fix-type-truncation-sysctl_msecs_to_jiffies.patch`


## Two ledger defects found by the 2026-09-16 sweep

**Four numbers are indexed as carried but exist nowhere.** `2401`, `2402`,
`2501` and `2600` all appear in the patch index above and are described in the
prose as if present, but none is in `source=()` and none is on disk:

```
2401  in-PKGBUILD=0  on-disk=0    2501  in-PKGBUILD=0  on-disk=0
2402  in-PKGBUILD=0  on-disk=0    2600  in-PKGBUILD=0  on-disk=0
```

`2600` is the hrtimer hard-expiry patch, and no carried patch touches
`kernel/time/hrtimer.c` at all. Either they were dropped without the index being
updated, or they were planned and never added. **The new sysctl trio is numbered
`2603`-`2605` rather than `2600`-`2602` specifically to avoid squatting a number
the ledger already documents.** Resolve before the 7.4 bump.

**A carried patch applies with fuzz, which is why one candidate could not.**
Patch `2155`'s `mm/zswap.c` hunk expects the context line

```
	if (!si)
		return -ENOENT;
```

but our base has `return -EEXIST;` at `mm/zswap.c:1001`. GNU `patch` accepted the
hunk with fuzz, so the file was not rejected and the build reports success. The
`SWP_XSWAP` guard itself landed in the right function, so this is harmless
today — but the tree and the patch text disagree, and it is exactly why
`c93496f5133e` ("return -ENOENT when the swap device is gone") cannot apply.
Regenerate the hunk against the current base rather than editing it by hand.

## Sweeps 2026-09-15 (from the rc3-12 cycle)

### Sweep 2026-09-15: three parallel sweeps (MM, crypto/block/net, PM/x86/sched + work items)

**Hazard for the 7.4 bump — re-test the flicker fix.** Upstream has merged
"Enable HDMI FRL by default" (`af6139855b55`, in amd-staging only for now,
targeted 7.4), which sets `DC_FRL_MASK` in `amdgpu_dc_feature_mask`. That is
exactly the variable this project bisected for the 240 Hz flicker and dropped
as `1144` (`PATCH_SOURCES.md`). When the bump lands, re-check the MAG251RX at
1920x1080@240 Hz before shipping. Related: Fangzhi Zuo's FRL patches 61/66 and
65/66 in Chenyu Chen's DC 3.2.398 series sit on the same surface as our `0058`
and `1136`.

**Already carried — the sweeps re-found our own patches.**
- `2500` is `f7491d7c81db` (the Phoronix "silent user-space data loss since
  2023" item); `2502` is `27600805e62f` (x86/amd_node PCI refcount);
  `2404` is `c7a1c6e8004a` (sched_ext). All three are now upstream post-rc3
  and go on the drop-list for the next bump.
- `1159` is patch 58/66 of Chenyu Chen's DC 3.2.398 series — the patch AMD
  developers recommend in work items #5829, #5834 and #5839 for `update_config`
  NULL dereferences. Carrying it already.
- The kbuild series Phoronix covered on 2026-09-15 ("~36% faster builds") is
  the `[PATCH v2 00/21]` series we already carry as `2302`–`2322`.
- `2140` (direct compaction for costly `__GFP_NORETRY`) is in mm-unstable —
  ours already. `2011` is byte-identical to the r8169 LTR ML v4.

**Deferred, with reasons.**
- zswap "optimize zswap invalidate and store" v3 (Kefeng Wang, 3 patches)
  applies cleanly and is on-target now that zswap backs the swap stack. Held
  back deliberately: it rewrites `swap_range_free()`, the same function the
  xswap series (`2155`–`2166`) rewrites, and both are unmerged review-stage
  series. Composing two of those in the swap hot path is how this project got
  the flicker. Re-evaluate at the 7.4 bump, when at least one of them lands.
- Usama Arif's PMD-level swap entries for anonymous THPs v7 (29 patches) is
  the most on-target MM series found (THP swap + zswap + xswap all in play),
  but it is a large review-stage rewrite of the same paths. Watch.
- Hugh Dickins' `mm/fbatch` drain v2 (26 patches): the author states he is
  taking three weeks off, expects "some disappointments" on performance, and
  asks someone else to shepherd it.
- Lorenzo Stoakes' VMA-flag semantics v2 (40 patches) is the same churn that
  already broke LRU-MARIE once (`vm_flags` → `vma_flags`).
- CPPC: our `1210`–`1224` are Christian Loehle's **v5**; a **v6** exists
  (2026-08-30, same 15-patch shape, still under review with an outstanding
  request from Rafael Wysocki). Refresh at the bump rather than mid-cycle.
- amd-pstate 7.4 pull: Zen 6 EPP tunings do not apply to Zen 4, but the pull
  restructures `amd-pstate.c`/`.h` where our `1201`/`1202` live — expect a
  rebase surface.
- **BBR3 rebase surface**: linux-next `cb145191e9d3` renames `min_tso_segs()`
  to `tso_segs()` with a new signature; `0101-cachy-bbr3.patch` references the
  old name 13 times.
- io_uring: cancel-at-ring-close (merged for 7.4) and Jens Axboe's 15-patch
  thread-identity handoff RFC are 7.4 material — the RFC's own table shows
  large queue-depth-1 wins but losses at higher depth (−65% fsync on ext4 at
  qd32), so it is not obviously a win. `net/sched` qdisc handle scan needs 32767 HTB classes to
  matter (ours has one). Rejected as off-target: r8169 RSS v13 (RTL8127),
  realtek PHY firmware writes (RTL8261x), `xor_gen` AVX-512 (`CONFIG_BLK_DEV_MD`
  is off), `tcp_poll()` `smp_rmb()` (an ARM64 win), zonelist/NUMA and
  cache-aware-scheduling work (single-CCD desktop), ESMTP (SEV-SNP guests).

**Checked and dismissed: the NAP governor.** A sweep pass reported that the
NAP cpuidle governor never tests `states_usage[].disable` and could enter a
C-state disabled via sysfs. It does test it — in `nap_fallback_heuristic()`,
in `nap_find_min_valid_state()` (behind the cached-minimum path), and in the
neural-net decision loop inside `nap_fpu_select()` before it accepts a
candidate. No action.

**Machine profile corrections that shrink the search space.** `CONFIG_NUMA` is
**not set** in this build, so the NUMA-targeted optimizations that dominate mm
and net-next (zonelist refactors, per-node reclaim, `skb_defer_free` node
iteration, cache-aware scheduling) are inert here, and `for_each_node()` and
`for_each_online_node()` compile to the same thing. `CONFIG_BLK_DEV_MD` is off,
so the raid6/xor `vzeroupper` work is inert. `CONFIG_EROFS_FS` is off.

**Two branches/dirs we do not adopt from, checked.** CachyOS's `7.3/vesa-dsc-bpp`
carries VESA DSC EDID parsing and a DSC `max_qp` spec fix; the EDID side is
already upstream in rc3 and this machine never negotiates DSC (1080p240 fits
HDMI 2.0's 600 MHz TMDS without it), so nothing to take. sirlucjan ships
**ADIOS**, a 2,062-line non-upstream "Adaptive Deadline I/O scheduler"
(`block/adios.c`, Piotr Gorski, 3.3.0) that CachyOS patches to be the default.
Not adopted: it is unreviewed third-party block-layer code, and this machine's
scheduler is a deliberate distro choice — `60-ioschedulers.rules` sets **kyber**
for NVMe, bfq for rotating, mq-deadline for other flash. Worth revisiting only
if desktop I/O latency ever becomes a complaint.

**Verified drop-list (reverse-apply audit against torvalds master, 2026-09-15).**
Five carried patches are already in master and disappear at the next bump:
`2141` (filemap retain mapped dropbehind folios), `2145` (mm/vma unaccount on
mmap_prepare failure), `2146` (mm/mlock IRQ-safe NR_MLOCK accessor), `2500`
(MADV_FREE/THP data loss) and `2502` (x86/amd_node PCI refcount). The check is
`git apply --check -R` per patch against a worktree at `origin/master` — note it
must run against a master checkout, not the repo's working tree, which sits at
rc3 and makes every patch look un-applied.

**Work items.** The five tracked issues (#5821 hang, #5820 SMU bus loss, #5800
vblank timeout, #5812 VRR black level, #5780 HDMI FRL) still have no referenced
fix. #5720's fix (`c4a5160e3be0`) is absent from rc3 but concerns YCbCr-4:2:0
sinks, which this monitor is not. #5663 (TTM/SDMA artifacts after resume) is
acknowledged by Christian König as known and being investigated.

### Deep sweep 2026-09-15 (second pass): GPU/display, core, work items

**A patch we carry does nothing on this hardware — `1140`.** It modifies only
`dc/clk_mgr/dcn42b/dcn42b_clk_mgr.c`. That clk_mgr is instantiated exclusively
under `AMDGPU_FAMILY_GC_11_5_0` with `DCN_VERSION_4_2B`
(`dc/clk_mgr/clk_mgr.c`). Our GPU is GC IP (12,0,1), which
`amdgpu_discovery.c` maps to `AMDGPU_FAMILY_GC_12_0_0` → `dcn401_clk_mgr_construct`,
and the kernel reports "Display Core v3.2.392 initialized on DCN 4.0.1". The
DCN42B file is dead code here, so the patch is inert — the "a patch that applies
can still do nothing" trap again. A scan of every carried patch against the
display blocks we do not instantiate (dcn42, dcn42b, dcn60) found this as the
only case. Removal needs the user's approval; it is harmless where it sits.

**DC 3.2.398 (66 patches) triage — nothing adopted.** The reviewer-recommended
patch 58 is already ours (`1159`). The rest of the fix-shaped subset is
off-target or inert:
- patches 42, 43, 56, 57, 60 touch `pg/dcn42/`, `resource/dcn42b/` and the
  DCN42B MALL/HPO paths — the same dead blocks as `1140`; patch 61 touches
  `hpo/dcn42/` and `hpo/dcn60/`; patch 04 targets DCN31/35/42.
- `35c21515dbe1` ("fix MALL hysteresis timer underflow at high refresh rates")
  looked ideal — a 240 Hz-relevant underflow in the hysteresis timer — but it
  patches `dcn30_apply_idle_power_optimizations()`, and DCN 4.0.1 has its own
  `dcn401_apply_idle_power_optimizations()` (DMUB CAB based, no such timer).
  It is the DCN 3.x implementation that underflows, not ours.
- `37531443a4f3` ("mes12: clear event log on resume to avoid MES page fault",
  Jesse Zhang, AMD, 2026-09-15) is on-target but **inert at defaults**: its
  guard checks `amdgpu_mes_log_enable`, and
  `amdgpu_mes_event_log_init()` returns before allocating the buffer unless
  that parameter is set — it defaults to 0.
- DC 59 and DC 52 are behaviour changes inside a 66-patch drop that lands with
  the next drm merge; taking them piecemeal invites conflicts with the rest.

**Deferred for breadth, not doubt.** `2d606b35a24c` ("drm/sched: fix
use-after-free of the fence timeline name", v3 0/2) is a real UAF fix but a
121-line rewrite of fence lifetime across `sched_fence.c`, `sched_main.c` and
`gpu_scheduler.h` — and this series already carries four drm/sched patches.
`1528781b16c7` ("drm/vblank: Don't arm vblank timer with invalid frame
duration", v4) changes `drm_calc_timestamping_constants()` from `void` to `int`
across DRM. Both land upstream; revisit at the bump.

**Core sweep:** nothing includable. The only real candidate, a hrtick repick
fix (Shubhang Kaushik), is measured on ARM64 and the author partially withdrew
v2 ("please disregard the DL portion of v2") — and `CONFIG_SCHED_HRTICK` plus
HRTICK_DL are on here, so the withdrawn half is not inert. Wait for v3.
Everything else was already carried (`2012`/`2013`, `2148`/`2149`, `2302`–`2322`),
queued for 7.4, or inert.

## Sweep 2026-09-18 — four series replaced with their current revisions

Fetched every source and swept the carried series for newer revisions. Four
replacements were verified and taken; the series is 303 -> 302.

### build-speedup v3 (`2302`-`2321`, was `2302`-`2322`)

`[PATCH v3 0/20] kbuild: significantly speed up kernel builds`, Lorenzo Stoakes,
2026-09-17. Found via the lore **git** endpoint
(`git clone --mirror https://lore.kernel.org/rust-for-linux/0`) — the web UI is
blocked, the git endpoint is not.

Verified by substitution: all 21 carried patches reverse cleanly, all 20 v3
patches apply, zero rejects. v3 touches 49 files and **no later carried patch
(`>2322`) touches any of them**, so there is no ordering hazard.

**v3 drops the rustc front-end threading patch** (was `2319`). Its cover letter
states the reason and the remedy:

> "Dropped what was 18/21 - the rustc front end threading patch, as the parallel
> flag name is still uncertain and a user can set `KRUSTFLAGS=-Zthreads=8` to get
> the behaviour without it."

`CONFIG_RUST=y` here, so the PKGBUILD now exports `KRUSTFLAGS="-Zthreads=8"`
(line 643) to keep the parallelism. Other v3 changes: `15/20` drops the
relocation hash and builds one section at a time incrementally, falling back to
a linear scan; `17/20` limits parallelisation to the `--link` step only;
`20/20` moves pigz onto the make job server via `KPGZIP`; `19/20` stops
`modules_prepare` duplicating a `rust/` build; `14/20` restricts
`.module-common.o` to the top-level make instance.

### ACPI CPPC v6 (`1210`-`1224`, 15 patches)

`[PATCH v6 0/15] ACPI: CPPC: Fix register access and lifetime bugs`,
Christian Loehle, 2026-08-30. Ours were v5, posted 2026-08-27 — three days
older. Live on this machine: `amd-pstate` is built on ACPI CPPC.

### net GSO `2041` (v2)

`[PATCH net v2 1/1] net: gso: limit recursive IP-in-IP segmentation`, Zihan Xi,
2026-09-17. Ours was v1, posted 2026-09-13 — the v2 landed four days later.

### `2147` (v5)

`[PATCH v5] mm/memcg: clear folio memcg after changing per memcg stats`,
Bingfang Guo, 2026-09-10. Ours was four revisions behind.

### Locally adapted and taken

- **`1070` — SDMA 7.0 compact IB emission**, from `[PATCH 17/18]` of Tvrtko
  Ursulin's "More compact IB emission" series
  (`<20260918120518.96922-18-tvrtko.ursulin@igalia.com>`, 2026-09-18). Authorship
  stays with Ursulin; the patch carries his `Signed-off-by` plus an
  `Assisted-by: Claude` trailer for the adaptation.

  Upstream hunk 4 targets `sdma_v7_0_ring_pad_ib()` and is written against a
  base carrying a prerequisite refactor this tree does not have: it expects
  `const bool burst_nop = sdma->burst_nop;` hoisted out of the loop with the
  `sdma &&` NULL check dropped, where rc3 still reads
  `sdma && sdma->burst_nop && (i == 0)`. The hunk therefore does not apply, on
  the series tree **or** on clean rc3.

  The adaptation ports that hunk's delta — the early `return` when
  `pad_count == 0`, the register pointer, and the single
  `ib->length_dw += pad_count` write-back — onto the rc3 function form and
  changes nothing else. The diff body was regenerated with `git diff` rather
  than written by hand (the `1026` reconstruction method). The only textual
  difference from the original is one spacing fix, `*ptr++=` to `*ptr++ =`,
  matching the sibling branch in the same hunk.

  Of the 18-patch series, only `17/18` targets Navi 48; the rest are GFX8/9, SI,
  CIK, UVD, VCE and SDMA 2.4-6.0, so they are not carried.

### Other findings

- **`repos/torvalds` and `repos/drm-next` were corrupt** (394 and 144 fsck
  issues respectively, both unable to fetch). Both re-cloned; `torvalds` now
  reaches 2026-09-18. Any GPU or mainline negative result recorded before this
  re-clone is weaker than it reads.
- **`lore-dri-devel` and `lore-netdev-new`** carry two unresolved pack deltas
  each. Usable, but `lore-netdev-new` reports a 2026-09-22 commit — a sender's
  bad clock on a Lynx PCS patch, not corruption.
- **`lore-rust-for-linux`** added to `repos/` as the build-speedup series source.
- The drm/amd work items reference message-id `20260908113338` across five
  open issues (`#5834`, `#5839`, `#5843`, `#5846`, `#5859`). That is the DC IRQ
  register read-modify-write patch, **already carried as `1159`**. The two
  commit shas the tracker cites are dead ends: `112d2111f50a…` is 32 characters
  and not a valid kernel sha, and `dc59e4fe…` resolves to the `Linux 7.2-rc1`
  tag.

## Bump notes from the 2026-09-21 sweep (for the 7.4 bump)

### The SDMA refactor that retires `1070`'s local adaptation

`1070` (SDMA 7.0 compact IB emission, Tvrtko Ursulin) is carried **locally
adapted** because upstream hunk 4 expects `const bool burst_nop =
sdma->burst_nop;` hoisted out of the loop and the `sdma &&` NULL check dropped,
where this base still reads `sdma && sdma->burst_nop && (i == 0)`.

A five-commit series by the **same author** does exactly that refactor, and
**`e0e9c2257911`** deletes precisely those lines:

```c
-	const bool burst_nop = sdma->burst_nop;
-		if (i == 0 && burst_nop)
+	if (count && sdma->burst_nop) {
```

| sha | subject |
|---|---|
| `61a68bbfd5ac` | Add `amdgpu_sdma_types.h` header (creates the file) |
| `f315ca00f903` | Convert SDMA instance and index to direct lookup |
| `99c9ca0af04d` | Cache the SDMA CSA address |
| `35ac2639df55` | Add SDMA ring init helper |
| `e0e9c2257911` | Use memset32 for SDMA padding |

All five are absent from `torvalds` and `linux-next` — they sit only on
`amd-staging-drm-next` @ `e0e9c2257` (and rebased onto `agd5f-linux`
`origin/drm-next` @ `cf48bd0a` under different shas). **They are 7.4-queue
material.**

**They do not apply to `v7.3-rc4`:** 4 of the 5 fail at hunk #1 (`61a68bbfd5ac`,
`99c9ca0af04d`, `35ac2639df55`, `e0e9c2257911`), only `f315ca00f903` applies,
and they are interdependent — the first creates the header the rest consume. So
taking them now means rebasing five interdependent commits across
`sdma_v2_4.c` … `sdma_v7_0.c`, in the driver this GPU depends on, to replace a
`1070` that is already verified and building.

**Do this at the 7.4 bump, not before.** At that point the series arrives with
the merge, `1070` has to be refreshed anyway, and the adapted hunk can be
swapped for the clean upstream one. Ordering matters: `61a68bbfd5ac` first,
`e0e9c2257911` before any `1070` refresh.

### HDMI interface churn arriving at the 7.4 bump

`drm-misc-next` landed a 30+ commit HDMI 2.0 scrambling / SCDC /
`bridge_connector` series on 2026-09-19: `f27fb7e31` (scrambler
infrastructure), `d65381832` (scrambling management helpers), `245e321b6`
(renames `drmm_connector_hdmi_init()` → `*_ini2()`), `400c9ede1` (new-signature
version). Generic `drm/display` + `drm/connector`, not amdgpu — but it is
interface churn directly under our `0055`/`0058`/`0059`/`1136` HDMI/FRL patches.
Expect it alongside the already-recorded `DC_FRL_MASK` /
`parse_hdmi_amd_vsdb()` conflicts.

### The GPU trees were frozen on 2026-09-21

Verified against the remotes with `ls-remote`, not just locally: `drm-next`,
**all 132** `agd5f-linux` refs (including `drm-fixes-7.3`, `drm-next`,
`tlb_inv_rework`, `ualink`) and `amd-staging-drm-next` contained **zero**
commits with committer date ≥ 2026-09-17. The newest AMD work anywhere was
`e0e9c2257` (09-14/16). Nothing post-rc4 in `torvalds` is on-target either —
one xfs-fixes merge, a `net: qrtr` MHI patch and four i2c DMA-cleanup commits.

### Re-triage trap: the dropbehind re-post

`c8107330f4b5` and `4e31aa026794` (Alexandre Ghiti) appear "new" in `akpm-mm`
with committer dates of 2026-09-20, but they are the **same series already
rejected** as `2b09efabae8f`/`e42fa88021a8`/`f9abcb602ef3` — same author, same
`Link:` base (`20260911121341.178028-3-alex@ghiti.fr`). The rejection stands for
the same reason: xswap has no backing store, so the writeback-completion paths
they fix are unreachable here. **Re-verify only if xswap gains a physical
backend** (which is what RFC 1169641 proposes).

### sirlucjan `hdmi-patches-v2` — a rebundle of work we already carry, not an upgrade

sirlucjan added `7.3-rc/hdmi-patches-v2/` and `7.3-rc/hdmi-patches-v2-sep/` on
**2026-09-21** (`fabe84aa`, 7 patches). It is the **same 7 patches as CachyOS's
`7.3/hdmi` branch** (`a2f9247a396c` … `454b328c28ee`, merged into `7.3/base` at
`2e790384a738`). All 7 apply cleanly to pristine `v7.3-rc4`.

Mapped against our carries — five of the seven are already ours, some
byte-identical:

| sirlucjan v2 | ours | result |
|---|---|---|
| `0001` Add 2.1 FreeSync support for AMD VSDB | `0059` | identical file content |
| `0004` Enable HDMI ALLM for Gaming-VRR | `0061` | identical file content |
| `0005` Add passive_vrr properties | `1150` | identical file content |
| `0006` Use passive_vrr properties in amdgpu | `1151` | **byte-identical** |
| `0007` Keep FreeSync for HF-VSDB VRR sinks | `1163` | functionally identical |

`0007` matching is worth recording on its own: `1163` is a *reconstruction*
(the patch note records it was dropped at the rc3 rebase and rebuilt by hand).
The upstream author's own v2 carries the same guard in the same place, so the
rebuild is independently confirmed correct. CachyOS's `7.3/hdmi` HEAD
(`454b328c28ee`) is the same change, which is the "CachyOS's flicker-free kernel
demonstrably carries the guarded version" claim in that patch note, now verified
against the branch itself rather than inferred.

**Where the two differ, we are ahead, not behind.** Verified against pristine
rc4, which carries only the "VSDB version 3" struct:

- Their `0002` is the V3-only AMD VSDB parse. Our `0050` is Alex Huang's
  `[PATCH v3 1/4]` (2026-08-04) adding FreeSync refresh-range fields
  (`freesync_supported`, `min_frame_rate`, `max_frame_rate`,
  `freesync_vcp_code`) — rc4 has none of them, so this is ours alone.
- Their VTEM emission is FRL-only (`new_stream->sink->sink_signal ==
  SIGNAL_TYPE_HDMI_FRL`). Ours (`1152`) also emits on TMDS when the sink
  advertises HF-VSDB VRR.
- Decisively, our `0055` is a deliberate **struct-only strip** of the HF-VSDB
  parse — "without enabling the parse" — which sirlucjan enables in full. That
  divergence is the whole reason `1164` exists (the MAG251RX must not be
  advertised VRR-capable). Adopting v2 would re-enable the parse our series
  deliberately withholds and undo the rc3-9 flicker fix.

**No action. Do not adopt.** Re-check at the 7.4 bump, where the same set
arrives under the `drm-misc-next` HDMI 2.0 scrambling/SCDC churn already
recorded above.

### drm/amd work-items tracker, 2026-09-21

100 open issues; 34 created since 09-14. Plain `curl`, no User-Agent; comments
via GraphQL. On-target threads (Navi 48 / RX 9070 XT / DCN 4.0.1):
`#5872` USB4 pageflip timeout, `#5869` gfx1201 ring reset → MODE1, `#5870`
`amdgpu_sync_add_later` UAF, `#5868` HDMI disconnect loop (already recorded —
this machine is at 1080p, below the threshold), `#5862` Navi 48 FRL, `#5859`
DCN 4.0.1 DDC/CI, `#5852` HDMI audio stutter, `#5831` panic, `#5843`/`#5846`
9070xt pageflip.

**The display "box" root cause is now externally confirmed.** `63e19ef3ddab`
("drm/amd/display: Atomize IRQ register read/modify/write ops", Leo Li,
2026-08-25) is the VUPDATE_NO_LOCK read/modify/write race fix. AMD's Mario
Limonciello (`superm1`) tells users "Please apply this patch" with that exact
sha in `#5872`, `#5843` and `#5846` — all RX 9070 XT pageflip-timeout reports.
It is **contained in `v7.3-rc4`**, so `7.3.0_rc4-1` carries it natively. We
used to carry this as `1159` and dropped it at the rc4 rebase as absorbed —
that drop is now validated from the vendor side, not just by reverse-apply.

**Candidate — unreviewed, verified, applies clean:** Donggeun Yoo,
*drm/amdgpu: don't release the fence reference consumed by the scheduler*,
2026-09-10, `<20260910035531.559908-1-donggeunyoo.kernel@gmail.com>`
(mirror sha `1acff2c440eb600154fb909b9dcf496353a0303d` in `lore-dri-devel`).
Reported in `#5870` against an RX 9070 XT. Three call sites
(`amdgpu_cs_submit()`, `amdgpu_sync_push_to_job()`, `amdgpu_vm_sdma_update()`)
take a reference for `drm_sched_job_add_dependency()` and then put it again on
the error path.

**The ownership claim is verified independently in our tree**, not taken on the
author's word: `sched_main.c` line 694 puts the fence on the dedup path and
line 701 (`if (ret != 0) dma_fence_put(fence);`) puts it when `xa_alloc()`
fails — so the callee consumes the reference in both the success and the error
case. The caller's extra put is therefore a double-put, a refcount underflow,
and a UAF on an unrelated thread. Applies cleanly to `v7.3-rc4` under both
`git apply --check` and `patch -p1 --dry-run -N`. Trigger is `xa_alloc()`
failing, i.e. memory pressure during command submission or a VM update.

Status: **no replies, no revision, no acked-by** — 11 days with zero list
traffic. AI-assisted (`Assisted-by: Claude`), human author with
`Signed-off-by`, which this project permits. Not currently carried; flagged to
the user as a decision.

Two classifier traps hit while reading the tracker, both worth keeping:
`curl … | head && echo OK` reports OK regardless, because the exit status is
`head`'s — it printed "APPLIES CLEANLY" over `corrupt patch`. And
`git merge-base --is-ancestor` reported three 2022–23 commits as *not* in rc4
when they plainly are: the shallow-clone lie already recorded in `LESSONS.md`.
Use `git cat-file` and read the code.

`112d2111f50a85276245fa9fd5b64981` (cited in `#5859`) is confirmed **not a
commit** in any tree — the image-upload path the skill warns about.

#### Deep pass — every description and comment on all 100 issues

31 real commits are referenced across the tracker (301 further hex tokens were
image paths, blob ids and other non-commits). Triage by the authoritative test,
forward-applies ⇒ absent, reverse-applies ⇒ already present:

| sha | subject | verdict |
|---|---|---|
| `c953b39f9487` | Reintroduce "Force validation link training on all ASICs" | **rev-OK — already in rc4** |
| `db7e8108809a` | Fix VFCT bus number matching with soft filter | **rev-OK — already in rc4** |
| `2ee9836545e6` | Fix VCE 3 ring align_mask | rev-OK, and VCE 3 is not this ASIC |
| `482b6542a862` | restore FRL cap on non-destructive HDMI link verify | fwd-OK — **is our `0058`**, absent from pristine rc4 as expected |
| `c22f9a61e288` | Remove gfxoff calls in **GC v12.1** | fwd-OK but **wrong chip** — this is GC 12.0 (`gfx_v12_0.c`); `smu_v14` gfxoff is not v12.1's |
| `0b0ff65d3ca1` | Refactor stream validation | 315 lines rewritten in `amdgpu_dm_connector.c` — the file `0059`/`1152`/`1163`/`1164` live in. A refactor, not a fix. Not worth the conflict surface |
| `7e5760f084d0` | add HDMI 2.1 Compliance Support | **absent from rc4, from our tree, and from amd-staging** |

The only genuine include-candidate is `7e5760f084d0`: it adds the
`force_yuv422_output` / `force_yuv444_output` debugfs knobs AMD points HDMI 2.1
compliance reporters at (`#5760`, `#5789`, `#5796`). It sits on `agd5f-linux`'s
`drm-fixes-7.2` and `drm-fixes-7.3`, so it is stable material that will reach
mainline on its own schedule. It is a **debugging aid with no runtime effect
when unused** — worth taking only because this machine's display work is
HDMI-heavy and these are the knobs AMD triages with. Low priority; not taken.

`63e19ef3ddab` is referenced in **five** issues (`#5747`, `#5795`, `#5843`,
`#5846`, `#5872`) — more than any other commit in the tracker.

#### `0b0ff65d3ca1` (Refactor stream validation) — already in rc4, nothing to gain

I first dismissed this on its file list as "a refactor, not a fix". **That was
wrong, and the commit message says so.** It fixes a genuine modeset hang:
`amdgpu_dm_create_validate_stream_for_sink()` drove its RGB → YUV422 → YUV420
chroma fallback by *recursing* while toggling the shared, **unlocked**
`aconnector->force_yuv420_output` / `force_yuv422_output` and resetting them
after each recursive call. The function runs concurrently on one connector from
two paths — the connector probe worker (`->mode_valid`) and a compositor atomic
check (`dm_update_crtc_state`) — so one thread can clear the override just
before the other tests its exit condition, the exit is missed, and **validation
loops indefinitely, hanging the modeset path**. It carries
`Reviewed-by: Jerry Zuo` (the author of our HDMI patches) and sits on
`drm-fixes-7.3`.

**Verdict: rc4 already has it.** Commit dated 2026-07-21, rc4 dated 2026-09-20 —
merged in between. Every identifier the commit introduces is present in rc4
(`encoding_order`, `bpc_order`, `encoding_mask` ×13, `bpc_mask`, `is_hdmi_ep`),
the shared `force_yuv420_output`/`force_yuv422_output` fields are **gone** from
`amdgpu_dm_connector.c`, only the unrelated older debugfs knob
`force_yuv_pixel_format` remains, and the function **no longer recurses** —
only its definition line matches, no self-call. Our series tree is byte-identical
to rc4 across that function.

The reverse-apply test fails at `:2279`, which would normally read as "absent".
It is context drift from unrelated display commits between 07-21 and rc4, not
absence — **so reverse-apply is not authoritative for older commits**; grep for
the introduced identifiers instead. This is the third distinct way in one sweep
that a mechanical test gave the wrong answer.

#### Broad optimization sweep — the one clear win

Three patches, ~33 lines, one file, absent from our tree, applying cleanly to
`v7.3-rc4` with zero fuzz, **applied by Tejun Heo to `sched_ext/for-7.4`**:

| sha | date | author | subject |
|---|---|---|---|
| `b65f0cbb5` | 2026-09-21 | Usama Arif | sched_ext: Specialize the DSQ hashtable compare |
| `8ad4dc5f3` | 2026-09-21 | Usama Arif | sched_ext: Specialize the TID hashtable compare |
| `290cf02bb` | 2026-09-21 | Usama Arif | sched_ext: Specialize the scheduler hashtable compare |

The three rhashtable params structs supply no `obj_cmpfn`, so rhashtable falls
back to `rhashtable_compare()`, which reads `key_offset`/`key_len` out of
`ht->p` at runtime and emits an out-of-line `memcmp()` per element. Each patch
adds an `__always_inline` cmpfn so the compare folds to a single `cmp`. Our tree
has exactly the three structs and **zero** `obj_cmpfn`. `find_user_dsq()` is on
the `__schedule()` path. Author's in-kernel A/B on `scx_layered` DSQ ids:
**lookup 2.9× faster**. `Suggested-by: Tejun Heo`; Tejun applied all three.

Two more worth knowing:

- **`7b60a55e`** (Lijo Lazar, 2026-09-16, `lore-amdgfx`) — *drm/amd/pm: Fix
  SMUv14/15 power context allocation*. Our `smu_v14_0.c` does
  `kzalloc_obj(struct smu_14_0_dpm_context)` where `struct
  smu_14_0_power_context` is required — a **wrong-size allocation** on the DPM
  path, in a MUST-match file for this GPU. Verified present, applies cleanly.
  Unreviewed (author self-reply only).
- **Rebase hazard for the 7.4 bump:** upstream `cb145191e9d3` replaces
  `min_tso_segs()` with a `tso_segs()` CC callback. **Our `0101-cachy-bbr3.patch`
  performs that same rename itself** — so `0101` needs regeneration at the bump.
  Nothing to do at rc4.

#### mm deep-read — one clean candidate

**`b6cf1d1c5`** | David Carlier | 2026-09-20 | *mm/shmem: don't release a
swapin-error marker as a swap entry* | `lore-linux-mm`. A failed shmem swapin
frees the swap slot but leaves a `PTE_MARKER_POISONED` entry in the page cache;
on truncate or eviction `shmem_free_swap()` handed that marker to
`swap_put_entries_direct()`, which warns because it is not a swap entry.
Four lines, one file:

```c
+	const softleaf_t swp = radix_to_swp_entry(radswap);
...
+	if (nr_pages && softleaf_is_swap(swp))
 		swap_put_entries_direct(swp, nr_pages);
```

Provenance is complete: `Reported-by: syzbot+23b25ba3c6bf…`, a `Closes:`
link, `Fixes: ac2d3268284b`. No replies, no objections in any mirror.

Verified independently: the unguarded form is **live in our tree**
(`mm/shmem.c:995-996` in `_audit`), `softleaf_is_swap()` is reachable
(`mm/shmem.c:70` includes `<linux/leafops.h>`, which defines it at line 208),
and the patch passes `git apply --check` (exit 0) and `patch -p1 --dry-run -N`
against **both** pristine `v7.3-rc4` and our full series tree.

Ruled out from the same pass: the **xswap writeback RFC** (`e2b62953b`,
Baoquan He, 2026-09-20) is the next layer over the xswap v3 foundation we carry
verbatim as `2155`–`2168`, but it is RFC-only, has zero replies, depends on an
unmerged base still carrying Johannes Weiner's two stipulations, two of its 17
patches are acknowledged-incomplete, and **none of the 17 contains
`do_swapout`** — so it would not supersede local `2199`. Ridong Chen's
`94526fefe` (vmscan LRU-tail rotation) drew a serious objection from Barry Song
in v1 (un-reclaimable clean folios re-isolated forever → kswapd spin at 100%),
fixed in v2 by a refcount check, but its only `do_rotate=true` call site is the
traditional-LRU `shrink_inactive_list()` — **inert here**, where
`CONFIG_LRU_GEN_ENABLED=y` and LRU-MARIE 0.11.1r2 own reclaim. Also inert or
off-target: Zhang Peng's `shrink_folio_list()` refactor (prep only, no
functional change), `bpf_proactive_reclaim` v12 (bpf-next, Alexei objected to
selftest size), Julian Sun's foreign-bdev writeback v7 (off-target, and it
touches `mm/page_io.c`, which our swap-writeout patches also touch — rebase
risk, not a carry), `CONFIG_SPARSEMEM_CLASSIC` (we use `SPARSEMEM_VMEMMAP`, so
the new symbol is off), Yu Kuai's blk-cgroup v4 (off-target, same
`mm/page_io.c` overlap).

#### `2140` — we carry an ABANDONED revision (v5); upstream restored v4

The 2100–2199 revision audit (72 files) found exactly one row where our carried
content diverges from what upstream actually took, and it is a real divergence,
not a rebase.

- **We carry v5** (2026-09-11, `60adb47f4fa3`): a `costly_noretry` predicate that
  keeps `__GFP_DIRECT_RECLAIM` in `gfp_mask` and exempts
  `__GFP_THISNODE | __GFP_NOFAIL`. Our patch carries a comment explaining why it
  deliberately does *not* clear `__GFP_DIRECT_RECLAIM`.
- **Upstream carries v4** — linux-next `a0259b922845` and akpm-mm
  `98f58cbfaaaf`, both 2026-09-04, same subject; posted as
  `[PATCH v4]` (`lore-mirror 30646c127278`). Its shape:

```c
	if (costly_order && (gfp_mask & __GFP_NORETRY) &&
	    !(gfp_mask & __GFP_THISNODE))
		gfp_mask &= ~__GFP_DIRECT_RECLAIM;   /* exempts THISNODE only */
```

Verified against `linux-next origin/master` directly, not from the audit's
summary: no `costly_noretry` variable exists there, `__GFP_NOFAIL` is **not**
exempt, and `__GFP_DIRECT_RECLAIM` **is** cleared. These are different
behaviours, so our kernel currently diverges from upstream on this path.

**akpm dropped v5 and restored v4** in mm-unstable, and v4 is now in
mm-hotfixes-stable (Vlastimil Babka, 2026-09-18). Salvatore Dipietro, the
author, is preparing **v6 = v4 plus a further change**, which is the revision
to target once it lands.

Scope is clean: `2140` is the **only** patch in our series touching this region,
and the v4 content passes both `git apply --check` and `patch -p1 --dry-run -N`
against pristine `v7.3-rc4`. So this is a straight content swap of one file, not
a rebase. **Not done — needs your call**, since replacing a carried patch is a
removal under this project's rules. Options: swap to v4 now (matches upstream,
lands in mm-hotfixes-stable), or wait for v6.

Everything else in the range is healthy: 52 of 72 patches are already merged
upstream with identical or rebase-only payloads, and 16 have no newer revision
at all. `2101` LRU-MARIE is current (0.11.1r2, firelzrd `a05089b`), our only
delta being the local `#include <linux/kvm_types.h>` in `mm/folio.c`. `2100`
zstd is md5-identical to sirlucjan's newest v5. `2120`–`2127` (Rik van Riel gup
batching) is at the newest revision — RFC v3 — and is still unmerged, so nothing
newer exists to take.

#### `9007` — a dead carry that is silently DUPLICATING code

`9007-drm-gfx12-Program-DB_RING_CONTROL.patch` fails standalone against pristine
`v7.3-rc4` (`error: patch failed: gfx_v12_0.c:1827`) because **rc4 already has
it** — the identical block is at `gfx_v12_0.c:1842-1850`.

But the cumulative audit reports it `ok`, and that is the problem. Our patch's
hunk context is the lines *preceding* the block
(`gfx_v12_0_get_tcc_info()`, `pa_sc_tile_steering_override = 0`), which rc4
still has. So `git apply` finds a valid anchor and **inserts a second copy**
instead of failing. Confirmed in the series tree: `DB_RING_CONTROL` appears
**twice** (`_audit` `gfx_v12_0.c:1836-1844` and `1851-1859`, byte-identical),
against once in rc4.

**`audit_series.py` cannot distinguish "applied" from "applied as a
duplicate"** — a patch whose content upstream already absorbed still reports
`ok` as long as its context anchor survives. Reverse-applicability is the test
that catches this, and the audit does not run it per-patch.

**Removal candidate.** Needs explicit approval per CLAUDE.md.

#### The retry-fault carry (9011–9024) is a superseded design

Ours is the **v1** posting (2026-07-01, 14 patches). Upstream took **v4**
(2026-08-28, `[PATCH 00/11]`, merged 2026-09-02) — eleven patches, not fourteen.
v4 **silently dropped three of ours**: `9014`, `9021`, `9022` (the
`retry_cam_ack` / MMIO-ACK approach was abandoned upstream; `git log --grep
retry_cam_ack` is empty in linux-next). v4 replaces the MMIO ACK with a
**doorbell** design in `9023`/`9024` (`ih_v6_0_setup_retry_doorbell()`,
`IH_DOORBELL_RETRY_CAM`, plus an `nbif_v6_3_1.c` change). Three further real
content differences: `9011` retargeted from `ENABLE_RETRY_FAULT_INTERRUPT` to
`RETRY_PERMISSION_OR_INVALID_PAGE_FAULT` (two hunks dropped, and its remaining
hunks are GFX12.1/MMHUB4.2 — **inert on this machine**), `9012` hard-codes `1`
where ours programs `!adev->gmc.noretry` (8 sites; differs only under
`amdgpu.noretry=1`), and `9020` **drops our local `AMDGPU_PTE_NOALLOC` (MALL)
hunk**, which upstream deliberately left out. All eleven v4 patches apply clean
to rc4. Either adopt v4 or consciously keep the MMIO-ACK variant — but the
current split (v1 minus nothing, upstream at v4) is not a state to leave.

#### Two more removals / flags in 1100–1199

- **`1140` is inert on this machine.** It references `dcn42b` 23 times and
  `dcn42` 10, with **zero** `dcn401`/`dcn4` — it is the DCN 4.2B /
  `AMDGPU_FAMILY_GC_11_5_0` Strix path, exactly the class CLAUDE.md's critical
  trap describes ("applies and compiles, and does nothing here"). Also already
  merged upstream (linux-next `50eed169c`), so it is doubly redundant. Removal
  candidate, needs approval. (Already on the unapproved-removal list from the
  earlier boot sweep — this is the evidence for it.)
- **`1158`'s provenance is untraceable.** Our patch header claims
  `dfd0e5aa6aadcd477ccca12dcc1433a76aa8d543` (Sultan Alsawaf, 2025-08-25), and
  the ledger repeats that sha — but it **exists in no tree and no mirror** we
  hold (`linux-next`, `torvalds`, `drm-next`, `amd-staging-drm-next`,
  `agd5f-linux`, `lore-mirror`, `lore-dri-devel`, `lore-amdgfx`). Sultan
  Alsawaf is an out-of-tree contributor (kerneltoast), so the commit plausibly
  lives in a GitHub repo we do not clone — meaning **unverifiable from our
  sources**, not necessarily fabricated. Per CLAUDE.md's spirit, re-derive it
  or drop it rather than carry an unverifiable sha.

**Validated as correct, keep:** `1164` (our MCCS revert) — upstream has **not**
reverted it; the target content was re-applied as `ac3aea794fb4`, so the revert
is still live and still needed. And `1165` + `1167` together equal upstream's
split pair (`fb1b272db` + `532823d7b`) exactly.

#### `1140` — REMOVED 2026-09-21 (inert on this hardware)

`1140-drm-amd-display-clamp-force_min_dcfclk-to-dcn42b-range.patch` patched
exactly one file, `dc/clk_mgr/dcn42b/dcn42b_clk_mgr.c`, and the series is
gated on `ctx->dce_version == DCN_VERSION_4_2B` (`clk_mgr.c:343`, `:454`). The
running kernel reports **DCN 4.0.1**. The Makefile compiles the file
unconditionally, so it *builds* — it is never *executed* here. That is
CLAUDE.md's critical trap verbatim.

Removed with the user's explicit approval: dropped from `source=()`, file
deleted, `updpkgsums` re-run (arrays realign at 278/278), series now **274**
patches. Cumulative audit re-run on a separate worktree: **274/274 clean, exit
0, zero skips/reversals/fuzz**.

#### `1158` — provenance RESOLVED, and it stays

Previously flagged as untraceable: the header claims
`dfd0e5aa6aadcd477ccca12dcc1433a76aa8d543` (Sultan Alsawaf, 2025-08-25) but no
kernel tree or lore mirror holds it. **It is real** — GitHub commit search
resolves it to `kerneltoast/kernel_x86_laptop`, the author's own repo, which is
simply not a source we clone. Fetched the commit from GitHub's plain patch
endpoint and compared change-lines: **23 vs 23, identical set**. Our copy
reproduces it faithfully.

Still needed, verified against rc4's source: `dmub_srv_wait_for_idle()` still
has `udelay(polling_interval_us)` with `polling_interval_us = 1` in a loop up to
100 ms, and the fix is not upstream. Applies standalone to pristine rc4. Our
copy is correctly based — it *removes* the `polling_interval_us` constant, which
is present in rc4. Developed on Strix Halo, but `dmub_srv_wait_for_idle()` is
generic DMUB code that every DCN generation uses, this one included.

**Lesson for the ledger: "exists in no tree or mirror" must not be recorded as
"fabricated".** Two of the three untraceable-provenance flags raised this sweep
were personal GitHub repos (see also the CRIU case in `LESSONS.md`). Check
GitHub before concluding a sha is invented.

#### Removals and drop-list from the revision sweep

- **`0112` (cachy-amdgpu-avoid-evicting-resources-at-S5) — drop candidate.**
  CachyOS reverted its own change (`bd3b950c5b0f`, 2026-08-17, *"Revert 'Merge
  branch '7.2/s5-power'…'"*), and the revert deletes **exactly our 4-line
  hunk**. It exists in no current CachyOS branch. Needs explicit approval.
- **Drop at the 7.4 bump — already merged in linux-next, absent from rc4:**
  `2005` (`92344fad5b54`), `2413` (`8b9b3698796a`), `2414` (`8848333264b7`),
  `2415` (`c659e506f9a7`). All byte-identical to the merged commits. Note `2415`
  is *newer in effect* than the v3 mail: Tejun took the function form
  `__scx_kf_allowed_ctx()` over the statement-expression macro, and our carry
  already matches the merged shape.
- **Watch, not settled:** `2014` — the author withdrew it in favour of Keith
  Busch's `blk_op_bypass_sched()` refactor, which has not been posted as a patch
  yet. Keep it for now; do not treat it as final.
- **`0101` (bbr3) rebase hazard confirmed for 7.4:** upstream `cb145191e9d3`
  changes the `tso_segs` shape (prototype `u32 (*tso_segs)(struct sock *sk, u32
  mss_now)`, `READ_ONCE`, `clamp_t`) whereas ours matches CachyOS's (`unsigned
  int mss_now`, no `READ_ONCE`, `min_t`). Nothing to do at rc4.

Verified current, no action: `0001`–`0007`, `0031`–`0034` (local, author/
`Signed-off-by`/`Assisted-by` correct); `0010` (upstream AMD post; content
confirmed still absent from rc4); `0102`, `0103`, `0111` (still carried by
CachyOS on the 7.3 line); `2000`–`2004` (byte-identical to sirlucjan's newest
7.3-rc carry, not merged); `2006`–`2013`, `2015`, `2016`; `2200` NAP (v0.5.0 is
the newest that exists, byte-identical, and there is no `7.2/` or `7.3-rc/` NAP
directory); `2302`–`2321` (v3 is latest, all 20 diff-bodies identical, no v4);
`2400` (not merged); `2505`.

**`2600`–`2699` is an empty range** — no patches. Worth noting so no future
sweep goes looking.

#### `1065`/`1066` — NOT superseded. The maintainer defended them.

A sweep pass reported these as "genuinely superseded" by a three-part series
posted 2026-09-17 (cover `17f8c1fa50b4`: reverts `c091c58ee996` +
`9e785a48cb21`, replacement `bf951301d32f`). **That framing is wrong, and acting
on it would have replaced working code with a rejected design.**

Christian König's reply, `5de2a7d1` (2026-09-17, `lore-amdgfx`), on the
replacement hunk:

> That doesn't work like this.
>
> The problem is that dma_resv_reserve_fences() allocates memory and that in
> turn can invalidate the eviction fence we just created again.
>
> **The patches you want to revert actually look correct to me.** The fence
> slots usually needs to be reserved directly after we locked the BOs.

The revert series exists but is **rejected, not accepted**; it is in no tree
(amd-staging tip is 09-14, the series was posted 09-17). Our carries are
byte-identical to the amd-staging copies (`118037152820`, `00af92666f29`).
**Keep them.** This is the second time a sweep has read "a newer posting
exists" as "ours is superseded" — a *revert* of a carried patch is the opposite
of a supersession, and must be checked for maintainer objection before any
conclusion is drawn.

#### `1158` — one more fact: CachyOS dropped it (no reason given)

Provenance is settled (kerneltoast repo, verified identical, see above). But the
same content also lived in CachyOS `7.1/cachy` as `fe0c46c5a03b`/`bb8ee041e40e`
and was **reverted on 2026-05-01** by Eric Naim (`dd5e72df5d64`,
`5aecdca15236`, `0bb166ba01aa` — three branches, same day). The revert carries
**no reason**: just *"This reverts commit bb8ee041e40e."* plus a `Signed-off-by`.
Three same-day reverts across branches is the signature of a rebase that dropped
the patch, not a technical objection. `7.3/base` does not carry it.

Verdict: **keep** — rc4 still has the 1 µs busy-wait loop the patch removes, the
fix is not upstream, and it applies standalone. But it is a
carry-at-discretion item: one downstream dropped it without documenting why.

#### Remaining ranges — 1000–1099 and 1200–1299

- **`1200`–`1299` (24 patches): nothing newer, nothing to take.** No CPPC v8
  exists; `1230` is at v3 (newest); `1201`–`1203` were never posted to any list
  or mirror we hold.
- **`1027` has a v2** (`5db5edb876849cac1c22fc6f08a622f96fdf7ef2`): the
  force-completion loop walks `i < AMDGPU_MAX_MES_INST_PIPES` instead of only
  `ring[0]`. Ours is the narrow form. Small robustness fix; applies with fuzz 1.
- **`1063` has a v2** (`0242f8ca0d705eba63567d924df2365168ad1c91`) — comment
  reword only, 4 lines → 5. Cosmetic.
- **TLB V3 parts 17–20** (`43ca6cc668e7`, `eec49884e9f4`, `4bc39facf85b`,
  `d2f5a60edde`, cover `abee57dc9a9a`) would supersede our `1013`–`1017` with
  `enum amdgpu_tlb_inv_method` + `adev->gmc.gart_inv_method` in place of our
  function-pointer helpers. **Still at review stage** — `AMDGPU_TLB_INV_METHOD`
  appears in no tree. A coordinated 23-patch swap, not a drop-in; revisit at the
  7.4 bump. `1004`–`1012` are rebase-only.
- `1056`/`1060` are byte-identical to their merged tree copies; `1058` is
  unchanged at its pixelcluster origin.

#### Correction: the fence patch was ALREADY carried as `1064`

I earlier listed Donggeun Yoo's *"drm/amdgpu: don't release the fence reference
consumed by the scheduler"* (from drm/amd `#5870`) as a candidate to **add**.
That was wrong — it is already in the series as **`1064`** (ledger row 91, same
author, msgid `20260910054551.634054-1-donggeunyoo.kernel@gmail.com`). Compared
added-line sets: identical. Nothing to add.

It is also still doing work: rc4 still has the double-put at
`amdgpu_cs.c:1306-1308` (`dma_fence_put(fence)` on the error path after
`drm_sched_job_add_dependency()` has already consumed the reference), and
`sched_main.c:701` puts the fence when `xa_alloc()` fails. So `1064` is a live
carry, not a candidate.

**Lesson: before proposing a patch, grep the series for its subject and author.**
A candidate surfaced from an issue tracker looks "new" even when we have carried
it for days. Two separate agents and I all missed this.

#### Automated duplicate detection does NOT work — do not retry these

Four approaches were tried to find `9007`-class dead carries programmatically.
All failed; record them so no future sweep burns time:

| approach | failure mode |
|---|---|
| reverse-apply each patch to pristine rc4 | **false negatives** — `9007` forward-fails, so it cannot reverse-apply either. Reported "none" while a known duplicate existed. |
| added-block present contiguously in rc4 | **both** — `9007` missed because `*/` is a *context* line inside its added block, breaking contiguity; `1064` falsely flagged because its addition (`if (r)` / `return r;`) is generic and matches elsewhere. |
| count of a distinctive added line > rc4_count + 1 | **false positives** — a patch legitimately adding the same line in two functions trips it. 84 KB of suspects, nearly all valid. |
| sliding 5-line window: once in rc4, twice+ in series | **false positives** — every legitimately *inserted* block whose lines also occur elsewhere (zstd merge, xswap series) is flagged, and one insertion produces W overlapping windows. |

The reliable methods remain **reading the code** and the cumulative audit.
`9007` was found by grepping the series tree for the register it programs and
seeing it twice. A cheap targeted variant that does work: after a rebase, grep
the series tree for the *distinctive symbol or register* each patch is named
after and confirm it appears the expected number of times.

#### REMOVED 2026-09-21: `9007` and `0112` (user-approved)

Two patches removed with explicit approval; series **275 → 272**.

**`9007-drm-gfx12-Program-DB_RING_CONTROL.patch` — a duplicate.**
rc4 already had the change; our copy's context anchor survived, so it inserted a
second byte-identical `DB_RING_CONTROL` block. Verified fixed:
`_audit272`'s `gfx_v12_0.c` now contains the block **once** (it read twice
before). This is the failure mode `audit_series.py` cannot see — it reported
`ok` throughout. Full write-up in `LESSONS.md`.

**`0112-cachy-amdgpu-avoid-evicting-resources-at-S5.patch` — reverted
upstream, and behaviourally redundant.** CachyOS reverted its own change
(`bd3b950c5b0f`, Peter Jung, 2026-08-17, reverting the whole `7.2/s5-power`
branch merge), and the revert deletes exactly our 4-line hunk. Checked before
removing, because unlike the others this one changes behaviour: neither rc4
**nor upstream `linux-next`** (the 7.4 queue) has a `SYSTEM_HALT` term — both
carry only

```c
	/* No need to evict when going to S5 through S4 callbacks */
	if (system_state == SYSTEM_POWER_OFF)
		return 0;
```

so ours added a case upstream deliberately does not have. Removing it aligns us
with both upstream and CachyOS. Verified: `SYSTEM_HALT` is now absent from
`_audit272`'s `amdgpu_device.c`.

Both removals followed the full sequence — `source=()` entry, patch file, root
symlink, `updpkgsums` (arrays realign), then a fresh cumulative audit:
**272/272 clean, exit 0**, and `verify.py` fast tier passes.

**Still open, needing a decision:** `2140` (we carry the abandoned v5; upstream
restored v4 and a v6 is pending) and the retry-fault v4 swap. Neither was
approved for this pass.

#### `1027` — a SECOND dead carry of the same class, NOT yet removed

Found while evaluating the sweep's "1027 v2 is worth taking" recommendation. That
recommendation was based on comparing v1 against v2 — but **rc4 already has v2's
code**, and more:

```c
	/*
	 * MES scheduler rings have no drm scheduler, so they are missed by the
	 * loop above. Realign their polling fence too (one per XCC), otherwise the
	 * first post-reset submission polls forever on a stale seq. …
	 */
	for (i = 0; i < AMDGPU_MAX_MES_INST_PIPES; i++) {
		struct amdgpu_ring *mes_ring = &adev->mes.ring[i];
		if (mes_ring->fence_drv.initialized && mes_ring->sched.ready)
			amdgpu_fence_driver_force_completion(mes_ring, fence);
	}
```

rc4 carries that loop **plus** an equivalent KIQ loop. Our `1027` (v1) adds a
`mes.ring[0]`-only force-completion that the loop now supersedes:

| | rc4 | our series tree |
|---|---|---|
| `AMDGPU_MAX_MES_INST_PIPES` loop | 1 | 1 |
| `mes.ring[0]` | **0** | **3** (our v1's block) |

So `1027` is the same defect as `9007` — a carry whose purpose upstream has
absorbed, adding redundant work on top. It also fails standalone against
pristine rc4 (`patch does not apply` at `amdgpu_device.c:4988`), which is the
signal.

Attribution checked: `1016` and `1017` contain `mes.ring[0]` only as *context*
`-` lines (0 added); `1027` is the only patch that adds it.

**REMOVED 2026-09-21**, under the user's standing authorisation to remove any
patch that passes verification. Five checks, all passed:

1. fails standalone against pristine rc4 (`patch does not apply` at
   `amdgpu_device.c:4988`) — the signal for a carry whose content upstream has;
2. applies cumulatively (the series audit reaches it);
3. rc4 carries superseding code — the `AMDGPU_MAX_MES_INST_PIPES` loop **and** an
   equivalent KIQ loop;
4. count check: `mes.ring[0]` is **0** in rc4, **3** in our tree;
5. removal preserves function — rc4's loop already covers `ring[0]`, verified by
   `mes.ring[0]` reading **0** in the post-removal series tree while the MES loop
   is still present.

Series **272 → 271**; `pkgrel` 3 → 4. Cumulative audit re-run: **271/271 clean**,
and `verify.py`'s fast tier passes.

Worth noting how it was found: not by the revision audit, which compared v1 to
v2, but by grepping the series tree for the symbol the patch is named after —
the targeted check recorded in `LESSONS.md` as the one method that works.

### drm/amd tracker, 2026-09-22 — nothing to carry, one confirmation

**No new on-target fix, no candidate absent from our base, and no revert of
carried work.** All 49 issues updated since 2026-09-20 were pulled in full.
Every real on-target commit cited is either already in `v7.3-rc4` or already
carried (`1064`). Grepping all 49 for our carried patches' identifiers (MCCS
FreeSync cap, `passive_vrr`, `DB_RING_CONTROL`, `9051`/`9052`, `dmub_srv_wait_for_idle`,
`mqd_prop`, HUBP plane-addr) returned **zero hits** — no maintainer objection and
no upstream revert touching the series.

**The display fix confirmation is now much stronger.** `63e19ef3ddab`
("Atomize IRQ register read/modify/write ops") is cited in **24 issues**, not
the five previously recorded. Mario Limonciello posted a blanket reply across
the whole `flip_done`/pageflip family on 2026-09-21: *"Could you please retest
this on kernel 7.3-rc4 or later? There is a fix that may address this issue"* —
pointing at the **merged** commit. In `#5843` the reporter found the posted
patch **would not apply** ("some lines could not be applied") and Limonciello
replied that CachyOS may backport it early. Our base sidesteps that entirely,
and **the `1159` drop at the rc4 rebase is confirmed correct from the vendor
side**.

New on-target threads, all additional reports of that same family: `#5718`
(Navi 48 dual-DP `flip_done timed out`), `#5647` (pageflip, one display
freezes), `#5511` (9070xt pageflip), plus `#5762` — a **Navi 48** 4-GPU box
where wrong VFCT selection causes a black screen. None carries a fix.

`29393ab0e49f` ("Promote DC to 3.2.397") is real but exists only on
`amd-staging-drm-next`/`agd5f-linux`; it is a Krackan reporter's custom-kernel
pin, not a candidate. The `#5663` DCC/Navi-4x SDMA workaround still has no
upstream commit — König attributes it to a **hardware** bug — so that verdict
stands unchanged.

**Method gap found and fixed in the skill:** the documented query
`?state=opened&per_page=100` returns only **page 1** — the newest 100 by
*creation* date — while the project holds **1808** open issues. An old issue
updated recently is invisible to it. `updated_after=2026-09-20` returned 49
issues; only 24 were on page 1, and the missing 25 included the three on-target
threads above, missed for several passes. The skill now filters by update time.

### `next-20260922` — three findings, none carried

**1. The sched-ext hashtable trio is MERGED — do not carry it.** The three
Usama Arif patches recommended as "the one clear win" on 2026-09-21 are now in
`next-20260922`: `e4c5ba819d3c` (DSQ), `daaab0f42e2e` (TID), `b9e602f30bea`
(scheduler). They arrive at the 7.4 bump on their own; carrying them now would
mean maintaining a patch that upstream already has. **Supersedes the earlier
"worth carrying" note.**

**2. Our `1227` is now upstream.** `4bcc60d326c5` — *"ACPI: CPPC: Accept requests
to retain immutable autonomous selection"* — is byte-for-byte our `1227`'s
subject in `next-20260922`, alongside Christian Loehle's other CPPC commits
(`995e7d468070`, `21e018235d99`). **The CPPC v7 series (`1210`–`1229`) is
landing; drop it at the 7.4 bump.** Note this is also the patch that already
fixed the amd-pstate TOCTOU we rejected `1231` for.

**3. r8169 will enable EEE by default — and that cuts against our policy.**
`5f22f5fb9051` (Javen Xu, **Realsil** — the chip vendor), 2026-09-16, in
`next-20260922`:

```c
	tp->phylink_config.lpi_capabilities = rtl8169_get_lpi_caps(tp);
+	tp->phylink_config.eee_enabled_default = !!tp->phylink_config.lpi_capabilities;
```

`eee_enabled_default` exists in rc4 (`include/linux/phylink.h:179`) but
`r8169_main.c` does **not** set it — so the patch turns EEE on at probe for any
EEE-capable part, and **this machine's RTL8125B is one** (`ethtool --show-eee`
reports 100/1000/2500baseT supported, currently disabled).

We disable EEE **deliberately**: `sleepy-next/net-tune/README.md` records that
switching EEE restarts auto-negotiation and drops the link for ~3 s, which from
the NetworkManager dispatcher landed exactly when blocky resolves its DoQ
upstream and left DNS broken ~11 s after login. `net-tune-eee.service` turns EEE
off *before* NetworkManager for that reason.

**Not carried — it does the opposite of what we want.** At the 7.4 bump it
arrives whether we want it or not, so **verify then that `net-tune-eee.service`
still turns EEE off cleanly with no boot flap**; the service runs while the link
is down, which is why it has been flap-free, but the driver's default changing
underneath it is worth one measurement.

### `2041` — SWAPPED v2 → v4 (2026-09-22)

*net: gso: limit recursive IP-in-IP segmentation.* The only carried patch in the
whole 271 that had a genuinely newer revision this sweep, and the upgrade is a
strict simplification.

| | our v2 | upstream v4 |
|---|---|---|
| mechanism | `gso_header_len_add()` + a `skb_gso_segment_cb()` wrapper, with ~14 call-site checks | `#define GSO_MAX_HEADER 256` + `gso_header_len_exceeded()`, checked only at the two IP GSO entry points |
| added lines | 83 | **15** |
| files | 10 | 3 (`include/net/gso.h`, `net/ipv4/af_inet.c`, `net/ipv6/ip6_offload.c`) |

Zihan Xi, `[PATCH net v4 1/1]`, 2026-09-22, `02ede8ffda7c` (`lore-mirror`) /
`5ab3aa25815c` (`lore-netdev-new`), cover `7bb4b593a3b3`.

**The 2026-09-21 deferral to the 7.4 bump is obsolete** — it was based on v3
predating rc4. v4 is written against rc4 and applies to it directly.

**v4 is the version the reviewer asked for.** Willem de Bruijn, reviewing v3:

> This is a lot of code change compared to v1, a simple recursion counter. Wang
> already suggested a simplification. **If the previous approach could be tested
> at only the two network header callbacks, then this likely can too.** By just
> bounding `skb_network_header - skb_mac_header`? Or `skb->data`.

v4 bounds the header length at exactly those two callbacks. So this is not
merely a newer revision — it is the shape the maintainer requested, which is a
stronger reason to take it than the version number alone.

Trailers: `Fixes: 3347c9602955`, `Reported-by: Vega`, and two `Signed-off-by`
(Luxing Yin, Zihan Xi).

Verified: `git apply --check` rc=0 and `patch -p1 --dry-run -N` rc=0 against
pristine `v7.3-rc4`; cumulative audit **271/271 clean, exit 0** after the swap;
in the resulting series tree `gso_header_len_exceeded` appears once in each of
the three files and `gso_header_len_add`/`skb_gso_segment_cb` appear **zero**
times — the old API is fully gone. Applied over our v2 it fails loudly on all
three files, so there is no silent double-apply risk.

Same number, filename and series position kept, per the `patch-audit` skill.
`pkgrel` 4 → 5.

*Coverage caveat from this sweep, for the record:* `drm-next` and `drm-misc`
re-fetches failed with git protocol errors (`fatal: expected
'acknowledgments'`). Their recorded tips (drm-next `2446a767f` 09-17,
drm-misc-next 09-21) are at or before the window, and all postings were still
covered through the lore mirrors, so the conclusion holds — but a working
re-clone is worth doing before acting on any GPU patch from those trees.

### Alignment with upstream-merged versions — what was taken and what was not

Asked to align carried patches with the versions upstream actually merged,
**safely**. Surveyed every carry where ours differs from the merged commit:

| ours | merged upstream | decision |
|---|---|---|
| `2041` v2 | **v4** | **TAKEN** — strict simplification, reviewer-requested shape, 83→15 added lines |
| retry-fault `9011`–`9024` v1 (14) | **v4** (11) | **not taken** — see below |
| `2140` v5 (abandoned) | **v4** | **not taken** — v4 is *contested*, not settled |

**Retry-fault v4 — deliberately not swapped, and the reason is coupling.**
It looked like a clean alignment, but the pieces are not separable:

- v4 replaces the MMIO-ACK approach with a **doorbell**, allocating
  `adev->irq.retry_cam_doorbell_index = (adev->doorbell_index.ih + 2) << 1`.
- To make room, it **must** widen the IH doorbell range —
  `nbif_v6_3_1.c`, `S2A_DOORBELL_PORT1_RANGE_SIZE` **2 → 8**.
- That branch runs when `use_doorbell` is true, and our IH reaches it through
  `ih_v7_0.c:350` → `adev->nbio.funcs->ih_doorbell_range()`. So it is **live
  code for this machine**, not dormant.

A partial swap would leave the doorbell allocated without the wider range; a
full swap rewrites live interrupt handling on this GPU — retry-CAM enablement,
the IH doorbell range, and it drops our local `AMDGPU_PTE_NOALLOC` (MALL) hunk
in `9020`. Our v1 works today.

**And the benefit is temporary.** At the 7.4 bump the base itself carries the
merged v4, so any alignment gained now evaporates while the risk is taken now.
**Defer to the bump**, which is exactly what the earlier sweep recommended.

**`2140` likewise stays.** Upstream restored v4, but v4 was pulled *back out* of
mm-hotfixes-stable into mm-hotfixes-unstable — Vlastimil Babka now says to
target 7.4 rather than treat it as an urgent 7.3 fix — and a real objection
stands on MIGRATE_HIGHATOMIC grounds (v4 lets
`__GFP_DIRECT_RECLAIM|__GFP_NORETRY` costly-order attempts eat the highatomic
reserves). Matthew Wilcox: *"still piling hack on hack."* Contested, not
settled; keep waiting.

**The one thing worth stating plainly:** every carry that is already merged
upstream *and byte-identical to the merged commit* (`9072`–`9075`, `9019`,
`9050`, `1056`, `1060`, `2005`, `2413`–`2415`) needs **no action at all** —
aligning them with upstream is a no-op, because our copy *is* upstream's. They
belong on the 7.4 drop list, not on a swap list.

### Removed 2026-09-23 — 12 patches for IP blocks this machine never instantiates

A scan for patches whose **every** touched file belongs to another chip's code
found 14; two were false positives and were kept (below). The other 12 modify
code in IP blocks that are never constructed on this GPU.

The kernel states its own versions at boot:

```
amdgpu: detected ip block number 1 <gmc_v12_0_0> (gmc_v12_0)
amdgpu: detected ip block number 5 <gfx_v12_0_0> (gfx_v12_0)
amdgpu: detected ip block number 7 <sdma_v7_0_0> (sdma_v7_0)
[drm] Display Core v3.2.392 initialized on DCN 4.0.1
```

`lspci` shows exactly one display device (Navi 48, `1002:7550`); the Ryzen 7
7700 exposes no integrated GPU here, so there is no second amdgpu instance that
could reach gfx11/gmc11 code. Every removed patch touches **only** files for a
block in neither list:

| Removed | Target | This machine |
|---|---|---|
| `1004` `1005` `1006` | gmc_v9_0 / gmc_v10_0 / gmc_v11_0 | `gmc_v12_0` |
| `1015` `1016` | gmc_v10_0 / gmc_v11_0 (tlb inv helpers) | `gmc_v12_0` |
| `1009` `1010` `1011` | sdma_v5_0 / sdma_v5_2 / sdma_v6_0 | `sdma_v7_0` |
| `9073` | sdma_v6_0 (detect_hung_queue) | `sdma_v7_0` |
| `9017` | gmc_v11_0 (cam_index) | `gmc_v12_0` |
| `9064` | gfx_v11_0 (userq refs) | `gfx_v12_0` |
| `1135` | `dcn42/dcn42_dio_link_encoder.c` | DCN 4.0.1 |

Each is the unused sibling of a per-chip series whose ours-chip member stays:
`1007` (gmc12), `1012` (sdma7), `1017` (gmc12), `9018` (gmc12), `9065` (gfx12),
`9074` (sdma7). Verified before removal that no shared symbol is orphaned —
`1008` and `9072` only add struct **function pointers**, so the unused slots
stay NULL rather than undefined, and `1014` *re-adds*
`amdgpu_gmc_flush_gpu_tlb_helper` (a move, not a deletion) so the `.flush_gpu_tlb`
assignment every GMC file still carries keeps resolving.

**Two were kept as false positives.** `1142` and `1143` touch `dcn/dce/dce_i2c*`,
which the name suggests is legacy pre-DCN code — but `dcn401_resource.c` includes
`dce/dce_i2c.h` and builds `dcn401_i2c_hw_create()` on it. `dce_i2c` is shared
by every DCN generation including DCN 4.0.1, so both are **live**. This is the
"confirm the subsystem is actually owned by the code you are patching" trap, and
a filename is not evidence of ownership.

### Adopted 2026-09-22 (second pass) — four fixes, all verified in series order

The 2026-09-22 tree/branch sweep surfaced six on-target candidates. Four were
carried; every one was tested **in series order** against the fully-applied
271-patch tree, which is the test that caught `1231`'s earlier redundancy.

| # | patch | why it is on-target |
|---|---|---|
| `1231` | `cpufreq: amd-pstate: Restore previous mode when changing driver mode fails` | amd-pstate is this machine's cpufreq driver |
| `1232` | `cpufreq: amd-pstate: Propagate cppc_set_auto_sel() errors on mode change` | same driver |
| `2045` | `net/sched: sch_cake: prevent shaper corruption and stall in cake_overhead()` | **CAKE is our SQM** — `sleepy-next/net-tune/` runs it on the RTL8125B path |
| `9076` | `drm/amdgpu: fix ip discovery table validation` | `amdgpu_discovery.c` is how Navi 48 enumerates every IP block |

**`2045` — three real defects in CAKE's shaper, live in rc4.** Confirmed against
rc4's `cake_overhead()`: `unsigned int hdr_len` lets a negative offset wrap; the
`segs == 1` test misses `segs == 0`, underflowing the shaper interval; and an
unset transport header returns the `~0U` sentinel, inflating the computed length
to ~66 KB. Carries `Fixes: a41851bea7bf`, `Cc: stable`, and `Signed-off-by`
(Yuchao Zhang, v2). **`sch_cake.c` is otherwise untouched by our whole series**,
so this is purely additive. `2045` sits with the other `net-sched-*` patches
(`2039`, `2040`).

**`1231`/`1232` — the amd-pstate pair.** `amd_pstate_change_driver_mode()`
unregisters the active driver *before* registering the requested mode, so a
failed registration returned the error leaving **no scaling driver at all**;
`1231` re-registers the previous mode and still reports the original error.
`1232` stops discarding `cppc_set_auto_sel()`'s return value, which previously
let a firmware rejection be recorded as a successful transition. Both are Mario
Limonciello's, both Sashiko-reported with `Closes:`/`Fixes:` trailers.

**They carry upstream's `[PATCH 1/4]` and `[PATCH 2/4]` subjects deliberately.**
They are 2 of that series' 4 parts: part 3 (`3bd87e32b2e4`, the TOCTOU) is
**redundant with our carried `1227`** and was rejected as `1231` earlier in the
day; part 4 is a `amd-pstate-ut` unit test. Keeping upstream's numbering intact
is what CLAUDE.md rule 4 requires, and `verify.py` states it explicitly.

**`9076` — the strongest provenance of any AMD candidate this sweep**:
`Reviewed-by: Frank Min` and `Signed-off-by: Alex Deucher`. It adds missing
`&& table_size` / `&& size` guards in `check_table`, `get_mall_info` and
`get_vcn_info` — the tables this GPU's IP discovery walks.

All four: `git apply --check` rc=0 **and** `patch -p1 --dry-run -N` rc=0 against
pristine `v7.3-rc4`; reverse-apply fails (genuinely new); each applies cleanly
**in series order** against the applied tree. Cumulative audit after adding all
four: **275/275 clean, exit 0.**

**Two candidates from the same sweep were NOT carried:** the io_uring trio (two
are unreviewed and the third has a reviewer-requested change pending) and the
`page_alloc` reserve pair from Johannes Weiner, which Babka and Wilcox were both
still reviewing on 2026-09-22 — expect a v2. Also noted: `b959ffd01324` (shmem
swapin marker) is now in `mm-unstable` and will arrive on its own.

### Ledger corrections (2026-09-22)

- **`1056` belongs on the 7.4 drop list.** It is already merged upstream: applied
  to drm-misc-next 2026-08-18 per the author's own reply, and `next-20260922`
  carries the locked `drm_sched_entity_is_idle()` at `sched_entity.c:208`.
  `1060` likewise. The drop list at the top of this file named only `2005`,
  `2413`, `2414`, `2415`.
- **`1026` was dropped at the rc4 rebase** (`8e1d5fa` — "its upstream fix landed
  as a null guard rather than the reconstruction we carried") but the ledger
  still lists it in the table and describes it in the present tense. The 39 rc4
  drops exist only in the commit message; the rc3 round has a "Dropped" section
  and rc4 does not.

### Evaluated 2026-09-22 — not carried, awaiting v2

**`blk-mq: set RQF_USE_SCHED when the operation is known`** — Keith Busch,
`[PATCH]`, 2026-09-21, `2a907b7cf18ca64913fd5a026a32e435fa3adef1` on
`lore-linux-block`. **Directly on-target: kyber is this machine's io
scheduler.**

A cached request is allocated for one operation but can be handed out for
another. A passthrough command has `RQF_USE_SCHED` cleared, so using those
flags for a subsequent read/write bio inserts it into the scheduler without
`->prepare_request()` and frees it without `->finish_request()`. The author's
words: *"For kyber, this leaks the domain token acquired at dispatch and
**stalls the queue**."* Carries `Cc: stable`, `Reported-by: Henry Hu`, and
`Fixes: 4b6a5d9cea91` — which is Jens Axboe's **2022-09-21** commit, present in
rc4, so the bug is live here. rc4 has the buggy `data->rq_flags |=
RQF_USE_SCHED;` at `blk-mq.c:526`.

**Why not carried: the reviewer asked for restructuring.** Christoph Hellwig:
*"This looks generally good, but also a bit hard to follow"*, then three
requests — update/remove the `blk_mq_rq_ctx_init` comment in mq-deadline,
consider combining `blk_mq_rq_time_init` with `blk_mq_set_rq_sched`, and move
the `op_is_flush` check removal to a documented follow-on patch. A v2 that
differs materially is therefore coming, and carrying this revision would mean
churning it next sweep. The bug is four years old and needs a passthrough
command's cached request to be reused for a bio, so it is rare in practice.

**Re-check at the next sweep for the v2.**

*Extraction note:* this mail is `Content-Transfer-Encoding: quoted-printable`.
Extracted raw it looks malformed; QP-decoded it is 10 clean hunks and
`git apply --check` exits 0. See `LESSONS.md` — this is the third distinct way
a lore mail has silently produced a broken patch.

### 7.4 bump hazards found in the 2026-09-22 sweep

**The `__swap_writepage()` → `__swap_writeout()` rename will break `2101`.**
linux-next carries `a310a5fb79b3` (Tal Zussman, 2026-08-29) — *"mm/swap: rename
`__swap_writepage()` to `__swap_writeout()`"* — across `mm/page_io.c`,
`mm/swap.h`, `mm/swapfile.c` and `mm/zswap.c`. It is **not** in `v7.3-rc4`, so
it lands at 7.4.

This originally listed three patches. **Two of them are gone** — `2199` and the
`2155` xswap foundation series were removed on 2026-09-22 when the backend
moved to zswap + a swapfile, so the exposure is now a single patch:

- `2101` (LRU-MARIE) — the only carried patch still referencing the old name;
  verify with `rg -l '__swap_writepage' sleepy-next/patches/` at the bump.

**Action at the 7.4 bump: rename the symbol in those three patches** (and check
`PATCH_SOURCES.md`'s `2199` analysis section, which quotes
`__swap_writepage()` in prose). This is a mechanical rename, but it is easy to
miss because the patches apply cleanly to rc4 right now.

**The shmem swapin-marker fix has merged upstream.** `b959ffd01324` (David
Carlier) — *"mm/shmem: don't release a swapin-error marker as a swap entry"* —
is now in `linux-next origin/master`. We evaluated it as a candidate on
2026-09-21 (`b6cf1d1c5` on `lore-linux-mm`, verified applicable and clean) but
did not carry it. **It will arrive on its own**; do not re-evaluate it as new.

#### Method notes (both cost real time here)

The GraphQL endpoint enforces a **query complexity cap of 200**. Asking for
`title description notes { nodes { author { username } body } }` on 15 issues
needs complexity 211 and returns a single error object with **no partial
data** — 90 of 100 issues came back empty and the script still reported
success. Batch at 10. `notes.nodes.author` is what pushes it over.

**Every clone in `repos/` is shallow** (`rev-parse --is-shallow-repository`
returns true for `linux-next`, `torvalds`, `amd-staging-drm-next`,
`agd5f-linux` and `drm-next`). So `merge-base --is-ancestor` is unreliable in
all of them, not just some — it reported three 2022–23 commits as absent from
rc4. Use forward/reverse applicability, or read the code.

## `2199` — the xswap writeout guard, for the path MARIE added

**Our patch.** Author `Sleepy <sleepy@localhost>`, `Assisted-by: Claude`.
It fixes a NULL-mempool panic reachable from two kernel threads; there is no
upstream patch for it (see below).

### The panic

Two oopses on 2026-09-20, `kcompressd0` and `kswapd0`, identical faulting
instruction: `mempool_alloc_noprof+0x9a`, both from `swap_add_folio()`. Registers
agree on a NULL pool — `R14`/`RDI` = 0, `CR2` = 0x18 (`pool_data`), `RSI` =
`0xc00` (`GFP_NOIO`). Afterwards the machine had **no `kswapd` at all**.

### Why the pool is NULL

`sio_pool` is initialised by `sio_pool_init()`, which has exactly **one caller
in the tree**: `setup_swap_extents()` in `mm/swapfile.c`, reachable only from
the file/block `swapon()` path. xswap devices are created through
`/sys/kernel/mm/xswap/create` — `2159` explains why: *"xswap devices have no
backing storage, so there is no file to swapon."* `xswap_create()` builds the
`swap_info_struct` by hand and never calls `sio_pool_init()`. On a machine whose
only swap is xswap, `sio_pool` is NULL for the whole uptime.

### Why the existing guard does not cover it

`2155` does guard the write path — in `swap_writeout()`:

```c
	if (unlikely(__swap_entry_to_info(folio->swap)->flags & SWP_XSWAP)) {
		folio_mark_dirty(folio);
		return AOP_WRITEPAGE_ACTIVATE;
	}
	__swap_writepage(ctx, folio);
```

That covers stock reclaim. It does not cover `do_swapout()`, which `2101`
(LRU-MARIE) adds and which calls `__swap_writepage()` **directly**:

```c
	} else
		__swap_writepage(ctx, folio); /* straight past the guard */
```

`do_swapout()` has two callers, both from kswapd: `do_swapout_batch()` (the
kcompressd drain) and `kcompressd_store()`'s synchronous fallback. The latter
is `static` and inlines into `swap_writeout()`, which is why the `kswapd0` oops
named `swap_writeout` for what is really MARIE's frame.

`2101` applies before `2155`, so neither patch's author could see the other's
entry point. **A guard placed in one caller of a shared callee protects only
that caller.**

### The fix

The same guard in `do_swapout()`, honouring *its* contract: `do_swapout()` owns
the unlock on every branch, so the guard unlocks before the trailing
`folio_put()`, where `swap_writeout()` leaves the folio locked for an
`AOP_WRITEPAGE_ACTIVATE` retry.

A guard at the shared choke point, `__swap_writepage()`, would be more robust —
no future caller could bypass it. It is not done here because the two callers
have different locking contracts, and reconciling them is a larger change than
a crash fix should carry.

### Upstream status, checked 2026-09-20

**Upstream has not fixed this.**

- **v3** of the xswap series (2026-09-16, the newest posting) is byte-identical
  to the carried v2 in every affected file — `mm/page_io.c`, `mm/swapfile.c`,
  `mm/swap_state.c`, `include/linux/swap.h`, `mm/zswap.c`.
- A new **RFC** (patchwork series `1169641`, 2026-09-20, 17 patches) touches the
  same guard — patch 06, *"fall back to disk when zswap refuses an xswap page"* —
  and its commit message describes this exact condition: *"zswap_store() can
  refuse a page if the pool may be at its limit... Under memory pressure that
  turns into a livelock."* But it is a feature adding a physical backend for
  xswap, not a fix: it never mentions `sio_pool`, and its patch 06 rewrites the
  guard to write to that new backend.
- `linux-mm/linux-mm` PRs `#4867` (the RFC) and `#4774` (v3) track both.

### Exhaustive upstream sweep, 2026-09-20

A multi-channel sweep (mailing-list trees, akpm's branches, patchwork, GitHub,
the crash signature, and `sio_pool`'s design history) with independent
re-verification of every candidate. Result: **nothing upstream fixes or
mitigates this**, and nothing can — **`do_swapout()` does not exist upstream at
all.** Zero hits across all 13 lore mirrors; absent from torvalds, akpm and
linux-next. It is MARIE's invention, so the bypass is ours to close.

- **akpm has no xswap at all.** `mm-everything-2026-09-20` (`62310f16ff3f`)
  contains zero `SWP_XSWAP` / `xswap_create` / `nr_real_swapfiles`.
- **The RFC cannot help here.** Beyond being a feature, it is a no-op on this
  machine: `xswap_alloc_phys_slot()` skips `SWP_XSWAP` devices, `/proc/swaps`
  has one row, so `xswap_backend_alloc()` returns empty and patch 06 performs
  exactly the guard already carried. Patch 06 also edits `swap_writeout()`,
  which `do_swapout()` never enters.
- **Independent prior art.** `RAMDRAGONS/jcachy` `6c82211cd` (2026-09-20T00:57Z,
  ~16 h before `2199`) carries the same fix in `do_swapout()`, differing only by
  a `data_race()` wrapper. Not adopted: `CONFIG_KCSAN` is off so it compiles
  away, and upstream's own guard in `2155` omits it.

### Do not add `sio_pool_init()` to the xswap path

It is the obvious belt-and-braces move and it is **harmful**, as is adding a
real disk swap device. Both make `mempool_alloc()` succeed, after which the
write reaches code that cannot work for xswap: `si->bdev` is NULL and
`swap_extent_root` is empty (`add_swap_extent()` is unreachable from
`xswap_create()`). `swap_bdev_can_merge()` calls `swap_folio_sector()` during
the merge test — BUG before any submit with two or more batched folios — and
otherwise `offset_to_swap_extent()` ends in `BUG(); /* It *must* be present */`.
That trades a conditional NULL-deref for a deterministic kernel BUG.

### Guard inventory (rebase-sensitive)

Exactly **three** callers of `__swap_writepage()`: `swap_writeout()` (`2155`),
`zswap_writeback_entry()` in `mm/zswap.c` (`2155`), `do_swapout()` (`2199`).
`swap_add_folio()` is reached only from `__swap_writepage()` (WRITE) and
`swap_read_folio()` (READ, guarded). The RFC renames the callee to
`__swap_writeout()` and adds an argument, and Nhat Pham's vswap series adds call
sites, so re-derive this count after every bump.

### Unexplained: why the store was refused

The OOM snapshot 21 s before the oopses shows `zspages` at ~86.6% of the 20%
ceiling, below the 90% accept threshold — so pool-full may not be the trigger.
A failure inside `zswap_store_page()` (zsmalloc allocation, entry cache, xarray)
is at least as likely. This widens the set of refusals nothing upstream handles.

`2199` is therefore ours alone. **Drop it when upstream lands a fix for the
bypass**, rather than merging it forward — the correct long-term shape is a
guard the shared callee cannot be reached around.

## Update 2026-09-20 — every carried patch checked against its latest revision

A version sweep ran over all 305 carried patches against the 13 lore mirrors,
matching on normalised subject **ignoring the `n/m` denominator** (a resized
series otherwise reads as a different patch — that blind spot is exactly why
the first pass missed CPPC v7, whose subjects move from `N/15` to `N/20`).

46 higher-version postings were found. Three filters reduced them to a real
work list: already merged upstream, content-identical, and written against a
base newer than ours.

### Adopted

| # | Change |
|---|---|
| `1210`–`1229` | ACPI CPPC **v6 → v7** (20 patches; was `1210`–`1224`, 15) |
| `2005` | v1 → **v2** |
| `1071` | **new** — `drm/amdgpu: More compact VCN IB emission` |
| `1230` | **new** — `cpufreq/amd-pstate: Skip auto_sel write when it already matches the mode` v3 |
| `1231` | **evaluated, REJECTED as redundant** — `cpufreq/amd-pstate: Fix TOCTOU when changing driver mode via sysfs` |

### `1231` — amd-pstate TOCTOU: evaluated and REJECTED (already fixed by our `1227`)

Found in the 2026-09-22 sweep and initially admitted — then the **cumulative
audit caught it** and it was backed out. Worth recording in full, because the
whole sequence is the lesson.

Mario Limonciello (AMD, amd-pstate maintainer), `[PATCH]`, 2026-09-21,
`<3bd87e32b2e42c9f938d9f7b65a82cfb54bbbefd>` on `lore-linux-pm`. Real bug:
`amd_pstate_update_status()` resolved `mode_state_machine[cppc_state][mode_idx]`
before taking `amd_pstate_driver_lock` and again after, so concurrent writes to
`/sys/devices/system/cpu/amd_pstate/status` could re-read a changed `cppc_state`
and hit either a self-transition (NULL deref) or a second
`amd_pstate_driver_cleanup()` (double-free of `current_pstate_driver->attr`).

It passed **both** mandated checks standalone against pristine `v7.3-rc4`
(`git apply --check` and `patch -p1 --dry-run -N`, hunks settling at offset
−107), the reverse check failed (genuinely new), it was absent from every tree,
and the author is the maintainer. On that evidence it was admitted as `1231`.

**Then the cumulative audit failed it:** `Hunk #1 FAILED at 1901`, `Hunk #2
FAILED at 1910`. The reason is the point —

**our `1227` already makes exactly this fix.** Its hunk rewrites the same
function:

```c
-	if (mode_state_machine[cppc_state][mode_idx]) {
-		guard(mutex)(&amd_pstate_driver_lock);
-		return mode_state_machine[cppc_state][mode_idx](mode_idx);
+	guard(mutex)(&amd_pstate_driver_lock);
+
+	if (!mode_state_machine[cppc_state][mode_idx])
+		return 0;
```

The lock is taken **before** the read and the transition resolved **under** it,
so `cppc_state` is stable and the race is gone — and ours additionally guards
the immutable-autonomous-`auto_sel` case. Functionally the same fix, already
carried.

**Two lessons, both already in `LESSONS.md` and now demonstrated together:**

1. **Standalone applicability is not admission.** The patch applied cleanly to
   pristine rc4; only the in-order cumulative apply exposed the conflict, and
   the conflict *was* the information.
2. **Grep our own series for the function before proposing a fix.** `1227`
   touches `amd_pstate_update_status`, and one `rg` over `sleepy-next/patches/`
   would have shown it before the patch was ever admitted.

The offset is the tell: standalone the hunks landed at **−107**, meaning the
patch was authored against a tree ~107 lines ahead of rc4. Our CPPC v7 series
(`1210`–`1230`) is what moved that region — and it is also what already fixed
the bug.

**Re-derived and re-rejected — 2026-09-22, later pass.** The same candidate came
back out of the live LKML mirror (`8f502e90b`, `lore-mirror`) and was admitted
again on standalone evidence *before* this ledger was consulted; the patch was
assembled, dry-run clean at offset −107, and only the next step — reading the
ledger — stopped it. It is the same patch, with the same verdict.

The cumulative condition was re-tested against the series tree rather than
argued: `Hunk #1 FAILED at 1901`, `Hunk #2 FAILED at 1910`, `2 out of 2 hunks
FAILED`, and `git apply --check` agrees. The −107 offset that made it look
applicably-new is exactly the region `1227` had already rewritten — the offset
is the tell, every time.

**The sharper lesson.** The function-name grep *did* run this time
(`rg -l 'mode_state_machine|amd_pstate_update_status' sleepy-next/patches/`)
and *did* surface `1227` — but only the patch whose **subject** matched
(`1231`) was inspected; `1227` was set aside as unrelated to mode changes. A
name grep that returns several patches has to be read for **all** of them: the
carried patch that already fixes your bug is rarely the one named after it.

### Superseded entry retained below for the record

Mario Limonciello (AMD, amd-pstate maintainer), `[PATCH]`, 2026-09-21,
`<3bd87e32b2e42c9f938d9f7b65a82cfb54bbbefd>` on `lore-linux-pm`. No replies, no
`Reviewed-by`/`Acked-by` — but it is the maintainer's own patch for the driver
he maintains.

`amd_pstate_update_status()` resolved `mode_state_machine[cppc_state][mode_idx]`
**before** taking `amd_pstate_driver_lock`, then resolved it **again** once the
lock was held. `cppc_state` is global and only stable under the lock, so two
concurrent writes to `/sys/devices/system/cpu/amd_pstate/status` can have the
second one re-read a *different* state — resolving to a self-transition
(`NULL`, immediate **NULL dereference**) or to an unexpected transition that
runs `amd_pstate_driver_cleanup()` a second time, **double-freeing**
`current_pstate_driver->attr`.

The fix takes the lock first and resolves the transition exactly once into a
local before calling it.

On-target: `amd-pstate` is this machine's CPU driver, and the file is live
(`CONFIG_X86_AMD_PSTATE`). Trigger is narrow — concurrent sysfs mode writes —
but the failure is a crash, and the fix is five lines.

Verified before admission: the buggy pattern is present in rc4
(`amd-pstate.c:1806-1809`); `git apply --check` and `patch -p1 --dry-run -N`
both pass against pristine `v7.3-rc4` (hunks settle at offset −107); the
reverse check **fails**, confirming it is genuinely new. Not present in
`linux-next`, `torvalds` or `linux-pm` at the time of the sweep.

Series is 312 patches. The cumulative audit applies all 312 to `v7.3-rc3`.

### ACPI CPPC v6 → v7

Christian Loehle, `[PATCH v7 0/20]`, 2026-09-16. This is live code:
`amd-pstate` is built on ACPI CPPC, and this machine is Zen 4 with CPPC.

**v7 drops `1213`** (`Use 64-bit masks for register fields`). The cover letter
states the reason directly: *"All supported CPPC configurations are already
64-bit, so this is only a cleanup I'll submit later on."* It is the author's
own drop, and the removal was approved before this update was made.

**v7 adds six patches:**

- `1224` Keep Performance Limited clearable on NVIDIA T41
- `1225` Validate FFH register fields before hardware access
- `1226` Propagate errors from cross-CPU FFH calls
- `1227` Accept requests to retain immutable autonomous selection
- `1228` cpufreq: CPPC: Select the frequency-invariance callback per CPU
- `1229` cpufreq: CPPC: Create the FIE worker before enabling PCC callbacks

v7 patches 4–14 correspond to v6 patches 5–15 with real content changes, so this
is a renumber as well as a revision.

Verified by substitution against the series-applied tree: all 14 v6 patches
reverse cleanly, all 20 v7 patches apply, and no later patch is disturbed.

### `1071` — More compact VCN IB emission

Tvrtko Ursulin, `[PATCH 01/18]`, 2026-09-18. Part of the same 18-patch series
that `1070` came from; see below. This machine enumerates **`vcn_v5_0_0`**, and
the patch touches the shared `amdgpu_vcn.c`, so it is on-target. It applies
cleanly to both pristine `v7.3-rc3` and the series-applied tree — no adaptation
needed, unlike `1070`.

### `1070` is already current — checked, not changed

`1070` is patch **17/18** of that same series. The series' hunk 4 does not apply
to our base because it expects a `const bool burst_nop = sdma->burst_nop;` hoist
this tree lacks — which is precisely what `1070`'s own commit message already
documents. Our adaptation ports that hunk's delta onto the rc3 form. No update
was needed and none was made.

### Checked and deliberately not changed

- **`2041` v3, `2415` v3, `2158` v3** — real content deltas (14, 10 and 16
  changed lines), but written against a base **newer than `v7.3-rc3`**: neither
  `patch` direction is clean against our tree, and the deltas are adaptations to
  post-rc3 API changes (`gso_segment` signatures, `in_nmi()`-based kfunc
  guards). Our `v2`/`v1`/`v1` are correct for this base. Revisit at the 7.4 bump.
- **`2144`, `2168`, `2185`** — reported as higher-version; the newer revision
  reverse-applies cleanly, meaning our content already matches. Version label
  only.
- **`2141`, `2412`, `2506`** — upstream commits that are already merged; the
  higher mailing-list versions are draft history.
- **`1151` v4** — dated 2026-02-16, older than what we carry. The sweep's
  version comparison ignores dates; this one is stale, not newer.

### Also evaluated this round

- **io_uring `[SECURITY]` trio** (Andres Berbescu, 2026-09-16) — three
  vulnerability reports, **not patches**: the mails carry no diff bodies and
  Jens Axboe replied to them. Nothing to apply.
- **amd-staging `memset32 for SDMA padding`** — same author and area as `1070`,
  but applies only partially and the 18-patch series has no GFX12 member.
- **`2ac2fe765` MALL hysteresis at high refresh rates** — rejected. It patches
  `dcn30_apply_idle_power_optimizations()`; DCN 4.0.1 has its own
  `dcn401_apply_idle_power_optimizations()` (`dcn401_init.c:90`), so the patched
  code never runs here. It would apply, compile, and do nothing.
- **`9413959fa` smu 14.0.3 energy accumulator** — rejected. It patches
  `smu_v14_0_2_ppt.c`; this machine enumerates **`smu_v14_0_0`**.

Hardware IP versions above are read from this machine's own IP discovery, not
inferred: `psp_v14_0_0` · `smu_v14_0_0` · `gfx_v12_0_0` · `sdma_v7_0_0` ·
`vcn_v5_0_0` · Display Core on DCN 4.0.1.

### Branch sweep — tips are not enough

The first pass read only each repo's HEAD. Sweeping **every branch** of
`amd-staging-drm-next`, `agd5f-linux` (129 branches), `drm-next`, `drm-misc`,
`linux-pm`, `akpm-mm` and `tip` found six additional on-target commits that the
tip-only pass had missed. Two of those were wrong-chip traps:

- `55765c2ff` `drm/amdkfd: Fix TCP XNACK scoreboard reset race` — touches
  `gfx_v9_4_2.c` and `kfd_int_process_v9.c`: CDNA/Aldebaran, not GFX 12.0.
- `79b709bc3` `drm/amdgpu: Fix kfd device lock during partition` — touches
  `aqua_vanjaram.c` and `soc_v1_0.c`: MI300 and datacenter SoCs.

And one was worth taking:

**`1072`** — `92a1b0734` `drm/amdgpu/atom: bound the VBIOS date, part number,
version and build getters`, Hari Mishal, 2026-09-15, `Signed-off-by` also from
Alex Deucher. Four unbounded reads while walking the VBIOS image using offsets
and counts taken from the image itself. The commit message names each: a
14-byte read at `OFFSET_TO_VBIOS_DATE` that `check_atom_bios()`'s `0x49`
minimum does not cover, an image-supplied `u16` string offset dereferenced
without a bound, a match advanced by a fixed 18 bytes and copied with only a
length cap, and a config-string walk from an image-supplied offset. All are now
checked against `ctx->bios_size`. Not in linux-next or torvalds — amd-staging
only. Applies cleanly to pristine `v7.3-rc3` and to the series tree.

Also evaluated from the branch sweep and not carried:

- `af619209b` `Reuse cached PCIe link device` (Mario Limonciello) — replaces a
  local `amdgpu_device_get_aspm_pdev()` helper with a cached `adev->link_dev`.
  A refactor with no fix claimed, in ASPM handling, which this machine disables
  anyway via `pcie_aspm=off`. Not worth the blast radius.
- `7710fb929` `Extend logical to device instance lookup to all devices` — a
  34-file refactor of `amdgpu_ip.c`.
- `2cae0b425`, `e0e9c2257`, `99c9ca0af` — apply only partially.
- `159149c51` — touches `dcn42_hwseq.c`. DCN 4.2, not our DCN 4.0.1.

### drm/amd work items, 2026-09-20

Four open issues concern this hardware. **None references a fix**, so there is
nothing to carry; they are tracked, not merged.

- **`#5868`** (filed 2026-09-20) RX 9070 XT: HDMI disconnect/reconnect loop
  above 1080p. This machine drives its MAG251RX at 1080p over HDMI, below the
  reported threshold.
- **`#5862`** (2026-09-19) Navi 48 / RX 9070 XT: HDMI 2.1 FRL link not trained
  against an LG OLED sink at 4K.
- **`#5859`** (2026-09-18) `[RDNA4][DCN 4.0.1]` DDC/CI loss and surface noise on
  DP-4. The reporter rolled back kernel, Mesa and linux-firmware with no change,
  and calls it a DCN 4.0.1 reset/recovery issue.
- **`#5855`** (2026-09-17) VRR refused on DP (`vrr_range 0 0`) but working on
  HDMI, on an MSI MAG display. A different model from this machine's MAG251RX,
  but the same vendor and behaviour class as `1164`.

The image reference in `#5859` (`112d2111f50a…`) is an upload path, not a
commit — the same dead end this ledger already records.

### A test that reported success while testing nothing

The nine amd-staging commits above were first classified as *already carried* —
all nine, including ones never seen before. The cause: `repos/_audit` had been
removed before the previous build (which ran `audit_series.py` **without**
`--keep`), so every `patch -d repos/_audit` invocation failed with

```
patch: **** Can't change to directory repos/_audit : No such file or directory
```

That text matches neither `FAILED` nor `ignored`, which was the entire
classification criterion, so the failure fell through to the "carried" branch.
**`patch` also returned exit 0 on that fatal error**, so checking `$?` would not
have caught it either.

Two rules follow. A test that reads a reference tree must assert the tree exists
before using it, and must treat "no verdict" as an error rather than a result.
And `audit_series.py --keep` is what leaves the tree behind — a plain run
consumes it.

### Source health

`repos/torvalds` reported a successful `fetch --all` while sitting two days
stale (local `c3d85c66`, remote `518e5b79` — 105 commits missed, including
`amd-drm-fixes-7.3-2026-09-17`). Caught by comparing against `git ls-remote`,
not by the fetch. All 11 lore mirrors had been pruned from `repos/` and were
re-cloned (~8 GB); `lore-mirror` and `lore-sched-ext` are **bare** mirrors, so
a `.git`-directory existence check misreports them as missing.

## Sweep 2026-09-18 (second round)

Three passes: the accumulated `v7.3-rc3`..`master` window, a fresh pull of the
third-party patchset repos, and a re-clone of the two remaining damaged trees.

### `v7.3-rc3`..`master` — 415 commits (364 non-merge)

`v7.3-rc4` is not tagged yet, but 14 `-rc4` pull tags are already merged, so
this window drains into rc4 within days. Everything below is rc4-bound unless
stated otherwise; carrying it now only shortens the wait.

**Adopted**

- **`2045`** — `8e759cd1f` `tcp: Don't call skb_clone_and_charge_r() for
  close()d listener in tcp_v6_do_rcv()`, Kuniyuki Iwashima, 2026-09-14. The
  IPv6 receive path charged an skb to a listener that had already closed. One
  file, two lines.
- **`2198`** — `2081d8d042e4` `mm: filemap: move lruvec accounting outside the
  xarray lock`, Usama Arif, 2026-09-16. Taken from `akpm-mm`
  `mm-everything`, and **not** in linux-next, so a version bump would not bring
  it. `NR_FILE_PAGES`/`NR_FILE_THPS` accounting moves past `xas_unlock_irq()`,
  shortening the xarray critical section on the page-cache add path.

**Evaluated and not carried**

- `55a8e1451` `x86/mm: Don't force unencrypted DMA for IOMMU-backed devices` —
  `CONFIG_AMD_MEM_ENCRYPT=y` is set, but SME is not active on this desktop, so
  the path is unreachable. rc4-bound.
- `150dba2c6` `net: remove WARN_ON_ONCE() from the dev_fill_forward_path() loop
  check` — removes a warning, changes no behaviour. rc4-bound.
- The `scx_qmap` quartet (`89ff16f07`, `63b4ff622`, `a0d356696`, plus the
  userspace half of `9a0b159ff`) — they touch `tools/sched_ext/scx_qmap.bpf.c`,
  a userspace sample. This machine runs `cake_1.2.1` from the `scx-scheds`
  package, so none of it is loaded. `9a0b159ff` is already carried as `2410`
  for its kernel-side hunk.
- The Ghiti swap-dropbehind trio (`2b09efabae8f`, `e42fa88021a8`,
  `f9abcb602ef3`) — none are in linux-next, so they are genuinely incremental,
  but the two that do the work hang off swap writeback completion and this
  machine's xswap has no backing store. `2b09efabae8f` on its own is pure
  plumbing. `f9abcb602ef3` additionally fails to apply (hunks 1 and 3). Left
  out.
- `7891fbb95` `mm/folio: EXPORT_SYMBOL_FOR_KVM(lru_cache_drain_for_folio)` — a
  symbol export for KVM, partially present already and not needed here.

### Third-party repos

- **sirlucjan** — `zstd-dev-patches-v4` and `-v5` landed 2026-09-18. `2100`
  replaced with v5; see below.
- **CachyOS** — no commits since 2026-09-15.
- **linux-tkg** — the 2026-09-18 activity is BORE, linux-hardened, a Gentoo
  Kconfig patch and a 7.2 config refresh. None of it is on-target: this machine
  runs sched-ext rather than BORE, and is not a `-hardened` tree.

### `2100` replaced with sirlucjan zstd `v5`

`zstd-dev-patches-v5/0001-zstd-7.3-merge-v1.6.0-into-kernel-tree.patch`,
Piotr Gorski, 2026-09-18, supersedes the 2026-09-14 revision already carried.
The delta is 14 added and 7 removed lines: an
`assert(MEM_32bits() || !longOffsets)` guard tightened to
`MEM_32bits() && longOffsets`, and the FSE state updates in
`zstd_decompress_block.c` switched to pass `DInfo` directly instead of copying
`nextState`/`nbBits` into locals first.

The file name is unchanged, so this is a byte-level replacement at `2100`, not
a renumber. Verified by reverse-applying the old revision from the
series-applied tree, applying v5 in its place, and re-running
`audit_series.py`: every patch then in the series still applied, including the
four zstd dependents (`2129`, `2130`, `2148`, `2149`) that follow it. The full
build then applied all 305 with zero skips.

### Clone repair

`repos/tip` and `repos/akpm-mm` were still the damaged trees. Both re-cloned
with `--depth=300`; `--shallow-since` is what fails against these two, with
`fatal: error processing shallow info: 4`. `tip` now reaches 2026-09-18 and
`akpm-mm` 2026-09-05, both with sane dates, and `akpm-mm`'s non-`master`
branches needed an explicit `+refs/heads/*:refs/remotes/origin/*` fetch. The
damaged trees are parked as `repos/tip.damaged` and `repos/akpm-mm.damaged`.

### Methodology correction: subject matching is not a duplicate test

The first pass through the window classified candidates by searching the
carried patches for the upstream commit subject. That produced four **false
negatives** — `1587d3394`, `e14a34548`, `93d88ac4a` and `9a0b159ff` were
reported as absent, and all four are carried (`2507`, `2146`, `2405`, `2410`),
filed under subjects shortened relative to upstream. Our subjects and upstream
subjects differ often enough that text matching cannot decide this.

The authoritative test is reverse-applicability against the series-applied
tree: if `patch -R` succeeds, the change is already in the series. Recorded in
`LESSONS.md`.

## Sweep 2026-09-16 (from the rc3-16 cycle)

Base was current: `v7.3-rc3` was the newest mainline tag and `next-20260916` the
newest snapshot.

### Drop list for the next bump

Subjects of all 217 carried patches were matched against linux-next, then the
15 hits were checked by content, because subject matching alone produces false
positives: `1061`, `1062`, `1152` and `2005` each matched a subject but differ
in content, and stay. **Eleven are content-identical to upstream commits:**

| Ours | Upstream | Subject |
|---|---|---|
| `0050` | `5c1a6c9736a6` | drm/edid: Parse AMD VSDB for FreeSync refresh range |
| `0058` | `482b6542a862` | drm/amd/display: restore FRL cap on non-destructive |
| `0061` | `8b607d6f54b0` | drm/amd/display: Enable HDMI ALLM for Gaming-VRR |
| `1056` | `0e118b936dc5` | drm/sched: Lock drm_sched_entity_is_idle() |
| `1060` | `38f4fe785b5d` | drm/amdgpu: cancel hang_detect_work before taking |
| `1135` | `6ee70c955ffc` | drm/amd/display: fix HPD program filter programming |
| `1136` | `455c7c34707c` | drm/amd/display: Update and revert FRL LT Timeout |
| `1138` | `20331505df9c` | drm/amd/display: pull colorops into state |
| `1140` | `50eed169c0ab` | drm/amd/display: clamp force_min_dcfclk to dcn42b |
| `1154` | `dd601ed4ce28` | drm/amd/display: Fix NULL deref of new_stream->sink |
| `2006` | `3de3d4336b8c` | zram: convert to SG-list zsmalloc object read API |

These are **drop-at-the-bump, not drop-now**: they are in linux-next and 7.4
bound, not in the 7.3-rc3 base, so dropping them today would remove the fixes.
`1140` is the first to drop when its base arrives — a DCN42B clamp, inert on
DCN 4.0.1.

### Conflicts to expect at the 7.4 bump

- **amd-pstate EPP rework** (`amd-pstate-v7.4-2026-09-14`, Mario Limonciello)
  adds a per-SoC and per-core-type EPP table plus `cpudata->epp_default_ac/dc`.
  It collides with `1202` (`epp_boost`): both add fields to
  `struct amd_cpudata` and both touch `amd_pstate_epp_cpu_init()`. `1202` is not
  superseded — upstream never mentions `epp_boost`; they are different
  mechanisms that clash textually.
- **zswap rework** (Longlong Xia, Kefeng Wang, Jianyue Wu; 2026-09-06 to 09-10)
  rewrites the tail of `zswap_store()` (`bcfacfe16322`), which is where the
  xswap hunk lives, changes `zswap_invalidate()` to take a range
  (`6a391b347b5e`) — the path xswap pages leave the pool by — and moves pools to
  an xarray with `entry->pool` becoming `pool_idx`. The series barely touches
  the structs, so the struct churn is harmless; the `zswap_store()` overlap is
  not.
- **`0412b1064a3b` "Cover EDID CEA parsing helpers"** refactors
  `dm_edid_parser_send_cea()` in `amdgpu_dm_connector.c`, the file the flicker
  fixes patch (`1151`: 8 hunks, `1163`: 4, `1164`: 9). Mechanical
  (`STATIC_IFN_KUNIT` visibility), so a rebase rather than a redesign.
- **`0059` will likely conflict.** `730c6d807` ("Drop KUnit tests for removed
  `parse_hdmi_amd_vsdb()`") records that `parse_hdmi_amd_vsdb()` was removed
  when HDMI FreeSync detection moved to the common EDID parser. It is gone at
  drm-next HEAD and still present on amd-staging.
- **AMDGPU HDMI 2.1 enabled by default (7.4)** — `f13a8b4a7e86`,
  `0505751e5019`, `9ec95eed935c`, `2151ff7f88f3`, `453506fdab7c` are what
  `0055`/`0059`/`0061` carry, so all three become drop candidates.

### Source health at the time

`repos/drm-next` was stuck at 2026-09-11, its shallow clone failing to
unshallow; linux-next aggregates its content. `repos/amd-staging-drm-next` was
stale at 2026-07-23 and `repos/akpm-mm` at 2026-08-10, both refusing to refresh,
so negative results from those two were weak. `repos/linux-tkg` and
`repos/cachyos-linux` local refs were behind their remotes.

### Not carried, tracked

- `[PATCH v4 4/8] drm/amdgpu/gfx12: honor mqd_prop modify flag in init_mqd`
  (Jesse Zhang, 2026-09-07) touches only `gfx_v12_0.c` (+14/-9), consuming the
  `mqd_prop` modify flag so a re-enabled queue keeps the firmware
  context-saved rptr/wptr. Not in amd-staging and no merge yet.
- `drm/amdgpu: fix sched entity leak in ttm buffer entity init`.
- `drm/amd/display: Fix HDMI RGB quantization updates` (Alex Hung).
- `#5663` (artifacts after S3 resume on RX 9070 XT) carries only a user-posted,
  unmerged workaround diff pinning DCC BO moves to move-entity 0 in
  `amdgpu_move_blit()`; the maintainer calls it a Navi 4x SDMA hardware bug.
  No upstream commit, so nothing to carry.
- `[PATCH 00/66] DC Patches Sep 14 2026` contains on-target items, notably
  `40/66 Decouple HUBP_UPDATE_PLANE_ADDR from pipe_ctx` — the HUBP plane-address
  path the display "box" misread lives in. Arrives with the bump.

## The CachyOS squashes (0101–0112)

Each squash is generated **against the current series state**, not against a
clean rc, because the patches before them touch shared files such as
`drm_edid.c`. Two conflicts are handled inside the squashes: `0151` duplicates
`0055`, and `0053` must be dropped when the HDMI branch is present. To refresh
them, use the `patch-cachy-branches` skill.

| Patch | Branch |
|---|---|
| `0101` | `bbr3` |
| `0102` | `kbuild` |
| `0103` | `cpu-isa` |
| `0110` | `config-hooks` — the `CONFIG_CACHY` gates |
| `0111` | ACPI: disable bus-master check for AMD |
| `0112` | amdgpu: avoid evicting resources at S5 |

`0111` is Sultan Alsawaf's (kerneltoast) patch verbatim, re-applied to 7.3 by
CachyOS under the same `From:` line.

**Caveat:** `0110-cachy-config-hooks.patch` applies only with fuzz on rc2 — its
`bus_lock.c` hunk carries `CONFIG_PROC_SYSCTL` context where rc2 has
`CONFIG_SYSCTL`. `git apply --check` rejects it, while the build's
`patch -p1 --forward -F2` accepts it. Harmless today, but it is precisely the
"zero `.rej` does not prove application" trap in `LESSONS.md`.

`vm.watermark_boost_factor=0` and `vm.compaction_proactiveness=0` are live
through `0110` under `CONFIG_CACHY`, which `PKGBUILD` forces on with
`scripts/config -e CACHY`. Note that `config:43` still reads
`# CONFIG_CACHY is not set`, so the config file alone is misleading here.

## Evaluated and not carried

These were examined and rejected, with the reason. They are recorded so a later
sweep does not re-derive the same conclusion.

### Other kernel patchsets

- **linux-zen** has no 7.3 line; its tags stop at `v7.2.4-zen2`. `zen-sauce` is
  now mostly Alfred Chen's out-of-tree `sched/alt` (BMQ/PDS), which cannot be
  adopted alongside EEVDF and sched-ext. Its `ZEN_INTERACTIVE` tunables are
  already duplicated by `0110`.
- **linux-tkg and XanMod** largely duplicate `0110`. XanMod's one interesting
  item, firelzrd's `le9uo` working-set protection, hooks
  `shrink_folio_list()` and `get_scan_count()`, which MARIE replaces; its own
  last port is 7.1-rc1.
- **Clear Linux** is dead: the organisation was archived in 2025-08 and its last
  kernel was 6.15.7. Only config-level items remained.
- **MuQSS and the CK patchset** are mutually exclusive with sched-ext: the patch
  adds `scx_cpuperf_target()` and `scx_switched_all()` stubs that disable SCX,
  and this config sets `CONFIG_SCHED_CLASS_EXT=y`.
- **The Reflex cpufreq governor** verifies clean and shares no files with the
  series, but is deferred.
- **XanMod's "rwsem spin faster"** drops `cpu_relax()` from the spin loop, which
  is a poor trade on SMP. Its `VM_READAHEAD_PAGES`, `dirty_ratio=50` and Polly
  items are snake oil here: the prebuilt LLVM has no Polly, and
  `-fmodulo-sched` and `-fivopts` are GCC-only.

### Individually rejected

- **`364e520095b2` / `4cf50332b538`** (`crypto: rsassa-pkcs1 - reject undersized
  keys`, verifying and signing halves; KASAN out-of-bounds on an undersized
  key). Both are genuine, both are absent from the rc3 base, and
  `CONFIG_CRYPTO_RSA=y` with `CONFIG_MODULE_SIG=y`. **Not taken, because on this
  kernel it is not a security boundary:** `CONFIG_MODULE_SIG_FORCE` is unset, so
  an unsigned module loads regardless, and the parser here only ever sees
  signatures this machine produced with its own generated key under
  `CONFIG_MODULE_SIG_ALL`. The bug needs an attacker-supplied malformed
  signature to reach, and nothing on this machine accepts one. Recorded rather
  than silently dropped — revisit if `MODULE_SIG_FORCE` is ever enabled.
- **`evdev`: `call_rcu` instead of `synchronize_rcu`** (identical in
  XanMod, zen and tkg; Kenny Levinsen, 2020). Attractive on paper, because the
  author measured 27.1 s down to 0.018 s for 1000 open-close cycles and this
  machine's compositor restarts close many evdev file descriptors. Not taken:
  it has never been merged upstream in five years, and nobody established
  *why*. Answer that before carrying it.
- **The kerneltoast kswapd trio** ("Stop kswapd early", "Don't stop kswapd on a
  per-node basis", "Increment kswapd_waiters") is desktop-targeted but fails to
  apply: two of three hunks in `mm/page_alloc.c` and the `mm/internal.h` hunk
  are rejected because `2101` rewrites those files. It needs a deliberate
  rebase.
- **`47b020a24ae3`** (revert "cpumask: limit FORCE_NR_CPUS to just the UP case")
  is inert unless `CONFIG_NR_CPUS` is exactly 16 and `CONFIG_FORCE_NR_CPUS=y`;
  this config uses 512 for hotplug headroom. Upstream restricted it to UP
  precisely because a wrong `NR_CPUS` breaks the kernel.
- **`e5b7e9d87ace`** (lower the non-hugetlb pageblock size) is superseded by
  `CONFIG_PAGE_BLOCK_MAX_ORDER`, and lowering it alongside
  `TRANSPARENT_HUGEPAGE_ALWAYS` and `HUGETLBFS` risks both THP success and 2 MB
  hugetlb pages.
- **`nvme: bump genctr when cancelling a request`** — **now carried as `2015`.**
  The sha recorded here previously (`7f607455c3b9`) was wrong: it resolves in
  `torvalds` to a 2010 OMAP merge commit. The real commit is
  `7f60745ec3ff54acb2b8afa5781b18ab596aed53`. The note said it "needs a rebase";
  that rebase has since happened upstream and it now applies clean (offset 17).
- **`finish_task_switch()` always-inline** (zen and tkg) quotes a 34.8% figure
  that applies to spectre_v2 retpolines. This machine reports Enhanced /
  Automatic IBRS, so only the roughly 8.6% clang function-level case applies,
  under 0.3% end to end, at the cost of forcing about 20 functions inline.
- **The nvme-pci adaptive interrupt polling v2 series**: patch 1 applies,
  patch 2 needs a rebase (1 of 20 hunks).
- **hrtick repick v2** needs a rebase and collides with the `0105` and `0113`
  regions. **sched_ext lazy preemption** is inert because `CONFIG_PREEMPT_LAZY`
  is unset. **Hugh Dickins' 26-patch fbatch** needs two
  `mm-hotfixes-stable` prerequisites and has unproven performance. **Jan Kara's
  deferred inode reclaim** is still in review. **CPPC v6** is hardening rather
  than performance.
- **The gfx12 dynamic-VGPR trap handler**, the **bind-imported-BOs** series (two
  same-day revisions still in review) and the **TTM LRU bulk-move nested-sublist
  refactor** were deferred as large, unstabilised or invasive.
- **Off-target by construction:** the menu-governor wakeup fix (Intel Xeon),
  RTL8261C/D (not this NIC), the DRM fair-policy fix (this config defaults to
  FIFO), k10temp per-CCD (EPYC only), and the Infinity Scheduler (an EEVDF
  modification that conflicts with sched-ext).

### Tracked but unpatched upstream

- The **`flip_done` and pageflip-timeout freeze family** is about 25 open
  drm/amd work items, several naming the RX 9070 XT. No upstream patch exists.
- The **SMU driver and firmware IF mismatch** (`0x2e` against `0x33`, work item
  !5538) is unfixed in rc2 and in drm-next, which is why the
  `pcie_aspm=off`, `amdgpu.aspm=0` and `amdgpu.runpm=0` stopgaps remain.
- Palazzi's cursor-vblank patch (!5799) no longer applies: its target was
  rewritten by the VUPDATE_NO_LOCK rework `f64a9be56536` in rc2. The underlying
  bug class survives and would need a rebase onto `dm_arm_vblank_event()`.

## 2026-09-15 note: LRU-MARIE r2 and xswap

`2101` now carries the author's **0.11.1r2** packet from
<https://github.com/firelzrd/lru_marie> (`patches/testing/`). The r2 revision is
0.11.1 minus the `localversion` file creation (the `-marie` version suffix) with
the diffstat corrected; the author's packet subject still reads `0.11.1` while
the file is named `r2`. Everything else is byte-identical, including the
`scripts/setlocalversion` hunk.

`2155`–`2166` carry Baoquan He's **v2 xswap series** ("extendable swap
devices"), posted to linux-mm on 2026-09-13 and also shipped by CachyOS in its
`7.3/xswap` branch. It is upstream work in review: drop it when it lands in
mainline, and re-check for a v3 before rebasing. `CONFIG_XSWAP=y` is set in
`config`.

## 2026-09-15 note: 2169 (formerly 2142) needed its series prerequisites

`2171` — carried as `2142` until the 2026-09-15 renumber — is patch **3/4** of Xueyuan Chen's "[PATCH v7 0/4] mm: avoid large folio
splits when swap is unavailable". Only 3/4 was ever carried. On its own it is
not just incomplete but wrong: it gates the large-folio split fallback on
`ret != -E2BIG`, and nothing in the tree returned `-E2BIG` — 2/4 is what
introduces that classification — so every `folio_alloc_swap()` failure took the
"do not split" branch and the split fallback was dead code. `2169` (1/4) and
`2170` (2/4) complete the series and restore the intended behaviour: split only
when splitting might actually help (`-E2BIG`), skip the pointless split when
swap is exhausted (`-ENOSPC`) or would not help (`-ENOMEM`). Patch 4/4 (shmem)
is not carried and not needed for correctness here.

## Pass 2026-09-22 — `lkml.org/hot.xml`, and everything on-target it led to

Asked to check `https://lkml.org/hot.xml` for includable material.

### The feed itself is dead — do not use it as a source

`hot.xml` returns HTTP 200 with a full-looking 57 KB payload, but it is a
**frozen snapshot from May 2026**. Two fetches returned byte-identical bodies
(56,969 B), the newest `/lkml/2026/5/…` entry carries `Linux 7.1-rc4`, and
there is no live `/hot` page at all (404). lkml.org itself is *not* stale — its
front page serves Sep 22–23, 2026 — so only the hot-thread generator has
stopped. A 200 with a plausible body is not evidence of freshness; check the
**newest date in the payload**. `lkml.org` is not a source this project uses
anywhere; LKML is reached through `repos/lore-mirror`.

The live portion of the page is only the last ~15 messages, which is a sliver
of LKML's daily volume and strictly worse than the mirror. Nothing was
includable from either slice.

### What the real source did have

Scanning `repos/lore-mirror` (current through 2026-09-22) for on-target traffic
from 09-20 onward produced ten threads. All ten were resolved, **none adopted**:

| Thread | Verdict |
|---|---|
| `[PATCH v2] sch_cake: prevent shaper corruption` | **Already carried as `2045`** — same author, same timestamp (2026-09-22 16:41:24 +0800), same changelog, same `11 insertions(+), 4 deletions(-)`; diffs byte-identical apart from the mail signature |
| `[PATCH] cpufreq/amd-pstate: Fix TOCTOU…` | **Redundant — already fixed by `1227`**; see above |
| `[PATCH 1/4]`, `[2/4]` amd-pstate mode-change | **Already carried as `1231`/`1232`** (Mario's series) |
| `[PATCH 3/4]`, `[4/4]` amd-pstate-**ut** | **Inert** — unit-test module only; `CONFIG_X86_AMD_PSTATE_UT` is not set |
| `[PATCH] io_uring: initialize task context before the BPF loop` | **Awaiting v2** — still pending since the last sweep |
| `[PATCH] drm/amdgpu: unmap GART dma pages before free` | **Inert** — targets `amdgpu_gart_table_ram_alloc()`, reached only under `if (!adev->gmc.real_vram_size)` (the "Put GART in system memory for APU" branch in `gmc_v9_0.c`). A dGPU takes `amdgpu_gart_table_vram_alloc()` in `gmc_v12_0.c:798`, so the code never executes here |
| `[PATCH 0/3] drm/amd/display: NULL derefs on MST HPD` | **Off-target** — MST is DisplayPort-only; live connectors are `HDMI-A-1` and `HDMI-A-2`, no DP. Also unreviewed (the cover letter still reads `*** BLURB HERE ***`) |
| `[PATCH net-next v14 0/7] r8169 RSS / multi-queue` | **Inert + wrong tree** — RSS is gated `mac_version == RTL_GIGA_MAC_VER_80` (**RTL8127**); this NIC is RTL8125B. `net-next`, so 7.4 anyway |
| `[PATCH v2 0/3] mm: bypass swap readahead for zswap` | **Skip** — under review since 2026-08-19; on 09-22 the author offered to "revert to the simpler version", so the shape is not settled |
| `[PATCH v5 0/3] cpufreq: cppc: Handle Highest Performance changes` | **Skip** — a feature, still in review (Wysocki commenting); not a fix for anything we hit |

### Confirmed still-open

- The io_uring BPF-loop NULL deref remains **pending a v2** — unchanged from the
  previous sweep.
- `CONFIG_X86_AMD_PSTATE_UT=n` here, which is why both `amd-pstate-ut` patches
  in Mario's series are skipped rather than carried; if that config is ever
  enabled they become live again.

## Adopted 2026-09-24 — nine patches, all verified before adding

Every one passed: named human author + `Signed-off-by`, symbol existence in the
base, and **both** `git apply --check` and GNU `patch -p1 --forward -F2 --dry-run`
against pristine `v7.3-rc4`. 243 -> **251**.

| # | Subject | Author | Source | Why it is on-target here |
|---|---|---|---|---|
| `2046` | blk-mq: set RQF_USE_SCHED when the operation is known | Keith Busch | `lore-linux-block` `e6f523c` | **kyber is this machine's io scheduler.** `Fixes: 4b6a5d9cea91` is present in rc4, so the leaked domain token and stalled queue are live. `Reviewed-by: Christoph Hellwig`; applied as `ab6c756f28c7` |
| `2047` | blk-mq: allow cached requests to be used for flush operations | Keith Busch | same series `e6eb5c5` | 2/2 of the pair; `Reviewed-by: Christoph Hellwig`, applied as `9d2c70986bb7`. Applies clean **on top of `2046`** |
| `2048` | io_uring: initialize task context before running the BPF loop | Yao Kai | `lore-io-uring` `e779402` | NULL deref in `io_submit_sqes()` via `bpf_io_uring_submit_sqes`. v2 applied by Jens as `a3bdf68feecc`; content-identical to v1 (empty changed-line delta) |
| `2416` | sched_ext: Fix CPU hotplug hang when a dying CPU's tasks sit in the BPF scheduler | Tejun Heo | `lore-sched-ext` `ed5b728` | marked **`for-7.3-fixes`**, `Cc: stable`. This machine runs scx full-switch (`switch_all=1`, `scx_cake`) |
| `1073` | drm/amdgpu: keep GFX12 DCC blits off the SDMA move entity | `pepp` (GitLab) | drm/amd work item **#5663** | confirmed by a reporter on **RX 9070 XT (Navi 48, gfx1201)** to fix artifacts after S3 suspend. The guard is absent from rc4's `amdgpu_ttm.c` |
| `9077` | drm/amdgpu/userq: fix reading the WPTR at a non-zero BO offset | Jesse Zhang | `lore-amdgfx` `f275e7c7` | wrong fence seqno in `amdgpu_userq_fence.c` |
| `9078` | drm/amdgpu/userq: reserve the VM root BO around CWSR param validation | James Zhu | `lore-amdgfx` `ec5c91df` (v2) | fixes `dma_resv_assert_held` on every compute queue create, `mes_userqueue.c` |
| `0104` | sched/core: Make `finish_task_switch()` and its subfunctions always inline | Xie Yuanbin | sirlucjan `7.3-rc/cachyos-fixes-patches-v6` part 07/12, commit `909c59d8ef23` | **the premise holds here**: `spectre_v2` reads *"Enhanced / Automatic IBRS; IBPB: conditional; STIBP: always-on"*, so mitigations are on, and `finish_task_switch()` is core code scx does **not** bypass. Its `arch/arm|riscv|s390|sparc` hunks are inert in an x86_64 build; the live parts are `arch/x86/include/asm/sync_core.h`, `kernel/sched/core.c`, `kernel/sched/sched.h`, `include/linux/sched/mm.h` |
| `2041` | net: gso: limit recursive IP-in-IP segmentation | Zihan Xi | `lore-netdev-new` `29a00ee7` | **updated in place v4 -> v6**: replaces the `GSO_MAX_HEADER`/`gso_header_len_exceeded()` headroom test with a per-skb `recursion_counter` in `SKB_GSO_CB` plus `gso_recursion_inc_test()` and `IP_TUNNEL_RECURSION_LIMIT` |

**Provenance note on `1073`.** Its source is a GitLab issue note, not a list
posting or a merged commit. It carries a `Link:` to the note and a
`Reported-by:`, but the author is a GitLab handle with **no real name and no
`Signed-off-by`** — so `Signed-off-by`/`Assisted-by` trailers were added
naming this project, and the origin is stated rather than implied. The change
is a 4-line guard; it forces `e = 0` for `AMDGPU_GEM_CREATE_GFX12_DCC` blits
into VRAM. That is **not** a no-op here: `num_move_entities` is
`MIN(num_buffer_funcs_scheds, TTM_NUM_MOVE_FENCES)` and Navi 48 has more than
one SDMA instance, so the engine really is being constrained. It is a
workaround whose author frames it as experimental ("give it a try and report
if it helps"). **Drop it first if display artifacts or blit behaviour regress.**

> **CORRECTION (2026-09-24, same evening).** `2417` was adopted correctly, but
> this pass also exposed that **`2416`, adopted earlier the same day, was
> corrupt**, and it had already been built and installed.
>
> My mail decoder was Python's `quopri.decodestring`, and **it silently eats one
> `=` from a bare `==`**:
>
> ```
> quopri.decodestring(b'if (x == y)')  ->  b'if (x = y)'
> ```
>
> The mailer had emitted a bare `==`, which is invalid quoted-printable but
> common. The result, in `2416` (`kernel/sched/ext/ext.c`):
>
> ```c
> +    if (p->scx.dsq = &rq->scx.local_dsq)      /* shipped - assignment, always true */
> +    if (p->scx.dsq == &rq->scx.local_dsq)     /* what Tejun Heo actually wrote */
> ```
>
> **Neither the build nor the series audit can catch this.** It compiles (no
> `-Werror`), and the audit only proves a patch *applies*. A passing build is not
> a correctness check for patch content.
>
> Caught by re-decoding every mail-sourced patch adopted that day with a
> **safe decoder** (expand `=XX` and soft breaks only, leave a bare `=` alone)
> and diffing the bodies: of `2046`, `2047`, `2048`, `2416`, `9077`, `2041`,
> **only `2416` differed**. Then two whole-series scans: assignment-in-condition
> (5 hits, 4 benign — the `while ((x = f()))` idiom and a removed line's
> `isascii((type = *p++))`), and non-ASCII bytes as a proxy for `=XX` decoding
> (23 hits, all author names or em-dashes in comments).
>
> Fixed, sums regenerated, re-audited (253 clean), rebuilt, reinstalled.
>
> **Rule: never decode a mail-derived patch with `quopri.decodestring`.** Use a
> decoder that expands only `=XX` and `=\n`. And verify patch *content*, not
> just appliability.
>
### Adopted 2026-09-24 (evening) — one patch from `next-20260924` (252 -> 253)

The daily linux-next delta carried exactly one on-target commit.

| # | Subject | Why |
|---|---|---|
| `2417` | sched_ext: Avoid relocking DSQ during remote DSQ moves | 1-line change in `kernel/sched/ext/ext.c`: `move_task_between_dsqs()` drops `src_dsq->lock` while `p->scx.dsq` is still set, so the following `deactivate_task()` reacquires the lock just to unlink and clear it. Calling `dispatch_dequeue_locked()` before the unlock takes the `!dsq` path instead. **This machine runs scx full-switch** (`switch_all=1`, `scx_cake`), so `move_task_between_dsqs()` is live code. `Suggested-by` **and** `Signed-off-by: Tejun Heo`, plus `Signed-off-by: Usama Arif`. Not in rc4 or mainline. Applies clean to pristine rc4 **and in series order** |

**Everything else in the delta resolved to nothing:**

- **The `mm-unstable` zswap series reappeared with different shas** in `next-20260924` (`610bd40b3e3d` vs `349d75f4907c` for the dropbehind patch). That is linux-next **rebasing its branches**, not new content — the same patches we already adjudicated.
- **Work items updated since 2026-09-24:** 7 issues, all other-chip. `#5036` and `#5035` name "RDNA 4" in the title but their descriptions say **Navi 44 / RX 9060** — dropped.
- **sirlucjan's new 2026-09-24 commit** adds the **POC scheduler** (2890 lines). We run sched-ext, not POC.
- **sirlucjan `zstd-dev-patches-v5`**: our `2100` is **content-identical** (zero changed-line delta in both directions, byte-identical at 130533). We are already at the newest revision.
- **CachyOS `7.3`**: no new content. The branches are `hdmi` (09-21, already carried as `1163`/`1164`), `base`, `xswap` (deliberately removed), `cachy`, `fixes` (a `drm/gud` revert, not this hardware), and `vesa-dsc-bpp` (08-31, DSC `max_qp` bounds — 1080p240 on FRL6 does not use DSC).
- **firelzrd**: `lru-marie` is the same `0.11.1r2` we carry, `BORE 7.0.0` is a no-op under sched-ext, `le9uo` is from 2026-05.
- **Trees**: `torvalds` (now at `415f2044228`, "Merge tag 'landlock-7.3-rc5'"), `drm-next`, `agd5f-linux`, `amd-staging`, `akpm-mm`, `tip`, `linux-pm` — **0 on-key commits** since the previous pass.

### Deep work-items sweep, 2026-09-24 — nothing new to adopt

Exhaustive pass over the drm/amd tracker for this machine's silicon: **295
issues enumerated** across six search terms, paginated to exhaustion and
deduped (`9070` 174, `Navi 48` 198, `gfx1201` 43, `DCN 4.0.1` 36, `dcn401` 7 —
every term's row count matched its `x-total`). 32 dropped as other-chip, 187
on-target, **1642 comments read** via GraphQL. Of **629** distinct hex tokens
extracted, only **30 resolved to real commits**; the rest were GitLab
`/uploads/` paths (257), blob ids, UUIDs, register dumps and version strings.

**Every candidate resolved to nothing actionable here:**

| Finding | Verdict |
|---|---|
| `366e77cd4923` / `4408b59eeacf` / `afcdf51d97cd` — the "FPU protect" trio, posted by **agd5f himself across 12 issues**, the sweep's largest grouped find | **Already in rc4.** Verified individually with `git tag --contains` |
| `63e19ef3ddab` — the pageflip cluster, cited across 12 issues | **Already in rc4** (also recorded at line ~1188) |
| `c4a5160e3be0` (#5720, HDMI 4K60 black screen / RGB vs YCbCr 4:2:0) | **Already in rc4** |
| `24ddca9a3af1` (#4877, "Defer transitions from minimal state to final state") | Real AMD commit (Joshua Aberback, 137 insertions in `dc.c`/`dc.h`) with **no upstream equivalent — but it does not apply** to rc4 (`patch failed at dc.c:2963`), and it targets SubVP, which 1080p outputs do not use |
| #5446 — `amdgpu_driver_release_kms()` clears drvdata owned by vfio-pci | **Off-target.** A VFIO GPU-passthrough bug (unbind `amdgpu` → bind `vfio-pci` with a monitoring daemon holding the DRM node). No upstream fix exists, and this machine has one GPU and no passthrough |
| `572193a6e3a8` (#4230, mmhub page fault) | A **linux-firmware** "[FW Promotion]" blob, not kernel code |
| `00c391102abc` (#4753) | A **2024-04-26** commit, outside mainline; stale |
| Inline patches in notes (#4555 VCN5 decode perf, #4655 stutters, #5720, #4076) | #5720 and #4076's fixes are already in rc4; #4555/#4655 predate the window and carry no sha |

**Two traps this sweep demonstrated**, both worth keeping:
- **`a23cbb057` (#5339) resolves to a real commit and is still not a fix** — it is
  the mainline revision the reporter tested on, cited as a version identifier.
  Grep-and-verify alone files it as an unlanded patch.
- **`3467811` (#5274) is a GitLab note id** (`#note_3467811`) that is
  coincidentally a valid 7-hex prefix of an unrelated 2012 `xen-blkfront` commit.
  And `b89d58b` *is* real, but a 7-char prefix is collision-prone — check by
  subject, not just `cat-file -t`.

**Two issues were dropped as other-chip but are borderline and are recorded as
such:** #5135 and #5380 both name DCN 4.0.1 in the title while the reporter's
silicon is Navi 44. If Navi 44 shares the dcn401 display block, their fixes may
be generic. Re-run those two through the note pass at the next sweep.

### Two more adopted 2026-09-24, from a branch sweep (250 -> 252)

The all-branches pass over `agd5f-linux` (132 remote refs) surfaced display
commits that a tip-only scan does not show — most were test infrastructure, but
two are real fixes on this machine's display path.

| # | Subject | Why it is on-target here |
|---|---|---|
| `1169` | drm/amd/display: Fix null deref of link_enc in `dce110_enable_tmds_link_output` (Srinivasan Shanmugam) | **`dcn401_init.c:97` assigns `.enable_tmds_link_output = dce110_enable_tmds_link_output`**, so this is DCN 4.0.1's own TMDS (HDMI) hook, and the early-return guards a deref of `link->link_enc`. Smatch-reported by Dan Carpenter, `Fixes:` tagged, `Signed-off-by` + 2 `Reviewed-by` |
| `1170` | drm/amd/display: Fix LSDMA divide by zero (Alex Hung) | `element_size_to_bytes_per_pixel()` in **DML21** returned 0 for element sizes above 4, and an unexpected size divides by it. `dcn401_resource.c` sets `using_dml21 = true`, so DML21 is this machine's display mode library. `Signed-off-by` x2, `Reviewed-by`, `Tested-by` |

Both apply clean to pristine rc4 **and** in series order.

**Considered and not taken** from the same branch sweep:

- **`cb546fdd2cd1`** (clamp cursor hotspot at the register write) — touches
  `dcn401_hubp.c`/`dcn401_hwseq.c`, so it is genuinely our silicon, but it
  **fails to apply**: it sits on a cursor refactor chain (`3771cb44ea44` →
  `a7f51e8c53ca` → `026c7b8249d2` → `f1b4f58e60c1`) that is not carried. The bug
  it fixes needs the ODM/MPC slice case, which two 1080p outputs do not reach.
- **`bc7f95c8ddb6`** (Revert "request DMUB HW cursor offload") — its own
  rationale is *"causes the following failures on **DCN42**"*. DCN 4.2 is not
  this chip, and we do not carry the reverted commit, so there is nothing to
  revert.
- `16b705acfebe`, `9fc881919393`, `f1b4f58e60c1` — display refactors with no
  fix content, several depending on the same untaken cursor chain.
- The `Test …` / `Fold … tests` commits are unit-test additions, inert here.

**One adopted candidate was dropped during the series-order audit.** `9078`
(drm/amdgpu/userq: reserve the VM root BO around CWSR param validation) applies
to *pristine* rc4 in neither direction and references
`amdgpu_userq_input_trap_params_validate()`, which **does not exist in rc4** —
it is written against a newer base where that call was factored out. Fails
Check 2 (symbol existence) and is dropped. That is what the cumulative audit is
for: it applies the whole series in order, and three of the nine adopted
patches initially failed there (`2047` and `1073` needed rebasing or
reconstruction, `9078` was unfixable).

**Rejected, and why:**

- **`USB: core: sanitize string descriptors against C0`** (cachyos-fixes-v6
  #08) — a real robustness fix, but the reported device is an ASUS ROG Azoth
  dongle and this machine's USB tree is a Logitech receiver, a HyperX QuadCast
  S and two hubs. Generic hardening for a symptom not present here.
- **`sched/fair: do not scan twice in detach_tasks()`** (v6 #06) — **inert**:
  `fair.c` does not schedule under scx full-switch.
- The other ten patches in cachyos-fixes-v6 are for other machines (znver5,
  two i915 RC6 quirks for a Tuxedo InfinityBook, iwlwifi, Dell XPS `sof`, a
  touchpad, device-specific `btusb`, a motherboard BT entry, a `drm/gud`
  revert).
- **`GPIO-serialization-v4`** (linked from work item #5716) — the GitLab upload
  returns **HTTP 404**; not retrievable, so not adoptable and not assessable.

## The 2026-09-24 third-party pass — CachyOS, sirlucjan, firelzrd

These three were **listed in the inventory but not actually swept** in the
earlier passes; this closes that gap. All three are now current.

### sirlucjan — its local `master` was stale, and that hid real content

`repos/sirlucjan-kernel-patches` local `master` sat at `445db953f8` against
origin `b564922bc3` — **the same silent-staleness trap** that hit `torvalds`
and `lore-linux-mm`. The fetch had exited 0. The hidden diff added
`hdmi-patches-v2`, `bore-dev-patches`, `7.2/t2-patches-v2` and the `poc`
selector — 49,414 lines across 61 files. Load-bearing files were only visible
after reading `origin/master`.

| Candidate | Verdict |
|---|---|
| `7.3-rc/lru-marie-patches-v2` | **No update.** Ours is `0.11.1**r2**` and differs by exactly one changed-line pair; theirs is plain `0.11.1`. We are ahead. |
| `7.3-rc/hdmi-patches` → `-v2` | **Reflow only.** The v1→v2 delta is `!connector->display_info…` becoming `if (!connector->display_info…` plus a line re-wrap. No semantic change. |
| `7.3-rc/cachyos-fixes-patches-v6` | **Mostly off-target**, see below. |
| `7.3-rc/xswap-patches*` | Deliberately removed 2026-09-22 (backend is zswap + swapfile). |
| `bore-dev-patches`, `poc-selector` | Not carried: this machine runs sched-ext, not BORE/POC. |
| `7.2/t2-patches-v2` | Apple T2. Not this hardware. |

**`cachyos-fixes-patches-v6` is 12 patches and ten of them are for other
machines**: `znver5` (this CPU is Zen 4), two `drm/i915` RC6 quirks for a Tuxedo
InfinityBook, `iwlwifi`, a Dell XPS `sof` quirk, an ASUE140D touchpad, a
device-specific `btusb` VID/PID, a motherboard-specific BT entry, and a
`drm/gud` revert (USB display). Two are worth a decision:

- **`sched/fair: do not scan twice in detach_tasks()`** — **inert here**:
  `fair.c` does not schedule under scx full-switch.
- **`sched/core: Make finish_task_switch() always inline`** — **the premise
  holds on this machine.** Its argument is that the call is not inlined even at
  -O2 and that this costs when Spectre mitigations are active, because
  `finish_task_switch()` sits right after `switch_mm_irqs_off()`. This machine
  reads `spectre_v2: Enhanced / Automatic IBRS; IBPB: conditional; STIBP:
  always-on`, so mitigations are on and `finish_task_switch()` is core code that
  scx does *not* bypass. Carrying the CachyOS `fixes` squash is a judgement call
  the project has made before (`0105`/`0106`, last regenerated from **7.2-rc
  v11** per the notes) — **and it was not regenerated at the 7.3 bump, with no
  reason recorded.** Flagged as a gap rather than decided unilaterally.

- **`USB: core: sanitize string descriptors against C0`** — a real robustness
  fix (firmware leaves control characters in string descriptors, systemd then
  refuses `ID_SERIAL_SHORT` and mutter won't open the device). The reported
  device is an ASUS ROG Azoth dongle; not observed on this machine's USB tree
  (Logitech receiver, HyperX QuadCast S, two hubs). Generic hardening, not a
  fix for a symptom here.

### firelzrd — nothing to take

| Repo | Newest | Verdict |
|---|---|---|
| `firelzrd-lru-marie` | Marie LRU **v0.11.1r2**, 2026-09-15 | Same revision we carry (`2101`). No update. |
| `firelzrd-bore-scheduler` | BORE **7.0.0**, 2026-09-19 | **No-op here** — this machine runs sched-ext (`scx_cake`), not BORE. |
| `firelzrd-le9uo` | le9uo 1.15, 2026-05-01 | Stale, and inert under LRU-MARIE, which owns reclaim. |

### CachyOS — all 7.3 branches, not just the tips

Only three exist for 7.3: `7.3/hdmi`, `7.3/base`, `7.3/xswap`.

- `7.3/hdmi` — its head is `96f023bb8c13` *"Keep FreeSync for HF-VSDB VRR sinks
  in MCCS fallback"*, which **we already carry as `1163`** (plus `1164`). The
  rest of that branch is `1150`/`1151` (passive_vrr) and `1152` (VTEM). Synced.
- `7.3/base` and `7.3/xswap` — the latter is the xswap series we removed
  deliberately; the former is CachyOS's own tree, not a patch source.

### Work-item comments: the pageflip cluster is already fixed here

Scanning comment bodies across the 25 recently-updated on-target issues via
GraphQL, one commit shows up in **eleven** pageflip-timeout threads:
`63e19ef3ddab` — *"drm/amd/display: Atomize IRQ register read/modify/write
ops"*. The maintainers' reply on all of them is the same: *"Could you please
retest this on kernel 7.3-rc4 or later? There is a fix that may address this
issue: 63e19ef3ddab ... test with 7.3-rc4+."*

**We have it.** `merge-base --is-ancestor` confirms it is in `v7.3-rc4`, and
the symbols it introduces (`amdgpu_dm_irq_set()`, `amdgpu_dm_irq_ack()`,
`amdgpu_dm_irq.h`) are present in the rc4 tree. AMD's recommended fix for this
machine's documented symptom area is therefore already in the base — worth
recording precisely because the symptom *looks* like the one this machine has
history with.

Also confirmed from the same pass: our **`1163` is an AMD posting**, not our
own work — `[PATCH v1 3/3] drm/amd/display: Keep FreeSync for HF-VSDB VRR sinks
in MCCS fallback`, Fangzhi Zuo `<Jerry.Zuo@amd.com>`, 2026-09-01,
`lore-dri-devel` `115cfc056b8d`. Only `1164` (the revert of `cfdcf5571c31`) is
local. That matters for the `6f742bc837f1` analysis above: the exemption it
would undo is AMD's, not ours.

No other issue's comments produced an uncarried fix.

## REBASE 2026-09-27: v7.3-rc4 -> v7.3-rc5 (268 -> 257 patches)

`v7.3-rc5` was cut 2026-09-27 (`72d3fcf802c`); the watcher caught it and the
series was rebased the same evening. `pkgver` `7.3.0_rc4` -> `7.3.0_rc5`,
`pkgrel` reset to 1.

### Eleven patches dropped — all now upstream in rc5

The cumulative audit against rc5 reported **11 patches `Skipping patch`**, which
the script correctly treats as a defect rather than a success. Each was verified
by hand as **genuinely present in rc5**, then removed:

| # | Subject | Why |
|---|---|---|
| `1076` | amdgpu: vmid_wait fence leak in `amdgpu_ring_init()` | adopted 2026-09-26 *from* the rc5 DRM pull — naturally in rc5 |
| `1077` | amdgpu: last_update fence leak in `amdgpu_vm_init()` | same |
| `1078` | amdgpu: runtime PM leak in `amdgpu_debugfs_test_ib_show()` | same |
| `1079` | amdgpu: acpi device leak in `amdgpu_acpi_enumerate_xcc()` | same |
| `1080` | amdkfd: use-after-free in `kfd_dev_mapping` | same |
| `1174` | display: dc stream excess put in `dm_update_crtc_state()` | same |
| `9079` | amdgpu/userq: double jiffies conversion in hang detect | same |
| `9080` | amdgpu: move userq fence wait out of signalling section | same |
| `2040` | net/sched: reject idr error pointers | merged upstream in the rc4→rc5 window |
| `2043` | fs: avoid repeated scans in `evict_inodes()` | merged upstream in the rc4→rc5 window |
| `2153` | writeback: Tasks-RCU quiescent state per cgwb drain | merged upstream in the rc4→rc5 window |

**Two of the eleven reverse-applied *cleanly* to rc5 and still needed dropping**,
which is the documented reverse-apply false negative in its milder form: `9080`
and `2043` failed the reverse check while their content was plainly present —
`amdgpu_eviction_fence.c:71` carries `9080`'s exact comment and call, and rc5's
`evict_inodes()` has `2043`'s restructure (no `again:` label, the `need_resched`
block in place) with only the comment wording differing from the posted version.
Both were confirmed by content probe, not by the apply check. That is why the
rule is *grep the identifiers the patch introduces*, not *trust reverse-apply*.

### CachyOS branch patches: nothing to regenerate

The audit passes with every `01xx` unchanged, and sirlucjan's sources for the
branches we carry (`bbr3-cachyos-patches-sep`, `kbuild-patches-sep`,
`cpu-isa-patches-sep`) have **zero changed files** between our local `master`
(2026-09-18) and `origin/master` (2026-09-24).

sirlucjan's 8 new commits add, for the 7.3-rc line: `hdmi-patches-v2` — the
rebundle already assessed here as *"a rebundle of work we already carry, not an
upgrade"* — and a new `sched-7.3-introduce-POC-selector` (a scheduler feature we
do not use; this machine runs scx). Neither is adoptable.

**Note the stale-local trap fired again:** local `master` was 8 commits behind
`origin/master` after a clean-looking fetch. Always read `origin/<branch>`.

## Sweep 2026-09-27 12:36 — nothing to adopt (post-shutdown pass)

Machine had been off 05:34–12:24, so this pass covers ~7.5 h of upstream time.
**Nothing adoptable.** Per-source:

| Source | Result |
|---|---|
| `linux-next` | **No new tag.** Newest is still `next-20260925` — it is the weekend, and linux-next publishes on weekdays |
| `torvalds` | **unchanged** at `fd179f8a05b` |
| `tip` | `a14fcf2723cc` → `f23427766130`, but every AMD commit in the delta is one **already dispositioned** — the rc5 fixes we adopted as `1076`-`1080`/`1174`/`9079`/`9080`, the DML frame-warn trio (rejected), the `vcn5.0.1`/`vcn4.0.3` pair (wrong chip), and `4fde4482251` (NBIO, not our silicon) |
| `agd5f-linux` | unchanged at `a24db07159cd` (2026-09-17) |
| `drm-misc` | no TTM / dma-buf / sched change. See the mirror note below |
| lore mirrors | refreshed; weekend volume is small (netdev 61, dri-devel 5, mm 5, io-uring 3, block 1) |
| work items | 1 on-target updated (`#5894`) — a "will retest when firmware lands" reply, no fix |
| version sweep | same 10 higher-version postings; all already dispositioned |

### Candidate recorded, NOT adopted: io_uring TX_TIMESTAMP multishot

`4797a0bd87c9` — *"io_uring/cmd_net: end TX_TIMESTAMP multishot when the CQ is
full"* (`Fixes: 9e4ed359b8ef`, `Cc: stable@vger.kernel.org`). The bug is real and
**present in our base**: `io_uring/cmd_net.c` exists in rc4 with
`io_uring_cmd_post_mshot_cqe32()` (line 101) and `SOCKET_URING_OP_TX_TIMESTAMP`
(line 184). Aux CQEs have no overflow backing, so the multishot loop fails once
the CQ ring fills, splices unprocessed skbs back and returns `-EAGAIN`, which is
`IOU_RETRY` — so the request idles until the next poll event instead of ending.

**Not adopted: no `Reviewed-by`, and the posting is hours old** (2026-09-27
15:42, three hours before this pass). Same bar that deferred the ATOM
parameter-space pair. Revisit when it has review, or if it appears in a
drm-fixes-style pull.

### `repo.or.cz` is no longer a reliable drm-misc source

Last pass it served a **newer** tip than freedesktop (`f7afecd542`, 09-23);
this pass it advertises `98c7fc4219` (2026-06-25) — **backwards**. Freedesktop
now reports the same `98c7fc4219`, so the branch itself was rebased between
merge windows (normal for a development branch), but the episode shows the
mirror can serve a stale tip. **Query freedesktop first and use repo.or.cz only
as a cross-check**, not as the primary.

## Sweep 2026-09-27 05:02 — nothing to adopt

Scheduled overnight pass. **Every source was queried; none produced an
adoptable patch.** Per-source, so "found nothing" is distinguishable from
"did not look":

| Source | Result |
|---|---|
| `linux-next` | **No new tag.** Remote's newest is still `next-20260925`; no `next-20260926/27` was cut |
| `torvalds` | advanced `6812ce4e437` → `fd179f8a05b`, 64 new commits. One on-target candidate (below); the rest are arm64/RISC-V KVM, ata, and probes |
| `tip` | advanced `630761837841` → `a14fcf2723cc`, 305 new commits. Three `perf/x86/amd/uncore` commits — all optimizations, no `Fixes:` tag (below) |
| `agd5f-linux` | 1 new commit: `15814c01ac57` DML frame-warn "all builds" — already rejected 2026-09-26 as inert |
| `amd-staging-drm-next`, `akpm-mm`, `linux-pm` | unchanged |
| `drm-misc` (via repo.or.cz) | **no TTM / dma-buf / scheduler change** since 09-23 |
| `lore-amdgfx`, `lore-dri-devel`, `lore-sched-ext`, `lore-linux-block`, `lore-io-uring`, `lore-netdev-new`, `lore-linux-pm`, `lore-fsdevel-new`, `lore-linux-nvme` | refreshed to 2026-09-26/27; **no new DRM fixes pull** (no `[git pull] drm fixes` since the rc5 one we mined) |
| `lore-linux-mm` | **initially appeared stale at 2026-09-24 — that was my fetch, not the mirror.** A plain `fetch origin` in a mirror clone only updates `FETCH_HEAD`; the explicit refspec `+refs/heads/master:refs/heads/master` advanced it to **2026-09-27**, exposing **172** unseen patch mails. Swept: all feature series (batched rmap/swapfile, guest_memfd, bpf_proactive_reclaim) plus two `mm/hugetlb` fixes — the latter irrelevant here (no hugepages on this desktop), and one is explicitly a `[PATCH 5.10.y]` stable backport. **Nothing to adopt.** |
| work items | 3 on-target updated (`#5900`, `#5896`, `#5894`); **no new fixes** — `#5894` is a firmware fix, the other two have no comments |
| version sweep | same 10 higher-version postings as 2026-09-26; all already dispositioned |

### The one candidate worth recording: AMD NBIO enhanced atomics

`4fde4482251` — *"x86/PCI: Disable enhanced atomics on AMD NBIO 7.7 and 7.11"*
(Mario Limonciello, `Signed-off-by` from Bjorn Helgaas, `Cc: stable@vger.kernel.org`).
**This is a data-corruption fix**, and it is the most serious thing in the pass:

> *"Multiple users report data corruption during 64-bit DMA transfers on
> systems with AMD NBIO 7.7 and 7.11 controllers. This occurs when BIOS enables
> AMD 'enhanced atomic operations' on PCIe Root Ports. When enhanced atomics
> are enabled, any 64-bit DMA access may be corrupted."*

**Rejected as not-our-silicon, and this is the check that decided it.** The quirk
registers by PCI device ID:

| ID | Part | Ours? |
|---|---|---|
| `0x14E8` | Phoenix / Hawk Point (NBIO 7.7) | no — mobile APU |
| `0x1507` | Strix / Krackan (NBIO 7.11) | no — mobile APU |
| `0x1122` | Strix Halo variant (NBIO 7.11) | no — mobile APU |

Our root complex is **`1022:14d8` "Raphael/Granite Ridge Root Complex"** — desktop
Zen 4, and **not in the list**. rc4 has no existing enhanced-atomics quirk for
any AMD ID. So AMD scoped this to mobile parts; adding Raphael would be
inventing an erratum AMD has not published.

**Revisit if a Raphael/Granite Ridge corruption report appears** — that is the
trigger, not a date.

### Rejected: `perf/x86/amd/uncore` (three commits, tip)

`6350de8671b9` (free counter slot by index), `4a8557a4e5d2` (remove redundant
slot scan), `df935e26ca9a` (events as a flexible array). The code does run here
(Zen 4 has uncore PMUs) but all three are **optimizations or refactors with no
`Fixes:` tag** — the first turns an O(N²) teardown into O(N), the second skips a
scan, the third merges two allocations. Nothing is being repaired, and the
package targets no bloat. Not carried.

## Version sweep 2026-09-26 — every carried patch against its latest posting

The pass the sweep skill calls step 2: 268 carried patches checked against all
11 lore mirrors (18,260 distinct normalised subjects). Ten carried patches had a
**strictly higher-version posting** upstream. Seven died to Filter 2, and the
three survivors died to reasons worth recording.

| Carried | Ours → posted | Verdict |
|---|---|---|
| `2037` net/neighbour proxy timer | v1 → v2 | resend — changed lines identical |
| `2039` net/sched qdisc_alloc_handle | v1 → v3 | resend — identical |
| `2049` io_uring sqpoll RCU | v1 → v2 | resend — **it *is* the v2 we just adopted**; our header drops the `v2` marker, so the comparison always says v1 |
| `2144` xarray xas_find | v1 → v2 | resend — identical |
| `2151` shmem forced collapse | v1 → v2 | resend — identical |
| `2154` page_alloc bulk GFP | v1 → v3 | resend — identical |
| `2185` mm/swap off-by-one | v1 → v6 | resend — identical |
| `1151` passive_vrr | v1 → "v4" | **posting is OLDER than the carry** — v4 is 2026-02-16, ours is 2026-09-01. The documented false positive; the version number says nothing about recency |
| `2415` sched_ext NMI kfuncs | v1 → v3 | **superseded by our own pair.** The v3 adds an `in_nmi()` check to `scx_kf_allowed()`, but it is written against the pre-split `kernel/sched/ext.c`; our carry targets `kernel/sched/ext/ext.c` and uses `scx_kf_allowed_ctx()`, with the NMI rejection living in `2414` (`scx_locked_rq()` returns NULL from NMI) |
| `2032` tcp collapse timestamps | v2 → v3 | **real update — adopted** (below) |

**Seven of ten were resends.** That is the expected shape: a higher `vN` is
usually a rebase or a repost, and `lset()` on the changed lines is what tells
them apart. Do not skip Filter 2 — a version-number sweep without it reports
ten actions where one is real.

### The one real update: `2032` → v3

`[PATCH v3 net] tcp: preserve timestamps across receive queue collapse`
(Jason Xing, 2026-09-24, `Fixes: 98aaa913b4ed`) adds one line our v2 lacks:

```c
	memcpy(nskb->cb, skb->cb, sizeof(skb->cb));
+	TCP_SKB_CB(nskb)->has_rxtstamp = false;
```

v3's changelog says it came from **Eric Dumazet**: *"fix a corner case (where
an skb can contribute no bytes if OOO happens) spotted by AI and Eric"*. The
`memcpy` of `cb` inherits `has_rxtstamp` from an skb that may contribute no
bytes (a fully-covered skb left in the ofo tree by `tcp_ooo_try_coalesce()` →
`coalesce_done`), so the new skb could advertise an RX timestamp it does not
have. Clearing it first makes the conditional block the only place that sets it.

It scored **NEITHER** in the first dry-run — forward failed on the second hunk
(already carried), reverse failed on the first (not carried). That is the
*partial* signature, not a duplicate: our tree has hunk 2 and lacks hunk 1.
Verified by reverting our v2 to base and applying v3 at that exact series
position — both checkers clean.

### The duplicate I nearly added — and the reason I missed it

`#5870` (an `amdgpu_sync_add_later` use-after-free on RX 9070 XT) has a
commenter pointing at Donggeun Yoo's *"don't release the fence reference
consumed by the scheduler"*. The bug is real and I verified it from source:
`drm_sched_job_add_dependency()` puts the incoming fence both when
deduplicating and when `xa_alloc()` fails, and stores it otherwise — so every
path consumes it, and the callers' `dma_fence_put()` on error is a double put.
Unchanged in `next-20260925`, so it is live. I numbered it `1081` and was one
step from building it.

**We already carry it as `1064`** — the same three files, the same hunks, and
CLAUDE.md names `1064` as the worked example of this exact mistake. The check I
ran to rule it out was:

```bash
rg -l 'dma_fence_put(f)' sleepy-next/patches/     # matches nothing
```

`(f)` is a **capture group**, not a literal — that regex matches the string
`dma_fence_putf`, which appears nowhere, so the search came back empty and I
read the silence as "no patch touches this". It needed `dma_fence_put\(f\)`.

Two rules, one old and one new:

- **Escape the parentheses.** A grep for a C function call must escape `(`/`)`,
  or it silently matches nothing — and "nothing" is indistinguishable from
  "clean" unless you also grep for something you know is there.
- **Grep the *subject* and the *function*, not just an identifier you pick.**
  The rule was already written down and I still skipped it. `rg -l 'consumed by
  the scheduler' sleepy-next/patches/` would have found `1064` immediately.

## ADOPTED 2026-09-26: `2049` — io_uring SQPOLL task-work publication UAF

`[PATCH v2] io_uring/sqpoll: protect task-work publication with RCU`,
Jérémy Jean `<Jeremy.Jean@oss.cyber.gouv.fr>`, 2026-09-25,
`lore-io-uring` `7512dd8004b2`, `Fixes: af5d68f8892f` ("io_uring/sqpoll: manage
task_work privately").

**The bug is in our base, confirmed by reading rc4 directly.**
`io_uring/tw.c:226` in `v7.3-rc4` reads `tctx->task` *after*
`mpscq_push()`; SQPOLL can consume the request immediately, drop the final
ring reference, and free `ctx`/`tctx` underneath. The reporter's KASAN trace:

```
BUG: KASAN: slab-use-after-free in io_req_normal_work_add+0x439/0x510
BUG: KASAN: slab-use-after-free in queue_work_on+0x25/0x70
```

**Why this one is adopted, and it is not the author's first design.** The v1
patch pinned the task with `get_task_struct()`/`put_task_struct()` around the
push. **Jens Axboe rejected that approach on the list:** *"Thinking about this
a bit more, I think the following fix would be better: 1) Add a `guard(rcu)()`;
in `io_req_normal_work_add()` at the top, which is how we handle this for
DEFER_TASKRUN as well. 2) And similarly, expand the `synchronize_rcu()` run in
`io_ring_exit_work()` to also include `IORING_SETUP_SQPOLL`. I think that's both
a cleaner and more efficient fix, rather than fiddle with task_struct
references."*

**v2 implements exactly that**, hunk for hunk. So the `Signed-off-by` is the
reporter's, but the design is the maintainer's, prescribed in the thread — which
is why this clears the bar despite carrying no `Reviewed-by`. Taking v1 here
would have been taking a fix the maintainer had just argued against.

**On-target?** It is not hardware-specific, but the code path is live: the
sequence is reachable by any `IORING_SETUP_SQPOLL` user whose completion drops
the last ring reference. The fix is three hunks over two files, it applies
cleanly to the 267-patch series tree with both checkers, and it pairs its
`guard(rcu)()` with the widened `synchronize_rcu()` exactly as intended — the
two halves are useless apart, so they must be carried together or not at all.

### Not adopted from the same sweep

- **`sched-ext`** (9 postings since 09-24): `Use fetching atomics for cmask`,
  `Test scx_has_subs() inline before calling sub-sched hooks`,
  `Count cap-rejected local DSQ inserts in SCX_EV_SUB_REJECT`, and Andrea
  Righi's `sched_ext/for-7.4` CID/numa kfunc work. **None carries a
  `Reviewed-by`/`Acked-by` and none is in `next-20260925`.** The CID kfunc is a
  new feature, not a fix.
- **`linux-pm`** (31 postings): nothing touching amd-pstate, CPPC, ACPI or
  cpuidle — the nearest is a hibernation secretmem fix.

## ADOPTED 2026-09-26: `2197` — SLUB prefilled sheaves refill from the barn

`mm/slub: refill prefilled sheaves from the barn`, Hao Li `<hao.li@linux.dev>`,
2026-09-21, `slab.git` `1b87ea06a34b213e45e3e0c4effd5043f15046ed`.
`Reviewed-by: Vlastimil Babka (SUSE)` — the SLUB maintainer —
`Reviewed-by: Harry Yoo (Meta)`, `Signed-off-by: Harry Yoo`.

**What it fixes.** The prefill API refilled a non-full sheaf from partial slabs
and *never* from the full sheaves in the barn, so once the barn's full list
filled up it stayed full — and every `kfree_rcu()` sheaf then had to be flushed
to slabs because there was no room. The patch lets the refill drain the barn
first and adds a partial sheaf to hold the leftovers, so every full sheaf taken
out makes room for a future RCU sheaf.

**Why it is on-target here, not merely applicable.** The prefill API has
exactly one caller in the tree — `lib/maple_tree.c:154` and `:160`
(`kmem_cache_prefill_sheaf()` / `kmem_cache_refill_sheaf()` on
`maple_node_cache`) — and the maple tree backs every process's VMA mapping, so
the path runs constantly. The author's benchmark is will-it-scale `mmap1` on
that same `maple_node` cache: `27778727 -> 34500556`, **+24.2%**.

**Isolation check.** `rg -l 'mm/slub.c' sleepy-next/patches/` returns nothing —
no other carried patch touches this file, so there is no interaction with
LRU-MARIE, gup batching, zswap or zstd. Both checkers pass against the
266-patch series tree.

### Recorded uncertainty — drop this one first

Stated plainly because it is the weakest part of the entry: **this is an
optimization, not a fix.** There is no `Fixes:` tag, so unlike the rest of this
series it is not repairing a known defect on this machine. Two consequences:

- **The measured benefit is from a synthetic.** 192-process will-it-scale
  `mmap1` is not this desktop's workload. The real gain here is unmeasured and
  likely much smaller; it is carried because the path is demonstrably live, not
  because a speedup was observed on this machine.
- **It has not been through a full -rc cycle.** It sits in `slab.git` for-next,
  i.e. 7.4 — maintainer review is not the same as mainline exposure. A subtle
  bug in a core allocator is a severe failure mode, so this patch is the first
  thing to drop if anything unexplained appears: allocation failures, slab
  warnings, `BUG: Bad page state`, or anything in `dmesg` naming
  `barn`/`sheaf`/`slub`.

It is one self-contained file and reverts cleanly, which is what makes carrying
it an acceptable risk rather than a reckless one.

## Sweep 2026-09-26 — the 7.3-rc5 DRM fixes pull (258 -> 267)

The highest-yield source this pass was not a tree but a **pull request**.
`[git pull] drm fixes for 7.3-rc5` (Dave Airlie, `lore-dri-devel`,
`CAPM=9twjOfCE5-LzepSB58uaQtn4kS2yF2sOu52kiJp2xkJXkQ@mail.gmail.com`, merged
into torvalds as `6812ce4e4379`) carries 60 non-merge commits, 13 of them AMD —
and every one is a **fix for the kernel we are running**, since our base is
rc4 and these are the rc5 fixes.

**Why the PR and not the tree.** `repos/torvalds` had the merge; the branch is
60 commits, of which 13 are ours. Reading the PR body first made the triage
almost mechanical — the summary lines name exactly the areas ("Display ref
count fix", "Userq fixes", "VCN 4, 5 reset fixes").

### Adopted (8)

| # | Commit | Subject |
|---|---|---|
| `1076` | `aea841bc62a` | amdgpu: Fix vmid_wait fence leak in `amdgpu_ring_init()` |
| `1077` | `b4f7b4459b1` | amdgpu: Fix last_update fence leak in `amdgpu_vm_init()` |
| `1078` | `2b86ab1bd66` | amdgpu: Fix runtime PM leak in `amdgpu_debugfs_test_ib_show()` |
| `1079` | `a997baa6117` | amdgpu: Fix acpi device leak in `amdgpu_acpi_enumerate_xcc()` |
| `1080` | `c3a31087b1c` | amdkfd: fix use-after-free and multi-container gap in `kfd_dev_mapping` |
| `1174` | `c5fd4eaad50` | display: Fix dc stream excess put in `dm_update_crtc_state()` |
| `9079` | `cd195f1616b` | userq: fix double jiffies conversion in hang detect timeout |
| `9080` | `3022bdfe3e6` | amdgpu: move userq fence wait out of signalling section |

Seven apply clean as posted. `9080` needed **rebasing**, and the reason is worth
recording: all three of its hunks target code we still have verbatim, but one
context line in `amdgpu_userq.h` drifted because **our own series changed
`amdgpu_userq_ensure_ev_fence()` from `void` to `int`**. That is the standing
"a clean dry-run at a large offset in a subsystem we patch heavily means one of
our own patches is in there" rule, in its benign form. Rebased by applying with
GNU patch to a copy and regenerating the diff; the added and removed lines are
byte-identical to upstream's, only line numbers and that one context line
differ. Both checkers pass on the result.

`9078` was skipped deliberately — it is a **burned number** (adopted then
dropped on 2026-09-24 when it turned out to reference a symbol absent from
rc4). The gap is the evidence.

### Rejected (5)

- **`15814c01ac5`, `18779dd8451`, `0fd5e9ddf36` — the DML frame-warning-limit
  family.** They exist so the DML build stops *failing* under `CONFIG_WERROR`
  (and, for the UBSAN one, under sanitizers). **None of that applies here:**
  `CONFIG_WERROR` is not set, nor `CONFIG_UBSAN`, nor `CONFIG_KASAN`. Our
  `dc/dml/Makefile` sits at `frame_warn_limit := 2048` against
  `CONFIG_FRAME_WARN=2048`, so `test-lt` is false and the per-directory flag is
  **not even emitted**. The family would silence warnings we do not treat as
  errors — and it *removes* a real signal, since a 2512-byte stack frame on a
  16 KiB stack is worth seeing. Inert, and inert in the wrong direction.
- **`f952ed353a2` (vcn5.0.1) and `6b13ddbf5bb` (vcn4.0.3) — video_timeout unit
  mismatch in the JPEG reset wait.** Real bugs: `adev->video_timeout` is in
  jiffies and `amdgpu_fence_wait_polling()` takes usecs, so the intended ~2 s
  wait is a couple of microseconds. **Not ours, and this was checked the hard
  way rather than by filename.** `amdgpu_discovery.c:2946` shows
  `IP_VERSION(5,0,0) -> vcn_v5_0_0_ip_block`, and the running kernel reports
  `vcn_v5_0_0`, so we take `vcn_v5_0_0.c`, not the patched `vcn_v5_0_1.c`.
  Then the important half: grepping the whole `amdgpu/` tree for the
  *unconverted pattern* `amdgpu_fence_wait_polling(... video_timeout)` returns
  exactly two files, `vcn_v4_0_3.c:1692` and `vcn_v5_0_1.c:1338` — and both our
  `vcn_v5_0_0.c` and `jpeg_v5_0_0.c` have **zero** occurrences of either
  identifier. So there is no latent equivalent on our silicon. The counter-case
  that made this worth doing: `vcn_v5_0.c` does not exist in this tree at all,
  so filename-matching would have been wrong in both directions.

### `#5663` — our `1074` confirmed as the current fix

Read through the work-items tracker this pass (see the GraphQL note below).
Issue `#5663` is a **Navi 4x SDMA hardware bug** — König: *"this is not related
to suspend/resume but rather seems to be a HW bug in the SDMA on Navi 4x"* —
producing accumulating DCC corruption across sleep/wake on **RX 9070 XT**, this
machine's exact GPU.

Two things worth recording:

1. **`1074` is the v2 patch, and it is what the reporter of the fix calls
   current.** `pepp` posted the original `e = 0` per-blit workaround on
   2026-09-16; on **2026-09-25** he wrote that it *"makes the issue much less
   likely but it doesn't fix it completely"* and linked
   `lists.freedesktop.org/archives/amd-gfx/2026-September/153767.html` as *"going
   to be merged soon"*. That mail is
   `[PATCH v2] drm/amdgpu: implement workaround for sdma dcc corruption`,
   `20260924140616.2647-1-pierre-eric.pelloux-prayer@amd.com` — **the commit we
   already carry as `1074`**. A user on 2026-09-26 confirms *"the v2 patch works
   for me"* on a kernel containing it.
2. **It is an acknowledged interim workaround.** The same comment says it *"will
   be revisited once the root cause is understood"*. Do not treat DCC
   corruption on this GPU as closed if it reappears; the standing mitigation
   users report is `AMD_DEBUG=nodcc` or `QSG_RHI_BACKEND=vulkan`.

**Work-item comments are readable again — via GraphQL.** The REST `/notes`
endpoint is 401-gated, but `POST /api/graphql` with
`{ project(fullPath: "drm/amd") { issue(iid: "5663") { notes(first: 100) { nodes { body createdAt author { username } } } } } }`
returns them unauthenticated (plain `curl`, no User-Agent). `first:` must be
sized per issue. This restores the comment sweep the 2026-09-24 pass had to skip.

### `next-20260925` — nothing

1520 non-merge commits. The on-target hits are all 7.4 refactoring —
`mm/sparse` (twelve commits from Hildenbrand), `mm/damon`, `mm/hugetlb`,
`mm/swapops` — none of them fixes. One AMD commit,
`e74db71a3530` "amdgpu: Enable PerfOpt IOMMU perf optimization", is **wrong
chip**: its own message says *"The AMD IOMMU spec indicates this is only
supported on integrated GPUs so check explicitly for `AMD_IS_APU`"*, and the
RX 9070 XT is a discrete GPU.

## drm-misc (TTM / dma-buf / dmemcg) — swept, and where to get it when freedesktop is down

The 2026-09-24 sweep could not reach this subsystem: every request returned
**HTTP 503**. It was a freedesktop outage, not a dead host — by the next
session every endpoint answered again (`/drm/misc/kernel.git/info/refs`, the
`drm/kernel.git` path, and the GitLab API all return 200). `drm-misc-next`
fetched fine and is now at `8ef59ee79` (2026-09-21); only `drm-misc-fixes`
still 503'd.

### Where to get it when freedesktop is down

Tried in this order; the first two are the useful ones.

| Source | Status | Notes |
|---|---|---|
| `git.kernel.org/.../next/linux-next.git` | **works, different infrastructure** | drm-misc-next is merged in daily. The `drm-misc` merge commit is in `next-YYYYMMDD` — e.g. `f10d8e0012dc next-20260921/drm-misc`, with the branch tip as its second parent. **The best fallback: different host, different operators, already cloned here.** |
| `repos/lore-dri-devel` | **works, local** | Every drm-misc patch passes through dri-devel with its review tags. Best source for patch *content and provenance*; carries no tree topology. |
| `repo.or.cz/drm/drm-misc.git` | **reachable, and was the freshest** | Verified by `git ls-remote`: has `drm-misc-next`, `drm-misc-fixes` and `drm-misc-next-fixes`. **Its `drm-misc-next` was newer than the freedesktop copy** (2026-09-23 vs 2026-09-21) — see the correction below. Fetch from it with `--shallow-since`; a plain fetch **silently no-ops** against our shallow clone. |
| `cgit.freedesktop.org`, `anongit.freedesktop.org` | **dead** | Both fail to connect at all (curl code 000). The 2024 GitLab migration left these as read-only pull mirrors; they are not a fallback. |
| `git.kernel.org/.../drm/drm-misc.git` | **does not exist** | 404. kernel.org does not mirror the drm trees. |
| GitHub | **no mirror** | `freedesktop/drm-misc`, `drm-misc/linux` and `danvet/drm-misc` are all 404. `mripard/linux` exists but is Maxime Ripard's personal fork — 36 heads, no drm-misc branch. Do not treat it as a mirror. |

### CORRECTION (same day): the first pass used a stale tip

The entry above originally claimed the sweep was complete. It was not. The
freedesktop fetch had **503'd partway** — it left `origin/drm-misc-next` at
`8ef59ee79` (2026-09-21) while the branch was really at `f7afecd542`
(**2026-09-23**), which `repo.or.cz` then served. A partial fetch that leaves
an older tip is indistinguishable from a complete one unless you compare tips,
so: **after any 503, check the tip against a second source before trusting the
sweep.**

Two fetch traps came out of this, both worth the ink:

- **A plain `git fetch <orcz> +refs/heads/X:refs/remotes/orcz/X` into our
  *shallow* clone exits 0, does two `POST git-upload-pack` round trips, and
  writes no ref and no `FETCH_HEAD`.** It looks like success. `--shallow-since`
  makes it actually fetch. The shallow boundary is the difference: without it
  the negotiation concludes there is nothing to send.
- `git merge-base --is-ancestor` against `repos/torvalds` is meaningless for
  commits outside the shallow window — it reports "not an ancestor" for
  commits that *are* in rc4. Where the object is missing, probe content
  instead. In the table below, "in rc4" means the object resolved and the
  ancestry check actually ran.

### Re-swept against the newer tip: still nothing to adopt

The 2026-09-21 → 09-23 delta adds seven TTM / dma-buf / sched commits the
first pass never saw. Each is inert or already in the base:

| Commit | Subject | Why not |
|---|---|---|
| `3db7d7d583` | ttm: fix swapped-out resources never leaving their bulk_move range | **already in rc4** — a genuine use-after-free fix, but the base has it |
| `fcfe64715b` | ttm: apply the swapout bulk_move fix to the intended condition | **already in rc4** |
| `2ab510e631` | drm/sched: Fix virtual runtime race | **inert here.** Fixes the *FAIR* policy's rq insertion; `sched_main.c:87` sets `drm_sched_policy = DRM_SCHED_POLICY_FIFO` and the module param doc calls FAIR "experimental". amdgpu selects no policy. |
| `2302669bb4` | drm/sched: Free the run queues at the end of `drm_sched_fini()` | Robustness only — its own commit message says *"no correct driver can be there"* |
| `3ed11c671f` | dma-buf/dma-fence: fix checking signaling bit for timeline and driver name | in rc4 |
| `b344ca94e8` | dma-buf: Fix silent overflow for phys vec to sgt | in rc4 |
| `06dd5e1ae8` | dma-buf: Split sgl by largest page-aligned chunk | in rc4 |
| `143755bdab` | dma-buf: Make `DMABUF_DEBUG` default to y on `DEBUG_KERNEL` | in rc4 |
| `28cc4d5a75` | drm/sched: Create a fake device for KUnit tests | in rc4 |

The two TTM ones were checked by **content**, not ancestry, because they matter:
`ttm_bo.c:1437` reads `if (ret > 0)` and `ttm_bo.c:535` reads `if (ret)` in
both rc4 and the series tree — which is precisely the pair `3db7d7d583` +
`fcfe64715b` establish. The base is correct on both.

### What the first pass found: nothing to adopt

469 non-merge commits in `drm-misc-next` since 2026-09-01; **29** touch
`drivers/gpu/drm/ttm`, `drivers/dma-buf`, `drivers/gpu/drm/scheduler` or the
`dma-buf`/`dma-fence`/`dma-resv` headers. Sorted out:

- **`CONFIG_DMEM*` is not set here**, so the whole cgroup/dmem / dmem-controller
  line — `425a783e1` "Hook up a cgroup-aware reclaim callback for the dmem
  controller" and Natalie Vock's four-patch `ttm` charge/reclaim series
  (`4e6d9bc15`, `3f356c0e3`, `3d33e9c72`, `bbc744c06`) — **cannot execute on
  this machine**. That is most of the recent TTM churn, and none of it is ours.
- **`0e118b936`** `drm/sched: Lock drm_sched_entity_is_idle()` (Philipp Stanner,
  `Reviewed-by: Tvrtko Ursulin`) is the only real fix in the set — it replaces
  an invalid lockless read of `entity->stopped`/`entity->list` with the
  spinlock. It is **already carried as `1056`**.

  Worth recording *how* that was established, because `git apply --check`
  failed on it while GNU `patch` said *"Reversed (or previously applied) —
  Skipping"*. Neither is trustworthy alone. The identifier probe settled it:
  `v7.3-rc4:…/sched_entity.c:210` still reads `rmb(); /* for list_empty to work
  without lock */`, while our series tree has the `spin_lock(&entity->lock)`
  form. Same shape as the `1227` amd-pstate case — the fix is carried inside a
  patch found by grepping the *function*, not the subject.
- Everything else is docs, kernel-doc, coding style, `MAINTAINERS`, or a
  refactor (`ttm_swap_ops` static, `drm_class_device_*` removal, dropping the
  unused `drm_sched_fence_alloc()` argument, the `is_cow_mapping` move).

Also checked and already in rc4: `30d0aff2c` `dma-buf: dma-heap: don't publish
fd before copy_to_user()` and the `drm/sched` fair-policy reverts
(`67cf83ac8`, `9e9da8625`, `2bbea6b81`, `9a11db688`).

## Live dispute over `1065`/`1066` — three postings, none adopted

The upstream-revert pass (triage.md) turned up an active argument about two
patches we carry, so it is recorded here in full rather than as a one-liner.

**What we carry.** `1065` (`reserve eviction-fence slot at WPTR caller`) and
`1066` (`reserve root PD fence slots for userq eviction-fence rearm`) reserve
`dma_resv` fence slots up front so `amdgpu_evf_mgr_rearm()` cannot fail with
`-ENOSPC` when it later adds an eviction fence.

**Posting 1 — the revert** (`c091c58ee9` + `9e785a48cb`, 2 of a 3-part series,
2026-09-17, Vitaly Prosyak): reverts both, on the argument that the up-front
reservation is the wrong place. **Rejected here, and already on record:**
CLAUDE.md's trap list says König defended `1065`/`1066` against exactly such a
series — *"a revert of a carried patch is the opposite of superseding it."*
No maintainer objection to the revert exists in the mirror.

**Posting 2 — a different fix** (`1c36287c5eec`, 2026-09-23, same author, Cc
König / Deucher / Priyak Liang): does not revert. It adds a re-reservation in
`amdgpu_userq_vm_validate_and_restore_queue()` after the validation walk:

```c
	/* Re-reserve the rearm slot after validation may have rebuilt the lists. */
	drm_exec_for_each_locked_object(&exec, tmp_key, obj) {
		ret = dma_resv_reserve_fences(obj->resv, 1);
		if (ret)
			goto unlock_all;
	}
```

**Not adopted, and deliberately not decided here.** It carries no
`Reviewed-by`, it is one day old, and it sits in the middle of a dispute whose
other side wants our carries gone. It may well be complementary rather than
alternative — the comment says validation can *rebuild the lists*, which our
up-front reservation does not cover — but "may well be" is not the bar. If the
revert is dropped and this gains review, it becomes a normal candidate; if the
revert lands, this patch's context changes with it.

**Watch item:** re-read this thread at the next sweep. The state to look for is
König's reply to `1c36287c5eec`.

### Other reverts checked, no action

- `Revert "drm/amd/display: Fix CalculateFlipSchedule Calculation"` and
  `Revert "… Unify CalculateFlipSchedule Logic"` (both 2026-08-28) — **we carry
  neither side**, so there is nothing to un-carry. Note them because
  CalculateFlipSchedule is flip-path code and this machine has flip history.
- `Revert "request DMUB HW cursor offload"` (the nested case) — already
  assessed: DCN42-only and the reverted commit is not carried.
- `Revert "drm/amd/pm: defer UCLK DPM enablement on Apple Navi 14"` — Apple.
- `Revert "drm/amdgpu: debugfs: avoid extra EOLs in amdgpu_gem_info"` — cosmetic.

## Work-items pass, 2026-09-24 — one lead to **measure**, not to patch

The tracker yielded no adoptable patch this time: the one issue that had a
usable fix, **#5663** (`bisected`), is the SDMA DCC regression we already took
as **`1074`** — the issue still lists `3a6f6eeb3db5` as the culprit, which is
exactly the `Fixes:` in that patch.

### `#5418` — 5 s vblank off-delay, idle power

`drm/amd/display: Restore 5s vbl offdelay for NV3x+ DGPUs`
(`a1fc7bf6677e`, 2026-04-22, `Reviewed-by: Mario Limonciello`) **is in our
base** and **applies to this GPU**: it triggers for a DGPU whose `DCE_HWIP`
is `>= IP_VERSION(3, 2, 0)`, and Navi 48 is a DGPU at DCN 4.0.1. The commit is
an explicit workaround — *"Rapid vblank off is causing flip-done timeouts for
NV3x and newer ... A proper fix requires further investigation. In lieu of it,
let's workaround it for now."*

`#5418` reports the cost of that workaround on a 7900 XTX: the 5 s timer keeps
the vblank path from quiescing at idle, so `dm_handle_vmin_vmax_update` is
queued at refresh cadence (~5 % of one core at 180 Hz, +10 W, and the IRQ core
never reaches a low power state).

**Not reverted, deliberately.** This machine has a documented flip-timeout
history, and the workaround exists precisely to suppress flip-done timeouts on
this GPU family. Trading a known display-stability workaround for idle power,
on a hunch, is not a trade this repo makes. Also note the reporter's chip is
Navi 31 — the *code* is NV3x+, but the symptom has not been reproduced on
Navi 48 by anyone.

**Measure before believing it applies here**, and do it on an idle machine
with no build running:

```bash
# is the IRQ core busy at idle?
grep amdgpu /proc/interrupts; sleep 10; grep amdgpu /proc/interrupts
# is the vmin/vmax worker firing?
sudo bpftrace -e 'kprobe:dm_handle_vmin_vmax_update { @ = count(); }'
# and the power side
sudo turbostat --quiet --show PkgWatt,Busy%,Bzy_MHz sleep 10
```

If `dm_handle_vmin_vmax_update` is firing at refresh cadence here, that is a
real finding worth a ledger entry of its own — but the answer is a targeted
fix or an AMD follow-up, not a revert of `a1fc7bf6677e` on its own.

### Other on-target issues with no adoptable fix

- **`#5883`** RX 9060 XT (Navi 44 — same GC 12.0 / DCN 4.0.1 family): black
  4K DP output after S3, `drm_crtc_vblank_get()` returning `-EINVAL` in
  `amdgpu_dm_atomic_commit_tail` (`amdgpu_dm.c:10211`). Open, no fix posted,
  and the topology (DP 4K160 + S3) is not this machine's (HDMI 1080p240).
- **`#5716`** NULL deref in `dal_ddc_open` on DP HPD — labelled *Strix /
  Kraken*, and **already guarded here by our `1161`**.
- **`#5418`/`#4707`/`#5754`/`#5840`** are labelled 6000/7000/5000 series
  (RDNA 2/3): `pp_dpm_mclk` stuck under FreeSync, KWin page-fault + ring
  timeout, Samsung-TV HDMI link retrain loop. Different silicon.

## Mailing-list and merged-tree sweep, 2026-09-24 (the "everything in linux-next" pass)

Two method notes first, because both cost time and produced **false clean
results** that looked like real answers.

### `v7.3-rc4` is not a tag in the AMD trees

`git -C repos/agd5f-linux log v7.3-rc4..origin/amd-staging-drm-next` printed
nothing — and prints nothing when the tag does not resolve, with the `2>/dev/null`
hiding `fatal: bad revision`. Every "0 commits since rc4" reading for
`agd5f-linux`, `amd-staging-drm-next`, `drm-next`, `linux-pm` and `akpm-mm` was
an **empty range, not an empty diff**. Those clones are `--shallow-since`, so
the rc4 *commit object* is absent too and cannot be substituted. Use a date
window (`--since=`) on a shallow tree, or verify the ref first:

```bash
git -C repos/<tree> rev-parse -q --verify v7.3-rc4^{commit} || echo TAG-MISSING
```

### The lore mirrors are bare repos

`repos/lore-*` have no `.git` — the repo *is* the directory. `git -C repos/lore-amdgfx`
fails; use `git --git-dir=repos/lore-amdgfx`. And `git show <sha>` on a mirror
**diffs the mail file**, so the payload must be recovered by replaying the
hunks (context `+` added lines), not by taking `+` lines alone — the latter
drops every context line and yields a malformed patch. Two further traps hit
here: a folded `Subject:` needs unfolding (a naïve `^Subject:` regex truncates
it mid-sentence), and splitting a multi-file diff on `'\ndiff --git '` consumes
the final newline, which `git apply` reports as *"corrupt patch at line N+1"*.
`patch` accepted that file with fuzz; `git apply` did not. **Run both.**

### The tracker's notes endpoint is now authenticated

`/projects/drm%2Famd/issues/<n>/notes`, `/discussions` and `/links` return
`401 Unauthorized` to an unauthenticated client; `/issues`, `/participants`,
`/related_merge_requests` and `/closed_by` still return 200. Issue **comments
are no longer readable without a token** — earlier sweeps' 1642-comment pass
cannot be repeated as written. The issue *descriptions* are still served.

### `tip` — 304 commits since rc4, all 7.4-queued

Twelve looked on-target; **all twelve are already in `next-20260924`**, so they
are next-merge-window material, not 7.3 fixes. Not adopted. The nearest misses:

- `a0bb6fac53fa` sched/core PSI IRQ-time accounting (`Fixes:` tag) — relevant
  in principle, we do use PSI, but under scx full-switch the core accounting
  path is not what this machine runs.
- `b8d1d5b63a8e` x86/mce hardware debug-register corruption on task migration.
- The six `sched/cache` commits (`CONFIG_SCHED_CACHE=y` here) include two UAF
  fixes. **Worth revisiting at the bump**: the UAF is in
  `task_struct->sched_cache_grp` teardown, which can fire independently of
  which class schedules the task, so "inert under scx full-switch" may not
  cover those two the way it covers the LLC-placement hunks.
- `228200f695c0` `x86/CPU/AMD: Fix Zen5 TLB sizes` — **Zen5**, not Zen 4.

### `sched-ext` — four candidates, none clearing the bar

We run scx full-switch, so this list matters. Not adopted, and the reason is
provenance rather than applicability: each carries only the author's
`Signed-off-by`, is **not in `next-20260924`**, and has no `Reviewed-by`.

| Mail sha | Subject | Status |
|---|---|---|
| `ab87217cfb` | Count `SCX_EV_SUB_BYPASS_DISPATCH` in the dispatch fallback | author SoB + `Fixes:` only |
| `740162e26b` | Specialize the DSQ hashtable compare | author SoB only |
| `4b47fc7629`/`b8a7215ddc` | Specialize the TID / scheduler hashtable compare | `Suggested-by: Tejun Heo`, no review |
| `ffd987bc41`/`4d960bbde1` | reject DSQ draining / reenqueue (08 and 09 of a 16-part Andrea Righi series) | not reviewed; adopting two parts of sixteen out of order is its own risk |

Already carried from the same list: `2416` (CPU-hotplug hang), `2417` (DSQ
relock on remote moves), `2418` (dsq_vtime placement).

### `linux-pm` — both amd-pstate candidates already carried

`cpufreq: amd-pstate: Propagate cppc_set_auto_sel() errors on mode change` is
**`1232`**. The `TOCTOU when changing driver mode via sysfs` posting is the
documented false candidate: **`1227` already takes the lock before reading
`mode_state_machine[][]`**, which is the fix. Neither adopted; both recorded so
the next sweep does not re-open them. The `ACPI: CPPC: Resource Priority
Register` series (10+ parts) is new but is a feature for platforms exposing
those `_CPC` entries, not a fix.

### `netdev` — wrong chip

`RTL8261C/D` PHY work (LEDs, SerDes lane polarity) is a **discrete 10G PHY**;
this machine's NIC is an **RTL8125B** MAC-integrated 2.5GbE driven by `r8169`.
Nothing for `r8169` in the window.

### Still unreachable

`drm-misc` — TTM / dmemcg / dma-buf — returned **HTTP 503** for the whole
session, and `drm-next`'s fetch failed the same way (`RPC failed; HTTP 503`).
That remains the one subsystem this sweep cannot speak to.

## Adopted 2026-09-24 — the DC Patches September 22th batch (255 -> 258)

`[PATCH 00/34] DC Patches September 22th, 2026`, posted to `lore-amdgfx`
2026-09-24 by Fangzhi Zuo. Three taken, one rejected on evidence.

| # | Subject | Mail sha | Review |
|---|---|---|---|
| `1171` | Serialize HDMI FRL status polling against link detect (05/34) | `118d17a1b8` | `Reviewed-by: Harry Wentland` |
| `1172` | Skip HDMI FRL status polling while link is down (11/34) | `24647c058c` | `Reviewed-by: Harry Wentland` |
| `1173` | avoid to write signal specific for tmds (23/34) | `ecd548fd4f` | `Reviewed-by: Michael Strauss` |

### Why these three, and not the other thirty-one

The batch is a DC pull request, so most parts are DCN60 / DCN42 / DCN30 /
DCE 6.x and **cannot run here** — this machine is DCN 4.0.1. The three taken
all sit on paths this machine actually executes:

- **`1171`/`1172` are one change in two steps**, both in
  `hdmi_frl_status_polling_work()` — the HPD-driven FRL status poll. `1171`
  takes `dm->dc_lock` with `mutex_trylock()` around the *whole* link walk
  instead of only around `dc_link_detect()`, so polling can no longer race a
  link detect after an unplug/replug; `1172` then skips links whose
  `link_status.link_active` is false. The mail states the failure plainly:
  *"Hotplugging an HDMI FRL sink can wedge DMCUB when a poll-driven retrain
  lands on a link whose PHY has just been torn down ... the sink SCDC reads
  back version 0 and the display fails to light up."* This machine drives the
  MSI MAG251RX over HDMI **on FRL** (boot log: `DP-HDMI FRL PCON supported`),
  so both the race and the wedge are reachable here.
- **`1173`** adds an `is_frl` argument to `write_scdc_data()` and passes
  `dc_is_hdmi_frl_signal()` from `enable_link_hdmi()` and
  `link_set_dpms_off()`, so a TMDS mode change stops writing signal-specific
  SCDC state. *"some panel will generate HPD if receive invalid the action"* —
  a spurious HPD on a TMDS transition. Both call sites are on this machine's
  HDMI enable/disable path.

`1172`'s mail also carries a hunk against
`display/amdgpu_dm/tests/amdgpu_dm_connector_test.c` that does **not** apply:
the test additions it edits arrived in the *September 16th* batch, which is
not carried. Its test hunk was stripped; the diffstat line is absent
accordingly. The code hunk applies with no fuzz and was verified in series
order after `1171`.

### Rejected: `24/34` — "Fix HDMI2.2 LT timeout duration" (`b59580b90b`)

This one is the reason the batch needed reading rather than skimming. It
rewrites the polling loop in `hdmi_frl_perform_link_training()` — the *same
function* as our carried `1136` + `1168` — replacing poll counting with
wall-clock timeouts. It applies cleanly to the series tree. **It is rejected
because adopting it would undo `1168` at exactly the rate class this machine
uses.**

`24/34` sets `poll_timeout_ns = 200 ms`, then raises it to 300 ms only
`if (link_settings->frl_link_rate >= HDMI_FRL_LINK_RATE_16GBPS)`. The ledger
entry for `1168` records that this machine's MAG251RX link is **FRL6, below
the 16 Gbps threshold**, which is precisely why `1168` makes the 300 ms
budget unconditional. Under `24/34` that link would get **200 ms** — *less*
than the 105-poll (~210 ms) budget it had before `1136`, and well under the
~310 ms `1168` gives it. The rewrite may be the better structure, but as
posted it is a regression here.

**Revisit together with `1136`/`1168` at the 7.4 bump**, where a rebase is
required anyway: at that point either AMD widens the budget at every rate, or
the local delta is re-applied on top of their rewrite. Do not cherry-pick
`24/34` alone.

### Rejected: `6f742bc837f1` — "Restore FreeSync VCP code check for HDMI/PCON sinks"

Same batch, older posting (`2026-09-09`, `Reviewed-by: Roman Li`, `Reviewed-by:
Alex Hung`, `Tested-by: Dan Wheeler`). Its `Fixes:` names *"Consult MCCS
FreeSync cap only if requested & supported"* — **the exact commit our `1164`
reverts.** That makes it look like an obvious swap. It is not, and the
difference is the whole reason `1163`/`1164` exist.

Upstream's restored check is:

```c
if ((sink->sink_signal == SIGNAL_TYPE_HDMI_TYPE_A ||
     as_type == FREESYNC_TYPE_PCON_IN_WHITELIST) &&
    !sink->edid_caps.freesync_vcp_code)
	freesync_capable = false;
```

Our applied tree (`amdgpu_dm_connector.c:3965`) instead has:

```c
if ((sink->sink_signal == SIGNAL_TYPE_HDMI_TYPE_A ||
     as_type == FREESYNC_TYPE_PCON_IN_WHITELIST) &&
    !connector->display_info.hdmi.vrr_cap.supported &&
    (!sink->edid_caps.freesync_vcp_code ||
     (sink->edid_caps.freesync_vcp_code && !sink->mccs_caps.freesync_supported)))
	freesync_capable = false;
```

Two differences, both decisive:

1. **`6f742bc837f1` covers only the `!freesync_vcp_code` half.** Our
   unconditional clear already handles that case *and* the
   `freesync_vcp_code && !mccs_caps.freesync_supported` case — which is the
   one that actually fires on the MAG251RX, an AMD-VSDB sink whose MCCS VCP
   does not answer. So the upstream patch adds nothing for this monitor.
2. **Adopting it would *undo* `1163`.** The new check has no
   `!connector->display_info.hdmi.vrr_cap.supported` guard, so it clears
   `freesync_capable` for HF-VSDB VRR sinks that lack an EDID VCP code —
   the exact population `1163` was written to keep capable, and the reason
   the flicker stopped in rc3-9. Its KUnit change confirms this is
   deliberate upstream: `dm_test_fs_caps_hdmi_vsdb` flips from
   `KUNIT_EXPECT_TRUE` to `KUNIT_EXPECT_FALSE`.

Recorded as a **standing divergence**, not a pending swap: if a future base
drops `1163`, take `6f742bc837f1` and re-verify the MAG251RX with
`/sys/class/drm/card*-HDMI-A-1/vrr_capable`.

### Checked and already carried (no action)

Every on-target commit in agd5f `drm-next` / `amd-staging-drm-next` since
2026-09-08 was reverse-tested **and** identifier-probed against the series
tree, because reverse-apply alone false-positives:

| Commit | Subject | Status |
|---|---|---|
| `aee05c455ad3` | atom: bound the VBIOS getters | carried as **`1072`** (`bios_size` guards at `atom.c` 1423/1491/1498 confirmed) |
| `a2a27745350c` | reserve root PD fence slots for userq eviction-fence rearm | carried |
| `5e6b21bce9d9` | reserve eviction-fence slot at WPTR caller | carried |
| `636139603b99` | hold a runtime PM reference for P2P dma-buf attachments | carried |
| `04de4007d323` | Fix GPU PCIe link capability reporting | carried |
| `bc7f95c8ddb6` | Revert "request DMUB HW cursor offload" | rejected earlier, reason in ledger: DCN42-only, reverted commit not carried |

### Wrong-chip rejections from the same pass

- `f35aa5c77f5f` `pm: bound SCLK FCW range entries` — the stack overflow is in
  `polaris10_get_sclk_range_table()` / `vegam_get_sclk_range_table()`. Both are
  powerplay DPM; this machine runs `smu_v14_0_0`. Never called here.
- `a24db07159cd` gfx12.**1** trap workaround, `b2adbdf861e3` GFX 12.**1**
  `CP_HQD_PQ_CONTROL.SCOPE`, `473b54b63504` DCN42B plane alpha,
  `228200f695c0` **Zen5** TLB sizes — four different versions of "the filename
  or the family looks like ours".

## Adopted 2026-09-24 (late) — two reviewed fixes from the mailing-list pass (253 -> 255)

Both cleared the bar the rest of this session's adoptions cleared: reviewed by
an AMD maintainer, or applied by the subsystem maintainer.

| # | Subject | Review | Why on-target |
|---|---|---|---|
| `1075` | drm/amdgpu: don't leak bo_va when `gem_object_open` fails (Xiang Liu, AMD) | **`Reviewed-by: Felix Kuehling`**, **`Acked-by: Alex Deucher`** | Real leak in `amdgpu_gem.c`: an unchecked `amdgpu_vm_bo_add` plus a missing `amdgpu_vm_bo_del` on the error path. Reachable — `amdgpu_evf_mgr_attach_fence` can fail via `ttm_bo_validate`. Applies clean to rc4 **and in series order** |
| `2418` | sched_ext: Place `dsq_vtime` next to `dsq_priq` (Usama Arif) | **Applied by Tejun Heo to `sched_ext/for-7.4`** | Moves `u64 dsq_vtime` beside `struct rb_node dsq_priq` so rbtree insertion reads both on one cache line. This machine runs scx full-switch, so the DSQ path is hot. Applies clean to rc4 **and in series order**. Changes `struct sched_ext_entity` layout, so out-of-tree scx schedulers built against an older `vmlinux.h` would need a rebuild — CO-RE consumers are unaffected |

### Considered and NOT adopted, with the reason

- **The ATOM parameter-space pair** (`[PATCH v2] fix ATOM parameter space index
  bounds check` and `[PATCH v3] prevent parameter-space underflow in nested ATOM
  table calls`, Aldo Ariel Panzardo). Genuinely interesting: external callers
  pass `sizeof(args)` (bytes) for `params_size`, while `atom.c` uses `ctx->ps_size`
  as an *element* count in `idx < ctx->ps_size` — so the bound really is 4x too
  permissive, and `ps_size / 4` is the correct expression. Two things stop it:

  1. **No review.** Zero `Reviewed-by`/`Acked-by` anywhere in either thread, and
     the author posted v2 and v3 inside one day, so the shape is unsettled.
  2. **An unresolved interaction.** `atom.c` line ~1669 calls
     `amdgpu_atom_execute_table(ctx, ATOM_CMD_INIT, ps, 16)` for a buffer that is
     64 bytes (`memset(ps, 0, 64)` two lines later). Under the patch's own
     bytes model that call should pass `64`, and the patch would shrink its
     window from 16 elements to 4. `ATOM_CMD_INIT` only writes `ps[0]`/`ps[1]`,
     so it likely still works — but "likely still works" is not a review, and
     this is the VBIOS parser every AMD GPU here depends on. **Revisit when it
     gets review or the call site is fixed.**
- **The io_uring `CQE32`/`CQE_MIXED` refill pair** (Hui Peng). Jens Axboe replied
  to the author: *"I did do this work for you and split it into a 7.3 and 7.4
  set. See my branches."* Checked his branches directly — **`io_uring-7.3`'s head
  is `a3bdf68feecc`, which is exactly the commit we carry as `2048`.** So the
  7.3 half is already ours and the refill fix is on `for-7.4/io_uring`:
  **7.4-bound, not for now.**

## `1073` replaced by `1074` — the upstream, reviewed version of the same fix

`1073` was adopted earlier on 2026-09-24 from **drm/amd work item #5663** with
provenance this ledger already flagged as weak: a GitLab handle with no real
name and **no `Signed-off-by`**, and a diff that was space-indented where the
tree uses tabs *and truncated*, so its hunk body had to be rebuilt by hand.

The mailing-list pass found the **proper upstream posting** of the same fix:

| | `1073` (dropped) | `1074` (adopted) |
|---|---|---|
| Origin | GitLab issue note | `[PATCH v2]` on amd-gfx, Message-ID `<20260924140616.2647-1-...>` |
| Author | `pepp` (handle) | **Pierre-Eric Pelloux-Prayer <pierre-eric.pelloux-prayer@amd.com>** |
| Review | none | **`Reviewed-by: Alex Deucher`**, **`Reviewed-by: Christian König`** (both AMD maintainers) |
| Fixes | — | `Fixes: 3a6f6eeb3db5 ("drm/amdgpu: give ttm entities access to all the sdma scheds")` |
| Link | issue note | **the same** issue #5663 |
| Mechanism | per-blit: force `e = 0` for GFX12 DCC blits into VRAM | **device-level:** set `num_move_entities = 1` for `IP_VERSION(7,0,0) || IP_VERSION(7,0,1)` in `amdgpu_ttm_enable_buffer_funcs()` |

The device-level form **subsumes** the per-blit one — with `num_move_entities == 1`
the round-robin `e = atomic_inc_return(...) % num_move_entities` is 0 for every
blit, not only DCC ones. So carrying both would be redundant, and the weaker
one is the one to drop.

Rebased to rc4: the author's change is verbatim; the posting's base differs only
in surrounding context (`rc4` has `kzalloc_objs()` where the posting's base had
`kcalloc()`), an offset of −25 lines. Applies clean to pristine rc4 **and in
series order**.

**`1073`'s number is left vacant rather than reused** — the gap is the record
that something was tried and replaced.

## The 2026-09-24 full-series audit — every patch placed

Ran three independent tests over all **243** carried patches. Result: no patch is
misplaced, none duplicates the base, and 75 are queued upstream.

| Test | Reference | Result |
|---|---|---|
| reverse-apply (already in our base?) | pristine v7.3-rc4 | **0 of 243** — no duplicates |
| reverse-apply (already in mainline?) | `torvalds` origin/master | **1** — `2153` |
| reverse-apply (queued upstream?) | `next-20260923` | **74** |
| on-target silicon | running kernel's IP blocks | **0 foreign-only** |

**On-target: clean.** After removing the 12 foreign-chip patches earlier the same
day, **no carried patch touches only another chip's silicon.** The kernel names
its own blocks — `gfx_v12_0_0 gmc_v12_0_0 sdma_v7_0_0 smu_v14_0_0 psp_v14_0_0
vcn_v5_0_0 ih_v7_0_0 mes_v12_0_0 jpeg_v5_0_0`, plus DCN 4.0.1 and `dce_v1_0_0`
(the last of which is exactly why `1142`/`1143` are live and were kept).

**No duplicates of the base.** Nothing reverse-applies against rc4, so no patch
is inserting a second copy of something the base already has.

### The 7.4 drop list is much larger than recorded — and the old list was right

74 reverse-apply against `next-20260923`. **That test has known false negatives,
and two fired:** `2005` and `2415` do not reverse-apply, yet both are merged.
Confirmed by the authoritative identifier test rather than by reverse-apply —
`pcpu_user` is 0 in rc4 and 1 in linux-next; `scx_kf_allowed_ctx` is 0 in rc4 and
6 in linux-next. So the real figure is **75 queued upstream** (74 + `2005` +
`2415`), of which **`2153` is already in mainline** (via `a52a93358ac`, merged
2026-09-22) and the other 74 are 7.4-bound.

None is removable now: the base is rc4, which lacks all of them.

**A ledger typo found by this audit:** `2414` was recorded as `8848333267b7`;
the real commit is `8848333264b7` (a digit transposition). Corrected.

### Version sweep — one real update

34,759 normalised subjects indexed from 132,801 mails across 13 mirrors, narrowed
to 45 raw hits, then filtered:

| Filter | Removed |
|---|---|
| date / different author | 1 — `1151`'s "v4" is a different patch by a different author, older |
| already merged | 1 — `2415` |
| content-identical | 31 |
| different base | 11 — the kbuild v4 block |

**One survives: `2041` (net: gso: limit recursive IP-in-IP segmentation), v4 →
v6**, posted 2026-09-24. A genuine rework — it replaces v4's
`gso_header_len_exceeded()` headroom test with a per-skb `recursion_counter` in
`SKB_GSO_CB` plus `gso_recursion_inc_test()` and `IP_TUNNEL_RECURSION_LIMIT`.
It applies clean to pristine rc4 **and** to the series tree with `2041` removed,
and `2041` is the only carried patch touching `include/net/gso.h`,
`net/core/gso.c`, `net/ipv4/af_inet.c` or `net/ipv6/ip6_offload.c` — so it is a
safe in-place swap.

**The kbuild v4 block is a bump item, not an update.** Lorenzo Stoakes reposted
the build-speedup series as `[PATCH v4 NN/22]` (we carry v3 `NN/20`); the series
resized and renumbered, 11 parts have real deltas, and part `01/22` does not
apply even to pristine rc4 (it expects `.modinfo : { *(.modinfo) }` where both
our base and mainline carry `.modinfo : { *(.modinfo) . = ALIGN(8); }`). Keep v3.

**Sweep coverage caveat, stated because it bounds the result:** `lore-linux-mm`
is lore epoch `linux-mm/2`, which only reaches back to **2026-09-21**. Higher
epochs return `Not Found`, so `/2` is genuinely newest — but **any mm revision
posted before 2026-09-21 is invisible**, and we carry 51 mm patches.

### Source status

- **`drm-misc`: UNREFRESHED.** gitlab.freedesktop.org returns HTTP 503
  (`expected 'acknowledgments'`) on repeated attempts. Origin sits at
  `8ef59ee79407` against remote `6e375de99d0c`. Negative TTM/dmemcg/dmabuf
  results are weaker than they read.
- **`tip`: queried, current.** Its new on-target content is the `sched/cache`
  series (2026-09-21) — a *feature*, 7.4-bound, and inert under our scx
  full-switch — plus `x86/mm/pat` warn tweaks. The `posix-cpu-timers` fix
  (`c21eaa72f02f`) is already **in rc4**.
- **Work items: 60 issues enumerated** (23 in the tighter 09-22 window).
  On-target items worth tracking: **#5663** confirmed by a reporter on
  **RX 9070 XT (Navi 48, gfx1201)** as fixing artifacts after S3 suspend, with
  the guard verified absent from rc4's `amdgpu_ttm.c`; **#5716**
  (`NULL deref in dal_ddc_open`), where @rockowitz reports the same class takes
  *"AMDGPU … off the PCI bus and freezes Plasma"* on Navi. #5716 links a
  `GPIO-serialization-v4.mbox` uploaded to GitLab — **that upload returns HTTP
  404 and cannot be retrieved**, so it is recorded as referenced-but-unavailable,
  not as a candidate. #5418 has bulk retest requests against `63e19ef3ddab`.

## The 2026-09-24 sweep — the two pending v2s both landed

Base rc4, 243 patches. Window since 2026-09-20.

**Headline: both items recorded as "awaiting upstream v2" now have a v2, and both
have been APPLIED by their maintainers.** Verified by applying them.

| Item | v2 posting | Review | Applied as | Applies to rc4 |
|---|---|---|---|---|
| `blk-mq: set RQF_USE_SCHED when the operation is known` (Keith Busch) | `[PATCHv2 1/2]`, 2026-09-22 | `Reviewed-by: Christoph Hellwig` | `ab6c756f28c7` | clean |
| `blk-mq: allow cached requests to be used for flush operations` (2/2) | same series | `Reviewed-by: Christoph Hellwig` | `9d2c70986bb7` | clean atop 1/2 |
| `io_uring: initialize task context before the BPF loop` (Yao Kai) | `[PATCH v2]`, 2026-09-23 | — | `a3bdf68feecc` | clean |

The kyber pair is **directly on-target** — kyber is this machine's io scheduler,
per `60-ioschedulers.rules`. Its `Fixes: 4b6a5d9cea91` is present in rc4, so the
leaked domain token and stalled queue are live here. The io_uring v2 is
content-identical to v1 (empty changed-line delta) — a resend, not a revision.

**Two extraction traps fired and were caught**, both documented above but worth
recording as instances: the mails are **quoted-printable** (`=3D` for `=`, `=20`
for space, `--=20` for the signature separator), so `git apply` reported
*corrupt patch* while GNU patch reported clean — decode with `quopri` before
extracting. And `cat-file -p <sha>` yields the COMMIT object; the email is the
blob named `m`, so it must be `<sha>:m`.

### New on-target candidates found (triaged, not yet adopted)

| Candidate | Author / date | Why it matters here | State |
|---|---|---|---|
| `sched_ext: Fix CPU hotplug hang when a dying CPU's tasks sit in the BPF scheduler` | Tejun Heo, 09-23 | marked **for-7.3-fixes**, `Cc: stable`; this machine runs scx full-switch (`switch_all=1`, `scx_cake`). Applies clean, 4 files / 10 hunks, not yet upstream | ready |
| `drm/amd/display: Fix compound literal stackframe limit` + `Bump frame warning limit for clang builds of dml` (+ all-builds variant) | 09-23 | our config is exactly `CONFIG_CC_IS_CLANG=y` + `FRAME_WARN=2048`, the case these target | ready |
| `drm/amdgpu/userq: fix reading the WPTR at a non-zero BO offset` | Jesse Zhang, 09-23 | wrong fence seqno, `amdgpu_userq_fence.c` | ready |
| `drm/amdgpu/userq: reserve the VM root BO around CWSR param validation` v2 | James Zhu, 09-21 | fixes `dma_resv_assert_held` on every compute queue create | ready |
| 21-patch gfx12 pipe-reset series (`gfx12: implement detect_hung_queue`, `mes12: gate gfx pipe reset on PER_PIPE`, …) | Jesse Zhang, 09-21 | touches `gfx_v12_0.c` / `mes_v12_0.c`; we carry only the SDMA half (`9072`/`9074`/`9075`) | needs prerequisite check |
| `drm/amdgpu: reserve fence slot before userq eviction rearm` | Vitaly Prosyak, 09-23 | same author and function as carried `1066`; the author states it supersedes earlier approaches — **resolve against `1066` before adopting either** | resolve first |
| issue **5663** — `amdgpu_move_blit` picks a non-zero SDMA move entity for `AMDGPU_GEM_CREATE_GFX12_DCC` | GitLab, updated 09-24 | the guard is **absent** from rc4's `amdgpu_ttm.c`; reporter confirmed the fix over 5 suspend cycles on Navi 48 | inline patch, weaker provenance |

### Rejected, with the reason (the reusable part)

- **The whole `mm-unstable` zswap set is already settled.** Every un-carried
  commit in it has a ledger entry above: `e0f869c71622` is inert (its own scope
  is `cgroup.memory=nokmem`, which this machine does not set); the folio
  conversions and `constify` are pure refactors that belong with the pool work;
  the pool-by-id + xarray pair is a 7.4-bump decision. The newest, Ghiti's
  `349d75f4907c` "drop cold writeback folios via swap dropbehind", is a
  self-described workaround **and does not apply**: it needs
  `remove_mapping_set_shadow()`, which has **zero occurrences** in rc4. Its two
  predecessors (`5b0fec7c8786`, `debcef32116f`) do apply, but adopting them
  without the third leaves the mechanism with no user.
- **Already carried, byte-identical:** amdgpu ip-discovery validation (= `9076`),
  `sch_cake` v2 (= `2045`), the secure-userq-lifecycle resend (= `9062`–`9071`),
  Mario's amd-pstate 4-patch (= `1231`/`1232`).
- **"Already carried" trap again:** Mario Limonciello's `amd-pstate: Fix TOCTOU
  when changing driver mode via sysfs` (09-21) is **covered by carried `1227`**,
  which already takes `guard(mutex)(&amd_pstate_driver_lock)` before reading
  `mode_state_machine[][]`. Subject-matching alone would have added a duplicate.
- **Wrong chip**, confirmed by target filename: `gfx v12_1` MGCG/VFI, `GFX12.1`
  RLC clock, `SMUv15.0.8`, `PSP v15.0.3`, `LSDMA v8.0.1`, `HDP v8.0.1`,
  `IH v8.0`, `sdma v7.1`, VPE 3.0.x, `soc v2_0`, MI300, `RTL8127`/`RTL8125D`,
  DCE 6.x/8.1.
- **Inert here:** `tools/sched_ext` sample changes, selftests, `blktests`.
- **Track, do not adopt:** `[PATCH v6 0/13] nvme-pci` dma-buf-backed requests
  (Pavel Begunkov, 09-21) — relevant to the Phison E16 but a large new feature
  under active objection from Hellwig.
- **No reverts of anything we carry** appeared in the window.

### Source status — what was actually queried

Queried and current: `torvalds`, `linux-next` (tag `next-20260923`), `drm-next`,
`agd5f-linux`, `amd-staging-drm-next`, `linux-pm`, `tip`, `akpm-mm`, the ten lore
mirrors, and the `lists.freedesktop.org` amd-gfx / dri-devel archives (HTTP 200).

**UNREFRESHED: `drm-misc`** — gitlab.freedesktop.org returns HTTP 503
(`expected 'acknowledgments'`); origin sits at `8ef59ee79407` against remote
`6e375de99d0c`. Any negative result for TTM/dmemcg/dmabuf this sweep is weaker
than it reads.

**Two stale-mirror traps fired**, both while `fetch` exited 0: `torvalds`'s local
`master` and `lore-linux-mm`'s `master` (810 mails behind). Both were caught by
comparing against `git ls-remote` rather than trusting the fetch — and this is
why every scan keyed on `origin/<branch>`.

The AMD trees are quiet: `drm-next`'s tip since 09-17 is only a `v7.3-rc4`
backmerge, and `agd5f-linux`'s newest is a `gfx12.1` commit (not our chip). The
activity is in `akpm-mm` (zswap) and the lists.

## The 2026-09-22 Discord OOM — MARIE's thrash watchdog, not memory exhaustion

`electron` (PID 2606) was killed at `Sep 22 21:14:27` on boot 0 (rc4-6, so
`2199` was already in). The kill did **not** come from the kernel's OOM path
and not from systemd-oomd:

```
thrash livelock: net-progress 131141 refault / 192089 steal, free 175450, invoking OOM
Workqueue: events thrash_wd_fn
 out_of_memory+0x26b/0x340
 thrash_wd_fn+0x4c8/0x600
```

`thrash_wd_fn` is MARIE-only (0 hits in `v7.3-rc4`, 3 in our `2101`). MARIE's
livelock watchdog *chose* to invoke the OOM killer.

**Its premise was false.** The watchdog fires when, in its own words, "the
working set provably does not fit in RAM". At the fire moment:

| At OOM | |
|---|---|
| Free swap | 27,235,488 kB of 32,432,124 kB — **84% free** |
| `inactive_file` | 21,599,852 kB, of which dirty only 3,468 kB |
| `inactive_anon` | 6,069,172 kB — resident, never swapped |
| `free` | 175,450 pages = 685 MB |

The escape gate is `free > high`; the zone highs sum to 219,589 pages
(857 MB), so 685 MB < 857 MB → the gate never trips, the watchdog stays armed,
scores `w = 1` per 2s window (`dr < ds`, so no `+2`; `free > min`, so no `+1`),
and fires at 8 windows = **16 seconds**.

Reclaim was running **file-dominant**, backwards from intent:

- `pgsteal_file` **31,181,709** vs `pgsteal_anon` **8,779,224** → 3.55× file
- `workingset_refault_file` 6,809,943 ≈ `workingset_refault_anon` 6,741,786

**Cause: `low_swappiness_mode=1`.** MARIE's own docs in `2101` state it:

> *"Marie clamps its effective swappiness to at most 1 in-kernel by default via
> `low_swappiness_mode` … so the higher values udev rules, tuning daemons, or
> distro defaults install in `vm.swappiness` are **ignored** by the reclaim
> pick driver."*

`vm.swappiness = 180` has therefore never been in effect on this machine. The
~6 GB anon working set is never moved into 27 GB of idle swap, MARIE grinds
file cache instead, the refault ratio stays ≥1:2 for 16s, and its own watchdog
kills the biggest process. `low_swappiness_mode_store()` calls
`lru_marie_swappiness_changed()`, so it is a live, reversible knob.

**Not xswap, and not swappiness-as-a-value.** swappiness is only the lever an
operator would use — MARIE overrides it. And zswap was **not** full:
`NR_ZSPAGES` 497,747 pages against a `max_pool_percent = 20` cap of 1,655,956
pages (20% of 8,279,784) = **30.1%**, so `zswap_check_limits()` was returning
false. `pswpout`/`pswpin` are both **0** for the whole boot because MARIE's
`kcompressd` writes through its own path.

> **CORRECTION (2026-09-23).** The conclusion above — that the clamp is the
> fault and clearing it is the fix — **was wrong**, and the analysis is
> preserved as written at the time for exactly that reason.
> `low_swappiness_mode = 1` is MARIE's correct default for this workload.
> Clearing it made MARIE reclaim anon almost exclusively against a ~2.3 GB
> live desktop working set, producing 201M anon steals and 192M anon refaults
> and driving PSI `memory full` to 16%. The watchdog described above was not a
> false positive: it was correctly detecting the livelock the clamp change
> created. Clamp restored 2026-09-23; `vm.swappiness` is now 1 to match. See
> `../swap-stack/README.md` and `LESSONS.md`, "CORRECTION: the watchdog was
> right".

## `[RFC PATCH 00/17] mm, swap: xswap writeback to a physical backend` (2026-09-20)

Baoquan He, `lore-linux-mm`, no replies as of 2026-09-22. The base series
(`[PATCH v3 00/14] extendable swap devices`) is what we carry — `2155`–`2168`
are v3, already current; there is no v4.

**What it adds.** A physical backend for xswap slots: when zswap refuses a
page, take a slot on the real swap device with the highest priority and write
it there rather than bouncing the folio back to the LRU. Plus THP swapin for
xswap entries, contiguous backing runs for large folios, xswap swapoff,
reclaim of slots backing cache-only entries, and charging changes (charge only
once an entry gets physical backing).

**Would it have prevented the OOM? No.** Patch `06/17` triggers on "zswap
refused this page", and zswap was at 30% of its cap (see above). Its commit
message describes a real livelock — *"reclaim keeps picking the same page and
the pool keeps refusing it"* — but that is not the livelock we hit. The
remaining refusal path, `reject_alloc_fail` / `reject_compress_poor`
(zsmalloc failing to allocate), is a *symptom* of pressure rather than a
cause, and `/sys/kernel/debug/zswap` is absent on this kernel
(`zswap_debugfs_init` compiles to a no-op), so those counters could not be
read to fully exclude a contribution late in the storm.

**Would it help after the MARIE fix? Yes, materially.** Today the pool never
fills, so the fallback is never exercised. Clear `low_swappiness_mode` and
anon starts flowing into xswap and the pool climbs toward its cap; at that
point base v3 (what we carry) bounces refused pages to the LRU — *exactly* the
livelock `06/17` describes. Raising `max_pool_percent` buys the same headroom
more cheaply in the meantime.

**Two blockers before it is carryable:**

1. **It is an RFC.** Zero replies. The author: *"Since the charging of xswap is
   still under discussion, I didn't merge them into commits. Will squash them
   or take them off once decision is made"* — `13/17`–`17/17` are explicitly
   provisional.
2. **It needs a real swap device.** The fallback writes to "the real swap
   device with the highest priority"; this machine has none (only `xswap0`).
   Adopting it means adding a swapfile or partition first.

**7.4 hazard — `2199` collides semantically.** RFC `06/17` *replaces* the
`SWP_XSWAP` guard inside `swap_writeout()`; our `2199` mirrors that same guard
into `do_swapout()` (MARIE's path). Different functions, so no textual
conflict, but once the RFC lands `2199`'s "keep the folio" becomes the **wrong**
behaviour on MARIE's path — it must become the same backend fallback, not the
guard. The RFC is also written against the `__swap_writepage()` →
`__swap_writeout()` rename, i.e. 7.4-era, so it cannot be carried on rc4 as-is.

## REMOVED 2026-09-22: the xswap series (`2155`–`2168`, `2199`) — 15 patches

This machine moved its swap device from xswap to zram, with explicit user
approval to remove patches that are verified no longer needed. Series 275 → 260.

**Removed:** `2155`–`2168` contiguous, plus `2199`.

**Deliberately NOT removed:** `2173`, `2174`, `2177`, `2190`–`2193`. Those are
*upstream zswap* fixes, not xswap patches. They are dormant while zswap is off
but `CONFIG_ZSWAP` has to stay compiled because LRU-MARIE calls
`zswap_store()` and `zswap_is_enabled()`. They are a separate question from
this one and were not part of the approval.

### The five verification passes

1. **MARIE is independent of xswap.** `rg -c 'SWP_XSWAP|xswap'` against `2101`
   returns **0**. MARIE neither defines nor consumes any xswap symbol.
2. **`2199` is xswap-conditional and its bug is xswap-specific.** Its guard is
   `else if (unlikely(...->flags & SWP_XSWAP))`, and the NULL deref it fixes
   was caused by xswap's creation path: `/sys/kernel/mm/xswap/create` never
   runs `setup_swap_extents()`, so `sio_pool` stays NULL and
   `swap_add_folio()`'s `mempool_alloc(sio_pool, ...)` dereferences it. zram
   goes through `swapon()`, so `sio_pool` **is** allocated and the bug cannot
   occur. `2199` exists only because of xswap, and goes with it.
3. **Nothing else in the tree references xswap.** `rg -l 'SWP_XSWAP|CONFIG_XSWAP|xswap' sleepy-next/` outside the 15 names only `PKGBUILD` (the
   `source=()` entries), `config` (the `CONFIG_XSWAP=y` line) and docs — all
   edited in the same change.
4. **No non-series patch in `2100`–`2199` mentions xswap.** Scanned every file
   in the range excluding the 15; zero hits.
5. **Cumulative audit after removal: `OK: all 260 patches applied cleanly to
   v7.3-rc4.`** This is the one that actually proves it — a patch left behind
   that depended on `2157`'s cluster-info refactor, for instance, would have
   failed here. It did not.

Plus the build, which is the sixth check in practice.

### Why they were removed rather than left dormant

They were not merely unused, they were the implementation of the device being
abandoned, and the series had three properties this repo actively fights:
a capacity `/proc/swaps` advertises that the device cannot hold (the real
ceiling was zswap's `max_pool_percent` — 6.4 GB against a claimed 32 GB); a
deliberate block on its own drain (`2155` inserts `-EINVAL` for `SWP_XSWAP`
into `zswap_writeback_entry()`, and gates the shrinker on
`nr_real_swapfiles`, which is zero with no real swap device); and an extra
15-patch rebase surface at every version bump.

### What replaces it

`CONFIG_ZSWAP_DEFAULT_ON` is now off and `swap-stack/` carries the zram
configuration. `CONFIG_XSWAP` is gone from `config`. If the swap backend is
ever revisited, the v3 base series is `[PATCH v3 00/14] mm, swap: extendable
swap devices`, and the writeback RFC above is what would make a tiered
xswap-to-disk setup work — neither is carried now.

**Reversing this is one command** if it was the wrong call:
`git revert` the removing commit restores all 15 files and the `source=()`
entries, and `CONFIG_XSWAP=y` is a one-line re-add.

## Sweep 2026-09-22 (later) — zswap optimisation sweep

Run after the switch to zswap + swapfile, over `lore-linux-mm`, `lore-mirror`,
`torvalds`, `linux-next` and `akpm-mm`. Everything touching `mm/zswap.c` now
touches code this machine actually runs, so the filter is different from the
xswap era.

### Already carried (verified present, not re-added)

`2173` publish initial pool with `list_add_rcu`, `2174` `zswap_ever_enabled`
in `zswap_pool_create`, `2177` large-folio swapin not in zswap, `2190` release
retired pools via `queue_rcu_work`, `2191` `zswap_invalidate` takes a range,
`2192` skip the xarray walk when unused, `2193` reuse `zswap_invalidate` in
`zswap_store`. All seven match `cabbf6b3a4f5`, `8cbdd90a659a`, `220d8dddd52c`,
`3d41ebf7fb75`, `0bdbe1ccedd9`, `50eb352dcd30`, `81a798cf85e9` in
`linux-next`/`akpm-mm`. Plus the zstd-side work: `2130` BMI2 probe, `2148`/
`2149` crypto zstd stream init.

### Adopted — `2196`

`mm: zswap: return -ENOENT when the swap device is gone`, Baoquan He,
2026-09-13, `<20260913063031.1689420-1-hebaoquan@kylinos.cn>`, `Acked-by: Nhat
Pham`, in `akpm-mm` as `b1cfb5ba373f`.

`zswap_writeback_entry()` returned `-EEXIST` when `get_swap_device()` found no
device — but `-EEXIST` is the shrinker's *"page already in swap cache"*
signal, which makes `zswap_shrinker_scan()` **stop shrinking entirely**. A
missing device instead means it is being swapped off, so the entry is merely
stale. Returning `-ENOENT` lets the scan skip it and continue.

On-target because the shrinker *is* this machine's drain path now, and because
the trigger — a swap device going away while zswap holds entries for it — is
exactly what happens on a swapoff, which this machine has just done by hand.
The original submission uses `if (!si)`, matching rc4 verbatim (`git apply
--check` and `patch -p1 --dry-run -F2` both pass on pristine `v7.3-rc4` with
no fuzz); the queued `akpm-mm` form differs only in carrying an earlier
`IS_ERR_OR_NULL()` conversion from that series, so the original was used.

Provenance worth recording: the commit message says *"This is taken from xswap
patchset. Nhat suggested this is a fix, should be sent out independently."*
It is the one part of the xswap work that survives as a standalone zswap fix —
which is why removing the series did not lose it.

Numbered `2196`, not `2199`: `2199` is now a **vacated** number from this
change, and a gap is the evidence that something was tried.

### Evaluated and REJECTED

| Candidate | Why not |
|---|---|
| `mm: zswap: mark the zswap shrinker SHRINKER_NONSLAB` (`e0f869c71622`) | **Inert here.** The commit's own scope is `cgroup.memory=nokmem`: without it the shrinker keeps its memcg awareness and is never demoted to slab. This machine sets no `cgroup.memory=`, so the bug cannot fire. Correct and cheap, but it would do nothing — the trap this repo keeps re-learning |
| `mm: zswap: drop cold writeback folios via swap dropbehind` (`349d75f4907c`) | One day old and self-describing as a **workaround**: it clears `PG_active` by hand so `bad_page()` does not trip under `CONFIG_DEBUG_VM`, with the comment *"That is a workaround: the refault should not be evaluated on a writeback buffer at all. A fix for that is on the mailing list."* Re-visit once that fix lands |
| `mm/zswap: reference the pool by id to shrink struct zswap_entry` (`98955a1ebf14`) + `mm/zswap: replace the zswap_pools list with an allocating xarray` (`487b92ae1f10`) | Real optimisation (56→48 byte entry, ~2 MiB metadata per GiB held) but the xarray patch is a **122-line replacement of the `zswap_pools` list** — the exact structure our `2173` and `2190` operate on. Adopting means dropping and reworking both, for a ~14% metadata saving. A 7.4-bump decision, not a mid-cycle one |
| `mm/zswap: use folio_swap_entry() in zswap_store_page()` (`cb0b6eaa6df1`), `mm/zswap: convert zswap_store_page()/zswap_compress() to take a folio` (`3b50b6850f92`), `mm: memcontrol: constify the zswap and socket pressure helpers` (`7e2d0e0a4761`) | Pure refactors/cleanups with no functional or measurable benefit. The folio conversions are prerequisites for the pool work above and should come with it |
| `mm/zswap: flush dcache in the compressed decompression path` | Cache-coherency for non-coherent DMA. x86-64 is coherent; nothing to flush |
| `selftests/cgroup: *zswap*` (`8c7fdc0b4`, `abfacab3e2a5`) | Test-only, and the test tree is not built here |
| `mm: swap: move LRU insertion out of the swap cache allocator` (`5b0fec7c8786`) | Broad swap-core change that exists to support the dropbehind work above; take it with that, if ever |

### Correction owed from this sweep

An earlier entry in this ledger stated that `/sys/kernel/debug/zswap` is
"absent on this kernel (`zswap_debugfs_init` compiles to a no-op)". **That is
wrong.** The directory exists; the check behind that claim was
`if [ -d /sys/kernel/debug/zswap ]`, which fails with `EACCES` for an
unprivileged user and so reports "absent" for a directory that is merely
mode-restricted. It reads fine under `sudo`:

```
pool_limit_hit 0   pool_total_size 0   stored_pages 0
reject_reclaim_fail 720488   written_back_pages 0
```

Same failure shape as `ls ... | head` masking an error — a probe that cannot
distinguish "missing" from "denied" is not a probe.

### Second correction, and a method fix: probe the code, not the commit message

Hao Jia's two-patch zswap shrinker series — `mm/zswap: fix global shrinker
when memory cgroup is disabled` and `mm/zswap: support batch writeback in
shrink_memcg()` — looked like strong candidates. The batch patch's message
describes a failure mode that maps directly onto this machine's new
architecture:

> "shrink_memcg() writes back at most one entry per-node during its traversal
> ... **Under high memory pressure, this can cause the writeback speed to be
> too slow to keep up with refaults, leading to zswap store failures and
> forcing pages to skip zswap and go directly to disk, which results in an LRU
> inversion.**"

A content probe appeared to confirm they were missing:
`rg -c 'shrink_memcg_batch|batch writeback'` against rc4 returned **0**.

**Both are already in `v7.3-rc4`.** Reading the functions settled it:
`shrink_memcg()` already carries `unsigned long nr_to_walk = SWAP_CLUSTER_MAX`
with the patch's own `/* Nothing was scanned: every LRU under @memcg was
empty. */` comment, and `shrink_worker()` already carries the patch-1 comment
verbatim plus `if (!memcg && !mem_cgroup_disabled())`. The whole v4 series
landed before rc4.

**The probe was searching for the wrong thing.** `batch writeback` is phrasing
from the commit *message*; it appears nowhere in the resulting code. A
content probe has to grep for an identifier or a line the patch **introduces**,
not a phrase that describes it. Combined with the `/sys/kernel/debug/zswap`
correction above, this sweep produced two false "absent" verdicts from probes
that could not fail informatively — the same shape as the
`repos/_audit`-missing incident, in a third costume.

**Residual candidates, all resolved:** `dropbehind` (v6 now, still
self-described as a workaround pending a proper refault fix — re-visit when
that lands), `SHRINKER_NONSLAB` (inert, `nokmem` only), the pool xarray rework
(deferred to 7.4, conflicts with `2173`/`2190`), and `-ENOENT` (adopted as
`2196`).

### Web-sweep findings worth carrying (2026-09-22)

Sources: kernel.org docs and source, Arch Wiki, Fedora/Ubuntu/CachyOS configs,
LKML archives, and Chris Down's "Debunking zswap and zram myths" (2026-03-24).

**A bug in exactly this configuration, unfixed.** Alexandre Ghiti's
`[PATCH v3/v4 0/3] mm: fix workingset refaults in the zswap writeback path`
(v4 2026-09-11) targets anon refault accounting in the zswap writeback path:
the shrinker's buffer folio is counted as a refault, and adding it to the swap
cache overwrites the slot's eviction cookie. Measured on sysbench with
**shrinker on and NVMe swap** — this machine's configuration exactly —
`workingset_refault_anon` −48% with comparable writeback volume. Unmerged;
track for the 7.4 window. It is an *accounting* bug (inflated counters driving
reclaim decisions), not a throughput one.

**mTHP swap-in is likely disabled while zswap is on.** `alloc_swap_folio()`
falls back to order-0 in the anonymous synchronous swap-in path whenever
`zswap_never_enabled()` — the range can mix zswap and non-zswap entries.
Fujunjie's `[RFC PATCH 0/5] mm: support zswap-backed anonymous large folio
swapin` (2026-05) addresses it; pending. A quiet cost of enabling zswap, worth
knowing given this series also carries mTHP/gup batching work.

**No knob writes back early.** `accept_threshold_percent` is *hysteresis only*
— `zswap_check_limits()` latches a full flag at `max_pool_percent` and
unlatches it below the threshold. It cannot start draining earlier. The
mechanism that drains early is the **dynamic shrinker**, which is exactly what
`CONFIG_ZSWAP_SHRINKER_DEFAULT_ON=y` gives us, and it is confirmed working
here: `written_back_pages` reached 91,874 with `pool_limit_hit` still 0.

**`same_filled_pages_enabled` no longer exists** (removed 2024 by Yosry Ahmed,
`c074e1467f85`). The full module-parameter set is: `enabled`, `compressor`,
`max_pool_percent`, `accept_threshold_percent`, `shrinker_enabled`. `zpool`,
`z3fold` and `zbud` are gone from upstream too. Do not tune knobs that are not
there.

**No primary sizing rule relates `max_pool_percent` to swapfile size.** Kernel
docs contain no guidance at all. The honest arithmetic for this box: 32 GB RAM
+ 16 GiB swapfile + ~19 GB of anon held compressed in the 6.4 GB pool. The
swapfile is the binding constraint, not the pool.

**Down's article is unambiguous and it is *for* this configuration**:
*"If you are in doubt, I strongly recommend you use zswap with disk-backed
swap."* and *"Do not run zram alongside disk swap wherever possible."* He gives
no `page-cluster`, `max_pool_percent`, or swappiness value — anyone citing him
for one is inventing it. The strongest organized dissent is CachyOS, and it is
about *defaults*, not facts: their config is zram-only with no disk swap, which
is self-consistent.

**`vm.page-cluster=0` — evidence is weak, left alone.** It was chosen from the
Arch *zram* page, where it is redundant (the kernel already bypasses readahead
for `SWP_SYNCHRONOUS_IO`). With zswap, readahead *does* apply, so it now has an
effect. One RFC benchmark (kernel build in a small memcg, shrinker **off**)
favours bypassing readahead for pool-resident pages but *keeps* it for
disk-resident ones — so 0 is a blunt version of a nuanced result. CachyOS's own
comment names `1` for physical SSD swap, with no measurement. No published
comparison exists for zswap-over-NVMe on a desktop. Left at 0, documented.

## ADOPTED 2026-09-23: `1168` — HDMI FRL link-training budget to 300 ms at every rate

`drm/amd/display: Allow 300 ms for HDMI FRL link training at every rate`,
David Janice `<djanice1980@gmail.com>`, 2026-09-19,
`lore-amdgfx` blob `f00dff3b`. Found by the 2026-09-23 mail sweep.

**It builds directly on our `1136`.** The patch's diff context *is* 1136's
post-image — its `-` lines are 1136's added lines verbatim, and its base blob
(`7f93009`) matches 1136's post-image sha. So this is not a competing patch;
it is the next step in the same change.

### What it does

`hdmi_frl_perform_link_training()` runs one poll budget for LTS:3 that starts
at the FRL_Rate write and is **not restarted** when the sink raises its first
`FLT_update` with the LTP request. Our `1136` raised that budget to 155 polls
(~300 ms) only for `frl_link_rate >= HDMI_FRL_LINK_RATE_16GBPS`; every slower
rate kept the 105-poll (~210 ms) default. This patch makes the 300 ms
unconditional.

### Why it is on-target here, not merely applicable

This machine drives the MSI MAG251RX at 1920x1080@240Hz over **HDMI, on FRL**.
1080p240 8bpc is ~14 Gbps, which lands on **FRL6 — below the 16 Gbps
threshold** — so `1136` does *not* currently give this link the larger budget.
The patch therefore changes real behaviour here rather than being a no-op, which
is the test this repo applies to every candidate.

Second reason to take it now rather than later: `1136` is the only thing in the
series holding this timeout, and both patches touch the *same hunk* at
`link_hdmi_frl.c:528`. A future rebase of `1136` would silently lose this if it
were not carried alongside it.

### Verification

- `git apply --check` — exit 0 against a tree with `1136` applied.
- `patch -p1 --forward -F2 --dry-run` — **succeeds with no fuzz**.
- Provenance: named human author, `Signed-off-by`, traceable to a mailing-list
  posting with a Message-ID on `lore-amdgfx`.

### Recorded uncertainty

The reporter's evidence is an **LG C2 at 4K120 on a DP-HDMI FRL PCON** — a
different sink and a different topology from this machine's direct HDMI. **No
FRL link-training failure has been observed in this machine's logs** (the only
FRL line in a boot is `DP-HDMI FRL PCON supported`), so the failure mode being
fixed has not been reproduced here. What justifies carrying it is that it is a
strict widening on the path we use, at a rate class our existing fix misses,
with a downside measured in ~100 ms on a link that is already failing. It is
not carried because a failure was observed.

An extractor trap is worth recording with it: the hunk is 10 old / 18 new lines
and its final context line is the *second* blank-before-`while`, not the first.
Cutting the mail body one line short produced a patch that `patch` accepted
**with fuzz 1** while `git apply` correctly rejected it as corrupt — the exact
"cut at the wrong line, and only one of the two checkers notices" failure mode
already on record here.

## Sweep 2026-09-28 07:03 — 7 AM all-source verification, nothing to adopt

The watcher fired with **no new linux-next snapshot** (`next-20260925` is still
current; there is no `next-20260926` or `next-20260927`), so this ran as the
instructed full verification pass over every source rather than as a linux-next
delta sweep. **No patch was added, dropped or regenerated.**

`torvalds` master is at `72d3fcf802c` = `v7.3-rc5` with no commits beyond it, so
there was no new mainline content to sweep for either. All ten lore mirrors were
refreshed to 2026-09-28 (new mail: amdgfx 13, dri-devel 64, mm 7, sched-ext 2,
block 6, netdev 174, pm 14). There is still **no `[git pull] drm fixes` for
7.3-rc5/rc6** — the rc5 pull we mined on 2026-09-26 remains the latest, so that
highest-yield source had nothing new in it.

Nothing on-target in the refreshed mail: mm was hugetlb (no hugepages on this
desktop), DAX, DAMON and `ptr_eq`; sched-ext was a CID feature; block was a Rust
`DropGuard` and drbd; pm was ARM/embedded. None of those target the hardware in
the table in `CLAUDE.md`.

### Work items — checked including comments

Three on-target items were open (#5900, #4697, #5896). Comments were read via
the GraphQL endpoint (REST `/notes` is still 401-gated). **#5900** gained one
comment on 2026-09-27 from kernelOfTruth — VRR/adaptive-sync and FreeSync
troubleshooting suggestions plus a request for monitor specs. It is user-side
triage advice, **not a patch and not a fix**, so there was nothing to adopt.
Noted because it is at least directionally interesting: the suggestion implies
RDNA4 pageflip timeouts correlate with VRR being enabled, and this machine runs
FreeSync. Nothing actionable follows from it today.

### Version sweep — 11 hits, one genuinely new, and it needs no action

The sweep re-reads every carried patch's subject against all 18,118 upstream
postings across the ten mirrors. It reported **11 higher-version postings**; ten
of those are already dispositioned in this file (`2049`, `2032` adopted; `2185`,
`2037`, `2039`, `2154`, `2151`, `2144` resends with identical content; `2415`
superseded by our own `2414` pair; `1151`'s "v4" is an *older* posting from a
different author).

The eleventh was new: **`2045` sch_cake is now v3 (2026-09-27)**. It is on-target
— CAKE is this machine's SQM via `sleepy-next/net-tune/` on the RTL8125B — so it
was examined properly rather than waved through.

**Verdict: no adoption. The v3 code is byte-identical to the v2 we already
carry.** The v3 is a packaging change only — the single v2 patch split into a
two-patch series so each defect carries its own accurate `Fixes:` tag and stable
backport range (patch 1 `Fixes: c5d34f4583ea`, patch 2 `Fixes: a729b7f0bd5b`,
per Simon Horman and the Sashiko AI review). The split is bookkeeping for stable
backports, which this repo does not do: we build one kernel for one machine and
never backport.

The evidence is the hunk content, not the line count, because a matching diffstat
is exactly the kind of coincidence that has fooled this audit before:

| | our v2 carry | v3 patches 1/2 + 2/2 |
|---|---|---|
| added lines | 11 | 11 — identical set |
| removed lines | 4 | 4 — identical set |
| diffstat | `15 +++++++++++----` | `15 +++++++++++----` |

Every added and removed line matches exactly, including the `int hdr_len;`
declaration, the `skb_transport_header_was_set()` guard, the `hdr_len < 0`
fallback and the `segs <= 1` change (which simply moves from patch 2/2's hunk
into patch 1/2). Splitting our `2045` in two would gain nothing and would churn
the series numbering.

**The adoption bar is not met either**: Horman's two replies of 2026-09-27 are
process feedback — "do include lore.kernel.org links to earlier versions in the
changelog" and "please start a new thread for each version" — with **no
`Reviewed-by`**.

### Rebase and build verification

The rc5 rebase recorded above was re-verified end to end rather than trusted:

- **Cumulative audit**: `audit_series.py --tag v7.3-rc5` reports **all 257
  patches applied cleanly to v7.3-rc5** — no `FAILED`, no `Skipping patch`, no
  `Reversed`.
- **Installed**: `linux-sleepy-next 7.3.0_rc5-1`; the running kernel is still
  `7.3.0-rc4-18-sleepy-next` pending a reboot, which is expected.
- **Boot path**: `/boot/loader/loader.conf` defaults to `linux-sleepy-next.conf`,
  whose `vmlinuz-linux-sleepy-next` and `initramfs-linux-sleepy-next.img` are
  both dated 2026-09-27 23:08 — the rc5 build. The `loader.conf` comment records
  that the file now agrees with the EFI variables, so losing NVRAM no longer
  silently boots the cachyos-rc A/B kernel.
- **BTF**: `.BTF` sections are present in the installed modules, so
  `resolve_btfids` ran and the `TCP_CONG_BBR`/`TCP_CONG_BBR3` kfunc collision
  rule did not fire. `TCP_CONG_BBR` is disabled at `PKGBUILD:732` and again at
  `:807`; the running kernel offers `reno bbr3 cubic` with `bbr3` default and no
  `bbr`, confirming the override takes effect as written.

## ADOPTED 2026-09-28: `2045` regenerated to the sch_cake **v4** revision

This supersedes the v3 verdict recorded in the 07:03 entry above, which found v3
to be a packaging-only split. **v4 is not a repackaging — the code changed**, and
it now meets the adoption bar on review grounds as well.

### What changed from v2/v3

Patch 1 of the series is unchanged (`segs == 1` → `segs <= 1`). Patch 2 is
restructured: the three early `return cake_calc_overhead(q, len, off);` fallback
exits become `goto err;`, with a single label at the end of the function:

```c
err:
	return cake_calc_overhead(q, len, off);
```

Per the cover, this is "per Toke Høiland-Jørgensen review". Patch 1 also gains
`Acked-by: Toke Høiland-Jørgensen <toke@toke.dk>` — the CAKE maintainer. The
adoption bar here is **maintainer review**, which the v2 and v3 did not have.

### Why on-target

CAKE is this machine's SQM: `sleepy-next/net-tune/` runs it on the RTL8125B
path, and both defects (a `segs == 0` shaper stall and an unvalidated transport
header offset) corrupt live shaper accounting rather than being theoretical.

### Form of the carry

Kept as the single patch `2045` with the combined content of v4 1/2 + 2/2. The
upstream split exists so each defect carries its own `Fixes:` tag and stable
backport range; this repo does not backport, so the split buys nothing and would
only churn the numbering. Both `Fixes:` tags are recorded in the commit message.

### Verification

- Built by applying v4 1/2 then 2/2 to a throwaway worktree at **v7.3-rc5**, then
  `git diff` — so the combined patch is generated from the tree, not hand-merged.
- The resulting `cake_overhead()` was read: all three fallbacks route to `err:`,
  and the label sits after the function's real return.
- The new `2045` **reproduces that tree byte-for-byte** (`diff` identical),
  passes `git apply --check`, and passes GNU `patch -p1 --forward -F2 --dry-run`
  with **no fuzz and no `Skipping patch`**.
- Cumulative audit: **all 257 patches apply cleanly to v7.3-rc5**.
- UTF-8 checked byte-wise: the maintainer's name is `H\xc3\xb8iland-J\xc3\xb8rgensen`
  on disk, not a mojibake replacement character. (See the extractor trap below.)

### Extractor trap hit while doing this

`email.message_from_string()` on a **`str`** silently mangles 8-bit content:
`Toke Høiland-Jørgensen` came out as `Toke H�iland-J�rgensen`. Read the
mail as **bytes** and parse with `message_from_bytes()`. The corruption is
invisible in a terminal and would have shipped a wrong name into the ledger.

## Sweep 2026-09-28 (evening) — all sources, one adoption

Every source queried. Everything below is recorded so the rejections are not
re-derived next pass.

### Adopted

`2045` → v4 (above). **Series stays at 257.**

### Rejected, with reasons

| Candidate | Source | Reason |
|---|---|---|
| kbuild build-speedups **v3 → v4** (`2302`, `2308`, `2313`, `2314`, `2315`, `2317`) | lkml | **Does not apply to rc5.** The v4 series is based on `36d4a11b56aa` in the kbuild tree plus three *unmerged* dependency series (module_ver_remove v2, an objtool series, a kees series), which its cover states outright. Both v4 patches tested fail `git apply --check` on `scripts/kallsyms.c` and `include/asm-generic/vmlinux.lds.h`. Our v3 carries remain correct for this base; revisit when the deps merge |
| `r8169: add RSS support for RTL8127` v15 (7 patches) | netdev | **Wrong chip.** Explicitly `RTL_GIGA_MAC_VER_80` (RTL8127, 10G-class). This machine is **RTL8125B, XID 641** (confirmed from dmesg). Also a net-next *feature*, not a fix — 970 insertions |
| `zram: fix short reads from block_state` | block | **zram is not used here.** `lsmod` shows no zram module; the swap stack is zswap + a 16 GiB `/swapfile` |
| `USB: core: sanitize string descriptors against C0 control chars` | sirlucjan fixes v7 | **Problem not present.** Scanned every `/sys/bus/usb/devices/*/{serial,product,manufacturer}` on this machine: **0** attributes contain control characters. The motivating device (ASUS ROG Azoth, `0b05:1a85`) is not attached; ours are a Logitech receiver, HyperX QuadCast S and two dongles. USB core is also not one of this machine's target components |
| `EDAC/amd64: … UMC csrow decode` v2 | lkml | EDAC is not loaded (`lsmod` clean). Patch 2 targets **Family 1Ah** (Zen 5); this CPU is Family 19h |
| `sched/fair: do not scan twice in detach_tasks()` | sirlucjan fixes v7 | **Inert.** `switch_all=1` is set (`/sys/kernel/sched_ext/switch_all`) and `scx_cake` is the active scheduler, so CFS load balancing does not run — the documented `fair.c`-under-scx trap |
| `x86/mm: Don't apply va_align to hugetlb mappings on AMD F15h` | tip | **Wrong silicon.** F15h is Bulldozer; this is Zen 4 (19h) |
| `sched_ext: Add a size argument to scx_bpf_cid_topo()` | tip | **Already in rc5.** Probed rather than assumed: rc5's `kernel/sched/ext/cid.c:927` already declares `size_t out__sz`, with `len = min(out__sz, sizeof(*out))` and the `memset(out, 0xff, out__sz)` fill. tip merely has not rebased |
| sched proxy-execution series (5 commits) | tip | Feature series, not fixes |
| `xswap` vswap infrastructure (12 patches, ~5,500 lines) | sirlucjan | Unmerged feature series, far outside the fix-shaped bar |
| `bore` 7.0.0, `poc` selector | sirlucjan | Alternative CPU schedulers. This machine runs **sched-ext**, so both are no-ops here |
| i915 RC6, `btusb` VID/PID, `iwlwifi`, `sof` Dell XPS, ASUE140D touchpad, `drm/gud` revert | sirlucjan | Off-target hardware (Intel GPU, Bluetooth, Intel wifi, laptop audio, laptop touchpad, USB display) |
| `iommu/amd: PerfOpt compulsory for APUs` | amdgfx | APU-only; this is a desktop with a discrete GPU |
| amdgpu SR-IOV VF series (SRAT/VRAM/VBIOS), `ras: skip RAS TA reload for VFs`, `RLC GPU clock on GFX12.1 VF` | amdgfx | **VF (SR-IOV virtual function) and/or GFX12.1.** This is a bare-metal GFX12.0 part |
| `drm/amdgpu: extend MacBook VRAM-at-0 workaround to VERDE` | dri-devel | Apple hardware and an ancient chip |
| `nvme-rdma`, `nvmet: cgroup_id` | nvme | We are a PCIe NVMe initiator (Phison E16); neither RDMA nor target mode is used |
| KVM `5.15.y` backports, ALSA HDA quirks | lkml | Stable backports for old kernels; laptop audio |
| `mm/zswap: shrinker writeback with iocost` | mm | **RFC** — not mergeable material |

### Recorded but NOT adopted — deferred on the adoption bar

`drm/amdgpu: guard against failed kfd node init` (Yiqing Yao, amdgfx,
2026-09-28). A real NULL-deref guard — `kfd->num_nodes` is set before
`kfd->nodes[]` is populated, so a failed `kgd2kfd_device_init()` leaves NULL
node pointers that `amdgpu_amdkfd_clear_kfd_mapping()` walks. Has
`Signed-off-by` but **no `Reviewed-by`, no `Fixes:`, no `Cc: stable`**, and is
not in `agd5f-linux`, `amd-staging-drm-next` or `drm-next` (the hits those trees
return are a different, August `kfd_dev_mapping` patch). Posted hours ago —
**adoption bar not met; revisit when reviewed**, same treatment as the io_uring
fix deferred on 2026-09-27.

### Work items

Six issues moved. Two on-target: `#5905` (RX 9070 XT fan stops below ~50 °C
hotspot in custom `fan_curve`) and `#5900` (pageflip timeout on a 9070). Comments
read over GraphQL (REST `/notes` still 401-gated). **Neither yields a patch.**
`#5905` has no comments; `#5900` is a user reporting back after disabling
FreeSync, and the one hex-shaped token in it is a bol.com product URL, not a
commit — the known image-path false positive. Others (#5906 Navi31, #5893 Strix
Halo, #5871 HawkPoint1, #5847 HP OmniBook) are wrong-chip.

### Source coverage — two gaps, stated rather than skipped

- **`repos/lore-lkml` and `repos/lore-rust-for-linux` are not usable mirrors.**
  Both are *non-bare single-message* clones (with a stray checked-out `m` and a
  `.git` subdirectory), so `git --git-dir=` fails on them. lkml is nevertheless
  fully covered by **`lore-mirror`**, whose origin is `lore.kernel.org/lkml/20`
  and which is current to 2026-09-28 (1,053 patch mails in the window alone).
  **Rust is genuinely uncovered** — `repos/lore-rust-for-linux` is the broken
  clone and `CONFIG_RUST=y` is set, so this is a real, if low-yield, gap. Worth
  re-cloning: `git clone --mirror https://lore.kernel.org/rust-for-linux/0 repos/lore-rust-for-linux`.
- **`next-20260928` could not be fetched.** The tag exists on the remote
  (`97952267cf37`) but the tree is ~13 GB and the fetch exceeded its budget
  twice. Everything linux-next *aggregates* — tip, drm-next, agd5f, amd-staging,
  drm-misc, linux-pm, akpm-mm — was swept individually, and the mainline base is
  unchanged (`origin/master` = `72d3fcf802c` = v7.3-rc5), so the snapshot has no
  unique content this pass. **Not to be confused with "checked and empty".**

### Freshness trap hit again

`repos/torvalds` **`master` is a stale local branch at 2026-09-21** while
`origin/master` is current at 2026-09-27 (`72d3fcf802c`). Reading `master` would
have reported mainline as far older than it is. Same class as the sirlucjan
stale-local-branch trap: **always read `origin/<branch>`.** The
`sirlucjan-kernel-patches` working tree is likewise at 2026-09-18 while
`origin/master` is at 2026-09-28 — which is why the fixes series reads as **v7**
there and not the v6 visible in the checkout.

### Patch hygiene observation (not acted on)

**151 of 257** carried patches end with a stray `-- ` signature separator and a
`cgit 1.3.1-korg` line, left by git.kernel.org's HTML view. Always *after* the
final hunk, so both `git apply` and GNU `patch` ignore it and the cumulative
audit is unaffected — cosmetic only. Not mass-edited here because it would churn
151 files and invalidate every checksum for no functional gain; worth stripping
the next time the extractor is touched, at which point `updpkgsums` is required.

## `next-20260928` — fetched and examined (7.4 material, nothing adopted)

The 2026-09-28 snapshot was fetched with **`git fetch --depth=1 origin tag
next-20260928`** after two plain fetches blew their budget on history. A
`--depth=1` tag fetch pulls the tag's tree and nothing else, which is all a
content comparison needs — worth remembering, since the full fetch had failed
twice and looked like an unreachable source. The linux-next clone can no longer
walk history afterwards, so `git log v7.3-rc5..next-20260928` returns *only* the
tip commit; that is the shallow graft, not an empty range.

Diffing the snapshot's tree against `v7.3-rc5`, for this machine's files:

| File | Δ (ins/del) | What it is |
|---|---|---|
| `gfx_v12_0.c` | 18 / 26 | 7.4 refactors: `ring_test_ib` moved to `amdgpu_job_alloc_with_ib()` + `amdgpu_job_submit_direct()`, the VMID loop replaced by `for_each_vmid_and_zero()`, and `gfx_v12_0_is_idle()` removed |
| `dcn401_resource.c` | 1 / 1 | include path only: `dml2_0/dml2_wrapper.h` -> `dml2_wrapper/dml2_wrapper.h` |
| `zswap.c` | 210 / 151 | queued zswap work |
| `r8169_main.c` | 561 / 145 | the **RTL8127** RSS series rejected above |
| `smu_v14_0_0.c`, `sch_cake.c` | — | unchanged |

**Nothing adopted.** Everything here is queued for the **7.4 merge window**, not
a 7.3 fix — these are refactors and layout churn (`gfx_v12_0_is_idle()` removal
and the DML2 directory rename have no `Fixes:` behaviour to port), and the
`r8169` delta is a series already rejected for targeting the wrong chip. Carrying
7.4 refactors on a 7.3 base would only manufacture conflicts at the 7.4 bump,
where they arrive for free. Recorded so the 7.4 rebase knows what to expect in
`gfx_v12_0.c`.

Note `sch_cake.c` is unchanged in the snapshot, so the v4 CAKE fix adopted above
has **not** reached linux-next yet — the carry is genuinely ahead of it.

## Work items, 2026-09-28 evening — read deeply, nothing adoptable

The earlier pass that day queried only a 6-hour `updated_after` window and read
three issues. Redone properly: **88 open issues moved in 7 days, 66 on-target by
title**, descriptions as well as comments fetched, and every hex-shaped token
checked against the trees rather than cited.

### The one that matters: `#5897` independently confirms `1168`, and shows `1171` is partial

`7.3: HDMI FRL status poll re-detects a live link, next CRTC disable hangs
(DCN 3.2.1)` — reporter on an RX 7600 with a JVC DLA-NZ9 over HDMI, running
7.2.3 with the two named commits backported.

**It confirms `1168` targets a real defect, with numbers.** The reporter
measured the sink setting FRL_Start after a **median ~450 ms**, against a
**~310 ms** busy-wait budget, and upstream lighting only 2/12 in each of two
runs — a longer wait lit 23/24. Our `1168` makes the 300 ms FRL link-training
budget unconditional at every rate; this is the same budget, measured failing,
on someone else's hardware. That is the first independent corroboration of
`1168` outside our own reasoning.

**It also shows `1171` is necessary but not sufficient.** The reporter tested
"the poll under `mutex_trylock(&dm->dc_lock)`" — which *is* our `1171` — and it
hung twice anyway. Their diagnosis is deeper: with one HDMI connector
`is_hdmi_frl_in_use()` is false, so the RETRAIN detect is destructive under a
live stream — it disables the HPO encoder and DSC and runs
`hdmi_frl_verify_link_cap()` at the sink's maximum rate, and **nothing
re-enables the stream**. The next CRTC disable then spins in
`optc32_disable_crtc()` forever. Locking does not help because the damage is in
what the detect *does*, not in racing for the lock.

Verified present in our base, not inferred: `amdgpu_dm_connector.c:3141` walks
links with no `dc_lock` and calls `dc_link_detect(..., DETECT_REASON_RETRAIN)`,
and `link_detection.c:908` runs the destructive `hdmi_frl_verify_link_cap()`
when `!is_hdmi_frl_in_use(link)`. Both files are shared across DCN versions, so
this is not a DCN 3.2.1-only path even though the reporter's hardware is.

Our `1172` implements **one of the two gates** the reporter says are needed
("skip it when the link has no dpms-on stream") — it skips polling unless
`link_status.link_active`. The second gate and the reporter's proposed
mechanism — answer `FLT_Update` with a stream restart (dpms off/on via
`dc_commit_updates_for_stream()`) instead of the destructive RETRAIN detect —
**exist only as prose in the comment. No patch was posted, in the thread or
anywhere.** Not adoptable; recorded so the next sweep recognises it if AMD
posts one.

`1171`/`1172` are both Fangzhi Zuo (AMD) with `Reviewed-by: Harry Wentland`, so
they were correctly sourced; the point is that they mitigate, and AMD's own
reviewer approved them as mitigation, not as the whole fix.

### `#5907` — carries `[PATCH]` in its title but the patch is in the description

`Null pointer dereference in ttm_lru_bulk_move_tail / amdgpu_vm_move_to_lru_tail`.
**Not adoptable, three times over:** the hardware is a **Ryzen 9 8945H /
Radeon 780M (Phoenix, GFX1103)** — an APU, not this machine's Navi 48; the
trigger is `options amdgpu gttsize=76800`, which we do not set; and the proposed
2-step fix is written **by the reporter inside the issue body** ("We propose the
following 2-step patch… 1. Reset the cursor bucket… 2. Add defensive check"),
with no author trail, no `Signed-off-by`, no commit or Message-ID. Per CLAUDE.md
YOU MUST NOT #3 that is not a traceable submission, and the change is a
`WARN_ON_ONCE` band-aid over a reservation mismatch rather than a root cause.
Worth watching if a real TTM fix follows it; nothing here to carry.

### Others checked, none actionable

- **`#5894` RX 9070 XT (VCN 5.0.0) vcn_unified_0 ring reset** — answered by
  nowrep: **a firmware bug, already fixed, pending a linux-firmware update**.
  Not a kernel fix at all. Useful for us because our GPU is VCN 5.0: if this
  ring reset ever appears here, the answer is firmware, not a patch.
- **`#5900`/`#5905`/`#5896`** — read the same evening; no patch in any of them.
- **`#5868` RX 9070 XT HDMI disconnect/reconnect loop** — a Samsung UE50MU6125
  declaring no FRL support (`max_frl_rate` 0). Sink-specific, not our display.
- **`#5663`** — already tracked; the SDMA DCC workaround question, unchanged.
- The large pageflip-timeout cluster (`#5647`, `#5511`, `#5872`, `#5843`,
  `#5640`, and ~10 more) remains **bug reports with no referenced fix** —
  consistent with the standing read of this tracker.

### Method note

The tracker's hex-shaped tokens are mostly noise: in this pass the only
"commit" in `#5900` was a **bol.com product URL**, and `#5907` cites no sha at
all. The two genuinely useful commits — `df94112ceebf` and `c953b39f9487` — were
named in `#5897`'s *description*, not its comments, and `c953b39f9487` is
**absent from our shallow clone by hash** even though the issue says mainline
7.3-rc4 has it; it had to be traced by its effect (`is_hdmi_frl_in_use()` at
`link_detection.c:908`) rather than by `git cat-file`. Reading descriptions, not
just comments, is what surfaced it.

## Sweep 2026-09-28 (late) — tip + "anything else" recheck; a CachyOS scan bug found

Prompted by "check the tip repo too". Tip is clean, but the recheck exposed a
**real bug in how this sweep scans CachyOS**, which had been reporting "nothing
new" while new content sat on the remote.

### The bug: `cachyos-linux` was being read off a stale 2022 ref

The sweep's freshness loop used `git -C repos/cachyos-linux log -1
origin/master`, which reports **2022-06-23** — a ref that has nothing to do with
this kernel. The branches that matter are `7.3/base`, `7.3/fixes`, `7.3/hdmi`
and friends. Read off the correct refs and compared against `ls-remote`:

| Branch | Local | Remote | |
|---|---|---|---|
| `7.3/hdmi` | `96f023bb8c13` | `96f023bb8c13` | up to date |
| `7.3/base` | `2630fcfd768e` | `8855497eb51b` | **behind** |
| `7.3/fixes` | `d10310a163ce` | `68f054f6774b` | **behind** |

The fetch had been run and reported success; it simply was never compared
against the right ref. Same family as the `sirlucjan` stale-local-branch trap
and the stale `torvalds` `master`: **name the branch you actually care about,
and compare it to the remote.** A freshness check pointed at the wrong ref is
worse than none, because it produces a confident "nothing new".

### What the correct refs revealed

**`7.3/fixes` — `68f054f6774b` `mm/slub: refill prefilled sheaves from the
barn` (Hao Li, 2026-09-21, `mm/slub.c | 81 +++`).** This is **the patch we
already carry as `2197`** — same author, same 81-insertion one-file shape, and
our copy was already verified content-identical to upstream v2 and to
sirlucjan's `0013`. CachyOS has now picked it up. **No action**; recorded so a
future pass does not re-derive it as a candidate.

**`7.3/base` — the `xswap` series was REVERTED and replaced by `vswap` v5**
(`596d0b52c29e` reverts the merge we had previously assessed; `8855497eb51b`
merges `7.3/xswapv5`). Twelve `mm, swap:` commits by **Nhat Pham**, 2026-09-18:

```
mm, swap: add virtual swap device infrastructure
mm, swap: support zswap and zero-filled swap pages as vswap backends
mm, swap: prepare the swap IO path for vswap
mm, swap: support physical swap as a vswap backend
mm, swap: enable THP swapin for vswap entries
mm, swap: write back vswap zswap entries to physical swap
mm, swap: reclaim physical slots backing cache-only vswap entries
mm, swap: only charge physical swap entries
mm, swap: add debugfs counters for vswap
mm, swap: defer memcg_table allocation for physical swap clusters
mm, swap: back vswap clusters with a VM_SPARSE array
```

**Not adopted.** It is a *feature* series — **23 files, 2206 insertions, 285
deletions**, with a single Fixes/Cc-stable marker across the whole thing — and
this repo's bar is fixes with traceable provenance or maintainer review. Two
further reasons to leave it: we **deliberately removed** the xswap predecessor
on 2026-09-22 and documented why the zswap+swapfile design was chosen (its
drain is automatic — the shrinker writes pool entries back to the entry's own
swap device, so a real file behind the pool keeps anonymous pages reclaimable),
and a 2200-line unmerged series in `mm/zswap.c` and the swap core would fight
every rebase.

**Recorded because it is the one live, moving thing in our exact subsystem.**
If the zswap+swapfile design is ever revisited, `vswap` v5 is the candidate and
this is where it lives. Note it also touches `mm/zswap.c` heavily (+135), which
we already carry ~20 patches against — a future adoption would need a conflict
pass, not a clean apply.

### tip — clean, and the reason is worth stating

`origin/master` is at `72c51a366945` (2026-09-28), verified against
`ls-remote`. Twenty commits in tip/master are **absent from rc5**, and none is
adoptable:

- **13** are the new **Preferred-CPU** series (`cpumask: Introduce
  cpu_preferred_mask`, `sysfs: Add preferred CPU file`, `sched/fair: Load
  balance only among preferred CPUs`, …). A feature, and its `sched/fair`
  load-balancing piece is **inert here** under `switch_all=1`.
- **5** are the **proxy-execution** series (`sched: Add sched_ext hooks for
  proxy execution`, …). A feature.
- **1** is `x86/cpu: Constify struct x86_cpu_id` — a treewide cleanup.
- **1** is `x86/mm: Don't apply va_align to hugetlb mappings on AMD F15h` —
  **F15h**, not our Zen 4; already rejected once.
- **4** are `virt: Introduce steal governor driver` — we are not a VM guest.

The apparent candidates that look like fixes (`x86/mce: Fix hardware debug
register corruption`, `drm/amdgpu: Fix last_update fence leak in
amdgpu_vm_init()`, `drm/amdgpu: Fix runtime PM leak in
amdgpu_debugfs_test_ib_show()`, `drm/amd/display: Fix dc stream excess put in
dm_update_crtc_state()`, `sched_ext: Count SCX_EV_SUB_BYPASS_DISPATCH`) are
**all already in rc5** — present by hash, and confirmed by content probe
(`SCX_EV_SUB_BYPASS_DISPATCH` appears at both `kernel/sched/ext/inlines.h:67`
and `:133` in rc5, the second being exactly what that fix adds). tip simply has
not been rebased onto rc5. **Grep for merges too:** the first pass matched
merge commits whose tag names contain the subject and briefly looked like five
adoptable fixes.

## 2026-09-30: switched from sched-ext (scx_cake) to BORE

User decision: drop `scx_cake`, run BORE instead, with explicit permission to
drop the sched_ext carries. `pkgrel` 2 -> 3. **257 -> 252 patches.**

### Added

- **`2419-sched-bore-7.0.0-burst-oriented-response-enhancer.patch`** — BORE
  7.0.0 by **Piotr Gorski**, from sirlucjan `7.3-rc/bore-dev-patches`. 47 hunks,
  14 files, 947 insertions. Adds `CONFIG_SCHED_BORE` and
  `CONFIG_MIN_BASE_SLICE_NS` (default 2000000), plus two new files
  (`kernel/sched/bore.c`, `include/linux/sched/bore.h`). BORE makes EEVDF task
  selection in `fair.c` burst-aware: it discriminates by runtime since the task
  last slept or yielded and favours less bursty (more interactive) tasks.

  BORE 6.8.0 also exists in `7.3-rc/bore-patches`; **7.0.0 taken as the newer
  major** (it is the `-dev` directory — see the risk note below).

- **`2420-sched-fair-do-not-scan-twice-in-detach_tasks.patch`** — Huang Shijie,
  `sched/fair: do not scan twice in detach_tasks()`. **This is a patch the
  previous sweep rejected as inert** ("`fair.c` under scx full-switch mode"), and
  switching to BORE makes it live — exactly the re-evaluation the user asked
  for. `env.loop_max` was computed from `busiest->nr_running` *without* the RQ
  lock, so it could disagree with the actual `cfs_tasks` length and walk the same
  tasks twice; SpecJBB hit it 330,000 times in a 30-minute run. Sets `loop_max`
  under the lock from `busiest->cfs.h_nr_queued`.

  **Adopted on `Reviewed-by: Vincent Guittot` + `Reviewed-by: Valentin
  Schneider`** — both scheduler maintainers — which clears the adoption bar.
  Series numbering `[PATCH 06/13]` stripped per CLAUDE.md YOU MUST #4. Applies
  clean to `v7.3-rc5`; BORE does not touch `detach_tasks()`.

### Removed — the seven sched_ext carries (user-approved)

`2005`, `2413`, `2414`, `2415`, `2416`, `2417`, `2418`. Every one targets
`kernel/sched/ext/` or `include/linux/sched/ext.h`. Under BORE the scheduler is
`fair.c`, so this code is not executed; the user explicitly authorised dropping
them in favour of BORE. **Recorded plainly because this is the first time this
repo has removed patches that were not superseded upstream** — they were
removed because the machine stopped using the subsystem, which is a different
reason and worth being able to reconstruct. If sched-ext is ever re-enabled,
these seven need to come back with it: they fix a NULL sub-sched dereference
raised from NMI (`2414`), a CPU-hotplug hang (`2416`), and a use-after-free.

### Modified — `0110` lost its `fair.c` hunk

BORE and `0110` write the same lines. BORE wraps `sysctl_sched_base_slice` in
`#ifdef CONFIG_SCHED_BORE ... #else ... #endif`; `0110` wraps the *same* lines
in `#ifdef CONFIG_CACHY`, setting the base slice to 400000 instead of 700000.
The two collide at `fair.c:80` and BORE cannot apply.

Resolved by **stripping `0110`'s `fair.c` section**, because BORE makes it dead
code: with `CONFIG_SCHED_BORE=y` the CachyOS block lands in BORE's `#else`
branch and is never compiled — `sysctl_sched_base_slice` is recomputed from
`nsecs_per_tick` and `min_base_slice` regardless. This is the *inverse* of the
situation the repo has documented for two years: that hunk was inert under
`switch_all=1`, and it is inert again under BORE, for a completely different
reason.

`0110`'s other seven hunks (`bus_lock.c`, `init/Kconfig`, `sched/sched.h`,
`mm/compaction.c`, `mm/huge_memory.c`, `mm/page_alloc.c`, `mm/vmscan.c`) are
untouched and remain live — which is why the patch stays rather than being
dropped. **An inert hunk is not an inert patch**, as this file has said before.

### Config

- `scripts/config -e SCHED_BORE` added at `PKGBUILD:750`. `MIN_BASE_SLICE_NS`
  left at its 2000000 default.
- **`CONFIG_SCHED_CLASS_EXT` deliberately LEFT ENABLED.** The user asked to drop
  the sched_ext *changes*, not the config, and BORE does not require it to be
  off — with no scx scheduler loaded, CFS+BORE is what runs. Keeping it means a
  fallback exists if BORE 7.0.0 (a `-dev` revision) misbehaves, at the cost of
  compiled-in code we do not exercise. **Flagged for the user to decide.**
- `scx_loader.service` disabled and stopped, so no BPF scheduler is loaded and
  `fair.c` — now BORE — is the active scheduler.

### Verification

- Cumulative audit: **all 252 patches apply cleanly to v7.3-rc5.**
- BORE 7.0.0 and 6.8.0 both apply clean to bare rc5; the conflict appeared only
  on the full series, and only in `fair.c` — which is how the `0110` overlap was
  found rather than assumed.

## Sweep 2026-09-30 — all sources, nothing else adopted

Run alongside the BORE switch; the fixes previously written off as inert were
re-examined in the new `fair.c`-is-live context.

**Version sweep: nothing new.** 16 content-identical resends; the 6 remaining
hits are all already dispositioned (`2045` v4 is the one adopted on 09-28;
`2302`/`2308`/`2314` are the kbuild v4 that cannot apply to rc5; `1151`'s "v4"
is an older February posting; `2032` is the mail line-wrap artifact).

**`next-20260930` (today) and `next-20260929` fetched with `--depth=1`.**
`next-20260930` vs `next-20260928` is **unchanged** in `fair.c`, `zswap.c`,
`slub.c` and `gfx_v12_0.c`. Against rc5 the snapshot differs in
`fair.c` (61/73), `core.c` (232/214), `zswap.c` (210/151), `slub.c` (206/129),
`r8169_main.c` (561/145, the RTL8127 series already rejected for wrong silicon)
and `gfx_v12_0.c` (18/26, 7.4 refactors). **All 7.4 material, not 7.3 fixes.**

**Re-examined per the user's instruction — the things we ignored *because of*
scx_cake, now that `fair.c` is live:**

| Candidate | Verdict |
|---|---|
| `detach_tasks()` scan-twice fix | **ADOPTED** as `2420` (above) |
| tip `sched/cache` fixes ×6 (all `Fixes:`, up to 3 `Reviewed-by`) | **All already in rc5** — checked by hash, every one. Nothing to do |
| tip `sched/fair: Load balance only among preferred CPUs` | Part of the **Preferred-CPU feature series**; a feature, not a fix |
| tip proxy-execution series (5) | Feature |
| `sched/fair` in `next-20260930` (61/73) | 7.4 work |

**`CONFIG_SCHED_CACHE=y` is set here** — worth knowing, because it is why the
six `sched/cache` fixes were checked at all rather than waved past as
feature-adjacent. They are all in rc5, so the config being on costs nothing.

**tip freshness verified against the remote** (`72c51a366945`); the 20 commits
absent from rc5 remain the Preferred-CPU, proxy-exec, `x86_cpu_id`, F15h and
steal-governor sets — none adoptable.

**CachyOS**: read off `7.3/*` (the `origin/master` bug fixed last pass).
`7.3/base` and `7.3/fixes` had both advanced; the fixes advance is `2197`
(SLUB barn) which we already carry, and the base advance is the `vswap` v5
series already recorded as a feature.

## Work items + cachymod, 2026-09-30 — nothing adoptable, two useful connections

Done with the methods this conversation established: **descriptions as well as
comments** (that is what surfaced `#5897` last time), `updated_after` rather than
page 1, and every hex-shaped token checked as a real commit rather than cited.

23 issues had moved since the previous pass. Nothing carried a fix.

### `#5912` may be the root cause `1074`'s TODO is waiting for

`[amdgpu][gfx1200] Possible DCC metadata corruption on static desktop surfaces
after S3 resume` — an **RX 9060 XT (Navi 44, `1002:7590`)**, 100% reproducible
on every S3 cycle, corrupting cached composited surfaces so the damage shows in
*software screenshots* (i.e. VRAM/backbuffer data, not scanout).

Our `1074` keys on `sdma_ip_version == IP_VERSION(7,0,0) || IP_VERSION(7,0,1)`
— this machine reports `sdma_v7_0_0` — with the comment:

```c
/* TODO: workaround for DCC corruption when moving BOs from multiple queues at
 * the same time: use a single queue until the root cause is identified and fixed.
 */
```

So `1074` is a *mitigation with an open TODO*, and `#5912` is a fresh DCC
corruption report on a **different Navi 4x chip running the same SDMA 7.0.x**.
Same failure class, same family, root cause still unidentified. **Recorded as a
corroborating data point for `#5663`**, not as something to adopt — the issue has
**0 comments** and no patch. Worth re-reading if AMD ever posts a root-cause fix,
because that would let `1074` (a serialising workaround) be retired.

### `#5910` — a real shared-code bug, no patch, not our chip

`amdgpu_vm_tlb_flush()` returns early on `!*fence`, so a CPU page-table update
can leave the fence slot NULL and the GEM VA timeline may signal **before** the
TLB invalidation completes. Silent memory corruption under VA reuse. Reported on
Navi 32, 0 comments, no patch. **Shared amdgpu code**, so it would apply here,
but there is nothing to carry. Notable because our `1065`/`1066` are also
fence-slot work — different path (eviction slots / userq rearm), same subsystem,
and a reminder this area has more than one live hole.

### Also checked, nothing in them

- `#5909` — Navi 48, but **over USB4/TB5**; its 4 comments are all "changed the
  description". Not our topology (direct PCIe dGPU).
- `#5916` — hibernation `thaw()` made a no-op by a 2026-07 patch; superm1 (AMD)
  engaged, discussion only. We use `mem_sleep_default=deep` (suspend), not
  hibernation.
- `#5915`/`#5914` (Navi14), `#5891` (Navi 33), `#5822` (Strix Point),
  `#5908` (780M), `#5845`/`#5847` (laptop backlight) — wrong silicon or
  laptop-only.

## cachymod — checked, nothing to include

`repos/cachymod` is a **separate community project** ("CachyMod — run a custom
kernel on CachyOS"), fresh to 2026-09-27, and it carries **only
`linux-cachymod-7.2/`** — there is no 7.3 line, so its patches are written
against a base two releases behind ours.

Its fair.c content is exactly the category we would have skipped while on scx,
so it was examined properly rather than dismissed:

| Patch | What it is | Verdict |
|---|---|---|
| `0260-fair-update-cachy-mods` | sets `sysctl_sched_tunable_scaling = TUNABLESCALING_NONE`, `base_slice = 800000000ULL/HZ*(HZ>500?2:1)`, `migration_cost = 400000` | **Superseded by BORE** |
| `0360-fair-revert-cachy-mods` | the inverse (back to `TUNABLESCALING_LOG`, 700000, 500000) | alternative option, not a fix |
| `0280-prefer-idle-core` | `sched/fair: Prefer the previous cpu for wakeup`, Eric Naim | **Reverted — by its own author** |
| `0000-revert-gaming-sched` | Piotr Gorski reverting CachyOS's gaming-sched | we never carried gaming-sched |

**`0260` independently confirms the `0110` strip was right.** It edits the *same
lines* BORE and `0110` collide on — `sysctl_sched_tunable_scaling` and
`sysctl_sched_base_slice` — and it *deletes* the `#ifdef CONFIG_CACHY` block to
do so. CachyMod reaches by hand the same conclusion BORE reaches structurally:
when this design is in use, the CACHY base-slice block goes away.

**`0280` is the one to be careful about.** It *applies cleanly to our rc5 base*,
which for a 7.2-era patch is surprising and would normally invite adoption — but
`a4808133047d` (2026-07-15) reverts it, and the reverting author **is the patch's
own author**, on both `7.2/base` and `7.2/cachy`. A clean apply is not evidence
of anything; the author withdrawing their own patch is the signal that counts.

## Ultra-sweep 2026-09-30 (late) — work items + mailing lists, 2 adopted

### Adopted: `9078`, `9079` — two reviewed amdgpu/userq fixes

Both by **Jesse Zhang**, posted 2026-09-30, and both **`Reviewed-by: Christian
König`** (in his replies, not in the reposted patches — see below).

- **`9078` `drm/amdgpu/userq: only accept doorbell BOs as queue doorbell`.**
  `amdgpu_userq_get_doorbell_index()` pinned *any* BO passed as
  `doorbell_handle` into the doorbell domain. For a regular BO, TTM moves it
  with `ttm_bo_move_null()` and **its contents are lost** — and since an
  importer on the same device gets the exporter's GEM object, a client could do
  this to a buffer another client had shared with it. `Fixes: f09c1e6077ab`.
- **`9079` `drm/amdgpu/userq: return the memdup_user() error for the user MQD`.**
  `mes_userq_mqd_create()` returned `-ENOMEM` for every `memdup_user()`
  failure, masking `-EFAULT` (bad pointer) and `-EINTR` (signal). Also drops
  two error messages a client could spam the log with. Two `Fixes:` tags.

Both fixes target code confirmed present in our base by content probe
(`doorbell_handle` x4 in `amdgpu_userq.c`, `memdup_user` x3 in
`mes_userqueue.c`), in the userq subsystem we already carry `9062`-`9071` for.

**On the `Reviewed-by`:** König's tag is in his reply, and the author's v2 folds
in his feedback ("v2: drop the error message, use a local abo variable
(Christian)"), but the reposted patch carries only `Signed-off-by`. The patch is
kept **exactly as posted** rather than having a trailer grafted on that its
author did not write; the review is recorded here with its message-ids
(`1affeb9e5704cad6f209bb75c3d0bbf09255408d`,
`6ba77392579e3f055e47f3da9bbfa6e371c73898`) so the provenance is traceable
without editing the artefact.

### Rejected by the maintainer: the third patch of that series

`drm/amdgpu/userq: don't publish the queue before create is done with it`
(Jesse Zhang) describes a create/free race on a guessable queue ID. **König
declined it outright:** *"I honestly don't see that as problematic. debugfs has
tons of such issues and that is generally ok."* (`02588cfaad04d2cce60715d4c29cbb652e298f56`).

That is why the V2 of the series is 2 patches and the original was 3 — **the
maintainer dropped it, not the author.** Taking the V2 whole is the correct
read; taking the original 3-patch series would have carried something its
maintainer explicitly rejected. This is the "read the thread for an objection"
rule earning its keep.

### The ultra-sweep of the tracker itself

Done exhaustively rather than by window, because hand-picked sets keep missing
things: **all 1,835 open issues enumerated** (19 pages of the REST API) and
**7,078 distinct hex-shaped tokens** extracted from titles *and* descriptions.
Batch-checked with `git cat-file --batch-check`: **128 are real commits**; the
rest are URLs, image paths and PCI ids — the expected ratio.

**Every one of the 128 is accounted for. Nothing adoptable.** Probing them
surfaced a methodology error worth recording: the first pass used
`rev-list v7.3-rc5` for ancestry, which is **worthless here — the clone reports
`--is-shallow-repository == true`**, so it returns only grafted history and
reported 38 commits as "not in rc5". Content probes showed **7 of the 10 most
plausible were actually present**. The three that still looked absent were also
false negatives, from grepping the commit's *subject words* instead of the code
it introduces: `11752c013f56` "mes ring buffer overflow" adds no such string —
its change is `AMDGPU_RING_TYPE_MES` in `amdgpu_ring.c:245` and the
`error_undo:` label in `mes_v12_0.c`, both present in rc5.

**The rule this yields: probe for the identifier the commit *adds*, never for
the words in its subject.** The existing trap in CLAUDE.md covers the duplicate
direction (a carried patch re-inserting itself); this is the mirror — a
*false "absent"* that would have justified adding a patch we already have.

**One live check worth recording:** `#5685` reports `GPUReclaim` in
`/proc/meminfo` drifting to ~93 GiB on a **Navi 48** GPU after a game exits,
against ~397 MiB of real GTT use. Its referenced fix (`ae80122f3896`, Airlie's
`NR_GPU_*` accounting v4) **is already in rc5** — `ttm_pool.c:195/232/344/345/370/371`,
with `NR_GPU_RECLAIM` defined in `mmzone.h`. Measured on this machine:
`GPUReclaim` 103 MiB against `mem_info_gtt_used` 132 MiB — **consistent, no
leak reproduces here.**

### Mailing lists

All eleven mirrored lists refreshed to 2026-09-30. New mail scanned for
on-target material. **The scheduler inversion now shows up in the sweep
itself:** 14 new `sched_ext` patches arrived, and they are now *low*-value for
this machine, while `fair.c` mail is the live category — the reverse of every
previous pass.

Rejected for lack of review (`Reviewed-by` count 0) or wrong scope: amdgpu
debugfs GRBM/SRBM lock copy-out, amdkfd interrupt-drain lost wakeup, the
`gfx12 xccs-per-xcp` VFI patch, `io_uring/tw` task-work starvation, and König's
8-patch VM rework (a restructuring of `amdgpu_vm_update_range` across 6 files,
not a standalone fix — it carries Timur Kristóf's `Reviewed-by` but taking one
patch out of a rework series would be incoherent).

**Series is 254 patches.**

### Addendum: making the sched-ext switch survive a reboot

Disabling `scx_loader.service` on 2026-09-30 was **not sufficient**, and the
reason is worth recording because it is invisible to the obvious check.

**Two paths could have re-armed scx_cake at boot:**

1. **`/etc/scx_loader.toml` shipped `default_sched = "scx_cake"`**, and the file
   says so itself: *"the scheduler that will be started automatically when
   scx_loader starts (e.g., on boot)"*. Note the real config path is
   **`/etc/scx_loader.toml`**, *not* `/etc/scx_loader/config.toml` — the latter
   is what a `find`-by-convention looks for and it does not exist.
2. **`scx_loader.service` is D-Bus-activatable.** It is described as a *"DBUS
   on-demand loader"* and `/usr/share/dbus-1/system-services/org.scx.Loader.service`
   maps the bus name `org.scx.Loader` to `Exec=/usr/bin/scx_loader` with
   `SystemdService=scx_loader.service`. **A `disabled` unit with an empty
   `WantedBy=` is still startable on demand via D-Bus**, so `disable` alone
   left a live re-arm path: anything requesting that bus name would have
   started the loader, which would then have loaded `scx_cake` — silently
   taking the scheduler back off `fair.c` and off BORE.

**Both neutralised:**

- `systemctl mask scx_loader.service` — symlinked to `/dev/null`, which blocks
  systemd *and* D-Bus activation. Verified by trying it: `systemctl start`
  returns *"Unit scx_loader.service is masked."*
- `default_sched` commented out in `/etc/scx_loader.toml` (original saved as
  `.bak-scx-cake`), so even a later unmask does not immediately re-arm scx_cake.

Post-state, checked rather than assumed: `sched_ext state: disabled`,
`switch_all: 0`, no scx userspace process, zero enabled scx units.

**The generalisable lesson:** for a service that must not come back, `disable`
answers "will systemd start it?", not "can anything start it?". Check for a
D-Bus activation file (`/usr/share/dbus-1/system-services/`), a socket unit, an
autostart entry, and the service's own config for an auto-start default. This
service had **all four** categories worth checking and two of them were live.

## Sweep 2026-10-01 — all sources; nothing adopted, two drop-list items, one watch

Ran on `rc5-5` with BORE confirmed live (`sched_burst_penalty_scale`,
`sched_burst_cache_lifetime`, `sched_burst_smoothness` all present;
`sched_ext state: disabled`, `switch_all: 0`, `scx_loader: masked`).

### Drop list grows: `2041` and `2151` are both upstream now

Mainline has moved **147 commits past rc5** with a `net-7.3-rc6` merge and no
`v7.3-rc6` tag yet. Two of our carries are in it, by subject **and** author:

| Ours | Now in mainline |
|---|---|
| **`2041`** `net: gso: limit recursive IP-in-IP segmentation` | `006c8b834ae` — same author (Zihan Xi), same date (2026-09-24) |
| **`2151`** `mm: shmem: ignore sysfs configs for shmem forced collapse` | `72c3d682c16` — same author (Baolin Wang), same stat |

Both will be duplicates at the next rebase. **7.4 drop list is now: `2041`,
`2151` (landed upstream), `1063` (superseded by Stanner's `4b7a49d66c`).**

### The `fair.c` candidate died on the maintainer's own words

The most promising find was **`sched/fair: Take slice protection into account
when arming HRTICK` (Christian Loehle, v2 1/5)** — `fair.c`, and therefore
**live here now that BORE runs**, where it would have been inert a week ago.

**Peter Zijlstra rejected it:**

> *"Right, so I don't much like this. This wrecks the steady state behaviour in
> favour of our 'dodgy' wakeup heuristics. I would much rather we stick to the
> paper for steady state, and let wakeups be wakeups."*

and **the author conceded**:

> *"Alright, I guess the same reasoning then for 5/5? Again these are all just
> from throwing a bunch of artificial rt-app tests against Vincent's patchset
> and seeing what sticks…"*

**Not adopted.** This is the third time this session that reading the thread
reversed a verdict — a patch that looks well-formed and is in the live
subsystem is still not carryable when its maintainer objects and its author
agrees. Note the sweep would have shown it as a clean, unreviewed candidate.

### Watch: a possible kernel regression in RDNA3/4 gaming

`#5873` (MODE1 reset, *"Illegal opcode in command stream"*, Navi 31) has agd5f
calling it a possible duplicate of `#5711`, and a reporter giving the decisive
bisect-shaped observation:

> *"**The kernel is the variable:** linux-cachyos 7.2.6 and 7.2.8 hang within
> ~10 minutes. linux-cachyos-lts 6.18.52 ran the same game, Mesa and Proton for
> 66 minutes clean. My last known-good 7.x kernel was **7.1.8**. **Same firmware
> on both kernels** (ME 0x9ec, PFP 0xa96, MEC 0xae6, MES 0x92 …)."

Same firmware across good and bad kernels rules firmware out — this reads as a
**kernel regression introduced around 7.2**, with the signature *illegal opcode
→ MES reset failure → MODE1*.

**`#5917` is the one to watch for this machine specifically:** *"RX9070XT,
7.3.0-rc5 kernel, ring comp_1.0.1 timeout, screen output freeze with
Overwatch"* — **our exact GPU (`1002:7550`, Navi 48) on our exact kernel
version (7.3.0-rc5)**, with a devcoredump attached and one comment that is only
"changed the description". No fix referenced, no patch. **It reproduces on
7.2.8 too**, so it is not new to rc5.

Recorded rather than acted on: there is nothing to carry, and the RDNA4 and
RDNA3 reports may or may not share a root cause. If a fix lands it will matter
here directly.

### Checked and rejected

- **`drm/amdgpu: copy debugfs register data outside the GRBM/SRBM locks` is now
  v2** — still the debugfs/umr-only circular-lock path identified on 2026-09-30.
  Progressing, still no review, still not on our path.
- The amdgfx **UALink/NPA** series (`Enable remote TLB shootdown`, `Enable RPC
  on importer NPA mappings`, `Fix NPA-REVOKE racing an in-flight UALink
  import`) — datacenter interconnect, not Navi 48.
- `amdgpu: Use 2-argument strscpy()`, `drm/amdkfd: fix lost wakeup in interrupt
  drain`, `drm/amdgpu: fix memleak when amdgpu_vm_ptes_update fails`,
  `drm/amdgpu: serialize vblank counter reads against GPU reset`,
  `io_uring: fix out-of-bounds bvec access`, `io_uring/memmap: fix non-compound
  alloc fallback`, `mm: Make swapoff interruptible when unusing mms/shmem` —
  **all originals show zero `Reviewed-by`/`Acked-by`**, and the threads contain
  no review either.
- `tcp_bic`/`tcp_hybla`/`tcp_cubic` divide-by-zero series — net-next, and we run
  BBR3.
- `nvme-pci: avoid the deepest sleep state on Transcend MTE672A` — not our SSD
  (Phison E16); `nvme-multipath` v4 — we do not use multipath.
- 21 work-items moved; the on-target ones beyond the above are Navi 31, Navi 33,
  Navi 44, Vega20, Picasso/Raven2 and Strix Point — none of this machine.

Series stays at **255 patches**.

## Sweep 2026-10-02 — coverage gap closed; nothing adopted

### The gap: five subsystem lists were never mirrored

Prompted by merge-tag output listing `driver-core`, `i2c`, `wq`, `cgroup` and
`perf` — subsystems whose **own** mailing lists this sweep did not watch, so
their work was only visible after it reached mainline. **Coverage went from 14
to 18 mirrors**, adding `linux-i2c`, `linux-pci`, `cgroups`, `linux-usb` and
`linux-gpio`. Probed with `git ls-remote` (a plain `curl` to the list URL
returns **403** — that is the Anubis-gated web UI, not the git endpoint, which
is the same trap as the lore.kernel.org rule).

Also tested and **not available as git mirrors**: `linux-wq`,
`linux-driver-core`, `linux-thermal` (see `linux-pm`), `linux-vfs` (see
`linux-fsdevel`), `linux-hid`, `linux-pinctrl` (see `linux-gpio`). `ata` is
`linux-ide`, `hid` is `linux-input`; both available but not on this hardware.

**Relevance of the new five:** `linux-i2c` (we carry DDC/I2C display fixes
`1141`-`1143`), `linux-pci` (`pcie_aspm=off` is in our cmdline), `cgroups`
(memcg — the `mem_cgroup_update_lru_size` warning), `linux-usb` and
`linux-gpio`. `linux-gpio` mattered specifically because our cmdline carries
`gpiolib_acpi.ignore_interrupt=AMDI0030:00@3,AMDI0030:00@10`.

### What the new lists produced: one near-miss, nothing adoptable

**`pinctrl: amd: Clear S4 wake bits when firmware has _AEI`** (Mario Limonciello,
2026-10-02) looked promising against our `ignore_interrupt` cmdline workaround.
Read in full, it is **off-target**: the symptom is *"the machine powers back on
immediately after shutdown"* on a **Chuwi CoreBook Plus laptop**, caused by
firmware leaving the S4/S5 wake bit set on GPIO 24. Its `Fixes:` targets
`ffe8a0c6b552`, a laptop-visible regression. Our workaround addresses a
different mechanism — spurious GPIO **interrupts** on AMDI0030, not S4 wake
bits. It carries `Fixes:`, `Cc: stable`, `Reported-by`, `Tested-by` and
`Closes:` but **no `Reviewed-by`**.

Also from the new lists, all rejected: `linux-i2c` was entirely vendor (Nuvoton,
Rockchip, Qualcomm, NXP, MCTP); `linux-pci` was ATS / s390 / lan966x / AtomISP;
`cgroups` had `mm: preserve nolock context through memcg cleanup` (memcg+slub,
worth a look, unreviewed); `linux-usb` was gadget/typec/dwc3; `linux-gpio` was
pinctrl-qualcomm, loongson and laptop quirks.

### Work items: checked for patches, not just bug reports

Swept for issues whose **title or description actually contains a patch** —
`[PATCH]`, "we propose", ```diff``` — rather than triaging titles. Of 59 issues
in the window, **4 carry one**: `#5923`, `#5910`, `#5907`, `#5760`.

- **`#5923`** `[gfx1036] GPU memory writes vanish after idle with agent-scope
  dispatch fences` — **gfx1036 is Navi 23 (RDNA2 iGPU)**, not Navi 48, and the
  reporter states the diagnosis came from an LLM and they *"can only verify as
  much as I can"* on hardware they *"aren't familiar with"*. Not adopted.
- `#5910` (Navi 32, `amdgpu_vm_tlb_flush` early-return), `#5907` (Phoenix APU +
  `gttsize=76800`, reporter-written patch) — both already assessed on 2026-09-30.

### Sources checked, nothing new

- **`next-20261002` does not exist yet** — newest tag is `next-20261001`, already
  fetched. **`v7.3-rc6` is not tagged**; master sits at the `net-7.3-rc6` merge.
- Mainline unchanged since the 2026-10-01 pass (147 commits past rc5).
- tip and drm-misc unchanged.

Series stays at **255 patches**.

## Sweep 2026-10-02 (evening) — nothing adopted; six io_uring candidates listed

Full pass: all trees, all 17 lore mirrors, the drm/amd work-items tracker with
comments, and the version sweep over all 255 carries. **Series stays at 255.**

### Version sweep — 6 flagged, all resolved

18 carries were byte-identical to a newer resend and skipped. The 6 that
differed:

| Carry | Verdict |
|---|---|
| `2045` | The v4 "hits" are cover letters (`[PATCH net v4 0/2]`, no diff). Already adopted 2026-09-28. |
| `2032` | **Line-wrap artifact only.** Upstream v3 wraps one expression across a line break, we emit it as two; the added-line *sets* are otherwise identical. Not a new version. |
| `2302`, `2308`, `2314` | kbuild **v4** vs our **v3**. Verified below. |
| `1151` | The "v4" is the older February posting; a September `[PATCH v1 2/3]` re-post of the same passive-VRR work carries no newer content. |

### The kbuild v4, verified rather than assumed

The prior pass recorded "v4 cannot apply to rc5" but did not show the check.
Re-ran it against a throwaway rc5 worktree (`git apply --check`):

- `2302` **FAILS** — `include/asm-generic/vmlinux.lds.h:855`, `scripts/Makefile.vmlinux:103`
- `2308` **FAILS** — `scripts/kallsyms.c:5`
- `2314` applies **clean**, but it is one stage of a reworked interdependent
  series (the part count went 20 → 22, so part numbering shifted), and it
  depends on the two that fail.

Independently, **v4's additional content is predominantly ARM64 support** — the
lines v4 adds that v3 lacks are `_veneer`, `_SDA2_BASE_`,
`__kvm_nvhe___kcfi_typeid_`, `L0`, `/* arm */`. That is hardware this machine
does not have. **Not adopted**; revisit at the version bump when the base moves.

### Mailing-list coverage gap: `rg -r` is `--replace`, not `--recursive -l`

Caught mid-sweep. `rg -rln '<pattern>' <path>` does not mean "list files"; `-r`
is `--replace`, so the match text is substituted in the output. A first pass
used it while probing for `drm_connector_hdmi_*` and `drm_hdmi_helper.h` in rc5
and produced mangled output (`#include <drm/display/ln>`). The negatives were
re-run with plain `rg -n` / `rg -l` and a positive control before being
believed. Same family as the `rg -h` trap already in `LESSONS.md`.

### Work items — 28 updated since 2026-09-30

One new on-target thread, no fix posted:

- **`#5921` (filed 2026-10-02) `[Navi 48 / DCN 4.0.1] MODE1 reset on every
  suspend`** — another RX 9070 XT (`1002:7550`) + DCN 4.0.1 box, Bazzite,
  kernel 7.2.7. Reports the SMU driver/firmware IF mismatch
  (`driver 0x2e` vs `fw 0x33`) and an `optc401_disable_crtc` `REG_WAIT`
  timeout. **agd5f answered the same day: *"The firmware IF is a red herring.
  We've already removed that message from the driver to avoid future
  confusion."*** So the obvious lead is ruled out by the maintainer and the
  cause is unstated. **Checked against this machine: the journal has never
  logged a `MODE1 reset`, and this box does not suspend.** Watch only.
- `#5917` (RX 9070 XT / 7.3.0-rc5 comp_1.0.1 timeout) and `#5912` (gfx1200 DCC
  after S3) had **description edits only** — no new analysis.

### Candidates found, not adopted (phase 2 — list before adding)

**1. `io_uring` 7.3-rc6 fixes pull — six un-carried commits.** (Jens Axboe, tag
`io_uring-7.3-20261002`, head `a92193c91e88`.) This is a maintainer pull, so it
clears the bar. **We already carry its two most important commits**: `2049` *is*
the SQPOLL `task_work` use-after-free (`io_req_normal_work_add`), and `2048` is
the BPF-loop task-context init. Not carried, and the configs are **live here**
(`CONFIG_IO_URING_ZCRX=y`, `CONFIG_IO_URING_BPF=y`):

| Commit | Author |
|---|---|
| `io_uring/bpf_filter: mark source as COW when cloning filters` | Hui Peng |
| `io_uring: only post the dummy skip CQE on CQE_MIXED rings` | Hui Peng |
| `io_uring: fix free entry check for 32b CQEs on CQE32 rings` | Hui Peng |
| `io_uring: zero big_cqe for aux CQEs on CQE32 rings` | Hui Peng |
| `io_uring/zcrx: requeue multishot receives stopped by a local resource` | Junyuan Feng |
| `io_uring: End a TX_TIMESTAMP multishot cmd when the CQ is full` | lollipopkit |

**The basis for an earlier verdict changed here — re-read it.** The 2026-09-27
entry dispositioned the Hui Peng CQE32/CQE_MIXED work as *"7.4-bound, not for
now"*, because Axboe had replied *"I did do this work for you and split it into a
7.3 and 7.4 set"* and the remaining half sat on `for-7.4/io_uring`. **He has now
folded those same three commits into the 7.3-rc6 pull.** The branch a patch sits
on is not a durable property; this is the same failure mode as `2420`, rejected
under scx and adopted once `fair.c` became live. All six clear the audit bar.

**2. `drm/sched: Fix out of bounds entity priority check`** (Tvrtko Ursulin,
part 1/9 of a cleanup series). The bug is real: `entity->rq_priority` is computed
from the **unclamped** `priority` and then used to index `sched_rq[]`, and rc5's
default is `DRM_SCHED_POLICY_FIFO` (`sched_main.c:87`), so the raw priority is the
one used. **Unreachable here:** amdgpu sets `num_rqs = DRM_SCHED_PRIORITY_COUNT`
(the maximum, `amdgpu_device.c:2294`) and sanitizes userspace priority through an
allowlist that maps to values 1–3, so it cannot emit an out-of-bounds index. No
`Reviewed-by` yet — posted the same day. **Deferred**, either way.

**3. `drm/display: hdmi: Prevent NULL dereference in sync_scdc()`** (Cristian
Ciocaltea, `Reported-by: Dan Carpenter`). **Rejected with evidence:** the code it
fixes does not exist in rc5. `drivers/gpu/drm/display/drm_hdmi_helper.c` is 428
lines of infoframe helpers only, containing **zero** `drm_connector_hdmi_*`
symbols — verified with a positive control on the surrounding helpers — and
amdgpu references `drm_connector_hdmi` in **zero** files. The whole HDMI
scrambling/SCDC framework the `Fixes:` tag points at is 7.4 material.

### Other sources — nothing on-target

- **cachyos `7.3/fixes`**: `68f054f6774b mm/slub: refill prefilled sheaves from
  the barn` is **already ours** (`2197`, adopted 2026-09-26 — same Hao Li patch,
  CachyOS picked it up afterwards). `2d0a9e75fe41 wireguard: queueing: preserve
  tstamp_type` — **`# CONFIG_WIREGUARD is not set`**, no path here.
- **`bdea4980182 net: page_pool: fix use-after-free in page_pool_recycle_ring_bulk()`**
  — a well-formed fix (two `Reviewed-by`, `Fixes:`, one line) but **rejected as
  unreachable**: `r8169` does not use page_pool; the only Realtek driver that
  does is `rtase`, a different part, and nothing else on this machine loads a
  page_pool user. Machine-specific rejection, not a quality judgement.
- `drm-next` / `agd5f-linux` / `amd-staging` — 7.4 material (`amd-drm-next-7.4`)
  and MacBook VI ASIC resets. Not our silicon.
- `tip` — 7.4-window merges (`x86/tdx`, `sgx`, `sev`, `microcode`, …).
- `firelzrd-bore-scheduler` tops out at **BORE 6.8.0 for 7.3-rc2**; we carry
  **7.0.0** (`2419`) — the repo is behind us, not ahead.
- `firelzrd-lru-marie` **v0.11.1r2** = what we carry. Current.
- `sirlucjan/7.3-rc/cachyos-fixes-patches-v6` = what we carry; no v7 exists.
  `bore-patches/` carries `bore6.8.0`.
- `linux-tkg` idle since 2026-09-12. `linux-mm` v2 is an unused-API removal.

### State

**`next-20261002` still does not exist** — newest is `next-20261001`. **`v7.3-rc6`
is not tagged**: `git ls-remote --tags` on torvalds returns rc1–rc5 only and
`origin/master`'s `Makefile` reads `EXTRAVERSION = -rc5`, so the `pm-7.3-rc6`
and `mtd/fixes-for-7.3-rc6` tags in the subsystem trees are pull-request tags
named for the rc they are destined for, **not** evidence that rc6 exists.
Mainline is 203 commits past rc5 (was 147); master `5e0f8396d48`.

## Sweep 2026-10-03 — one candidate; three carries confirmed absorbed upstream

Full pass: torvalds, linux-next (`next-20261002`, newly published), tip, drm-next,
agd5f, amd-staging, all 17 lore mirrors, the drm/amd tracker with comments, and
the version sweep over all 255 carries. **Series stays at 255.**

### `1074` has been absorbed upstream — drop list

`next-20261002`'s change to `amdgpu_ttm.c` **is our `1074`, line for line** — the
same `TODO` comment, the same `num_move_entities = 1` for
`IP_VERSION(7,0,0) || IP_VERSION(7,0,1)`. The landed commit is agd5f
`c1702ed0d64a` *"drm/amdgpu: implement workaround for sdma dcc corruption"*
(Pierre-Eric Pelloux-Prayer, `Reviewed-by: Alex Deucher`, `Reviewed-by:
Christian König`, `Fixes: 3a6f6eeb3db5`), present in `amd-staging-drm-next` and
now in linux-next.

Work item **`#5663` is resolved**: agd5f, 2026-10-02 — *"The patch was sent
upstream for 7.3/7.4 this week and once that lands it will make its way back to
stable kernels."* This is the condition the ledger has been watching for since
`1073`→`1074`; the workaround's `TODO` (root cause still unknown) has **not**
been closed, so the workaround is the accepted resolution, not a stopgap we
replaced.

**Our rc5 base does not contain it, so `1074` stays for now.** Drop it when the
base moves to a tree that has `c1702ed0d64a` — otherwise it is a duplicate
carry, the `9007` failure mode.

### Three more carries now in mainline master — drop list

Mainline advanced `5e0f8396d48` → `e767a4ea70a` (123 new commits). Among them:

| Carry | Upstream commit | Note |
|---|---|---|
| `2046` | `ab6c756f28c` blk-mq: set RQF_USE_SCHED when the operation is known | Keith Busch, `Reviewed-by: Christoph Hellwig` |
| `2048` | `a3bdf68feec` io_uring: initialize task context before running the BPF loop | |
| `2049` | `a92193c91e8` io_uring: fix task_work add use-after-free with SQPOLL | |

The whole `io_uring-7.3-20261002` pull is in master, so the six io_uring commits
listed as candidates on 2026-10-02 will arrive with the base — they no longer
need carrying as patches, they need dropping once the base has them. **All four
are drop-list entries, not removals**: nothing is removed without explicit
approval.

### Candidate: `2198` — `mm/slab: do not wake up kswapd in __kfree_rcu_sheaf()`

| | |
|---|---|
| Commit | `af2fb3ee667` (mainline master) |
| Author | Harry Yoo (Meta) `<harry@kernel.org>` |
| Problem | `kfree_rcu()` can run under `pi_lock` (a raw spinlock in the scheduler). Allocating with `__GFP_KSWAPD_RECLAIM` wakes kswapd, which takes `pi_lock` — **circular lock dependency and deadlock**. Confirmed with a lockdep splat (`&p->pi_lock` vs `&pgdat->kswapd_wait`). |
| Fix | Use `__GFP_NOWARN` instead of `GFP_NOWAIT` in `__pcs_replace_full_main()` and `__kfree_rcu_sheaf()`, so no kswapd wakeup. |

**Verified:**

- **Not carried** — grepped the series for the subject, the author and the
  function; the only `kswapd` hits are unrelated (`2139`, `2140`, `2184`,
  `2101`).
- **Applies clean** to a throwaway rc5 worktree (`git apply --check`).
- **Target lines exist in rc5**: `mm/slub.c:5972`
  (`alloc_empty_sheaf(s, GFP_NOWAIT, SLAB_ALLOC_DEFAULT)`) and `:6131`
  (`gfp_t gfp = allow_spin ? GFP_NOWAIT : __GFP_NOWARN`).
- **No conflict with our series.** `2197` is the only patch of ours that touches
  `mm/slub.c`, and its hunks are at lines 453/3329/3346/5104 while this one's are
  at 5969/6128/6157 — disjoint regions.
- Numbered `2198` (next free in `2100–2199`). **Listed, not adopted** — per the
  documented cycle, candidates are listed before anything is added.

### Sources with nothing on-target

- **Mainline's other 120 commits** are laptop ALSA/ASoC quirks, CIFS/netfs
  client fixes, bpf tracing edge cases, spi, virtio_blk and kprobes. None touch
  this machine's hardware.
- **tip: 0 new commits** since `8f511d67b4fb` — unchanged.
- **`next-20261002` vs `next-20261001`**: 221 on-target files changed, an
  amdgpu-wide batch (`drivers/gpu/drm/amd/amdgpu/*`). The only on-target delta
  that is a *fix* rather than 7.4 material is the `amdgpu_ttm.c` hunk above.
- **cachyos `7.3/fixes`** unchanged since the 2026-10-02 pass
  (`2d0a9e75fe41`). **drm-next / agd5f / amd-staging** on 7.4 material.
- **Version sweep: the identical six, unchanged.** `2045` (cover letters,
  adopted), `2032` (line-wrap artifact — content-identical, re-confirmed),
  `2302`/`2308`/`2314` (kbuild v4, verified to fail against rc5),
  `1151` (older February posting). 18 content-identical resends skipped.
- **Work items (35 updated)**: `#5663` resolved as above. The other on-target
  threads are CC-only or unresolved — `#5902` (HDMI FRL same-sink HPD pulse
  leaves the display dark), `#5905` (Navi 48 fan stops below ~50 °C in custom
  fan_curve mode), `#5910` (missing TLB flush fence for CPU page-table updates)
  each have a single `agd5f` CC note and no patch. `#5921` (Navi 48 MODE1 reset
  on suspend) had agd5f rule the SMU IF mismatch a red herring on 2026-10-02.
- **New list postings** are features or off-target: the amdgpu second-level trap
  handler v3 series, the 17-part DC 3.2.401 batch (7.4), the v9 luminance
  property series, and an amdkfd surprise-removal pair (GPU hot-unplug — not
  this machine's topology).

### Tooling traps hit and corrected this pass

- **`git rev-parse <rev>:<path>` echoes its argument back when the path does not
  resolve** rather than failing. My snapshot comparison printed
  `next-2026` for `kernel/sched/bore.c` (not upstream — it is our patch) and for
  a `dcn401_resource.c` path I had spelled wrong, and both compared "same" — a
  **false "unchanged"** for files that simply do not exist. Absence must be
  tested with `git cat-file -e <rev>:<path>`, not by comparing `rev-parse`
  output.
- **`for f in $FILES` does not word-split in zsh.** This shell is zsh, and an
  unquoted expansion stayed one word, so a 13-file comparison silently ran as a
  single 300-character path. Use a `while read` loop.
- `fatal: expected 'acknowledgments'` during the fetch-all is a **transient
  remote error, not corruption** — `fsck --connectivity-only` over every
  top-level clone found no damage, only benign dangling commits in `agd5f-linux`
  and `akpm-mm`.

**`v7.3-rc6` is still not tagged** (torvalds tags stop at rc5) and
`next-20261003` does not exist — 2026-10-03 is a Saturday.

## Sweep 2026-10-03 (pre-rc6) — sirlucjan/cachyos refreshed; every delta a verified no-op

Run in advance of the rc6 tag expected 2026-10-04. `v7.3-rc6` is **still not
tagged** (torvalds tags stop at rc5; `origin/master` Makefile reads `-rc5`).
**Series stays at 255.**

### sirlucjan — refreshed, and the stale-HEAD trap fired again

Local `master` was at `445db953` while `origin/master` was `0f0dfad7`, hiding
three commits (*"Add 7.3-rc line"* for fixes/amd/cambyses). **Always read
`origin/<branch>`** — this is the second time this exact repo has hidden content
behind a stale local ref.

The 7.3-rc tree grew 76 → **93 directories**. Every one that intersects our
carries was checked against its content, not its version label:

| New dir | Verdict |
|---|---|
| `cachyos-fixes-patches-v7`, `-v8` | **No-op.** v8 is v6 plus exactly two patches: `13/14 mm/slub: refill prefilled sheaves from the barn` — **already ours as `2197`** — and `14/14 wireguard: preserve tstamp_type`, and `# CONFIG_WIREGUARD is not set` here. Patches 01–12 are identical to the v6 set we already triaged. |
| `hdmi-patches-v2` | **Rebase only, no content change.** A plain `diff` shows 70 changed lines, but those are entirely `From <sha>` headers and `@@` line offsets. Comparing **added/removed content lines only**: 124 vs 124, with **zero** lines unique to either side. v2 is v1 rebased onto a newer base. |
| `bore-dev-patches` | **Identical to our `2419`.** Both `linux7.3-bore7.0.0`; the diff bodies are byte-identical (1370 lines each). BORE 7.0.0 is current, and `bore-patches/` still carries the older 6.8.0. |
| `amd-iommu-patches` (11 patches, new) | **Rejected — wrong IOMMU mode.** The series adds PerfOpt and *"Force identity mode for selected GPUs only"*, and is aimed at **APUs in identity mode**. This machine is verified **not** in identity mode: `journalctl -k` reports `iommu: Default domain type: **Translated**`, there is no `iommu=pt` on the cmdline, and `lspci` shows **no Raphael iGPU at all** — only the Navi 48 card. This settles on evidence the earlier PerfOpt question that had rested on inference. |
| `xswap-patches-v3` | **Not applicable** — xswap was dropped deliberately on 2026-09-22 in favour of zswap + swapfile. |
| `poc-selector-dev-patches`, `cambyses-patches-v2` | **Competing scheduler designs** (*"introduce POC selector"*, *"Context-Aware Migration Balancer"*). This machine runs BORE; neither is a fix to it. |
| `aufs-patches`, `arch-patches-v2` | aufs (unused filesystem); a sysctl to disable unprivileged `CLONE_NEWUSER` plus another copy of the wireguard patch. |

### cachyos — unchanged

`7.3/base`, `/cachy`, `/fixes`, `/hdmi`, `/xswap` are all at the same commits as
the 2026-10-02 pass (`7.3/fixes` still `2d0a9e75fe41`). Nothing new.

### Version sweep — five remaining, all previously dispositioned

`2032` **left the list** and is now counted among the 19 content-identical
resends, which independently confirms the line-wrap finding made by hand on
2026-10-02. The five that remain are `2045` (v4 cover letters, no diff), the
three kbuild v4 that fail to apply to rc5, and `1151` (the older February
posting).

### New on-target work item: `#5807` — the open DCN4 flip-pending root cause

**`#5807`** *"[amdgpu] Pageflip timed out / CRTC flip_done timeout freezes KWin
Wayland (RX 9070 XT, RDNA4)"*, filed 2026-09-11, **updated 2026-10-03**. This is
our exact part (`1002:7550`, rev c0) with HDMI at 1080p and FreeSync forced
always, plus a second DP monitor — the closest match to this machine of anything
in the tracker.

It matters because it is the same family as the workaround our `README` already
documents: `dcdebugmask=0x800` covers *"the clock-gated HUBP flip-pending
misread: when the HUBP is clock-gated, `hubp2_is_flip_pending()` reports no
pending flip, so flip completion can arrive before the hardware latches"*. That
note ends *"drop it if a proper DCN4 flip-pending fix lands"* — **no such fix has
landed**, and the thread's newest note (2026-10-03) says only *"The cause is as
yet unknown."*

**Checked against this machine rather than assumed:**

- **No `flip_done timed out` and no `fbcon: Taking over console` anywhere in the
  journal** — the signature this issue is built on has never occurred here.
- **Neither HDMI output advertises VRR** (`vrr_capable` is empty for both
  `card1-HDMI-A-1` and `card1-HDMI-A-2`), which is the intended result of our
  `1164` MCCS fix. The reporter's suspected trigger is *"FreeSync forced always
  on"* — **that state is not active on this machine.**
- `amdgpu.dcdebugmask=0x800` is confirmed live on the running cmdline.

**Verdict: watch item.** It reinforces keeping `dcdebugmask=0x800` rather than
retiring it, and it is the thread to re-read if a DCN4 flip-pending fix is ever
posted. No action now.

### Tooling trap hit this pass

A comparison printed **"DIFF CONTENT IDENTICAL" while both `sed` invocations had
failed** — empty outputs compare equal, so the `&&` branch fired on nothing. Same
family as the `… | head && echo OK` rule already in `LESSONS.md`. Both
comparisons above were re-run resolving filenames with `find`, asserting the
extracted files were non-empty, and comparing **content lines only**. The BORE
result survived; the naive `diff` verdict on the HDMI series did not — it would
have reported a 70-line content change where there is none.

## Sweep 2026-10-03 (second pass) — Guittot's short-slice series assessed: rejected

Fresh refresh of every tree and all 17 lore mirrors, plus an assessment of the
linux-pm series the user linked. **Series stays at 255.**

### `[PATCH 00/18 v2] Improving latency of short slice tasks` (Vincent Guittot) — REJECTED

<20261002154415.2270586-1-vincent.guittot@linaro.org>, linux-pm, 2026-10-02.
Read from `repos/lore-linux-pm`; the lore web UI is Anubis-gated and was not
fetched. The linked `-1-` id is the **cover letter**.

The series has five parts: 1–2 decay positive lag, 3–5 use slice when selecting
CPU, 7–11 add a push callback for fair, 12–14 push short-slice tasks, 15–18 make
`feec`/EAS slice-aware.

**Four independent reasons, any one sufficient:**

1. **No review.** Every patch carries only the author's own `Signed-off-by`. No
   `Reviewed-by`/`Acked-by` anywhere in v1 or v2. Peter Zijlstra *did* engage the
   v1 `[PATCH 0/8]` on 2026-09-22 (patches 4, 5, 6 and 8) — but his replies are
   questions (*"Should this …"*), not tags. This is the case the adoption bar
   exists for: substantive maintainer discussion is not endorsement.
2. **It does not apply to rc5.** Spot-checked against a throwaway rc5 worktree,
   all three fail: 01/18 at `kernel/sched/fair.c:8019`, 03/18 at `:1116`,
   07/18 at `:9799`. It is written against a tree that already has the queued v1
   patches — the cover says *"The first 3 patches of v1 have been queued"*.
3. **Patches 15–18 are EAS/energy-model** (`energy_model.h`, `feec()`), which
   only activate on **asymmetric CPU capacity topologies**. This machine is a
   symmetric 8-core Zen 4 desktop, so that quarter of the series is inert by
   construction. The benchmarks were run on a **dragonboard rb5** (ARM
   big.LITTLE) using uclamp to *"target the high and mid cores"*.
4. **It is a feature, not a fix** — a latency optimisation series competing with
   the scheduler design this machine actually runs.

**On live-vs-inert, stated honestly rather than over-claimed:** BORE does *not*
replace everything here. It rewrites task *selection* and the slice in
`pick_next_task_fair`, so parts 1–2 and 12–14 (lag decay, short-slice push) are
EEVDF-internal and would land in BORE's shadow — the `0110` precedent, where the
CACHY hunk fell into a dead `#else` because BORE recomputes the slice. But parts
3–5 and 7–11 touch `wake_affine`/`select_task_rq_fair` and the load-balancing
push path, which **BORE does not replace**, so they would not be automatically
inert. The question is moot given (1) and (2), and it is recorded here so a
future pass does not have to re-derive it.

**Revisit only if** it gains `Reviewed-by` and rebases onto our base.

### tip has ~90 branches and `master` is not where all sched work lives

While locating the queued v1 patches, a `--grep` restricted to `origin/master`
found nothing. Searching **every** ref showed sched work on
`origin/sched/core` and the `origin/core/*` family that `master` does not
surface: `sched/eevdf: Always update slice protection`, `sched/eevdf: Take into
account current's lag when updating slice protection`, `sched/fair: Prevent
negative lag increase during delayed dequeue`, `sched/fair: Revert force wakeup
preemption`, `sched/fair: Limit run to parity to the min slice of enqueued
entities`, `sched/eevdf: Ensure that vprot will never go above a min slice`.
**These are EEVDF-internals fixes, and `fair.c` is live here under BORE** — but
membership in rc5 was not established this pass, so they are recorded as
**unresolved, not rejected**. That is the next thing to check.

### Fresh state

- `v7.3-rc6` **still not tagged** — torvalds tags stop at rc5.
- Mainline advanced `e767a4ea70a` → **`a74306e2e67`**.
- **tip unchanged** (`8f511d67b4fb`), **cachyos `7.3/fixes` unchanged**
  (`2d0a9e75fe41`), **sirlucjan unchanged** (`0f0dfad7`).
- `next-20261002` remains the newest linux-next.
- **Version sweep: identical again** — 19 content-identical resends, and the
  same 5 remaining (`2045` cover letters, the three kbuild v4 that fail against
  rc5, `1151`'s February posting).

### New work items

- **`#5931`** — *stack-protector panic in `dp_parse_link_loss_status` on the HPD
  RX IRQ*. A stack-protector panic is a buffer overflow, so this is a real
  memory-safety bug in the DisplayPort path. **Both displays here are HDMI**
  (`card1-HDMI-A-1`, `card1-HDMI-A-2`), so the DP link-loss path is not
  exercised — watch item, not a carry.
- **`#5932`** — shutdown hangs when a monitor is connected through USB-C. Not
  this machine's topology.
- `#5807` (the open DCN4 flip-pending root cause) remains the highest-value
  on-target watch item, as recorded in the previous pass.

### Tooling

A `--grep` over *all* tip refs matched unrelated commits — the pattern
`min slice` hit `drm/amd/display: Correct Slice reset calculation` across dozens
of branches, producing ~90 blocks of noise with ~6 real hits. **Anchor greps on
symbol names or exact subjects, not on short common words**, when scanning every
ref of a large tree.

## Sweep 2026-10-04 (rc day) — futex UAF is the candidate; EEVDF thread closed

Full refresh of every tree and all 17 lore mirrors. **Series stays at 255.**
`v7.3-rc6` is **not tagged yet** (master `6addb4f3855`); Sunday tags land later
in the day.

### The open EEVDF thread from yesterday is CLOSED — all in rc5

Resolved by commit *date* rather than by an ancestry walk (`merge-base` lies in
these shallow clones), then confirmed by content:

| Subject | Commit date |
|---|---|
| `sched/fair: Limit run to parity to the min slice of enqueued entities` | 2025-07-08 |
| `sched/fair: Revert force wakeup preemption` | 2026-01-23 |
| `sched/fair: Prevent negative lag increase during delayed dequeue` | 2026-04-23 |
| `sched/eevdf: Always update slice protection` | 2026-06-24 |
| `sched/eevdf: Ensure that vprot will never go above a min slice` | 2026-09-21 |

rc5 was tagged **2026-09-27**, so the last one is six days before it. Content
probe confirms it: rc5's `fair.c` has `se->vprot = min_vruntime(se->vprot,
vruntime + calc_delta_fair(slice, se));` at line **1154**, which is that commit's
whole change (1 insertion, 2 deletions upstream). **All five are in rc5 — nothing
to carry.** They appear as ancestors on ~90 tip refs because they are old common
history, which is also why the subject grep looked alarming.

### Candidate: `f35e3b578422` — futex private-hash use-after-free on resize

| | |
|---|---|
| Author | Chris Mason (Meta) |
| Trailers | **`Reviewed-by: Paul E. McKenney`**, `Signed-off-by: Peter Zijlstra (Intel)`, `Assisted-by: kres`, `Fixes: 56180dd20c19` |
| Status | **tip only** (2026-10-02) — not in mainline master |
| File | `kernel/futex/core.c` |

`__futex_pivot_hash()` publishes `mmph->batches` **before** swapping
`mmph->hash`. New grace periods can start in between, so `futex_ref_drop()` can
advance while a reader still holds the old hash — a use-after-free. The fix
swaps the two assignments and drops the now-unneeded `scoped_guard(rcu)`.

**Verified live in our tree, not assumed:**

- rc5's `kernel/futex/core.c:217-218` contains the buggy ordering verbatim:
  `mmph->batches = get_state_synchronize_rcu();` then
  `rcu_assign_pointer(mmph->hash, new);`
- `Fixes: 56180dd20c19` is dated **2025-07-10** — so this is **not** a 7.3
  regression; it has been latent for over a year, across every kernel since.
- Core kernel, reachable by any threaded program that resizes its futex hash.

**Disposition: hold for rc6, then carry if absent.** It clears the audit bar
outright (maintainer-signed *and* independently reviewed). It may well ride into
rc6 later today; if it does, the version bump absorbs it and no carry is needed.
Re-check at the moment the tag appears.

### Rejected / already covered

- **`drm/amdgpu/gmc12: properly pass flush_type to gmc_v12_0_flush_vm_hub()`
  (`0bfb1bfc82e8`) — MOOT for us.** The bug is real and present in rc5
  (`gmc_v12_0.c:330` still calls `gmc_v12_0_flush_vm_hub(adev, vmid, vmhub, 0)`),
  and it is our exact IP (`gmc_v12_0` = GC 12.0). But **our `1017` is part 14/16
  of the TLB-invalidation rework and deletes the entire function** the upstream
  patch edits — 211 removed lines from `gmc_v12_0.c`. The patch cannot apply to
  our series tree and the code it fixes does not exist after `1017`. Our
  `1008`/`1012`/`1013`/`1014`/`1017` carry `flush_type` through the new helpers.
  This is the mirror image of the `9007` duplicate trap: not "applies twice", but
  "looks like a fix for code our own series already replaced".
- **`drm/amdgpu/gfx12: set KMD_QUEUE for kernel gfx queues` (`9fe5745f9d8e`) —
  already in rc5** (content probe: `gfx_v12_0.c:3251` has the
  `REG_SET_FIELD(..., CP_HQD_PQ_CONTROL, KMD_QUEUE, 1)`).
- **Wrong-chip traps filtered from tip's 434 new commits**, by identifier rather
  than by subject: `sdma 7.1` (we are `sdma_v7_0`), `gmc_v12_1` (we are
  `gmc_v12_0`), `gfx6`, `gfx11` (we are `gfx_v12_0`), `drm/amd/pm/si`,
  `drm/radeon`, `switcheroo`-parked GPUs, `MacBookPro14,3`, `MST mode`
  (no MST here), and PWM backlight curves (desktop monitors).

### Sources with nothing on-target

- **torvalds**: 7 new commits, all EDAC `altera`/`versalnet` — SoC/FPGA hardware.
- **tip**: 434 new commits, overwhelmingly `x86/tdx`, bpf, `drm/mediatek`,
  Input and EDAC. The only on-target material is listed above.
- **New list postings since 2026-10-03** are the 38-part VMA-predicate refactor
  (Lorenzo Stoakes, v4) and an MGLRU RFC — **MGLRU is inert here** (LRU-MARIE
  owns reclaim, per the `2131`–`2137` finding), and the VMA series is a refactor
  with no fix content.
- One new posting worth a look next pass: **`drm/amdgpu: Fix double runtime PM
  put in amdgpu_debugfs_gpr_read()`** (dri-devel, 2026-10-04) — a refcount bug,
  though `amdgpu.runpm=0` is on this machine's cmdline, which may make the path
  unreachable. Not yet triaged.
- **Version sweep: identical for the fourth consecutive pass** — 19
  content-identical resends and the same 5 (`2045` cover letters, the three
  kbuild v4 that fail against rc5, `1151`'s February posting).
- **cachyos and sirlucjan unchanged** (`2d0a9e75fe41`, `0f0dfad7`).

## Sweep 2026-10-04 (work items + comments, freshly) — one strong lead

The rc-day pass had covered the trees, mirrors and version sweep but **not** the
tracker; this pass adds it. 24 issues updated since 2026-10-03, and the
`x-total: 24` / `x-total-pages: 1` headers confirm the full set was read rather
than page 1 of many.

**Commit shas in comment bodies: zero real ones.** The only two hex-looking
tokens were `548bbb036f76622de151dbd048b0ee73` (a GitLab `/uploads/` path from a
`dmesg` attachment) and `bea0000000000108` (a register value). Both were caught
by the verify-before-citing rule — a tracker full of image paths is exactly the
`112d2111f50a…` trap the skill documents.

### `#5759` — the lead, and it is our exact GPU

*`amdgpu/mes12: MES(0) intermittently fails to respond to REMOVE_QUEUE on Navi 48
(gfx1201), forcing MODE1`* — new substantive comment 2026-10-04 by `bkvargyas`,
on five Navi 48 parts (`1002:7551`, the AI PRO R9700 — ours is `1002:7550`, same
silicon family).

- **Signature:** `MES(1) failed to respond to msg=INVALIDATE_TLBS`, ~150 times
  since 2026-09-17, always while page tables are written at full speed.
- **Escalation:** three `INVALIDATE_TLBS` timeouts → `MES(0) failed to respond to
  msg=REMOVE_QUEUE` → *"MES might be in unrecoverable state, issue a GPU reset"* →
  `device lost from bus!` with SMU bus errors.
- **What does NOT change the rate:** MES firmware version (0x8b / 0x91 / 0x93),
  power draw (32–75 W as readily as 210 W), temperature, `vm_update_mode=3`,
  `ras_enable=0`.
- **What DOES:** **`amdgpu.mes_log_enable=1` — 0 timeouts in 24 four-card
  launches, against 6-in-6 with the default**, with identical launch time and
  throughput. Their read of `mes_v12_0.c` is that the only thing the flag
  changes toward firmware is `enable_mes_event_int_logging = 1` plus the
  `event_intr_history_gpu_mc_ptr` buffer in `SET_HW_RESOURCES`.

**This is the MES TLB-invalidation path, and we carry a whole TLB-invalidation
rework (`1008`–`1017`).** It also shares a family with the `#5910` note already
in this ledger (`amdgpu_vm_tlb_flush()` returning early on `!*fence`).

**Checked against this machine, and the result is a clean negative — see the
correction below for why the scoping matters.** Across the full 12-day, 26-boot
journal: `INVALIDATE_TLBS` **0**, `failed to respond to msg` **0**,
`device lost from bus` **0**, `unrecoverable state` **0**, `MODE1` **0**,
`ring … timeout` **0**, `GPU reset` **0**, `flip_done timed out` **0**.

**Disposition: watch, do not act.** `mes_log_enable` is available here (the
param exists and reads `0`), so the workaround is one cmdline token away if the
signature ever appears. It is **not** being adopted on the strength of one
reporter's 24 launches on different hardware in a vfio/passthrough topology —
that is a measurement, not a review, and we have never reproduced the fault.

### Other on-target items from the same pass

- **`#5934`** (filed today) — DCN 4.0.1, RX 9070 XT: `enabling link 3 failed: 19`
  plus `CRB Config Warning: DET size (3,14,8,0) + Compbuf size (1) > CRB segments
  (21)`, white-noise static over **HDMI 2.1 FRL + DSC at 4K120 with VRR/ALLM**.
  Our display block, but not our configuration — both displays here are 1080p,
  under HDMI 2.0 rates, and neither advertises VRR. Watch item.
- **`#5935`** (filed today) — RX 9070 XT, `1002:7550` rev c0: raising
  `power1_cap` after a `pp_od_clk_voltage` commit silently reverts the voltage
  offset. Our exact part, but it is an overclocking/undervolting interaction we
  do not exercise. Watch item.
- **`#4753`** — `gfx1201` display pipeline stall on memory clock change with
  FAMS2 (100 notes, active). Our exact IP. No fix: fililip notes FAMS2 on RDNA4
  *"just never works as well as FAMS1"*, everything reports healthy (no
  underflows, no DMUB errors), and suspects a coordinated firmware+kernel fix.
  Watch item.

### CORRECTION: `journalctl -k` is boot-scoped, and I had been treating it as global

**`journalctl -k` implies `-b`.** The man page states `--dmesg` is equivalent to
`--boot --dmesg` — so every "this machine has never logged X" conclusion drawn
from `journalctl -k` in this session was scoped to **the current boot alone**.
On this pass that was a **39-minute window** (the box rebooted at 12:34), and
earlier passes were no better. The claims were stated with more confidence than
the evidence supported.

Re-run against the **whole journal** — `journalctl --no-pager | rg …`, no `-k` —
the picture is Sep 23 14:14 → Oct 04 13:13, **26 boots, 1,002,265 lines**, and
the negatives above are now genuinely cross-boot. The conclusions did not change;
the evidence now actually supports them. Two further traps hit in the same
sequence:

- **`rg -i 'mes'` matched `names`, `frames`, `timestamps`, `Estimated`** — it
  reported "17 MES lines" where the word-boundary probe finds **2**. Anchor on
  `\bMES\b`, not on a short case-insensitive substring.
- **`… | tail -8 || echo "none"` cannot report absence** — `tail` exits 0 on
  empty input, so the fallback never fires. Same family as the `… | head && echo
  OK` rule already in `LESSONS.md`.

`/var/log/journal` exists with `SystemMaxUse=500M`, so the history **is** there —
the scoping was mine, not the journal's.

## Sweep 2026-10-04 (second pass) — the drm-next-7.4 AMD pull, assessed

Fresh refresh of every tree and all 17 lore mirrors, plus an assessment of the
pull the user linked. **Series stays at 255.** `v7.3-rc6` is **still not tagged**
(master `6addb4f3855`).

### `[pull] amdgpu, amdkfd, radeon drm-next-7.4` (Alex Deucher, 2026-10-02)

<20261002175316.1428352-1-alexander.deucher@amd.com>, read from
`repos/lore-dri-devel` / `lore-amdgfx`; the lore web UI is Anubis-gated and was
not fetched. Tag `amd-drm-next-7.4-2026-10-02`, head `41505ac433cc`, built on
`2abe8e7e339` — which is **exactly where our `drm-next` clone still sits**, so
Dave Airlie has not merged it yet.

**This is 7.4 merge-window material, and our base is 7.3-rc5.** Nothing in it is
carryable now: porting 7.4 driver code onto a 7.3 base is the wrong-base case the
ledger has rejected repeatedly. It is recorded here as the thing to re-read when
7.4 becomes the base.

I fetched the tag (bounded, `--depth=200`) and inspected the commits rather than
judging by the summary. **175 commits: ~20 on-target, 31 confirmed wrong-chip**
(recorded below so a future pass does not re-litigate them).

**Three clusters matter, and two map onto open work items from yesterday:**

| Cluster | Commits | Links to |
|---|---|---|
| MES / userq reset | `mes12: restore collateral gfx queues after pipe reset`, `mes12: read the gfx user queue VMID for MMIO reset`, `gate gfx pipe reset on PER_PIPE`, `userq: fix reading the WPTR at a non-zero BO offset`, `userq: preserve kernel rings during gfx pipe reset`, `userq: reject mappings without a backing BO` | **`#5759`** — the MES `REMOVE_QUEUE` / `INVALIDATE_TLBS` MODE1 escalation |
| HDMI FRL | `Serialize HDMI FRL status polling against link detect`, `Skip HDMI FRL status polling while link is down`, `Fix HDMI2.2 LT timeout duration`, `Default HDMI RGB output to limited range on CTA modes` | **`#5934`** — the DCN 4.0.1 `enabling link 3 failed: 19` FRL report |
| `mes_dbgext` | `add mes_dbgext core support`, `update MES v11/v12 API for mes_dbgext`, `wire mes_dbgext on gfx11 and gfx12` | Likely the *proper* upstream mechanism behind `#5759`'s `mes_log_enable=1` workaround |

**Every one of the seven spot-checked on-target commits carries a `Reviewed-by`
from an AMD maintainer, and NONE carries `Cc: stable`.** That is the decisive
detail: there is no backport path into 7.3.y, so none of this reaches our line
except by a 7.4 rebase.

Also present: **our `1074`** (`drm/amdgpu: implement workaround for sdma dcc
corruption`) — a third confirmation it is upstream — and the `gmc12 flush_type`
fix already established last pass as **moot here** (`1017` deletes that function).

**Disposition: no action. Re-read at the 7.4 rebase.** The two clusters are the
strongest argument yet that `#5759` and `#5934` have real upstream work behind
them; if either fault ever appears on this machine, the fixes exist, just not on
our line.

### Everything else

- **Version sweep: identical for the fifth consecutive pass** — 19
  content-identical resends and the same 5 (`2045` cover letters, the three
  kbuild v4 that fail against rc5, `1151`'s February posting).
- **cachyos (`2d0a9e75fe41`) and sirlucjan (`0f0dfad7`) unchanged.**
- Wrong-chip commits recorded from this pull, by identifier not subject:
  `mmhub v5_0_1`, `sdma 7.1`, `gmc_v12_1`, `GC 12.1.0 A0`, `vpe v3.0`, `dcn60`,
  `PSP 15.0.3`, `nbif v7_10`, `lsdma v8_0_1`, `SI DPM`, `DCE 6`/`DCE 8.1`,
  `MacBookPro14,3`, `Sun XVR-300`/Sparc64.

## Question answered 2026-10-04: what would rebasing to linux-next give us?

`next-20261002` (`d64fba75362e`) vs our base `v7.3-rc5` (`72d3fcf802c`). rc5 **is**
an ancestor of the snapshot, so the trees diff directly — but the linux-next
clone is `--depth=1`, so `rev-list <range>` returns **1** and commit counts are
unavailable. **Tree diffs work; commit ranges do not.** Use `git diff <sha1>
<sha2> -- <path>` here, never a range.

### What we would gain, verified by content probe

| Item | In next-20261002? |
|---|---|
| `af2fb3ee667` slab kswapd deadlock (our pending `2198`) | **YES** — both `Don't wake up kswapd, it will cause deadlock under pi_lock` hunks present (`mm/slub.c:6093`, `:6281`) |
| Our `1074` SDMA DCC workaround | **YES** — `num_move_entities = 1` present, so `1074` would become a drop |
| io_uring `CQE32`/`CQE_MIXED` fixes | **YES** — `CQE_MIXED` ×5, `big_cqe` ×14 |
| 7.4 amdgpu MES/userq + HDMI FRL clusters | **YES** (the 792-file batch) |

**Scale of the change:** `drivers/gpu/drm/amd` **792 files**, `arch/x86` 175,
`mm` 106, `kernel/sched` 21, `io_uring` 21, `block` 14, `drivers/nvme` 13,
`r8169` 2.

### What it would NOT give us

**The futex UAF fix (`f35e3b578422`) is absent** — `kernel/futex/core.c` is
**byte-identical** between rc5 and next-20261002. The one genuinely live bug
found this cycle would still have to be carried.

### The cost, now quantified

**73 of our 255 patches touch an amdgpu file that changed in that window** —
29% of the series needs rebase work in amdgpu alone, before the CachyOS squashes
and the other subsystems are counted.

### Verdict

**Not worth it now.** Almost everything a rebase would hand us is either already
carried and working (`1074`, `2046`, `2048`, `2049`, the io_uring set) or
destined for our line anyway via rc6 / 7.3.y. The genuinely new content is 7.4
**feature** work — 792 amdgpu files of new silicon support (SMU 15, MMHUB 5.0,
VCN/VPE 3.0, GC 12.1, DCN 6) aimed at hardware this machine does not have — and
it replaces a stabilised rc line with a daily-rebuilt preview, which `CLAUDE.md`
reserves for when the RC line is unusable. The right next base is **rc6**.

## Checked 2026-10-04: MGLRU-FG RFC v3 — inert here by construction

`[PATCH RFC v3 04/17] mm/mglru: frequency guided workingset promotion (MGLRU-FG)`
— Kairui Song (Tencent) via B4 Relay, to linux-mm, 2026-10-03,
<20261003-mglru-fg-v3-4-cbd4546a5bd9@tencent.com>. Read from `repos/lore-mirror`;
the lore web UI is Anubis-gated and was not fetched.

It complements MGLRU's eviction-time tier-PID protection with access-time
frequency-guided promotion, reworking the `refs` count in folio flags
(`LRU_REFS_REFERENCED/WORKINGSET/PROTECTED/MAX`), folding `PG_workingset` and
`PG_referenced` into the low two bits of `refs`. Touches
`include/linux/mm_inline.h`, `include/linux/mmzone.h`, `kernel/bounds.c`,
`mm/folio.c`, `mm/vmscan.c`, `mm/workingset.c`. Only `Signed-off-by` — no
review. **RFC, v3 of 17 parts, still under discussion.**

**Verdict: reject. Three independent reasons, and the third is structural.**

1. **RFC** — explicitly not proposed for merging.
2. **MGLRU-only** — the cover states *"This doesn't affect classical LRU in any
   way"*, so nothing here reaches the LRU path this machine uses.
3. **The MGLRU path is inert here, verified rather than recalled.** Our `2101`
   (LRU-MARIE 0.11.1r2) **renames `lru_gen_enabled()` to
   `lru_gen_core_enabled()`** and introduces a masking `lru_gen_enabled()` that
   additionally returns false whenever Marie owns aging. Our own patch comment:
   *"Marie and MGLRU are mutually exclusive at runtime. When Marie owns aging,
   every MGLRU code path must be inert... Reporting MGLRU as disabled here makes
   'both managers touch the same folio' structurally unrepresentable."* The live
   kernel confirms Marie is the active manager (`Marie LRU 0.11.1 by Masahito
   Suzuki`).

**The trap this sits on, worth restating:** `/sys/kernel/mm/lru_gen/enabled`
reads **`0x0007`** on this machine — the tunable is present, readable, and says
MGLRU is enabled, while the masking makes every MGLRU path inert. This is the
same shape as the `vm.swappiness = 180` finding: **a readable knob is not
evidence that it is consulted.** That is why the `2131`–`2137` batch was removed
on 2026-09-23 and why this RFC is rejected on inertness rather than on quality.

## Work items, 2026-10-04 (fresh)

**15 issues updated; `x-total: 15`, `x-total-pages: 1` — the full set.**

New/updated on-target:

- **`#5872`** (today, 17:17) — *RX 9070 XT (Navi 48) over USB4: pageflip timeout
  when set as primary display*. Our GPU, and a pageflip-timeout family — but
  over USB4/eGPU, which is not this machine's topology. Watch.
- **`#5902`** (updated today 12:46) — *HDMI FRL: same-sink HPD pulse leaves the
  display dark after the destructive verify*. Previously CC-only; now re-updated.
  HDMI is our display path, so this stays on the watch list.
- `#5934` (DCN 4.0.1 HDMI FRL / `enabling link 3 failed: 19`), `#5935` (SMU
  14.0.2 power cap), `#5917` (RX 9070 XT `comp_1.0.1`), `#5759` (MES
  `REMOVE_QUEUE`), `#4753` (`gfx1201` FAMS2 stall) — all previously triaged,
  no change in disposition.
- `#5939` (DCN 3.5 Strix panel replay), `#5938` (gfx1152), `#5937` (Granite
  Ridge iGPU), `#5936`/`#5751`/`#4843`/`#5005`/`#3659` — other silicon.

## Rebase to v7.3-rc6 — 13 of 255 patches need resolution (AWAITING APPROVAL)

Base `v7.3-rc5` (`72d3fcf802c`) → `v7.3-rc6` (`4eeccbed21e`, tagged 2026-10-04).
Tag verified by control: `git.kernel.org/torvalds/t/linux-7.3-rc6.tar.gz` 301→**200**,
against rc9 301→**404**. PKGBUILD bumped `_rcver=rc6`, `pkgver=7.3.0_rc6`,
`pkgrel` 5→**1** (the reset convention: rc3→rc4 was 26→1, rc4→rc5 18→1),
`_srctag`/`source=()` to rc6.

Cumulative audit (`audit_series.py --tag v7.3-rc6`) reports **13 of 255 failing**:
9 inert `Skipping patch`, 4 `FAILED`.

### Drop candidates — 9, content-verified present in rc6

| # | Patch | Evidence |
|---|---|---|
| `1074` | drm-amdgpu-workaround-for-sdma-dcc-corruption | 4/4 added lines in rc6; landed as agd5f `c1702ed0d64a` |
| `1162` | dc_state_create_copy NULL check in dm_suspend | 5/5 |
| `2010` | blk-cgroup save IRQ state in blkg_tryget_closest | 3/3 |
| `2016` | nvme-multipath ANA log bounds | 3/3 |
| `2041` | net gso limit recursive ip-in-ip | 10/10 (already on the agreed drop list) |
| `2046` | blk-mq set RQF_USE_SCHED | 22/22; landed as `ab6c756f28c` |
| `2047` | blk-mq allow cached requests for flush ops | the 2 lines it **deletes** are gone from rc6 (0 occurrences) — the change is in |
| `2048` | io_uring init task context before BPF loop | 1/1; landed as `a3bdf68feec` |
| `2151` | mm shmem ignore sysfs configs for forced collapse | 1/1 (already on the agreed drop list) |

`2041` and `2151` were already signed off. **The other seven await explicit approval** —
`CLAUDE.md` YOU MUST NOT #8.

### Regenerate — 4

| # | Patch | Why |
|---|---|---|
| `1007` | gmc12: disallow gfxoff around TLB flushes | 0/4 added lines in rc6 — genuinely drifted (part 04/16 of the TLB-inv series) |
| `1017` | gmc12: switch to new gmc tlb inv helpers | 0/3 — genuinely drifted (part 14/16) |
| `2049` | io_uring SQPOLL task_work RCU | its two distinctive added lines (`struct task_struct *task = tctx->task;`, `__set_notify_signal(task);`) are **absent** from rc6 — our carry may be a different revision than what landed; needs care, not a blind drop |
| `2311` | kbuild: move toolchain checks into init/Kconfig.toolchain | `init/Kconfig.toolchain` **does not exist in rc6** |

### Two probe errors caught in the process — both would have caused a wrong drop

- **`2311`'s content probe read 99% (116/117 lines "present") and was wrong.** The patch
  *moves* lines from `init/Kconfig` into a new file, so every added line already
  exists at the source location and the probe counted it as "upstream". Verified
  properly by testing for the **created file**, which is absent. **A content probe
  cannot distinguish "this line is new here" from "this line already lives
  elsewhere"** — for any patch that moves code, probe the created artefact, not
  the lines.
- **`2047` reverse-applies *failing* while its content is plainly present.** This is
  the documented trap in the direction the ledger had not recorded: rc6 has **zero**
  occurrences of the two lines it deletes, so the change is in — but `--check -R`
  fails because the surrounding context moved underneath it. Reverse-apply is
  unreliable in *both* directions, exactly as `CLAUDE.md` warns.

## Sweep 2026-10-05 — nothing to adopt; three of our carries appear in the 7.4 amd-pstate pull

Full refresh (trees + all 17 lore mirrors), version sweep, and the trees the
user named. **Series stays at 255.**

### Version sweep — no patch of ours has a new version

**Sixth consecutive identical pass**: 17 mirrors, 255 carries, **19
content-identical resends**, and the same 5 needs-look entries, all previously
dispositioned — `2045` (v4 cover letters, no diff), `2302`/`2308`/`2314` (kbuild
v4, fail against both rc5 and rc6), `1151` (older February posting).

### The `[GIT PULL] amd-pstate 7.4 content (10/4/26)` — and our overlap with it

Mario Limonciello, linux-pm, 2026-10-04 (`5a3fc9d654`), tag
`amd-pstate-v7.4-2026-10-14`, head `6b64d65c8368` — **not merged yet** (absent
from our linux-pm clone; only its base `c8663e0457e6` is present). Ten patches
across `arch/x86/kernel/acpi/cppc.c`, `drivers/cpufreq/acpi-cpufreq.c`,
`amd-pstate.c`, `amd-pstate.h`, `amd-pstate-ut.c`.

**Three of the ten are already ours** — we adopted them from the list before the
pull was assembled:

| Upstream (7.4 pull) | Our carry |
|---|---|
| `cpufreq/amd-pstate: Skip auto_sel write when it already matches the mode` (Wentao Guan) | **`1230`** |
| `cpufreq: amd-pstate: Restore previous mode when changing driver mode fails` (Mario) | **`1231`** |
| `cpufreq: amd-pstate: Propagate cppc_set_auto_sel() errors on mode change` (Mario) | **`1232`** |

The rest: `Fix TOCTOU when changing driver mode via sysfs`, `ACPI: CPPC: Refactor
boost ratio handling`, `acpi-cpufreq: Use amd_get_boost_ratio()`, `Get Highest
Freq for a CPU`, `Restore previous EPP if profile_name allocation fails`, plus
**two Zen6-only** entries (`amd-pstate-ut: Fix max_freq and EPP test failures on
Zen6`, `Update Zen6 client EPP tuning values`) which do not apply to Zen 4.

**Our `1227` is adjacent but not the same layer.** It is
`[PATCH v7 18/20] ACPI: CPPC: Accept requests to retain immutable autonomous
selection` — the **CPPC-level** fix at `arch/x86/kernel/acpi/cppc.c`. The pull's
TOCTOU patch is the **amd-pstate-level** fix. Worth a deliberate comparison at
the 7.4 rebase rather than assuming one subsumes the other.

**Disposition: nothing to adopt now.** It is explicitly *"content for 7.4"*, our
base is rc6, and the three overlapping carries are already in.

### Trees — nothing on-target

- **tip: 0 new commits** since `f191df9f71d2`.
- **linux-pm: nothing new** in the tree (`100638f0f`, 2026-10-01); the pull above
  is on the list, not yet merged.
- **akpm-mm: 14 new commits**, none matching the on-target filter.
- **linux-next: `next-20261002` remains the newest** (dated **2026-10-03**).

**A silent failure caught here.** `git -C repos/linux-next diff --name-only
4eeccbed21e next-20261002` returned **0 files**, which reads as "nothing
changed". It was a **failed lookup**: rc6 (`4eeccbed21e`) is **absent from the
linux-next clone**, and geometrically so — the snapshot is dated 2026-10-03 and
rc6 was tagged 2026-10-04, so **the snapshot predates the tag**. Re-run against
rc5 (a genuine ancestor) the delta is real: **792 amdgpu files, 175 x86, 106 mm,
21 sched, 21 io_uring, 14 block, 13 nvme, 2 r8169**. `2>/dev/null` is what made
"bad revision" and "no differences" indistinguishable.

### Work items — 19 updated, full set (`x-total: 19`, `x-total-pages: 1`)

- **`#4960`** *(20 notes, updated 2026-10-05)* — *Excessive power consumption due
  to low default driver GPU load targeting*. On this GPU family: amdgpu raises
  core clocks to hold ~70 % GPU load, so a frame-capped game draws ~220 W for no
  frame-rate gain. Long-running (since 2026-02), newest note contrasts Linux
  behaviour with Windows' fixed 85 % target. Behavioural, no patch.
- **`#5902`** — the reporter **corrected their own environment**: "connected
  directly" was actually through a **5 m HDMI-powered active optical cable**, and
  re-running on 1.5 m passive copper with a `c953b39f9487` backport changed the
  picture. **`c953b39f9487` verified as a real commit** —
  `drm/amd/display: Reintroduce "Force validation link training on all ASICs"`
  (2026-06-11), present in tip and linux-next. Not an upload path; the
  verify-before-citing rule was applied and passed.
- New since the last pass: `#5940` (firmware brightness curve steps near 0 %),
  `#5669` (Navi 44 T-Bar eGPU), `#4333` (Valve Index HPD). Other silicon.
- `#5934`, `#5935`, `#5917`, `#5872`, `#5759`, `#4753` — unchanged dispositions.

### Mailing lists — nothing on-target

`drm/rockchip` dw-hdmi-qp v12 (Rockchip), `net/sched: cls_bpf`, and
`sched_ext/for-7.4: Add NUMA balancing support` — **sched_ext is inert here**
(BORE owns scheduling; `kernel/sched/ext/` is the dead path, per the
2026-09-30 inversion). Two mm postings worth a look next pass:
`mm/page_alloc: skip shuffling and reporting for no-lock frees` and
`mm: vmscan: don't count per-node proactive reclaim as memory pressure`.

### Docs gate caught a real omission

The `commit-gate.sh` hook blocked a command because `docs/README.md` still said
base `7.3.0_rc5-5` after the PKGBUILD was bumped to `7.3.0_rc6-1`. **The gate was
right** — a bump is not complete until the docs agree. Corrected the base version
and the "mainline Linux 7.3-rc5" line in `docs/README.md`. The only remaining
`rc5` string is a *historical* CHANGELOG entry describing the rc4→rc5 bump, which
is correct as written.

## Duplicate audit against rc6 — no silent duplicates found (2026-10-05)

The rebase audit only reports the 13 patches that *fail*. `CLAUDE.md` records the
opposite trap: **a patch can apply cleanly while its content is already upstream,
inserting a second copy** (`9007` programmed `DB_RING_CONTROL` twice). So all 255
carries were scanned against rc6 for content that is already present.

### Method, and why the first pass over-reported

**Pass 1 — added-line presence.** 207 patches clean, **35 with ≥70 % of added
lines already in rc6** (many at exactly 100 %), 13 with no testable content.

That number is not trustworthy on its own: a check for "does this line exist in
the target file" matches a line that *legitimately lives elsewhere in the same
file*. `1166` (a 1-line change), `9019`, `1056`, `1018`, `0034` and others were
100 % on this test and are not duplicates.

**Pass 2 — hunk post-image.** For each suspect, build the hunk's post-image
(context + added lines) and require it to appear as a **contiguous block** at the
patched location. This dropped most of the 35 to "genuinely new" and left **8**:

| Verdict | Patches |
|---|---|
| DUPLICATE, already known drops | `1074`, `1162`, `2010`, `2016`, `2041`, `2046`, `2048`, `2151` |
| **newly flagged** | `2026` |

### `2026` is a FALSE POSITIVE — and the reason generalises

`2026-io_uring-drop-files-buffers-at-release.patch` **moves**
`io_sqe_buffers_unregister()` / `io_sqe_files_unregister()` from
`io_ring_ctx_free()` to `io_ring_ctx_wait_and_kill()`. The post-image block is
found in rc6 **at the original location**, so the test called it a duplicate.

**Neither the added-line test nor the post-image test can distinguish "already
upstream" from "this patch moves code."** Both see the lines present. This is the
same failure that made `2311` read 99 % earlier in the same session, and it is
the third distinct spelling of one underlying error: **a content probe answers
"does this text exist", never "is this change already applied."** For move/refactor
patches only the structural test is valid — does the created artefact exist, or
does the source location still hold the code.

After resolving `2026`, **the duplicate set is exactly the 8 the audit had already
identified, of which 7 are proposed drops and `1162` is confirmed below. No silent
duplicates exist in the series against rc6.**

### The `drm-fixes-7.3` pull — the one for OUR line, found on this pass

The user linked the **drm-next-7.4** pull. There is a second, more relevant one:
**`[pull] amdgpu, amdkfd, radeon drm-fixes-7.3`**, Alex Deucher, 2026-10-01,
`<20261001230115.1319089-1-alexander.deucher@amd.com>`, tag
`amd-drm-fixes-7.3-2026-10-01` — **fixes for the 7.3 stream, which is our line**.

25 commits, cross-checked against all 255 carries by subject. **Exactly two match:**

- `Jiangshan Yi — drm/amd/display: check dc_state_create_copy() for NULL in dm_suspend` → our **`1162`**
- `Pierre-Eric Pelloux-Prayer — drm/amdgpu: implement workaround for sdma dcc corruption` → our **`1074`**

Both are already in the proposed drop set, **and this independently confirms
`1162`**: the rebase audit and the added-line test both said "already upstream"
while the post-image test said "genuinely new" (0/2 hunks). A named entry in the
7.3 fixes pull is the third and decisive signal. **`1162` drops.**

The other 23 commits in the pull are either not carried by us, wrong-chip
(`DCE 6.x`, `DCE 8.1`, `SI DPM`, `MacBookPro14,3`, `radeon`, `gfx11`, `sdma 7.1`,
`gmc_v12_1`), or already accounted for (`gfx12 KMD_QUEUE` is in rc5; the
`gmc12 flush_type` pair is moot because our `1017` deletes that function).

**Disposition: no change to the drop set. `1074` and `1162` confirmed; no new
drops, no regenerations added.**

### Rebase COMPLETED — all 245 patches apply cleanly to v7.3-rc6

Resolution of the 13 failures above:

- **10 dropped** (content-verified present in rc6): `1074`, `1162`, `2010`, `2016`,
  `2041`, `2046`, `2047`, `2048`, `2049`, `2151`.
- **3 regenerated**: `1007` and `1017` by one-token context rebase
  (`gmc_v12_0_flush_vm_hub(..., 0)` → `flush_type`, the 7.3 fixes pull changed it);
  `2311` rebuilt because rc6 inserted a `CC_OPT_INLINE_MEMSET` block inside the
  region it rewrites.
- `2049` was listed for regeneration but on inspection **was already upstream** —
  rc6 has both halves (`guard(rcu)()` in `io_req_normal_work_add()` and
  `IORING_SETUP_DEFER_TASKRUN | IORING_SETUP_SQPOLL` in the `synchronize_rcu()`
  condition). Only the *comments* differ, which is why reverse-apply **and** the
  added-line probe both missed it. Read the code, not the diff.

Final audit: **`OK: all 245 patches applied cleanly to v7.3-rc6.`**
Both `git apply --check` and `patch -p1 --dry-run` accept the regenerated `2311`.

Built `7.3.0_rc6-1` and verified: `.BTF` + `.BTF_ids` present in the vmlinux,
`CONFIG_TCP_CONG_BBR` **not set** with `CONFIG_TCP_CONG_BBR3=y` (the kfunc
collision avoided), `CONFIG_SCHED_BORE=y`, `CONFIG_LRU_MARIE=y`, built-in cmdline
unchanged. Installed and boot entries regenerated; default entry
`linux-sleepy-next.conf`.

## Activity check 2026-10-05 (post-bump) — nothing actionable

Run after the rc6 rebase landed (`483ca42`). Trackers, branches and lists all
checked.

### Work items — 11 updated, full set (`x-total: 11`, `x-total-pages: 1`)

- **`#5776` (new today) — poweroff/reboot hang, deadlock between
  `amdgpu_dm_ism_disable()` and `dm_ism_delayed_work_func`.** `dm_suspend` held
  the ISM mutex across `disable_delayed_work_sync()` while the pending work func
  tried to take the same mutex. Ray6161 confirmed today it is *"included in DC
  3.2.383 release and upstream Linux v7.2 kernel"*.

  **Verified present in rc6, not assumed.** rc6's `amdgpu_dm.c` carries the fix
  with its explanatory comment at **both** call sites — line 873 and line 1576:
  *"Quiesce workers first without dc_lock (they take dc_lock themselves, so
  syncing under it would deadlock)"*, followed by `amdgpu_dm_ism_disable()`
  outside the lock and `amdgpu_dm_ism_force_full_power()` inside it. **No action.**

  The sha in that thread (`dc9fed0990ae77f74b79b8b13ebb9110`) is an **`/uploads/`
  path** for the attached patch, not a commit — caught by the verify rule.

- **`#5872` — RX 9070 XT (Navi 48) over USB4, pageflip timeout as primary
  display.** New comment today: superm1 had suggested retesting on 7.3-rc4+ citing
  `63e19ef3ddab806c472748c825f4dc88dcd994e8`; **the reporter retested on mainline
  7.3-rc5 and it still reproduces**, now on Fedora 44 KDE rather than SteamOS, so
  Valve's out-of-tree patches are ruled out. `63e19ef3ddab` **verified as a real
  commit** (`drm/amd/display: Atomize IRQ register read/modify/write ops`,
  2026-08-25, present in torvalds/tip/agd5f/linux-next). **Not this machine's
  topology** (eGPU over USB4) — watch only.

- **`#5902` — HDMI FRL.** The reporter corrected their own environment again: the
  "direct" connection was a **5 m HDMI-powered active optical cable**, and they
  re-ran on 1.5 m passive copper with `amdgpu.hdmi_hpd_debounce_delay_ms=5000`
  and the `c953b39f9487` backport. `c953b39f9487` is a real commit
  (`Reintroduce "Force validation link training on all ASICs"`, 2026-06-11).

- `#5940`, `#5939`, `#5776`-adjacent, `#5751`, `#5669`, `#4960`, `#4843`,
  `#4333`, `#3659` — other silicon or unchanged.

### Branch activity — none

Every relevant branch is at the same commit as the pre-bump pass:

| Tree | Branch | Last commit |
|---|---|---|
| agd5f-linux | `drm-fixes-7.3` | 2026-09-24 |
| agd5f-linux | `drm-next` | 2026-09-23 |
| agd5f-linux | **`tlb_inv_rework`** | 2026-09-11 |
| agd5f-linux / amd-staging | HEAD | 2026-09-30 |
| drm-next | `drm-next`, `drm-next-tip` | 2026-09-26 |
| tip | `sched/urgent`, `sched/core` | 2026-09-22 |

Worth noting for a future pass: agd5f carries a **`tlb_inv_rework`** branch —
*"drm/amdgpu/gmc12: use MES or SDMA for pasid TLB invalidation"* — which is the
same territory as our `1008`–`1017` carries. It has not moved since 2026-09-11,
so there is nothing to sync, but if it advances it is the first thing to diff
against `1017`.

### Mailing lists — nothing on-target

- **amd-gfx: 1 message** since 2026-10-04 (a `dcn_optc_lock_unlock_state`
  trace-event patch). Effectively silent.
- **dri-devel: 155 messages**, all off-target — dma-buf heaps/CMA, `drm/armada`,
  `media: tegra-vde`, the `rockchip` `dw-hdmi-qp` v12 series, Intel `accel/ivpu`,
  Novatek/Synaptics panels, Qualcomm `msm/dpu`, `fastrpc`.
- **No thread in amd-gfx, dri-devel or linux-pm names any of this machine's IPs**
  (Navi 48, gfx12, DCN 4.0.1, SMU 14, PSP 14, SDMA 7, VCN 5, or the
  dcc/tlb/mes/userq/hdmi/flip families) since 2026-10-03.

## Full work-item enumeration 2026-10-05 — all 1855 open issues, not just recent

The `updated_after` filter only sees *recent* activity; the tracker is ~1855 open
issues across 19 pages and an older issue updated months later is invisible to
it. Enumerated the **entire set**: 19 pages, **1855 issues fetched, matching
`x-total: 1855` / `x-total-pages: 19` exactly** — no truncation.

- **165 issues name this machine's exact silicon** (Navi 48 / gfx1201 / `1002:7550`
  / RX 9070 / DCN 4.0.1 / SMU 14 / PSP 14 / SDMA 7.0 / VCN 5.0 / Granite Ridge).
- 436 more fall in the broader families that could touch us (flip_done,
  pageflip, FRL, VRR, DCC, userq, MES, TLB, HDMI, MODE1, suspend).

### What the full enumeration found that the recency filter had missed

**`#5870` — `amdgpu_sync_add_later` use-after-free (RX 9070 XT, 7.2.6).** Updated
2026-09-20, so it never appeared in any `updated_after=2026-10-xx` pass. A
commenter pointed at a mailing-list fix:

> `[PATCH] drm/amdgpu: don't release the fence reference consumed by the
> scheduler` — Donggeun Yoo, dri-devel, 2026-09-10,
> `<20260910035531.559908-1-donggeunyoo.kernel@gmail.com>`

**Three `Fixes:` tags**, including `c1c4a8b21721 ("drm/amdgpu: grab extra fence
reference for drm_sched_job_add_dependency")`. It removes a `dma_fence_put()` on
the error path after `drm_sched_job_add_dependency()` — which is claimed to
**consume** the reference — across `amdgpu_cs.c`, `amdgpu_sync.c` and
`amdgpu_vm_sdma.c`.

**Two things verified:**

1. **The bug is live in rc6, and therefore in what we just built.** rc6
   `amdgpu_cs.c:1303-1309` still reads:
   ```c
   fence = &p->jobs[i]->base.s_fence->scheduled;
   dma_fence_get(fence);
   r = drm_sched_job_add_dependency(&leader->base, fence);
   if (r) {
           dma_fence_put(fence);      /* <- the subject of the fix */
           return r;
   }
   ```
2. **The patch applies clean to rc6** — both `git apply --check` and
   `patch -p1 --dry-run`.

**Not adopted, and deliberately so.** It clears the *technical* bar (real bug,
live in our tree, applies cleanly, three `Fixes:` tags) but **fails the review
bar: zero replies on the list, no `Reviewed-by`, no `Acked-by`** — only the
author's `Signed-off-by`. Our bar is maintainer-applied, maintainer-signed, or
≥1 Reviewed-by. The patch's whole correctness rests on one claim — that
`drm_sched_job_add_dependency()` consumes the fence reference — and **that claim
was not independently verified this pass**; if it is wrong, removing the put
*leaks* a reference instead of fixing a double-put. Carrying an unreviewed
ownership change into the GPU submission path on the strength of one commenter's
"it applies cleanly" is precisely the mistake this ledger exists to prevent.

**Revisit if it gains a `Reviewed-by`.** It is a strong candidate the moment
someone signs off on it.

### Other items the full pass surfaced

- **`#5894` — RX 9070 XT (VCN 5.0.0) ring reset never recovers.** Our VCN.
  Resolved as a **firmware** bug: nowrep states it is *"already been fixed and
  will be available when VCN firmware in linux-firmware repo is updated."* Not a
  kernel fix — a `linux-firmware` update, outside this package.
- **`#5896`** — CRB Config Warning on RDNA4/DCN4, 0 notes; the sibling of `#5934`.
- Large recurring families on our part, for context rather than action:
  **"Pageflip timed out" / 9070 XT** (`#5511`, `#5647`, `#5217`, `#5059`,
  `#5132`, `#5040`, `#5067`, `#4763`, `#5843`, `#5799`), **`device lost from
  bus` + SMU** (`#5811`, `#5820`, `#5439`, `#5102`, `#5185`, `#5538`, `#4903`),
  and **HDMI FRL** (`#5862`, `#5869`, `#5671`, `#5349`). These corroborate the
  `#5807` watch item — the DCN4 flip-pending root cause is still open and still
  the most-reported class on this silicon.

## Sweep 2026-10-05 (post-boot) — CORRECTION: the futex UAF fix is already in rc6

The machine has rebooted into `7.3.0-rc6-1-sleepy-next` (boot 2026-10-05 22:23).
Full refresh, `next-20261005` fetched, work items re-read.

### CORRECTION to the 2026-10-04 entry

That entry recorded the futex private-hash use-after-free (`f35e3b578422`) as
**absent from rc6** and a candidate to carry. **That was wrong.** It is in rc6,
and therefore in the kernel currently running.

- rc6's `kernel/futex/core.c` shows the **fixed** ordering — `rcu_assign_pointer(mmph->hash, new)` at line 216, then
  `mmph->batches = get_state_synchronize_rcu()` at line 221, with the comment
  *"mmph->batches must reference a grace period which started after mmph->hash
  was assigned."*
- `git merge-base --is-ancestor f35e3b578422 v7.3-rc6` → **is an ancestor**.
- Timeline: the `locking-urgent-2026-10-04` pull merged **2026-10-04 08:29 -0700**;
  rc6 was tagged **13:45 -0700** — five hours later.

**How the error happened, because the shape recurs:** I compared
`v7.3-rc5:kernel/futex/core.c` against `next-20261002:kernel/futex/core.c`, found
them byte-identical, and *extrapolated* that the fix was in neither — without ever
reading rc6's copy. The comparison was correct; the conclusion drawn from it was
not. `next-20261002` predates the 10-04 locking pull, so of course it matched rc5.
**Two trees agreeing tells you about those two trees, nothing about a third.**

The original entry hedged with *"Re-check at the moment the tag appears"*, and
that hedge is what resolves it correctly: checked now, it is in. **No carry
needed.** The bug is fixed in what we run.

A second-order lesson for the same entry: a grep for
`mmph->batches = get_state_synchronize_rcu` matches **both** the buggy and the
fixed versions — the line is present either way, only its *order* changes. Any
probe for a reordering fix must read the surrounding lines, never grep for the
moved line alone.

### Today's linux-next — `next-20261005` (`15551282e82d`)

558 files changed vs `next-20261002`, but **on-target subsystems are nearly
static**:

| Subsystem | Files changed |
|---|---|
| `drivers/gpu/drm/amd` | **0** |
| `io_uring`, `block`, `drivers/nvme`, `r8169` | **0** each |
| `kernel/sched` | 6 (`core.c`, `fair.c`, `ext/*`, `sched.h`, `topology.c`) |
| `mm` | 4 (`memory.c`, `shmem.c`, `swap_state.c`, `swapfile.c`) |
| `arch/x86` | 5 (TDX, `cpu/bugs.c`, `bpf_jit_comp.c`) |
| `kernel/futex` | 1 |

**No amdgpu changes at all** — nothing new for this GPU in today's snapshot. The
`mm` files touched (`swapfile.c`, `swap_state.c`) are our swap stack's, and
`kernel/sched/fair.c` (+85/-21) is our live scheduler, but this pass did not
attribute their commits: the range query on this clone returns the linux-next
merge commit only, because it is `--depth=1`. **Recorded as unresolved, not
dismissed** — the content diff is real, the attribution is not yet done.

### sirlucjan — `cachyos-fixes-patches-v9` is a no-op for us

Directory set advanced `0f0dfad7` → `30f3785b` (*"Add 7.3-rc line (fixes)"* /
*"(arch)"*). **v9 is 15 patches; v8 was 14; the single addition is
`[PATCH 15/15] drm/i915/dp: On DPCD init wake the DPRx for eDP` — i915, not this
hardware.** Patches 01–14 are identical to v8. We source the fixes set from v6,
whose content is a subset. **No action.**

### Work items — 24 updated today, full set (`x-total: 24`)

New since the last read: **`#5754`** *"[REGRESSION] AMDGPU / KWin crash with VM
Page Fault and ring gfx timeout"*, **`#5395`** (*drm-resident-vram reports
impossibly high VRAM usage*), **`#5788`** (gfx1152/Krackan), **`#5742`** (7.3
regression, ONEXPLAYER handheld). The rest are the known set.

Two notes on reading this batch:

- **Many updates cluster at 13:36–13:59 with no new comments** (`#5930`, `#5933`,
  `#5934`, `#5935`, `#5936`, `#5938`, `#5939`, `#5940`, `#5927`, `#5929`) — the
  signature of a bulk label/edit sweep, not ten independent reports. Treating
  each as activity would have inflated this pass tenfold.
- `#5776`'s only new note is Ray6161 attaching `ism-deadlock-suspend.patch`
  (`/uploads/…`, not a commit). The fix is **already in rc6** — verified last pass
  at both call sites.

## Attribution pass 2026-10-05 — what actually moved in today's linux-next

The previous entry left `sched/fair.c` and four `mm` files unattributed because
the linux-next clone is `--depth=1` and range queries return only the merge
commit. Attributed by reading the **diffs** instead.

### `kernel/sched/fair.c` (+85/−21) — a feature, not a fix

Adds **`select_idle_smt_cpu()`**: *"Redirect a CPU to a higher-priority available
sibling in its SMT domain, subject to task affinity."* `select_idle_sibling()`
gains a `select_smt_priority` exit path; five `return` sites become `target = …;
goto select_smt_priority;`.

**It is gated on `sd->flags & SD_ASYM_PACKING`** and returns immediately if
`sched_smt_active()` is false or the domain lacks both `SD_SHARE_CPUCAPACITY` and
`SD_ASYM_PACKING`. That is the **preferred-core / ITMT** family — the same
"Preferred-CPU feature series" already recorded on tip as a feature rather than a
fix.

**Not carrying it: it is a feature, not a fix, and it is 7.4 material.** Whether
`SD_ASYM_PACKING` is even set on this machine was **not established** — the
debugfs domain path was unreadable without root, and the kernel log shows no
ITMT/asymmetric-packing lines (the "asymmetric key" hits are crypto, unrelated).
`amd_pstate_highest_perf` does exist, so CPPC preferred cores are exposed, but
whether they drive `SD_ASYM_PACKING` here is unresolved. Recorded as open, not as
"inert" — that word has burned this repo before.

### `mm/memory.c` (+76/−?) — a refactor, not a fix

Gives `insert_pfn()` a `bool mkwrite` parameter and moves the private-mapping /
COW-PFN comment into the `mkwrite` branch, adding a `pte_pfn(entry) != pfn` check
with `WARN_ON_ONCE(!is_zero_pfn(...))`. This is the
`__vm_insert_mixed()`/`vmf_insert_mixed_mkwrite()` series seen posted to
linux-mm (v2 1–3), which is cleanup work. Not a fix, 7.4 material.

### The rest

`mm/shmem.c` (+8), `mm/swap_state.c` (4), `mm/swapfile.c` (2) are small and were
not individually attributed; `arch/x86/kernel/cpu/bugs.c` is a 2-line change
matching the `CONFIG_MITIGATION_RETPOLINE=n` mitigation-reporting fix already seen
on tip; `kernel/futex/core.c` is the private-hash UAF fix **already in rc6** (see
the correction above).

**Nothing in today's snapshot is a fix we need to carry.**

### Work items — no new fixes, and one notable reversal

- **`#5910` (missing TLB flush fence) — the maintainer disputes it.** Christian
  König replied 2026-10-05: *"The bug description doesn't really adds up: …"*.
  This ledger had recorded it as *"shared code, real bug, no patch posted"* on
  the strength of the reporter's analysis. **That characterisation no longer
  stands** — a maintainer has challenged the premise. Downgraded from "real bug"
  to "disputed", pending what König concludes.
- **`#5754`** — the KWin/ring-timeout "regression": **not this hardware** (RX 5500
  XT, now a 6.12 LTS kernel). The newest comment offers an `ntsync` correlation
  and a `nocompute` workaround with frame-time cost. Not actionable here.
- **`#5395`** — drm-resident-vram over-reporting. pepp diagnosed it in June:
  buffers with `AMDGPU_GEM_CREATE_DISCARDABLE` are dismissed early in
  `ttm_bo_evict` without being removed from `drm-resident-vram`. **A diagnosis
  with no patch**, and a statistics-accounting bug — visible only through
  `amdgpu_top`, no correctness or stability impact.
- **`#5936`** — another instance of the pageflip family, this time RX 9070 XT with
  a 4K60 + 1440p144 pair. Zero notes, no analysis.

**No commit shas were cited in any of these comments** — the extraction returned
an empty set, so there was nothing to verify this pass.

## Broad work-item patch sweep 2026-10-05 — every commit reference, verified

The earlier passes extracted shas only from *recent* comments. This one scanned
the **whole tracker**: all 1852 open issues re-fetched, filtered to the 166 that
name this machine's silicon, and every hex-like token in their descriptions
extracted and verified.

**533 distinct hex-like tokens → only 10 real commits.** The other 523 were image
paths, `/uploads/` ids, register values and blob ids — consistent with the ratio
this skill documents (301 of 332 non-commits in an earlier measurement).

### The 10, and what they actually are

| Commit | Date | Cited in |
|---|---|---|
| `8382cd234981` consolidate DCN vblank/flip handling onto `vupdate_no_lock` | 2026-06-12 | `#5599` |
| `48ab86360af1` check `GRPH_FLIP` status before sending event | 2026-06-12 | `#5599` |
| `3eb46fbb601f` gfx11: adjust KGQ reset sequence | 2026-01-28 | `#5125` |
| `af3303970da5` Fix mismatched unlock for DMUB HW lock in HWSS fast path | 2025-12-08 | `#5853` |
| `6d92c4d03063` Rename FAMS2 global control lock to DMUB HW control lock | 2025-09-17 | `#4753` |
| `d69248cf4c91` gfx11: Implement the GFX11 KCQ pipe reset | 2025-02-21 | `#5125` |
| `6eb4c13a3845` Support "Broadcast RGB" drm property | 2025-01-07 | `#5812` |
| `dcc8e148e013` gfx11: Implement the GFX11 KGQ pipe reset | 2024-07-17 | `#5125` |
| `00c391102abc` Add misc DC changes for DCN401 | 2024-03-20 | `#4753` |
| `a48ce36e2786` iommu: Prevent RESV_DIRECT devices from blocking domains | 2023-08-09 | `#5644` |

**All ten are causal references, not pending fixes.** They are cited inside the
issues as *"this caused it"* or *"this is related"* — bisection results and
regression pointers. Not one is a fix awaiting inclusion. **Nothing to carry.**

**A methodology caveat on my own check.** I tested membership with
`git merge-base --is-ancestor <sha> v7.3-rc6`, which reported 6 present and 4
absent. `CLAUDE.md` warns that this command is unreliable in these shallow
clones, and it fails in one direction only: truncation produces **false
negatives**, never false positives. So the six "in rc6" results stand, and the
four "NOT in rc6" results are **untrustworthy** — `d69248cf4c91` and
`dcc8e148e013` are gfx11 commits from 2025 and `00c391102abc` a DCN401 commit
from 2024, all of which would necessarily be in a mid-2026 kernel. Correcting for
that, the honest reading is **all ten are upstream**. The durable rule: use
`is-ancestor` to *confirm* membership, never to deny it.

### The real finding: `#5125` belongs to the `#5759` cluster

`#5125` — *"[GFX11/GFX12] Pipe reset disabled on all RDNA 3 & RDNA 4 GPUs — MES
hang forces full GPU reset, destroying Wayland session"* — sat outside every
recency window (last updated 2026-07-05) and only surfaced here.

Its newest substantive comment is fholzer, 2026-07-05, on an **ASRock Navi 48 XTW
32GB**: *"I still observe failed MES REMOVE_QUEUE on my R9700, and I am on MES
firmware 0x8B."*

That is the **same failure as `#5759`** (`MES(0) fails to respond to
REMOVE_QUEUE on Navi 48`) and adjacent to `#5909` (MES stops after a large
VRAM transfer). Three independent reports of MES `REMOVE_QUEUE` failures on
Navi 48, and the two gfx11 pipe-reset commits cited here are the same territory
as the 7.4 pull's *"gate gfx pipe reset on PER_PIPE"* and *"restore collateral
gfx queues after pipe reset"* work.

**This strengthens the `#5759` watch item rather than adding a carry.** There is
still no patch to take; the fixes exist only in the 7.4 pull. But the case for
watching it is now three reports deep rather than one, and if this machine ever
logs a MES `REMOVE_QUEUE` timeout the `amdgpu.mes_log_enable=1` workaround is the
first thing to try.

## Sweep 2026-10-07 — zswap request-contention series assessed; next-20261006

Full refresh, `next-20261006` fetched, work items read.

### `[PATCH 0/2] mm: zswap: reduce request contention on loads` (Usama Arif) — candidate, not adopted

The series the user linked (`<20261006002307.2669023-1-usama.arif@linux.dev>`, the
`-1-` id is the **cover letter**). Usama Arif is already a contributor here — we
carry `2129` (*zstd: skip the BMI2 probe when dynamic BMI2 dispatch is
disabled*) from him.

- **1/2** `mm: zswap: use separate compression and decompression requests`
- **2/2** `mm: zswap: use stack requests for synchronous decompression`

The problem, from the patch text: *"A low-priority load that is preempted after
the codec drops its stream lock keeps holding the mutex and stalls every other
load on that CPU, including higher-priority ones."* The fix lets synchronous
codecs decompress with an **on-stack request and take no zswap lock**;
asynchronous ones keep the per-CPU request and mutex. *"All in-tree software
compressors qualify"* — **zstd is what this machine runs.**

**It clears the review bar: `Acked-by: Nhat Pham <nphamcs@gmail.com>`**
(2026-10-07) on patch 2/2. Nhat Pham maintains zswap. Sergey Senozhatsky and
Nhat Pham also replied on 1/2.

**But it does not apply to rc6**, so it cannot be carried as-is:

| Patch | Result against `v7.3-rc6` |
|---|---|
| 1/2 | `git apply --check` **FAILS** at `mm/zswap.c:866`; `patch` reports **1 of 9 hunks FAILED** — eight apply |
| 2/2 | **FAILS**, 4 of 5 hunks — because it **depends on 1/2** being in place first |

The single failing hunk in 1/2 is drift, not a rework — eight of nine hunks land.
A rebase is likely tractable. **I did not characterise that hunk** (a filename
glob missed and the command ran against nothing); recorded as unfinished rather
than guessed at.

**Disposition: candidate for the next bump, not a carry now.** It is a
contention/latency optimisation with an `Acked-by`, its base dependency needs
rebasing onto rc6, and it has not reached linux-next yet (`MAX_SYNC_COMP_REQSIZE`
is absent from both `next-20261005` and `next-20261006`). The natural moment to
take it is the rc7 rebase, where patch 1/2 may well be upstream already.

**Also noted in the same thread, not triaged:** `[PATCH v8 14/30] mm: zswap:
reject high-order swap cache allocations backed by zswap` (Usama Arif), and
Baoquan He's xswap v4 series — both touch our swap stack.

### `next-20261006` (`e634eccf3de1`)

On-target deltas vs `next-20261005`: `drivers/gpu/drm/amd` **1 file**, `mm` **16**,
`kernel/sched` 1, `io_uring` 1, `block` 0, `kernel/futex` 0. Not attributed this
pass. **The zswap series is not in it.**

### Work items — 16 updated since 2026-10-06

Most on-target is **`#5897` (2026-10-07)** — *"7.3: HDMI FRL status poll
re-detects a live link, next CRTC disable …"*. **This is our kernel line and our
display path**, and it is adjacent to work we already carry: `1171`
(*serialize HDMI FRL status polling against link detect*) and `1136`
(*update and revert FRL LT timeout*). Worth reading in full next pass — it may be
the same defect our `1171` addresses, or a second instance.

Also new: `#5946` (DP monitor with conflicting 420-only EDID declarations —
an **EDID** parser case, and we carry EDID patches), `#5942` (DCN35 PSR),
`#5941` (KCQ enable failure after hibernate), `#5944`/`#5884`/`#5906` (Navi31
"Illegal opcode" cluster), `#5945` (Navi21 ROCm queues stop with GFXOFF).
`#5339` (*RA24 little-endian is not valid for RDNA4 display hardware but is
listed as supported*) remains open and is a genuine display-caps mismatch on our
silicon.
