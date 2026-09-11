from services.ai_service import parse_expense


result = parse_expense(
    "I spent ₹500 on dinner with my friends."
)

print("Amount:", result.amount)
print("Description:", result.description)
print("Category:", result.category)