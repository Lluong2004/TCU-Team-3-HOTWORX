"""
HOTWORX Database Migration Script
This script attempts to add a new column `user_email` to the `bookings` table.
It supports extended functionality such as tracking bookings per user.
This should only be run once during database setup or migration.
"""

import sqlite3

# Connect to your bookings database
conn = sqlite3.connect("hotworx_users.db")
cursor = conn.cursor()

# Try adding the new column
try:
    cursor.execute("ALTER TABLE bookings ADD COLUMN user_email TEXT;")
    print("✅ Column user_email added.")
except sqlite3.OperationalError as e:
    print("⚠️ Skipping - column might already exist:", e)

conn.commit()
conn.close()
