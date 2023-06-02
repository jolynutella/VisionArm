import pytest
from click.testing import CliRunner
from dotenv import load_dotenv
from visionarm import create_app, db
from visionarm.models import User

@pytest.fixture()
def app():
    """
    Fixture that creates and configures a Flask application for testing.
    It uses the 'test_settings.py' configuration file.
    The database is created and initialized within the application context.
    """
    load_dotenv()
    app = create_app(config_file='test_settings.py')

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    """
    Fixture that provides a test client for making requests to the Flask application.
    It depends on the 'app' fixture for creating the application instance.
    """
    return app.test_client()

@pytest.fixture
def runner():
    """
    Fixture that provides a CliRunner instance for running command-line commands
    in the Flask application context.
    """
    return CliRunner()

