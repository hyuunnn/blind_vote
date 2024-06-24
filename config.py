import os

DEBUG = False

CSRF_ENABLED = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

SECRET_KEY = "secret"
