---
name: toolchain-python
description: Python toolchain commands for auto-coding — type check, lint, test/coverage, self-check one-liners, and the structural contract checker. Read when the project is Python.
---

# Python Toolchain

Prefer commands declared by the repository (CI, Makefile, task runner,
`pyproject.toml` scripts) over the defaults below. Requires Python 3.10+ for
the contract checker.

## Commands

| Purpose | Command |
|---|---|
| Import check | `python -c "from <pkg> import <symbol>"` |
| Behavior check | `python -c "from <mod> import demo; demo()"` / `python <file>.py` / `python -m doctest <file>.py` |
| Configured type check | `mypy --strict <file>` (or `pyright <file>` when configured) |
| Project type check | `mypy --strict <all files written so far>` |
| Type check | `mypy --strict <modified files>` |
| Lint | `ruff check <modified files>` |
| Behavior tests / configured coverage | `pytest --cov=<src_dir> --cov-report=term -v` |
| Structural contract pre-check | `python scripts/check_python_contracts.py --spec <spec.md> --source <src_dir>` |

## Contract checker

`check_python_contracts.py` parses typed signatures from a spec file
(`name(a: int, b: int) -> int`, class-prefixed methods supported) — or
Gherkin endpoint contracts (`WHEN POST /path`) as a fallback — and compares
them against actual source via AST. Exit code 0 = structural match.

- Run it before the relevant behavioral contract comparison; fix structural issues
  first.
- Empty contract (no supported symbols) → it reports nothing checkable;
  **never** present that as contract verification — do the manual comparison
  and say so.
- It covers structural checks only; error codes and side effects still
  require manual review.

## Unavailable checks

Follow [adaptive.md](adaptive.md). Preserve configured checks as BLOCKED when
unavailable, identify the prerequisite, and continue independent work. Use existing
behavioral checks when no framework is configured; do not install or invent gates.
