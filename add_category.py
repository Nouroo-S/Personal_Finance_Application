import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "PersonalFinance.accdb")
    return pyodbc.connect(rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};')

def open_add_category(username=None):
    window = tk.Toplevel()
    window.title("Add Category")
    window.geometry("350x250")

    tk.Label(window, text="Category Name").pack()
    category_name_entry = tk.Entry(window)
    category_name_entry.pack()

    tk.Label(window, text="Category Type").pack()
    category_type_var = tk.StringVar()
    category_type_dropdown = ttk.Combobox(window, textvariable=category_type_var, state="readonly")
    category_type_dropdown['values'] = ["Income", "Expense"]
    category_type_dropdown.pack()

    tk.Label(window, text="Description (optional)").pack()
    description_entry = tk.Entry(window)
    description_entry.pack()

    def submit():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Categories (CategoryName, CategoryType, Description)
                VALUES (?, ?, ?)
            """, (
                category_name_entry.get(),
                category_type_var.get(),
                description_entry.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Category added.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Submit", command=submit).pack(pady=10)
