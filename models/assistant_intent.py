from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AssistantIntent(str, Enum):
    TOTAL_SPENDING = "total_spending"
    CATEGORY_SPENDING = "category_spending"
    HIGHEST_CATEGORY = "highest_category"
    COMPARE_SPENDING = "compare_spending"
    CATEGORY_COMPARISON = "category_comparison"
    GENERAL = "general"


class SpendingPeriod(str, Enum):
    ALL_TIME = "all_time"
    TODAY = "today"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"


class AssistantIntentResult(BaseModel):
    intent: AssistantIntent
    category: Optional[str] = None
    period: SpendingPeriod = SpendingPeriod.ALL_TIME