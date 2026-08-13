from . import db 
from flask_login import UserMixin 
from sqlalchemy.sql import func 
 
 
class User(db.Model, UserMixin): #database table storing user info 
    id = db.Column(db.Integer, primary_key = True) #unique ID 
    username = db.Column(db.String(100), unique = True, nullable = False) #unique username 
    password = db.Column(db.String(100), nullable = False) #users password 
 
class UserStats(db.Model): #database table storing users statistics 
    id = db.Column(db.Integer, primary_key = True) #unique ID 
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #the users id 
    shot_type = db.Column(db.String(15), nullable = False) #type of shot 
    shot_count = db.Column(db.Integer, nullable = False) #number of shots attempted 
    make_count = db.Column(db.Integer, nullable = False) #number of shots made 
    field_goal = db.Column(db.Integer, nullable = False) #field goal percentage 
 
 
 