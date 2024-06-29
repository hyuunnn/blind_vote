from flask import Flask, redirect, url_for, render_template, request, flash, send_file
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from models import db, User
from forms import LoginForm, VoteForm
from config import roles, candidates

import os
import io
import binascii
import csv

app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)  # SQLAlchemy 연결

login_manager = LoginManager()
login_manager.init_app(app)  # LoginManager 연결
login_manager.login_view = "login"  # 로그인이 필요한 페이지에 접근했을 때 redirect


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def generate_key():
    return binascii.hexlify(os.urandom(30)).decode("ascii")


def reset_votes():
    users = User.query.all()
    for user in users:
        user.is_voted = False
    db.session.commit()


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

    form = VoteForm()
    if form.validate_on_submit():
        for role in roles:
            selected_candidate = form.data.get(role)
            if selected_candidate:
                candidates[selected_candidate][role] += 1
            else:
                candidates["기권"][role] += 1

        current_user.is_voted = True
        db.session.commit()
        flash("투표가 완료되었습니다.", "success")
        return redirect(url_for("index"))

    return render_template("vote.html", form=form, roles=roles)


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


RESET_PATH = generate_key()
VOTE_STATUS_PATH = generate_key()
VOTE_EXPORT_PATH = generate_key()


@app.route(f"/{RESET_PATH}")
@login_required
def reset():
    reset_votes()
    for name in candidates:
        for role in candidates[name]:
            candidates[name][role] = 0

    flash("투표가 초기화되었습니다.", "success")
    return redirect(url_for("index"))


@app.route(f"/{VOTE_STATUS_PATH}")
@login_required
def vote_status():
    voted_users = User.query.filter_by(is_voted=True).all()
    not_voted_users = User.query.filter_by(is_voted=False).all()
    return render_template(
        "vote_status.html", voted_users=voted_users, not_voted_users=not_voted_users
    )


@app.route(f"/{VOTE_EXPORT_PATH}")
@login_required
def vote_export():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Role", "이름", "투표 수"])
    for name, roles_votes in candidates.items():
        for role, votes in roles_votes.items():
            writer.writerow([role, name, votes])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="vote_result.csv",
    )


if __name__ == "__main__":
    with app.app_context():
        reset_votes()

    print(f"RESET_PATH: {RESET_PATH}")
    print(f"VOTE_STATUS_PATH: {VOTE_STATUS_PATH}")
    print(f"VOTE_EXPORT_PATH: {VOTE_EXPORT_PATH}")

    app.run(host="0.0.0.0", port=5000)
