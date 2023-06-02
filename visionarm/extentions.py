from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initialize the LoginManager instance
login_manager = LoginManager()

# Initialize the SQLAlchemy instance
db = SQLAlchemy()