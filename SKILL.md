---
name: auto-coding
license: MIT
description: >
  Plan, implement, verify, and hand off code changes — from a vague idea to a
  reviewed diff. Use when asked to explore a requirement, build a feature, fix a
  bug, refactor, or modify a repository end to end. Route work by uncertainty and
  operational risk; reuse before writing; verify with the project's own tools;
  require explicit authorization for spec initialization, installs, commits,
  deployments, and destructive operations.
---

# Auto-Coding

Deliver the smallest change that satisfies the request, with planning depth and
verification evidence proportional to its risk. Reuse beats standard library
beats installed dependencies beats new code.

## Core contract

1. Read repository instructions, spec systems, and working-tree state before editing.
2. Preserve user-owned and unrelated changes.
3. Classify the task as Fast, Standard, or High-risk before any planning.
4. Never plan deeper than the route requires; never create process files by default.
5. Reuse existing implementations before writing new ones.
6. Verify with the project's native toolchain and report `PASS` / `FAIL` /
   `BLOCKED` / `NOT_APPLICABLE` exactly. Never convert `BLOCKED` into `PASS`.
7. Initialize spec systems, install dependencies, commit, push, deploy, migrate,
   or delete only with explicit authorization.

Treat source diffs, command output, and test results as proof. Do not treat
generated reports as proof.

## Workflow

### 1. Establish scope and authority

- Read `AGENTS.md`, repository instructions, CI configuration, and `openspec/`
  if the repository already uses it.
- Inspect version-control status before editing when the project uses version control.
- Identify the requested outcome, acceptance evidence, affected interfaces, and
  actions that require additional authorization.
- Ask only when a missing choice would materially change the result or authorize
  a new side effect. Otherwise make a narrow, reversible assumption and state it.
- If `ai_pipeline/ERROR_MEMORY.md` exists, read it before planning (see
  [references/sedimentation.md](references/sedimentation.md)).

Run `python scripts/detect_project.py <project-root>` when project shape or
available toolchains are not already obvious. Its JSON reports language template,
CI, spec system, greenfield/brownfield state, and tool availability. Treat the
output as discovery evidence, not as permission to install or execute tools.

Establish exactly one execution boundary before routing implementation risk:

- **Standalone**: derive one outcome, explicit non-goals, affected interfaces,
  and acceptance evidence from the request and repository. Do not create a
  phase-document tree for a bounded change.
- **OpenSpec-managed**: resolve the applicable change with `openspec status`
  and its apply instructions, then treat the returned artifacts as planning
  authority. Repository diffs and executed checks remain acceptance authority.
  Do not create a competing `STATUS.md` / `STEP_*.md` system.
- **Not yet bounded**: when the request contains multiple independently
  accepted outcomes or contradicts its governing artifacts, stop before
  implementation and propose or update the specification boundary.

### 2. Select a route

Read [references/routing.md](references/routing.md) and choose exactly one route:

| Route | Typical use | Required depth |
|---|---|---|
| Fast | Localized, clear, low-risk, easily reversible | Inspect, edit, L0/L1 self-check |
| Standard | Multi-file behavior, interface change, or meaningful uncertainty | Concise plan, caller-aware implementation, static checks and tests |
| High-risk | FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API / ENV_OPS, concurrency, or destructive behavior | Written invariants and rollback plan, staged implementation, risk-specific verification |

Risk overrides size. A one-line authorization or money change is High-risk.
State the route in one sentence before substantial work when it affects
execution depth.

### 3. Plan proportionally

Read [references/planning.md](references/planning.md).

- Fast: keep a short internal checklist unless the user requests a written plan.
- Standard: maintain a concise ordered plan with verification steps. Write it
  down when the change touches more than 5 files. With 3 or more unresolved
  design decisions, run the decision-grilling pass described in planning.md.
- High-risk: record invariants, failure modes, rollback or recovery approach,
  and acceptance evidence before editing.
- Use the repository's existing specification workflow (e.g. OpenSpec) when it
  is already present or the user requests it — see
  [references/openspec.md](references/openspec.md). Do not initialize a
  specification system automatically.

### 4. Implement the change

Read [references/implementation.md](references/implementation.md). For every
High-risk task, external side-effect task, or explicit cross-session/model
handoff, also read [references/risk-controls.md](references/risk-controls.md).

- Locate definitions and consumers before changing a contract (brownfield).
- Apply the reuse ladder: existing code > standard library > installed
  dependency > new code. Document the tradeoff for any new dependency.
- Keep the diff scoped; avoid speculative abstractions, unrelated cleanup, and
  generated process files.
- After each task, run the L0 (syntax/import) → L1 (behavior assert) → L2
  (contract match) self-check. Self-heal at most 3 rounds per failure.
- A self-heal that passes only via `Any`, `# type: ignore`, or `cast()` is an
  escape hatch: record it, never present it as a clean pass.
- If requirements conflict with reuse, or the spec proves incomplete, read
  [references/conflict-rulings.md](references/conflict-rulings.md) and follow
  the ruling.

### 5. Verify with evidence

Read [references/verification.md](references/verification.md), then read only
the matching toolchain reference:

- Python: [references/toolchain-python.md](references/toolchain-python.md)
- TypeScript or JavaScript: [references/toolchain-typescript.md](references/toolchain-typescript.md)
- Go: [references/toolchain-go.md](references/toolchain-go.md)
- Rust: [references/toolchain-rust.md](references/toolchain-rust.md)

Read [references/adaptive.md](references/adaptive.md) when a configured tool is
missing. Prefer commands declared by the repository, CI, task runner, or package
manager. Distinguish clearly between:

- `PASS`: executed and satisfied the stated criterion.
- `FAIL`: executed and found a defect.
- `BLOCKED`: could not execute because a dependency, credential, service, or
  permission was unavailable.
- `NOT_APPLICABLE`: the check does not apply to the changed behavior.

Degradation is not skipping: a degraded check still requires alternative
evidence, labeled as such. For a Python project with an explicit structured
contract, run `python scripts/check_python_contracts.py --spec <spec.md>
--source <src_dir>`; never claim contract verification when the contract
contains no supported symbols.

### 6. Hand off

Report:

1. The outcome and important files changed.
2. Verification commands and their exact results (`PASS` / `FAIL` / `BLOCKED` /
   `NOT_APPLICABLE`).
3. Escape hatches, assumptions, skipped or blocked checks, and remaining risks.
4. A suggested Conventional Commits message and any follow-up actions still
   requiring the user (commit, spec sync/archive, deployment).

Commit only when the user explicitly requested a commit or the active workflow
clearly includes it. Push, deploy, publish, open pull requests, modify remote
services, or install dependencies only with corresponding authority. When the
repository uses OpenSpec, suggest (but do not auto-run) the sync/archive
wrap-up per [references/openspec.md](references/openspec.md).

## Persistent state

Default to no process files. Use persistent state only for a long or
interruption-prone task, via `scripts/manage_state.py` with a single state file
— see [references/recovery.md](references/recovery.md). The only standing
artifact is `ai_pipeline/ERROR_MEMORY.md`, appended solely when a self-heal,
escape hatch, or Critical failure occurred — see
[references/sedimentation.md](references/sedimentation.md).

## Non-negotiable rules

- Never overwrite or revert unrelated user changes.
- Never weaken tests, gates, validation, or error handling merely to make
  checks pass.
- Never report a check as executed when it was inferred, simulated, skipped,
  or blocked.
- Never degrade a High-risk task to a lighter route, even when tools are
  missing — only alternative-evidence degradation is allowed.
- Never initialize OpenSpec, install dependencies, commit, deploy, migrate, or
  delete without explicit authorization.
- Never present placeholder-filled deliverables as completed work.

## Resource map

Read references only when their condition applies:

| Resource | Read when |
|---|---|
| [routing.md](references/routing.md) | Every task |
| [planning.md](references/planning.md) | Standard or High-risk tasks, or a written plan is requested |
| [implementation.md](references/implementation.md) | Every implementation task |
| [risk-controls.md](references/risk-controls.md) | Any risk flag is present |
| [verification.md](references/verification.md) | Every implementation task |
| [adaptive.md](references/adaptive.md) | A configured tool is unavailable, or no language template matches |
| [conflict-rulings.md](references/conflict-rulings.md) | A requirement, reuse, or spec conflict occurs |
| [sedimentation.md](references/sedimentation.md) | A self-heal, escape hatch, or Critical failure occurred |
| [recovery.md](references/recovery.md) | Cross-session state is justified |
| [openspec.md](references/openspec.md) | The repository already uses OpenSpec |
| [toolchain-python.md](references/toolchain-python.md) | The project is Python |
| [toolchain-typescript.md](references/toolchain-typescript.md) | The project is TypeScript/JavaScript |
| [toolchain-go.md](references/toolchain-go.md) | The project is Go |
| [toolchain-rust.md](references/toolchain-rust.md) | The project is Rust |

If repository instructions conflict with this skill, follow the higher-priority
instruction and state the practical consequence.
