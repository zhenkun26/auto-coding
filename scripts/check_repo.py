"""Repository-level mechanical checks for the auto-coding skill product.

Checks:
1. Every relative Markdown link resolves to an existing file (dirname-aware).
2. Every SKILL.md carries a ``license: MIT`` frontmatter entry or is covered by
   an exact, repository-approved MIT vendor override.
3. README.md and README-EN.md have identical heading structures.
4. Every language detected by ``detect_project.py`` has a routed toolchain reference.

Exit code is nonzero when any check fails. Standard library only.
"""

import re
import sys
from pathlib import Path

from detect_project import TEMPLATES

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PARTS = {".git", "plugins", ".codex"}
VENDOR_MIT_ROOTS = {Path("references/codex-skills")}
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
    """Return skills lacking MIT frontmatter or an approved vendor override."""
    if root is None:
        root = REPO_ROOT
    problems: list[str] = []
    for path in root.rglob("SKILL.md"):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root)
        if any(relative.is_relative_to(vendor_root) for vendor_root in VENDOR_MIT_ROOTS):
            continue
        text = read_text_safely(path)
        frontmatter_parts = text.split("---", 2)
        if len(frontmatter_parts) < 2 or "license: MIT" not in frontmatter_parts[1]:
            problems.append(str(relative))
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


def check_toolchain_routes(root: Path | None = None) -> list[str]:
    """Return detected templates missing a reference file or SKILL.md route."""
    if root is None:
        root = REPO_ROOT
    skill_text = read_text_safely(root / "SKILL.md")
    problems: list[str] = []
    for template, _manifests in TEMPLATES:
        relative = Path("references") / f"toolchain-{template}.md"
        if not (root / relative).is_file():
            problems.append(f"missing toolchain reference for {template}: {relative}")
        if relative.as_posix() not in skill_text:
            problems.append(f"SKILL.md does not route detected template {template}: {relative}")
    return problems


def main() -> int:
    """Run all checks and report failures."""
    link_problems = check_relative_links()
    license_problems = check_skill_licenses()
    readme_problems = check_readme_heading_structure()
    toolchain_problems = check_toolchain_routes()

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
    if toolchain_problems:
        print("TOOLCHAIN ROUTING GAPS:")
        for problem in toolchain_problems:
            print(f"  {problem}")

    if link_problems or license_problems or readme_problems or toolchain_problems:
        return 1
    print("check_repo: links, skill licenses, README headings, and toolchain routes OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
