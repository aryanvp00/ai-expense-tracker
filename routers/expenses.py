from fastapi import APIRouter, status, HTTPException, Depends

from dependencies.auth import get_current_user

from models.expense_request import ExpenseRequest
from models.expense_response import ExpenseResponse
from models.total_response import TotalResponse
from services.expense_service import ExpenseService


router = APIRouter()

expense_service = ExpenseService()


@router.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(user_id: str = Depends(get_current_user)):
    expenses = expense_service.get_expenses(user_id)

    return [
        ExpenseResponse.from_expense(expense)
        for expense in expenses
    ]


@router.get(
    "/expenses/category/{category}",
    response_model=list[ExpenseResponse]
)
def get_expenses_by_category(
    category: str,
    user_id: str = Depends(get_current_user)
):
    expenses = expense_service.get_by_category(
        category,
        user_id
    )

    return [
        ExpenseResponse.from_expense(expense)
        for expense in expenses
    ]


@router.get("/expenses/total", response_model=TotalResponse)
def get_total(user_id: str = Depends(get_current_user)):
    total = expense_service.get_total(user_id)

    return {"total": total}


@router.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: str,
    user_id: str = Depends(get_current_user)
):
    expense = expense_service.get_expense(
        expense_id,
        user_id
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return ExpenseResponse.from_expense(expense)


@router.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_expense(
    expense: ExpenseRequest,
    user_id: str = Depends(get_current_user)
):
    new_expense = expense_service.add_expense(
        expense.amount,
        expense.description,
        expense.category,
        user_id
    )

    return ExpenseResponse.from_expense(new_expense)


@router.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: str,
    expense: ExpenseRequest,
    user_id: str = Depends(get_current_user)
):
    updated_expense = expense_service.update_expense(
        expense_id,
        expense.amount,
        expense.description,
        expense.category,
        user_id
    )

    if updated_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return ExpenseResponse.from_expense(updated_expense)


@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: str,
    user_id: str = Depends(get_current_user)
):
    success = expense_service.delete_expense(
        expense_id,
        user_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return {"message": "Expense deleted successfully"}