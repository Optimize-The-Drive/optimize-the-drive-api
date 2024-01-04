'''
    Defines User Repo Tests.
'''

import pytest

from app.models.user import User
from app.repos.user import UserRepo
from tests.helpers import remove_user_from_db


repo = UserRepo()

@pytest.mark.usefixtures("app_ctx")
def test_by_username_and_id():
    '''
        Tests that a User can be queried by its username and id.
    '''

    user = User.create(username='test_user', email='test@email.com')
    user.set_password('test_password')

    repo.add(user)
    repo.commit()

    queried_user = repo.by_username(user.username)
    queried_user_one = repo.by_id(user.id)

    assert queried_user.username == user.username and queried_user_one.username == user.username

    remove_user_from_db(user)
