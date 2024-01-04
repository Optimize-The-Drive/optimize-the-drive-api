"""Test Script for app.py"""
import pytest

from app import create_app # pylint: disable=E0401


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

        Returns [client, access_token]
    '''

    login_data = {
        'username': 'test-user',
        'password': 'test-password'
    }

    response = client.post('/api/auth/login', json=login_data)
    access_token = response.json['access_token']

    return [client, f'Bearer {access_token}']
