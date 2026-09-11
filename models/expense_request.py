from pydantic import BaseModel, Field


class ExpenseRequest(BaseModel):
    amount: float = Field(gt=0)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)