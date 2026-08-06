## Purpose

Defines the hardening gates the repository must pass before release: no swallowed errors, loud CLI failures, ≥80% test coverage, 1000-concurrent-call smoke acceptance, and usable container/Kubernetes artifacts.

## ADDED Requirements

### Requirement: No swallowed exceptions
The Python tooling SHALL not contain bare `except Exception` handlers; parse and I/O failures SHALL be collected and reported.

#### Scenario: Parse failure is reported
- **WHEN** a source file cannot be parsed
- **THEN** the failure is recorded and reported instead of silently skipped

### Requirement: Loud CLI failures
The contract checker SHALL exit nonzero with a usage message when arguments are missing, invalid, or when the source directory does not exist.

#### Scenario: Missing source directory
- **WHEN** `--source` points to a nonexistent directory
- **THEN** the tool exits nonzero with an error instead of reporting zero contracts as success

### Requirement: Coverage gate
The test suite SHALL achieve at least 80% line coverage over the Python tooling modules.

#### Scenario: Coverage is measured
- **WHEN** `coverage run -m pytest` executes
- **THEN** line coverage of the tooling modules is ≥80%

### Requirement: Concurrency smoke acceptance
The CLI SHALL handle 1000 concurrent invocations without errors.

#### Scenario: Concurrent calls succeed
- **WHEN** 1000 invocations run concurrently against a valid spec/source pair
- **THEN** all invocations exit zero

### Requirement: Production container
A Dockerfile SHALL use multi-stage build, run as a non-root user, include HEALTHCHECK, use build cache mounts, and target an image under 100MB.

#### Scenario: Image builds and runs
- **WHEN** `docker build` completes
- **THEN** the image contains the tooling and runs as a non-root user

### Requirement: Kubernetes manifests
The `/deploy` directory SHALL contain Deployment with resource requests/limits and PDB, ClusterIP Service, ConfigMap, Secret with base64 placeholders, Ingress, HPA, and HTTP GET readiness/liveness probes.

#### Scenario: Manifests apply in order
- **WHEN** `kubectl apply -f /deploy` is run in the documented order
- **THEN** the resources are created without schema errors

### Requirement: Acceptance report
A Markdown report SHALL document the review findings, fixes, build/push commands, deploy order, acceptance results, and rollback plan.

#### Scenario: Report is present
- **WHEN** the change completes
- **THEN** `docs/ACCEPTANCE_REPORT.md` contains all six required sections with copy-pasteable code blocks
