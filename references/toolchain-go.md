---
name: toolchain-go
description: Go toolchain commands for auto-coding — format checking, vetting, focused and package tests, race detection, and module safety. Read when the project is Go.
---

# Go Toolchain

Prefer commands declared by the repository (CI, Makefile, task runner) over
the fallbacks below. Project package boundaries and build tags determine the
real verification scope.

## Commands

| Purpose | Command |
|---|---|
| L0 compile/import check | `go test ./<affected-package> -run '^$'` |
| L1 focused behavior check | `go test ./<affected-package> -run '<TestName>'` |
| Format gate | `gofmt -l <modified-go-files>` (output must be empty) |
| Static gate | `go vet ./<affected-packages>` |
| Package regression | `go test ./<affected-packages>` |
| Repository regression | `go test ./...` |
| Race/concurrency gate | `go test -race ./<affected-packages>` when concurrency, shared state, or goroutines are affected |

## Notes

- Preserve repository build tags and platform targets. A default `go test`
  does not prove tagged or cross-platform variants.
- Run the race detector for changed concurrent behavior when the platform
  supports it; an unavailable detector is `BLOCKED`, not a normal test pass.
- Do not run `go get`, `go mod tidy`, or dependency upgrades automatically;
  they can change `go.mod` and `go.sum` and require the task's authority.
- Perform the manual L2 contract comparison from
  [implementation.md](implementation.md); the bundled structural checker is
  Python-only.

## Degradation

Missing configured Go tooling or an unavailable target environment follows
[adaptive.md](adaptive.md): report `BLOCKED` with safe alternative inspection,
without installing tools or rewriting module files.
