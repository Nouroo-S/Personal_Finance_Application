import tkinter as tk
from tkinter import messagebox

from add_transaction import open_add_transaction
from add_account import open_add_account
from add_category import open_add_category
from set_budget import open_set_budget
from report import open_report
from goal import open_goal
from notification import open_notification
from manage_data import open_manage_data

def open_dashboard(username):
    dashboard = tk.Tk()
    dashboard.title("Personal Finance Management App")
    dashboard.geometry("600x700")
    dashboard.configure(bg="#2f70a0")

    tk.Label(
        dashboard,
        text=f"Welcome to Your Personal Finance Manager, {username}!",
        font=("Arial", 16),
        bg="#2f70a0",
        fg="white"
    ).pack(pady=15)

    def create_section(title, button_text, command):
        section = tk.Frame(dashboard, bg="lightgray", padx=10, pady=10)
        section.pack(fill="x", padx=20, pady=5)

        tk.Label(section, text=title, font=("Arial", 12), anchor="w", bg="lightgray").pack(fill="x")
        tk.Button(section, text=button_text, width=25, command=lambda: command(username)).pack(pady=5)

    # Real Features
    create_section("Transaction Management", "Add Transaction", open_add_transaction)
    create_section("Account Setup", "Add Account", open_add_account)
    create_section("Category Setup", "Add Category", open_add_category)
    create_section("Budget Management", "Set Budget", open_set_budget)
    create_section("Report Summary", "Generate Report", open_report)
    create_section("Goal Setting", "Create Financial Goal", open_goal)
    create_section("Notification Center", "Send Notification", open_notification)
    create_section("Data Management", "Manage Data", open_manage_data)

    dashboard.mainloop()
