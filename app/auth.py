import re
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import Users

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    """# Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))"""
    return render_template('index.html')


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)

        # Check if account exists using MySQL
        # Fetch one record and return result
        account = Users.query.filter_by(username=username).first()

        if account:
            password_rs = account.password
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account.id
                session['username'] = account.username
                session['fullname'] = account.firstname + account.lastname
                # Redirect to home page
                return redirect(url_for('auth.home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')

    return render_template('auth/login.html')


@auth.route('auth/register', methods=['GET', 'POST'])
def register():

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        firstname = request.form['firstname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        _hashed_password = generate_password_hash(password)

        # Check if account exists using MySQL
        account = Users.query.filter_by(username=username).first()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            user = Users(username=username, firstname=firstname, password=_hashed_password, email=email)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered!')
            redirect(url_for('auth.login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('auth/register.html')


@auth.route('/auth/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = Users.query.filter_by(id=session['id']).first()
        # Show the profile page with account info
        return render_template('auth/profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('auth.login'))


@auth.route('/auth/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('auth.login'))
