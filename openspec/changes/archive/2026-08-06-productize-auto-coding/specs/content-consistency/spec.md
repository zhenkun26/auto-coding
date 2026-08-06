## Purpose

Guarantees that product naming, routing rules, stage numbering, component names, and verification claims are consistent and reproducible across all documentation.

## ADDED Requirements

### Requirement: Unified product name
All user-facing documents and metadata SHALL refer to the product as `auto-coding`; `sb_coding` may appear only as a historical reference.

#### Scenario: Name is consistent
- **WHEN** SKILL.md frontmatter, README titles, plugin metadata, and CHANGELOG are scanned
- **THEN** they all use `auto-coding` as the product name

### Requirement: Consistent complexity routing
The C0/C1a/C1b/C2 routing rules SHALL be described identically in the top-level SKILL.md and the README, with no contradictory statements about whether Nodes 2/3 run for C1b.

#### Scenario: Routing tables agree
- **WHEN** the C1b prose and the routing table in SKILL.md are compared
- **THEN** they state the same rule for when Nodes 2/3 run and what reports they produce

### Requirement: Consistent stage numbering
The pipeline SHALL use one stage count everywhere: six stages (Nodes 2/3/4/5/6/8), with no conflicting "5-stage"/"6-stage"/"8-stage" labels.

#### Scenario: Stage count is uniform
- **WHEN** SKILL.md, pipeline/SKILL.md, README.md, and README-EN.md are scanned for stage-count labels
- **THEN** every label reads "6-stage" (or the Chinese equivalent "6 阶段")

### Requirement: Component names match responsibilities
The Node 6 component SHALL be named after its responsibility (runtime verification) in directory names, skill names, and references.

#### Scenario: Runtime verification naming
- **WHEN** the pipeline directory tree and all documents referencing Node 6 are scanned
- **THEN** they use `runtime_verify` / `runtime-verify` instead of `simulator_verify` / `simulator-verify`

### Requirement: Codex-oriented bootstrap
The Phase 0 bootstrap SHALL initialize OpenSpec with Codex tooling, not Claude tooling.

#### Scenario: Bootstrap command is platform-correct
- **WHEN** the top-level SKILL.md bootstrap section is read
- **THEN** it instructs `openspec init --tools codex` and creates `.codex/` integration

### Requirement: Reproducible verification claims
README verification claims SHALL only describe verification artifacts that exist in the repository or are explicitly marked as historical/unshipped.

#### Scenario: Claims match repository contents
- **WHEN** the README quality-assurance section is compared with the repository contents
- **THEN** every claimed test suite, script, or matrix either exists in the repository or is labeled as historical and not shipped
