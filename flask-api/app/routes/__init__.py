'''
    All routes are assigned to the base API blueprint in
    this file.
'''
from flask import Blueprint, current_app

from app.common.utility import create_server_res
from app.routes.auth import auth_routes
from app.routes.user import user_routes


api_routes = Blueprint("api", __name__, url_prefix="/api")
api_routes.register_blueprint(auth_routes)
api_routes.register_blueprint(user_routes)

@api_routes.get('/')
def index():
    '''
        Root API ROUTE

        RESPONSE:
            msg, 200
    '''
    return create_server_res('Optimize The Drive API'), 200
