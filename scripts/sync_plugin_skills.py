"""Synchronize canonical skills without deleting destination content.

Preflight both bundles before writing. Unexpected files and symlinks require
human reconciliation; --check is read-only. Use a single writer: this is not a
transaction across bundles, and interrupted copies are detected by --check.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

RUNTIME_FILES = ("check_python_contracts.py", "manage_state.py", "detect_project.py", "state_schema.json")


def tree_files(directory: Path, excluded: str | None = None) -> list[Path]:
    """Collect canonical files, rejecting symlinks before following content."""
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"expected a real source directory: {directory}")
    files: list[Path] = []
    for path in sorted(directory.rglob("*")):
        if excluded and path.relative_to(directory).parts[0] == excluded:
            continue
        if path.is_symlink():
            raise ValueError(f"source symlink is unsupported: {path}")
        if path.is_file():
            files.append(path)
        elif not path.is_dir():
            raise ValueError(f"unsupported source path: {path}")
    return files


def manifests(root: Path) -> dict[Path, dict[Path, Path]]:
    """Map each destination's relative file path to its canonical source."""
    core = {Path("SKILL.md"): root / "SKILL.md"}
    core.update({p.relative_to(root): p for p in tree_files(root / "references", "codex-skills")})
    core.update({Path("scripts") / name: root / "scripts" / name for name in RUNTIME_FILES})
    bundles: dict[Path, dict[Path, Path]] = {}
    for destination, names in (
        (root / "plugins/auto-coding/skills", ("verify-evidence", "setup-auto-coding")),
        (root / "skills", ("verify-evidence", "setup-auto-coding", "auto-coding-openspec")),
    ):
        expected = {Path("auto-coding") / relative: source for relative, source in core.items()}
        for name in names:
            expected.update({Path(name) / p.relative_to(root / name): p for p in tree_files(root / name)})
        bundles[destination] = expected
    return bundles


def preflight(root: Path, bundles: dict[Path, dict[Path, Path]]) -> list[str]:
    """Reject unsafe shapes and unexpected files in all bundles before writes."""
    problems: list[str] = []
    for destination, expected in bundles.items():
        for source in expected.values():
            if source.is_symlink() or not source.is_file():
                problems.append(f"missing or unsupported source: {source}")
        required_directories = {destination, *destination.parents}
        for relative in expected:
            required_directories.update((destination / relative).parents)
        for directory in sorted(required_directories):
            if directory == root or not directory.is_relative_to(root):
                continue
            if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
                problems.append(f"expected a real destination directory: {directory}")
        if destination.is_symlink():
            continue
        for path in sorted(destination.rglob("*")):
            relative = path.relative_to(destination)
            if path.is_symlink():
                problems.append(f"destination symlink is unsupported: {path}")
            elif path.is_dir():
                if relative in expected:
                    problems.append(f"expected a destination file: {path}")
            elif not path.is_file() or relative not in expected:
                problems.append(f"unexpected destination path; preserved: {path}")
    return sorted(set(problems))


def synchronize(root: Path, *, check: bool = False) -> list[str]:
    """Return preflight/drift reports; successful sync returns an empty list."""
    try:
        bundles = manifests(root)
    except ValueError as exc:
        return [str(exc)]
    problems = preflight(root, bundles)
    if problems:
        return problems
    for destination, expected in bundles.items():
        for relative, source in sorted(expected.items()):
            target = destination / relative
            if not target.exists() or target.read_bytes() != source.read_bytes():
                if check:
                    problems.append(f"bundle drift: {target.relative_to(root)}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args()
    try:
        problems = synchronize(Path(__file__).resolve().parent.parent, check=args.check)
    except OSError as exc:
        print(f"error: sync interrupted; inspect retained files and rerun --check: {exc}", file=sys.stderr)
        return 1
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print("Distribution bundles match canonical sources." if args.check else "Distribution bundles synchronized without deletion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
