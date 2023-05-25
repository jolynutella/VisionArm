import pytest
from visionarm.models import User

@pytest.fixture
def user():
    # Create a sample user object for testing
    return User(
        login='testuser',
        password='testpassword',
        name='John',
        surname='Doe',
        expert=False,
        admin=False
    )


def test_unhashed_password_property(user):
    # Verify that accessing unhashed_password raises an AttributeError
    with pytest.raises(AttributeError) as exc_info:
        _ = user.unhashed_password

    # Verify that the correct error message is raised
    assert str(exc_info.value) == 'Cannot view unhashed password!'