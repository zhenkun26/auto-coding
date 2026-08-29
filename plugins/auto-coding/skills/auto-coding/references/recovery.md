---
name: recovery
description: Cross-session recovery for auto-coding — when a single state file is justified and how to manage it with scripts/manage_state.py. Read when persistent state is justified.
---

# Recovery

Default to no persistent state. Use a state file only for a long or
interruption-prone task when the surrounding product does not already provide
reliable task state. Never use more than **one** state file.

## State file

Path: `ai_pipeline/state.json` (created on first use). Managed exclusively
through `scripts/manage_state.py`, which writes atomically (temp file +
rename) so a crash never leaves a torn file.

```bash
python scripts/manage_state.py init ai_pipeline/state.json --route Standard
python scripts/manage_state.py update ai_pipeline/state.json \
    --set phase=implement --set current_task=T003 \
    --set current_file=src/services/auth_service.py --set self_heal_round=0
python scripts/manage_state.py update ai_pipeline/state.json \
    --set resume_hint="mypy no-untyped-def on routes.py:93; add -> ReturnType"
python scripts/manage_state.py read ai_pipeline/state.json
python scripts/manage_state.py clear ai_pipeline/state.json
```

## Fields

| Field | Meaning |
|---|---|
| `route` | Fast / Standard / High-risk |
| `phase` | plan / implement / verify / handoff |
| `current_task` | Atomic task in flight |
| `current_file` | File being edited |
| `self_heal_round` | 0–3 |
| `escape_hatches` | List of `[ESCAPE_HATCH]` records for the run |
| `resume_hint` | Exact next action in one sentence |

Schema reference: `scripts/state_schema.json`.

List fields (`escape_hatches`) accept a JSON array literal (preferred — items
may contain `;`) or a legacy `;`-separated string, e.g.
`--set escape_hatches='["T001 import: Any; deferred"]'`.

## Write points

1. Before starting each task (implementation).
2. After each self-heal round (with `resume_hint` set to error + fix
   direction).
3. At the entry of the verification stage.
4. On handoff: mark completed (`clear`), do not delete the file
   automatically.

## Resuming

On a new invocation, if the state file exists and is non-empty, print the
exact breakpoint — phase, task, file, self-heal round — and ask:

```text
⚠️ Incomplete run detected. Last state: <phase>/<current_task>
(file: <current_file>, self-heal round <n>/3). Reply 'resume' to continue
from the breakpoint, or 'restart' to start fresh.
```

Never infer breakpoints from logs or reports; the state file is the only
authoritative source.

### Evidence staleness

A resumed session inherits the breakpoint, not the proof. Treat every
verification result from the earlier session — including every `PASS` —
as unverified, and re-run the gates the selected route requires before
building on them. Old command output in chat or reports is context, not
evidence.

### Resume or restart

- **Resume** when the state file, the working tree, and the governing
  plan still agree.
- **Restart** when the plan contradicts the repository, the diff is
  unrecognizable, or most recorded tasks can no longer be located. State
  the reason honestly before starting over.

Design rationale: the auto-coding repository's `docs/MEMORY_STRATEGY.md`
(four-layer memory model; rule 2 — evidence has a shelf life, rule 4 —
resume beats redo, redo beats a stale plan).
