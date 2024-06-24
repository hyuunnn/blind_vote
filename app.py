from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from models import db, User
from forms import LoginForm

# roles, names만 수정하면 됩니다.
roles = ["회장", "부회장", "총무"]
names = [
    "Alice",
    "Bob",
    "Charlie",
]
candidates = {name: {role: 0 for role in roles} for name in names}


app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)  # SQLAlchemy 연결

login_manager = LoginManager()
login_manager.init_app(app)  # LoginManager 연결


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_voted:
            return redirect(url_for("result"))
        else:
            return redirect(url_for("vote"))
    else:
        return redirect(url_for("login"))


@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    if current_user.is_voted:
        flash("이미 투표하셨습니다.", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        for role in roles:
            selected_candidate = request.form.get(role)
            if selected_candidate:
                candidates[selected_candidate][role] += 1

        current_user.is_voted = True
        db.session.commit()
        flash("투표가 완료되었습니다.", "success")
        return redirect(url_for("index"))

    return render_template("vote.html", roles=roles, names=names)


@app.route("/result", methods=["GET"])
@login_required
def result():
    if not current_user.is_voted:
        flash("투표를 먼저 진행해주세요.", "info")
        return redirect(url_for("index"))

    return render_template("result.html", roles=roles, candidates=candidates)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        users = User.query.all()
        for user in users:
            user.is_voted = False
        db.session.commit()

    app.run(host="0.0.0.0", port=5000)
