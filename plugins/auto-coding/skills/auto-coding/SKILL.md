---
name: auto-coding
license: MIT
description: >
  Plan, implement, verify, and hand off code changes — from a vague idea to a
  reviewed diff. Use when asked to build a feature, fix a bug, refactor, or
  modify a repository end to end. Route work by uncertainty and operational
  risk; reuse before writing; verify with the project's own tools; require
  explicit authorization for installs, commits, deployments, and deletions.
---

# Auto-Coding

Deliver the smallest change that satisfies the request, with planning depth and
verification evidence proportional to its risk. Reuse beats standard library
beats installed dependencies beats new code.

## Core contract

1. Read repository instructions and working-tree state before editing.
2. Preserve user-owned and unrelated changes.
3. Classify the task as Fast, Standard, or High-risk before any planning.
4. Never plan deeper than the route requires; never create process files by default.
5. Reuse existing implementations before writing new ones.
6. Verify with the project's native toolchain and report `PASS` / `FAIL` /
   `BLOCKED` / `NOT_APPLICABLE` exactly. Never convert `BLOCKED` into `PASS`.
7. Install dependencies, commit, push, deploy, migrate, or delete only with
   explicit authorization.
8. Treat an existing planning workflow's artifacts (OpenSpec, spec-kit, a
   tracked issue, a plan document) as planning authority — never initialize a
   spec system unasked; otherwise plan inline.

Treat source diffs, command output, and test results as proof. Do not treat
generated reports as proof.

## Workflow

1. **Establish scope** — Read `AGENTS.md`, repository instructions, CI
   configuration, and existing plan or spec artifacts; inspect version-control
   status before editing. Identify the requested outcome, acceptance evidence,
   affected interfaces, and actions requiring authorization. Ask only when a
   missing choice would materially change the result or authorize a new side
   effect; otherwise make a narrow, reversible assumption and state it. Read
   `ai_pipeline/ERROR_MEMORY.md` before planning when it exists. Run
   `python scripts/detect_project.py <project-root>` when project shape or
   toolchains are not obvious — discovery evidence, not permission.
2. **Select a route** — Read [references/routing.md](references/routing.md)
   and choose exactly one: Fast (localized, clear, low-risk), Standard
   (multi-file behavior, interface change, meaningful uncertainty), High-risk
   (FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API / ENV_OPS,
   concurrency, destructive behavior). Risk overrides size: a one-line
   authorization or money change is High-risk. State the route in one sentence
   when it affects execution depth.
3. **Plan proportionally** — Read
   [references/planning.md](references/planning.md). Fast: short internal
   checklist unless the user asks for a plan. Standard: concise ordered plan
   with verification steps, written down past 5 files; with 3+ unresolved
   design decisions, grill one question at a time. High-risk: record
   invariants, failure modes, rollback approach, and acceptance evidence
   before editing.
4. **Implement** — Read
   [references/implementation.md](references/implementation.md); add
   [references/risk-controls.md](references/risk-controls.md) for any risk
   flag. Locate definitions and consumers before changing a contract; keep the
   diff scoped. After each task run the three-pass self-check — imports load,
   behavior asserts pass, contract matches; self-heal at most 3 rounds. A pass
   that relies on `Any`, `# type: ignore`, or `cast()` is recorded debt, never
   a clean pass. If the spec proves incomplete or wrong, stop and report.
5. **Verify with evidence** — Read
   [references/verification.md](references/verification.md), then only the
   matching toolchain reference (see the resource map). Distinguish `PASS`,
   `FAIL`, `BLOCKED` (could not execute), and `NOT_APPLICABLE`; a degraded
   check still requires labeled alternative evidence. For a Python project
   with an explicit structured contract, run
   `python scripts/check_python_contracts.py --spec <spec.md> --source <src_dir>`.
6. **Hand off** — Report outcome and files changed; verification commands
   with exact results; recorded debt, assumptions, blocked checks, and
   remaining risks; a suggested Conventional Commits message and follow-ups
   still requiring the user. Commit only when the user explicitly requested
   it; push, deploy, publish, or install only with corresponding authority.

## Persistent state

Default to no process files. Use persistent state only for a long or
interruption-prone task, via `scripts/manage_state.py` with a single state file
— see [references/recovery.md](references/recovery.md). After resuming from a
state file, treat every verification result from the earlier session as
unverified and re-run the gates the route requires. The only standing artifact
is `ai_pipeline/ERROR_MEMORY.md`, appended solely when a self-heal, an escape
hatch, or a Critical failure occurred — see
[references/sedimentation.md](references/sedimentation.md).

## Non-negotiable rules

- Never overwrite or revert unrelated user changes.
- Never weaken tests, gates, validation, or error handling merely to make checks pass.
- Never report a check as executed when it was inferred, simulated, skipped, or blocked.
- Never degrade a High-risk task to a lighter route, even when tools are missing.
- Never present placeholder-filled deliverables as completed work.
- Facts first: report work that is factually complete as complete, and work
  that is not as not — never silently reconcile a checklist either way.

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
| [sedimentation.md](references/sedimentation.md) | A self-heal, escape hatch, or Critical failure occurred |
| [recovery.md](references/recovery.md) | Cross-session state is justified |
| [toolchain-python.md](references/toolchain-python.md) | The project is Python |
| [toolchain-typescript.md](references/toolchain-typescript.md) | The project is TypeScript/JavaScript |
| [toolchain-go.md](references/toolchain-go.md) | The project is Go |
| [toolchain-rust.md](references/toolchain-rust.md) | The project is Rust |

If repository instructions conflict with this skill, follow the higher-priority
instruction and state the practical consequence.
