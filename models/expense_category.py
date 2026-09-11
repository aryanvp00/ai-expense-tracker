from enum import Enum


class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    BILLS = "Bills"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    TRAVEL = "Travel"
    EDUCATION = "Education"
    OTHER = "Other"