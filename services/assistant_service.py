from models.assistant_intent import (
    AssistantIntent,
    AssistantIntentResult,
    SpendingPeriod
)

from services.ai_service import client
from services.expense_service import ExpenseService
from services.financial_service import FinancialService

from utils.date_utils import (
    get_date_range,
    get_this_month_range,
    get_last_month_range
)


financial_service = FinancialService()
expense_service = ExpenseService()


def try_rule_based_intent(question):
    """
    Detect common financial questions using normal Python rules.

    This avoids an AI call when the question is predictable.
    """

    question_lower = question.lower().strip()

    # ---------------------------------------------------------
    # 1. Detect time period
    # ---------------------------------------------------------

    period = SpendingPeriod.ALL_TIME

    if "today" in question_lower:
        period = SpendingPeriod.TODAY

    elif "this month" in question_lower:
        period = SpendingPeriod.THIS_MONTH

    elif "last month" in question_lower:
        period = SpendingPeriod.LAST_MONTH

    # ---------------------------------------------------------
    # 2. Detect total spending comparisons
    # ---------------------------------------------------------

    comparison_phrases = [
        "did i spend more this month",
        "did i spend less this month",
        "compare this month and last month",
        "compare this month to last month",
        "compare my spending this month",
        "this month compared to last month"
    ]

    for phrase in comparison_phrases:
        if phrase in question_lower:
            return AssistantIntentResult(
                intent=AssistantIntent.COMPARE_SPENDING,
                period=SpendingPeriod.THIS_MONTH
            )

    # ---------------------------------------------------------
    # 3. Detect category comparisons
    # ---------------------------------------------------------

    categories = [
        "food",
        "transport",
        "shopping",
        "bills",
        "entertainment",
        "health",
        "travel",
        "education",
        "other"
    ]

    if (
        "this month" in question_lower
        and "last month" in question_lower
    ):
        for category in categories:

            if category in question_lower:

                if (
                    "spend more" in question_lower
                    or "spend less" in question_lower
                    or "compare" in question_lower
                ):
                    return AssistantIntentResult(
                        intent=AssistantIntent.CATEGORY_COMPARISON,
                        category=category.title(),
                        period=SpendingPeriod.THIS_MONTH
                    )

    # ---------------------------------------------------------
    # 4. Detect category spending
    # ---------------------------------------------------------

    category_phrases = [
        "how much did i spend on",
        "how much have i spent on",
        "spending on",
        "spent on"
    ]

    for category in categories:

        if category in question_lower:

            for phrase in category_phrases:

                if phrase in question_lower:
                    return AssistantIntentResult(
                        intent=AssistantIntent.CATEGORY_SPENDING,
                        category=category.title(),
                        period=period
                    )

    # ---------------------------------------------------------
    # 5. Detect highest spending category
    # ---------------------------------------------------------

    highest_phrases = [
        "where do i spend the most",
        "which category do i spend the most",
        "what do i spend the most on",
        "highest spending category"
    ]

    for phrase in highest_phrases:

        if phrase in question_lower:
            return AssistantIntentResult(
                intent=AssistantIntent.HIGHEST_CATEGORY,
                period=period
            )

    # ---------------------------------------------------------
    # 6. Detect total spending
    # ---------------------------------------------------------

    total_phrases = [
        "how much did i spend",
        "how much have i spent",
        "what is my total spending",
        "what's my total spending",
        "total spending"
    ]

    for phrase in total_phrases:

        if phrase in question_lower:
            return AssistantIntentResult(
                intent=AssistantIntent.TOTAL_SPENDING,
                period=period
            )

    # ---------------------------------------------------------
    # No confident rule-based match
    # ---------------------------------------------------------

    return None


def detect_intent(question):
    """
    Determine what the user wants.

    First try Python rules.
    If no confident rule matches, use Gemini.
    """

    # Try deterministic Python rules first
    rule_result = try_rule_based_intent(question)

    if rule_result is not None:
        return rule_result

    # ---------------------------------------------------------
    # AI fallback
    # ---------------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        Understand the user's financial question.

        Possible intents:

        total_spending
        - User wants their total spending.

        category_spending
        - User wants spending for a specific category.

        highest_category
        - User wants to know which category has the
          highest spending.

        compare_spending
        - User wants to compare total spending between
          this month and last month.

        category_comparison
        - User wants to compare spending for a specific
          category between this month and last month.

        general
        - Anything that does not fit the above.

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

        Possible periods:

        all_time
        - No specific time period.

        today
        - User asks about today.

        this_month
        - User asks about the current month.

        last_month
        - User asks about the previous month.

        User question:
        {question}

        Return:
        - the appropriate intent
        - the category if applicable
        - the time period if applicable
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": AssistantIntentResult,
        },
    )

    return response.parsed


def answer_question(question, user_id):
    """
    Main financial assistant flow.
    """

    # ---------------------------------------------------------
    # Step 1: Understand the question
    # ---------------------------------------------------------

    intent_result = detect_intent(question)

    # ---------------------------------------------------------
    # Step 2: Determine requested period
    # ---------------------------------------------------------

    start_date, end_date = get_date_range(
        intent_result.period.value
    )

    # ---------------------------------------------------------
    # Step 3: Retrieve relevant expenses
    # ---------------------------------------------------------

    if start_date is not None:

        expenses = expense_service.get_expenses_by_date_range(
            user_id,
            start_date,
            end_date
        )

    else:

        expenses = expense_service.get_expenses(user_id)

    # ---------------------------------------------------------
    # Step 4: Total spending
    # ---------------------------------------------------------

    if intent_result.intent == AssistantIntent.TOTAL_SPENDING:

        total = financial_service.get_total_spending(
            expenses
        )

        return f"You spent ₹{total:.2f}."

    # ---------------------------------------------------------
    # Step 5: Category spending
    # ---------------------------------------------------------

    if intent_result.intent == AssistantIntent.CATEGORY_SPENDING:

        category = intent_result.category

        total = financial_service.get_category_spending(
            expenses,
            category
        )

        return f"You spent ₹{total:.2f} on {category}."

    # ---------------------------------------------------------
    # Step 6: Highest spending category
    # ---------------------------------------------------------

    if intent_result.intent == AssistantIntent.HIGHEST_CATEGORY:

        category, amount = (
            financial_service.get_highest_category(
                expenses
            )
        )

        if category is None:
            return "You don't have any expenses for this period."

        return (
            f"You spend the most on {category}, "
            f"with ₹{amount:.2f} spent."
        )

    # ---------------------------------------------------------
    # Step 7: Compare total spending
    # ---------------------------------------------------------

    if intent_result.intent == AssistantIntent.COMPARE_SPENDING:

        current_start, current_end = get_this_month_range()
        previous_start, previous_end = get_last_month_range()

        current_expenses = (
            expense_service.get_expenses_by_date_range(
                user_id,
                current_start,
                current_end
            )
        )

        previous_expenses = (
            expense_service.get_expenses_by_date_range(
                user_id,
                previous_start,
                previous_end
            )
        )

        comparison = financial_service.compare_spending(
            current_expenses,
            previous_expenses
        )

        current_total = comparison["current_total"]
        previous_total = comparison["previous_total"]
        difference = comparison["difference"]
        percentage = comparison["percentage_change"]

        if previous_total == 0:

            return (
                f"You spent ₹{current_total:.2f} "
                f"this month compared with ₹0.00 last month."
            )

        if difference > 0:

            return (
                f"You spent {percentage:.1f}% more "
                f"this month than last month "
                f"(₹{current_total:.2f} vs "
                f"₹{previous_total:.2f})."
            )

        if difference < 0:

            return (
                f"You spent {abs(percentage):.1f}% less "
                f"this month than last month "
                f"(₹{current_total:.2f} vs "
                f"₹{previous_total:.2f})."
            )

        return (
            f"You spent the same amount this month "
            f"and last month: ₹{current_total:.2f}."
        )

    # ---------------------------------------------------------
    # Step 8: Compare category spending
    # ---------------------------------------------------------

    if intent_result.intent == AssistantIntent.CATEGORY_COMPARISON:

        category = intent_result.category

        current_start, current_end = get_this_month_range()
        previous_start, previous_end = get_last_month_range()

        current_expenses = (
            expense_service.get_expenses_by_date_range(
                user_id,
                current_start,
                current_end
            )
        )

        previous_expenses = (
            expense_service.get_expenses_by_date_range(
                user_id,
                previous_start,
                previous_end
            )
        )

        comparison = (
            financial_service.compare_category_spending(
                current_expenses,
                previous_expenses,
                category
            )
        )

        current_total = comparison["current_total"]
        previous_total = comparison["previous_total"]
        difference = comparison["difference"]
        percentage = comparison["percentage_change"]

        if previous_total == 0:

            return (
                f"You spent ₹{current_total:.2f} "
                f"on {category} this month, compared "
                f"with ₹0.00 last month."
            )

        if difference > 0:

            return (
                f"You spent {percentage:.1f}% more on "
                f"{category} this month than last month "
                f"(₹{current_total:.2f} vs "
                f"₹{previous_total:.2f})."
            )

        if difference < 0:

            return (
                f"You spent {abs(percentage):.1f}% less on "
                f"{category} this month than last month "
                f"(₹{current_total:.2f} vs "
                f"₹{previous_total:.2f})."
            )

        return (
            f"You spent the same amount on {category} "
            f"this month and last month: "
            f"₹{current_total:.2f}."
        )

    # ---------------------------------------------------------
    # Step 9: Open-ended question
    # ---------------------------------------------------------

    return ask_financial_assistant(
        question,
        expenses
    )


def ask_financial_assistant(question, expenses):
    """
    Use the LLM only for open-ended financial questions.

    Python calculates the facts.
    Gemini only explains them.
    """

    insight_data = financial_service.build_insight_data(
        expenses
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        You are a helpful financial assistant.

        Use ONLY these pre-computed financial facts:

        {insight_data}

        User question:
        {question}

        Rules:
        - Do not invent numbers.
        - Do not recalculate the numbers.
        - Do not make unsupported claims.
        - Explain the provided financial patterns clearly.
        - Keep the answer concise.
        """
    )

    return response.text