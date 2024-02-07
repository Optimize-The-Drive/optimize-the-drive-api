''' Defines the user routes. '''

from flask import abort, current_app
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)

from app.common.utility import create_server_res
from app.common.logger import log_details
from app.repos import user_repo
from app.models.user import User
from app.schema.user import UserResponseSchema, UserRegisterSchema

user_routes = Blueprint("user", __name__, url_prefix="/user")


@user_routes.post('/register')
@user_routes.arguments(UserRegisterSchema)
@user_routes.response(201, UserResponseSchema)
def register_user(register_data):
    '''
        Registers a user with the API.

        RESPONSE:
            201, user
    '''
    username = register_data['username']
    password = register_data['password']
    email = register_data['email']

    user_by_email = user_repo.by_email(email)
    user_by_username = user_repo.by_username(username)

    if user_by_email:
        abort(409, description={'email': 'Email already taken.'})
    elif user_by_username:
        abort(409, description={'username': 'username already taken.'})

    new_user = User.create(username=username, email=email)
    new_user.set_password(password)

    user_repo.add(new_user)
    user_repo.commit()

    current_app.logger.info(log_details(f'User created: {new_user.id}'))

    return {'user': new_user}


@user_routes.get('/me')
@user_routes.response(200, UserResponseSchema)
@jwt_required()
def get_me():
    '''
        Returns the requesting user's information.
        
        RESPONSE:
            200, user
    '''
    user = get_current_user()

    if user:
        return {'user': user}

    abort(404, description='User not found.')


@user_routes.delete('/me')
@jwt_required()
def delete_me():
    '''
        Deletes the user making the request.
        
        RESPONSE:
            200, msg
    '''
    user = get_current_user()

    if user:
        user_repo.delete(user)
        user_repo.commit()
        current_app.logger.info(log_details('User self deleted.'))

        return create_server_res('User deleted successfully.', 200)

    abort(404, description='User not found.')
