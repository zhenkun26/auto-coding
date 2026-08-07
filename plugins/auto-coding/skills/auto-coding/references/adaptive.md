---
name: adaptive
description: Toolchain adaptation for auto-coding — language template detection, degradation rules for missing tools, and CI threshold priority. Read when a configured tool is unavailable or no language template matches.
---

# Toolchain Adaptation

Decide the verification strategy from the project's existing tools. Never
force-install missing tools; never silently skip configured checks.

## Template detection

Detect flag files at the project root (or run
`python scripts/detect_project.py <root>`):

| Flag files | Template | Toolchain |
|---|---|---|
| `pyproject.toml` + `src/` | Python | mypy / ruff / pytest |
| `package.json` + `tsconfig.json` | TypeScript | tsc / eslint / jest |
| `go.mod` | Go | go vet / gofmt -l / go test |
| `Cargo.toml` | Rust | cargo check / clippy / cargo test |
| None | Generic | Map an equivalent "compile/static check → lint → test" toolchain without halting; label `[CUSTOM_TOOLCHAIN]` and state the mapping in the handoff report |
| Multiple at once | — | Ask the user to choose |

## Degradation rules

| Condition | Action |
|---|---|
| Type-check config exists, tool installed | Run type checks |
| Type-check config exists, tool **not** installed | Show the install command and **halt** — no degradation; re-run after installation |
| No type-check config | Degrade to IDE diagnostics + line-by-line review, reported as `BLOCKED` + alternative evidence |
| Lint config exists, tool installed | Run lint |
| Lint config exists, tool **not** installed | Show the install command and **halt** — no degradation |
| No lint config | Degrade to AI code review, reported as `BLOCKED` + alternative evidence |
| Test framework configured | Run coverage mode (Mode A) |
| No test framework config | Degrade to behavior self-check + manual acceptance of key paths, reported as `BLOCKED` + alternative evidence |
| CI config exists (`.github/workflows/`, `.gitlab-ci.yml`, …) | Align thresholds with the CI-declared values |

Rule priority: **explicit config > degradation**. Only a project with no
corresponding config may degrade. High-risk tasks additionally follow the
non-degradable baseline in [risk-controls.md](risk-controls.md) — degradation
there still requires the flag's alternative evidence.

## Summary line

Print one line at the start of verification:

```
Adaptation: type check ✅(mypy) | lint ✅(ruff) | tests ✅(pytest, 80%) | CI aligned ✅(github-actions)
Adaptation: type check ⚠️(BLOCKED, no mypy config) | tests ⚠️(BLOCKED, no pytest) | no CI
```
