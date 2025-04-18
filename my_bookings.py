import tkinter as tk
from db import get_all_bookings, cancel_booking
from PIL import Image, ImageTk
from help_center import open_help_center

# UPDATED: Now accepts user_email
def show_bookings_screen(user_email):
    def refresh():
        for widget in list_frame.winfo_children():
            widget.destroy()

        # UPDATED: Fetch bookings for this specific user
        bookings = get_all_bookings(user_email)

        if not bookings:
            tk.Label(list_frame, text="No bookings found.", bg="#f5f5f5", fg="gray").pack(pady=20)
        else:
            for b in bookings:
                booking_id, workout, date, time, sauna = b
                info = f"{date} — {time} | {workout} (Sauna #{sauna})"

                row = tk.Frame(list_frame, bg="#f5f5f5")
                row.pack(fill='x', padx=20, pady=4)

                tk.Label(row, text=info, bg="#f5f5f5", anchor="w", width=40).pack(side="left")
                tk.Button(
                    row,
                    text="Cancel",
                    command=lambda i=booking_id: handle_cancel(i),
                    bg="#f44336",
                    fg="white",
                    width=8
                ).pack(side="right")

    def handle_cancel(booking_id):
        cancel_booking(booking_id)
        refresh()

    win = tk.Tk()
    win.title("My Bookings")
    win.geometry("520x400")
    win.configure(bg="#f5f5f5")

    # Logo
    logo_raw = Image.open("hotworx_logo.png").resize((130, 45))
    logo = ImageTk.PhotoImage(logo_raw, master=win)
    tk.Label(win, image=logo, bg="#f5f5f5").pack(pady=(10, 5))
    win.logo = logo

    # Help icon
    help_img_raw = Image.open("helpcenter_icon.png").resize((20, 20))
    help_icon = ImageTk.PhotoImage(help_img_raw, master=win)
    tk.Button(win, image=help_icon, command=open_help_center, bg="#f5f5f5", borderwidth=0).place(x=480, y=10)
    win.help_icon = help_icon

    tk.Label(win, text="📅 My Booked Sessions", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    list_frame = tk.Frame(win, bg="#f5f5f5")
    list_frame.pack(fill="both", expand=True)

    refresh()

    tk.Button(win, text="Close", command=win.destroy, bg="#ff7f50", fg="white", width=15).pack(pady=20)

    win.mainloop()