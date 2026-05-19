import tkinter as tk
from tkinter import messagebox
import threading
import time

def open_notification(username):
    window = tk.Toplevel()
    window.title("Set Reminder Notification")
    window.geometry("400x300")

    tk.Label(window, text=f"Create a Reminder for {username}", font=("Arial", 12)).pack(pady=10)

    tk.Label(window, text="Title").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()

    tk.Label(window, text="Message").pack()
    message_entry = tk.Entry(window)
    message_entry.pack()

    tk.Label(window, text="Remind me in (minutes)").pack()
    delay_entry = tk.Entry(window)
    delay_entry.insert(0, "1")  # Default to 1 minute
    delay_entry.pack()

    def send_later(title, msg, delay_minutes):
        time.sleep(delay_minutes * 60)
        messagebox.showinfo(f"⏰ Reminder: {title}", msg)

    def schedule_reminder():
        try:
            title = title_entry.get()
            msg = message_entry.get()
            delay = int(delay_entry.get())

            if not title or not msg or delay <= 0:
                raise ValueError

            threading.Thread(target=send_later, args=(title, msg, delay), daemon=True).start()
            messagebox.showinfo("Scheduled", f"Reminder will appear in {delay} minute(s).")
            window.destroy()

        except:
            messagebox.showerror("Input Error", "Please enter a valid title, message, and delay time.")

    tk.Button(window, text="Schedule Notification", command=schedule_reminder).pack(pady=15)
