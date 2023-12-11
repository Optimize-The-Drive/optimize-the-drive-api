''' Defines the session routes. '''
from datetime import datetime

from flask import jsonify, current_app
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_refresh_cookies,
    decode_token
)

from app.schema.auth import LoginSchema
from app.repos.user import UserRepo
from app.common.utility import create_server_res
from app.models import JWT
from app.models.jwt import JWTType
from database import db 

auth_routes = Blueprint("auth", __name__, url_prefix="/auth")

user_repo = UserRepo()

@auth_routes.post('/login')
@auth_routes.arguments(LoginSchema)
def login(login_data):
    username = login_data['username']
    password = login_data['password']

    user = user_repo.by_username(username)

    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify(access_token=access_token)
        set_refresh_cookies(response, refresh_token)
        add_jwt_to_db(access_token)
        add_jwt_to_db(refresh_token)
        return response, 200

    return create_server_res('Unauthorized.'), 401

# @auth_routes.get('/logout')
# def logout():
#     '''
#         TODO: MAKE ACTUAL REQUEST A POST REQ
#     '''
#     return {'res': 'you hit the logout!'}


# TODO MOVE FCN SOMEWHERE ELSE
def add_jwt_to_db(token: str):
    decoded_token = decode_token(token)
    jti = decoded_token["jti"]
    type = JWTType.ACCESS if decoded_token["type"] == 'access' else JWTType.REFRESH
    user_id = decoded_token[current_app.config["JWT_IDENTITY_CLAIM"]]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    jwt = JWT.create(jti=jti, type=type, user_id=user_id, expires=expires)
    
    db.session.add(jwt)
    db.session.commit()