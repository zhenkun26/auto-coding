---
name: toolchain-rust
description: Rust toolchain commands for auto-coding — format checking, clippy, focused and workspace tests, feature matrices, and configured concurrency checks. Read when the project is Rust.
---

# Rust Toolchain

Prefer repository-declared CI, workspace aliases, feature sets, and target
triples over the fallbacks below. Preserve the repository's supported toolchain
and MSRV rather than silently selecting a newer compiler.

## Commands

| Purpose | Command |
|---|---|
| L0 compile check | `cargo check -p <affected-package>` |
| L1 focused behavior check | `cargo test -p <affected-package> <test-name>` |
| Format gate | `cargo fmt --all --check` |
| Static gate | `cargo clippy --workspace --all-targets -- -D warnings` |
| Package regression | `cargo test -p <affected-package>` |
| Workspace regression | `cargo test --workspace --all-targets` |
| Feature matrix | Repository-declared feature jobs; otherwise targeted `cargo test --no-default-features` / `cargo test --all-features` when those combinations are supported |
| Concurrency gate | Existing Loom, Miri, sanitizer, or stress tests when configured for the changed behavior |

## Notes

- A default-feature build does not prove optional or production feature
  combinations. Report exactly which feature sets and targets executed.
- Do not claim Loom, Miri, sanitizer, or cross-target evidence unless the
  repository configures it and the command actually runs.
- Do not run `cargo add`, `cargo update`, or toolchain installation
  automatically; manifest, lockfile, and compiler changes require authority.
- Perform the manual L2 contract comparison from
  [implementation.md](implementation.md); the bundled structural checker is
  Python-only.

## Degradation

Missing configured Rust tooling, feature dependencies, or target environments
follows [adaptive.md](adaptive.md): report `BLOCKED` and separate any safe
alternative inspection from an executed pass.
