"""
HOTWORX Time Slot Selection Screen
This module presents available time slots per sauna for a selected workout and date.
Includes:
- Logo branding
- Color-coded sauna availability
- Booking conflict checks
- Dynamic button generation
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import book_session
from confirmation import show_confirmation_screen
from PIL import Image, ImageTk

status_colors = {
    "available": "#4caf50",  # green (2-3 left)
    "warning": "#ffc107",    # yellow (1 left)
    "blocked": "#9e9e9e"      # gray (0 left)
}

# Fixed time slots and sauna mapping
fixed_slots = [
    {"time": "06:00 AM – 06:30 AM", "sauna": 1},
    {"time": "07:00 AM – 07:30 AM", "sauna": 2},
    {"time": "08:00 AM – 08:30 AM", "sauna": 3},
    {"time": "09:00 AM – 09:30 AM", "sauna": 4},
    {"time": "10:00 AM – 10:30 AM", "sauna": 5},
]

class TimeSlotScreen:
    def __init__(self, workout_name, selected_date, user_email, user_full_name):
        self.workout_name = workout_name
        self.selected_date = selected_date
        self.user_email = user_email
        self.user_full_name = user_full_name
        self.conn = sqlite3.connect('hotworx_users.db')
        self.cursor = self.conn.cursor()

        self.win = tk.Tk()
        self.win.title("Select a Time Slot")
        self.win.geometry("500x450")
        self.win.configure(bg="#f5f5f5")

        self.setup_ui()
        self.win.mainloop()

    def setup_ui(self):
        # Logo
        logo_raw = Image.open("hotworx_logo.png").resize((130, 45))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.win)
        tk.Label(self.win, image=self.logo, bg="#f5f5f5").pack(pady=(10, 5))

        # Header
        tk.Label(self.win, text=f"Workout: {self.workout_name}", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self.win, text=f"Date: {self.selected_date}", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)
        tk.Label(self.win, text="Select your time slot:", bg="#f5f5f5").pack(pady=10)

        frame = tk.Frame(self.win, bg="#f5f5f5")
        frame.pack(pady=5)

        for slot in fixed_slots:
            count = self.get_booking_count(slot)
            remaining = 3 - count

            if remaining >= 2:
                status = "available"
            elif remaining == 1:
                status = "warning"
            else:
                status = "blocked"
    

            label = f"{slot['time']} — Sauna #{slot['sauna']} ({remaining} left)"
            tk.Button(frame, text=label,
                      bg=status_colors[status], fg="white", width=40,
                      command=lambda s=slot: self.reserve_slot(s),
                      state=tk.NORMAL if remaining > 0 else tk.DISABLED
                      ).pack(pady=5)
        tk.Button(self.win, text="Cancel", command=self.win.destroy, bg="#ddd", width=15).pack(pady=10)

    def get_booking_count(self, slot):
        self.cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE date = ? AND sauna_number = ? AND time_slot = ?",
            (self.selected_date, slot["sauna"], slot["time"])
        )
        return self.cursor.fetchone()[0]

    def reserve_slot(self, slot):
        # Prevent duplicate booking at same time by this user
        self.cursor.execute(
            "SELECT * FROM bookings WHERE date = ? AND time_slot = ? AND user_email = ?",
            (self.selected_date, slot["time"], self.user_email)
        )
        if self.cursor.fetchone():
            messagebox.showerror("Booking Conflict", "You already have a session booked at this time.")
            return

        if self.get_booking_count(slot) >= 3:
            messagebox.showerror("Limit Reached", f"Sauna #{slot['sauna']} is fully booked for this time.")
            return

        # Book it
        book_session(self.workout_name, self.selected_date, slot["time"], slot["sauna"], self.user_email)
        self.win.destroy()
        show_confirmation_screen(self.workout_name, self.selected_date, slot["time"], slot["sauna"], self.user_full_name, self.user_email)


def open_time_slot_screen(workout_name, selected_date, user_email, user_full_name):
    TimeSlotScreen(workout_name, selected_date, user_email, user_full_name)

# For testing only
# open_time_slot_screen("Hot Core", "2025-04-20", "test@example.com")

