from flask import Flask

from .commands import create_tables
from .extentions import db, login_manager
from .models import User
from .routes.auth import auth
from .routes.main import main
from .routes.manipulator import manipulator

# Create the Flask application
def create_app(config_file='settings.py'):
    app = Flask(__name__)

    # Load configuration from the specified file
    app.config.from_pyfile(config_file)

    # Initialize the database
    db.init_app(app)

    # Initialize the login manager
    login_manager.init_app(app)

    # Set the login view for authentication
    login_manager.login_view = 'auth.login'

    # Define the user loader function for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register blueprints for different routes
    app.register_blueprint(main)
    app.register_blueprint(auth)
    #app.register_blueprint(manipulator)

    # Add custom CLI commands
    app.cli.add_command(create_tables)

    return app
