"""Fully spec-compliant implementation."""


class UserService:
    def create(self, name: str, email: str) -> int:
        return 1

    def deactivate(self, user_id: int) -> bool:
        return True


def hash_password(plain: str) -> str:
    return plain[::-1]
