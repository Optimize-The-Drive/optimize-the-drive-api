"""Test Script for app.py"""
import pytest

from app import create_app # pylint: disable=E0401


@pytest.fixture
def test_app_fixture():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    yield app

@pytest.fixture
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture()
def runner(app):
    """Runner for testing"""
    return app.test_cli_runner()
