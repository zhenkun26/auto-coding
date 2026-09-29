---
name: adaptive
description: Adapt checks when native tooling or an environment is unavailable without overstating evidence.
---

# Toolchain Adaptation

Inspect existing project commands, CI, manifests, and installed tools. In a
mixed project, select the affected toolchains; ask only when the intended
platform or acceptance environment is genuinely ambiguous. The detector is
optional discovery evidence, not authority to install or run a service.

- Configured and available: run the appropriate check.
- Configured but unavailable: report BLOCKED with the missing prerequisite.
  Use an already installed equivalent only when it establishes the same claim;
  otherwise label it alternative evidence. Preserve the required gate.
- No configured tool: choose useful existing behavioral/static checks based on
  the task. Missing configuration is not automatically a defect or permission
  to install a framework. Report any material verification gap.
- Unsupported environment: keep platform-specific acceptance blocked and
  distinguish local evidence from target-runtime evidence.

Honor existing installation authority; ask before adding a new dependency.
Do not stop unrelated authorized work because one check is unavailable. A
material blocked gate prevents acceptance of its affected outcome. Explain
what can resolve it and the next executable action.
