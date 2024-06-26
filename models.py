from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from bcrypt import checkpw
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_voted = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        try:
            return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        except ValueError as e:
            return check_password_hash(self.password, password)
        except Exception as e:
            raise Exception(f"비밀번호 확인 중 예외 발생: {str(e)}")

    def __repr__(self):
        return f"<User {self.username}>"
