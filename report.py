import tkinter as tk
from tkinter import messagebox
import pyodbc
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_report(username):
    window = tk.Toplevel()
    window.title("Report Summary")
    window.geometry("550x600")
    window.configure(bg="#f5f5f5")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT UserID FROM Users WHERE Username=?", (username,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            window.destroy()
            return
        user_id = result[0]

        # Income & Expenses
        cursor.execute("SELECT SUM(Amount) FROM Transactions WHERE UserID=? AND TransactionType='Income'", (user_id,))
        income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(Amount) FROM Transactions WHERE UserID=? AND TransactionType='Expense'", (user_id,))
        expense = cursor.fetchone()[0] or 0

        # Spending by Category
        cursor.execute("""
            SELECT Categories.CategoryName, SUM(Transactions.Amount)
            FROM Transactions, Categories
            WHERE Transactions.CategoryID = Categories.CategoryID
            AND Transactions.UserID=? AND Transactions.TransactionType='Expense'
            GROUP BY Categories.CategoryName
        """, (user_id,))
        category_spending = cursor.fetchall()

        # Financial Goals
        cursor.execute("""
            SELECT GoalName, TargetAmount, CurrentAmount, DueDate
            FROM Goals
            WHERE UserID=?
        """, (user_id,))
        goals = cursor.fetchall()

        # Budgets
        cursor.execute("""
            SELECT Categories.CategoryName, AmountAllocated, StartDate, EndDate
            FROM Budgets, Categories
            WHERE Budgets.CategoryID = Categories.CategoryID AND Budgets.UserID=?
        """, (user_id,))
        budgets = cursor.fetchall()

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        window.destroy()
        return

    # Display Main Report
    tk.Label(window, text=f"User: {username}", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)
    tk.Label(window, text=f"Total Income: ${income:.2f}", fg="green", font=("Arial", 12), bg="#f5f5f5").pack()
    tk.Label(window, text=f"Total Expenses: ${expense:.2f}", fg="red", font=("Arial", 12), bg="#f5f5f5").pack(pady=(0, 10))

    # Spending by Category
    tk.Label(window, text="Spending by Category:", font=("Arial", 11, "bold"), bg="#f5f5f5").pack()
    if category_spending:
        for name, amt in category_spending:
            tk.Label(window, text=f"• {name}: ${amt:.2f}", anchor="w", bg="#f5f5f5").pack(fill="x", padx=20)
    else:
        tk.Label(window, text="(No expenses yet)", fg="gray", bg="#f5f5f5").pack()

    # Goals
    tk.Label(window, text="\nFinancial Goals:", font=("Arial", 11, "bold"), bg="#f5f5f5").pack()
    if goals:
        for name, target, current, due in goals:
            tk.Label(window, text=f"• {name} → ${current:.2f} / ${target:.2f} due {due}", anchor="w", bg="#f5f5f5").pack(fill="x", padx=20)
    else:
        tk.Label(window, text="(No goals yet)", fg="gray", bg="#f5f5f5").pack()

    # Budgets
    tk.Label(window, text="\nActive Budgets:", font=("Arial", 11, "bold"), bg="#f5f5f5").pack()
    if budgets:
        for cat, amt, start, end in budgets:
            tk.Label(window, text=f"• {cat}: ${amt:.2f} from {start} to {end}", anchor="w", bg="#f5f5f5").pack(fill="x", padx=20)
    else:
        tk.Label(window, text="(No budgets set)", fg="gray", bg="#f5f5f5").pack()
