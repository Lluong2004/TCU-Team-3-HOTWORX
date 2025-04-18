import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from help_center import open_help_center

# -------------------------------
# Database Connection
# -------------------------------
conn = sqlite3.connect('hotworx_users.db')
cursor = conn.cursor()

# -------------------------------
# Login Function
# -------------------------------
def login():
    email_val = email.get().strip()
    pw = password.get()

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email_val, pw))
    result = cursor.fetchone()

    if result:
        full_name = f"{result[1]} {result[2]}"
        messagebox.showinfo("Login Successful", f"Welcome back, {full_name}!")
        # Simulate redirection (you could destroy this window and open the dashboard)
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("HOTWORX Member Login")
root.geometry("400x300")
root.configure(bg="#f5f5f5")

help_img_raw = Image.open("helpcenter_icon.png").resize((20, 20))
help_icon = ImageTk.PhotoImage(help_img_raw, master=root)
tk.Button(root, image=help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).place(x=360, y=10)
root.help_icon = help_icon

tk.Label(root, text="Login to HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

tk.Label(root, text="Email", bg="#f5f5f5").pack()
email = tk.Entry(root, width=30)
email.pack(pady=5)

tk.Label(root, text="Password", bg="#f5f5f5").pack()
password = tk.Entry(root, width=30, show="*")
password.pack(pady=5)

tk.Button(root, text="Login", command=login, bg="#4caf50", fg="white", width=20).pack(pady=20)

root.mainloop()

conn.close()
