import pytest

from flask_login import login_user

from visionarm.models import User, Question
from visionarm import db


def test_home_title(client):
    response = client.get("/")
    assert b"<title>Questions & Answers</title>" in response.data
    assert response.status_code == 200


def test_ask_title(client):
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    
    response = client.get("/ask")
    assert b"<title>Ask a Question</title>" in response.data


def test_ask(app, client):

    with app.app_context():

        response = client.post('/register', data=dict(login='expert', password='password', name='expert', surname='expert'), follow_redirects=True)
        assert response.status_code == 200

        expert_user = User.query.filter_by(login='expert').first()
        expert_user.expert = True
        db.session.commit()

        response = client.post('/register', data=dict(login='test', password='test_password', name='test', surname='test'), follow_redirects=True)
        assert response.status_code == 200

        response = client.post('/login', data=dict(login='test', password='test_password', name='test', surname='test'), follow_redirects=True)
        assert response.status_code == 200

        response = client.post('/ask', data=dict(question='How to test code?', expert=1), follow_redirects=True)
        assert response.status_code == 200

        question = Question.query.filter_by(question='How to test code?').first()
        assert question.expert_id == 1
        assert question.asked_by_id == 2
        assert len(Question.query.all()) == 1


def test_answer(app, client):

    with app.app_context():
        
        # Register expert user
        response = client.post('/register', data=dict(login='expert', password='password', name='expert', surname='expert'), follow_redirects=True)
        assert response.status_code == 200

        # Ensure registration was successful
        expert_user = User.query.filter_by(login='expert').first()
        assert expert_user is not None

        # Set expert flag
        expert_user.expert = True
        db.session.commit()

        # Register test user
        response = client.post('/register', data=dict(login='test', password='test_password', name='test', surname='test'), follow_redirects=True)
        assert response.status_code == 200

        # Login as test user
        response = client.post('/login', data=dict(login='test', password='test_password', name='test', surname='test'), follow_redirects=True)
        assert response.status_code == 200

        # Ask a question
        response = client.post('/ask', data=dict(question='How to test code?', expert=1), follow_redirects=True)
        assert response.status_code == 200

        # Get question answer (should redirect to /)
        response = client.get('/answer/1')
        assert response.status_code == 302

        response = client.get('/logout')
        assert response.status_code == 302

        response = client.post('/register', data=dict(login='expert', password='password', name='expert', surname='expert'), follow_redirects=True)
        assert response.status_code == 200

        # Set expert flag
        expert_user.expert = True
        db.session.commit()

        # Login as expert user
        response = client.post('/login', data=dict(login='expert', password='password', name='expert', surname='expert'), follow_redirects=True)
        assert response.status_code == 200

        response = client.get('/answer/1')  # GET-запрос для получения страницы ответа
        assert response.status_code == 200

        # Answer question
        response = client.post('/answer/1', data=dict(answer='test answer for question 1'), follow_redirects=True)
        assert response.status_code == 200


def test_question_page(app, client):
    with app.app_context():
        # create a test question
        test_question = Question(question='Test Question',
                                answer='This is a test question answer.',
                                asked_by_id = 1,
                                expert_id=1)
        db.session.add(test_question)
        db.session.commit()

        # send a GET request to the question page
        response = client.get('/question/1')

        # check that the response status code is 200 OK
        assert response.status_code == 200


def test_question_route_invalid(client):
    response = client.get('/question/2')
    assert response.status_code == 404


def test_unanswered_route_for_regular_user(app, client):

    with app.app_context():

        client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
        client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

        response = client.get('/unanswered')

        assert response.status_code == 302
        assert response.location == '/'


def test_users_route(app, client):
    with app.app_context():
        # Login with the example user.
        client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
        client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

        # Try to access /users - should be redirected to the index page due to regular user permissions.
        response = client.get('/users')
        assert response.status_code == 302
        assert response.location == '/'

        # Promote the example user to an admin user.
        example_user = User.query.filter_by(login='test_user').first()
        example_user.admin = True
        db.session.commit()

        # Login as the promoted admin user.
        client.post('/login', data=dict(
            login='test_user',
            password='test_password'
        ), follow_redirects=True)

        # Access /users - should return the users page with a list of users.
        response = client.get('/users')
        assert response.status_code == 200


def test_promote_route(app, client):
    with app.app_context():
        # Login with the example user.
        client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
        client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

        # Try to promote a user - should be redirected to the index page due to regular user permissions.
        response = client.post('/promote/1')
        assert response.status_code == 302
        assert response.location == '/'

        # Promote the example user to an admin user.
        example_user = User.query.filter_by(login='test_user').first()
        example_user.admin = True
        db.session.commit()

        # Login as the promoted admin user.
        client.post('/login', data=dict(
            login='test_user',
            password='test_password'
        ), follow_redirects=True)

        # Promote the example user to an expert.
        response = client.post('/promote/1')
        assert response.status_code == 302
        assert response.location == '/users'

        # Verify that the example user is now an expert.
        example_user = User.query.filter_by(login='test_user').first()
        assert example_user.expert == True


def test_account_title(client):
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

    response = client.get("/edit")
    assert b"<title>Account</title>" in response.data


def test_successfull_edit(app, client):
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    response = client.post('/edit', data=dict(new_login="new_test_user",
                                              new_unhashed_password="new_password",
                                              new_name="new_name",
                                              new_surname="new_surname"))
    
    with app.app_context():
        assert response.status_code == 302
        user = User.query.filter_by(login='new_test_user').first()
        assert user is not None
        assert user.login == 'new_test_user'
        assert user.name == 'new_name'
        assert user.surname == 'new_surname'
        assert User.query.count() == 1


def test_unsuccessfull_edit(app, client):

    with app.app_context():

        client.post('/register', data=dict(login='test_user_1', password='test_password_1', name='John_1', surname='Doe_1'))
        client.post('/register', data=dict(login='test_user_2', password='test_password_2', name='John_2', surname='Doe_2'))

        client.post('/login', data=dict(login='test_user_1', password='test_password_1', name='John_1', surname='Doe_1'))

        response = client.post('/edit', data=dict(new_login="test_user_2",
                                              new_unhashed_password="test_password_2",
                                              new_name="John_2",
                                              new_surname="Doe_2"))
    
        assert response.status_code == 302
        assert  response.location == '/edit'
        user_1 = User.query.filter_by(login='test_user_1').first()
        user_2 = User.query.filter_by(login='test_user_2').first()
        assert user_1 is not None
        assert user_1 != user_2
        assert user_1.login == 'test_user_1'
        assert user_1.name == 'John_1'
        assert user_1.surname == 'Doe_1'


def test_delete_user(app, client):
    client.post('/register', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))
    
    with app.app_context():

        # Make sure the user is logged in
        response = client.get('/login')
        assert response.status_code == 200
        client.post('/login', data=dict(login='test_user', password='test_password', name='John', surname='Doe'))

        # Test deleting an existing user
        response = client.post('/delete/1')
        assert response.status_code == 302
        user = User.query.filter_by(id=1).first()
        assert user is None

        # Test deleting a non-existing user
        response = client.post('/delete/10')
        user = User.query.filter_by(id=10).first()
        assert user is None
        assert response.status_code == 302

        # Test deleting a user with a wrong user ID format
        response = client.post('/delete/abc')
        user = User.query.filter_by(id='abc').first()
        assert user is None
        assert response.status_code == 404
