# Spec: payment service

## Interface contracts

```python
PaymentService:
    authorize(user_id: str, amount: int) -> bool
    refund(transaction_id: str) -> bool

audit_log(event: str) -> None
```
