from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import enum
from appdata.extensions import db

class VisitType(enum.Enum):
    RES = 0
    NOW = 1
    PAS = 2

class RoomType(enum.Enum):
    ECON = 0
    PREM = 1
    SUPR = 2

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    isEmployee = db.Column(db.Boolean, nullable=False, default=False)

    customers = db.relationship('Customer', uselist=False, backref='user', cascade="all, delete-orphan")
    employees = db.relationship('Employee', uselist=False, backref='user', cascade="all, delete-orphan")

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot read unhashed password.')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Employee(db.Model):
    user_id = db.Column(db.String(32), db.ForeignKey('user.login'), primary_key = True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    isOwner = db.Column(db.Boolean, nullable=False, default=False)
    isManager = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(254))

class Customer(db.Model):
    user_id = db.Column(db.String(32), db.ForeignKey('user.login'), primary_key = True)
    email = db.Column(db.String(254), nullable=False)
    
    visits = db.relationship('Visit', backref='customer', cascade="all, delete-orphan")


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String)
    description = db.Column(db.String)

    rooms = db.relationship('Room', backref='hotel', cascade="all, delete-orphan")
    employees = db.relationship('Employee', backref='hotel')

room_visit = db.Table('room_visit',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True),
    db.Column('visit_id', db.Integer, db.ForeignKey('visit.id'), primary_key=True)
)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    number = db.Column(db.Integer, nullable=False)
    night_price = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.Enum(RoomType))
    number_of_beds = db.Column(db.Integer, nullable=False)

    visits = db.relationship(
        'Visit',
        secondary=room_visit,
        lazy='subquery',
        backref=db.backref('rooms')
    )

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.String(32), db.ForeignKey('customer.user_id'))
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float)
    visit_type = db.Column(db.Enum(VisitType))

    reservation = db.relationship('Reservation', uselist=False, backref='visit')
    ongoing = db.relationship('Ongoing', uselist=False, backref='visit')
    past = db.relationship('Past', uselist=False, backref='visit')


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
