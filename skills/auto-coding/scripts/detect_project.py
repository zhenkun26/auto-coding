#!/usr/bin/env python3
"""Read-only project detection for auto-coding.

Reports language template, CI, spec system, greenfield/brownfield state, and
tool availability as JSON on stdout. Makes no modifications and executes no
project tooling — its output is discovery evidence, not permission to install
or run anything.

Usage: python scripts/detect_project.py <project-root>
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs"}

TEMPLATES = [
    ("python", ["pyproject.toml"]),
    ("typescript", ["package.json", "tsconfig.json"]),
    ("go", ["go.mod"]),
    ("rust", ["Cargo.toml"]),
]

TOOLS = {
    "python": ["mypy", "ruff", "pytest"],
    "typescript": ["node", "tsc", "eslint", "jest"],
    "go": ["go"],
    "rust": ["cargo"],
}

CI_PATHS = [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", ".circleci"]

SOURCE_ROOT_CANDIDATES = ["src", "lib", "app", "pkg", "cmd"]


def detect_templates(root: Path) -> list[str]:
    """Return language templates whose flag files are all present."""
    return [
        name
        for name, flags in TEMPLATES
        if all((root / flag).exists() for flag in flags)
    ]


def detect_ci(root: Path) -> list[str]:
    """Return CI configurations present in the repository."""
    return [path for path in CI_PATHS if (root / path).exists()]


def detect_codebase_state(root: Path) -> dict[str, object]:
    """Report greenfield/brownfield state from all matching source roots.

    Every candidate directory that exists is reported in ``source_roots`` so
    layouts with several roots (e.g. ``src`` and ``cmd``) are not missed.
    The primary ``source_root`` is the one with the most source files.
    """
    hits: list[tuple[str, int]] = []
    for candidate in SOURCE_ROOT_CANDIDATES:
        source_root = root / candidate
        if not source_root.is_dir():
            continue
        count = sum(
            1
            for path in source_root.rglob("*")
            if path.suffix in SOURCE_EXTENSIONS and path.is_file()
        )
        hits.append((candidate, count))
    if not hits:
        return {
            "source_root": None,
            "source_roots": [],
            "state": "greenfield",
            "source_files": 0,
        }
    primary, _primary_count = max(hits, key=lambda item: item[1])
    total = sum(count for _name, count in hits)
    return {
        "source_root": primary,
        "source_roots": [name for name, _count in hits],
        "state": "brownfield" if total else "greenfield",
        "source_files": total,
    }


def detect_tools(templates: list[str]) -> dict[str, bool]:
    """Report which template tools are on PATH (no execution)."""
    names = {tool for template in templates for tool in TOOLS.get(template, [])}
    names.update(["git", "bash"])
    return {name: shutil.which(name) is not None for name in sorted(names)}


def _has_test_files(tests_dir: Path) -> bool:
    """Return True when a tests/ directory contains actual test modules."""
    if not tests_dir.is_dir():
        return False
    return any(
        path.is_file()
        and (path.name.startswith("test_") or path.name.endswith("_test.py"))
        for path in tests_dir.rglob("*.py")
    )


def detect_configs(root: Path) -> dict[str, bool]:
    """Report tool configuration presence (config exists vs tool installed)."""
    pyproject = root / "pyproject.toml"
    pyproject_text = (
        pyproject.read_text(encoding="utf-8", errors="replace")
        if pyproject.exists()
        else ""
    )
    return {
        "mypy": (root / "mypy.ini").exists()
        or (root / ".mypy.ini").exists()
        or "[tool.mypy]" in pyproject_text,
        "ruff": (root / "ruff.toml").exists()
        or (root / ".ruff.toml").exists()
        or "[tool.ruff]" in pyproject_text,
        "pytest": (root / "pytest.ini").exists()
        or (root / "setup.cfg").exists()
        or "[tool.pytest" in pyproject_text
        or '"pytest' in pyproject_text
        or _has_test_files(root / "tests"),
        "eslint": any(
            (root / name).exists()
            for name in (".eslintrc", ".eslintrc.js", ".eslintrc.json", "eslint.config.js", "eslint.config.mjs")
        ),
    }


def main(argv: list[str] | None = None) -> int:
    """Detect project shape and print the JSON report."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: detect_project.py <project-root>", file=sys.stderr)
        return 2
    root = Path(args[0]).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    templates = detect_templates(root)
    report = {
        "root": str(root),
        "templates": templates or ["custom"],
        "ci": detect_ci(root),
        "openspec": (root / "openspec" / "config.yaml").exists(),
        "git": (root / ".git").exists(),
        "codebase": detect_codebase_state(root),
        "tools": detect_tools(templates),
        "configs": detect_configs(root),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
