from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin): #database table storing user info
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(100), unique = True, nullable = False) 
    password = db.Column(db.String(100), nullable = False) 

class UserStats(db.Model): #database table storing users statistics
    id = db.Column(db.Integer, primary_key = True) 
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    shot_type = db.Column(db.String(15), nullable = False) 
    shot_count = db.Column(db.Integer, nullable = False) 
    make_count = db.Column(db.Integer, nullable = False) 
    field_goal = db.Column(db.Integer, nullable = False) #field goal percentage



