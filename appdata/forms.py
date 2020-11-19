from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, PasswordField, HiddenField
from wtforms.validators import Length, Email, EqualTo, InputRequired, DataRequired
from werkzeug.security import check_password_hash

from appdata.models import User, Customer

class RegisterForm(FlaskForm):
    """Register form."""
    reg_login = StringField('Login', [
        InputRequired()
        ])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        InputRequired()
        ])
    reg_password = PasswordField('Password', [
        DataRequired(),
        Length(min = 5, message='Enter at least 5 characters.')
        ])
    confirmPassword = PasswordField('Repeat Password', [
            DataRequired(),
            EqualTo('reg_password', message='Passwords must match.')
            ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_reg_login(self, field):
        #check if the login is already used
        if User.query.filter_by(login=field.data).first():
            field.errors.append('Login already exists.')

    def validate_email(self, field):
        #check if the email is alreday used
        if Customer.query.filter_by(email=field.data).first():
            field.errors.append('User with this email already exists.')


class LoginForm(FlaskForm):
    """Login form."""
    login = StringField('Login', [
        InputRequired()
    ])
    password = PasswordField('Password', [
        InputRequired()
    ])
    submit = SubmitField('Login')

    def validate_login(self, field):
        if not User.query.filter_by(login=field.data).first():
            field.errors.append('Login does not exist.')

    def validate_password(self, field):
        user = User.query.filter_by(login=self.login.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                field.errors.append('Wrong password entered.')
