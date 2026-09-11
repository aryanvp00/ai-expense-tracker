from pydantic import BaseModel, Field


class AIExpenseRequest(BaseModel):
    text: str = Field(min_length=1)