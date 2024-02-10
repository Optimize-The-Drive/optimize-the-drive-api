'''
    Houses the shared repositories.
'''

from app.repos.jwt import JWTRepo
from app.repos.user import UserRepo
from app.repos.trip import TripRepo


jwt_repo = JWTRepo()
user_repo = UserRepo()
trip_repo = TripRepo()
