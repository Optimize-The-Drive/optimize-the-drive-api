'''
    Defines user model tests.
'''
import pytest

from app.common.errors import ModelException
from app.models import User


class TestUserModel:
    '''
        Tests for the user model.
    '''

    _test_username = "testuser"
    _test_email = "testemail@email.com"

    def test_create(self):
        '''
            Tests that user creation works as expected.
        '''
        user = User.create(username=self._test_username, email=self._test_email)
        user_obj = user.to_obj()

        assert user_obj['username'] == self._test_username
        assert user_obj['email'] == self._test_email

        # Can't test other attributes of the user until they are saved into the db.

    def test_no_attribute(self):
        '''
            Tests that user creation throws when no username or email is passed.
        '''
        with pytest.raises(ModelException):
            _user = User.create(email="testemail@email.com")
        with pytest.raises(ModelException):
            _user = User.create(username="testuser")
