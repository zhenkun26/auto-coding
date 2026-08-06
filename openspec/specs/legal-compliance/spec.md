# legal-compliance Specification

## Purpose
Establishes the legal baseline for publishing the repository: an MIT license for original content and explicit attribution for bundled third-party skills.
## Requirements
### Requirement: Repository license
The repository SHALL include an MIT `LICENSE` file covering the original content authored for this skill set.

#### Scenario: License is present
- **WHEN** the repository is published
- **THEN** a valid MIT `LICENSE` file exists at the repository root

### Requirement: Third-party attribution
The repository SHALL include a `THIRD_PARTY.md` file listing each bundled third-party component, its origin, and its license.

#### Scenario: Third-party components are documented
- **WHEN** a reviewer opens `THIRD_PARTY.md`
- **THEN** they find entries for ponytail (MIT, DietrichGebert) and the OpenSpec skills (MIT, Fission-AI), each with source and license

### Requirement: License metadata in skills
Every bundled skill's `SKILL.md` frontmatter SHALL declare a `license` field consistent with the repository license.

#### Scenario: Frontmatter is consistent
- **WHEN** all `SKILL.md` files in the repository are scanned
- **THEN** each one carries a `license: MIT` field or an explicit exception documented in `THIRD_PARTY.md`

