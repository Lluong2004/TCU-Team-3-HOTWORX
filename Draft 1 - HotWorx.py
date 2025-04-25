"""
HOTWORX
"""
import tkinter as tk  # GUI library for building interface
from tkinter import messagebox  # Module for displaying popup messages
import re  # Module for regular expressions (used in validation)
import sqlite3  # Module to interact with SQLite database

# -------------------------------
# Database Setup
# -------------------------------

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('hotworx_users.db')
cursor = conn.cursor()

# Create the 'users' table if it doesn't already exist
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

# Check if the name only contains letters
def is_valid_name(name):
    return name.isalpha()

# Validate the email format using a regular expression
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Check password for minimum 6 characters, 1 uppercase, and 1 digit
def is_valid_password(pw):
    return len(pw) >= 6 and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)

# -------------------------------
# Register Logic
# -------------------------------

# Function called when "Register" button is clicked
def register():
    # Get input values from entry fields
    first = first_name.get().strip()
    last = last_name.get().strip()
    email_val = email.get().strip()
    pw = password.get()

    # Input validation checks
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
        # Try to insert new user into the database
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first, last, email_val, pw))
        conn.commit()

        # Success message and clear input fields
        messagebox.showinfo("Success", f"Account created for {first} {last}!")
        first_name.delete(0, tk.END)
        last_name.delete(0, tk.END)
        email.delete(0, tk.END)
        password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        # If email already exists (unique constraint), show error
        messagebox.showerror("Error", "This email is already registered.")

# -------------------------------
# GUI Setup
# -------------------------------

# Create the main application window
root = tk.Tk()
root.title("HOTWORX Member Registration")
root.geometry("400x420")
root.configure(bg="#f5f5f5")

# UI title
tk.Label(root, text="Register for HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

# Input fields and labels
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

# Register button
tk.Button(root, text="Register", command=register, bg="#ff7f50", fg="white", width=20).pack(pady=20)

# Start the application loop
root.mainloop()

# -------------------------------
# Cleanup
# -------------------------------

# Close the database connection when the app is closed
conn.close()
