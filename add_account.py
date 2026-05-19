import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import os
from datetime import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_add_account(username):
    window = tk.Toplevel()
    window.title("Add Account")
    window.geometry("350x300")

    # Get UserID from username
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE Username=?", (username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found.")
            window.destroy()
            return
        user_id = user[0]
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        window.destroy()
        return

    # Account Type Dropdown
    tk.Label(window, text="Account Type").pack()
    account_type_var = tk.StringVar()
    account_type_dropdown = ttk.Combobox(window, textvariable=account_type_var, state="readonly")
    account_type_dropdown['values'] = ["Checking", "Savings", "Credit", "Investment"]
    account_type_dropdown.pack()

    tk.Label(window, text="Bank Name").pack()
    bank_name_entry = tk.Entry(window)
    bank_name_entry.pack()

    tk.Label(window, text="Starting Balance").pack()
    balance_entry = tk.Entry(window)
    balance_entry.pack()

    def submit():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Accounts (UserID, AccountType, BankName, Balance, CreatedAt)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                account_type_var.get(),
                bank_name_entry.get(),
                float(balance_entry.get()),
                datetime.now().date()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account added.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit).pack(pady=10)
