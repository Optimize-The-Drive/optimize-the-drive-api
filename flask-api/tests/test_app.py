import pytest

def test_home_route(client):
    """A test client for the app."""
    response = client.get('/api/')
    assert response.status_code == 200
