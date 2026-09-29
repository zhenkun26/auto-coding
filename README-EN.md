# auto-coding — complete delivery with a lightweight framework

🌐 Language / 语言: [简体中文](README.md) · [English](README-EN.md)

[![CI](https://github.com/zhenkun26/auto-coding/actions/workflows/ci.yml/badge.svg)](https://github.com/zhenkun26/auto-coding/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Give a capable coding agent room to choose its methods. Keep the outcome,
protected behavior, authority, verification, memory, and completion conditions clear.

## What it does

A short [entry skill](SKILL.md) coordinates planning, implementation, verification,
and delivery. Detailed references load only when relevant. Small tasks need no
process files. Existing plans and status records remain authoritative; OpenSpec
and other specification systems are optional.

The workflow targets observable premature stopping: delivering a scaffold instead
of working behavior, omitting integration, declaring success after a weaker check,
or returning routine in-scope repairs as optional next steps. It cannot guarantee
agent compliance or independently certify agent-written evidence.

## Working flow

1. Inspect instructions, current changes, consumers, and the authorized outcome.
2. Resolve consequential uncertainty; decide routine technical choices independently.
3. Plan complete outcomes in dependency order, with acceptance and boundaries.
4. Implement through required integration and in-scope repairs.
5. Verify affected behavior with native project checks; repair and recheck failures.
6. Reconcile the request, final diff, evidence, and remaining work before completion.
7. Preserve the delivery record, commit when authorized, and report genuine limitations.

A plan or progress message is not completion. Continue until the authorized
outcome is complete, the user pauses it, or an actual dependency/permission block
prevents progress. Continue independent authorized work when another part is blocked.

## Planning depth and boundaries

| Route | Appropriate depth |
|:---|:---|
| Fast | Clear, local, reversible result: inspect, edit, and check the affected behavior |
| Standard | Meaningful uncertainty or connected behavior: concise outcome plan, consumer-aware changes and verification |
| High-risk | Actual consequential effects on data, privileges, money, external contracts or operations: explicit invariants, recovery and applicable risk checks |

Route by consequences and uncertainty, not keywords or file counts. No fixed
number of questions, tests, or repair rounds is imposed. Repeated failures call
for diagnosis and replanning; they do not make ordinary repair the user's job.

Authorization is action-specific. Existing permission persists within its scope;
readiness and broad task approval do not override explicit restrictions or authorize
push, release, deployment, new dependencies, or unrelated work. The host and project
rules enforce permissions; the skill is not a sandbox or independent runtime.

An explicitly requested cleanup audit uses [evidence-based simplification](references/simplification.md):
read-only discovery, independently challenged candidates, scoped GO, bounded
experiments, restoration, and final review. This is a conditional branch, not the
default process for ordinary edits.

## Memory and evidence

Keep three kinds of information distinct without requiring three new files:

- **Project knowledge:** stable decisions and verified lessons worth retaining.
- **Current task state:** one existing plan/status authority with the boundary,
  completed and remaining work, blockers, evidence pointers, and next action.
- **Verification evidence:** checked content, command, environment, result, and
  applicability. Include relevant uncommitted work in the content identity.

If standalone long-running work lacks an existing state authority,
`scripts/manage_state.py` offers an optional single-writer JSON record. `init`
refuses existing files; `complete --summary ...` preserves the record and rejects
known remaining work, blockers, or missing delivery fields. The deprecated `clear`
alias now follows completion semantics and never empties a record. Legacy records
remain readable and can be enriched. Structural validation does not prove a claim true.

Use `PASS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE` precisely. A required unavailable
check is blocked, not inapplicable. On resume, reconcile evidence with the current
content and environment; rerun affected or untraceable checks. A session change alone
does not invalidate unchanged, traceable evidence. See [memory design](docs/MEMORY_STRATEGY.md).

## Installation and use

The existing Codex plugin channel ships `auto-coding`, `verify-evidence`, and
`setup-auto-coding`. The skills.sh channel also offers `auto-coding-openspec`.

```bash
codex plugin marketplace add zhenkun26/auto-coding
codex plugin add auto-coding@auto-coding

# Alternative installer; choose only the skills you need
npx skills@latest add zhenkun26/auto-coding

# Local development source
codex plugin marketplace add /path/to/this/repo
codex plugin add auto-coding@auto-coding
```

```text
Use $auto-coding to complete this feature, including integration and verification.
```

Setup is optional. `$setup-auto-coding` records only useful repository-specific
pointers and boundaries in the existing instruction file. It does not require a
profile questionnaire or fabricate thresholds. `$verify-evidence` works independently.
The OpenSpec companion is for an applicable existing OpenSpec task and never
initializes a specification system merely to use this workflow.

The working tree is the next-major development version; this does not publish a
release or update installed copies. Install/update commands have external effects
and are run only under the applicable authorization.

## Repository and maintenance

| Path | Responsibility |
|:---|:---|
| `SKILL.md`, `references/` | Canonical contract and conditional guidance |
| `verify-evidence/`, `setup-auto-coding/`, `auto-coding-openspec/` | Canonical companion skills |
| `scripts/detect_project.py` | Read-only project/toolchain discovery |
| `scripts/check_python_contracts.py` | Python structural precheck; not behavioral proof |
| `scripts/manage_state.py`, `scripts/state_schema.json` | Optional recovery record |
| `scripts/sync_plugin_skills.py` | Non-deleting distribution synchronization and read-only drift check |
| `scripts/check_repo.py`, `scripts/run_tests.py`, `tests/` | Repository checks and retained-fixture tests |
| `skills/`, `plugins/auto-coding/skills/` | Generated distributions; edit canonical sources |
| `docs/WORKFLOW_PLAN.md` | Current implementation plan, research decisions and acceptance record |

Python 3.10+ runs the stdlib helpers. Bash is needed only for the compatibility
sync wrapper. Target projects use their own available toolchains; no default tool
installation or invented coverage threshold is required. Configured unavailable
checks remain visible as blocked while independent work continues.

For repository development, use an environment with the tools declared in CI:

```bash
python -B scripts/run_tests.py
ruff check --no-cache scripts/ tests/
mypy --cache-dir=/dev/null scripts/
python -B scripts/sync_plugin_skills.py
python -B scripts/sync_plugin_skills.py --check
python -B scripts/check_repo.py
```

The test runner retains unique fixture directories and disables automatic pytest
cleanup; it is not a subprocess sandbox. Sync preflights both bundles, preserves
unexpected files and refuses to proceed until the user reconciles them. `--check`
does not write. Interrupted multi-file synchronization is detectable, not transactional.
No automatic cleanup of retained files is provided.

## Verification limits and attribution

Mechanical checks cover links, license declarations, README heading parity,
language-reference routing, versions, helper behavior and distribution fidelity.
Behavioral skill tests exercise bounded scenarios; they are not a reliability
benchmark. Neither Markdown rules nor a state file prevents every premature stop.
See the [current plan and evidence](docs/WORKFLOW_PLAN.md) for actual results and
limitations; historical acceptance reports describe their historical versions.

MIT for original project content. See [THIRD_PARTY.md](THIRD_PARTY.md),
[decision records](docs/DECISIONS.md), and [CHANGELOG.md](CHANGELOG.md).
