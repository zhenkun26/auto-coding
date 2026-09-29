---
name: verify-evidence
license: MIT
description: Check whether implementation and completion claims are supported by current, scope-matched verification evidence.
---

# Verify Evidence

Use repository-native checks and distinguish their outcomes:

- `PASS`: executed and met its criterion.
- `FAIL`: executed and found a defect.
- `BLOCKED`: a required check could not execute or produce usable evidence.
- `NOT_APPLICABLE`: irrelevant to this change, with a reason.

An omitted required check is missing evidence. Alternative inspection does not
turn a blocked integration into PASS. A test count, report, reviewer assertion,
or successful structural check alone does not prove the requested behavior.

Select checks from the agreed outcome, affected consumers, and repository gates.
Inspect side effects before execution, including tests and cleanup. Honor existing
authority for installations and external effects. Start focused, then cover the
required integration/runtime paths and wider gates. Fix in-scope failures and
rerun affected checks rather than handing ordinary repairs back to the user.

Retain command, working directory, exit/result, scope, checked content (including
relevant uncommitted files), environment and dependency context when needed for
recovery. Report limitations and distinguish tests from semantic review.

Relevant later changes invalidate affected results. On resume, reconcile identities
and applicability; rerun changed or untraceable checks. A new conversation alone
does not invalidate unchanged, traceable evidence. Live external evidence may
expire even without a code change.

Before claiming completion, reconcile every requested outcome, inspect the final
diff, resolve material findings, and update existing delivery records. Continue
remaining authorized work. A genuine blocker names the affected outcome, evidence,
missing prerequisite, and next action; it is not a completed outcome. Preserve
unrelated work, test strength, and explicit scope/authority boundaries.
