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
- Usage documentation now invokes OpenSpec through the bundled skills (`$openspec-explore` / `$openspec-propose` / `$openspec-apply-change` / `$openspec-sync-specs` / `$openspec-archive-change` / `$openspec-update-change`) instead of legacy `/opsx:*` slash commands.
- `scripts/check_repo.py` now also verifies that `README.md` and `README-EN.md` have identical heading structures.
- First release gates verified locally: the plugin was installed from the repo marketplace (`codex plugin add auto-coding@auto-coding`), its 18 skills loaded, and it was removed cleanly afterwards.
- Adversarial hardening: `pipeline/_contract_check.py` no longer swallows errors (`except Exception` removed), reports parse/read failures via diagnostics, validates CLI arguments instead of crashing on missing values, and fails loudly on a missing spec or source directory.
- `scripts/check_repo.py` is encoding-safe and no longer crashes on SKILL.md files without frontmatter.
- Test suite expanded to 36 cases (CLI boundaries, diagnostics, check_repo checks, 1000 concurrent CLI invocations); tooling line coverage is 88%.

### Added (containerization)

- Production `Dockerfile` (multi-stage, non-root user with fixed UID, HEALTHCHECK, pip build cache) and `.dockerignore`; two modes: `validate` (pytest + checks) and `serve` (read-only docs mirror).
- Kubernetes manifests under `deploy/` (Namespace, ConfigMap, Secret with base64 placeholders, Deployment with resource limits and HTTP probes, PDB, ClusterIP Service, Ingress, HPA).
- Adversarial acceptance report: `docs/ACCEPTANCE_REPORT.md`.
- Containerization verified locally: image builds to **88.9MB** (<100MB target), validation mode passes, and serve mode answers HTTP 200 with a working HEALTHCHECK.
- GitHub Actions: CI workflow (`ci.yml`) and release-on-tag workflow (`release.yml`) configured; README top now carries a full badge set.
- README optimized and the English version synchronized: fixed intro formatting, real install commands, added Quickstart and Contributing sections, and brought the directory tree and QA numbers up to date.
- README now opens with the creation story ("创作初衷 / Origin story") explaining the vibe-coding pain points that motivated the system; English version synced.

### Renamed

- `pipeline/simulator_verify/` → `pipeline/runtime_verify/` (Node 6 runtime verification).
  - **Migration**: update any references to the old `simulator_verify` path or the `simulator-verify-runtime` skill name.

### Removed

- Legacy `openspec/commands/opsx/` slash-command definitions (superseded by the `openspec/skills/` skill implementations).
  - **Migration**: use the `$openspec-*` skill invocations listed above.

### Completed

- Phase D for the initial productization change: delta specs merged into `openspec/specs/` (content-consistency, legal-compliance, plugin-distribution) and the change archived.
