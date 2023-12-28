''' Service for handling common JWT actions. '''

from datetime import datetime

from flask import current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app.repos.jwt import JWTRepo
from app.models.jwt import JWTType, JWT
from app.common.errors import ServiceException

class JWTService:
    '''
        JWTService definition.

        attributes:
            jwt_repo
        
        methods:
            generate_access_refresh
            generate_access
            blacklist_token
            is_token_revoked
    '''
    jwt_repo = JWTRepo()
    def generate_access_refresh(self, identity: str = '') -> dict:
        refresh_token = create_refresh_token(identity=identity)
        access_token = self.generate_access(refresh_token, identity)

        return {'refresh': refresh_token, 'access': access_token}
    
    def generate_access(self, refresh: str = '', identity: str = '') -> str:
        additional_claims = { 'refresh_token': refresh }
        access_token = create_access_token(identity=identity, additional_claims=additional_claims)

        return access_token
    
    def blacklist_token(self, token: dict) -> None:
        try:
            jti = token["jti"]
            jwt_type = JWTType.ACCESS if token["type"] == 'access' else JWTType.REFRESH
            user_id = token[current_app.config["JWT_IDENTITY_CLAIM"]]
            expires = datetime.fromtimestamp(token["exp"])
        except KeyError as _error:
            raise ServiceException('Malformed token passed') from _error
       
        jwt = JWT.create(jti=jti, type=jwt_type, user_id=user_id, expires=expires)
        self.jwt_repo.add_one(jwt)
        self.jwt_repo.commit()

    def is_token_revoked(self, payload) -> bool:
        jti = payload["jti"]
        token = self.jwt_repo.by_jti(jti)

        return token is not None
        