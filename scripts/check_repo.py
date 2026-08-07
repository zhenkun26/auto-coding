"""Repository-level mechanical checks for the auto-coding skill product.

Checks:
1. Every relative Markdown link resolves to an existing file (dirname-aware).
2. Every SKILL.md carries a ``license: MIT`` frontmatter entry.
3. README.md and README-EN.md have identical heading structures.

Exit code is nonzero when any check fails. Standard library only.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PARTS = {".git", "plugins", ".codex"}
LINK_PATTERN = re.compile(r"\]\(([^)]+)\)")


def read_text_safely(path: Path) -> str:
    """Read a text file, warning to stderr and returning '' on unreadable input."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"WARNING: cannot read {path}: {exc}", file=sys.stderr)
        return ""


def iter_markdown_files(root: Path | None = None) -> list[Path]:
    """Return all Markdown files under the repo root except generated bundles."""
    if root is None:
        root = REPO_ROOT
    return [
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.parts)
    ]


def check_relative_links(root: Path | None = None) -> list[str]:
    """Return broken relative-link reports across all Markdown files."""
    if root is None:
        root = REPO_ROOT
    problems: list[str] = []
    for path in iter_markdown_files(root):
        for match in LINK_PATTERN.finditer(read_text_safely(path)):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "/")):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                problems.append(f"{path.relative_to(root)} -> {target}")
    return problems


def check_skill_licenses(root: Path | None = None) -> list[str]:
    """Return SKILL.md files whose frontmatter lacks a MIT license field."""
    if root is None:
        root = REPO_ROOT
    problems: list[str] = []
    for path in root.rglob("SKILL.md"):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        text = read_text_safely(path)
        frontmatter_parts = text.split("---", 2)
        if len(frontmatter_parts) < 2 or "license: MIT" not in frontmatter_parts[1]:
            problems.append(str(path.relative_to(root)))
    return problems


def check_readme_heading_structure(root: Path | None = None) -> list[str]:
    """Return reports when the Chinese and English README heading structures differ."""
    if root is None:
        root = REPO_ROOT
    heading_levels = {}
    for name in ("README.md", "README-EN.md"):
        path = root / name
        levels = [
            len(line) - len(line.lstrip("#"))
            for line in read_text_safely(path).splitlines()
            if line.startswith("#")
        ]
        heading_levels[name] = levels

    if heading_levels["README.md"] != heading_levels["README-EN.md"]:
        return [
            (
                "README heading structures differ: "
                f"README.md={heading_levels['README.md']} vs "
                f"README-EN.md={heading_levels['README-EN.md']}"
            )
        ]
    return []


def main() -> int:
    """Run all checks and report failures."""
    link_problems = check_relative_links()
    license_problems = check_skill_licenses()
    readme_problems = check_readme_heading_structure()

    if link_problems:
        print("BROKEN RELATIVE LINKS:")
        for problem in link_problems:
            print(f"  {problem}")
    if license_problems:
        print("SKILLS MISSING license: MIT:")
        for problem in license_problems:
            print(f"  {problem}")
    if readme_problems:
        print("README HEADING STRUCTURE MISMATCH:")
        for problem in readme_problems:
            print(f"  {problem}")

    if link_problems or license_problems or readme_problems:
        return 1
    print("check_repo: links, skill licenses, and README heading structure OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
