from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    question: str = Field(min_length=1)
    