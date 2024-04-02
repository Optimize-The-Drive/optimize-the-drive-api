'''
    Common utility functions for the server.
'''

from enum import IntEnum

from flask import jsonify


def create_server_res(message: str, code: int) -> dict:
    '''
        Creates a generic message for the API response.
        
        ARGS:
            message (str): message to encapsulate.
            code (int): HTTP Status code.

        RETURNS:
            Dict { msg: <message> }, <code> - The JSONified message.
    '''
    return jsonify({
        'msg': message
    }), code



##### Websocket stuff ######
class SocketStatus(IntEnum):
    """
        Status of the response for a socketio request.
    """
    SUCCESS = 0
    ERROR = 1


def create_socket_res(message, status: SocketStatus) -> dict:
    '''
        Creates a generic message for a SocketIO response

        ARGS:
            message (str): message to encapsulate.
            status (int): Status.
            
        RETURNS:
            Dict { status: <status>, msg: <message>} - The constructed message
    '''
    return {
        "status": status,
        "msg": message
    }
