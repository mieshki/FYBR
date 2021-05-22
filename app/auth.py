from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    return render_template('base.html')


@auth.route('/auth/login')
def login():
    return render_template('auth/login.html')


@auth.route('/auth/register')
def register():
    return render_template('auth/login.html')


@auth.route('/auth/logout')
def logout():
    return render_template('base.html')
