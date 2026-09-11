from pydantic import BaseModel


class TotalResponse(BaseModel):
    total: float