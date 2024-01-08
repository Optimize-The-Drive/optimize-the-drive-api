''' Defines the user routes. '''

from flask import abort, request
from flask_smorest import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from sqlalchemy.exc import IntegrityError

from app.common.utility import create_server_res
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

    new_user = User.create(username=username, email=email)
    new_user.set_password(password)

    try:
        user_repo.add(new_user)
        user_repo.commit()
    except IntegrityError as e:
        print(e)
        abort(409, description='Username or email taken.')

    return new_user

@user_routes.get('/email_unique')
def email_unique():
    '''
        Checks if email is valid

        RESPONSE:
            200, boolean
    '''
    email_val = request.args.get('email', '')
    existing_user = user_repo.by_email(email_val)

    return create_server_res(existing_user is None), 200


@user_routes.get('/username_unique')
def username_unique():
    '''
        Checks if username is valid

        RESPONSE:
            200, boolean
    '''
    username_val = request.args.get('username', '')
    existing_user = user_repo.by_username(username_val)

    return create_server_res(existing_user is None), 200


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
        return create_server_res('User deleted successfully.'), 200

    abort(404, description='User not found.')
