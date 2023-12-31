'''
    All routes are assigned to the base API blueprint in
    this file.
'''
from flask import Blueprint, jsonify
from app.common.utility import create_server_res
from app.routes.auth import auth_routes


api_routes = Blueprint("api", __name__, url_prefix="/api")
api_routes.register_blueprint(auth_routes)

@api_routes.get('/')
def index():
    '''
        Root API ROUTE

        RESPONSE:
            msg, 200
    '''
    return create_server_res('Optimize The Drive API'), 200
