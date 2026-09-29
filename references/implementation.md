---
name: implementation
description: Implement complete behavior, preserve consumers, and repair failures within the agreed boundary.
---

# Implement the Agreed Result

Inspect relevant definitions, callers, tests, and configuration before editing.
Read enough to understand behavior, including error paths and side effects;
line counts and symbol-search hits do not substitute for this understanding.
Resolve routine naming or location ambiguity through inspection.

Prefer existing code, standard-library/native facilities, and installed
components before new code or dependencies. Preserve abstractions that carry
compatibility, policy, lifecycle, observability, or test boundaries. A single
implementation or fewer lines is not sufficient reason to remove one. The reuse
principle is adapted from Ponytail; attribution lives in the repository's
THIRD_PARTY.md. Any dependency or deletion follows the applicable authority.

## Complete the behavior

Build a coherent slice including required consumers, configuration, entrypoints,
and failure handling. Keep speculative extensions out. Preserve trust-boundary
validation, data-loss protection, security, accessibility, and supported contracts.
A stub, TODO, mock-only path, or unconnected helper is incomplete when the user
requested working behavior.

Use a tight project-native feedback loop. Reproduce bugs and add meaningful
regression protection where warranted. Choose checks by the affected behavior,
not a fixed number of assertions or checks after every edit. Imports can execute
side effects; inspect them before using import-as-verification.

## Repair and continue

A failed check is input to diagnosis. Fix an in-scope defect and re-run affected
checks; do not stop simply because lint, type checking, or tests failed. Separate
baseline defects, new defects, unavailable environments, and unresolved causes
using evidence. Never weaken tests or validation to obtain a pass.

If repairs repeat a failure or introduce material regressions, stop patching
symptoms, preserve diagnostic evidence, and revisit the root cause. Resume with
an evidence-supported approach within scope. Stop the affected unit only when
further safe progress needs missing information, authority, or a wider boundary;
continue independent authorized work. Do not impose arbitrary retry counts or
continue the same unproductive loop indefinitely.

Inspect the diff before recovery. Reverse only the task's own changes with a
reviewed, permitted edit; preserve unrelated work. Recovery, generated artifacts,
and test cleanup are subject to the same deletion/effect restrictions.

## Contracts and debt

Prefer repository-native machine-readable contracts, then an applicable plan,
then the agreed behavior. Check relevant signatures, return shapes, failure
semantics, side effects, and consumers. Compilers cover structural checks for
TypeScript, Go, and Rust. For an explicit supported Python contract, the bundled
`scripts/check_python_contracts.py` adds a structural pre-check; an empty contract
or a successful AST match does not prove behavior.

Record deliberate limitations and any newly weakened type/validation boundary.
`Any`, `cast`, and suppressions require contextual judgment: their presence alone
is not a defect, but using them to hide an unresolved material issue prevents
completion. When the required contract is wrong or ambiguous, resolve the
material decision before building dependent behavior; do not silently accept a
new requirement or force an invalid implementation.
