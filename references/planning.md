---
name: planning
description: Frame outcomes, decisions, dependencies, and boundaries for work that benefits from a plan.
---

# Plan to Completion

A useful plan answers: what result, why this approach, what stays protected,
what is outside scope, what evidence establishes completion, and where to stop.
Use the repository's plan or status convention. Keep short work inline; persist
only when coordination or recovery needs it, or the user asks for a written plan.

## Decisions

Investigate technical facts. Ask about consequential product choices, conflicting
requirements, or missing authority, with concrete options and a recommendation.
One consequential decision is sufficient reason to ask; numerous routine choices
are not. Stop interviewing once implementation is sufficiently determined.
A bounded prototype or investigation may settle uncertainty, but is not the
production deliverable unless that is what the user requested.

## Delivery units

Prefer one complete, independently verifiable behavior per unit. Include its
necessary code, tests, wiring, and contract updates. Sequence by real dependencies;
architectural layers may guide implementation within a unit, not force separate
unfinished deliveries. Migrations and broad refactors may need compatible
intermediate states and distinct recovery boundaries.

Outline later outcomes; detail only the current one. Adjust methods when facts
change, preserving the approved result and constraints. Do not silently shrink
acceptance to fit the implementation. Record completed, remaining, blocked, and
explicitly deferred outcomes; deferral requires the user's applicable decision.

## Boundaries and phase work

Use module or behavior boundaries unless exact file ownership is necessary.
Distinguish read-only investigation, permanent edits, temporary diagnostic edits,
and external effects. Check tests/builds for side effects too. If a prohibited
operation is required for an outcome, block that outcome before dependent edits;
do not deliver a permitted half that cannot stand alone.

When an identified phase governs this request, use its current STEP and STATUS,
validate the handoff as the repository requires, and respect its role ownership.
The executor cannot change acceptance, approve its own phase, or create a
successor. Return a conflict with evidence to the planner rather than inventing
a parallel plan. Known, reviewed drift can be reconciled by the authorized
owner; unexplained boundary or authority drift is a blocker.

Within an end-to-end authorization, continue through the agreed outcomes. A
phase-specific authorization stops at its boundary. Independent parallel work
requires authorized delegation, non-overlapping writes, and isolated test
resources; otherwise execute sequentially.
