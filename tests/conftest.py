import pytest

from click.testing import CliRunner
from dotenv import load_dotenv

from visionarm import create_app, db
from visionarm.models import User

@pytest.fixture()
def app():
    load_dotenv()
    app = create_app(config_file='test_settings.py')

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner():
    return CliRunner()