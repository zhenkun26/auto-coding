---
name: conflict-rulings
description: Conflict rulings for auto-coding — what wins when requirements, reuse opportunities, specs, and task checklists disagree. Read when a conflict occurs.
---

# Conflict Rulings

Facts first; then these four rulings, in order of precedence.

## R1 — Requirement existence

**Trigger**: the reuse ladder judges a feature unnecessary, but the spec (or
the user) has confirmed it.
**Ruling**: the spec wins. Implement the requirement with the least code.
YAGNI applies to speculative features, not to confirmed ones. When the user
insists on the full version of anything, build it and stop arguing.

## R2 — Code reuse

**Trigger**: an existing implementation is found that the plan did not
account for.
**Ruling**: reuse wins. Use the existing implementation; mark the
corresponding task `REUSED` and keep it in the plan for traceability — do not
implement it, do not delete it from the record. When the repository uses
OpenSpec, check its tasks.md entry with a `<!-- reused: <source> -->`
annotation.

## R6 — Design defect

**Trigger**: implementation reveals the spec is incomplete or wrong (and the
code is right).
**Ruling**: the spec's intent wins over blind implementation. Roll back the
affected change, output a defect report, and resume after the user updates
the spec.

Grading:

| Grade | Meaning | Action |
|---|---|---|
| Critical | Structural defect | Fall back immediately |
| Standard | Omission | Complete current work, then fall back |
| Advisory | Optimizable | Record as a known issue, continue |

## R8 — Task checklist unchecked

**Trigger**: a spec system's task checklist (e.g. OpenSpec tasks.md) has
unchecked items at wrap-up.
**Ruling**: facts first.

- Work factually complete but boxes unchecked → check them, no warning.
- Tasks genuinely incomplete (skipped/not implemented) → say so explicitly in
  the handoff report; do not silently check them off. `REUSED` counts as
  complete.
- When a CLI asks "incomplete task(s), continue?" and the work is factually
  complete → proceed.
