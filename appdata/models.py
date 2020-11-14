from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from appdata.extensions import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot read unhashed password.')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))