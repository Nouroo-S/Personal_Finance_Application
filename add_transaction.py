import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import os
from datetime import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_add_transaction(username):
    window = tk.Toplevel()
    window.title("Add Transaction")
    window.geometry("400x450")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get UserID based on username
        cursor.execute("SELECT UserID FROM Users WHERE Username=?", (username,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            window.destroy()
            return
        user_id = result[0]

        # Fetch accounts for this user
        cursor.execute("SELECT AccountID, BankName FROM Accounts WHERE UserID=?", (user_id,))
        accounts = cursor.fetchall()

        # Fetch all categories
        cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
        categories = cursor.fetchall()

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        window.destroy()
        return

    # If no accounts or categories exist, show message and disable form
    if not accounts or not categories:
        msg = "You must first create:\n"
        if not accounts: msg += "- At least one Account\n"
        if not categories: msg += "- At least one Category"
        tk.Label(window, text=msg, fg="red", font=("Arial", 12)).pack(pady=30)
        return

    # Dropdown for Account
    tk.Label(window, text="Select Account").pack()
    account_var = tk.StringVar()
    account_dropdown = ttk.Combobox(window, textvariable=account_var, state="readonly")
    account_dropdown['values'] = [f"{a[0]} - {a[1]}" for a in accounts]
    account_dropdown.pack()

    # Dropdown for Category
    tk.Label(window, text="Select Category").pack()
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(window, textvariable=category_var, state="readonly")
    category_dropdown['values'] = [f"{c[0]} - {c[1]}" for c in categories]
    category_dropdown.pack()

    # Transaction type
    tk.Label(window, text="Transaction Type").pack()
    transaction_type_var = tk.StringVar()
    ttk.Combobox(window, textvariable=transaction_type_var, values=["Income", "Expense"], state="readonly").pack()

    # Amount
    tk.Label(window, text="Amount").pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    # Date
    tk.Label(window, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    date_entry.pack()

    def submit():
        try:
            account_id = int(account_var.get().split(" - ")[0])
            category_id = int(category_var.get().split(" - ")[0])
            transaction_type = transaction_type_var.get()
            amount = float(amount_entry.get())
            date = date_entry.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Transactions (UserID, AccountID, CategoryID, TransactionType, Amount, [TransactionDate])
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, account_id, category_id, transaction_type, amount, date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Transaction added successfully.")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit).pack(pady=15)
