"""
HOTWORX Dashboard Screen
This class-based module renders the main dashboard after user login. It allows the user to:
- View their name
- Select a workout date from a calendar
- Choose a workout from a list
- Navigate to My Bookings
- Open Help Center
"""

import tkinter as tk 
from tkcalendar import Calendar
from datetime import datetime, timedelta
from timeslot import open_time_slot_screen
from PIL import Image, ImageTk
from help_center import open_help_center
from my_bookings import show_bookings_screen

# Simulated workouts
workouts = [ # List of workouts and descriptions, this will show up in the dashboard
    {"name": "Hot Core", "description": "Core strength in infrared heat."},
    {"name": "Hot Cycle", "description": "Cardio and sweat session."},
    {"name": "Hot Pilates", "description": "Infrared-enhanced pilates."}
]

class Dashboard: #this is the main dashboard class that will be used to show the dashboard after login
    def __init__(self, user_full_name, user_email):
        self.user_full_name = user_full_name
        self.user_email = user_email
        self.window = tk.Tk()
        self.window.title("HOTWORX Dashboard")
        self.window.geometry("600x500")
        self.window.configure(bg="#fff8f0")

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self): #this function sets up the UI for the dashboard
        # Logo
        logo_raw = Image.open("hotworx_logo.png").resize((150, 60))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.window)
        tk.Label(self.window, image=self.logo, bg="#fff8f0").pack(pady=(10, 5))

        # Top buttons (My Bookings + Help)
        cal_raw = Image.open("calendar_icon.png").resize((20, 20))
        self.calendar_icon = ImageTk.PhotoImage(cal_raw, master=self.window)
        tk.Button(self.window, image=self.calendar_icon, command=lambda: show_bookings_screen(self.user_email), bg="#fff8f0", borderwidth=0).place(x=10, y=10)

        help_raw = Image.open("helpcenter_icon.png").resize((20, 20))
        self.help_icon = ImageTk.PhotoImage(help_raw, master=self.window)
        tk.Button(self.window, image=self.help_icon, command=open_help_center, bg="#fff8f0", borderwidth=0).place(x=560, y=10)

        # Greeting
        tk.Label(self.window, text=f"Welcome back, {self.user_full_name}!", font=("Arial", 16, "bold"), bg="#fff8f0").pack(pady=10)

        # Calendar
        today = datetime.today()
        max_date = today + timedelta(days=30)
        tk.Label(self.window, text="Select your workout date:", bg="#fff8f0").pack()
        self.cal = Calendar(self.window, mindate=today, maxdate=max_date, date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)

        # Workout selection
        workout_frame = tk.Frame(self.window, bg="#fff8f0")
        workout_frame.pack(pady=20)

        tk.Label(workout_frame, text="Available Workouts:", font=("Arial", 14), bg="#fff8f0").grid(row=0, column=0, columnspan=2, pady=10)

        for i, workout in enumerate(workouts):
            tk.Label(workout_frame, text=workout["name"], font=("Arial", 12, "bold"), bg="#fff8f0").grid(row=i+1, column=0, sticky="w", padx=10)
            tk.Button(
                workout_frame, text="Select",
                command=lambda w=workout: self.select_workout(w),
                bg="#ff7f50", fg="white"
            ).grid(row=i+1, column=1, padx=10, pady=5)

    def select_workout(self, workout):
        selected_date = self.cal.get_date()
        self.window.destroy()
        open_time_slot_screen(workout["name"], selected_date, self.user_email, self.user_full_name)


def open_dashboard(user_full_name, user_email):
    Dashboard(user_full_name, user_email)

# For testing only
# open_dashboard("Test User", "test@example.com")
