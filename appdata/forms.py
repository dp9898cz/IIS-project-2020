from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Email
#from wtfrecaptcha.fields import RecaptchaField

class RegisterForm(FlaskForm):
    """Register form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Submit')