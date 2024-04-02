'''
    Defines JWT Service Tests.
'''

import pytest

from flask_jwt_extended import decode_token

from tests.helpers import jwt_service


@pytest.mark.usefixtures("app_ctx")
def test_access_refresh_create(db_user):
    '''
        Tests access and refresh token creation.
    '''
    tokens = jwt_service.generate_access_refresh(db_user.id)

    assert tokens.get('access') and tokens.get('refresh')


@pytest.mark.usefixtures("app_ctx")
def test_access_create(db_user):
    '''
        Tests access token creation.
    '''
    tokens = jwt_service.generate_access_refresh(db_user.id)
    access = jwt_service.generate_access(tokens['refresh'], db_user.id)

    assert access


@pytest.mark.usefixtures("app_ctx")
def test_token_blacklist(db_user):
    '''
        Tests token blacklisting.
    '''
    tokens = jwt_service.generate_access_refresh(db_user.id)

    decoded_access = decode_token(tokens['access'])
    decoded_refresh = decode_token(tokens['refresh'])

    assert not jwt_service.is_token_revoked(decoded_refresh['jti'])
    assert not jwt_service.is_token_revoked(decoded_access['jti'])

    jwt_service.blacklist_tokens([decoded_access, decoded_refresh])

    assert jwt_service.is_token_revoked(decoded_access['jti'])
    assert jwt_service.is_token_revoked(decoded_refresh['jti'])
