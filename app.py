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


def is_all_roles_selected(request_form):
    missing_roles = [role for role in roles if not request_form.get(role)]
    return not bool(missing_roles)


def is_candidates_valid(request_form):
    for role in roles:
        selected_candidate = request_form.get(role)
        if selected_candidate not in candidates:
            return False
    return True


@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    if current_user.is_voted:
        flash("이미 투표하셨습니다.", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        if not is_all_roles_selected(request.form):
            flash("모든 역할에 대해 선택하지 않았습니다.", "danger")
            return redirect(url_for("vote"))

        if not is_candidates_valid(request.form):
            flash("선택한 후보가 유효하지 않습니다.", "danger")
            return redirect(url_for("vote"))

        for role in roles:
            selected_candidate = request.form.get(role)
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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset-votes",
        "-r",
        action="store_true",
        help="모든 사용자의 투표 상태를 초기화합니다.",
    )
    args = parser.parse_args()

    if args.reset_votes:
        with app.app_context():
            users = User.query.all()
            for user in users:
                user.is_voted = False
            db.session.commit()
        print("[*] 모든 사용자의 투표 상태가 초기화되었습니다.")

    app.run(host="0.0.0.0", port=5000)
