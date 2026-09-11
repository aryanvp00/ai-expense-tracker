from datetime import datetime


class Expense:
    # Represents one expense

    def __init__(
        self,
        amount,
        description,
        category,
        expense_id=None,
        user_id=None,
        created_at=None
    ):
        self.id = expense_id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.category = category
        self.created_at = created_at

    @classmethod
    def from_mongo(cls, data):
        return cls(
            data["amount"],
            data["description"],
            data["category"],
            data["_id"],
            data.get("user_id"),
            data.get("created_at")
        )