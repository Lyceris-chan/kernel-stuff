#!/usr/bin/env python3
"""Verify that every patch in the series applies, in order, to a pristine base.

This is the authoritative check for the sleepy-kernel series. Applying the
patches one at a time in isolation gives false negatives, and GNU patch's exit
status alone is not enough: with ``--forward`` a patch whose content is already
present is *skipped* and reported as success. A skipped patch is an inert
no-op, so this script detects three failure modes per patch:

* a non-zero exit from ``patch``,
* ``FAILED`` (a rejected hunk), and
* ``Skipping patch`` / ``Reversed`` (silently did nothing).

Run it before a build, and after any change to the series or to source=():

    python3 .claude/skills/kernel-build/scripts/audit_series.py

It creates a throwaway worktree, so it never touches the live build tree or any
tree you are working in. Exit status is 0 when every patch applied, 1 when any
patch failed or was skipped, and 2 when the environment is not usable.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# `patch` prints these when it did NOT apply the patch cleanly. "Skipping patch"
# and "Reversed" appear when patch believes the change is already present.
FAILURE_MARKERS = ("FAILED", "Skipping patch", "Reversed (or previously applied)")

# The base tag is derived from the PKGBUILD's _srctag so it cannot drift. That
# variable holds the *tarball* name (e.g. "linux-7.3-rc2" -> tag "v7.3-rc2"),
# and it is "next-YYYYMMDD" for a linux-next snapshot, which has no tag at all.
FALLBACK_TAG = "v7.3-rc3"


class AuditError(RuntimeError):
    """Environment problem — the audit could not be attempted."""


def find_repo_root(start: Path) -> Path:
    """Walk up from *start* until a directory containing sleepy-next/ is found."""
    for candidate in [start, *start.parents]:
        if (candidate / "sleepy-next" / "PKGBUILD").is_file():
            return candidate
    raise AuditError(
        "could not find the repository root (no sleepy-next/PKGBUILD above "
        f"{start}). Run this from inside the sleepy-kernel checkout."
    )


def parse_source_patches(pkgbuild: Path) -> list[str]:
    """Return the patch entries of source=() in declaration order."""
    text = pkgbuild.read_text(encoding="utf-8")
    match = re.search(r"^source=\((.*?)^\)", text, re.S | re.M)
    if not match:
        raise AuditError(f"no source=() array found in {pkgbuild}")
    entries = []
    for line in match.group(1).splitlines():
        entry = line.strip().strip('"').rstrip()
        if entry.endswith(".patch"):
            entries.append(entry)
    if not entries:
        raise AuditError(f"source=() in {pkgbuild} lists no .patch files")
    return entries


def derive_tag(pkgbuild: Path) -> tuple[str, str]:
    """Return (git_tag, note) derived from the PKGBUILD's _srctag.

    _srctag names the source *tarball*, so "linux-7.3-rc2" maps to the git tag
    "v7.3-rc2" and "linux-7.3" to "v7.3". A linux-next snapshot (_srctag
    "next-YYYYMMDD") has no corresponding tag, so it is reported rather than
    guessed at.
    """
    match = re.search(r"^_srctag=(\S+)", pkgbuild.read_text(encoding="utf-8"), re.M)
    if not match:
        return FALLBACK_TAG, f"_srctag absent; assumed {FALLBACK_TAG}"
    srctag = match.group(1).strip().strip('"')
    if srctag.startswith("linux-"):
        return "v" + srctag[len("linux-") :], ""
    return FALLBACK_TAG, (
        f"_srctag is {srctag!r}, which is not a mainline tag (linux-next "
        f"snapshots have none); assumed {FALLBACK_TAG}"
    )


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def make_worktree(repo: Path, worktree: Path, tag: str) -> None:
    """Create a detached worktree at *tag*, replacing any previous one."""
    if worktree.exists():
        # Reuse is safe only after resetting: a tree left with patches applied
        # would make every later patch fail for the wrong reason.
        reset = run(["git", "checkout", "--", "."], cwd=worktree)
        clean = run(["git", "clean", "-fdq"], cwd=worktree)
        if reset.returncode or clean.returncode:
            raise AuditError(
                f"could not reset the existing worktree at {worktree}. "
                "Remove it and re-run."
            )
    result = run(["git", "worktree", "add", "--quiet", "--detach", str(worktree), tag], cwd=repo)
    if result.returncode:
        raise AuditError(
            f"could not create a worktree at {tag} in {repo}:\n"
            f"  {result.stderr.strip()}\n"
            "Fetch the tag first, or pass --tag with one that exists."
        )


def audit(worktree: Path, patches: list[Path]) -> list[tuple[Path, str]]:
    """Apply each patch in order; return the failures as (patch, reason) pairs."""
    failures: list[tuple[Path, str]] = []
    for index, patch in enumerate(patches, start=1):
        with patch.open("rb") as handle:
            result = subprocess.run(
                ["patch", "-Np1", "--forward"],
                stdin=handle,
                cwd=worktree,
                capture_output=True,
                text=True,
            )
        output = result.stdout + result.stderr
        marker = next((m for m in FAILURE_MARKERS if m in output), None)
        if result.returncode != 0 or marker:
            reason = marker or f"patch exited {result.returncode}"
            rejected = [ln.strip() for ln in output.splitlines() if "FAILED at" in ln]
            if rejected:
                reason = f"{reason} ({'; '.join(rejected[:3])})"
            failures.append((patch, reason))
        print(f"  [{index:>3}/{len(patches)}] {'FAIL' if (result.returncode or marker) else 'ok  '} {patch.name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pkgbuild", type=Path, default=None, help="default: sleepy-next/PKGBUILD")
    parser.add_argument("--repo", type=Path, default=None, help="clone to branch the worktree from; default: repos/linux-next")
    parser.add_argument("--tag", default=None, help="base tag; default: _srctag from the PKGBUILD")
    parser.add_argument("--worktree", type=Path, default=None, help="scratch worktree path; default: repos/_audit")
    parser.add_argument("--keep", action="store_true", help="leave the worktree in place afterwards")
    parser.add_argument("--quiet", action="store_true", help="print only the summary")
    args = parser.parse_args()

    try:
        root = find_repo_root(Path.cwd())
        pkgbuild = (args.pkgbuild or root / "sleepy-next" / "PKGBUILD").resolve()
        package_dir = pkgbuild.parent
        repo = (args.repo or root / "repos" / "linux-next").resolve()
        worktree = (args.worktree or root / "repos" / "_audit").resolve()

        if not pkgbuild.is_file():
            raise AuditError(f"no PKGBUILD at {pkgbuild}")
        if not (repo / ".git").exists():
            raise AuditError(
                f"{repo} is not a git clone. Clone it with "
                '--shallow-since="YYYY-MM-DD" (never --depth=1), or pass --repo.'
            )

        tag, tag_note = derive_tag(pkgbuild)
        if args.tag:
            tag, tag_note = args.tag, ""
        entries = parse_source_patches(pkgbuild)

        patches: list[Path] = []
        missing: list[str] = []
        for entry in entries:
            path = package_dir / entry
            (patches if path.is_file() else missing).append(path if path.is_file() else entry)
        if missing:
            raise AuditError(
                "source=() lists patch files that do not exist on disk:\n  "
                + "\n  ".join(str(m) for m in missing)
            )

        # Fail before creating a worktree if the tag is not in the clone, so the
        # message names the real problem instead of a raw git error.
        if run(["git", "rev-parse", "--verify", f"{tag}^{{commit}}"], cwd=repo).returncode:
            raise AuditError(
                f"tag {tag} is not in {repo}. Fetch it (git fetch origin tag {tag}) "
                "or pass --tag with one that exists."
            )
        if tag_note:
            print(f"note: {tag_note}", flush=True)

        print(f"Base tag:  {tag}", flush=True)
        print(f"Series:    {len(patches)} patches, from {pkgbuild}", flush=True)
        print(f"Worktree:  {worktree}", flush=True)

        make_worktree(repo, worktree, tag)
        failures = audit(worktree, patches)
    except AuditError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    finally:
        if "worktree" in locals() and not args.keep:
            run(["git", "worktree", "remove", "--force", str(worktree)], cwd=repo)
            run(["git", "worktree", "prune"], cwd=repo)

    if failures:
        print(f"\nFAILED: {len(failures)} of {len(patches)} patches did not apply cleanly:")
        for patch, reason in failures:
            print(f"  {patch.name}: {reason}")
        print(
            "\nA 'Skipping patch' entry is inert, not a success — either the change is\n"
            "already upstream in the base, or its context has drifted and it needs a rebase."
        )
        return 1

    print(f"\nOK: all {len(patches)} patches applied cleanly to {tag}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
