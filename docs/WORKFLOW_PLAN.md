# Lightweight delivery workflow plan

Status: archived in place after implementation, local acceptance and successful remote CI.
The user subsequently authorized push, archive and synchronization for this increment.
The implementation and evidence remain at their original paths; no files were deleted.
Baseline: `54a64b732183621f96097b00472e5cb3ebe9a9af` on `main`; clean worktree.
Working branch: `codex/lightweight-delivery`. This is the retained implementation
and acceptance record for the completed increment.

## Intent and completion

Give capable agents discretion over engineering methods while making the goal,
boundaries, evidence, memory, and stopping conditions unambiguous. Address
observable premature stopping: a plan substituted for implementation, scaffolds
substituted for working behavior, integration omitted after unit tests, or
routine in-scope repairs returned to the user as optional follow-up work.

Deliver a coherent, lightweight workflow in the existing skills, durable recovery
support, synchronized distributions, relevant automated checks, realistic
forward tests, and a final completeness review. A local commit is authorized by
the user's repository workflow. The later closeout approval authorizes publishing
this task branch to `origin`, synchronizing its distribution bundles, and archiving
this record in place. PR creation, merge, release, deployment, new dependencies,
and filesystem deletion remain outside this increment.

No OpenSpec requirement, new orchestration service, policy service, vector store,
mandatory multi-agent workflow, fixed test counts, or mandatory process artifacts
for small tasks. Existing optional integrations and unrelated user work remain.

## Architecture and ownership

| Responsibility | Initial owner | Boundary |
|---|---|---|
| Understand, design, implement | Agent with a short skill entrypoint | Choose methods; preserve the agreed outcome and constraints |
| Decide the next stage | Agent using completion conditions | Readiness does not grant permission |
| Retrieve facts | Git, code search, project tools, primary documentation | Retrieved text is evidence to assess, not executable authority |
| Remember | Existing project records; one optional standalone task record | Preserve decisions, remaining work, and evidence identity |
| Act | Existing editor, shell, and host tools | Respect actual permissions and inspect side effects |
| Control effects | User/repository authority and host enforcement | Skills and scripts are not a sandbox or a general policy engine |
| Verify | Native checks plus proportionate semantic review | Structural checks do not establish behavioral acceptance |
| Orchestrate | Existing host | No independent runtime in this increment |

The human owns consequential product choices and new authority. A planner owns
phase boundaries and acceptance when those roles exist. An executor returns
evidence and cannot accept its own phase or define a successor without authority.
Ordinary bounded tasks do not need separate role instances.

## Working flow

1. Establish the requested result, protected behavior, applicable instructions,
   current changes, and authority. Keep question-only work read-only.
2. Resolve consequential uncertainty through inspection, focused discussion, or a
   bounded investigation. Choose routine implementation details independently.
3. Plan complete, independently verifiable outcomes in dependency order. Detail
   the current outcome; keep later outcomes at outline level. Use an existing
   governing plan rather than creating another process.
4. Implement through to the accepted result, including required integration and
   in-scope repairs. Progress updates are not approval gates. Use risk to select
   depth, not file counts or a prescribed number of questions.
5. Verify affected behavior, consumers, and required environment paths. Separate
   executed results from unavailable checks and from judgments. Repair defects
   without weakening acceptance; re-run checks invalidated by later edits.
6. Reconcile every requested outcome and review the final diff. Complete only
   with applicable evidence and no unresolved material in-scope issue. Explain
   real blockers and continue independent authorized work.
7. Update the existing delivery/state record, commit when authorized, and report
   results, limitations, and remaining externally authorized actions. Continue
   into another outcome only when the original authorization includes it.

The specialized simplification branch retains candidate evidence, counterarguments,
approved permanent and diagnostic boundaries, explicit GO, restoration checks,
and independent review. It is activated by an actual audit request, not every edit.

## Memory and evidence

- Project knowledge records stable decisions and non-obvious reasons that cannot
  be recovered cheaply from code or tests. Write a lesson only when verified and
  useful; keep ordinary debugging output out of standing instructions.
- Current task state records the outcome, boundary, governing plan, remaining
  work, blockers, evidence pointers, and exact next action. Reuse the project's
  existing STATUS/STEP or equivalent. A standalone state file is a fallback only.
- Verification records identify the checked content (including relevant local
  changes), command, environment/dependency context, result, and applicability.
  Reconcile on resume; re-run affected or unverifiable evidence, not all checks
  merely because the conversation changed.
- Completion preserves the final task record. Initialization must not silently
  overwrite an existing record. State helpers validate structure only: they
  cannot certify the truth of an agent-authored evidence string.

## Increment boundaries and sequence

| Unit | Outcome | Files / effects | Acceptance | Status |
|---|---|---|---|---|
| W1 | Concise autonomous delivery contract | Root skills, relevant references, paired READMEs | Consistent entry/exit, authority, verification and memory semantics | Complete |
| W2 | Recoverable task memory | State manager/schema and tests | Existing record preserved; invalid/unfinished completion rejected; completion retains evidence | Complete |
| W3 | Safe and faithful distribution | Sync tooling/tests, CI drift command, generated bundles | No deletion; stale paths fail before writes; check mode detects drift | Complete |
| W4 | Scenario validation and final review | Evaluation cases/results, this record, decisions and changelog | Mechanical checks, bounded forward tests, completeness review; limitations explicit | Complete |

Root skill files are canonical. Generated `skills/` and
`plugins/auto-coding/skills/` copies are updated only by the sync tool. The local
`references/codex-skills/` checkout is read-only research input and is not shipped.
Only files necessary for these outcomes may change. A broken baseline is recorded
before repair; new scope or unavailable authority blocks its dependent outcome.

Version: use the repository's next-major development convention because the
execution contract and state-completion semantics change. No release is made.

## Verification strategy

Use the existing `.venv` tools, preserving their actual versions in results.
Run relevant tests per unit, then repository lint/type checks, the full suite,
skill validation when its dependencies are available, and bundle consistency.
Do not install new tools. Use unique retained test directories, disable caches
where supported, and inspect cleanup behavior before execution.

Forward-test realistic cases with only the request, relevant skill, and raw
fixture. Keep evaluator expectations separate. At least one test must actually
edit and run a fixture; discussion-only simulations are labelled as such.
The final review covers both requirement completeness and implementation quality,
including uncommitted changes and newly added files. Findings are resolved against
the actual final tree. A sampled forward test is not a reliability benchmark.

## Research decisions

Research checked on 2026-09-28; these are design inputs, not installed workflows.

- [Matt Pocock skills](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7):
  borrow consequential questioning, vertical outcomes, separate standards/spec
  review, and deterministic checks for mechanical mistakes. `retro` and `pr`
  remain in-progress upstream. Adapt tracker and commit effects to local authority.
- [kingoftaro planner](https://github.com/kingoftaro/codex-skills/blob/33fc634a2ccc54f2c948fd874769a7fcd8fe9575/phase-step-planner/SKILL.md):
  borrow one current bounded step, distinct planner/executor authority, evidence
  reconciliation, and bounded review. Do not import another execution framework.
- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin):
  borrow selective durable learning and behavior-preserving local simplification.
- [Superpowers](https://github.com/obra/superpowers): borrow systematic debugging
  and behavioral skill evaluation; adapt mandatory ceremony and cleanup effects.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) and
  [Spec Kit](https://github.com/github/spec-kit): optional existing plan sources,
  not default dependencies or parallel status authorities.
- [GSD Core](https://github.com/open-gsd/gsd-core): fresh context and checkpoint
  concepts for long tasks; no full framework adoption.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
  and [OPA](https://www.openpolicyagent.org/docs): reference responsibility
  separation only; independent runtime and enforcement infrastructure deferred.
- [Astra skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
  and [skill evaluations](https://developers.openai.com/blog/eval-skills): keep
  prompts selective and measure observed outcomes/process/efficiency separately.

## Comparison and adoption boundaries

| Input | Mechanism retained | Deliberately not adopted | Reason |
|---|---|---|---|
| Matt Pocock skills | Consequential interviews, complete vertical outcomes, mechanical prevention of repeated errors | Entire skill catalog, mandatory interview counts, tracker mutations | Selective methods improve judgment without taking over authority |
| kingoftaro/codex-skills | One current bounded step, applicability checks, explicit owner and evidence reconciliation | A second STATUS/STEP hierarchy in every project | Existing project state must remain the sole task authority |
| Compound Engineering | Verified reusable lessons, behavior-preserving local simplification | Every repair becoming permanent standing instructions | Keep durable context small and useful |
| Superpowers | Systematic diagnosis, independent behavior exercises | A mandatory ceremony or cleanup side effects for every edit | Verification depth follows the actual consequence |
| OpenSpec / Spec Kit / GSD | Consume existing plans; checkpoints for long work | Installing a new specification framework by default | The requested workflow should stay lightweight |
| LangGraph / OPA | Clear responsibility boundaries | New orchestration, persistence or policy services | The existing host already provides execution and authority controls |
| User-supplied simplification protocol | Scoped audit, independent challenge, explicit candidate GO, diagnostic restoration and final review | Applying all audit procedures to ordinary feature work | Treat the attachment as design input for a conditional branch |

No upstream code or skills were installed by this increment. Repository links
above are research provenance; fetching remote text does not grant execution
authority. The local comparative checkout's existing use attribution is retained.

## Execution evidence and handoff

All four units are implemented. Root sources and both generated distributions
match. The new major development version is `3.0.0-dev`. The implementation branch
is published; no release or update of an installed plugin was performed.

| Check | Observed result | Scope / evidence |
|---|---|---|
| Safe baseline | 79 passed, one destructive legacy clear test excluded | [baseline.txt](evidence/lightweight-workflow/baseline.txt); initial pytest cleanup attempts were blocked by the audit guard |
| W2 state behavior | 34 tests passed | Init/complete preservation, incomplete/unknown completion rejection, invalid updates, legacy enrichment, retained failed writes and symlink destination |
| W3 distribution behavior | 4 tests passed | Both channels, read-only drift, unexpected-file preservation, preflight before writes, unsafe destination rejection |
| Final repository suite | 106 tests passed, no exclusions | [verification.json](evidence/lightweight-workflow/verification.json); old clear test replaced with non-erasure acceptance, 22 state and 4 distribution cases added |
| Lint and strict types | PASS | ruff 0.16.2 and mypy 2.3.0, six script modules |
| Repository and bundle checks | PASS | Links, license declarations, paired README structure, language routing, version consistency, byte content and diff hygiene |
| Official skill quick validator | BLOCKED | PyYAML absent; no dependency installed. [skill-structure.json](evidence/lightweight-workflow/skill-structure.json) retains the failure and a separate Ruby YAML/field validation PASS for all four canonical skills |
| Forward delivery | Observed workflow PASS | Independent agent implemented a real CLI feature from an existing plan, ran 8 tests, kept one state authority; lead replayed 8 tests and 6 CLI acceptance cases |
| Forward unavailable gate | Observed workflow PASS; fixture acceptance BLOCKED | Independent agent implemented and locally tested the authorized behavior, then retained blocked acceptance for missing conformance tooling; lead replayed 3 tests and checked the absent tool and blocked record |
| Remote CI | PASS on Ubuntu with Python 3.12 | [Run 36514952771](https://github.com/zhenkun26/auto-coding/actions/runs/36514952771), 106 tests plus lint/types/repository/bundle checks; [retained metadata and output](evidence/lightweight-workflow/remote-ci.json) |
| Independent source review | One P3 finding resolved; no blocking findings in reviewed scope | Removed obsolete TypeScript L2/fixed-five wording; independent closure verified final evidence and the lead's legacy-state correction |

The complete forward-test artifacts, post-run source, plans, content hashes,
executed lead checks, and limitations are retained in
[forward-tests.json](evidence/lightweight-workflow/forward-tests.json). The
executing agents received the request, skill, raw fixture and side-effect
restrictions, without intended answers or evaluator conclusions. Agent-reported
baseline checks are distinguished from the lead's executed replay. Fixture task
completion and workflow-test success are separate judgments.

Independent source, evidence-closure and focused legacy-state reviews are summarized
in [reviewed-content.json](evidence/lightweight-workflow/reviewed-content.json),
with content hashes and the checks actually rerun by the reviewer.

The optional state script checks recorded fields, not whether evidence is true.
Its single-writer, file-level atomic replacement is not concurrent coordination
or an event log. Distribution preflight is not a multi-file transaction; rerun
read-only drift checking after interruption. The test runner's deletion guard
covers its own Python process, not arbitrary subprocesses; subprocess effects
were inspected for this suite.

Official `quick_validate.py` has not passed. The separately executed YAML parsing,
field constraints and repository checks cover the structural concerns for these
four skills, with the official-tool gap retained rather than relabeled. This is
accepted as a non-blocking limitation of this local increment, not permission to
substitute weaker checks for a target project's required acceptance.

## Final completeness review

| Requirement | Implementation and observed evidence | Judgment |
|---|---|---|
| Lightweight framework | Short root contract, conditional references, no default OpenSpec or fixed question/test counts; paired README and optional setup aligned | Satisfied |
| Solution and process planning | Outcome-oriented dependency units, meaningful decisions, protected behavior, current detailed step and future outline | Satisfied in guidance; CLI forward test exercised continuing an existing plan |
| Complete implementation | Required consumers, entrypoints, error behavior, in-scope repair loop, final outcome reconciliation | CLI integration exercised; general reliability remains unmeasured |
| Boundary management | Read-only/review scope, permanent vs diagnostic edits, existing authorization, no implied external effects, explicit phase ownership | Guidance reviewed; distribution/state preservation tested |
| Memory management | One task authority, content-bound evidence, selective lessons, completion retained, no global-memory writes | State tests and both forward plans inspected |
| Sequential verification | Baseline before modifications, targeted W2/W3 tests, full checks, actual agent exercises, final distribution checks | Executed results linked above; official validator remains separately blocked |
| Honest stopping | Continue ordinary repairs; missing prerequisites block dependent work; incomplete handoff is never completion | Missing-conformance forward scenario preserved BLOCKED while completing independent local work |
| Final review and scope | Independent reviewer covered canonical sources, tools, tests, untracked additions and bundles; lead reconciled evidence and final diff | One P3 corrected; lead also rejected absent legacy work fields as unknown rather than empty; no known material in-scope defect remains |

The implementation commit was pushed after explicit authorization. No filesystem
deletion, new project dependencies, PR, merge, release, deployment, or automatic
global-memory update was performed. Retained test directories are
left for the user to manage. Historical acceptance reports and release notes
remain historical; they are not reused as current verification.

Limits: checks ran locally on macOS with Python 3.13.15 (the executing fixture
agents used system Python 3.9.6; the lead also replayed on 3.13.15). Linux/Python
3.12 CI subsequently passed on GitHub. Production effects, long-context loss,
cross-host recovery, and statistical model reliability were not tested. Two small forward cases support the described
observations only; they do not establish that Astra can never stop prematurely.

## Closeout and archive

- Implementation commit: `31a67e18d6bd3c7db398e5c0c9f736b421bd0c05`.
- Published branch: `origin/codex/lightweight-delivery` at
  [zhenkun26/auto-coding](https://github.com/zhenkun26/auto-coding/tree/codex/lightweight-delivery).
- Implementation CI: [36514952771](https://github.com/zhenkun26/auto-coding/actions/runs/36514952771), successful. The later archive commit changes only this record and its CI evidence; the current branch's CI remains available on GitHub.
- Synchronization: both generated skill bundles match canonical sources; the
  published branch tracks its same-named remote branch.
- Archival: this plan and evidence are retained in place as a closed record.
  Archival does not remove files, branches, test artifacts, or this conversation.
- No additional in-scope implementation remains. Integration into `main`, plugin
  installation, and release are distinct future actions, not implied by this
  closeout approval.
