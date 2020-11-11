from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from extensions import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean)

    @property
    def unhashed_password(self):
        raise AttributeError('cannot lol')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))