import pytest
from visionarm.models import User

@pytest.fixture
def user():
    """
    Fixture function to create a sample user object for testing.
    It creates a `User` instance with predefined attributes and returns it.
    """
    return User(
        login='testuser',
        password='testpassword',
        name='John',
        surname='Doe',
        expert=False,
        admin=False
    )


def test_unhashed_password_property(user):
    """
    Test case to verify the behavior of the `unhashed_password` property.
    It attempts to access the `unhashed_password` attribute of the provided `user` object
    and verifies that it raises an `AttributeError` exception. It also checks that the
    correct error message is raised.
    """
    with pytest.raises(AttributeError) as exc_info:
        _ = user.unhashed_password

    assert str(exc_info.value) == 'Cannot view unhashed password!'
    