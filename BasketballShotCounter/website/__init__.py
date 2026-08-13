import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from os import path 
from flask_login import LoginManager 
  
db = SQLAlchemy() #initialises SQLAlchemy 
DB_NAME = "user_info.db" 
 
def create_app(): 
    app = Flask(__name__) #initialises the Flask web application 
    app.config['SECRET_KEY'] = os.urandom(10) 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
 
    db.init_app(app) #connects database to flask app 
 
    from .models import User #imports the User model 
 
    create_database(app) #calls the function that creates the database if it doesnt exist  
 
    #imports the blueprints from auth.py and views.py 
    from .auth import auth 
    from .views import views 
 
    #defines the url prefix for the routes in both blueprints 
    app.register_blueprint(auth, url_prefix='/auth') 
    app.register_blueprint(views, url_prefix='/') 
 
    login_manager = LoginManager() #creates an instance of Login Manager 
    login_manager.login_view = 'auth.login' #sets default login URL to the login page 
    login_manager.init_app(app) #connects Login Manger to the flask app 
 
    @login_manager.user_loader 
 
    #function that gets the user object from the database using their ID  
    def load_user(id):  
        return User.query.get(int(id)) 
 
    return app 
 
def create_database(app): 
    if not path.exists(DB_NAME): #checks if database file exists 
        with app.app_context(): 
            db.create_all() #creates the tables in the database 
 
 