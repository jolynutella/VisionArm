import os

# Retrieve the database URI from the environment variable 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Retrieve the secret key from the environment variable 'SECRET_KEY'
SECRET_KEY = os.environ.get('SECRET_KEY')

# Disable modification tracking for SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
