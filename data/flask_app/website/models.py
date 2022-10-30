from . import db
from flask_login import UserMixin

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add Associated User Here
    stock = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    stocks = db.relationship("Stock")