from extensions import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean)
    isOwner = db.Column(db.Boolean)
    isManager = db.Column(db.Boolean)
    isCustomer = db.Column(db.Boolean)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))