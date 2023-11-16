"""Test Script for app.py"""
from app import app
def test_home_route():
    """tests if the api retruens a 200 code and the correct text
    """
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"<h1>Hello from our flask server!</h1>" in response.data
test_home_route()
