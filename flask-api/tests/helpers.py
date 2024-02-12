'''
    Helper functions for tests.
'''

import json

from app.models.user import User
from app.repos.user import UserRepo
from app.repos.jwt import JWTRepo
from app.repos.trip import TripRepo
from app.services.jwt import JWTService


# Repos for tests
user_repo = UserRepo()
jwt_repo = JWTRepo()
trip_repo = TripRepo()

# Services for tests
jwt_service = JWTService()

def add_user_to_db(username: str, email: str, password: str):
    '''
        Adds a user to the database.

        ARGS:
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user
        RETURNS:
            User - the created user.
    '''
    user = User.create(username=username, email=email)
    user.set_password(password)
    user_repo.add(user)
    user_repo.commit()

    return user


def remove_user_from_db(user: User):
    '''
        Removes a user from the database.

        ARGS:
            User (user): The user to remove
    '''
    user_repo.delete(user)
    user_repo.commit()


def get_response_body(response) -> dict:
    '''
        Parses and returns the response body
        
        ARGS:
            response: Response
        
        Returns:
            response body - dict
    '''
    return json.loads(response.data.decode('utf-8'))
