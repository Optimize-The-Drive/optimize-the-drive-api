""" Defines pytest fixures for the tests. """

from time import time
import pytest
from socketio import Client

from app import create_app, socketio # pylint: disable=E0401
from tests.helpers import (
    add_user_to_db, remove_user_from_db,
    add_trip_to_db, remove_trip_from_db
)


@pytest.fixture(scope='session')
def test_app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    yield app


@pytest.fixture
def app_ctx(test_app):
    """Creates an application context, useful for querying DB state."""
    with test_app.app_context():
        yield


@pytest.fixture
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()


@pytest.fixture
def runner(app):
    """Runner for testing"""
    return app.test_cli_runner()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call): # pylint: disable=W0613
    """Adds report to pytest output."""
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, '__doc__')
    if docstring:
        report.nodeid = docstring


@pytest.fixture
def auth_client(client):
    '''
        Logs in an authenticated user to use in other tests.

        Returns [client, headers(csrf_token, authorization)]
    '''
    def _auth_client(username: str = 'test-user', password: str = 'test-password'):
        login_data = {
            'username': username,
            'password': password
        }

        response = client.post('/api/auth/login', json=login_data)

        # If the user doesn't exist, register them and reauthenticate
        if response.status_code == 401:
            register_data = {
                'username': username,
                'email': f'{time()}@testemail.com',
                'password': password,
                'confirm_password': password
            }

            _res = client.post('/api/user/register', json=register_data)
            response = client.post('/api/auth/login', json=login_data)

        access_token = response.json['access_token']
        csrf_token = client.get_cookie('csrf_refresh_token').value

        return [client, {'Authorization': f'Bearer {access_token}', 'X-CSRF-TOKEN': csrf_token }]

    return _auth_client


@pytest.fixture
def db_user():
    '''
         Fixture to add a user to the db for a test.
    '''
    user = add_user_to_db(f'{time()}-user', f'{time()}@testemail.com', f'{time()}-password')
    yield user

    remove_user_from_db(user)

@pytest.fixture
def db_trip(db_user):
    '''
        Fixture to add a trip to the db for a test.
    '''
    trip = add_trip_to_db(f'{time()}-trip', user_id=db_user.id)
    yield trip

    remove_trip_from_db(trip)



# @pytest.fixture
# def user_in_db():
#     '''
#         Fixture to add a user to the db for a test.
#     '''
#     user = add_user_to_db(f'{time()}-user', f'{time()}@testemail.com', f'{time()}-password')

#     return user


# SocketIO stuff
@pytest.fixture
def sio_client(test_app, client):
    yield socketio.test_client(test_app, flask_test_client=client)

@pytest.fixture
def auth_sio_client(test_app, auth_client):
    client, headers = auth_client()
    auth = {'token': headers['Authorization'].split('Bearer ')[1]}

    yield socketio.test_client(test_app, flask_test_client=client, auth=auth)
