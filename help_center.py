"""
HOTWORX Help Center
This module provides a pop-up window with contact information and support
instructions for HOTWORX users. It is accessible from all screens via the help icon.
Includes:
- Branded header and instructions
- Static window that opens in response to help button
"""

import tkinter as tk #this will import the tkinter library for GUI creation
import tkinter as tk #this will import the tkinter library for GUI creation

def open_help_center(): #this will define the open_help_center function
    help_win = tk.Toplevel() #this will create a new top-level window
    help_win.title("HOTWORX Help Center") #this will set the title of the window to "HOTWORX Help Center"
    help_win.geometry("500x400") #this will set the size of the window to 500x400 pixels
    help_win.configure(bg="#f5f5f5") #this will set the background color of the window to a light gray color
     #This will create the label on the top
    tk.Label(help_win, text="📖 HOTWORX Help Center", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

    help_text = """
Need assistance?

📅 Booking
- Select a date and workout, then choose a time slot and sauna.

❌ Cancellations
- Click on the calendar on the top right then tap 'Cancel' on any session.

💬 Need More Help?
- Email support@hotworx.com

    """

    tk.Label(help_win, text=help_text, justify="left", bg="#f5f5f5", font=("Arial", 11)).pack(padx=20, pady=10)

    tk.Button(help_win, text="Close", command=help_win.destroy, bg="#ff7f50", fg="white", width=15).pack(pady=20)

    help_win.mainloop() #this will start the main loop of the window, allowing it to remain open until closed by the user
