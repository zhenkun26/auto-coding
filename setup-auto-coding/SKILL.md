---
name: setup-auto-coding
license: MIT
description: >
  One-time per-repository configuration for the auto-coding skill, invoked as
  /setup-auto-coding. Asks for a strictness profile, primary language, and
  evidence thresholds, then writes an `## auto-coding` section into the
  repository's AGENTS.md so every future session picks it up automatically.
---

# Set Up Auto-Coding

Configure once, inside the repository's own instructions — no new config
format, no state system. Future auto-coding sessions read `AGENTS.md` at
workflow step 1, so the section below is the entire configuration surface.

## Steps

1. Run `python scripts/detect_project.py <project-root>` (or inspect the
   repository directly) to propose sensible defaults; skip any question the
   repository already answers.
2. Ask, one question at a time with 2–4 concrete options each:

   - **Strictness profile** — strict / default / light (definitions below).
   - **Primary language** — Python / TypeScript / Go / Rust / mixed.
   - **Evidence thresholds** — follow repository/CI thresholds (default), or
     name explicit coverage/lint gates.

3. Write or update an `## auto-coding` section in `AGENTS.md` (create the
   file only if it does not exist), using the template below. Editing
   AGENTS.md is a repository change: show the diff and confirm before writing.
4. Report what was written and how each future session will apply it.

## Profile definitions

| Profile | Route bias | Planning | Verification |
|---|---|---|---|
| strict | Standard by default; Fast only for trivial, easily reversible edits | Written plan from Standard up | Full adjacent-contract matrix; no alternative-evidence degradation on Standard or above |
| default | Exactly as the auto-coding routing table dictates | Plan written down at 5+ files | Route-required gates; labeled alternative evidence when blocked |
| light | Fast by default; escalate on any risk flag | Internal checklist until 10+ files | Focused checks; adjacent-contract matrix only for High-risk |

Risk flags (FINANCE / AUTH / MIGRATION / STATE_MACHINE / EXTERNAL_API /
ENV_OPS) escalate to High-risk under every profile — profiles tune ceremony,
never safety.

## AGENTS.md section template

```markdown
## auto-coding

- Profile: <strict|default|light>
- Primary language: <language> (toolchain reference: references/toolchain-<language>.md)
- Evidence thresholds: <repository/CI defaults, or explicit values>
- Authorization notes: <actions this repository always requires approval for, or "standard">
```
