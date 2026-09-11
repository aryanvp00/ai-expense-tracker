# Import the service that handles expense logic
from services.expense_service import ExpenseService


# Create our expense service
expense_service = ExpenseService()


while True:
    print("===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. View by Category")
    print("5. Update Expense")
    print("6. Delete Expense")
    print("7. Exit")

    choice = input("Choose an option: ")

    # Add Expense
    if choice == "1":
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")
        category = input("Enter category: ")

        expense_service.add_expense(
            amount,
            description,
            category
        )

        print("Expense added successfully.")

    # View Expenses
    elif choice == "2":
        expenses = expense_service.get_expenses()

        print("\n----- YOUR EXPENSES -----")

        for expense in expenses:
            print("ID:", expense.id)
            print("Amount:", expense.amount)
            print("Description:", expense.description)
            print("Category:", expense.category)
            print("-------------------------")

    # Total Spending
    elif choice == "3":
        total = expense_service.get_total()

        print("Total Spending:", total)

    # View by Category
    elif choice == "4":
        category = input("Enter category: ")

        expenses = expense_service.get_by_category(category)

        print("\n----- EXPENSES -----")

        for expense in expenses:
            print("ID:", expense.id)
            print("Amount:", expense.amount)
            print("Description:", expense.description)
            print("Category:", expense.category)
            print("-------------------------")

    # Update Expense
    elif choice == "5":
        expense_id = input("Enter Expense ID to update: ")

        amount = float(input("Enter new amount: "))
        description = input("Enter new description: ")
        category = input("Enter new category: ")

        updated = expense_service.update_expense(
            expense_id,
            amount,
            description,
            category
        )

        if updated:
            print("Expense updated successfully.")
        else:
            print("Expense not found or nothing changed.")

    # Delete Expense
    elif choice == "6":
        expense_id = input("Enter Expense ID to delete: ")

        deleted = expense_service.delete_expense(expense_id)

        if deleted:
            print("Expense deleted successfully.")
        else:
            print("Expense not found.")

    # Exit
    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")