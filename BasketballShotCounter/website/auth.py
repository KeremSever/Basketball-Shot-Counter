from flask import Blueprint, render_template, request, flash, redirect
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 


@auth.route('/login', methods = ['GET','POST'])

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        
        existing_user = User.query.filter_by(username=username).first()
        
        if not username or not password:
                flash('Username or password cannot be empty')

        else:
            if existing_user: 
                if check_password_hash(existing_user.password, password): 

                    login_user(existing_user, remember = True) #marks user as logged in, True means that if they close and open the browser, they will stay logged in

                    return redirect('/') 
                else:
                    flash('Incorrect Password, try again') 

            else:
                flash('Username doesn\'t exist, try again') 
        

    return render_template("login.html", user = current_user)

@auth.route('/signup', methods = ['GET','POST'])

def signup():
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password') 

        
        existing_user = User.query.filter_by(username=username).first()

        special_characters = '!"£$%^&*()_+-=][{}#\'@~/.?><,'

        if not existing_user: 

            if not username or not password:
                flash('Username or password cannot be empty')

            elif len(username) <= 6:
                flash('Username must be greater than 6 characters')
            elif len(username) >= 15:
                flash('Username must be less than 15 characters')
            elif not any(char.isalpha() for char in username):
                flash('The username must contain at least one letter')

            
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
                
            else: 

                hashed_password = generate_password_hash(password, method = 'pbkdf2:sha512') 

                new_user = User(username = username, password = hashed_password) 
      
                db.session.add(new_user)
                db.session.commit()

                #marks user as logged in, True means that if they close and open the browser, they will stay logged in
                login_user(new_user, remember = True)
                
                return redirect('/') 
        else:
            flash('Username already exists')
                    
    return render_template("signup.html", user = current_user)

@auth.route('/logout')

def logout():
    logout_user()
    return redirect('/auth/login')

