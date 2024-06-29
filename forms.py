from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from config import roles, names


class LoginForm(FlaskForm):
    username = StringField("아이디", validators=[DataRequired()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    submit = SubmitField("로그인")


class VoteForm(FlaskForm):
    for role in roles:
        locals()[role] = SelectField(
            role,
            choices=[("", "선택하세요")] + [(name, name) for name in names],
            validators=[Optional()],
        )
    submit = SubmitField("투표하기")
