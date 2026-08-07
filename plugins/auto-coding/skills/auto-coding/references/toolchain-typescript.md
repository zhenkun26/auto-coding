---
name: toolchain-typescript
description: TypeScript/JavaScript toolchain commands for auto-coding — type check, lint, test, and self-check one-liners. Read when the project is TypeScript or JavaScript.
---

# TypeScript / JavaScript Toolchain

Prefer commands declared by the repository (CI, `package.json` scripts, task
runner) over the defaults below.

## Commands

| Purpose | Command |
|---|---|
| L0 import check | `node -e "require('./dist/<file>')"` |
| L1 behavior check | `node <file>.js` / the project's demo entry |
| Immediate type check (per task) | `tsc --noEmit` |
| Layer checkpoint | `tsc --noEmit` over the whole project |
| Static gate — Critical | `tsc --noEmit` |
| Static gate — Standard | `eslint <modified files>` |
| Runtime — Mode A | `jest --coverage` (or vitest equivalent) |

## Notes

- The structural contract checker (`scripts/check_python_contracts.py`) is
  Python-only. For TypeScript contracts, do the manual L2 five-item
  comparison in [implementation.md](implementation.md).
- Debug leftovers to scan for at the Standard gate: `console.log`,
  `debugger`.
- Degradation follows [adaptive.md](adaptive.md): configured-but-missing
  tsc/eslint/jest → show the install command and halt; no config → `BLOCKED`
  + alternative evidence.
