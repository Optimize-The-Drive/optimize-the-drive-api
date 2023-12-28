'''
    Common utility functions for the server.
'''

from flask import jsonify

def create_server_res(message: str) -> dict:
    '''
        Creates a generic message for the API response.
        
        arguments:
            message: Str
        returns: Dict in format { msg: <message> }
    '''
    return jsonify({
        'msg': message
    })