---
name: verification
description: Verification gates for auto-coding — evidence states, static gate (Critical type check / Standard lint), runtime verification modes A/B/C/D, threshold table, escape-hatch audit, and cumulative degradation warning. Read for every implementation task.
---

# Verification

Verify with the project's own tools and report exact evidence. Every check
ends in exactly one state:

- `PASS` — executed and satisfied the stated criterion.
- `FAIL` — executed and found a defect.
- `BLOCKED` — could not execute (dependency, credential, service, permission).
- `NOT_APPLICABLE` — the check does not apply to the changed behavior.

Never convert `BLOCKED` into `PASS`. Degradation is not skipping: a degraded
check still requires alternative evidence, labeled as alternative evidence
(see [adaptive.md](adaptive.md) for when degradation is allowed).

## Static gate

### Critical — type check (blocking)

- Python: `mypy --strict <modified files>`; TypeScript: `tsc --noEmit`.
- On type errors: **halt immediately**. Do not attempt fixes — implementation
  already had its self-heal rounds; a type error here is structural. Roll back
  the modified files (`git checkout -- <files>`), output the full error log,
  and request human intervention.
- Configured-but-missing tool → show the install command and halt (no
  degradation). No type-check config → degrade to IDE diagnostics + line-by-line
  review, reported as `BLOCKED` + alternative evidence (see adaptive.md).

### Standard — lint (self-healing)

- Python: `ruff check <modified files>`; TypeScript: `eslint <modified files>`.
- Also scan for debug leftovers (`print()`/`breakpoint()`/`console.log`/
  `debugger`), unused variables, naming conventions.
- Self-heal at most 3 rounds. Violations remaining after round 3 →
  `[MANUAL_REQUIRED]`, listed explicitly in the handoff report.
- Detect fix-oscillation (fix A → breaks B → fix B → breaks A) and force-exit
  to `[MANUAL_REQUIRED]` instead of looping.

### Escape-hatch audit (non-blocking)

Scan `ai_pipeline/ERROR_MEMORY.md` and the modified files for `[ESCAPE_HATCH]`
entries and `Any` / `# type: ignore` / `cast()` workarounds introduced during
implementation:

- Classify each: `LOW_RISK` (contained scope), `MEDIUM_RISK` (public API
  boundary), `HIGH_RISK` (e.g. on a FINANCE calculation).
- Escape hatches do not block delivery, but every one must be listed in the
  handoff report with its risk class. `HIGH_RISK` items get a prominent
  warning.

### Over-engineering review (advisory, non-blocking)

Review the diff for reinvented standard-library features, unnecessary
dependencies, and speculative abstractions. Findings are informational only —
append them to the handoff report; never block the gate on them.

## Runtime verification

Choose the mode by priority:

| Priority | Condition | Mode |
|---|---|---|
| 1 | User specified a mode | As specified |
| 2 | Project matches the AI-agent feature list below | Mode B (Eval baseline) |
| 3 | Change carries the ENV_OPS flag | Mode D (environment verification) |
| 4 | Tool library / SDK / server-side | Mode A (test coverage) |
| 5 | Cannot determine | Mode C (A then B) |

### Mode A — test coverage

- Run the project's test runner with coverage (Python: `pytest --cov=<src>
  --cov-report=term -v`).
- Unit test pass rate must be 100%; line coverage ≥ 80%; branch coverage
  ≥ 70%; modified-file coverage ≥ project threshold (default 80%).
- **Test-composition transparency**: report one line —
  `Tests: N unit + M integration = T total` (integration = files importing
  `TestClient` or matching `test_api*.py`). Informational only; thresholds are
  unchanged.
- No test files exist → generate a minimal test skeleton from the change, then
  run it.

### Mode B — Eval baseline

AI-agent feature list (any hit): LLM API calls; agent/ReAct loop; tool-calling
schemas; RAG retrieval component. Run the project's eval suite; each metric
defaults to ≥ 80%. No eval configuration → generate minimal cases from the
contract's edge conditions, or degrade to Mode A (`[SKIP_MODE_B: no
baseline]`).

### Mode C — combined

Run Mode A first; after it passes, run Mode B. Evaluate each independently.

### Mode D — environment verification (ENV_OPS)

0. Dependency readiness: probe external dependencies (DB/Redis/MQ ports or
   health checks); verify start-order and wait/retry strategy — the service
   must wait, not crash, when dependencies are not ready.
1. Startup liveness: start with the modified method; process/port/log probes
   pass 100%.
2. Crash-restart drill: kill the main process; confirm the keep-alive strategy
   restarts it (≥1 pass).
3. Exit codes and error logs match expectations for failure scenarios.

No real environment or no process-management permission → alternative
evidence: startup-script dry-run + unit tests for process-management logic +
review of restart/error paths, labeled `[SKIP_ENV: no environment]` /
`BLOCKED`.

### Threshold ruling

| Condition | Ruling | Action |
|---|---|---|
| All metrics meet thresholds, no FAILED tests | `PASS` | Proceed to handoff |
| Metrics at 90–100% of threshold, reasonable cause | ⚠️ release with warning | Deliver; list follow-up items explicitly |
| FAILED tests, or metrics below 90% of threshold | `FAIL` | Halt; embed input/expected/actual for each failure; request human intervention |

## Default thresholds

Single source of truth. CI-declared thresholds override these defaults.

| Config item | Default | Overridable by CI |
|---|---|---|
| Layer 0 timeout | 5 s | No |
| Layer 1 timeout | 30 s | No |
| Self-heal round cap | 3 rounds | No |
| Line coverage | ≥ 80% | Yes |
| Branch coverage | ≥ 70% | Yes |
| Modified-file coverage | ≥ project threshold (default 80%) | Yes |
| Single test/eval case timeout | 60 s (timeout = FAILED) | No |
| Eval metric threshold | ≥ 80% | Yes |
| Type-check gate | Critical; failure → halt + rollback | No |

## Cumulative degradation warning

Count every degraded check (`BLOCKED` + alternative evidence). At handoff:

- Degraded items ≥ 50% of total verification items → prominent warning in the
  handoff report and the suggested commit-message footer: "⚠️ N/M verification
  items degraded due to environment limits; focus human review on: <list>".
- Below 50% → record normally.
