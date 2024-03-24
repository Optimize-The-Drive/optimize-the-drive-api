'''
    SocketIO event defintions
'''

from flask import current_app
from flask_jwt_extended import get_jwt_identity, decode_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_socketio import emit
from jwt.exceptions import DecodeError

from app.extensions import socketio


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
        decode_token(socket_token)
        current_user = get_jwt_identity()

        return current_user is not None
    except (NoAuthorizationError, DecodeError):
        current_app.logger.info(
            "Invalid token found in websocket connect, disconnecting..."
        )
        return False


@socketio.on('disconnect')
def disconnect_socket():
    '''
        Handles the socket disconnect
    '''
    current_app.logger.info("Socket connection ended")


@socketio.on('generate_route')
def generate_route(json_data):
    """
        Method TBD.
    """
    current_app.logger.info(f"received {json_data}")

    # Call out to generator
    faux_response_data = {
        "points": [{"lat" : '1', "lon": '2'},{"lat" : '3', "lon": '4'}]
    }

    emit('generate_route_res', faux_response_data)
