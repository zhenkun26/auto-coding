---
name: sedimentation
description: Optional knowledge sedimentation for auto-coding — the ERROR_MEMORY standing artifact, escape-hatch records, TECH_NOTES, and ponytail debt tracking. Read when a self-heal, escape hatch, or Critical failure occurred.
---

# Sedimentation

Default: **no sedimentation**. Process files are not created for ordinary
runs. Only two artifacts may persist, and only on the conditions below.

## ERROR_MEMORY.md (the one standing artifact)

Location: `ai_pipeline/ERROR_MEMORY.md`. It exists to make the next run
smarter — read it at task entry when present.

**Append an entry immediately when any of these occurs** (never batch at the
end; at most one entry may be lost to a crash):

- A self-heal happened (any layer, any round).
- An escape hatch was taken (`[ESCAPE_HATCH]`).
- A Critical failure, `[BLOCKED]`, or ⚠️ release-with-warning occurred.

Entry format:

```markdown
- [ISO timestamp] <task/node> <layer>: <error description>, fix: <what fixed it>, prevention: <how to avoid next time>
```

Escape-hatch format:

```markdown
- [ISO timestamp] [ESCAPE_HATCH] <task> <layer>: <original error>, workaround: <Any/type:ignore/cast>, risk: <what type safety was lost>
```

Group entries under a run header (`## YYYY-MM-DD — <change summary>`), oldest
first. Append via read → concatenate → write, or atomically:

```bash
printf '%s\n\n%s' "$(cat ai_pipeline/ERROR_MEMORY.md 2>/dev/null)" "$entry" > ai_pipeline/ERROR_MEMORY.md
```

**Feedback loop**: when the same file or module accumulates escape hatches
across runs, review that module before implementing in it next time.

## TECH_NOTES.md (optional, High-risk or on request)

For High-risk work, or when the user asks for durable rationale, distill the
run into `ai_pipeline/TECH_NOTES.md`:

- §1 Implementation decisions (ADR): background / approach / rationale /
  impact, one per significant decision.
- §2 Known issues and pitfalls: severity-sorted, including every
  release-with-warning item and escape hatch.

Do not duplicate functional specs — this file records *why*, not *what*.

## Ponytail debt (optional)

Deliberate simplifications marked `# ponytail: <limit>, <upgrade path>` in the
source can be collected at wrap-up:

```bash
grep -rn "ponytail:" src/
```

Append findings as `<file>:<line> | <limit> | <upgrade path>` to
`ai_pipeline/PONYTAIL_DEBT.md` when the user wants a debt ledger. Do not
create the ledger unasked.
