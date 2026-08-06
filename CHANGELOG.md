# Changelog

All notable changes to auto-coding are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-06

### Added

- Codex plugin bundle (`plugins/auto-coding`) with a repo-local marketplace entry (`.agents/plugins/marketplace.json`) and one-command install via `codex plugin`.
- MIT license (`LICENSE`) and third-party notices (`THIRD_PARTY.md`).
- Unit tests for `pipeline/_contract_check.py` and a CI workflow (`.github/workflows/ci.yml`).
- Repository mechanical checks (`scripts/check_repo.py`): markdown link integrity + SKILL.md license scan.
- Skill sync script (`scripts/sync_plugin_skills.sh`) keeping the plugin bundle in sync with the repository root.

### Changed

- Product renamed from **sb_coding** to **auto-coding** across README, frontmatter, and plugin metadata (`sb_coding` remains only as a historical reference).
- Pipeline stage count standardized to **6-stage**.
- C1b routing prose aligned with the routing table: Nodes 2/3 are skipped for changes touching ≤5 files and run explicitly (greenfield summary / brownfield full) for >5 files.
- Phase 0 bootstrap now uses `openspec init --tools codex`.
- README verification claims rewritten: the historical test matrix (10 suites / 148 tests) is now explicitly marked as not shipped with the repository and currently non-reproducible.

### Renamed

- `pipeline/simulator_verify/` → `pipeline/runtime_verify/` (Node 6 runtime verification).
  - **Migration**: update any references to the old `simulator_verify` path or the `simulator-verify-runtime` skill name.
