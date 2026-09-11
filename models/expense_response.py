from pydantic import BaseModel


class ExpenseResponse(BaseModel):
    id: str
    amount: float
    description: str
    category: str

    @classmethod
    def from_expense(cls, expense):
        return cls(
            id=str(expense.id),
            amount=expense.amount,
            description=expense.description,
            category=expense.category
        )