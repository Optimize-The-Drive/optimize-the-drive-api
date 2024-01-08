'''
    Common utility functions for the server.
'''

from flask import jsonify


def create_server_res(message: str) -> dict:
    '''
        Creates a generic message for the API response.
        
        ARGS:
            message (str): message to encapsulate.

        RETURNS:
            Dict { res: <message> } - The JSONified message.
    '''
    return jsonify({
        'res': message
    })
