## Purpose

Defines the release gates the repository must pass before it is pushed to GitHub: planning archived, plugin installable and verified locally, documentation structurally consistent, and no duplicate skill sources.

## ADDED Requirements

### Requirement: Planning artifacts archived
The completed productize change SHALL have its delta specs merged into the main specs and its change directory archived.

#### Scenario: Sync and archive complete
- **WHEN** `openspec sync productize-auto-coding` and `openspec archive productize-auto-coding` are run
- **THEN** `openspec/specs/` contains plugin-distribution, legal-compliance, and content-consistency specs, and the change lives under `openspec/changes/archive/`

### Requirement: Plugin installable and verifiable
The auto-coding plugin SHALL be installable from the repo-local marketplace in a local Codex environment and its skills discoverable.

#### Scenario: Local install verification
- **WHEN** a user adds the local repository as a marketplace and installs the plugin
- **THEN** the plugin and its bundled skills are loaded, and the plugin can be removed again without side effects

### Requirement: Single skill source
The repository SHALL keep exactly one canonical copy of each skill; legacy duplicate command definitions SHALL be removed.

#### Scenario: No duplicate command sources
- **WHEN** the repository is scanned for `openspec/commands/opsx` references
- **THEN** no references remain outside historical notes in the CHANGELOG

### Requirement: README structural consistency
The Chinese and English READMEs SHALL have identical heading structures, enforced by a mechanical check.

#### Scenario: Heading parity check passes
- **WHEN** `scripts/check_repo.py` runs
- **THEN** it reports no README heading-structure mismatches and exits successfully

### Requirement: Release baseline committed
Before pushing to GitHub, all release-preparation changes SHALL be committed and the CHANGELOG SHALL describe the release.

#### Scenario: Clean working tree
- **WHEN** the release-preparation tasks are complete
- **THEN** `git status` is clean and the CHANGELOG documents the cleanup, verification, and alignment work
