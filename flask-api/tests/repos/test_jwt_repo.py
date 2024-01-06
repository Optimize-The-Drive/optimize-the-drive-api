'''
    Defines JWT Repo Tests.
'''

from datetime import datetime
import pytest

from app.models.jwt import JWTType, JWT
from app.repos.jwt import JWTRepo

from tests.helpers import add_user_to_db, remove_user_from_db


repo = JWTRepo()

@pytest.mark.usefixtures("app_ctx")
def test_by_jti():
    '''
        Tests that a JWT can be queried by it's JTI.
    '''
    user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
    jwt = JWT.create(jti='test_jti', type=JWTType.ACCESS, user_id=user.id, expires=datetime.now())

    repo.add(jwt)
    repo.commit()

    queried_jwt = repo.by_jti(jwt.jti)

    assert queried_jwt and jwt.jti == queried_jwt.jti

    remove_user_from_db(user)
