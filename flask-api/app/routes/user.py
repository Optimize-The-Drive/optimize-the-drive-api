''' Defines the user routes. '''

from flask_smorest import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

from app.common.utility import create_server_res
from app.repos import user_repo


user_routes = Blueprint("user", __name__, url_prefix="/user")


@user_routes.delete('/me')
@jwt_required()
def delete_me():
    '''
        Deletes the user making the request.
        
        RETURNS 200, msg
    '''
    user_id = get_jwt_identity()
    user = user_repo.by_id(user_id)

    if user:
        user_repo.delete(user)
        user_repo.commit()
        return create_server_res('User deleted successfully.'), 200

    return create_server_res('User not found.'), 404
