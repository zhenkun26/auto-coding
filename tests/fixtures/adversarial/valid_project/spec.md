# Spec: user service

## Interface contracts

```python
UserService:
    create(name: str, email: str) -> int
    deactivate(user_id: int) -> bool

hash_password(plain: str) -> str
```
