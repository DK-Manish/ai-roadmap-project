from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    id: int
    category: str
    amount: float

expenses = []

# Create an expense
@app.post("/expenses")
def add_expense(expense: Expense):
    expenses.append(expense)
    return expense

# Get all expenses
@app.get("/expenses")
def get_all_expenses():
    return expenses

# Find the highest expense
@app.get('/expenses/highest')
def get_highest_expense():
    if not expenses:  # similar to if len(expenses) == 0
        return {"error": "No expenses found"}
    
    highest = max(expenses, key=lambda expense: expense.amount)
    return highest

# Filter by Category
@app.get("/expenses/category/{category}")
def get_expenses_by_category(category: str):
    result = []

    for expense in expenses:
        if expense.category == category:
            result.append(expense)

    return result

# Display sum by category
@app.get("/expenses/summary")
def get_expense_summary():
    summary = {}

    for expense in expenses:
        if expense.category in summary:
            summary[expense.category] += expense.amount
        else:
            summary[expense.category] = expense.amount

    return summary