---
name: openspec
description: Using an existing OpenSpec workflow with auto-coding — artifact consumption, task-checkbox sync, and the sync/archive wrap-up. Read when the repository already uses OpenSpec.
---

# Working With an Existing OpenSpec Setup

Apply this file only when the repository already has `openspec/config.yaml`,
or the user explicitly asks to use OpenSpec. **Never run `openspec init`
automatically** — initializing a specification system requires authorization.
When OpenSpec is absent, plan inline per [planning.md](planning.md) and skip
this file entirely (`[NO_OPENSPEC]`).

## Consuming planning artifacts

When the user hands off a change directory (`openspec/changes/<name>/`):

- `tasks.md` — functional task list. Entries may carry `fileHint`,
  `symbolHint`, and `dependsOn`; use them for decomposition and location.
- `specs/<capability>/spec.md` — interface contracts: the L2 comparison
  baseline and (Python) the input to `scripts/check_python_contracts.py`.
  Contracts must use concrete types, never `any` / `object` / `unknown`.
- `design.md` — technical approach and architecture decisions, when present.

Requirement understanding is already done by these artifacts — refine them
into atomic tasks (see [planning.md](planning.md)); do not redo it.

## Task-checkbox sync (two checkpoints)

1. After each task completes (implementation), change the corresponding
   tasks.md entry from `- [ ]` to `- [x]`. `REUSED` tasks are checked too,
   with `<!-- reused: <source> -->` appended.
2. Before delivery, reconcile tasks.md against the actual work once more.

Unchecked items at wrap-up follow conflict ruling R8 (facts first — see
[conflict-rulings.md](conflict-rulings.md)).

## Wrap-up: sync and archive (authorized only)

After the change is delivered and verified, **suggest** the wrap-up — do not
run it unasked:

```bash
openspec sync-specs <change-name>     # merge delta specs into openspec/specs/
git add openspec/specs/ && git commit # requires commit authorization
openspec archive <change-name>        # move the change to archive/
```

Include these as follow-up actions in the handoff report. Sync and archive
both modify the repository and require the same authorization as a commit.
