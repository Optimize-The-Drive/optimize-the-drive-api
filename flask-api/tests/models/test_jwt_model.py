'''
    Defines JWT model tests.
'''

from datetime import datetime
import pytest

from app.common.errors import ModelException
from app.models.jwt import JWTType, JWT


TEST_JTI = "thisisalongjti"
TEST_USER_ID = 11
TEST_JWT_TYPE = JWTType.ACCESS
TEST_DATE = datetime.now()


def test_create():
    '''
        Tests that JWT creation works as expected.
    '''
    jwt = JWT.create(
        jti=TEST_JTI, user_id=TEST_USER_ID,
        type=TEST_JWT_TYPE, expires=TEST_DATE
    )

    assert jwt.jti == TEST_JTI
    assert jwt.user_id == TEST_USER_ID
    assert jwt.type == TEST_JWT_TYPE
    assert jwt.expires.timestamp() == TEST_DATE.timestamp()


def test_no_attribute():
    '''
        Tests that JWT creation throws when attributes aren't passed.
    '''
    with pytest.raises(ModelException):
        _jwt = JWT.create(
            user_id=TEST_USER_ID,
            type=TEST_JWT_TYPE, expires=TEST_DATE
        )
    with pytest.raises(ModelException):
        _jwt = JWT.create(
            jti=TEST_JTI,
            type=TEST_JWT_TYPE, expires=TEST_DATE
        )
    with pytest.raises(ModelException):
        _jwt = JWT.create(
            jti=TEST_JTI, user_id=TEST_USER_ID,
            expires=TEST_DATE
        )
    with pytest.raises(ModelException):
        _jwt = JWT.create(
            jti=TEST_JTI, user_id=TEST_USER_ID,
            type=TEST_JWT_TYPE
        )
