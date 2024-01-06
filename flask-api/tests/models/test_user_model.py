'''
    Defines user model tests.
'''
import pytest

from app.common.errors import ModelException
from app.models.user import User
from tests.helpers import add_user_to_db, remove_user_from_db


TEST_USERNAME = "userone"
TEST_EMAIL = "1@email.com"
TEST_PASSWORD = "thisisapassword"

def test_create():
    '''
        Tests that user creation works as expected.
    '''
    user = User.create(username=TEST_USERNAME, email=TEST_EMAIL)
    user_obj = user.to_obj()

    assert user_obj['username'] == TEST_USERNAME
    assert user_obj['email'] == TEST_EMAIL


@pytest.mark.usefixtures("app_ctx")
def test_password_check():
    '''
        Tests that user password verification works.
    '''
    user = add_user_to_db(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    assert user.verify_password(TEST_PASSWORD)
    assert not user.verify_password('notcorrect')

    remove_user_from_db(user)

    # Can't test other attributes of the user until they are saved into the db.


def test_no_attribute():
    '''
        Tests that user creation throws when no username or email is passed.
    '''
    with pytest.raises(ModelException):
        _user = User.create(email="testemail@email.com")
    with pytest.raises(ModelException):
        _user = User.create(username="testuser")
