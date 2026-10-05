import os
from datetime import datetime

from pymongo import MongoClient
from models.expense import Expense
from bson import ObjectId


class ExpenseService:
    # Handles expense-related business logic

    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
        # Select the database
        self.db = self.client["expense_tracker"]

        # Select the expenses collection
        self.collection = self.db["expenses"]

    def add_expense(self, amount, description, category, user_id):
        # Remove accidental spaces
        description = description.strip()
        category = category.strip()

        # Create a MongoDB document
        expense_data = {
            "amount": amount,
            "description": description,
            "category": category,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }

        # Insert the document into MongoDB
        result = self.collection.insert_one(expense_data)

        # Get the ID MongoDB created
        expense_data["_id"] = result.inserted_id

        # Convert it into an Expense object
        return Expense.from_mongo(expense_data)

    def get_expenses(self, user_id):
        # Get only this user's expenses from MongoDB
        documents = self.collection.find({
            "user_id": user_id
        })

        # Convert MongoDB documents into Expense objects
        expenses = []

        for document in documents:
            expense = Expense.from_mongo(document)
            expenses.append(expense)

        return expenses

    def get_expense(self, expense_id, user_id):
        # Check whether the ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(expense_id):
            return None

        # Convert text ID into MongoDB ObjectId
        expense_id = ObjectId(expense_id)

        # Find the expense belonging to this user
        document = self.collection.find_one({
            "_id": expense_id,
            "user_id": user_id
        })

        if document is None:
            return None

        return Expense.from_mongo(document)

    def get_total(self, user_id):
        # Get only this user's expenses
        documents = self.collection.find({
            "user_id": user_id
        })

        # Calculate total
        total = 0

        for document in documents:
            total += document["amount"]

        return total

    def get_by_category(self, category, user_id):
        # Remove accidental spaces
        category = category.strip()

        # Find only this user's expenses in the category
        documents = self.collection.find({
            "category": category,
            "user_id": user_id
        })

        # Convert documents into Expense objects
        results = []

        for document in documents:
            expense = Expense.from_mongo(document)
            results.append(expense)

        return results

    def update_expense(
        self,
        expense_id,
        amount,
        description,
        category,
        user_id
    ):
        # Check whether the ID is valid
        if not ObjectId.is_valid(expense_id):
            return None

        # Convert text ID into MongoDB ObjectId
        expense_id = ObjectId(expense_id)

        # Update only if the expense belongs to this user
        result = self.collection.update_one(
            {
                "_id": expense_id,
                "user_id": user_id
            },
            {
                "$set": {
                    "amount": amount,
                    "description": description.strip(),
                    "category": category.strip()
                }
            }
        )

        # Check whether the expense exists
        # and belongs to this user
        if result.matched_count == 0:
            return None

        # Get the updated expense
        document = self.collection.find_one({
            "_id": expense_id,
            "user_id": user_id
        })

        return Expense.from_mongo(document)

    def delete_expense(self, expense_id, user_id):
        # Check whether the ID is valid
        if not ObjectId.is_valid(expense_id):
            return False

        # Convert the ID into MongoDB ObjectId
        expense_id = ObjectId(expense_id)

        # Delete only if the expense belongs to this user
        result = self.collection.delete_one({
            "_id": expense_id,
            "user_id": user_id
        })

        # Check whether MongoDB actually deleted a document
        return result.deleted_count > 0

    def get_expenses_by_date_range(
        self,
        user_id,
        start_date,
        end_date
    ):
        # Get this user's expenses within the date range
        documents = self.collection.find({
            "user_id": user_id,
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            }
        })

        # Convert MongoDB documents into Expense objects
        expenses = []

        for document in documents:
            expenses.append(
                Expense.from_mongo(document)
            )

        return expenses