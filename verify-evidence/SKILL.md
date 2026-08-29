---
name: verify-evidence
license: MIT
description: >
  Standalone evidence discipline for AI coding agents — verify with the
  project's own toolchain and report PASS / FAIL / BLOCKED / NOT_APPLICABLE
  exactly. Use for any implementation task where verification claims must be
  trustworthy; works with or without the full auto-coding skill.
---

# Verify Evidence

Never claim a check you did not run, and never dress up what you could not
run as a pass. Verification evidence is the only currency this skill deals in.

## The four evidence states

Report every check with exactly one state:

- `PASS` — executed and satisfied the stated criterion.
- `FAIL` — executed and found a defect.
- `BLOCKED` — could not execute because a dependency, credential, service, or
  permission was unavailable.
- `NOT_APPLICABLE` — the check does not apply to the changed behavior.

Rules:

- Never convert `BLOCKED` into `PASS`, and never report a check as executed
  when it was inferred, simulated, skipped, or blocked.
- Degradation is not skipping: a degraded check still requires alternative
  evidence, labeled as such.
- A pass that relies on `Any`, `# type: ignore`, or `cast()` is recorded debt,
  never a clean pass.

## How to verify

Prefer commands the repository itself declares — CI configuration, task
runner, package manager scripts — over ones you invent. Run in this order:
focused checks for the changed behavior, then neighboring contracts (callers
and adjacent interfaces), then the repository's wider gates.

Match the toolchain to the project (Python: pytest/ruff/mypy; TypeScript:
tsc/eslint/jest; Go: go test/vet; Rust: cargo test/clippy). Do not install
missing tools without authorization; report the gap as `BLOCKED` with the
exact missing dependency.

For a Python project with an explicit structured contract, a deterministic
pre-check exists in the auto-coding skill (`scripts/check_python_contracts.py`
— function presence, parameter counts, return annotations). Structural
pre-checks never replace behavioral verification.

## Stale evidence

Evidence has a shelf life. After any behavior change, earlier `PASS` results
for affected paths are invalid and must be re-run. After resuming an
interrupted session, treat every verification result from the earlier session
as unverified until re-executed.

## Report format

```text
Verification
- <command>  →  PASS
- <command>  →  FAIL (<defect>)
- <command>  →  BLOCKED (<missing dependency>)
- <check>    →  NOT_APPLICABLE (<reason>)
Recorded debt: <escape hatches / weakened checks, or "none">
```

Attach the evidence block to every handoff; a claim without an evidence line
is treated as unverified.
