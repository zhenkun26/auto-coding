## 1. Establish bounded execution authority

- [x] 1.1 Update the canonical `SKILL.md` contract to distinguish standalone, OpenSpec-managed, and not-yet-bounded requests, route OpenSpec work through existing artifacts/instructions, and prohibit a competing phase status tree.
- [x] 1.2 Replace single-file atomicity in `references/planning.md` with one outcome, one primary risk boundary, and one independent acceptance gate; keep source, focused tests, and directly required contract updates together when they form one coherent result.
- [x] 1.3 Update `references/openspec.md` so task checkboxes are reconciled only after scoped acceptance evidence passes, while contradictions, blocked checks, and scope expansion stop implementation instead of being silently repaired.

## 2. Strengthen repair and verification behavior

- [x] 2.1 Update `references/implementation.md` to remove automatic version-control rollback, preserve diagnostic state, and add the semantic repair-regression fuse alongside the existing operational retry cap.
- [x] 2.2 Update `references/verification.md` with the conditional adjacent-path matrix, strict evidence-production order, stale-evidence invalidation, and repository/CI-first threshold policy.
- [x] 2.3 Update `references/risk-controls.md` with a conditional pre-code rehearsal for High-risk, external-effect, and explicit cross-session/model handoff work, including call chains, shared state, test isolation, likely mistakes, and stop conditions.

## 3. Close toolchain and consistency gaps

- [x] 3.1 Add concise Go and Rust toolchain references and route them from `SKILL.md`, using repository-native format, static, test, race/concurrency, and feature-matrix commands without automatic installation.
- [x] 3.2 Extend `tests/test_detect_project.py` to cover Go/Rust manifest detection and primary tool availability reporting, preserving the detector's read-only contract.
- [x] 3.3 Extend repository consistency checks and tests so every detected language template has a corresponding routed toolchain reference without weakening license, link, or generated-copy checks.

## 4. Align distribution and user-facing behavior

- [x] 4.1 Update `README.md` and `README-EN.md` only where the public workflow changed, keeping the explanation concise and the two heading structures aligned.
- [x] 4.2 Add a CHANGELOG entry describing outcome-bounded tasks, verified OpenSpec completion, adjacent-path evidence, non-destructive failure handling, and Go/Rust guidance.
- [x] 4.3 Run `scripts/sync_plugin_skills.sh` after canonical files are final and confirm the generated plugin bundle has no drift from the canonical skill.

## 5. Verify the bounded-delivery change

- [x] 5.1 Run focused detector and repository-check tests, then the full pytest suite, ruff, and strict mypy; record exact `PASS`/`FAIL`/`BLOCKED` results without converting alternative evidence into a pass.
- [x] 5.2 Run `scripts/check_repo.py`, plugin bundle diff verification, `git diff --check`, and strict OpenSpec validation for this change; report the pre-existing untracked `references/codex-skills/` license-scan conflict separately unless the user has authorized its relocation or an explicit vendor policy.
- [x] 5.3 Reconcile every checkbox against the final diff and current command output; do not mark implementation complete or prepare archive/sync claims while any required gate remains failed or blocked.
