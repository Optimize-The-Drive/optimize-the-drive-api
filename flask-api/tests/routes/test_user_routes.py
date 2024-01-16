'''
    Defines user route tests
'''

import pytest

from tests.helpers import (
    user_repo, get_response_body,
)

# USER CREATE
def test_user_create(client):
    '''
        Tests that user creation route as intended.
        
        POST /api/user/register
    '''
    form = {
        'username': 'test_user_one',
        'email': 'userone.test@email.com',
        'password': 'secretPassword1!',
        'confirm_password': 'secretPassword1!'
    }

    response = client.post('/api/user/register', json=form)
    user = get_response_body(response)['user']

    assert(
        response.status_code == 201 and
        user['username'] == 'test_user_one' and
        user['email'] == 'userone.test@email.com'
    )


def test_user_create_username(client):
    '''
        Tests that user creation fails if username doesn't meet criteria
        
        POST /api/user/register
    '''

    # repeated symbols
    form = {
        'username': 'test__userone',
        'email': 'userone.test@email.com',
        'password': 'secretPassword1!',
        'confirm_password': 'secretPassword1!'
    }
    response = client.post('/api/user/register', json=form)
    assert response.status_code == 422
    # Beginning with symbols
    form['username'] = '.userone'
    response1 = client.post('/api/user/register', json=form)
    assert response1.status_code == 422
    # Ending with symbols
    form['username'] = 'userone.'
    response2 = client.post('/api/user/register', json=form)
    assert response2.status_code == 422
    # Too short
    form['username'] = 'asd'
    response3 = client.post('/api/user/register', json=form)
    assert response3.status_code == 422
    # Too long
    form['username'] = 'asdasdfasdfasdfasdfasdfasdfasdfasdfsadfasdf'
    response4 = client.post('/api/user/register', json=form)
    assert response4.status_code == 422


def test_user_create_email(client):
    '''
        Tests that user creation fails if email doesn't meet criteria
        
        POST /api/user/register
    '''

    # No @ or .
    form = {
        'username': 'testusertwo',
        'email': 'invalid',
        'password': 'secretPassword1!',
        'confirm_password': 'secretPassword1!'
    }
    response = client.post('/api/user/register', json=form)
    assert response.status_code == 422
    # No .
    form['email'] = 'invalid@a'
    response1 = client.post('/api/user/register', json=form)
    assert response1.status_code == 422
    # No @
    form['email'] = 'a.com'
    response2 = client.post('/api/user/register', json=form)
    assert response2.status_code == 422


def test_user_create_password(client):
    '''
        Tests that user creation fails if password doesn't meet criteria
        
        POST /api/user/register
    '''
    # Too short
    form = {
        'username': 'testusertwo',
        'email': 'invalid',
        'password': 'pass',
        'confirm_password': 'secretPassword1!'
    }
    response = client.post('/api/user/register', json=form)
    assert response.status_code == 422
    # No Uppercase
    form['password'] = 'invalid2!!!!!!'
    response1 = client.post('/api/user/register', json=form)
    assert response1.status_code == 422
    # No lowercase
    form['password'] = 'INVALID2!!!!'
    response2 = client.post('/api/user/register', json=form)
    assert response2.status_code == 422
    # No symbol
    form['password'] = 'InvalidPassword2'
    response3 = client.post('/api/user/register', json=form)
    assert response3.status_code == 422
    # No number
    form['password'] = 'InvalidPassword!'
    response4 = client.post('/api/user/register', json=form)
    assert response4.status_code == 422


def test_user_exists(client):
    '''
        Tests that user creation fails a user already exists with the same email
        or username.
        
        POST /api/user/register
    '''
    # User from the above create test, already exists
    form = {
        'username': 'test_user_one', #exists
        'email': 'another.test@email.com',
        'password': 'secretPassword1!',
        'confirm_password': 'secretPassword1!'
    }
    response = client.post('/api/user/register', json=form)
    assert response.status_code == 409
    form = {
        'username': 'another_user',
        'email': 'userone.test@email.com', #exists
        'password': 'secretPassword1!',
        'confirm_password': 'secretPassword1!'
    }
    response1 = client.post('/api/user/register', json=form)
    assert response1.status_code == 409


# USER DELETE
@pytest.mark.parametrize(
    'auth_client',
    [{'username': 'testuserdelete', 'password': 'testuserdeletepassword'}],
    indirect=True
)
@pytest.mark.usefixtures("app_ctx")
def test_user_delete(auth_client):
    '''
        Tests that user deletion route as intended.
        
        DELETE /api/user/me
    '''
    client, headers = auth_client

    response = client.delete('/api/user/me', headers={'Authorization': headers['Authorization']})
    response1 = client.post('/api/auth/logout', headers={'Authorization': headers['Authorization']})

    user = user_repo.by_username('testuserdelete')

    assert response.status_code == 200 and response1.status_code == 401 and user is None



def test_user_delete_guarded(client):
    '''
        Tests that the user deletion route is protected.

        DELETE /api/user/me
    '''

    response = client.delete('/api/user/me')

    assert response.status_code == 401
