import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import os
from datetime import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_set_budget(username):
    window = tk.Toplevel()
    window.title("Set Budget")
    window.geometry("400x350")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get UserID
        cursor.execute("SELECT UserID FROM Users WHERE Username=?", (username,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            window.destroy()
            return
        user_id = result[0]

        
        cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
        categories = cursor.fetchall()

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        window.destroy()
        return

    if not categories:
        tk.Label(window, text="No categories available. Please add one first.", fg="red").pack(pady=30)
        return

    # Dropdown for Category
    tk.Label(window, text="Select Category").pack()
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(window, textvariable=category_var, state="readonly")
    category_dropdown['values'] = [f"{c[0]} - {c[1]}" for c in categories]
    category_dropdown.pack()

    tk.Label(window, text="Amount Allocated").pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    tk.Label(window, text="Start Date (YYYY-MM-DD)").pack()
    start_entry = tk.Entry(window)
    start_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    start_entry.pack()

    tk.Label(window, text="End Date (YYYY-MM-DD)").pack()
    end_entry = tk.Entry(window)
    end_entry.pack()

    def submit():
        try:
            category_id = int(category_var.get().split(" - ")[0])
            amount = float(amount_entry.get())
            start_date = start_entry.get()
            end_date = end_entry.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Budgets (UserID, CategoryID, AmountAllocated, StartDate, EndDate)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, category_id, amount, start_date, end_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Budget set successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit).pack(pady=15)
