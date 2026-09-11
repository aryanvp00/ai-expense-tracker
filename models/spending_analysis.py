from pydantic import BaseModel


class SpendingAnalysis(BaseModel):
    summary: str
    highest_category: str
    highest_category_amount: float
    total_spending: float
    insight: str
    