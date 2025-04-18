import sqlite3

conn = sqlite3.connect("hotworx_users.db")
cursor = conn.cursor()

# ✅ UPDATED: includes user_email
def book_session(workout, date, time, sauna, user_email):
    cursor.execute(
        "INSERT INTO bookings (workout_name, date, time_slot, sauna_number, user_email) VALUES (?, ?, ?, ?, ?)",
        (workout, date, time, sauna, user_email)
    )
    conn.commit()

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('hotworx_users.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()

# -------------------------------
# USER FUNCTIONS
# -------------------------------

def register_user(first_name, last_name, email, password):
    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, password))
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Email already registered."

def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchone()
    if result:
        full_name = f"{result[1]} {result[2]}"
        return True, full_name
    else:
        return False, "Invalid email or password."

# -------------------------------
# Cleanup (optional)
# -------------------------------

def close_connection():
    conn.close()

# Create bookings table if not already there
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_name TEXT,
    date TEXT,
    time_slot TEXT,
    sauna_number INTEGER
)
''')
conn.commit()
def cancel_booking(booking_id):
    cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    conn.commit()
# Fetch all bookings
def get_all_bookings(user_email):  # 🔧 accepts email
    cursor.execute(
        "SELECT id, workout, date, time_slot, sauna_number FROM bookings WHERE user_email = ?",
        (user_email,)
    )
    return cursor.fetchall()


