# Third-Party Components

This repository adapts or historically bundled the following third-party
components. Each component retains its own license; the MIT license in
`LICENSE` covers only the original content authored for auto-coding.

| Component | Source | License | Notes |
|:---|:---|:---|:---|
| Reuse ladder (references/implementation.md) | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT | The reuse ladder, no-laziness boundaries, money rule, and `ponytail:` comment convention are adapted from the Ponytail skill. Releases up to 0.1.x bundled the full skill under `ponytail_code/`; 0.2.0 condenses it into references. |
| OpenSpec skills (removed in 0.2.0) | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | MIT | Releases up to 0.1.x bundled the OpenSpec CLI's generated skills under `openspec/skills/` for offline use. They are regenerable via `openspec init --tools codex` and are no longer redistributed. |
| grill-me (removed in 0.2.0) | 原创（author-created） | MIT | The decision-grilling flow is condensed into `references/planning.md`. Historical attribution note: if grill-me was adapted from a third-party source, the original source should be credited here. |
| codex-skills comparative checkout (not distributed) | [kingoftaro/codex-skills](https://github.com/kingoftaro/codex-skills) | MIT (owner-approved for this use) | The untracked `references/codex-skills/` checkout is design input only. Its files are independently reviewed rather than copied, are excluded from the generated plugin bundle, and receive an exact-path license override in `scripts/check_repo.py`. |

## License compatibility

All adapted components are MIT-licensed, so the repository as a whole can be
distributed under MIT. See `LICENSE` for the repository license.
