''' Service for handling common JWT actions. '''

from datetime import datetime

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app.repos import jwt_repo
from app.models.jwt import JWTType, JWT
from app.common.errors import ServiceException


JWT_REFRESH_CLAIMS = 'refresh_token'

class JWTService:
    '''
        JWTService definition.

        attributes:
            jwt_repo - JWT Repository for db queries.
        
        methods:
            generate_access_refresh
            generate_access
            blacklist_tokens
            is_token_revoked
    '''
    _jwt_repo = jwt_repo

    def generate_access_refresh(self, identity: str = '') -> dict:
        '''
            Generates an access and refresh token. Injects the refresh token into the access
            token as an additional claim.

            ARGS:
                identity (str): Identity of the access token
            returns:
                dict { refresh, access } - The refresh and access token
        '''
        refresh_token = create_refresh_token(identity=identity)
        access_token = self.generate_access(refresh_token, identity)

        return {'refresh': refresh_token, 'access': access_token}

    def generate_access(self, refresh: str = '', identity: str = '') -> str:
        '''
            Generates an access token. Injects the refresh token into the access
            token as an additional claim.

            ARGS:
                refresh (str): Refresh token string. Injected into access token.
                identity (str): Identity of the access token.
            RETURNS:
                str - new access token.
        '''
        additional_claims = { JWT_REFRESH_CLAIMS: refresh }
        access_token = create_access_token(identity=identity, additional_claims=additional_claims)

        return access_token

    def blacklist_tokens(self, tokens: list) -> None:
        '''
            Adds tokens to the blacklist jwt database table.

            ARGS:
                token (list): Token to blacklist.
        '''

        jwts = []

        for token in tokens:
            try:
                jti = token["jti"]
                jwt_type = JWTType.ACCESS if token["type"] == 'access' else JWTType.REFRESH
                user_id = token['sub']
                expires = datetime.fromtimestamp(token["exp"])
            except KeyError as _error:
                raise ServiceException('Malformed token passed') from _error

            jwt = JWT.create(jti=jti, type=jwt_type, user_id=user_id, expires=expires)
            jwts.append(jwt)

        if len(jwts) > 0:
            self._jwt_repo.add(jwts)
            self._jwt_repo.commit()

    def is_token_revoked(self, jti: str) -> bool:
        '''
            Checks if a jti has been revoked before.

            ARGS:
                jti (str): The jti of the token.
            returns:
                Boolean - Whether the token has been revoked or not.
        '''
        token = self._jwt_repo.by_jti(jti)

        return token is not None
        