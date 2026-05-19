import tkinter as tk
from tkinter import messagebox
import pyodbc, os, hashlib
from datetime import datetime

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def open_register_window():
    reg = tk.Toplevel()
    reg.title("Create Account")
    reg.geometry("300x300")

    tk.Label(reg, text="Username").pack()
    username_entry = tk.Entry(reg)
    username_entry.pack()

    tk.Label(reg, text="Email").pack()
    email_entry = tk.Entry(reg)
    email_entry.pack()

    tk.Label(reg, text="Password").pack()
    password_entry = tk.Entry(reg, show="*")
    password_entry.pack()

    def create_account():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        hashed = hash_password(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM Users WHERE Username=?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already taken.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO Users (Username, Email, Password, CreatedAt)
                VALUES (?, ?, ?, ?)
            """, (username, email, hashed, datetime.now().date()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account created successfully!")
            reg.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(reg, text="Create Account", command=create_account).pack(pady=15)
