# Spec: report generator

The pipeline first calls validate(report: str) -> bool and then runs
render(report: str, fmt: str) -> str internally; those are prose mentions
of internal helpers, not interface contracts, and must be ignored.

## Interface contracts

```python
generate(title: str) -> str
```
