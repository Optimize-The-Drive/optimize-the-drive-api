import pytest
from database import db
from app.models import User
class Tests:
    def test_home_route(self, client):
        """A test client for the app."""
        response = client.get('/api/')
        assert response.status_code == 200

    @pytest.mark.usefixtures("app_ctx")
    def test_db(self, client):
        '''
            TODO remove. POC that db interactions work with tests
        '''
        assert db.session.query(User).where(User.username == 'testuser').one() is not None, 'the test user exists'