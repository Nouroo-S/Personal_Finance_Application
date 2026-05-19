import os
import pyodbc
import hashlib
import tkinter as tk
from tkinter import messagebox
from dashboard import open_dashboard  # Opens the dashboard after login
from register import open_register_window  # Opens the create account form

# Database connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")
    conn = pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')
    return conn

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Login function connected to Tkinter
def login():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Password FROM Users WHERE Username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and hashed_password == user[1]:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            root.destroy()  # Close the login window
            open_dashboard(username)  # Open the dashboard window
        elif user:
            messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "User not found.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Build Tkinter login window
root = tk.Tk()
root.title("Login - Personal Finance App")
root.geometry("300x250")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Username:", bg="#f0f0f0").pack(pady=(20, 5))
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password:", bg="#f0f0f0").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

# 🔹 Create Account button
tk.Button(root, text="Create Account", command=open_register_window).pack()

root.mainloop()
