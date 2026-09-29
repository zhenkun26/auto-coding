---
name: verification
description: Produce current, scope-matched evidence and resolve failures before claiming an outcome complete.
---

# Verification Evidence

| Result | Meaning |
|---|---|
| PASS | The check executed and met its criterion |
| FAIL | The check executed and found a defect |
| BLOCKED | A required check could not execute or produce usable evidence |
| NOT_APPLICABLE | The check does not apply, with a reason |

A required check left unrun remains missing evidence; do not call it
NOT_APPLICABLE. Alternative inspection can reduce uncertainty but does not
convert a blocked integration into a pass. Reports summarize raw results.

## Select and execute

Prefer the repository's own commands and supported environment. Start with the
changed behavior and relevant consumers, then required package, integration,
and repository gates. Assess commands for real-data, process, network, and
cleanup effects before running them. Fixtures and mocks must isolate effects
that are outside authority.

Cover applicable boundaries: defaults and overrides, invalid/missing inputs,
failure and recovery, compatibility, and state transitions. Use configured
coverage/eval thresholds; when none exist, justify checks from acceptance
criteria rather than inventing numeric thresholds or generating token tests.
Small documentation/formatting edits do not require new behavioral tests.

A unit test cannot establish a deployed integration or user journey. If the
requested result includes running the app, exercise the relevant path and
inspect the result. For agent skills, separately test script behavior and
sample the agent's actual actions; word matching in a prompt is not a behavior
evaluation. Respect authorization for runtime checks and model/tool costs.

Fix in-scope failures using [implementation.md](implementation.md). Missing
tools use [adaptive.md](adaptive.md). Baseline failures need actual baseline
support and an impact assessment; they are not automatically caused by the
change or harmless. Acceptance cannot silently weaken because a check failed.

## Bind and reuse evidence

For material results retain command/check, working directory, exit/result,
checked scope, content identity, and relevant environment/dependency context.
Content identity includes relevant staged, unstaged, and untracked work, not
just HEAD. Link retained output when recovery or audit requires it; exclude
secrets and unnecessary private data. Missing metrics are unknown, not zero.

Subsequent relevant code, test, dependency, environment, or acceptance changes
invalidate affected evidence. Re-run those checks after the final fixes. On
resume, reconcile identities and applicability; re-run anything changed or
not reliably identifiable. A new chat alone does not invalidate unchanged,
traceable evidence. External/live-system evidence may expire independently.

## Review and report

Check both requirement completion and code quality. Review the final content,
including relevant uncommitted and new files, against an identified base.
Use independent review for material cross-boundary or high-risk work, or when
requested and authorized. Disclose when independence is unavailable; never
label self-review independent. Resolve material in-scope findings and reverify
changed paths. Speculative improvements do not create new acceptance gates.

Report commands and results, what each proves, missing evidence and its impact,
remaining debt, and acceptance status. A tool exit code, reviewer's confidence,
or aggregate pass rate alone does not establish complete delivery.
