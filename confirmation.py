"""
HOTWORX Confirmation Screen
This module displays a class-based confirmation screen for a successful booking.
Includes:
- Branded logo and help center icon
- Loop for displaying booking info lines
- Buttons to view bookings or exit
"""

import tkinter as tk  # Import tkinter for GUI
from my_bookings import show_bookings_screen  # Function to display the user's bookings
from PIL import Image, ImageTk  # Image handling libraries
from help_center import open_help_center  # Opens the Help Center screen


class ConfirmationScreen:
    def __init__(self, workout, date, time, sauna, user_full_name, user_email):
        """
        Initialize the confirmation window and its data attributes.
        """
        self.user_email = user_email  # Store user's email for future use
        self.workout = workout  # Workout name
        self.date = date  # Booking date
        self.time = time  # Time slot
        self.sauna = sauna  # Sauna number
        self.user_full_name = user_full_name  # Store user's full name
        self.user_email = user_email  # Store again (already set above)

        # Setup GUI window
        self.window = tk.Tk()
        self.window.title("Booking Confirmed")
        self.window.geometry("400x320")
        self.window.configure(bg="#f5f5f5")

        self.setup_ui()  # Initialize interface elements
        self.window.mainloop()

    def setup_ui(self):
        """
        Set up the visual components of the confirmation window.
        """
        # Load and display HOTWORX logo
        logo_raw = Image.open("hotworx_logo.png").resize((130, 45))
        self.logo = ImageTk.PhotoImage(logo_raw, master=self.window)
        tk.Label(self.window, image=self.logo, bg="#f5f5f5").pack(pady=(10, 5))

        # Help Center icon in top-right corner
        help_raw = Image.open("helpcenter_icon.png").resize((20, 20))
        self.help_icon = ImageTk.PhotoImage(help_raw, master=self.window)
        tk.Button(self.window, image=self.help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).place(x=360, y=10)

        # Confirmation title
        tk.Label(self.window, text="\u2705 Booking Confirmed!", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#4caf50").pack(pady=20)

        # Loop through booking info lines and display them
        info_lines = [
            f"Workout: {self.workout}",
            f"Date: {self.date}",
            f"Time: {self.time}",
            f"Sauna #: {self.sauna}"
        ]
        for line in info_lines:
            tk.Label(self.window, text=line, bg="#f5f5f5").pack(pady=3)

        # Button options
        btn_frame = tk.Frame(self.window, bg="#f5f5f5")
        btn_frame.pack(pady=20)

        # Button to view user's bookings (using user_email)
        tk.Button(btn_frame, text="View My Bookings", command=lambda: show_bookings_screen(self.user_email),
                  bg="#2196f3", fg="white", width=16).grid(row=0, column=0, padx=10)

        # Button to return to the dashboard
        tk.Button(btn_frame, text="Back to Dashboard", command=self.go_back,
                  bg="#ff9800", fg="white", width=16).grid(row=1, column=0, padx=10, pady=5)

        # Button to close the window
        tk.Button(btn_frame, text="Finish", command=self.window.destroy,
                  bg="#ff7f50", fg="white", width=12).grid(row=0, column=1, padx=10)

    def go_back(self):
        from dashboard import open_dashboard  # ✅ Import locally to avoid circular import
        """
        Close confirmation screen and open the dashboard again.
        """
        self.window.destroy()
        open_dashboard(self.user_full_name, self.user_email)
# Since the function no longer passes full name, you can add it to the call if available
def show_confirmation_screen(workout, date, time, sauna, user_full_name, user_email): 
    ConfirmationScreen(workout, date, time, sauna, user_full_name, user_email) # replace "Guest" with full name if needed
    """
    Launch the confirmation screen window.
    """

# Example for manual testing (uncomment to use):
# show_confirmation_screen("Hot Cycle", "2025-04-22", "07:00 AM", 2, "test@example.com")
