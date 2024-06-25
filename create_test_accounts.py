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

test_accounts = [
    ("user1", "password1"),
    ("user2", "password2"),
    ("user3", "password3"),
]

for username, password in test_accounts:
    hashed_password = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
    try:
        cursor.execute(
            """
            INSERT INTO user (username, password, is_voted)
            VALUES (?, ?, ?)
            """,
            (username, hashed_password, False),
        )
        print(f"Test user '{username}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")

conn.commit()
conn.close()
