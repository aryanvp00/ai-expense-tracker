import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

from models.expense_category import ExpenseCategory
from models.spending_analysis import SpendingAnalysis

# Load variables from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


class ExpenseAIResult(BaseModel):
    amount: float = Field(
        description="The amount of money spent"
    )

    description: str = Field(
        description="What the money was spent on"
    )

    category: ExpenseCategory = Field(
        description="The expense category"
    )


def parse_expense(text):
    """
    Convert a natural-language expense
    into structured expense data.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        Extract the expense information from this sentence.

        Choose the category ONLY from the allowed categories.

        Allowed categories:
        Food
        Transport
        Shopping
        Bills
        Entertainment
        Health
        Travel
        Education
        Other

        If the expense does not clearly fit
        another category, use Other.

        Expense:
        {text}
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": ExpenseAIResult,
        },
    )

    return response.parsed

def analyze_spending(spending_data):
    """
    Use Gemini to interpret already-calculated
    spending data.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        Analyze the user's spending data below.

        Spending data:
        {spending_data}

        Write:
        1. A short summary.
        2. The highest spending category.
        3. The amount spent in that category.
        4. The total spending.
        5. One useful financial insight.

        IMPORTANT:
        - Use only the numbers provided.
        - Do not recalculate or invent numbers.
        - Keep the analysis concise.
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": SpendingAnalysis,
        },
    )

    return response.parsed