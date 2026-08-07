# Adversarial fixtures — trap scenarios for deterministic tool assertions

Each subdirectory is a self-contained trap scenario. The scenarios encode the
failure modes this repository's own tooling must never silently pass:

| Fixture | Trap | Required tool behavior |
|---|---|---|
| `contract_mismatch/` | spec defines 3 contracts, code implements only 1 correctly | contract checker MUST exit 1 with MISSING/PARAM_COUNT failures |
| `false_pass_return_types/` | spec requires return types, code has none | contract checker MUST exit 1 (RETURN_TYPE_MISSING) — never a false PASS |
| `prose_trap/` | signature-looking prose outside fences, one real contract inside | checker MUST ignore prose and verify only the fenced contract |
| `valid_project/` | spec and code fully agree | contract checker MUST exit 0 (guards against over-strict regressions) |
| `stale_tests_dir/` | empty `tests/` dir, no pytest config anywhere | `detect_project.py` MUST report `configs.pytest == false` |
| `multi_source_root/` | `src/` (2 files) and `cmd/` (1 file) side by side | `detect_project.py` MUST report both roots, primary = `src` |
| `corrupt_state/` | torn JSON state file | `manage_state.py read` MUST exit 1 with a corruption error |

These are deterministic assertions on the repository's own tooling — they
verify that the *mechanisms* the skill relies on cannot confuse a trap for a
pass. What they cannot verify (agent compliance with prompt-level rules) is
documented as a known validation boundary in `docs/ACCEPTANCE_REPORT.md`.
