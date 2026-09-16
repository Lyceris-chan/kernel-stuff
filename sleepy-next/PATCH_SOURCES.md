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
| `0101–0113` | CachyOS branch squashes | 6 |
| `1000–1099` | GPU core (GFX12, GMC, SDMA, PSP, TTM, TLB) | 30 |
| `1100–1199` | AMD display (DCN4, colorops) | 20 |
| `1200–1299` | AMD power management (amd-pstate, CPPC) | 18 |
| `2000–2099` | Block, I/O, buffers and network (bfq, mq-deadline, zram, io_uring, r8169) | 45 |
| `2100–2199` | Memory management and swap (zstd, LRU-MARIE, MGLRU, gup, xswap) | 76 |
| `2200–2299` | CPU idle (NAP governor) | 1 |
| `2300–2399` | Build system and kbuild | 21 |
| `2400–2499` | Core scheduler and sched-ext | 14 |
| `2500–2599` | x86 and arch core | 7 |
| `2600–2699` | Time and timers | 3 |
| `9000–9099` | agd5f staging + userq lifecycle backports | 45 |

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
| `1004` | drm/amdgpu/gmc9: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `043453a07452` |
| `1005` | drm/amdgpu/gmc10: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `ebfc4cbbb580` |
| `1006` | drm/amdgpu/gmc11: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `a1efda0bc2ee` |
| `1007` | drm/amdgpu/gmc12: disallow gfxoff around TLB flushes | Alex Deucher | 2026-07-13 | `48026ef6756e` |
| `1008` | drm/amdgpu: add an buffer funcs callback for TLB invalidation | Alex Deucher | 2026-07-13 | `7b5120c066ad` |
| `1009` | drm/amdgpu/sdma5.0: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `c7a9aad03f6c` |
| `1010` | drm/amdgpu/sdma5.2: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `a461b17a3fec` |
| `1011` | drm/amdgpu/sdma6: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `748c1927ec4e` |
| `1012` | drm/amdgpu/sdma7: add tlb invalidation buffer func callback | Alex Deucher | 2026-07-13 | `4481ee06e2a3` |
| `1013` | drm/amdgpu: add core helper to do TLB invalidation via SDMA | Alex Deucher | 2026-07-13 | `1d5a9fb3dc8c` |
| `1014` | drm/amdgpu/gmc: add more gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `14a0ecfb5c9d` |
| `1015` | drm/amdgpu/gmc10: switch to new gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `497621ee93de` |
| `1016` | drm/amdgpu/gmc11: switch to new gmc tlb inv helpers | Alex Deucher | 2026-07-13 | `2ba771d6669d` |
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
| `9064` | drm/amdgpu/gfx11: hold userq refs in private fault worker | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-4-lingshan.zhu@amd.com` |
| `9065` | drm/amdgpu/gfx12: hold userq refs in private fault worker | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-5-lingshan.zhu@amd.com` |
| `9066` | drm/amdgpu: implement asynchronous userq destruction routine | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-6-lingshan.zhu@amd.com` |
| `9067` | drm/amdgpu: hold userq kref in MES reset | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-7-lingshan.zhu@amd.com` |
| `9068` | drm/amdgpu: hold userq kref during isolation scheduling | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-8-lingshan.zhu@amd.com` |
| `9069` | drm/amdgpu: hold userq kref during suspend and resume | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-9-lingshan.zhu@amd.com` |
| `9070` | drm/amdgpu: free userq by kref_put when fails to create | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-10-lingshan.zhu@amd.com` |
| `9071` | drm/amdgpu: take queue kref in userq_create to avoid UAF | Zhu Lingshan | 2026-09-14 | `20260914130724.130794-11-lingshan.zhu@amd.com` |
| `9072` | drm/amdgpu/sdma: add detect_hung_queue callback | Jesse Zhang | 2026-09-03 | `972a8cd8fba1` |
| `9073` | drm/amdgpu/sdma6: implement detect_hung_queue | Jesse Zhang | 2026-09-03 | `994dea375802` |
| `9074` | drm/amdgpu/sdma7: implement detect_hung_queue | Jesse Zhang | 2026-09-03 | `ba07df579939` |
| `9075` | drm/amdgpu/userq: reset a hung SDMA user queue over MMIO | Jesse Zhang | 2026-09-03 | `10a6760a1a64` |
| `1135` | drm/amd/display: fix HPD program filter programming | Charlene Liu | 2026-08-05 | `20260805063937.2145774-13-chiahsuan.chung@amd.com` |
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
| `2131` | mm/mglru: separate folio generation update from LRU accounting | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `54e9345e4563` |
| `2132` | mm/mglru: batch update lrugen->nr_pages in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `521a7c952c89` |
| `2133` | mm/mglru: enhance cold/hot inversion handling in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `3384a49a865e` |
| `2134` | mm/mglru: exclude folios promoted by aging from protected in inc_min_seq() | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `e25d6c041ca0` |
| `2135` | mm/mglru: make LRU folio prefetch helper an inline function | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `efac6d51d1d6` |
| `2136` | mm/mglru: move folios from oldest gen to second-oldest gen from head to tail | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `81cb06a097b3` |
| `2137` | mm/mglru: batch move folios to the second-oldest gen's LRU | "Barry Song (Xiaomi)" <baohua@kernel.org> | 2026-09-02 | `64fff1e3d929` |
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
| `9017` | drm/amdgpu/gmc11: Pass cam_index to retry fault handler | Timur Kristóf | 2026-07-01 | `20260701161721.85681-8-timur.kristof@gmail.com` |
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

**A trap that affects most of this range:** `lru_gen_enabled()` returns false
while `lru_marie_enabled()` is true, so **every MGLRU patch (`2131`–`2137`) is
inert here**. `CONFIG_LRU_GEN=y` and `LRU_GEN_ENABLED=y` are set, but MARIE owns
reclaim, so the MGLRU aging path never runs. Confirm which of the two owns the
subsystem before crediting either with a result.

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
