#!/usr/bin/env python3
"""Validate every SKILL.md against the Agent Skills specification.

The specification lives at https://agentskills.io/specification and its own
reference validator (`skills-ref`) is a separate checkout, so this implements the
normative checks directly. Run it after adding or editing a skill:

    python3 .claude/skills/docs-maintenance/scripts/validate_skills.py

Checks, per skill:

* `name` — 1-64 characters, lowercase letters/digits/hyphens only, no leading or
  trailing hyphen, no consecutive hyphens, and it MUST match the directory name.
* `description` — non-empty, at most 1024 characters, written in the third person.
* frontmatter — present, and every key is one the spec defines (Claude Code
  extensions such as `disable-model-invocation` are allowed).
* `compatibility` — 1-500 characters when present.
* body — under 500 lines.
* references — one level deep (a reference file must not link another `.md`), and
  any reference over 100 lines carries a table of contents.

Exit status: 0 when every skill passes, 1 on violations, 2 when the skills
directory cannot be found.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Keys the Agent Skills specification defines.
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

# Additional keys Claude Code accepts beyond the specification.
CLAUDE_CODE_KEYS = {"disable-model-invocation", "model", "argument-hint", "tools"}

# Second-person and first-person openings that break skill discovery, which the
# authoring guide requires to be third person.
NON_THIRD_PERSON = re.compile(r"\b(I can|I will|I help|You can use|You should|You can)\b")

BODY_LINE_LIMIT = 500  # specification: "Keep your main SKILL.md under 500 lines"
TOC_LINE_THRESHOLD = 100  # authoring guide: add a TOC beyond ~100 lines


class ValidationError(RuntimeError):
    """The skill set could not be validated at all."""


def logical(block: str) -> str:
    """Collapse a YAML block scalar into a single line."""
    body = block.strip()
    if body[:1] in (">", "|"):
        body = body[1:]
    return " ".join(line.strip() for line in body.splitlines() if line.strip())


def check_skill(path: pathlib.Path) -> list[str]:
    """Return the violations for one skill (empty when it passes)."""
    directory = path.parent.name
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return ["no YAML frontmatter (or it is not delimited by '---' lines)"]
    frontmatter, body = match.groups()

    keys = set(re.findall(r"^([A-Za-z_-]+):", frontmatter, re.M))
    name_match = re.search(r"^name:\s*(\S+)", frontmatter, re.M)
    desc_match = re.search(r"^description:\s*(.*?)(?=^[A-Za-z_-]+:|\Z)", frontmatter, re.S | re.M)
    description = logical(desc_match.group(1)) if desc_match else ""

    if not name_match:
        problems.append("missing 'name'")
    else:
        name = name_match.group(1)
        if not 1 <= len(name) <= 64:
            problems.append(f"'name' is {len(name)} characters (must be 1-64)")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            problems.append(f"'name' {name!r} has characters outside [a-z0-9-]")
        if name.startswith("-") or name.endswith("-"):
            problems.append(f"'name' {name!r} starts or ends with a hyphen")
        if "--" in name:
            problems.append(f"'name' {name!r} contains consecutive hyphens")
        if name != directory:
            problems.append(f"'name' {name!r} does not match directory {directory!r}")

    if not description:
        problems.append("missing or empty 'description'")
    elif len(description) > 1024:
        problems.append(f"'description' is {len(description)} characters (max 1024)")
    if NON_THIRD_PERSON.search(description):
        problems.append("'description' is not written in the third person")

    compat = re.search(r"^compatibility:\s*(.*)$", frontmatter, re.M)
    if compat and not 1 <= len(compat.group(1).strip()) <= 500:
        problems.append("'compatibility' is not 1-500 characters")

    unknown = keys - SPEC_KEYS - CLAUDE_CODE_KEYS
    if unknown:
        problems.append(f"frontmatter has keys the spec does not define: {sorted(unknown)}")

    body_lines = len(body.splitlines())
    if body_lines >= BODY_LINE_LIMIT:
        problems.append(f"body is {body_lines} lines (must be under {BODY_LINE_LIMIT})")

    for reference in sorted(path.parent.glob("references/*.md")) + sorted(path.parent.glob("reference*.md")):
        ref_text = reference.read_text(encoding="utf-8")
        if re.search(r"\]\([^)]*\.md", ref_text):
            problems.append(f"{reference.name} links another .md file (references must stay one level deep)")
        ref_lines = len(ref_text.splitlines())
        if ref_lines > TOC_LINE_THRESHOLD and not re.search(
            r"^##+ *(contents|table of contents)", ref_text, re.M | re.I
        ):
            problems.append(f"{reference.name} is {ref_lines} lines with no table of contents")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skills-dir", type=pathlib.Path, default=None, help="default: .claude/skills")
    args = parser.parse_args()

    skills_dir = args.skills_dir
    if skills_dir is None:
        # Walk up so the script works from anywhere in the checkout.
        here = pathlib.Path.cwd()
        for candidate in [here, *here.parents]:
            if (candidate / ".claude" / "skills").is_dir():
                skills_dir = candidate / ".claude" / "skills"
                break
    if skills_dir is None or not skills_dir.is_dir():
        print("error: could not find a .claude/skills directory. Pass --skills-dir.", file=sys.stderr)
        return 2

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(f"error: no */SKILL.md found under {skills_dir}", file=sys.stderr)
        return 2

    failures = 0
    print(f"Validating {len(skill_files)} skills in {skills_dir}\n")
    for path in skill_files:
        problems = check_skill(path)
        status = "ok  " if not problems else "FAIL"
        print(f"  {status} {path.parent.name}")
        for problem in problems:
            print(f"         - {problem}")
        failures += bool(problems)

    print()
    if failures:
        print(f"{failures} of {len(skill_files)} skills violate the specification.")
        return 1
    print(f"All {len(skill_files)} skills satisfy the Agent Skills specification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
