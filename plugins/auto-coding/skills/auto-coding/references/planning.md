---
name: planning
description: Proportional planning for auto-coding — planning depth per route, atomic task decomposition, decision-grilling for unresolved design decisions, and spec-system usage. Read for Standard or High-risk tasks, or when the user requests a written plan.
---

# Proportional Planning

Plan only to the depth the route requires. The plan may live in the
conversation or in the single state file (see [recovery.md](recovery.md));
never create a dedicated plan file by default.

## Depth per route

- **Fast**: short internal checklist. No written plan unless the user asks.
- **Standard**: concise ordered plan with verification steps. Write it down
  when the change touches more than 5 files.
- **High-risk**: written record of invariants, failure modes, rollback or
  recovery approach, and acceptance evidence — before editing anything.

## Task decomposition (Standard and High-risk)

Refine the requirement into atomic tasks with a topological order. This is
engineering refinement only — do not redo requirement understanding that a
spec system already did.

**Bounded-task principles**:

1. One outcome: the task delivers one behavior or contract result.
2. One primary risk boundary: do not combine independently hazardous effects,
   migrations, or compatibility changes merely because they share a feature.
3. One acceptance gate: the task has evidence that can pass, fail, or block
   independently of later tasks.

Implementation code, focused tests, and a directly required contract update
may stay together when they form that one result. Split when outcomes have
independently meaningful acceptance results, different rollback boundaries,
or can be reverted safely as separate checkpoints.

**Ordering rules**:

- Data model layer → business service layer → external interface layer.
- A depended-on task executes before its dependents; run tasks serially, never
  in parallel.
- When the requirement comes from a spec system, each task traces back to its
  spec entry; decomposition only refines and adds tasks, never removes them.
  A task satisfied by reuse is marked `REUSED` and kept for traceability —
  reuse wins over the original plan; never silently drop or re-implement it.

**Red lines**:

- A task spanning unrelated files, outcomes, or risk boundaries, or described
  with vague connectives ("etc.", "and also") → split it.
- A task with no identifiable target file → mark `[AMBIGUOUS]` and ask.
- Orphaned task with an implied dependency → annotate `[GUESSED_DEP]`.

**Self-check requirement per task** (used by the behavior pass in
[implementation.md](implementation.md)):

| Code type | Minimum self-check |
|---|---|
| Ordinary function | ≥1 assert covering the happy path |
| State machine (M legal + K illegal transitions) | ≥(M+K) asserts |
| Data validation | ≥1 valid-input assert + ≥1 per invalid input type |
| Algorithm-intensive (merge/encode/encrypt/compress) | ≥3 asserts across input scenarios |
| Financial calculation | Decimal enforced + ≥2 asserts (normal + boundary precision) |
| Trivial (≤3 lines, no branches; pure data class; docs/config only) | `[TRIVIAL]` — no self-check |

## Decision-grilling

When the task surfaces **3 or more unresolved design decisions**, stress-test
the design before planning further:

1. Ask one question at a time; wait for the answer before continuing.
2. Offer 2–4 concrete options per question. Reserve yes/no choices for
   genuinely binary decisions.
3. If a question can be answered by exploring the codebase, explore instead of
   asking.
4. Walk each branch of the decision tree until resolved, then summarize all
   decisions made before proceeding.

Do not grill for Fast tasks or for decisions with an obvious default — make
the narrow, reversible assumption and state it.

## Spec systems

- When the repository already uses a spec workflow (OpenSpec, spec-kit, …),
  plan inside it and treat its artifacts as planning authority; acceptance
  stays with repository evidence. OpenSpec-specific mechanics live in the
  optional `auto-coding-openspec` companion skill at the repository root.
- When no spec system exists, plan inline: requirements, interface contract,
  edge conditions, and tasks in one concise block. Interface contracts must
  use concrete types — never `any` / `object` / `unknown`.
- Do **not** initialize a specification system automatically. If a spec system
  would clearly help, suggest it once and let the user decide.
