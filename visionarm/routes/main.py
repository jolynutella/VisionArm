from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from visionarm.extentions import db
from visionarm.models import Question, User 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Route function for the index page.
    Retrieves all questions that have an answer and renders the home template with the questions.
    """
    questions = Question.query.filter(Question.answer != None).all()

    context = {
        'questions': questions
    }
    return render_template('home.html', **context)

@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    """
    Route function for the ask page.
    Handles GET and POST requests.
    - GET: Renders the ask template with the list of experts.
    - POST: Handles form submission and adds a new question to the database.
    """
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(question=question, expert_id=expert, asked_by_id=current_user.id)

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter_by(expert=True).all()

    context = {
        'experts': experts
    }
    return render_template('ask.html', **context)

@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    """
    Route function for answering a question.
    Only experts can access this page.
    Handles GET and POST requests.
    - GET: Renders the answer template with the question details.
    - POST: Handles form submission and updates the answer for the question in the database.
    """
    if not current_user.expert:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))

    context = {
        'question': question
    }

    return render_template('answer.html', **context)

@main.route('/question/<int:question_id>')
def question(question_id):
    """
    Route function for displaying a question.
    Retrieves the question details from the database and renders the question template with the details.
    """
    question = Question.query.get_or_404(question_id)

    context = {
        'question': question
    }
    return render_template('question.html', **context)

@main.route('/unanswered')
@login_required
def unanswered():
    """
    Route function for displaying unanswered questions.
    Only experts can access this page.
    Retrieves unanswered questions for the current user and renders the unanswered template.
    """
    if not current_user.expert:
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query.filter_by(expert_id=current_user.id).filter(Question.answer == None).all()

    context = {
        'unanswered_questions': unanswered_questions
    }
    return render_template('unanswered.html', **context)

@main.route('/users')
@login_required
def users():
    """
    Route function for displaying users.
    Only admins can access this page.
    Retrieves non-admin users from the database and renders the users template.
    """
    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users': users
    }
    return render_template('users.html', **context)

@main.route('/promote/<int:user_id>', methods=['GET', 'POST'])
@login_required
def promote(user_id):
    """
    Route function for promoting/demoting a user to/from expert status.
    Only admins can access this page.
    Retrieves the user from the database, toggles the expert status, and commits the changes.
    """
    if not current_user.admin:
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)

    user.expert = not user.expert
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """
    Route function for editing the current user's account.
    Handles GET and POST requests.
    - GET: Renders the edit template.
    - POST: Handles form submission and updates the user's account details in the database.
    """
    if request.method == 'POST':
        new_login = request.form['new_login']
        existing_user = User.query.filter_by(login=new_login).first()
        error_message = ''

        if existing_user is not None:
            error_message = 'Login already exists.'
            flash(error_message, 'danger')
            return redirect(url_for('main.edit'))

        current_user.login = new_login
        current_user.unhashed_password = request.form['new_unhashed_password']
        current_user.name = request.form['new_name']
        current_user.surname = request.form['new_surname']

        db.session.commit()
        edit_message = 'Account successfully updated!'
        flash(edit_message, 'success')
        return redirect(url_for('main.edit'))

    return render_template('edit.html')

@main.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    """
    Route function for deleting a user's account.
    Only admins can access this page.
    Retrieves the user from the database and deletes their account.
    """
    user_to_delete = User.query.get(user_id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('auth.register'))
    
    except Exception as e:
        flash(f'Error deleting account: {str(e)}', 'danger')
        return redirect(url_for('main.edit'))

@main.route('/manipulator')
@login_required
def manipulator():
    """
    Route function for rendering the manipulator template.
    """
    return render_template('manipulator.html')

