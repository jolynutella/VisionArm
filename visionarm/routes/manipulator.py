from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

manipulator = Blueprint('manipulator', __name__)

@manipulator.route('/manipulator')
@login_required
def manipulator():
    return render_template('manipulator.html')