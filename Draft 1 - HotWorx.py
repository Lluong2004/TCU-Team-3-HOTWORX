import tkinter as tk
from tkinter import messagebox
import re
import sqlite3

# -------------------------------
# Database Setup
# -------------------------------
conn = sqlite3.connect('hotworx_users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()

# -------------------------------
# Validation Functions
# -------------------------------
def is_valid_name(name):
    return name.isalpha()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(pw):
    return len(pw) >= 6 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)

# -------------------------------
# Register Logic
# -------------------------------
def register():
    first = first_name.get().strip()
    last = last_name.get().strip()
    email_val = email.get().strip()
    pw = password.get()

    if not is_valid_name(first):
        messagebox.showerror("Error", "First name must contain only letters.")
        return
    if not is_valid_name(last):
        messagebox.showerror("Error", "Last name must contain only letters.")
        return
    if not is_valid_email(email_val):
        messagebox.showerror("Error", "Enter a valid email address.")
        return
    if not is_valid_password(pw):
        messagebox.showerror("Error", "Password must be 6+ characters, include 1 uppercase and 1 number.")
        return

    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first, last, email_val, pw))
        conn.commit()
        messagebox.showinfo("Success", f"Account created for {first} {last}!")
        first_name.delete(0, tk.END)
        last_name.delete(0, tk.END)
        email.delete(0, tk.END)
        password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This email is already registered.")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("HOTWORX Member Registration")
root.geometry("400x420")
root.configure(bg="#f5f5f5")

tk.Label(root, text="Register for HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

tk.Label(root, text="First Name", bg="#f5f5f5").pack()
first_name = tk.Entry(root, width=30)
first_name.pack(pady=5)

tk.Label(root, text="Last Name", bg="#f5f5f5").pack()
last_name = tk.Entry(root, width=30)
last_name.pack(pady=5)

tk.Label(root, text="Email", bg="#f5f5f5").pack()
email = tk.Entry(root, width=30)
email.pack(pady=5)

tk.Label(root, text="Password", bg="#f5f5f5").pack()
password = tk.Entry(root, width=30, show="*")
password.pack(pady=5)

tk.Button(root, text="Register", command=register, bg="#ff7f50", fg="white", width=20).pack(pady=20)

root.mainloop()

# Don't forget to close DB connection when app ends
conn.close()
