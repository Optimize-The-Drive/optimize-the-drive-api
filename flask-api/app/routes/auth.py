''' Defines the session routes. '''

from flask import (
    jsonify, current_app, request, abort
)
from flask_smorest import Blueprint
from flask_jwt_extended import (
    set_refresh_cookies,
    decode_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.common.utility import create_server_res
from app.repos import user_repo
from app.schema.user import UserAuthSchema
from app.extensions import jwt
from app.services import jwt_service
from app.services.jwt import JWT_REFRESH_CLAIMS


auth_routes = Blueprint("auth", __name__, url_prefix="/auth")

@auth_routes.post('/login')
@auth_routes.arguments(UserAuthSchema)
def login(login_data):
    '''
        Handles user authentication. Returns an access token
        and sets a refresh token cookie.

        BODY:
            username
            password

        RESPONSE:
            access_token, 200
    '''
    username = login_data['username']
    password = login_data['password']

    user = user_repo.by_username(username)

    if user and user.verify_password(password):
        tokens = jwt_service.generate_access_refresh(user.id)

        response = jsonify(access_token=tokens['access'])
        set_refresh_cookies(response, tokens['refresh'])

        current_app.logger.info(f'User ({user.username}:${user.id}) logged in.')

        return response, 200

    abort(401, description="Username or password is incorrect.")


@auth_routes.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    '''
        Handles access token refreshing. Returns a new access token.

        COOKIE:
            REFRESH

        RESPONSE:
            access_token, 200
    '''
    refresh = request.cookies.get('refresh_token_cookie')
    current_user = get_jwt_identity()

    access_token = jwt_service.generate_access(refresh, current_user)

    return jsonify(access_token=access_token), 200


@auth_routes.post('/logout')
@jwt_required()
def logout():
    '''
        Handles user logout. Revokes both access and refresh tokens.

        HEADER:
            BEARER token

        RESPONSE:
            msg, 200
    '''
    access_token_decoded = get_jwt()
    refresh_token = access_token_decoded[JWT_REFRESH_CLAIMS]

    if not refresh_token:
        abort(422, description='Access token missing required claims')

    refresh_token_decoded = decode_token(refresh_token)

    jwt_service.blacklist_tokens([access_token_decoded, refresh_token_decoded])

    return create_server_res('Sucessfully logged out.'), 200


@jwt.user_lookup_loader
def user_lookup(_header, payload):
    '''
        Finds the owner of the token. Used in validating
        guarded routes.
    '''
    identity = payload[current_app.config["JWT_IDENTITY_CLAIM"]]
    return user_repo.by_id(identity)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_headers, jwt_payload):
    '''
        Checks to see if the token passed in the request has been
        blacklisted. Used in validating guarded routes.
    '''
    jti = jwt_payload['jti']

    return jti and jwt_service.is_token_revoked(jti)
