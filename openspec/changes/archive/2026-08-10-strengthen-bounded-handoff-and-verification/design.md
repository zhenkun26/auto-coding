## Context

See `proposal.md` for motivation and `specs/bounded-delivery/spec.md` for normative behavior. The current product is intentionally one end-to-end skill with on-demand references, an optional atomic recovery file, OpenSpec integration, generated plugin copies, and repository-level consistency tests. The design must strengthen cross-session handoff and verification without restoring the heavy multi-file pipeline state that earlier releases removed.

The comparative source repository is used only as design input. Its latest tree has no root license declaration and its planner instructions no longer require a validator that remains present in its scripts/templates; therefore this change will use independently written rules and tests rather than copying external implementation or adopting that repository wholesale.

## Goals / Non-Goals

**Goals:**

- Make a bounded result and its acceptance evidence the unit of work.
- Make OpenSpec-managed and standalone execution boundaries explicit.
- Prevent implementation claims, stale reports, or a green happy-path test from becoming premature acceptance.
- Add proportional safeguards for adjacent regressions, external effects, and repeated repair loops.
- Preserve the current small-by-default artifact model and plugin single-source workflow.

**Non-Goals:**

- Create separate planner and executor skills.
- Add `docs/phases`, `STATUS.md`, `STEP_*.md`, or another live status authority.
- Implement a general workflow engine or cryptographic phase-artifact protocol.
- Require High-risk rehearsal or full regression matrices for every Fast change.
- Copy external skill text or scripts into the distributable plugin.

## Decisions

### D1: Keep one orchestrating skill and add an execution-boundary section

`auto-coding` remains the user-facing entry point. `SKILL.md` will distinguish standalone, OpenSpec-managed, and not-yet-bounded requests before routing implementation risk.

Alternative considered: package `phase-step-planner` and `deliver-code-change` as additional skills. Rejected because the installed OpenSpec skills already own proposal/update/apply/archive lifecycle, while a second planner would create overlapping triggers and status authority.

### D2: Replace file-count atomicity with outcome/risk/gate atomicity

`references/planning.md` will define one task as one outcome, one primary risk boundary, and one independently executable acceptance gate. Source, test, and directly required contract files may travel together; unrelated outcomes or independently reversible gates must split.

Alternative considered: retain single-file tasks and add exceptions. Rejected because exceptions would become the normal path for coherent source-and-test changes and obscure the actual unit of acceptance.

### D3: Use OpenSpec artifacts as planning authority, repository evidence as acceptance authority

For OpenSpec-managed work, `openspec status` and apply instructions resolve the current artifact set. The executor may update a task checkbox only after its scoped acceptance evidence passes; blocked checks remain unresolved. Contradictions are reported rather than silently repaired during implementation.

Alternative considered: add a separate `STATUS.md` plus step SHA-256 checkpoints. Rejected because it duplicates OpenSpec state, and a document hash alone does not verify the recorded Git/worktree facts.

### D4: Add a conditional adjacent-path matrix

`references/verification.md` will require the original reproduction plus every relevant adjacent category: default, caller override, missing/invalid, cleanup, and compatibility. The matrix activates when the changed behavior can affect those paths; it is not a fixed test-count requirement.

Alternative considered: rely on coverage percentage. Rejected because coverage can be green while a default, cleanup, or compatibility contract is wrong.

### D5: Order evidence before narrative artifacts

The authoritative sequence will be implementation → focused regression → adjacent checks → relevant full gates → raw results → report/task reconciliation. Any behavior change invalidates earlier dynamic evidence whose inputs changed. Repository evidence-consistency checks run when available.

Alternative considered: permit reports to be drafted alongside implementation and corrected later. Rejected because intended results are easily retained as false-green acceptance claims.

### D6: Combine an operational retry cap with a semantic regression fuse

The existing self-heal round cap remains a general loop bound, but any two consecutive repair rounds that introduce material regressions in the same task trigger an earlier stop, invariant review, and task split/replan. A material regression means failure of a declared acceptance path or preserved contract, not an undefined severity label.

Alternative considered: use only a fixed number of retries. Rejected because retry count does not distinguish a harmless syntax correction from a symptom-patch cycle that is widening damage.

### D7: Never auto-restore through version control after verification failure

The implementation and verification references will remove instructions to run `git checkout -- <files>`. Failures retain their diagnostic state; any later restore must resolve exact task-owned changes and follow user/repository authority.

Alternative considered: keep automatic rollback for type errors. Rejected because Git cannot distinguish task changes from user edits already present in the same file.

### D8: Apply rehearsal and hard gates proportionally

High-risk, external-effect, and explicit handoff work gets a pre-code rehearsal covering call chain, shared state, isolation, likely mistakes, and stop conditions. Fast work stays lightweight. Repository/CI thresholds override defaults; fallback thresholds are explicitly labeled.

Alternative considered: apply the full rehearsal and default coverage threshold to every task. Rejected because it adds process cost without corresponding risk reduction and can misrepresent project policy.

### D9: Close the detected-toolchain loop

Add Go and Rust references, route them from `SKILL.md`, and extend detector tests for their manifests and tool probes. Follow the same minimal pattern as existing Python/TypeScript references while using repository-native commands.

Alternative considered: stop detecting Go/Rust until full support exists. Rejected because the detector already publicly reports those templates; actionable guidance is the smaller consistency fix.

## Risks / Trade-offs

- [More conditional rules can make the skill harder to scan] → Keep the top-level contract compact and route details into existing references.
- [OpenSpec checkbox semantics remain binary] → Define checkbox completion as “bounded task acceptance passed,” while reporting blocked or broader phase gates separately.
- [Adjacent-path checks could expand low-risk work] → Trigger only categories affected by the changed contract and allow explicit `NOT_APPLICABLE`/omission with rationale.
- [Generated plugin copies can drift] → Use the existing sync script and CI byte-diff gate after canonical files are updated.
- [The untracked `references/codex-skills/` checkout currently makes `scripts/check_repo.py` fail its license scan] → Treat it as unrelated pre-existing workspace state; do not weaken the repository license gate or claim a clean full check until the checkout is relocated, excluded by an explicitly approved vendor policy, or otherwise resolved.

## Migration Plan

1. Update canonical skill and reference contracts with the new boundaries and verification semantics.
2. Add Go/Rust guidance and detector/consistency tests.
3. Run focused tests, then the existing repository gates; report the external reference checkout separately if it still blocks `check_repo.py`.
4. Sync the canonical skill into the plugin bundle and verify no generated-copy drift.
5. Update user-facing documentation only where behavior descriptions changed; do not duplicate the full design in README.

Rollback is a normal source-level revert of this change's committed files after preserving any later user edits; no automated destructive restore is part of the runtime workflow.
