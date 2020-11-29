import datetime

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import DateField
from wtforms import StringField, TextField, SubmitField, PasswordField, HiddenField, FloatField, IntegerField, SelectField
from wtforms.validators import Length, Email, EqualTo, InputRequired, DataRequired, Optional
from werkzeug.security import check_password_hash

from appdata.models import User, Customer, Room, Visit, Reservation, Ongoing, Past

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
    submit_ = SubmitField('Přihlásit se')

    def validate_login(self, field):
        if not User.query.filter_by(login=field.data).first():
            field.errors.append('Tento uživatel neexistuje.')

    def validate_password(self, field):
        user = User.query.filter_by(login=self.login.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                field.errors.append('Špatné heslo.')


class ReservationForm(FlaskForm):
    hotel_id = 0
    avaiable_rooms = []

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
    one_rooms = SelectField('Počet pokojů',
        choices=[1,2,3,4],
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Vytvořit rezervaci')

    def validate_date_from(self, field):
        now = datetime.date.today()
        date_from = field.data
        if (date_from < now):
            field.errors.append('Pobyt nesmí začínat v minulosti.')
    
    def validate_date_to(self, field):
        now = datetime.date.today()
        date_from = field.data
        if (date_from < now):
            field.errors.append('Pobyt nesmí končit v minulosti.')
        delta = field.data - self.date_from.data
        if (delta.days > 30):
            field.errors.append('Pobyt lze zarezervovat na maximálně 30 nocí.')
        if (field.data == self.date_from.data):
            field.errors.append('Pobyt lze zarezervovat na minimálně 1 noc.')

    def validate_one_rooms(self, field):
        f_from = self.date_from.data
        f_to = self.date_to.data
        
        # get all avaiable rooms
        rooms = Room.query.filter_by(hotel_id=self.hotel_id).all()
        
        # get all forbidden rooms
        forbidden_visits = Visit\
                .query\
                .filter(Visit.visit_type != 'PAS')\
                .filter(((f_from >= Visit.date_from) & (f_from < Visit.date_to)) \
                    | ((f_to > Visit.date_from) & (f_to <= Visit.date_to)))\
                .all()
        forbidden_rooms = []
        for visit in forbidden_visits:
            forbidden_rooms.extend(visit.rooms)
        forbidden_rooms = list(set(forbidden_rooms))

        avaiable_rooms = list(set(rooms) - set(forbidden_rooms))
        if not avaiable_rooms or len(avaiable_rooms) < int(field.data):
            field.errors.append('Pro zvolené datum nejsou volné pokoje. Zbývá ' + str(len(avaiable_rooms)) + ' pokojů.')
        else:
            self.avaiable_rooms = avaiable_rooms
