"""Deliberately incomplete implementation: only authorize matches the spec."""


class PaymentService:
    def authorize(self, user_id: str, amount: int) -> bool:
        return amount > 0

    def refund(self, transaction_id: str, extra_arg: str) -> bool:
        return True
