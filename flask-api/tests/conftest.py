""" Defines pytest fixures for the tests. """

from time import time
import pytest

from app import create_app # pylint: disable=E0401
from tests.helpers import add_user_to_db


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
@pytest.mark.usefixtures("app_ctx")
def auth_client(request, client):
    '''
        Logs in an authenticated user to use in other tests.

        Returns [client, headers(csrf_token, authorization)]
    '''

    login_data = {
        'username': 'test-user',
        'password': 'test-password'
    }

    if request and getattr(request, 'param', None):
        username, password = request.param['username'], request.param['password']
        login_data = {
            'username': username,
            'password': password
        }
        response = client.post('/api/auth/login', json=login_data)

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


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def user_in_db():
    '''
        Fixture to add a user to the db for a test.
    '''
    user = add_user_to_db(f'{time()}-user', f'{time()}@testemail.com', f'{time()}-password')

    return user
