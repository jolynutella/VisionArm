from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extentions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
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
        raise AttributeError('Cannot view unhashed password!')
    
    @unhashed_password.setter 
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))
