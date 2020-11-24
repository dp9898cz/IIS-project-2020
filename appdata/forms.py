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
        Email(message=('Zadejte validní email.')),
        InputRequired()
        ])
    reg_password = PasswordField('Heslo', [
        DataRequired(),
        Length(min = 5, message='Zadejte alespoň 5 znaků.')
        ])
    confirmPassword = PasswordField('Heslo znovu', [
            DataRequired(),
            EqualTo('reg_password', message='Hesla se musí shodovat.')
            ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Registrovat se')

    def validate_reg_login(self, field):
        #check if the login is already used
        if User.query.filter_by(login=field.data).first():
            field.errors.append('Tento login už někdo používá.')

    def validate_email(self, field):
        #check if the email is alreday used
        if Customer.query.filter_by(email=field.data).first():
            field.errors.append('Tento email už někdo používá.')


class LoginForm(FlaskForm):
    """Login form."""
    login = StringField('Login', [
        InputRequired()
    ])
    password = PasswordField('Heslo', [
        InputRequired()
    ])
    submit = SubmitField('Přihlásit se')

    def validate_login(self, field):
        if not User.query.filter_by(login=field.data).first():
            field.errors.append('Tento uživatel neexistuje.')

    def validate_password(self, field):
        user = User.query.filter_by(login=self.login.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                field.errors.append('Špatné heslo.')
