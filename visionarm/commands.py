import click

from flask.cli import with_appcontext
from .extentions import db
from .models import User, Question

# CLI command to create database tables
@click.command(name='create_tables')
@with_appcontext
def create_tables():
    # Create the database tables
    db.create_all()

