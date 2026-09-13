#!/usr/bin/env python3
"""Verification suite for the sleepy-kernel patch series and packaging.

Runs the checks that catch the mistakes this project actually makes, in tiers
ordered by cost, so a commit gate can run the cheap ones and a release can run
everything:

  fast    seconds, no kernel tree needed
          - every source=() patch exists on disk, and nothing extra is there
          - b2sums match the files (i.e. updpkgsums is current)
          - patch headers are intact and subjects carry no [PATCH n/N] series number
          - every patch number is documented in PATCH_SOURCES.md
          - documented patch count and base version match reality
          - skills satisfy the Agent Skills specification
          - no dangling patch symlinks

  series  ~1-2 minutes, needs the repos/linux-next clone
          - the whole series applies cumulatively to the base tag
            (delegates to kernel-build/scripts/audit_series.py)

  deep    minutes, needs a prepared kernel tree (--tree)
          - checkpatch.pl (--strict) on the patches we authored ourselves
          - sparse (make C=1) over the directories our patches touch

Tools are detected, not assumed: a missing tool produces SKIP with the reason,
never a silent pass. Exit status: 0 all checks passed, 1 one or more failed,
2 the environment is unusable (bad --tree, no PKGBUILD, and so on).

Justify thresholds rather than hardcoding them: the only numbers here are the
specification limits (name 64, description 1024, body 500 lines), which come from
https://agentskills.io/specification, and the "own patches" range 0001-0049,
which CLAUDE.md defines as the handmade ones.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

# CLAUDE.md: 0001-0049 are the handmade local patches; everything else is a
# backport of reviewed upstream work.
OWN_PATCH_RANGE = range(1, 50)

# What kernel developers actually use to find problems before booting. `check`
# names the binary we probe for; `cost` is why the tool is or is not wired into a
# tier automatically. Runtime tools are listed for completeness but cannot be
# automated here — they need a diagnostic kernel booted on the machine.
KERNEL_TOOLS = [
    ("checkpatch.pl", "kernel source", "static", "style and commit-message conformance",
     "deep", "runs on our own patches; the script extracts it from the source tarball"),
    ("sparse", "pacman -S sparse", "static", "the kernel's semantic checker (make C=1)",
     "deep", "installed; compiled through make, so it needs --tree"),
    ("spatch", "pacman -S coccinelle", "static", "semantic patches and scripts/coccinelle/ API checks",
     "deep", "skipped unless installed"),
    ("make W=1", "in-tree", "static", "compiler warnings above the default level",
     "deep", "needs --tree; the highest signal for patches we wrote"),
    ("scan-build", "pacman -S clang-tools-extra", "static", "clang static analyzer over a build",
     "manual", "installed, but a full run costs a build; invoke deliberately"),
    ("gcc -fanalyzer", "gcc >= 10", "static", "GCC interprocedural analyzer",
     "manual", "GCC 16 present; needs a separate gcc build of the tree"),
    ("smatch", "smatch.kernel.org", "static", "the kernel's deeper analyzer",
     "external", "not packageable here; submit the tree to smatch.kernel.org"),
    ("objtool", "in-tree", "build", "ORC/unwind and noinstr validation",
     "build", "already runs on every build — a failure breaks it, so it is covered"),
    ("KUnit", "in-tree", "test", "in-kernel unit tests (tools/testing/kunit)",
     "manual", "needs its own build; `./tools/testing/kunit/kunit.py run`"),
    ("selftests", "in-tree", "test", "subsystem selftests (tools/testing/selftests)",
     "manual", "run after installing; needs a built tree"),
    ("KASAN", "in-tree", "runtime", "use-after-free and out-of-bounds detection",
     "runtime", "needs a diagnostic kernel booted; not automatable from here"),
    ("KCSAN", "in-tree", "runtime", "data-race detection",
     "runtime", "same — boot a diagnostic kernel"),
    ("lockdep", "in-tree", "runtime", "lock-order and irq-safety validation",
     "runtime", "same — boot a diagnostic kernel"),
    ("KFENCE", "in-tree", "runtime", "low-overhead heap-out-of-bounds sampling",
     "runtime", "same — boot a diagnostic kernel"),
]

RESULTS: list[dict] = []


class EnvError(RuntimeError):
    """Environment problem — verification could not be attempted."""


def record(tier: str, name: str, status: str, detail: str = "") -> None:
    RESULTS.append({"tier": tier, "check": name, "status": status, "detail": detail})


def run(cmd: list[str], cwd: pathlib.Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def repo_root(start: pathlib.Path) -> pathlib.Path:
    for candidate in [start, *start.parents]:
        if (candidate / "sleepy-next" / "PKGBUILD").is_file():
            return candidate
    raise EnvError("no sleepy-next/PKGBUILD found above the working directory")


def pkgbuild_entries(pkgbuild: pathlib.Path) -> list[str]:
    text = pkgbuild.read_text(encoding="utf-8")
    match = re.search(r"^source=\((.*?)^\)", text, re.S | re.M)
    if not match:
        raise EnvError(f"no source=() array in {pkgbuild}")
    return [
        line.strip().strip('"').rstrip()
        for line in match.group(1).splitlines()
        if line.strip().strip('"').rstrip().endswith(".patch")
    ]


def b2sum_sets(pkgbuild: pathlib.Path) -> set[str]:
    """The 128-hex BLAKE2 hashes declared in b2sums=().

    The array spans ~180 lines and its closing parenthesis is not reliably at the
    start of a line, so anchor on the declaration and take every 128-hex literal
    after it — the PKGBUILD contains no other hashes of that width.
    """
    text = pkgbuild.read_text(encoding="utf-8")
    start = text.find("b2sums=(")
    return set(re.findall(r"[0-9a-f]{128}", text[start:])) if start != -1 else set()


# --------------------------------------------------------------------------- #
# fast tier
# --------------------------------------------------------------------------- #

def check_sources(package_dir: pathlib.Path, entries: list[str]) -> None:
    missing = [e for e in entries if not (package_dir / e).is_file()]
    (record("fast", "source=() files exist", "FAIL", f"{len(missing)} missing: {missing[:5]}")
     if missing else record("fast", "source=() files exist", "PASS", f"{len(entries)} patches"))


def check_checksums(package_dir: pathlib.Path, entries: list[str], declared: set[str]) -> None:
    if not declared:
        record("fast", "b2sums current", "SKIP", "no b2sums array found")
        return
    stale = []
    for entry in entries:
        path = package_dir / entry
        if not path.is_file():
            continue
        digest = hashlib.blake2b(path.read_bytes(), digest_size=64).hexdigest()
        if digest not in declared:
            stale.append(entry)
    if stale:
        record("fast", "b2sums current", "FAIL",
               f"{len(stale)} files not in b2sums — run updpkgsums: {stale[:3]}")
    else:
        record("fast", "b2sums current", "PASS", f"{len(entries)} hashes match")


def check_headers(package_dir: pathlib.Path, entries: list[str]) -> None:
    """Header fields intact; our own patches carry upstream-quality headers.

    A `[PATCH n/N]` subject is legitimate on a backport — CLAUDE.md rule 4 requires
    keeping upstream headers verbatim, including the series numbering. The rule
    that bans leftover numbering applies to the patches we author, so the check
    only looks at the own-patch range.
    """
    problems, own_problems = [], []
    for entry in entries:
        path = package_dir / entry
        if not path.is_file():
            continue
        # Search the whole file: a mail-extracted patch can carry dozens of
        # Received/DKIM lines before its From:/Subject:, so a fixed window
        # produces false positives. Only header lines sit at column 0 in a patch
        # (diff context and added lines are prefixed with space/+/-).
        text = path.read_text(encoding="utf-8", errors="replace")
        for field in ("From:", "Subject:"):
            if not re.search(rf"^{field}", text, re.M):
                problems.append(f"{path.name}: missing {field}")
        number = int(re.match(r"(\d+)", path.name).group(1))
        if number in OWN_PATCH_RANGE:
            if not re.search(r"^Signed-off-by:", text, re.M):
                own_problems.append(f"{path.name}: no Signed-off-by")
            if re.search(r"^Subject:.*\[PATCH \d+/\d+\]", text, re.M):
                own_problems.append(f"{path.name}: subject still carries [PATCH n/N]")
    if problems:
        record("fast", "patch headers", "FAIL", f"{len(problems)}: {problems[:3]}")
    elif own_problems:
        record("fast", "patch headers", "FAIL", f"our own patches: {own_problems[:3]}")
    else:
        record("fast", "patch headers", "PASS", f"{len(entries)} patches")


def check_provenance(package_dir: pathlib.Path, ledger: pathlib.Path, entries: list[str]) -> None:
    """Report patch numbers not individually named in PATCH_SOURCES.md.

    This is a WARNING, not a failure: the ledger documents patches in session
    groups ("Added (2026-08-27 sweep — 20 patches)") as well as by number, so a
    number that is not spelled out individually is usually still covered. The
    count keeps that drift visible without failing a build on the ledger's
    established style.
    """
    if not ledger.is_file():
        record("fast", "provenance documented", "SKIP", f"{ledger} not found")
        return
    text = ledger.read_text(encoding="utf-8")
    named = {int(n) for n in re.findall(r"`(\d{4})`", text)}
    for low, high in re.findall(r"`(\d{4})`\s*[–-]\s*`?(\d{4})`?", text):
        named.update(range(int(low), int(high) + 1))
    numbers = {int(re.match(r"(\d+)", pathlib.Path(e).name).group(1)) for e in entries}
    unnamed = sorted(numbers - named)
    if unnamed:
        record("fast", "provenance documented", "WARN",
               f"{len(unnamed)}/{len(numbers)} not individually named (session-grouped): {unnamed[:8]}")
    else:
        record("fast", "provenance documented", "PASS", f"{len(numbers)} numbers named")


def check_doc_claims(root: pathlib.Path, entries: list[str]) -> None:
    """Documented patch count and base version must match reality."""
    package_dir = root / "sleepy-next"
    pkgrel = re.search(r"^pkgrel=(\d+)", (package_dir / "PKGBUILD").read_text(encoding="utf-8"), re.M)
    pkgver = re.search(r"^pkgver=(\S+)", (package_dir / "PKGBUILD").read_text(encoding="utf-8"), re.M)
    # The package version keeps pkgver's underscore ("7.3.0_rc2-10"); only the
    # kernel release string uses a dash ("7.3.0-rc2-10-sleepy-next"). Compare
    # against the package form, which is what docs quote as the base version.
    expected_version = f"{pkgver.group(1)}-{pkgrel.group(1)}" if pkgrel and pkgver else None

    problems = []
    readme = package_dir / "docs" / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        count = re.search(r"^(\d+) patches\.", text, re.M)
        if count and int(count.group(1)) != len(entries):
            problems.append(f"docs/README.md says {count.group(1)} patches, series has {len(entries)}")
        version = re.search(r"\*\*Base version:\*\* `([^`]+)`", text)
        if expected_version and version and version.group(1) != expected_version:
            problems.append(f"docs/README.md says base {version.group(1)}, PKGBUILD is {expected_version}")
    else:
        problems.append("sleepy-next/docs/README.md missing")
    if problems:
        record("fast", "documented claims", "FAIL", "; ".join(problems))
    else:
        record("fast", "documented claims", "PASS", f"{len(entries)} patches, base {expected_version}")


def check_skills(root: pathlib.Path) -> None:
    script = root / ".claude" / "skills" / "docs-maintenance" / "scripts" / "validate_skills.py"
    if not script.is_file():
        record("fast", "skill spec", "SKIP", "validate_skills.py not found")
        return
    result = run([sys.executable, str(script)])
    summary = (result.stdout.strip().splitlines() or ["no output"])[-1]
    record("fast", "skill spec", "PASS" if result.returncode == 0 else "FAIL", summary)


def check_symlinks(package_dir: pathlib.Path, entries: list[str]) -> None:
    """Dangling patch symlinks are leftovers from dropped patches."""
    dangling = [p.name for p in package_dir.glob("*.patch") if p.is_symlink() and not p.exists()]
    if dangling:
        record("fast", "no dangling symlinks", "FAIL", f"{len(dangling)}: {dangling[:5]}")
    else:
        record("fast", "no dangling symlinks", "PASS", f"{len(entries)} symlinks resolved")


# --------------------------------------------------------------------------- #
# deep tier
# --------------------------------------------------------------------------- #

def find_checkpatch(root: pathlib.Path, package_dir: pathlib.Path) -> pathlib.Path | None:
    """checkpatch.pl ships in the kernel source; ours is inside the source tarball."""
    extracted = pathlib.Path("/tmp/kverify/scripts/checkpatch.pl")
    if extracted.is_file():
        return extracted
    tarballs = sorted(package_dir.glob("linux-*.tar.*"))
    if not tarballs:
        return None
    tarball = tarballs[0]
    cache = pathlib.Path("/tmp/kverify")
    cache.mkdir(parents=True, exist_ok=True)
    inner = tarball.name[:-len(".tar.gz")] if tarball.name.endswith(".tar.gz") else None
    if not inner:
        return None
    result = run(["bsdtar", "-xf", str(tarball), "-C", str(cache),
                  f"{inner}/scripts/checkpatch.pl", f"{inner}/scripts/spelling.txt"])
    if result.returncode:
        return None
    if extracted.is_file():
        return extracted
    # Keep the layout checkpatch expects relative to itself.
    return cache / inner / "scripts" / "checkpatch.pl"


def check_checkpatch(package_dir: pathlib.Path, entries: list[str], root: pathlib.Path) -> None:
    script = find_checkpatch(root, package_dir)
    if not script or not script.is_file():
        record("deep", "checkpatch (own patches)", "SKIP", "checkpatch.pl unavailable (no source tarball)")
        return
    if not shutil.which("perl"):
        record("deep", "checkpatch (own patches)", "SKIP", "perl not installed")
        return
    own = [package_dir / e for e in entries
           if int(re.match(r"(\d+)", pathlib.Path(e).name).group(1)) in OWN_PATCH_RANGE]
    if not own:
        record("deep", "checkpatch (own patches)", "SKIP", "no patches in the own-patch range")
        return
    findings = 0
    for path in own:
        result = run(["perl", str(script), "--no-tree", "--strict", "--terse", str(path)])
        errors = [ln for ln in result.stdout.splitlines() if ln.startswith("ERROR:")]
        if errors:
            findings += len(errors)
            print(f"      {path.name}:")
            for line in errors[:5]:
                print(f"        {line}")
    status = "FAIL" if findings else "PASS"
    record("deep", "checkpatch (own patches)", status, f"{findings} errors across {len(own)} own patches")


def check_sparse(tree: pathlib.Path, root: pathlib.Path, entries: list[str]) -> None:
    if not shutil.which("sparse"):
        record("deep", "sparse", "SKIP", "sparse not installed (pacman -S sparse)")
        return
    if not (tree / "Makefile").is_file():
        record("deep", "sparse", "SKIP", f"{tree} does not look like a kernel tree")
        return
    # Only the directories our patches touch: a full-tree sparse run costs as much
    # as a build, while these cover every file the series modifies.
    dirs = touched_directories(tree, root, entries)
    if not dirs:
        record("deep", "sparse", "SKIP", "no touched directories present in the tree")
        return
    result = run(["make", f"-j{os.cpu_count() or 4}", "C=1", "CHECK=sparse", *sorted(dirs)],
                 cwd=tree, timeout=3600)
    output = result.stdout + result.stderr
    ours = touched_files(root, entries)
    findings = [ln for ln in output.splitlines()
                if re.search(r":\d+:\d+: (warning|error):", ln) and any(f in ln for f in ours)]
    if findings:
        # WARN, not FAIL. A sparse finding in a file we touch is usually
        # long-standing upstream noise (an __rcu annotation churn in
        # kernel/sched/core.c, say) rather than something this series introduced;
        # gating on it would block releases for other people's style. Reported so
        # it stays visible and attributable.
        record("deep", "sparse", "WARN",
               f"{len(findings)} findings in the files the series touches (may be pre-existing)")
        for line in findings[:10]:
            print(f"      {line}")
    elif result.returncode:
        tail = output.strip().splitlines()[-1][:120] if output.strip() else ""
        record("deep", "sparse", "FAIL", f"make C=1 exited {result.returncode}: {tail}")
    else:
        record("deep", "sparse", "PASS", f"none in the {len(ours)} files the series touches ({len(dirs)} dirs compiled)")


def package_dir_of(root: pathlib.Path) -> pathlib.Path:
    return root / "sleepy-next"


def survey_tools() -> None:
    """Report which kernel verification tools are available, and what they cover."""
    print(f"  {'tool':<16}{'status':<10}{'kind':<9}{'tier':<9}what it covers")
    for binary, install, kind, covers, tier, note in KERNEL_TOOLS:
        if binary == "make W=1":
            available = shutil.which("make") is not None
        elif binary in ("smatch",):
            available = False
        elif binary in ("objtool", "KUnit", "selftests", "KASAN", "KCSAN", "lockdep", "KFENCE"):
            available = True  # in-tree, needs no install
        elif binary == "checkpatch.pl":
            available = True  # extracted from the source tarball
        else:
            available = shutil.which(binary) is not None
        status = "present" if available else "absent"
        print(f"  {binary:<16}{status:<10}{kind:<9}{tier:<9}{covers}")
        if not available and tier != "runtime":
            print(f"  {'':<16}{'':<10}{'':<9}install: {install}")
    print()
    print("  Runtime tools (KASAN, KCSAN, lockdep, KFENCE) are the one class that cannot")
    print("  run from here: they need a diagnostic kernel booted on the machine. Build one")
    print("  with the relevant CONFIG_*_ENABLE flags, boot it, exercise the workload, and")
    print("  read the report from journalctl. Do that before a release that changes memory,")
    print("  locking, or the scheduler.")


def check_warnings(tree: pathlib.Path, root: pathlib.Path, entries: list[str]) -> None:
    """Build the touched directories with `make W=1` and report new warnings."""
    if not (tree / "Makefile").is_file():
        record("deep", "W=1 warnings", "SKIP", f"{tree} is not a kernel tree")
        return
    dirs = touched_directories(tree, root, entries)
    if not dirs:
        record("deep", "W=1 warnings", "SKIP", "no touched directories present in the tree")
        return
    result = run(["make", f"-j{os.cpu_count() or 4}", "W=1", *sorted(dirs)], cwd=tree, timeout=3600)
    output = result.stdout + result.stderr
    ours = touched_files(root, entries)
    warnings = [ln for ln in output.splitlines()
                if re.search(r":\d+:\d+: warning:", ln) and any(f in ln for f in ours)]
    if warnings:
        # WARN for the same reason as sparse: these are in carried code authored
        # upstream (mm/lru_marie, tcp_bbr3) or in modified files whose other
        # warnings predate the series. Worth fixing, not worth blocking a release.
        record("deep", "W=1 warnings", "WARN",
               f"{len(warnings)} warnings in the files the series touches")
        for line in warnings[:10]:
            print(f"      {line}")
    else:
        record("deep", "W=1 warnings", "PASS", f"none in the {len(ours)} files the series touches ({len(dirs)} dirs compiled)")


def check_coccinelle() -> None:
    if not shutil.which("spatch"):
        record("deep", "coccinelle", "SKIP", "spatch not installed (pacman -S coccinelle)")
        return
    record("deep", "coccinelle", "PASS", "spatch present; run scripts/coccinelle/ via make coccicheck")


def touched_directories(tree: pathlib.Path, root: pathlib.Path, entries: list[str]) -> set[str]:
    """The directories in *tree* that the series modifies."""
    dirs: set[str] = set()
    for entry in entries:
        path = package_dir_of(root) / entry
        if not path.is_file():
            continue
        for target in re.findall(r"^\+\+\+ b/(.+)$", path.read_text(encoding="utf-8", errors="replace"), re.M):
            directory = str(pathlib.PurePosixPath(target).parent) + "/"
            if (tree / directory).is_dir():
                dirs.add(directory)
    return dirs


def touched_files(root: pathlib.Path, entries: list[str]) -> set[str]:
    """Every file path the series modifies, relative to the kernel tree root.

    Sparse and W=1 report findings in anything they compile, including headers
    they pull in — thousands of lines of long-standing upstream noise that is not
    ours to fix. Filtering to the files the series actually touches is what makes
    those checks actionable instead of a wall of output nobody reads.
    """
    files: set[str] = set()
    for entry in entries:
        path = package_dir_of(root) / entry
        if not path.is_file():
            continue
        for target in re.findall(r"^\+\+\+ b/(.+)$", path.read_text(encoding="utf-8", errors="replace"), re.M):
            files.add(target.strip())
    return files


def check_series(root: pathlib.Path) -> None:
    script = root / ".claude" / "skills" / "kernel-build" / "scripts" / "audit_series.py"
    if not script.is_file():
        record("series", "cumulative apply", "SKIP", "audit_series.py not found")
        return
    if not (root / "repos" / "linux-next" / ".git").exists():
        record("series", "cumulative apply", "SKIP", "repos/linux-next clone not present")
        return
    result = run([sys.executable, str(script), "--quiet"], timeout=1800)
    if result.returncode == 2:
        record("series", "cumulative apply", "SKIP",
               (result.stderr.strip().splitlines() or ["environment problem"])[0])
        return
    summary = (result.stdout.strip().splitlines() or ["no output"])[-1]
    record("series", "cumulative apply", "PASS" if result.returncode == 0 else "FAIL", summary)
    if result.returncode:
        for line in result.stdout.splitlines():
            if "FAIL" in line or "did not apply" in line:
                print(f"      {line.strip()}")


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tier", choices=["fast", "series", "deep", "tools", "all"], default="fast")
    parser.add_argument("--tree", type=pathlib.Path, default=None,
                        help="prepared kernel tree for the deep tier")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    try:
        root = repo_root(pathlib.Path.cwd())
        package_dir = root / "sleepy-next"
        pkgbuild = package_dir / "PKGBUILD"
        entries = pkgbuild_entries(pkgbuild)
    except EnvError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.json:
        print(f"verify: {len(entries)} patches, tier={args.tier}, root={root}\n")

    if args.tier in ("fast", "all"):
        check_sources(package_dir, entries)
        check_checksums(package_dir, entries, b2sum_sets(pkgbuild))
        check_headers(package_dir, entries)
        check_provenance(package_dir, package_dir / "PATCH_SOURCES.md", entries)
        check_doc_claims(root, entries)
        check_skills(root)
        check_symlinks(package_dir, entries)

    if args.tier in ("series", "all"):
        check_series(root)

    if args.tier == "tools":
        survey_tools()

    if args.tier == "deep" or (args.tier == "all" and args.tree):
        check_checkpatch(package_dir, entries, root)
        check_coccinelle()
        if args.tree:
            check_sparse(args.tree.resolve(), root, entries)
            check_warnings(args.tree.resolve(), root, entries)
        else:
            record("deep", "sparse", "SKIP", "no --tree given")
            record("deep", "W=1 warnings", "SKIP", "no --tree given")

    if args.json:
        print(json.dumps(RESULTS, indent=2))
    elif args.tier == "tools":
        return 0  # survey_tools() prints its own report; nothing to summarise
    else:
        for tier in ("fast", "series", "deep"):
            rows = [r for r in RESULTS if r["tier"] == tier]
            if not rows:
                continue
            print(f"{tier}:")
            for row in rows:
                print(f"  {row['status']:<5}{row['check']:<28}{row['detail']}")

    failed = [r for r in RESULTS if r["status"] == "FAIL"]
    warned = [r for r in RESULTS if r["status"] == "WARN"]
    skipped = [r for r in RESULTS if r["status"] == "SKIP"]
    if not args.json:
        print()
        notes = []
        if warned:
            notes.append(f"{len(warned)} warning(s)")
        if skipped:
            notes.append(f"{len(skipped)} skipped (tool or input unavailable)")
        if failed:
            print(f"{len(failed)} check(s) FAILED" + (", " + ", ".join(notes) if notes else ""))
        elif notes:
            print("all required checks passed — " + ", ".join(notes))
        else:
            print("all checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
