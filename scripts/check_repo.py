"""Repository-level mechanical checks for the auto-coding skill product.

Checks:
1. Every relative Markdown link resolves to an existing file (dirname-aware).
2. Every SKILL.md carries a ``license: MIT`` frontmatter entry.

Exit code is nonzero when any check fails. Standard library only.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PARTS = {".git", "plugins", ".codex"}
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")


def iter_markdown_files() -> list[Path]:
    """Return all Markdown files under the repo root except generated bundles."""
    return [
        path
        for path in REPO_ROOT.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.parts)
    ]


def check_relative_links() -> list[str]:
    """Return broken relative-link reports across all Markdown files."""
    problems: list[str] = []
    for path in iter_markdown_files():
        for match in LINK_PATTERN.finditer(path.read_text(encoding="utf-8")):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "/")):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                problems.append(f"{path.relative_to(REPO_ROOT)} -> {target}")
    return problems


def check_skill_licenses() -> list[str]:
    """Return SKILL.md files whose frontmatter lacks a MIT license field."""
    problems: list[str] = []
    for path in REPO_ROOT.rglob("SKILL.md"):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if "license: MIT" not in text.split("---", 2)[1]:
            problems.append(str(path.relative_to(REPO_ROOT)))
    return problems


def main() -> int:
    """Run all checks and report failures."""
    link_problems = check_relative_links()
    license_problems = check_skill_licenses()

    if link_problems:
        print("BROKEN RELATIVE LINKS:")
        for problem in link_problems:
            print(f"  {problem}")
    if license_problems:
        print("SKILLS MISSING license: MIT:")
        for problem in license_problems:
            print(f"  {problem}")

    if link_problems or license_problems:
        return 1
    print("check_repo: all relative links and skill licenses OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
