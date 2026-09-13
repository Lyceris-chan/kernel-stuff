# Mailing-list access (amd-gfx, dri-devel)

`WebFetch` gets HTTP 403 on lists.freedesktop.org — use `curl` with a
browser User-Agent. The monthly `.txt.gz` mbox is fastest for keyword
scans; `thread.html` for a specific thread.

```bash
Mailing list archives (freedesktop, safe to curl)
#
IMPORTANT: WebFetch returns HTTP 403 on lists.freedesktop.org. The ONLY
working method is curl with a browser User-Agent. This is a proven workaround.
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
MONTH=$(date +%Y-%B)   # e.g. 2026-August
Option A — monthly .txt.gz mbox (fastest for keyword scanning):
curl -s -A "$UA" "https://lists.freedesktop.org/archives/amd-gfx/${MONTH}.txt.gz" -o /tmp/amd-gfx-${MONTH}.txt.gz
[ -s /tmp/amd-gfx-${MONTH}.txt.gz ] && gunzip -f /tmp/amd-gfx-${MONTH}.txt.gz
curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}.txt.gz" -o /tmp/dri-devel-${MONTH}.txt.gz
[ -s /tmp/dri-devel-${MONTH}.txt.gz ] && gunzip -f /tmp/dri-devel-${MONTH}.txt.gz
Option B — thread index HTML (use when you need a specific thread):
  https://lists.freedesktop.org/archives/amd-gfx/${MONTH}/thread.html
  https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html
Per-message pages live at .../{msgid}.html, e.g.:
  https://lists.freedesktop.org/archives/amd-gfx/2026-August/abcdef1234567890.html
Download one the same way, with the browser UA:
  curl -s -A "$UA" "https://lists.freedesktop.org/archives/dri-devel/${MONTH}/thread.html" -o /tmp/dri-thread.html
Message links in thread.html are <LI><A HREF="NNNNN.html">[PATCH n/N] subject
(msgid is a bare 6-digit number, NOT "msgNNNNN.html"). Extract subjects:
  rg -o '<LI><A HREF="[0-9]+\.html">[^<]*' /tmp/dri-thread.html \
    | sed -E 's/<LI><A HREF="([0-9]+)\.html">/\1: /'
The date/subject/author indexes only contain navigation links — use thread.html.
ML message extraction (learned 2026-08-26) — per-message pages are unreliable
as raw patches. Known gotchas:
  * QP-encoded mboxes (patchew.org mirrors): `git am <mbox>` decodes them
    natively — use git am on a scratch worktree, then cherry-pick the commits.
  * dri-devel pages use U+00A0 non-breaking spaces for indentation AND wrap
    lines as <LI><A HREF=...>mailing-list links; always
    .replace('&nbsp;',' ').replace('\xa0',' ') before git apply.
  * Some messages are replies that quote the patch (broken spacing). Find the
    ORIGINAL [PATCH] message via the thread.html rg above instead.
  * Pages may carry a trailing "-------------- next part --------------" HTML
    attachment after the "-- 2.xx.x" diff terminator — truncate at "-- ".
  * After extraction always `git apply --check`; if a hunk is stale against a
    newer base, apply the change manually with Edit rather than forcing fuzz.
If a download produced an EMPTY file or a page containing "403 Forbidden",
stop — do not continue. Re-run with the UA above, or use the git repos.
```
```

If a download is empty or shows "403 Forbidden", stop and re-run with the
UA above, or use the git repos.
