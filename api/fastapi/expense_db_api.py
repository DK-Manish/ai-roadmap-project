from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


class Expense(BaseModel):
    category: str
    amount: int


# Add expense
@app.post("/expenses")
def add_expense(expense: Expense):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses (category, amount) VALUES (%s, %s) RETURNING id;",
            (expense.category, expense.amount)
        )

        new_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "success": True,
            "id": new_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Get expense 
@app.get("/expenses")
def get_expenses():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses;")
        rows = cursor.fetchall()

        expenses = []
        for row in rows:
            expenses.append({
                "id": row[0],
                "category": row[1],
                "amount": row[2]
            })

        return {
            "success": True,
            "data": expenses
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Get highest expense

@app.get("/expenses/highest")
def get_highest_expense():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM expenses ORDER BY amount DESC LIMIT 1;"
        )
        row = cursor.fetchone()

        if row:
            return {
                "success": True,
                "data": {
                    "id": row[0],
                    "category": row[1],
                    "amount": row[2]
                }
            }

        return {
            "success": False,
            "error": "No expenses found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Get expense category total
@app.get("/expenses/category/{category}")
def get_by_category(category: str):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM expenses WHERE category = %s;",
            (category,)
        )

        rows = cursor.fetchall()

        expenses = [
            {
                "id": r[0],
                "category": r[1],
                "amount": r[2]
            }
            for r in rows
        ]

        return {"success": True, "data": expenses}

    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Get all expenses summary
@app.get("/expenses/summary")
def get_expense_summary():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            GROUP BY category;
        """)

        rows = cursor.fetchall()

        summary = []
        for row in rows:
            summary.append({
                "category": row[0],
                "total_amount": row[1]
            })

        return {
            "success": True,
            "data": summary
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Total expense for one category
@app.get("/expenses/category/{category}/total")
def get_total_by_category(category: str):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE category = %s
            GROUP BY category;
        """, (category,))

        row = cursor.fetchone()

        if row:
            return {
                "success": True,
                "data": {
                    "category": row[0],
                    "total_amount": row[1]
                }
            }

        return {
            "success": False,
            "error": "No expenses found for this category"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Modify Expenses
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE expenses
            SET category = %s, amount = %s
            WHERE id = %s
            RETURNING id;
            """,
            (expense.category, expense.amount, expense_id)
        )

        updated = cursor.fetchone()
        conn.commit()

        if updated:
            return {
                "success": True,
                "message": "Expense updated successfully",
                "id": updated[0]
            }

        return {
            "success": False,
            "error": "Expense not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Delete an expense 
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM expenses WHERE id = %s RETURNING id;",
            (expense_id,)
        )

        deleted = cursor.fetchone()
        conn.commit()

        if deleted:
            return {
                "success": True,
                "message": "Expense deleted successfully",
                "id": deleted[0]
            }

        return {
            "success": False,
            "error": "Expense not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()