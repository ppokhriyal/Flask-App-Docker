from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,ValidationError
from dockerwebapp.models import User

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Login')