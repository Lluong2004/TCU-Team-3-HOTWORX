"""
HOTWORX Authentication App
This module provides a GUI for user registration and login, integrated with a local database.
It also includes help center support and dashboard redirection upon successful login.
"""

import tkinter as tk  # GUI toolkit
from tkinter import messagebox  # To show popup messages
import re  # For validating email and password
from db import register_user, login_user  # DB functions for user auth
from dashboard import open_dashboard  # Opens the dashboard on successful login
from PIL import Image, ImageTk  # To display and resize images
from help_center import open_help_center  # Opens the help center window

class HotworxApp:  # Defines the GUI app class
    def __init__(self, master):
        """
        Initialize the application window and all frames.
        """
        self.master = master
        self.master.title("HOTWORX Member Portal")
        self.master.geometry("420x460")
        self.master.configure(bg="#f5f5f5")

        # Load and display the HOTWORX logo
        logo_raw = Image.open("hotworx_logo.png").resize((150, 60))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.master)
        tk.Label(master, image=self.logo, bg="#f5f5f5").pack(pady=(10, 0))

        # Load the help center icon
        help_img_raw = Image.open("helpcenter_icon.png").resize((20, 20))
        self.help_icon = ImageTk.PhotoImage(help_img_raw, master=self.master)

        # Set up login and registration frames
        self.login_frame = tk.Frame(master, bg="#f5f5f5")
        self.register_frame = tk.Frame(master, bg="#f5f5f5")

        self.create_login_frame()
        self.create_register_frame()

        # Show login frame first
        self.login_frame.pack()

    def create_login_frame(self):
        """
        Create the login interface.
        """
        tk.Label(self.login_frame, text="Login", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        # Create entry fields for login
        self.email_login = tk.Entry(self.login_frame, width=30)
        self.password_login = tk.Entry(self.login_frame, width=30, show="*")

        # Labels and entry widgets
        for label_text, entry in [("Email", self.email_login), ("Password", self.password_login)]:
            tk.Label(self.login_frame, text=label_text, bg="#f5f5f5").pack()
            entry.pack(pady=5)

        # Login button
        tk.Button(self.login_frame, text="Login", command=self.login, bg="#4caf50", fg="white", width=20).pack(pady=10)

        # Switch to registration
        tk.Button(self.login_frame, text="New user? Register", command=self.show_register, bg="#dddddd", width=20).pack()

        # Help icon
        tk.Button(self.login_frame, image=self.help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).pack(pady=5)

    def create_register_frame(self):
        """
        Create the registration interface.
        """
        tk.Label(self.register_frame, text="Register for HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        # Create entry fields for registration
        self.first_name = tk.Entry(self.register_frame, width=30)
        self.last_name = tk.Entry(self.register_frame, width=30)
        self.email_reg = tk.Entry(self.register_frame, width=30)
        self.password_reg = tk.Entry(self.register_frame, width=30, show="*")

        # Labels and entry widgets
        labels_entries = [
            ("First Name", self.first_name),
            ("Last Name", self.last_name),
            ("Email", self.email_reg),
            ("Password", self.password_reg)
        ]

        for label_text, entry in labels_entries:
            tk.Label(self.register_frame, text=label_text, bg="#f5f5f5").pack()
            entry.pack(pady=5)

        # Register button
        tk.Button(self.register_frame, text="Register", command=self.register, bg="#ff7f50", fg="white", width=20).pack(pady=10)

        # Switch to login
        tk.Button(self.register_frame, text="Already a member? Login", command=self.show_login, bg="#dddddd", width=20).pack()

    def show_login(self):
        """
        Switch to the login frame.
        """
        self.register_frame.pack_forget()
        self.login_frame.pack()

    def show_register(self):
        """
        Switch to the registration frame.
        """
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def register(self):
        """
        Handle user registration logic with validation.
        """
        first = self.first_name.get().strip()
        last = self.last_name.get().strip()
        email_val = self.email_reg.get().strip()
        pw = self.password_reg.get()

        # Validate names
        if not first.isalpha() or not last.isalpha():
            messagebox.showerror("Error", "Names must contain only letters.")
            return

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_val):
            messagebox.showerror("Error", "Enter a valid email.")
            return

        # Validate password strength
        if len(pw) < 6 or not any(c.isupper() for c in pw) or not any(c.isdigit() for c in pw):
            messagebox.showerror("Error", "Password must be 6+ characters, include 1 uppercase & 1 number.")
            return

        # Try to register user
        success, msg = register_user(first, last, email_val, pw)
        if success:
            messagebox.showinfo("Success", msg)
            # Clear fields after success
            for entry in [self.first_name, self.last_name, self.email_reg, self.password_reg]:
                entry.delete(0, tk.END)
            self.show_login()
        else:
            messagebox.showerror("Error", msg)

    def login(self):
        """
        Handle user login logic.
        """
        email_val = self.email_login.get().strip()
        pw = self.password_login.get()

        # Check credentials
        success, result = login_user(email_val, pw)
        if success:
            self.master.destroy()  # Close login window
            open_dashboard(result, email_val)  # Open dashboard with user info
        else:
            messagebox.showerror("Login Failed", result)

# -------------------------------
# Run the application
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HotworxApp(root)
    root.mainloop()
