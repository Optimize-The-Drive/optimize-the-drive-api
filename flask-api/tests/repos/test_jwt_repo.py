'''
    Defines JWT Repo Tests.
'''

from datetime import datetime
import pytest

from app.models.jwt import JWTType, JWT
from tests.helpers import jwt_repo

@pytest.mark.usefixtures("app_ctx")
def test_by_jti(db_user):
    '''
        Tests that a JWT can be queried by it's JTI.
    '''
    jwt = JWT.create(
        jti='test_jti', type=JWTType.ACCESS, user_id=db_user.id, expires=datetime.now()
    )

    jwt_repo.add(jwt)
    jwt_repo.commit()

    queried_jwt = jwt_repo.by_jti(jwt.jti)

    assert queried_jwt and jwt.jti == queried_jwt.jti
