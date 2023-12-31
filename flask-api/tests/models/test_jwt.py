'''
    Defines JWT model tests.
'''

from datetime import datetime
import pytest

from app.common.errors import ModelException
from app.models import JWT
from app.models.jwt import JWTType


class TestJWTModel:
    '''
        Tests for the JWT model.
    '''

    _test_jti = "thisisalongjti"
    _test_user_id = 11
    _test_jwt_type = JWTType.ACCESS
    _test_date = datetime.now()

    def test_create(self):
        '''
            Tests that JWT creation works as expected.
        '''
        jwt = JWT.create(
            jti=self._test_jti, user_id=self._test_user_id,
            type=self._test_jwt_type, expires=self._test_date
        )

        assert jwt.jti == self._test_jti
        assert jwt.user_id == self._test_user_id
        assert jwt.type == self._test_jwt_type
        assert jwt.expires.timestamp() == self._test_date.timestamp()

    def test_no_attribute(self):
        '''
            Tests that JWT creation throws when attributes aren't passed.
        '''
        with pytest.raises(ModelException):
            _jwt = JWT.create(
                user_id=self._test_user_id,
                type=self._test_jwt_type, expires=self._test_date
            )
        with pytest.raises(ModelException):
            _jwt = JWT.create(
                jti=self._test_jti,
                type=self._test_jwt_type, expires=self._test_date
            )
        with pytest.raises(ModelException):
            _jwt = JWT.create(
                jti=self._test_jti, user_id=self._test_user_id,
                expires=self._test_date
            )
        with pytest.raises(ModelException):
            _jwt = JWT.create(
                jti=self._test_jti, user_id=self._test_user_id,
                type=self._test_jwt_type
            )
