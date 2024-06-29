import os

DEBUG = False

CSRF_ENABLED = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

SECRET_KEY = "secret"

# roles, names만 수정하면 됩니다.
roles = ["회장", "부회장", "총무"]
names = [
    "Alice",
    "Bob",
    "Charlie",
]
candidates = {name: {role: 0 for role in roles} for name in names}
candidates["기권"] = {role: 0 for role in roles}
