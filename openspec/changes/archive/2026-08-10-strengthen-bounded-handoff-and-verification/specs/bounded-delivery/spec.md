## Purpose

为 `auto-coding` 定义可观察、可验证的有界交付行为，使任务拆分、OpenSpec 交接、修复验证和最终证据不会因文件数量、模型声明或陈旧报告而失真。

## ADDED Requirements

### Requirement: Outcome-bounded task decomposition
For Standard and High-risk work, `auto-coding` SHALL decompose work by one verifiable outcome, one primary risk boundary, and one independent acceptance gate rather than requiring every task to modify only one source file.

#### Scenario: Coherent implementation and test change stays together
- **WHEN** one behavior change requires implementation code, focused tests, and a directly related contract update
- **THEN** `auto-coding` keeps them in one bounded task when they share the same outcome, primary risk, and acceptance gate

#### Scenario: Independent outcomes are split
- **WHEN** requested work contains multiple outcomes with independently meaningful acceptance results
- **THEN** `auto-coding` splits them into separate ordered tasks before implementation

### Requirement: Explicit execution authority
`auto-coding` SHALL distinguish standalone execution from OpenSpec-managed execution and SHALL treat applicable OpenSpec artifacts and instructions as the planning boundary without creating a competing phase status system.

#### Scenario: OpenSpec-managed work remains within its boundary
- **WHEN** an applicable OpenSpec change governs an implementation request
- **THEN** `auto-coding` resolves the current artifacts and apply instructions, implements only the bounded work, and stops on contradictions or required scope expansion

#### Scenario: Standalone work does not create phase artifacts
- **WHEN** a bounded request is not governed by a specification system and does not require multi-stage decomposition
- **THEN** `auto-coding` plans proportionally without creating `STATUS.md`, `STEP_*.md`, or another persistent phase tree

### Requirement: Verification precedes completion claims
`auto-coding` SHALL NOT mark an OpenSpec task or acceptance state complete solely because implementation files were changed; the task-specific acceptance evidence MUST be executed and classified first.

#### Scenario: Implementation succeeds but required verification is blocked
- **WHEN** code is implemented but a required acceptance check cannot execute
- **THEN** `auto-coding` reports the check as `BLOCKED`, leaves the completion claim unresolved, and separates any alternative evidence from a pass

#### Scenario: Task is checked only after its gate passes
- **WHEN** the implementation and the task-specific acceptance checks satisfy their criteria
- **THEN** `auto-coding` may reconcile the corresponding OpenSpec task as complete and records the actual evidence used

### Requirement: Adjacent contract verification
For a behavior or contract repair, `auto-coding` SHALL verify every relevant adjacent path among default input, caller override, missing or invalid input, failure cleanup, and preserved compatibility in addition to the original reproduction.

#### Scenario: A localized repair has adjacent callers
- **WHEN** a fix changes a default, parser, public contract, fallback, cleanup path, or compatibility behavior
- **THEN** the verification evidence includes the original reproduction and each relevant adjacent path, with irrelevant paths explicitly omitted rather than implied to have passed

### Requirement: Ordered evidence production
`auto-coding` SHALL produce evidence in the order implementation, focused regression, relevant adjacent checks, relevant broader gates, raw results, and only then delivery or acceptance summaries.

#### Scenario: Behavior changes after a previous report
- **WHEN** code changes after a report or test result was generated
- **THEN** `auto-coding` treats affected evidence as stale and regenerates it before publishing a passing claim

### Requirement: Repair-loop stop condition
`auto-coding` SHALL stop iterative patching and return to the governing invariant and root cause when repeated repair attempts introduce consecutive material regressions in the same bounded task.

#### Scenario: Consecutive repairs break adjacent behavior
- **WHEN** two consecutive repair rounds introduce a new failure in a declared acceptance path or preserved contract
- **THEN** `auto-coding` stops adding patches, records the reproductions, reviews the root cause, and splits or replans the task before continuing

### Requirement: Proportional pre-code rehearsal
`auto-coding` SHALL require a pre-code rehearsal for High-risk work, external side effects, or explicit cross-session/model handoff, and SHALL NOT impose that rehearsal on ordinary Fast work.

#### Scenario: High-risk task crosses an external-effect boundary
- **WHEN** a High-risk task can reach a network, process, notification, persistent user data, migration, or irreversible action
- **THEN** the rehearsal identifies file touchpoints, the entry-to-effect call chain, shared mutable state, test isolation, likely mistakes with detecting tests, and the stop condition before editing

### Requirement: Non-destructive failure handling
`auto-coding` SHALL preserve the failed working state for diagnosis and SHALL NOT automatically run a version-control restore command that could overwrite pre-existing user changes.

#### Scenario: Static verification fails
- **WHEN** type checking, linting, compilation, or tests fail after an edit
- **THEN** `auto-coding` reports the exact failure and affected task files without automatically reverting them through `git checkout`, reset, or an equivalent destructive restore

### Requirement: Repository-native verification policy
`auto-coding` SHALL prefer validation commands and thresholds declared by the repository or CI; fallback thresholds SHALL be labeled as defaults rather than represented as project-proven acceptance criteria.

#### Scenario: Repository declares its own coverage threshold
- **WHEN** CI or project configuration defines a coverage, lint, type, or test gate
- **THEN** `auto-coding` applies that gate instead of a conflicting built-in threshold

### Requirement: Detected toolchains have actionable guidance
Every language explicitly detected by the shipped project detector SHALL have routed verification guidance and detector tests for its manifest and primary tool availability.

#### Scenario: Go or Rust project is detected
- **WHEN** the project contains `go.mod` or `Cargo.toml`
- **THEN** `auto-coding` routes to the corresponding toolchain guidance and reports the relevant local tool availability without installing anything
