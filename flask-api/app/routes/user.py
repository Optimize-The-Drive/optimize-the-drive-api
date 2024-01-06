''' Defines the user routes. '''

from flask_smorest import Blueprint

from app.common.utility import create_server_res

user_routes = Blueprint("user", __name__, url_prefix="/user")

@user_routes.get('/example')
def get_example():
    '''
        This is an example route that will be removed.
    '''
    return create_server_res('example user route'), 200
