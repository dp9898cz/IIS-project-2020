from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from appdata.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable = False)

    customers = db.relationship('Customer', uselist=False, backref='user')
    employees = db.relationship('Employee', uselist=False, backref='user')

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot read unhashed password.')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Employee(db.Model):
    user_id = db.Column(db.String(32), db.ForeignKey('user.login'), primary_key = True)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    isOwner = db.Column(db.Boolean, nullable=False, default=False)
    isManager = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(254))

class Customer(db.Model):
    user_id = db.Column(db.String(32), db.ForeignKey('user.login'), primary_key = True)
    email = db.Column(db.String(254), nullable=False)
    #todo datum narozeni?

    visits = db.relationship('Visit', backref='customer')


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.String(32), db.ForeignKey('customer.user_id'))
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer)

    reservation = db.relationship('Reservation', uselist=False, backref='visit')
    ongoing = db.relationship('Ongoing', uselist=False, backref='visit')
    past = db.relationship('Past', uselist=False, backref='visit')

    #todo many-to-many room relation


class Reservation(db.Model):
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), primary_key = True)
    is_paid_princ = db.Column(db.Boolean,nullable=False, default=False)
    is_paid_visit = db.Column(db.Boolean,nullable=False, default=False)

class Ongoing(db.Model):
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), primary_key = True)
    is_paid_visit = db.Column(db.Boolean,nullable=False, default=False)
    key_customer = db.Column(db.Boolean,nullable=False, default=False)

class Past(db.Model):
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), primary_key = True)
