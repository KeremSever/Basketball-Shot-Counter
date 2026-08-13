from flask import Blueprint, render_template, request, flash, redirect 
from . import db 
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user 
 
auth = Blueprint('auth', __name__) #creates a blueprint for auth routes 
 
#each @auth.route() gives the url for that page 
#function defines what happens when the user goes to that page 
 
@auth.route('/login', methods = ['GET','POST']) 
 
def login(): 
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password') 
 
        #checks if username is in database, if it is, stores that username, if not, stores 'None' 
        existing_user = User.query.filter_by(username=username).first() 
         
        if not username or not password: 
                flash('Username or password cannot be empty') 
 
        else: 
            if existing_user: #checks if user isnt 'None' 
                if check_password_hash(existing_user.password, password): #compares password entered by user to password in database 
 
                    login_user(existing_user, remember = True) #marks user as logged in, True means that if they close and open the browser, they will stay logged in 
 
                    return redirect('/') #sends the user to the homepage 
                else: 
                    flash('Incorrect Password, try again') #flashes a message if passwords dont match 
 
            else: 
                flash('Username doesn\'t exist, try again') #flashes a message if there are no usernames that match 
         
 
    return render_template("login.html", user = current_user) 
 
@auth.route('/signup', methods = ['GET','POST']) 
 
def signup(): 
    if request.method == 'POST': #checks if its a POST method 
        username = request.form.get('username') #gets the username inputted by the user 
        password = request.form.get('password') #gets the password inputted by the user 
 
        #checks if inputted username is in database, if it is, stores that object, if not, stores None 
        existing_user = User.query.filter_by(username=username).first() 
 
        #all special characters in a normal keyboard 
        special_characters = '!"£$%^&*()_+-=][{}#\'@~/.?><,' 
 
        if not existing_user: #checks if there are no usernames that are the same 
 
            #returns an error message if either box is left empty 
            if not username or not password: 
                flash('Username or password cannot be empty') 
 
            #validation specifically for username, flash messages explain what each line does 
            elif len(username) <= 6: 
                flash('Username must be greater than 6 characters') 
            elif len(username) >= 15: 
                flash('Username must be less than 15 characters') 
            elif not any(char.isalpha() for char in username): 
                flash('The username must contain at least one letter') 
 
            #validation for specifically password, flash messages explain what each line does 
            elif len(password) <= 6: 
                flash('Password must be greater than 6 characters') 
            elif len(password) >= 15: 
                flash('Password must be less than 15 characters ') 
            elif " " in password: 
                 flash('Password cannot contain spaces') 
            elif not any(char.isalpha() for char in password): 
                flash('The password must contain at least one letter') 
            elif not any(char in special_characters for char in password): 
                flash('The password must contain at least one special character') 
            elif not any(char.isdigit() for char in password): 
                flash('The password must contain at least one number') 
                 
            else: # if it has passed all of the checks 
                hashed_password = generate_password_hash(password, method = 'pbkdf2:sha512') #hashes the password for security 
 
                #creates a new object with users' username and hashes password 
                new_user = User(username = username, password = hashed_password)  
 
                #adds the new user to the database 
                db.session.add(new_user) 
                db.session.commit() 
 
                #marks user as logged in, True means that if they close and open the browser, they will stay logged in 
                login_user(new_user, remember = True) 
                 
                return redirect('/') #sends user to the homepage 
        else: 
            flash('Username already exists') 
                     
    return render_template("signup.html", user = current_user) 
 
@auth.route('/logout') 
 
def logout(): 
    logout_user() 
    return redirect('/auth/login') 
 