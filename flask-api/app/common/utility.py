'''
    Common utility functions for the server.
'''

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
