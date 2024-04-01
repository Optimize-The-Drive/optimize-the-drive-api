'''Socket auth defintions'''

from flask import current_app
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import DecodeError, ExpiredSignatureError

from app.extensions import socketio
from app.repos import user_repo

@socketio.on('connect')
def connect_socket(auth):
    '''
        Handles the socket connection. Reject if invalid token is passed.
    '''
    socket_token = auth.get('token') if auth else None

    if not socket_token:
        current_app.logger.info(
            "No authorization token found in websocket connect, disconnecting..."
        )
        return False

    try:
        token = decode_token(socket_token)
        return validate_user(token['sub'])
    except (NoAuthorizationError, DecodeError, ExpiredSignatureError) as err:
        current_app.logger.info(
            f"Invalid token found in websocket connect, disconnecting...: {err}"
        )
        return False


@socketio.on('disconnect')
def disconnect_socket():
    '''
        Handles the socket disconnect
    '''
    current_app.logger.debug("Socket connection ended")


def validate_user(user_id):
    """
        Do a lookup on the websocket user in the db. Since I can't use
        Flask_jwt_extended's middleware to verify, I am manually checking.
        
        PARAMS:
            user_id (int) - the requesting user's id
        RETURN:
            boolean - whether the user is valid or not
    """
    return user_repo.by_id(user_id) is not None
