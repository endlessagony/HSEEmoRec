from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(250))
    second_name = db.Column(db.String(250))
    position = db.Column(db.String(250))
    sex = db.Column(db.String(250))
    age = db.Column(db.Integer)
