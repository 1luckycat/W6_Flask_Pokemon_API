from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

# internal import
from pokemon_shop.models import User, db
from pokemon_shop.forms import RegisterForm, LoginForm


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        print(email, password, username)

        if User.query.filter(User.username == username).first():
            flash(f"Username {username} already exists.  Please try again.", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash(f"Email {email} already exists.  Please try again.", category='warning')
            return redirect('/signup')
        
        user = User(username, email, password, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        flash(f"Your username {username} have been successfully registered.", category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=registerform)



@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():

        email = loginform.email.data
        password = loginform.password.data

        print('Login Form', email, password)

        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"{email} was successfully logged in.", category='success')
            return redirect('/')
        else: 
            flash('Invalid Email and/or Password.  Please try again.', category='warning')
            return redirect('/signin')
        
    return render_template('sign_in.html', form=loginform)



@auth.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", category='success')
    return redirect('/')

