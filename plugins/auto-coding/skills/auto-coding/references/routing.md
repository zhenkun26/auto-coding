---
name: routing
description: Route selection for auto-coding — Fast / Standard / High-risk by uncertainty and operational risk, with risk-flag escalation and greenfield/brownfield detection. Read for every task.
---

# Routing

Choose exactly one route before any planning or implementation. Principle:
**don't do work that isn't worth doing** — and **risk overrides size**.

## Route table

| Route | Typical use | Heuristics | Required depth |
|---|---|---|---|
| **Fast** | Typo, small bugfix, single-field addition | 1 file, 0 new capabilities, no risk flags | Inspect, edit, L0/L1 self-check, focused verification |
| **Standard** | Small to medium multi-file change | 2–10 files, 1–2 new capabilities, single or cross module, no risk flags | Concise plan, caller-aware implementation, static checks and tests |
| **High-risk** | Platform/subsystem, or any risk flag | >10 files, ≥3 new capabilities, **or any risk flag below** | Written invariants + rollback plan, staged implementation, risk-specific verification, full verification gates |

Heuristics are guides, not gates. When in doubt between two routes, pick the
heavier one and say why in one sentence.

## Risk-flag escalation

When a change involves any of the following, the route is **High-risk
regardless of file count**. A one-line money or auth change is High-risk.

| Flag | Trigger condition |
|---|---|
| FINANCE | Amounts, billing, price calculations |
| AUTH | Authentication, authorization, encryption |
| MIGRATION | Data migration (DDL, data backfill) |
| STATE_MACHINE | State machine transitions |
| EXTERNAL_API | External API integration |
| ENV_OPS | Service startup/keep-alive/process management (background execution, daemon, restart policies) |

For each active flag, [risk-controls.md](risk-controls.md) defines mandatory,
non-degradable controls. A High-risk task may never fall back to a lighter
route, even when tools are missing — only alternative-evidence degradation is
allowed (see [adaptive.md](adaptive.md)).

## Greenfield / brownfield detection

The route is independent of codebase state. Codebase state only changes
**planning and location depth**:

- Check the project source root (default `src/`, or the language equivalent)
  for existing source files.
- No source files → `[GREENFIELD]`: every task is a new file; skip location
  work entirely and keep the plan to a summary (paths + symbols + order).
- Source files exist → `[BROWNFIELD]`: locate definitions and consumers before
  editing contracts; MODIFY/DELETE tasks need exact insertion points (see
  [implementation.md](implementation.md)).

`python scripts/detect_project.py <root>` performs this detection read-only.

## Scale protection

When the decomposed task count exceeds ~50 atomic tasks, stop and suggest
splitting the change into 2–3 independent changes. Only proceed in full when
the user explicitly says to continue.

## Route audit

When the route affects execution depth (Standard or High-risk), print one line
before substantial work:

```text
[ROUTE] <Fast|Standard|High-risk>: <N> files, <M> new capabilities, risk flags: <list|none>, <greenfield|brownfield>
```
