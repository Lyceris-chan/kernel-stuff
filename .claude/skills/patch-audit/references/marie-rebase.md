# Rebasing LRU-MARIE to a new kernel base

MARIE (`2101`) is a ~15k-line patch by firelzrd. When the base moves, its host
hooks (`memcontrol.h`, `swap.h`, `page_io.c`, `folio.c`/`swap.c`, `vmscan.c`)
may need re-anchoring while the `mm/lru_marie/` subsystem stays **byte-identical
to the author's** (a hard requirement — do not "improve" it).

## Method (learned 2026-09-07)

1. **Fresh tree at the new base** (a `git worktree` of the base tag).
2. **Apply the patch, collect rejects** — `patch -p1 --forward -F2 <
   2101.patch`. Typically 1–4 hunks fail, all in host files.
3. **Fix the rejects in-tree** against the base's actual API (for example, rc2 dropped
   the `long val`/`WARN` path in `mem_cgroup_get_zone_lru_size`; rc2 renamed
   `__swap_writeout` → `__swap_writepage`). Keep the change minimal and
   semantically identical to the author's intent.
4. **Regenerate only the changed file-sections** with
   `diff -u <pristine-copy> <fixed-file>` — **never hand-edit hunk headers**
   (wrong `@@` counts and literal `\t` vs real tabs are the usual failure) and
   **never `git diff` after `git add -A`** (it duplicates new-file sections).
5. **Splice** each regenerated section into the patch, replacing the stale one,
   with git-style headers:
   ```
   diff --git a/<file> b/<file>
   --- a/<file>
   +++ b/<file>
   <diff -u hunks>
   ```
   Do **not** add an `index 000000000000..000000000000 100644` line for an
   existing file — `patch` then treats it as a new file and prints
   `which already exists! Skipping patch`.
6. **Verify** on a fresh tree: `patch -p1 --forward -F2` must report 0 `FAILED`,
   produce 0 `.rej`, and the hooks must be present: `lru_marie_zone_size_read`
   in `memcontrol.h`, `kcompressd` in `swap.h`, `nr_swap_write_failed` bump in
   `page_io.c`, `include/linux/lru_marie.h` created.
7. **Fidelity check** — compare each `mm/lru_marie/*` file against the original
   patch's added lines; expect byte-identical except the documented one-line
   compile fixes.

## Pitfalls

- `patch --forward` exits **0 when it skips** a reversed/already-applied patch —
  always rg the output for `Skipping patch` / `Reversed`, or a no-op patch
  looks like a success.
- `git apply --check` passing does **not** mean GNU `patch` will accept it (the
  tool `prepare()` actually runs).
- MARIE's hooks are gated `#ifdef CONFIG_LRU_MARIE`; with the option off the
  host code must reduce exactly to stock.
