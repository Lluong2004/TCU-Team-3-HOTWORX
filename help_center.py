import tkinter as tk

import tkinter as tk

def open_help_center():
    help_win = tk.Toplevel()
    help_win.title("HOTWORX Help Center")
    help_win.geometry("500x400")
    help_win.configure(bg="#f5f5f5")

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

    help_win.mainloop()
    