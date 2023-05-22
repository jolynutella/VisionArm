import pytest

from visionarm import create_app, db
from dotenv import load_dotenv

@pytest.fixture()
def app():
    load_dotenv()
    app = create_app(config_file='settings.py')

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()