class FinancialService:
    """Handles deterministic financial calculations."""

    def get_total_spending(self, expenses):
        total = 0

        for expense in expenses:
            total += expense.amount

        return total

    def get_category_spending(self, expenses, category):
        total = 0

        for expense in expenses:
            if expense.category.lower() == category.lower():
                total += expense.amount

        return total

    def get_highest_category(self, expenses):
        category_totals = {}

        for expense in expenses:
            category = expense.category

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += expense.amount

        if not category_totals:
            return None, 0

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        return (
            highest_category,
            category_totals[highest_category]
        )

    def calculate(
        self,
        expenses,
        intent,
        category=None
    ):
        if intent == "total_spending":
            return {
                "total": self.get_total_spending(expenses)
            }

        if intent == "category_spending":
            return {
                "category": category,
                "total": self.get_category_spending(
                    expenses,
                    category
                )
            }

        if intent == "highest_category":
            category, amount = self.get_highest_category(
                expenses
            )

            return {
                "category": category,
                "amount": amount
            }

        return {}

    def compare_spending(
        self,
        current_expenses,
        previous_expenses
    ):
        current_total = self.get_total_spending(
            current_expenses
        )

        previous_total = self.get_total_spending(
            previous_expenses
        )

        difference = current_total - previous_total

        if previous_total == 0:
            percentage_change = None
        else:
            percentage_change = (
                difference / previous_total
            ) * 100

        return {
            "current_total": current_total,
            "previous_total": previous_total,
            "difference": difference,
            "percentage_change": percentage_change
        }

    def compare_category_spending(
        self,
        current_expenses,
        previous_expenses,
        category
    ):
        current_total = self.get_category_spending(
            current_expenses,
            category
        )

        previous_total = self.get_category_spending(
            previous_expenses,
            category
        )

        difference = current_total - previous_total

        if previous_total == 0:
            percentage_change = None
        else:
            percentage_change = (
                difference / previous_total
            ) * 100

        return {
            "category": category,
            "current_total": current_total,
            "previous_total": previous_total,
            "difference": difference,
            "percentage_change": percentage_change
        }

    def build_insight_data(self, expenses):
        total_spending = self.get_total_spending(expenses)

        category_totals = {}

        for expense in expenses:
            category = expense.category

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += expense.amount

        highest_category = None
        highest_category_amount = 0

        if category_totals:
            highest_category = max(
                category_totals,
                key=category_totals.get
            )

            highest_category_amount = (
                category_totals[highest_category]
            )

        return {
            "total_spending": total_spending,
            "category_totals": category_totals,
            "highest_category": highest_category,
            "highest_category_amount": highest_category_amount,
            "expense_count": len(expenses)
        }