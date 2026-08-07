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
| L0 import check | `python -c "from <pkg> import <symbol>"` |
| L1 behavior check | `python -c "from <mod> import demo; demo()"` / `python <file>.py` / `python -m doctest <file>.py` |
| Immediate type check (per task) | `mypy --strict <file>` (or `pyright <file>` when configured) |
| Layer checkpoint | `mypy --strict <all files written so far>` |
| Static gate — Critical | `mypy --strict <modified files>` |
| Static gate — Standard | `ruff check <modified files>` |
| Runtime — Mode A | `pytest --cov=<src_dir> --cov-report=term -v` |
| Structural contract pre-check | `python scripts/check_python_contracts.py --spec <spec.md> --source <src_dir>` |

## Contract checker

`check_python_contracts.py` parses typed signatures from a spec file
(`name(a: int, b: int) -> int`, class-prefixed methods supported) — or
Gherkin endpoint contracts (`WHEN POST /path`) as a fallback — and compares
them against actual source via AST. Exit code 0 = structural match.

- Run it before the manual L2 five-item comparison; fix structural issues
  first.
- Empty contract (no supported symbols) → it reports nothing checkable;
  **never** present that as contract verification — do the manual comparison
  and say so.
- It covers structural checks only; error codes and side effects still
  require manual review.

## Degradation

Per [adaptive.md](adaptive.md): configured-but-missing mypy/ruff/pytest →
show the install command and halt; no config → `BLOCKED` + alternative
evidence (IDE diagnostics / code review / behavior self-check).
