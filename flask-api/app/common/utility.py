'''
    Common utility functions for the server.
'''

from flask import jsonify


# RESPONSES

# Errors
# potential requests

# {
#     status: "success|error",
#     data: {
#         results: [],
#         page: int or null
#         count: int or null
#     },
#     data: {
#         item: {}
#     },
#     messages: ""
# }



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


# class ResponseType:
#     SUCCESS = 'success'
#     ERROR = 'errror'

# class ResponseBuilder:
#     _status: ResponseType = None
#     _message: dict = None
#     _data: dict = None

#     def __init__(self, status: ResponseType):
#         self._status = status

#     def set_data(self, data):
#         self.data = data
#         return data
    
#     def set_data(self, data)
#     def build(self):
#         return jsonify({
#             'status': self.status,
#             data: 
#         })
    


