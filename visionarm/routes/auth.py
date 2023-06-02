from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from visionarm.extentions import db
from visionarm.models import User

# Create a blueprint for authentication
auth = Blueprint('auth', __name__)

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Handle the POST request
    if request.method == 'POST':
        login = request.form['login']
        unhashed_password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        admin = bool(request.form.get('admin', False))
        expert = bool(request.form.get('expert', False))

        # Check if the user already exists
        existing_user = User.query.filter_by(login=login).first()

        error_message = ''

        if existing_user is not None:
            # User already exists, display an error message
            error_message = 'User already exists.'
            flash(error_message, 'danger')
            return redirect(url_for('auth.register'))

        if not error_message:
            # Create a new user and add it to the database
            user = User(login=login, unhashed_password=unhashed_password, name=name, surname=surname, admin=admin, expert=expert)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        
    # Render the registration template
    return render_template('register.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Handle the POST request
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']

        # Find the user in the database
        user = User.query.filter_by(login=login).first()

        error_message = ''

        if not user or not check_password_hash(user.password, password):
            # Invalid login credentials, display an error message
            error_message = 'Could not log in. Please check the information and try again.'
            flash(error_message, 'danger')
            return redirect(url_for('auth.login'))

        if not error_message:
            # Login the user and redirect to the main page
            login_user(user)
            return redirect(url_for('main.index'))
        
    # Render the login template
    return render_template('login.html')

# Logout route
@auth.route('/logout')
def logout():
    # Log out the user and redirect to the login page
    logout_user()
    return redirect(url_for('auth.login'))
