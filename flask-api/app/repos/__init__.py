'''
    Houses the shared repositories.
'''

from app.repos.jwt import JWTRepo
from app.repos.user import UserRepo

jwt_repo = JWTRepo()
user_repo = UserRepo()
