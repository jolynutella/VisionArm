from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from visionarm.extentions import db
from visionarm.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        unhashed_password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']

        existing_user = User.query.filter_by(login=login).first()

        error_message = ''

        if existing_user is not None:
            error_message = 'User already exists.'
            flash(error_message, 'danger')
            return redirect(url_for('auth.register'))
        
        if not error_message:
            user = User(login=login, unhashed_password=unhashed_password, name=name, surname=surname, admin=False, expert=False)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']

        user = User.query.filter_by(login=login).first()

        error_message = ''

        if not user or not check_password_hash(user.password, password):
            error_message = 'Could not log in. Please check the information and try again.'
            flash(error_message, 'danger')
            return redirect(url_for('auth.login'))

        if not error_message:
            login_user(user)
            return redirect(url_for('main.index'))
        
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))