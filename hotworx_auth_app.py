"""
HOTWORX Authentication App
This module provides a GUI for user registration and login, integrated with a local database.
It also includes help center support and dashboard redirection upon successful login.
"""

import tkinter as tk
from tkinter import messagebox
import re
from db import register_user, login_user
from dashboard import open_dashboard
from PIL import Image, ImageTk
from help_center import open_help_center


class HotworxApp:
    def __init__(self, master):
        """
        Initialize the application window and all frames.
        """
        self.master = master
        self.master.title("HOTWORX Member Portal")
        self.master.geometry("420x460")
        self.master.configure(bg="#f5f5f5")

        # Load logo
        logo_raw = Image.open("hotworx_logo.png").resize((150, 60))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.master)
        tk.Label(master, image=self.logo, bg="#f5f5f5").pack(pady=(10, 0))

        # Load help icon
        help_img_raw = Image.open("helpcenter_icon.png").resize((20, 20))
        self.help_icon = ImageTk.PhotoImage(help_img_raw, master=self.master)

        # Initialize frames
        self.login_frame = tk.Frame(master, bg="#f5f5f5")
        self.register_frame = tk.Frame(master, bg="#f5f5f5")

        self.create_login_frame()
        self.create_register_frame()

        self.login_frame.pack()

    def create_login_frame(self):
        """
        Create the login interface.
        """
        tk.Label(self.login_frame, text="Login", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        self.email_login = tk.Entry(self.login_frame, width=30)
        self.password_login = tk.Entry(self.login_frame, width=30, show="*")

        for label_text, entry in [("Email", self.email_login), ("Password", self.password_login)]:
            tk.Label(self.login_frame, text=label_text, bg="#f5f5f5").pack()
            entry.pack(pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, bg="#4caf50", fg="white", width=20).pack(pady=10)
        tk.Button(self.login_frame, text="New user? Register", command=self.show_register, bg="#dddddd", width=20).pack()
        tk.Button(self.login_frame, image=self.help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).pack(pady=5)

    def create_register_frame(self):
        """
        Create the registration interface.
        """
        tk.Label(self.register_frame, text="Register for HOTWORX", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

        self.first_name = tk.Entry(self.register_frame, width=30)
        self.last_name = tk.Entry(self.register_frame, width=30)
        self.email_reg = tk.Entry(self.register_frame, width=30)
        self.password_reg = tk.Entry(self.register_frame, width=30, show="*")

        labels_entries = [("First Name", self.first_name),
                          ("Last Name", self.last_name),
                          ("Email", self.email_reg),
                          ("Password", self.password_reg)]

        for label_text, entry in labels_entries:
            tk.Label(self.register_frame, text=label_text, bg="#f5f5f5").pack()
            entry.pack(pady=5)

        tk.Button(self.register_frame, text="Register", command=self.register, bg="#ff7f50", fg="white", width=20).pack(pady=10)
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

        if not first.isalpha() or not last.isalpha():
            messagebox.showerror("Error", "Names must contain only letters.")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_val):
            messagebox.showerror("Error", "Enter a valid email.")
            return
        if len(pw) < 6 or not any(c.isupper() for c in pw) or not any(c.isdigit() for c in pw):
            messagebox.showerror("Error", "Password must be 6+ characters, include 1 uppercase & 1 number.")
            return

        success, msg = register_user(first, last, email_val, pw)
        if success:
            messagebox.showinfo("Success", msg)
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

        success, result = login_user(email_val, pw)
        if success:
            self.master.destroy()
            open_dashboard(result, email_val)  # Pass full name + email
        else:
            messagebox.showerror("Login Failed", result)


# -------------------------------
# Run the application
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HotworxApp(root)
    root.mainloop()