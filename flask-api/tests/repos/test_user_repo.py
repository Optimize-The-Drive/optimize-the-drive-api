'''
    Defines User Repo Tests.
'''

import pytest

from tests.helpers import user_repo

@pytest.mark.usefixtures("app_ctx")
def test_by_username_and_id(db_user):
    '''
        Tests that a User can be queried by its username and id.
    '''
    queried_user = user_repo.by_username(db_user.username)
    queried_user_one = user_repo.by_id(db_user.id)
    queried_user_two = user_repo.by_email(db_user.email)

    assert (
        queried_user.username == db_user.username and
        queried_user_one.username == db_user.username and
        queried_user_two.username == db_user.username
    )
