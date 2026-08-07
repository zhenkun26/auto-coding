---
name: risk-controls
description: Mandatory controls for High-risk changes in auto-coding — per-flag controls for FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API / ENV_OPS, and the non-degradable verification baseline. Read whenever any risk flag is present.
---

# Risk Controls

Read this file whenever [routing.md](routing.md) assigns the High-risk route.
Risk overrides size: these controls apply even to a one-line change. A
High-risk task never degrades to a lighter route; when the environment blocks
a control, execute the alternative evidence and label it `BLOCKED` — never
skip silently.

## Per-flag controls

| Flag | Mandatory controls |
|---|---|
| **FINANCE** | Decimal/Fixed-Point arithmetic enforced; float/double forbidden. ≥2 self-check asserts per calculation (normal + boundary precision). Escape hatches on money paths classify as `HIGH_RISK`. |
| **AUTH** | Static type check must run — this is the one case where a missing configured tool still halts for install, and an unconfigured project requires line-by-line review as alternative evidence. Never weaken validation, token expiry, or error handling to make a check pass. |
| **MIGRATION** | Dry-run verification before execution; a written rollback script or recovery approach before editing; never run against production-like data without explicit authorization. |
| **STATE_MACHINE** | Self-check asserts = one per legal transition + one per illegal transition rejected. Transition table reviewed against the contract before implementation. |
| **EXTERNAL_API** | Runtime verification must include integration coverage: real integration tests, or — when the external system is unavailable/unmockable — ① unit tests over the calling logic, ② contract tests over request/response formats, ③ review of error-handling paths, labeled `[SKIP_INTEGRATION: external environment unavailable]` / `BLOCKED`. A clean unit test never proves an external integration works. |
| **ENV_OPS** | Mode D environment verification (see [verification.md](verification.md)): dependency readiness, startup liveness, crash-restart drill, exit-code/log probing. No real environment → dry-run + process-logic unit tests + restart-path review, labeled `[SKIP_ENV: no environment]` / `BLOCKED`. |

## Non-degradable baseline

Regardless of project configuration, the following verifications must execute
(in real or alternative-evidence form):

- Authentication/authorization/encryption changes → static type check.
- Data-persistence changes → runtime verification.
- External API calls → integration coverage (see EXTERNAL_API above).
- Service startup/keep-alive/process management → environment verification.

## Before editing

For High-risk tasks, record in writing before the first edit:

1. **Invariants** that must hold before, during, and after the change.
2. **Failure modes** the change can introduce.
3. **Rollback or recovery approach** (which files, which commands, which data).
4. **Acceptance evidence** that will demonstrate safety.
