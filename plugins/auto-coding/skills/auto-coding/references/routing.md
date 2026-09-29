---
name: routing
description: Choose execution depth by behavioral impact, uncertainty, and recovery cost when the route is unclear.
---

# Execution Depth

| Route | Use when | Depth |
|---|---|---|
| Fast | The outcome is clear, local, low impact, and readily recoverable | Inspect, change, focused verification |
| Standard | Behavior, multiple consumers, or meaningful uncertainty need coordination | Concise plan, coherent implementation, relevant regression and review |
| High-risk | A mistake can materially affect security, money, persisted data, availability, or external systems | Explicit invariants, effect boundaries, recovery and stronger acceptance evidence |

Risk overrides diff size. File counts, a topic keyword, or a large repository
alone do not determine the route. Changes to auth decisions, precision of money,
production migrations, consequential transitions, real external effects, or
service lifecycle normally require High-risk treatment; editing their prose or
an isolated example does not inherit that risk automatically.

Use [risk-controls.md](risk-controls.md) for affected high-risk behavior. Missing
tools do not reduce its required evidence. Explain the route briefly only when
it changes how the work proceeds.

Existing code requires tracing affected definitions and consumers. New code
still requires inspecting repository conventions and integrations. Large scope
is handled by independently acceptable outcomes, not a fixed task-count limit.
Respect an explicit phase stop; otherwise a technical checkpoint does not end
an authorized multi-outcome assignment.
