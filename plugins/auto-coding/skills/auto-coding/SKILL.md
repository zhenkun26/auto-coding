---
name: auto-coding
license: MIT
description: >
  Carry a bounded code change through planning, implementation, verification,
  and delivery. Use for features, fixes, or refactors that need coordinated
  execution; keep questions, reviews, and trivial edits in their direct workflow.
---

# Auto-Coding

Complete the agreed outcome with methods chosen for the project. Give capable
agents discretion over implementation; make scope, authority, evidence, and
completion explicit. Keep ordinary work lightweight.

## Delivery contract

- Establish the requested result, protected behavior, non-goals, and acceptance
  evidence from the request and repository. Inspect current changes first.
- Honor existing authorization throughout its scope. Follow applicable rules
  for dependencies, local commits, remote actions, and deletion; this skill
  grants none. Preserve unrelated work and secrets.
- Continue authorized work through required integration, verification, and
  in-scope repairs. A plan, scaffold, green unit test, or progress update is
  not a substitute for the requested deliverable.
- Stop on completion, an explicit user pause or scope limit, or a concrete
  blocker that cannot safely be resolved. Continue independent authorized work.
- Match claims to inspected code and actual results. Checklists and summaries
  describe evidence; they do not create it.

## Workflow

1. **Orient and decide.** Read the relevant repository instructions, current
   Git state, existing plan, and necessary code. Resolve technical facts
   yourself. Ask only for consequential choices or missing authority. Keep a
   research-only request read-only. Use `scripts/detect_project.py` only when
   the project or toolchain is unclear.
2. **Plan the result.** Choose Fast, Standard, or High-risk by impact and
   uncertainty; consult [routing](references/routing.md) if unclear. A small
   task needs only an internal checklist. For coordinated work, use
   [planning](references/planning.md) to state outcomes, dependencies, acceptance,
   and boundaries. Reuse an applicable project plan. Unrelated phase files do
   not establish authority. Resolve material product decisions before building.
3. **Implement completely.** Use [implementation](references/implementation.md)
   when behavior or consumers need coordinated changes, and
   [risk controls](references/risk-controls.md) for actual high-risk effects.
   Adjust routine methods within scope; resolve failures rather than returning
   ordinary repairs as optional follow-ups. Reopen a decision only when new
   evidence materially changes the outcome, protected contract, or authority.
4. **Verify and repair.** Use [verification](references/verification.md) for
   nontrivial acceptance and only the relevant toolchain reference below.
   Run appropriate project checks, inspect their results, and fix in-scope
   defects. Missing tools use [adaptation](references/adaptive.md). Repeat
   affected checks after changes; successful unaffected checks need not loop.
5. **Close the outcome.** Use [completion](references/completion.md) to reconcile
   the original request, final diff, evidence, and remaining work. Perform the
   required review and resolve material findings. Update the existing delivery
   record, commit when authorized, and report the result and genuine limitations.
   Continue the next outcome only if the authorization includes it.

## Memory and specialized work

Use one existing task-state authority. Only standalone work needing recovery
gets an optional record through [recovery](references/recovery.md); small tasks
create no process files. Preserve completed records. On resume, reconcile the
record with current code, boundaries, and evidence before proceeding.

Preserve useful decisions in the project's existing knowledge records. Read
[learning](references/sedimentation.md) when a verified, non-obvious lesson
would prevent recurrence or substantial rediscovery; ordinary repair logs do
not belong in standing instructions.

For an explicitly requested evidence-based cleanup audit, use
[simplification](references/simplification.md). Existing specification systems
remain optional planning inputs; do not initialize one merely to use this skill.

## Toolchain references

Consult these only when native commands or contract checks need guidance:

- Python: [toolchain-python](references/toolchain-python.md)
- TypeScript / JavaScript: [toolchain-typescript](references/toolchain-typescript.md)
- Go: [toolchain-go](references/toolchain-go.md)
- Rust: [toolchain-rust](references/toolchain-rust.md)

The host enforces execution permissions. This skill coordinates judgment and
checks; it is not a sandbox, a scheduler, or proof that an agent always complies.
