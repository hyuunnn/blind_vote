from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from bcrypt import checkpw
from hmac import compare_digest
import hashlib
import base64

db = SQLAlchemy()


# https://github.com/KEEPER31337/Homepage-Back-R2/blob/develop/src/main/java/com/keeper/homepage/global/config/password/PasswordFactory.java#L44
def check_pbkdf2_sha256(password, password_hash):
    try:
        parts = password_hash.split(":")
        if len(parts) != 4:
            return False

        iterations = int(parts[1])
        salt = parts[2]
        hash_value = parts[3]

        hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
            dklen=32,
        )
        computed_hash = base64.b64encode(hash).decode("utf-8")
        return compare_digest(computed_hash[:32], hash_value)
    except Exception as e:
        return False


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_voted = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        try:
            return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        except Exception as e:
            return check_pbkdf2_sha256(self.password, password)
        except Exception as e:
            raise Exception(f"비밀번호 확인 중 예외 발생: {str(e)}")

    def __repr__(self):
        return f"<User {self.username}>"
