import tkinter as tk
from tkinter import messagebox
import pyodbc
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_manage_data(username):
    window = tk.Toplevel()
    window.title("Manage My Data")
    window.geometry("400x300")

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

        cursor.execute("SELECT COUNT(*) FROM Transactions WHERE UserID=?", (user_id,))
        tx_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Goals WHERE UserID=?", (user_id,))
        goal_count = cursor.fetchone()[0]

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        window.destroy()
        return

    tk.Label(window, text=f"Data for: {username}", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(window, text=f"Transactions: {tx_count}").pack()
    tk.Label(window, text=f"Goals: {goal_count}").pack()

    def confirm_clear():
        if messagebox.askyesno("Warning", "Are you sure you want to delete your transactions and goals?"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Transactions WHERE UserID=?", (user_id,))
                cursor.execute("DELETE FROM Goals WHERE UserID=?", (user_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Done", "Your data has been deleted.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Button(window, text="🗑 Delete My Data", fg="red", command=confirm_clear).pack(pady=20)
