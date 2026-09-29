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
| Import check | Use the configured module/build entry after checking import side effects |
| Behavior check | `node <file>.js` / the project's demo entry |
| Configured type check | `tsc --noEmit` |
| Project type check | `tsc --noEmit` over the whole project |
| Type check | `tsc --noEmit` |
| Lint | `eslint <modified files>` |
| Behavior tests / configured coverage | `jest --coverage` (or vitest equivalent) |

## Notes

- The structural contract checker (`scripts/check_python_contracts.py`) is
  Python-only. For TypeScript, use compiler checks and the relevant behavioral
  contract comparison in [implementation.md](implementation.md).
- Debug leftovers to scan for at the Standard gate: `console.log`,
  `debugger`.
- Unavailable checks follow [adaptive.md](adaptive.md): preserve required
  BLOCKED results, use labeled safe alternatives, and continue independent work.
