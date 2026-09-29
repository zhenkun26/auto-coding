---
name: recovery
description: Recover interrupted work from one authoritative task record and reconcile evidence with the current repository.
---

# Task Memory and Recovery

Use the project's existing plan/status authority. Do not create `state.json`
beside an applicable STATUS/STEP or equivalent merely because this skill loaded.
For short work, the current diff and conversation suffice. For standalone long
work without an existing record, choose one retained path and use the optional
`scripts/manage_state.py` helper.

## Minimal useful record

Keep the objective, protected boundary and authorization, governing plan pointer,
completed and remaining outcomes, blockers, evidence pointers with content identity,
and exact next action. These are information needs, not a mandatory file template.
Update at meaningful progress, decisions, blockers, or handoff, not every tool call.

For the optional helper (resolve paths relative to the installed skill):

```bash
python scripts/manage_state.py init <state-path> --route Standard
python scripts/manage_state.py update <state-path> \
  --set 'objective=Deliver the agreed user-visible behavior' \
  --set 'boundary=Approved modules and effects; protected contracts' \
  --set 'remaining=["Wire the entrypoint and verify the user path"]'
python scripts/manage_state.py read <state-path>
python scripts/manage_state.py update <state-path> \
  --set 'completed=["Entrypoint and behavior verified"]' \
  --set 'remaining=[]' --set 'blockers=[]' \
  --set 'evidence=["Retained result path, command, content identity and environment"]'
python scripts/manage_state.py complete <state-path> --summary 'Agreed outcome verified'
```

The helper preserves completed records and refuses initialization over an existing
file. Choose a distinct task path for a new task; do not erase the old record.
`clear` is a deprecated alias for `complete` and requires the same summary and
completion checks. It no longer writes `{}`. Legacy populated records can be
read and enriched in place; completion requires explicit empty `remaining` and
`blockers` lists, not absent fields. Legacy empty records contain no recoverable evidence.
Failed atomic writes retain their temporary file and report its path. One writer
owns a record; the helper does not lock concurrent writers or enforce permissions.
Its completion checks validate recorded fields, not the truth of agent claims.

Choose an evidence location that survives the needed handoff. An ignored or
machine-local path is not automatically versioned or available on another host.
Never store credentials or unnecessary private data in task state.

## Resume

Read the task record, governing decisions, current Git/diff and relevant artifacts.
Resolve discrepancies before editing. Completed records are historical context,
not permission to restart. Explicit user pauses and phase boundaries remain in
force until the user authorizes continuation.

If the request already authorizes continuation and the state agrees, state the
next action and proceed without asking again. Investigate routine drift yourself;
ask only when conflicting outcome, boundary, authority, or evidence needs a
consequential decision. Preserve superseded decisions and record their replacement.

Reconcile retained verification using [verification.md](verification.md): rerun
checks invalidated by relevant changes or unreliable identity. Do not inherit
an unsupported PASS or redo all verified work merely because the chat changed.
