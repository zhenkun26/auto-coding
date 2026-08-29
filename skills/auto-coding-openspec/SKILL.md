---
name: auto-coding-openspec
license: MIT
description: >
  Optional companion skill for using auto-coding inside a repository that
  already uses OpenSpec. Read when the repository has `openspec/config.yaml`
  or the user explicitly asks for the OpenSpec workflow. Never run
  `openspec init` automatically.
---

# Auto-Coding for OpenSpec Repositories

OpenSpec is optional. The core auto-coding skill treats any existing planning
workflow as planning authority; this companion only adds the OpenSpec-specific
mechanics. Install it only when the repository already uses OpenSpec.

## Consuming planning artifacts

When the user hands off a change directory (`openspec/changes/<name>/`), first
resolve its current state and apply boundary through the installed OpenSpec
CLI. Use the returned `changeRoot`, `contextFiles`, and dynamic instruction
rather than assuming artifact paths or relying on chat history.

Then consume the applicable artifacts:

- `tasks.md` — functional task list. Entries may carry `fileHint`,
  `symbolHint`, and `dependsOn`; use them for decomposition and location.
- `specs/<capability>/spec.md` — interface contracts: the contract-comparison
  baseline and (Python) the input to `scripts/check_python_contracts.py`.
  Contracts must use concrete types, never `any` / `object` / `unknown`.
- `design.md` — technical approach and architecture decisions, when present.

OpenSpec artifacts are planning authority; current code, diffs, and executed
verification are acceptance authority. Stop before editing when artifacts are
blocked, stale, contradictory, or when required work would expand their scope.
Do not silently repair planning artifacts while implementing, and do not
create a second status tree beside OpenSpec.

## Task-checkbox sync (two checkpoints)

1. After a bounded task's implementation **and its scoped acceptance checks**
   pass, change the corresponding tasks.md entry from `- [ ]` to `- [x]`.
   Tasks satisfied by reuse are checked only after their existing behavior is
   verified, with `<!-- reused: <source> -->` appended.
2. Before delivery, reconcile tasks.md against the actual work once more.

Failed or blocked required checks leave the task unchecked. Facts first at
wrap-up: work factually complete but unchecked is checked without warning;
tasks genuinely incomplete are reported as incomplete — never silently
checked. Alternative evidence may narrow uncertainty but never upgrades
`BLOCKED` to completion.

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
