from visionarm.models import User
from visionarm.extentions import db

def test_register_title(client):
    response = client.get("/register")
    assert b"<title>Register</title>" in response.data


def test_login_title(client):
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data


def test_successfull_registration(client, app):
    response = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    
    with app.app_context():
        assert response.status_code == 302
        user = User.query.filter_by(login='test_user').first()
        assert user is not None
        assert User.query.count() == 1
        assert not user.admin
        assert not user.expert   


def test_failed_registration(client, app):
    response = client.post('/register', data=dict(login='', password='', name='', surname=''))
    
    with app.app_context():
        assert response.status_code == 302
        user = User.query.filter_by(login='test_user').first()
        assert user is None


def test_user_already_exists(client):
    response_1 = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    response_2 = client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    
    assert response_2.status_code == 302
        
    assert response_2.location == '/register'
      
def test_valid_login(client):
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 200

def test_invalid_login(client):
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 302


def test_logout(client):
    
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get('/ask')

    assert response.status_code == 200
        
    response = client.get('/logout')
    assert response.status_code == 302
        
    assert response.location == '/login'
