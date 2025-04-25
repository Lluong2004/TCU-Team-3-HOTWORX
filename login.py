"""
HOTWORX Login Script
This script provides a basic login interface that connects to the SQLite database to validate users.
Note: This file may be used for isolated testing or legacy purposes.
"""

import tkinter as tk  # GUI toolkit for creating window and form elements
from tkinter import messagebox  # To display popup messages
import sqlite3  # Library to interact with SQLite databases
from PIL import Image, ImageTk  # For image loading and display
from help_center import open_help_center  # External module to open the Help Center window

# -------------------------------
# Database Connection
# -------------------------------
conn = sqlite3.connect('hotworx_users.db')  # Connect to (or create) SQLite database
cursor = conn.cursor()  # Create a cursor object to interact with the database

# -------------------------------
# Login Function
# -------------------------------
def login():
    """
    Checks the entered email and password against the users table in the database.
    Displays a welcome message if correct, error message otherwise.
    """
    email_val = email.get().strip()  # Get and clean user input for email
    pw = password.get()  # Get password input (no trimming needed)

    # Check if email and password match an entry in the users table
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email_val, pw))
    result = cursor.fetchone()  # Fetch the first result

    if result:
        full_name = f"{result[1]} {result[2]}"  # Combine first and last name
        messagebox.showinfo("Login Successful", f"Welcome back, {full_name}!")  # Show success message
        # Note: Redirect to dashboard can be added here
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")  # Show error popup

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()  # Create the root application window
root.title("HOTWORX Member Login")  # Set window title
root.geometry("400x300")  # Set window dimensions
root.configure(bg="#f5f5f5")  # Set background color

# Load and display Help Center icon in the corner
help_img_raw = Image.open("helpcenter_icon.png").resize((20, 20))
help_icon = ImageTk.PhotoImage(help_img_raw, master=root)
tk.Button(root, image=help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).place(x=360, y=10)
root.help_icon = help_icon  # Retain reference to image to prevent garbage collection

# Display main login label
tk.Label(root, text="Login to HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

# Email label and entry field
tk.Label(root, text="Email", bg="#f5f5f5").pack()
email = tk.Entry(root, width=30)
email.pack(pady=5)

# Password label and entry field (masked)
tk.Label(root, text="Password", bg="#f5f5f5").pack()
password = tk.Entry(root, width=30, show="*")
password.pack(pady=5)

# Login button that triggers the login function
tk.Button(root, text="Login", command=login, bg="#4caf50", fg="white", width=20).pack(pady=20)

# Start the GUI event loop
root.mainloop()

# Close the database connection once the window is closed
conn.close()
