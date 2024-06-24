import sqlite3
from bcrypt import hashpw, gensalt

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_voted BOOLEAN DEFAULT 0
    )"""
)

test_username = "user"
test_password = "password"
hashed_password = hashpw(test_password.encode("utf-8"), gensalt()).decode("utf-8")

try:
    cursor.execute(
        """
        INSERT INTO user (username, password, is_voted)
        VALUES (?, ?, ?)
        """,
        (test_username, hashed_password, False),
    )
    print(f"Test user '{test_username}' created successfully.")
except sqlite3.IntegrityError:
    print(f"User '{test_username}' already exists.")

conn.commit()
conn.close()
