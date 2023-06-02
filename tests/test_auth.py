from visionarm.models import User
from visionarm.extentions import db

def test_register_title(client):
    """
    Test case to verify that the registration page has the expected title.
    It sends a GET request to the '/register' route and checks if the response
    contains the correct HTML title tag.
    """
    response = client.get("/register")
    assert b"<title>Register</title>" in response.data


def test_login_title(client):
    """
    Test case to verify that the login page has the expected title.
    It sends a GET request to the '/login' route and checks if the response
    contains the correct HTML title tag.
    """
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data


def test_successfull_registration(client, app):
    """
    Test case to verify a successful user registration.
    It sends a POST request to the '/register' route with valid user data,
    and then checks if the user is created in the database and if the
    response status code is 302 (redirect).
    """
    response = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    with app.app_context():
        assert response.status_code == 302
        user = User.query.filter_by(login='test_user').first()
        assert user is not None
        assert User.query.count() == 1
        assert not user.admin
        assert not user.expert


def test_failed_registration(client, app):
    """
    Test case to verify a failed user registration.
    It sends a POST request to the '/register' route with empty user data,
    and then checks if the user is not created in the database and if the
    response status code is 302 (redirect).
    """
    response = client.post('/register', data=dict(login='', password='', name='', surname=''))

    with app.app_context():
        assert response.status_code == 302
        user = User.query.filter_by(login='test_user').first()
        assert user is None


def test_user_already_exists(client):
    """
    Test case to verify that a user cannot be registered with an existing login.
    It sends two POST requests to the '/register' route with the same user data,
    and then checks if the second response has a status code of 302 (redirect)
    and redirects back to the '/register' route.
    """
    response_1 = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    response_2 = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    assert response_2.status_code == 302
    assert response_2.location == '/register'


def test_valid_login(client):
    """
    Test case to verify a valid user login.
    It sends a POST request to the '/register' route to create a user,
    and then sends a POST request to the '/login' route with the same user credentials.
    Finally, it sends a GET request to the '/ask' route and checks if the response
    status code is 200 (success).
    """
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 200


def test_invalid_login(client):
    """
    Test case to verify an invalid user login.
    It sends a POST request to the '/login' route without registering a user,
    and then checks if the response status code is 302 (redirect).
    """
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 302


def test_logout(client):
    """
    Test case to verify user logout functionality.
    It sends a POST request to the '/register' route to create a user,
    then sends a POST request to the '/login' route with the user credentials,
    and finally sends a GET request to the '/ask' route to verify successful login.
    After that, it sends a GET request to the '/logout' route and checks if the
    response status code is 302 (redirect) and redirects to the '/login' route.
    """
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 200

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.location == '/login'
