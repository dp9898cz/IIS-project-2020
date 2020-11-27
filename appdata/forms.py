from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import DateField
from wtforms import StringField, TextField, SubmitField, PasswordField, HiddenField, FloatField, IntegerField
from wtforms.validators import Length, Email, EqualTo, InputRequired, DataRequired, Optional
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



class ReservationForm(FlaskForm):
    """Form for main reservation"""
    login = StringField('Login', [
        Optional()
    ])
    name = StringField( 'Jméno', [
        InputRequired()
    ])
    surname = StringField( 'Příjmení', [
        InputRequired()
    ])
    email = StringField('Email', [
        Email(message=('Zadejte validní email.')),
        InputRequired()
    ])
    date_from = DateField(
        'Datum příjezdu', 
        format='%Y-%m-%d', 
        validators=[InputRequired()]
    )
    date_to = DateField(
        'Datum odjezdu', 
        format='%Y-%m-%d', 
        validators=[InputRequired()]
    )
    one_rooms = IntegerField('Počet jednolůžkových místností', [
        InputRequired()
    ])
    two_rooms = IntegerField('Počet dvoulůžkových místností', [
        InputRequired()
    ])
    three_rooms = IntegerField('Počet třílůžkových místností', [
        InputRequired()
    ])
    submit = SubmitField('Vytvořit rezervaci')