---
name: completion
description: Reconcile the agreed outcome, final changes, evidence, and task state before ending delivery.
---

# Completion Review

Use this review at outcome boundaries, not after every edit. For a trivial
change it can remain an internal check.

1. **Outcome:** compare the original request and accepted changes with the
   actual result. Account for every in-scope result: complete, blocked, or
   explicitly deferred by the user. Code presence is not functional integration.
2. **Evidence:** required checks apply to the final content. Resolve material
   failures, review findings, and missing verification before claiming complete.
   Report baseline failures and any remaining limitations honestly.
3. **Boundary:** inspect the complete task diff, including staged, unstaged,
   and relevant new files. Preserve unrelated work. Verify that tests, build
   artifacts, dependencies, temporary experiments, and remote effects stayed
   within authority. Confirm experimental restoration when applicable.
4. **Continuity:** update the existing task/delivery record with decisions,
   remaining work, evidence pointers, and the precise next action. Preserve the
   completed record. Record only useful verified lessons in long-term knowledge.
5. **Delivery:** commit completed task changes when already authorized by the
   user or applicable repository workflow. Otherwise hand off the verified diff.
   Push, PR, merge, and deployment remain distinct actions requiring their own
   authority. Report the commit when made and the current acceptance status.

## When to continue or stop

Continue routine integration, in-scope repairs, required verification, and
remaining authorized outcomes. Do not offer these as optional next work or
request permission already granted. Progress updates keep the user informed
without ending execution.

A legitimate blocker states the affected outcome, evidence, attempted resolution,
missing prerequisite/decision/authority, and next action. Stop dependent work,
continue independent work, and mark unfinished outcomes incomplete. A partial
handoff may be necessary but is not a completed increment. Honor explicit user
pauses, budgets, and phase boundaries; persistence never widens authorization.

A final summary or a state-helper success is not acceptance evidence. Scripts
can check records; semantic completeness still requires inspecting the result.
