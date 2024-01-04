'''
    Defines JWT Service Tests.
'''

import pytest

from flask_jwt_extended import decode_token

from app.services.jwt import JWTService
from tests.helpers import add_user_to_db, remove_user_from_db


service = JWTService()

@pytest.mark.usefixtures("app_ctx")
def test_access_refresh_create():
    '''
        Tests access and refresh token creation.
    '''
    user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
    tokens = service.generate_access_refresh(user.id)

    assert tokens.get('access') and tokens.get('refresh')

    remove_user_from_db(user)


@pytest.mark.usefixtures("app_ctx")
def test_access_create():
    '''
        Tests access token creation.
    '''
    user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
    tokens = service.generate_access_refresh(user.id)

    access = service.generate_access(tokens['refresh'], user.id)

    assert access

    remove_user_from_db(user)


@pytest.mark.usefixtures("app_ctx")
def test_token_blacklist():
    '''
        Tests token blacklisting.
    '''
    user = add_user_to_db('usertwo', '21@email.com', 'testpassword')
    tokens = service.generate_access_refresh(user.id)

    decoded_access = decode_token(tokens['access'])
    decoded_refresh = decode_token(tokens['refresh'])

    service.blacklist_token(decoded_access)

    assert service.is_token_revoked(decoded_access['jti'])
    assert not service.is_token_revoked(decoded_refresh['jti'])
