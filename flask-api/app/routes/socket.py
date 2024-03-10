'''
    SocketIO event defintions
'''

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_socketio import emit
from jwt.exceptions import ExpiredSignatureError

from app.extensions import socketio


@socketio.on('connect')
def connect_socket(_auth):
    '''
        Handles the socket connection / upgrade.
    '''
    current_user = get_socket_jwt_identity()
    if not current_user:
        current_app.logger.info("Not authenticated for socket connection, disconnecting...")
        return False

    current_app.logger.info("Socket connection created")
    return True


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



def get_socket_jwt_identity():
    '''
        Returns the user making the socket request.
        
        RETURNS:
            User or None: The user 
    '''
    try:
        verify_jwt_in_request()
    except (NoAuthorizationError, ExpiredSignatureError):
        return None

    return get_jwt_identity()
