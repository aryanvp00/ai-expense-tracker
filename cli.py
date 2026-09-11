import requests


BASE_URL = "http://127.0.0.1:8000"


def register():
    print("\n--- Register ---")

    username = input("Username: ")
    password = input("Password: ")

    response = requests.post(
        f"{BASE_URL}/register",
        json={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 201:
        print("Registration successful!")
    else:
        print("Registration failed:")
        print(response.json())


def login():
    print("\n--- Login ---")

    username = input("Username: ")
    password = input("Password: ")

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:
        data = response.json()

        token = data["access_token"]

        print("Login successful!")

        return token

    print("Login failed:")
    print(response.json())

    return None


def expense_menu(token):
    while True:
        print("\n==============================")
        print("       EXPENSE TRACKER")
        print("==============================")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spending")
        print("4. View by Category")
        print("5. Update Expense")
        print("6. Delete Expense")
        print("7. Logout")

        choice = input("\nChoose an option: ")

        # --------------------------------
        # 1. ADD EXPENSE
        # --------------------------------
        if choice == "1":
            try:
                amount = float(input("Amount: "))
                description = input("Description: ")
                category = input("Category: ")

                response = requests.post(
                    f"{BASE_URL}/expenses",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    json={
                        "amount": amount,
                        "description": description,
                        "category": category
                    }
                )

                if response.status_code == 201:
                    expense = response.json()

                    print("\nExpense added successfully!")
                    print(f"ID: {expense['id']}")
                    print(f"Amount: {expense['amount']}")
                    print(f"Description: {expense['description']}")
                    print(f"Category: {expense['category']}")

                else:
                    print("\nFailed to add expense:")
                    print(response.json())

            except ValueError:
                print("Amount must be a number.")

        # --------------------------------
        # 2. VIEW EXPENSES
        # --------------------------------
        elif choice == "2":
            response = requests.get(
                f"{BASE_URL}/expenses",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            if response.status_code == 200:
                expenses = response.json()

                if not expenses:
                    print("\nNo expenses found.")
                else:
                    print("\n--- Your Expenses ---")

                    for expense in expenses:
                        print(
                            f"\nID: {expense['id']}"
                            f"\nAmount: {expense['amount']}"
                            f"\nDescription: {expense['description']}"
                            f"\nCategory: {expense['category']}"
                        )

            else:
                print("\nFailed to get expenses:")
                print(response.json())

        # --------------------------------
        # 3. TOTAL SPENDING
        # --------------------------------
        elif choice == "3":
            response = requests.get(
                f"{BASE_URL}/expenses/total",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            if response.status_code == 200:
                data = response.json()

                print(
                    f"\nTotal Spending: ₹{data['total']}"
                )

            else:
                print("\nFailed to get total:")
                print(response.json())

        # --------------------------------
        # 4. VIEW BY CATEGORY
        # --------------------------------
        elif choice == "4":
            category = input("Enter category: ")

            response = requests.get(
                f"{BASE_URL}/expenses/category/{category}",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            if response.status_code == 200:
                expenses = response.json()

                if not expenses:
                    print(
                        f"\nNo expenses found in "
                        f"'{category}'."
                    )
                else:
                    print(
                        f"\n--- {category} Expenses ---"
                    )

                    for expense in expenses:
                        print(
                            f"\nID: {expense['id']}"
                            f"\nAmount: {expense['amount']}"
                            f"\nDescription: {expense['description']}"
                            f"\nCategory: {expense['category']}"
                        )

            else:
                print("\nFailed to get expenses:")
                print(response.json())

        # --------------------------------
        # 5. UPDATE EXPENSE
        # --------------------------------
        elif choice == "5":
            expense_id = input("Enter expense ID: ")

            try:
                amount = float(input("New amount: "))
                description = input("New description: ")
                category = input("New category: ")

                response = requests.put(
                    f"{BASE_URL}/expenses/{expense_id}",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    json={
                        "amount": amount,
                        "description": description,
                        "category": category
                    }
                )

                if response.status_code == 200:
                    expense = response.json()

                    print("\nExpense updated successfully!")
                    print(f"ID: {expense['id']}")
                    print(f"Amount: {expense['amount']}")
                    print(
                        f"Description: "
                        f"{expense['description']}"
                    )
                    print(
                        f"Category: "
                        f"{expense['category']}"
                    )

                else:
                    print("\nFailed to update expense:")
                    print(response.json())

            except ValueError:
                print("Amount must be a number.")

        # --------------------------------
        # 6. DELETE EXPENSE
        # --------------------------------
        elif choice == "6":
            expense_id = input("Enter expense ID: ")

            response = requests.delete(
                f"{BASE_URL}/expenses/{expense_id}",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            if response.status_code == 200:
                print("\nExpense deleted successfully!")

            else:
                print("\nFailed to delete expense:")
                print(response.json())

        # --------------------------------
        # 7. LOGOUT
        # --------------------------------
        elif choice == "7":
            print("\nLogged out successfully!")
            return

        else:
            print("Invalid option.")


def main():
    while True:
        print("\n==============================")
        print("       EXPENSE TRACKER")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            register()

        elif choice == "2":
            token = login()

            if token is not None:
                expense_menu(token)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()