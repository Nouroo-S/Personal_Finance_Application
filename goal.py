import tkinter as tk
from tkinter import messagebox
import pyodbc
import os
from datetime import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_goal(username):
    window = tk.Toplevel()
    window.title("Create Financial Goal")
    window.geometry("350x300")

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

    tk.Label(window, text="Goal Name").pack()
    goal_name_entry = tk.Entry(window)
    goal_name_entry.pack()

    tk.Label(window, text="Target Amount").pack()
    target_entry = tk.Entry(window)
    target_entry.pack()

    tk.Label(window, text="Current Amount").pack()
    current_entry = tk.Entry(window)
    current_entry.pack()

    tk.Label(window, text="Due Date (YYYY-MM-DD)").pack()
    due_entry = tk.Entry(window)
    due_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    due_entry.pack()

    def submit():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Goals (UserID, GoalName, TargetAmount, CurrentAmount, DueDate)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                goal_name_entry.get(),
                float(target_entry.get()),
                float(current_entry.get()),
                due_entry.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Goal added.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit).pack(pady=10)
