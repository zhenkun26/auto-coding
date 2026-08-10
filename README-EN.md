# auto-coding — risk-aware coding delivery skill for AI agents

🌐 Language / 语言：[简体中文](README.md) · [English](README-EN.md)

[![CI](https://github.com/zhenkun26/auto-coding/actions/workflows/ci.yml/badge.svg)](https://github.com/zhenkun26/auto-coding/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/zhenkun26/auto-coding)](https://github.com/zhenkun26/auto-coding/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **risk-aware delivery skill** for AI coding agents: select execution depth by uncertainty and operational risk, plan proportionally, change minimally, verify with the project's own toolchain, and deliver on evidence.

## What it is

auto-coding helps a coding agent, when modifying code, to first identify risks and constraints, then plan, implement, verify, and hand off at a depth proportionate to the task. It is a restructuring of a parallel development system distilled through repeated trial and error during vibe coding (OpenSpec planning + Pipeline execution + Ponytail code minimization + grill-me decision interviews) — every practical mechanism is preserved, on a more restrained structure:

- **The main file holds only the contract**: `SKILL.md` defines the execution contract; all detail lives in 14 on-demand references;
- **Zero process files by default**: no more TASK_PLAN / LOCATE_MAP / RUN_LOG pipelines — a single state file exists only for long tasks;
- **Clear authorization boundaries**: spec-system initialization, dependency installs, commits, deployments, migrations, and deletions all require explicit authorization.

## Core ideas

Not every change needs to go through the same heavy pipeline. This skill selects execution depth by uncertainty, blast radius, and operational risk, following the principle that **risk overrides change size** — even a one-line authorization or money change is High-risk.

This skill follows the principle of the **smallest complete change**: reuse existing implementations, the standard library, and installed dependencies first (reuse > stdlib > installed dependency > new code), avoiding unrelated refactoring, process-file bloat, and unauthorized side effects. Verification evidence strictly distinguishes `PASS` / `FAIL` / `BLOCKED` / `NOT_APPLICABLE`, and `BLOCKED` is never treated as `PASS`.

## Three routes

| Route | Typical use | Required depth |
|:---|:---|:---|
| **Fast** | Localized, clear, low-risk, easily reversible | Inspect, minimal edit, L0/L1 self-check |
| **Standard** | Multi-file behavior, interface change, or meaningful uncertainty | Concise plan, caller-aware implementation, static checks and tests |
| **High-risk** | FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API / ENV_OPS, concurrency, or destructive behavior | Written invariants and rollback plan, staged implementation, risk-specific verification |

Greenfield/brownfield state does not change the route — only planning and location depth (greenfield has no existing code to locate; files are created directly).

## How it works

1. Read repository instructions, CI, and working-tree state; optionally probe the project read-only via `scripts/detect_project.py`.
2. Establish the execution boundary: standalone requests use an inline plan; an existing OpenSpec change makes its dynamic instructions and artifacts the planning authority; an unbounded request stops before implementation.
3. Select the Fast / Standard / High-risk route.
4. Plan to the route's depth; with ≥3 unresolved design decisions, run the decision-grilling pass.
5. Implement along the reuse ladder; every task runs the L0 (import) → L1 (behavior assert) → L2 (contract match) self-check, with layer-level type checkpoints and escape-hatch detection.
6. Verify with the project's own commands in focused-regression → adjacent-contract → broader-gate order; behavior changes invalidate earlier evidence. Missing tools follow the adaptive rules and are reported honestly as `BLOCKED`.
7. Report changes, verification evidence, escape hatches, assumptions, and follow-ups; an OpenSpec task is checked only after scoped acceptance evidence passes, while commits and spec sync/archive remain authorization-gated suggestions.

Conflicts follow the established rulings: requirement existence defers to specs, code reuse follows the reuse ladder, spec defects stop implementation and trigger an honest defect report, and task lists defer to facts. See [references/conflict-rulings.md](references/conflict-rulings.md).

## Safety boundaries

By default, this skill does not automatically perform the following:

- initializes OpenSpec or any other specification system
- installs dependencies
- commits, pushes, publishes, or deploys
- deletes files, runs data migrations, or modifies remote services
- reports a check it could not execute as passed

All of the above require explicit user authorization. Checks that cannot run are marked `BLOCKED` and reported separately from alternative evidence.

## Sedimentation and recovery

- **No process files by default.** The only standing artifact is `ai_pipeline/ERROR_MEMORY.md`, appended solely when a self-heal, escape hatch, or Critical failure occurs (see [references/sedimentation.md](references/sedimentation.md)).
- **Breakpoint recovery**: only long or interruption-prone tasks use the single state file `ai_pipeline/state.json`, read and written atomically via `scripts/manage_state.py` (see [references/recovery.md](references/recovery.md)). The next invocation prints the exact breakpoint and asks whether to resume or restart.

## Repository layout

```text
├── SKILL.md                     # Control: core contract, routing, workflow, resource map
├── references/                  # 14 on-demand references
│   ├── routing.md               #   Fast/Standard/High-risk routing and risk flags
│   ├── planning.md              #   Proportional planning, atomic decomposition, decision-grilling
│   ├── implementation.md        #   Reuse ladder, location method, L0/L1/L2 self-check, escape hatches
│   ├── verification.md          #   Static/runtime gates, repository-first thresholds and fallbacks
│   ├── risk-controls.md         #   Non-degradable controls for the six risk flags
│   ├── adaptive.md              #   Toolchain adaptation and degradation rules
│   ├── conflict-rulings.md      #   R1/R2/R6/R8 conflict rulings
│   ├── sedimentation.md         #   ERROR_MEMORY / TECH_NOTES (optional)
│   ├── recovery.md              #   Cross-session breakpoint recovery
│   ├── openspec.md              #   Consuming and wrapping up an existing OpenSpec workflow
│   └── toolchain-python.md / toolchain-typescript.md / toolchain-go.md / toolchain-rust.md
├── scripts/
│   ├── detect_project.py         # Read-only project detection (language/CI/spec system/greenfield)
│   ├── manage_state.py           # Atomically reads/writes the single state file
│   ├── check_python_contracts.py # Python structural contract checker (AST + Gherkin fallback)
│   ├── state_schema.json         # State-file reference schema
│   ├── check_repo.py             # Repository mechanical checks (links/licenses/README/toolchain routes)
│   └── sync_plugin_skills.sh     # Plugin bundle sync (repo root is the single source of truth)
├── pyproject.toml               # ruff / mypy (strict) configuration for CI self-checks
├── plugins/auto-coding/         # Codex plugin bundle (generated from the repo root by the sync script)
├── tests/                       # pytest suite (including adversarial trap fixtures under fixtures/adversarial)
└── openspec/                    # This repository's own specs (dogfooding)
```

## Installation

Distributed as a Codex plugin + marketplace; the repo-local marketplace lives at `.agents/plugins/marketplace.json`.

```bash
# Install from GitHub
codex plugin marketplace add zhenkun26/auto-coding
codex plugin add auto-coding@auto-coding

# Local development install
codex plugin marketplace add /path/to/this/repo
codex plugin add auto-coding@auto-coding

# Update / uninstall
codex plugin marketplace upgrade
codex plugin remove auto-coding@auto-coding
```

After changing skill content, run `bash scripts/sync_plugin_skills.sh` before releasing to re-sync the plugin bundle; CI re-runs the script and fails on any drift between the bundle and the repository root.

## Usage

```text
Use $auto-coding to implement this change with risk-aware routing and verification.
```

Or describe the task directly and let the skill handle routing automatically. Repositories already using OpenSpec can hand off a change directory directly: `Implement openspec/changes/<name>/ with auto-coding`; completion requires passing scoped acceptance evidence.

## Environment requirements

| Dependency | Required? | When missing |
|:---|:---|:---|
| bash (POSIX sh) | Required | No fallback — bash is the execution environment |
| git | Required for commits | Code written but uncommitted, labeled honestly |
| Python 3.10+ | Contract checker / detection scripts | Contract check degrades to the manual L2 checklist |
| mypy / ruff / pytest | Python template | Configured but missing → install prompt and halt; no config → degrade to alternative evidence marked `BLOCKED` |
| tsc / eslint / jest | TS template | Same as above |
| go | Go template | Preserve repository tags/platform constraints; halt when missing, without installing tools or changing module dependencies |
| cargo | Rust template | Preserve toolchain/MSRV and feature constraints; halt when missing, without installing tools or updating dependencies |
| OpenSpec CLI | Optional | `[NO_OPENSPEC]` inline planning throughout; never auto-initialized |

## Quality assurance

- Three-layer self-check (L0/L1/L2) + hard gates: type check Critical (failure halts while preserving diagnostics), lint Standard (self-heal ≤3 rounds); coverage uses repository/CI thresholds first and labeled fallback values only when absent.
- Adjacent-contract checks select relevant default, override, missing/invalid-input, failure-cleanup, and compatibility paths; two repair rounds that consecutively introduce new acceptance or preserved-contract failures trip the semantic fuse and force root-cause replanning.
- Layer-level type checkpoints: after each topological layer, the type checker runs over every file written so far, catching cross-file type errors.
- Escape-hatch detection: self-heals that pass only via `Any` / `# type: ignore` / `cast()` are recorded as `[ESCAPE_HATCH]` quality debt and listed at handoff.
- Automated contract checking: AST comparison of spec signatures against actual code, with spec extraction scoped to fenced code blocks (prose that merely looks like a signature is ignored), namespace-aware (`ClassName.method`); empty contracts never report a false pass.
- Repository self-checks: the full pytest suite (including deterministic trap assertions over adversarial fixtures), ruff and mypy (strict) over the repository's own scripts, a plugin-bundle drift check, markdown link integrity, license-header scan, Chinese/English README structure parity, and complete detector-template-to-toolchain routing — all in CI (`.github/workflows/ci.yml`).

## Third-party components and license

MIT License. The reuse ladder is adapted from Ponytail (MIT); earlier releases bundled OpenSpec skills and grill-me. See [THIRD_PARTY.md](THIRD_PARTY.md) and [CHANGELOG.md](CHANGELOG.md).
