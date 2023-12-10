''' Defines the session routes. '''

from flask import  request
from flask_smorest import Blueprint

from app.schema.auth import LoginSchema
from app.repos.user import UserRepo
from app.common.utility import create_server_res

auth_routes = Blueprint("auth", __name__, url_prefix="/auth")

user_repo = UserRepo()

@auth_routes.post('/login')
@auth_routes.arguments(LoginSchema)
def login(login_data):

        username = login_data['username']
        password = login_data['password']

        user = user_repo.by_username(username)
        
        if user and user.verify_password(password):
            return 'logged in bb', 200
    
        # validate_errors = login_schema.validate(request.json)
        # print(validate_errors, flush=True)
        return create_server_res('Unauthorized.'), 401

# @auth_routes.post('/login')
# @auth_routes.arguments(LoginSchema)
# def login(user_data):
#     # print(user_data, flush=True)
#     return {'res': 'asdf'}, 200
    
# @auth_routes.get('/logout')
# def logout():
#     '''
#         TODO: MAKE ACTUAL REQUEST A POST REQ
#     '''
#     return {'res': 'you hit the logout!'}
