---
name: risk-controls
description: Select invariants, isolation, failure and recovery checks for actual high-impact behavior.
---

# High-Risk Effects

Before high-risk edits, record the relevant invariants, failure modes,
permitted effects, recovery approach, and acceptance evidence in the existing
plan or task record. Use only controls that apply to the actual change.

| Behavior | Evidence and controls |
|---|---|
| Money | Preserve required precision/rounding; exercise normal and boundary calculations with an appropriate exact representation |
| Authentication/authorization | Check allowed and denied paths, validation, expiry, and relevant failure modes; retain configured static and behavioral checks |
| Persistent data/migrations | Preserve compatibility and recovery; dry-run on isolated data; live execution requires authority |
| Consequential state transitions/concurrency | Check valid and invalid transitions, ordering, shared state, and recovery under relevant failures |
| External API behavior | Check requests, responses, errors, and actual integration when required; mocked tests alone do not establish external success |
| Service lifecycle | Check relevant startup, dependency readiness, failure/restart and shutdown behavior in an authorized isolated environment |

Trace relevant entry-to-effect paths and shared resources so tests cannot
silently reach real users, services, notifications, or persistent data. Use
existing factories, fixtures, and test seams. Crash drills and process actions
need the same authority as ordinary execution; a risk label never authorizes
those effects.

When a required runtime/control is unavailable, preserve that BLOCKED result,
perform safe useful alternatives, and explain the acceptance consequence.
Unrelated outcomes can continue. Plan recovery without destructive resets or
prohibited filesystem cleanup. Do not weaken a control merely to finish.
