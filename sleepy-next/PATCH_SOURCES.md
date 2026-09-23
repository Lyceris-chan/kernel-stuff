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

`2302`–`2322` are Lorenzo Stoakes' kbuild build-speedup series, now the
**v2** posting (`20260914-build-speedup-v2-0-39817ec5db23@kernel.org`,
21 patches, 2026-09-14), which supersedes the v1 carried previously. v2 drops
the modpost srcversion hashing pair and adds the toolchain-checks move into
`init/Kconfig.toolchain` and an objtool instruction-hash sizing patch, with
the review feedback from v1 folded in. This is why a full rebuild here takes
about 8 minutes. Build-time only — nothing here changes runtime behaviour.

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
