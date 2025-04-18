"""
HOTWORX Confirmation Screen
This module displays a class-based confirmation screen for a successful booking.
Includes:
- Branded logo and help center icon
- Loop for displaying booking info lines
- Buttons to view bookings or exit
"""

import tkinter as tk
from my_bookings import show_bookings_screen
from PIL import Image, ImageTk
from help_center import open_help_center

class ConfirmationScreen:
    def __init__(self, workout, date, time, sauna, user_email):
        self.user_email = user_email  # ✅ store it
        self.workout = workout
        self.date = date
        self.time = time
        self.sauna = sauna

        self.window = tk.Tk()
        self.window.title("Booking Confirmed")
        self.window.geometry("400x320")
        self.window.configure(bg="#f5f5f5")

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        # Logo
        logo_raw = Image.open("hotworx_logo.png").resize((130, 45))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.window)
        tk.Label(self.window, image=self.logo, bg="#f5f5f5").pack(pady=(10, 5))

        # Help button in top-right
        help_raw = Image.open("helpcenter_icon.png").resize((20, 20))
        self.help_icon = ImageTk.PhotoImage(help_raw, master=self.window)
        tk.Button(self.window, image=self.help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).place(x=360, y=10)

        # Confirmation Message
        tk.Label(self.window, text="\u2705 Booking Confirmed!", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#4caf50").pack(pady=20)

        # Loop through booking details and display them
        info_lines = [
            f"Workout: {self.workout}",
            f"Date: {self.date}",
            f"Time: {self.time}",
            f"Sauna #: {self.sauna}"
        ]
        for line in info_lines:
            tk.Label(self.window, text=line, bg="#f5f5f5").pack(pady=3)

        # Buttons
        btn_frame = tk.Frame(self.window, bg="#f5f5f5")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="View My Bookings", command=lambda: show_bookings_screen(self.user_email), bg="#2196f3", fg="white", width=16)
        tk.Button(btn_frame, text="Finish", command=self.window.destroy, bg="#ff7f50", fg="white", width=12).grid(row=0, column=1, padx=10)


def show_confirmation_screen(workout, date, time, sauna, user_email):
    ConfirmationScreen(workout, date, time, sauna, user_email)

# Example for manual testing
# show_confirmation_screen("Hot Cycle", "2025-04-22", "07:00 AM", 2)