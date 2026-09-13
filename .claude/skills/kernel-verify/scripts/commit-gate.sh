#!/usr/bin/env bash
# PreToolUse commit gate for sleepy-kernel.
#
# Runs the kernel-verify fast tier before a `git commit` and blocks the commit
# when it reports a real finding, so the invariants that have actually broken
# here — stale b2sums, a patch missing from the ledger, a documented version or
# patch count that no longer matches the PKGBUILD, a malformed patch header, a
# skill that violates the Agent Skills spec — cannot reach a commit unnoticed.
#
# Exit 2 blocks the tool call and returns this script's stderr to Claude.
# Exit 0 allows it.
#
# Deliberately fail-open: verify.py exits 2 on an environment problem (no
# PKGBUILD, no skills directory) and this gate treats that, and every other
# non-1 status, as "do not block". The gate guards correctness, not availability.
# A gate that bricks committing when a tool is missing is worse than no gate.
set -uo pipefail

payload=$(cat)

# Cheap pre-filter: almost every Bash call has no "commit" in it, so avoid
# spawning anything until one does.
case "$payload" in
  *commit*) ;;
  *) exit 0 ;;
esac

# Precise check. This repo commits as `git -c user.name=... -c user.email=...
# commit ...`, so a prefix match on "git commit" would miss it; test the words.
if ! printf '%s' "$payload" | python3 -c '
import json, sys
try:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(1)
words = cmd.split()
sys.exit(0 if "git" in words and any(w == "commit" for w in words) else 1)
' 2>/dev/null; then
  exit 0
fi

root="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$root" ]; then
  root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
fi
verify="$root/.claude/skills/kernel-verify/scripts/verify.py"
[ -f "$verify" ] || exit 0

results=$(python3 "$verify" --tier fast --json 2>&1)
status=$?

# 1 = a check failed. Anything else (0 pass, 2 environment) does not block.
if [ "$status" -ne 1 ]; then
  exit 0
fi

echo "kernel-verify (fast tier) found problems, so the commit was blocked:" >&2
if ! printf '%s' "$results" | jq -r '.[] | select(.status == "FAIL") | "  \(.check): \(.detail)"' >&2 2>/dev/null; then
  printf '%s\n' "$results" >&2
fi
echo "Re-run the suite for the full report: python3 .claude/skills/kernel-verify/scripts/verify.py" >&2
exit 2
