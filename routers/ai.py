from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user

from models.ai_expense_request import AIExpenseRequest
from models.assistant_request import AssistantRequest
from models.expense_request import ExpenseRequest
from models.expense_response import ExpenseResponse
from models.spending_analysis import SpendingAnalysis

from services.ai_service import (
    parse_expense,
    analyze_spending
)

from services.assistant_service import answer_question
from services.expense_service import ExpenseService


router = APIRouter()

expense_service = ExpenseService()


@router.post("/ai/parse-expense")
def parse_expense_with_ai(
    request: AIExpenseRequest,
    user_id: str = Depends(get_current_user)
):
    # Ask Gemini to understand the expense
    result = parse_expense(request.text)

    # Return the AI result without saving it
    return {
        "amount": result.amount,
        "description": result.description,
        "category": result.category.value
    }


@router.post(
    "/ai/expenses",
    response_model=ExpenseResponse
)
def create_expense_with_ai(
    request: AIExpenseRequest,
    user_id: str = Depends(get_current_user)
):
    # Step 1: Ask Gemini to understand the sentence
    result = parse_expense(request.text)

    # Step 2: Convert AI result into our
    # application's validated expense model
    expense = ExpenseRequest(
        amount=result.amount,
        description=result.description,
        category=result.category.value
    )

    # Step 3: Save the expense for this user
    new_expense = expense_service.add_expense(
        expense.amount,
        expense.description,
        expense.category,
        user_id
    )

    # Step 4: Return the saved expense
    return ExpenseResponse.from_expense(new_expense)


@router.get("/ai/dashboard-summary")
def dashboard_summary(
    user_id: str = Depends(get_current_user)
):
    """
    Calculate dashboard summary data directly in Python.

    This endpoint does NOT call Gemini.
    """

    expenses = expense_service.get_expenses(user_id)

    # Handle users with no expenses
    if not expenses:
        return {
            "total_spending": 0,
            "highest_category": "Other",
            "highest_category_amount": 0
        }

    # Calculate total spending
    total_spending = 0

    # Store spending grouped by category
    category_totals = {}

    for expense in expenses:
        total_spending += expense.amount

        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount

    # Find highest spending category
    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_category_amount = category_totals[
        highest_category
    ]

    return {
        "total_spending": total_spending,
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount
    }


@router.get(
    "/ai/spending-analysis",
    response_model=SpendingAnalysis
)
def spending_analysis(
    user_id: str = Depends(get_current_user)
):
    # Get this user's expenses
    expenses = expense_service.get_expenses(user_id)

    # Handle users with no expenses
    if not expenses:
        return {
            "summary": "You have no expenses yet.",
            "highest_category": "Other",
            "highest_category_amount": 0,
            "total_spending": 0,
            "insight": "Add some expenses to receive spending insights."
        }

    # Calculate total spending in Python
    total_spending = 0

    # Store spending grouped by category
    category_totals = {}

    for expense in expenses:
        total_spending += expense.amount

        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount

    # Find the category with the highest spending
    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_category_amount = category_totals[
        highest_category
    ]

    # Prepare exact data for Gemini
    spending_data = {
        "total_spending": total_spending,
        "category_totals": category_totals,
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount
    }

    # Ask Gemini to interpret the data
    analysis = analyze_spending(spending_data)

    return analysis


@router.post("/ai/assistant")
def financial_assistant(
    request: AssistantRequest,
    user_id: str = Depends(get_current_user)
):
    # Pass the user's ID to the assistant.
    # The assistant will retrieve the user's expenses itself.
    answer = answer_question(
        request.question,
        user_id
    )

    return {
        "answer": answer
    }