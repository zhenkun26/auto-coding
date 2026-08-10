---
name: implementation
description: Implementation protocol for auto-coding — reuse ladder, brownfield location method, per-task loop with immediate type checks and layer checkpoints, escape-hatch recording, and the L0/L1/L2 three-layer self-check. Read for every implementation task.
---

# Implementation

Understand first, modify second. The shortest working diff wins — but only
when you actually traced what the change touches.

## The reuse ladder

Stop at the first rung that holds:

1. Does this feature really need to exist? (YAGNI — if speculative, say so in
   one sentence and skip)
2. Already in the codebase? → reuse
3. Can the standard library do it? → stdlib
4. Does a native platform feature cover it? → native
5. Can an installed dependency solve it? → use what exists
6. Can it be done in one line? → one line
7. Last resort: minimal working code

Rules:

- No unrequested abstractions: no single-implementation interfaces, no
  factories for one product, no config that never changes.
- Deletion over addition. Boring over clever.
- Never add a dependency when the repository or standard library already
  provides a suitable solution without documenting the tradeoff.
- Mark deliberate simplifications with `# ponytail: <limit>, <upgrade path>`
  comments so they read as intent, not ignorance. (Ladder adapted from the
  Ponytail skill, MIT — see THIRD_PARTY.md.)
- **Bug fixes = root cause, not symptom.** Grep every caller of the function
  you are about to modify; fix once, where all callers converge.

**No-laziness boundaries** — never simplify away: input validation at trust
boundaries, error handling that prevents data loss, security measures,
accessibility basics, anything explicitly required.

**Money rule**: any code involving amounts, prices, billing, or financial
calculations uses Decimal/Fixed-Point arithmetic — float/double is forbidden.

## Brownfield location

For MODIFY/DELETE tasks in an existing codebase, locate before editing:

1. Infer candidate paths from the task's target file/symbol and directory
   conventions; use `rg` for class/function names.
2. Pin the symbol: AST/LSP where available, otherwise `rg -n` for exact lines.
   ADD tasks need an insertion point (end of file/class or after the most
   relevant symbol).
3. Read enough context around the target (≈15 lines each side) to understand
   the modification point.
4. Uniqueness check (hard gate): the same symbol name in multiple files with
   no way to decide → `[CONFLICT]`, halt and ask. Target symbol not found →
   `[NOT_FOUND]`, halt and ask. Located name differs from the task's name →
   annotate `[APPROXIMATE_MATCH]` and re-verify before implementing.
5. Line numbers drift after each edit — re-confirm the current position of the
   target symbol before every subsequent task.

Greenfield: skip location entirely; every file is new.

## Per-task loop

Execute tasks serially, in topological order:

1. Update the state file (when in use — see [recovery.md](recovery.md)) with
   the current task/file.
2. Generate complete code in the project's existing style, with complete type
   annotations and necessary imports. For values requiring precise computation
   or complex regexes, get deterministic results by running a one-liner
   instead of hand-writing them.
3. Inject in place with the editing tool; confirm scope with `git diff`
   afterwards so unrelated changes are never included.
4. **Immediate type check** (Python: `mypy --strict <file>`; TypeScript:
   `tsc --noEmit`). On error: fix and re-run, at most 3 rounds. Still failing
   after round 3 → halt, preserve the failed working state, report the exact
   errors and affected task files, and ask for human intervention. Never use
   version-control restore commands automatically: they cannot distinguish the
   task's edits from pre-existing user changes in the same file.
5. **Layer-level checkpoint**: after each topological layer (models, services,
   api...), run the type checker over **all files written so far** — per-file
   checks miss cross-file type errors. Fix before entering the next layer;
   never defer to the verification stage.
6. **Escape-hatch detection**: a self-heal that "passes" via `Any`,
   `# type: ignore`, `cast()`, or `Callable[..., Any]` as a last resort is not
   a true pass. Record it immediately (see
   [sedimentation.md](sedimentation.md)) as `[ESCAPE_HATCH]` with the original
   error, the workaround, and the type safety lost. It does not block, but it
   is quality debt and must surface in the handoff report.
7. Run the L0/L1/L2 self-check below and the task's scoped acceptance checks.
   Only when all required evidence passes is the task complete.
8. When the repository uses OpenSpec, check off the corresponding tasks.md
   entry only after that evidence passes — see [openspec.md](openspec.md).

Hard constraint: code with type errors must never leave implementation.

## Repair-regression fuse

The three-round cap bounds any one self-heal loop. Stop earlier when two
consecutive repair rounds in the same bounded task introduce a new failure in
a declared acceptance path or preserved contract. This is a material repair
regression, not an ordinary syntax correction.

On trigger:

1. stop adding patches and preserve the current diagnostic state;
2. record the original reproduction, governing invariant, each introduced
   regression, and the test or observation that exposed it;
3. review the root cause and caller boundary;
4. split or replan the task by independently accepted outcome before resuming.

Do not keep alternating symptom fixes until the generic round cap is exhausted.

## Three-layer self-check (L0/L1/L2)

After each task's code injection:

### Layer 0 — syntax and imports

| Property | Value |
|---|---|
| Command | Python: `python -c "from <pkg> import <symbol>"`; TS: `node -e "require('./dist/<file>')"` |
| Timeout | ≤ 5 s |
| Pass | Exit code 0, no Import/Syntax/ModuleNotFound errors |
| Self-heal | typos / missing imports / circular imports, ≤ 3 rounds |
| Limit exceeded | `[BLOCKED: L0]` — skip this task, finish the others, then request human intervention |
| Skip | Pure config/docs, no code change |

### Layer 1 — behavior self-check

| Property | Value |
|---|---|
| Form | `demo()`, `__main__`, doctest, or plain asserts — run it |
| Timeout | ≤ 30 s |
| Pass | All asserts pass, exit code 0 |
| Self-heal | read the stack, fix, re-run, ≤ 3 rounds |
| Limit exceeded | `[BLOCKED: L1]` with input/expected/actual/stack |
| Skip | Trivial code → `[TRIVIAL: no self-check]` |

Coverage baseline: per-task requirements are defined in
[planning.md](planning.md) (self-check requirement table).

### Layer 2 — interface contract comparison

Compare against the contract baseline (spec system artifacts, or the inline
contract from planning). Five items: ① name matches; ② parameters
(name/type/required) match; ③ return structure matches; ④ error codes match;
⑤ side effects match.

- Type mismatch → Critical; fix the code.
- Extra field in code not in contract → `[EXTRA_FIELD]` (concise addition,
  non-blocking) or `[COMPAT_FIELD]` (deliberate compatibility field; record
  the reason and suggest updating the spec).
- Code correct but contract wrong → conflict ruling R6
  ([conflict-rulings.md](conflict-rulings.md)).
- Pure refactor with unchanged interface → `[REFACTOR: contract unchanged]`.

**Automated structural pre-check** (Python): run
`python scripts/check_python_contracts.py --spec <spec.md> --source <src_dir>`
before the manual comparison to catch missing functions, parameter-count
mismatches, and missing return annotations. Fix structural issues first, then
do the manual five-item comparison (error codes and side effects still require
review). Never claim contract verification when the contract contains no
supported symbols.

Report each layer exactly: `L0 (import): PASS`, `L1 (self-check): PASS, N
asserts`, `L2 (contract): 5/5 matched` — or the corresponding `FAIL` /
`BLOCKED` / `NOT_APPLICABLE`.
