'''
    Defines user model tests.
'''
import pytest

from app.common.errors import ModelException
from app.models import User
from tests.helpers import add_user_to_db, remove_user_from_db

class TestUserModel:
    '''
        Tests for the user model.
    '''

    _test_username = "userone"
    _test_email = "1@email.com"
    _test_password = "thisisapassword"

    def test_create(self):
        '''
            Tests that user creation works as expected.
        '''
        user = User.create(username=self._test_username, email=self._test_email)
        user_obj = user.to_obj()

        assert user_obj['username'] == self._test_username
        assert user_obj['email'] == self._test_email

    @pytest.mark.usefixtures("app_ctx")
    def test_password_check(self):
        '''
            Tests that user password verification works.
        '''
        user = add_user_to_db(self._test_username, self._test_email, self._test_password)
        assert user.verify_password(self._test_password)
        assert not user.verify_password('notcorrect')

        remove_user_from_db(user)

        # Can't test other attributes of the user until they are saved into the db.

    def test_no_attribute(self):
        '''
            Tests that user creation throws when no username or email is passed.
        '''
        with pytest.raises(ModelException):
            _user = User.create(email="testemail@email.com")
        with pytest.raises(ModelException):
            _user = User.create(username="testuser")
