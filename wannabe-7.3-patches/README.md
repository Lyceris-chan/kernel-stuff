# wannabe-7.3-patches

Reproducible patch series for the **wannabe Linux 7.3-rc1 preview tree**
(`wannabe-7.3-rc1/`). These are the 15 commits applied on top of the
`linux-next` **next-20260825** snapshot. See `WANNABE-7.3.md` for the tree
history and `PATCH_SOURCES.md` (2026-08-26 record) for provenance.

## Rebuild

```bash
# 1. Fresh worktree at the base snapshot
git -C repos/linux-next worktree add wannabe-7.3-rc1 next-20260825
cd wannabe-7.3-rc1

# 2. Replay the 15 commits (verify against `WANNABE-7.3.md` Layer order)
git am ../wannabe-7.3-patches/*.patch
```

`git am` on this series reproduces the exact tree of branch `wannabe-7.3`
(verified 2026-08-26: `git diff` vs the branch tip is empty).

## Content (0001→0015)

1. `0001` — 18 upstream merges (17 amd-staging + drm/sched lock)
2. `0002` — 69 sleepy-kernel additive patches (CachyOS + local)
3. `0003`–`0010` — 8 RFC `mm/gup` follow_page_mask() batching commits
   (Rik van Riel, Phoronix 08-11 WIP)
4. `0011` — clean 7.3 HDMI: upstream HDMI 2.1 VRR/ALLM v4 amdgpu-side
5. `0012` — userq GPU-reset crash + lockdep 5-patch (Vitaly Prosyak)
6. `0013` — BO-bind for imported user-queue BOs (v5)
7. `0014` — KFD mark queues as reset after full GPU reset
8. `0015` — amdgpu_vm_init error-path NULL-deref reorder

Each patch keeps its original `From:`/`Subject:`/`Signed-off-by:` headers
(commit SHAs differ from the live branch because `git am` recreates them).
