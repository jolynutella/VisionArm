from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extentions import db

class User(db.Model, UserMixin):
    """
    Represents a user in the application.

    Inherits from db.Model and UserMixin for database and authentication functionality, respectively.
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question',
        foreign_keys='Question.asked_by_id',
        backref='asker',
        lazy=True
    )

    answers_requested = db.relationship(
        'Question',
        foreign_keys='Question.expert_id',
        backref='expert',
        lazy=True
    )

    @property
    def unhashed_password(self):
        """
        Property that raises an error when attempting to access the unhashed password.

        Used to prevent direct access to the unhashed password.
        """
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        """
        Setter for the unhashed_password property.

        Generates a hashed password from the provided unhashed password and sets it as the user's password.
        """
        self.password = generate_password_hash(unhashed_password)


class Question(db.Model):
    """
    Represents a question in the application.

    Inherits from db.Model for database functionality.
    """

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))


