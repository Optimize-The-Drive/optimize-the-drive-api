'''
    Helper functions for tests.
'''

import json
from socketio import Client

from app.models import User, Trip
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


def add_trip_to_db(name, user_id, description=""):
    '''
        Adds a trip to the database.

        ARGS:
            name (str): The name  of the trip
            user_id (int): The id of the trip's user
            description (str): The description of the trip
        RETURNS:
            User - the created trip.
    '''
    trip = Trip.create(name=name, user_id=user_id, description=description)
    trip_repo.add(trip)
    trip_repo.commit()

    return trip


def remove_trip_from_db(trip: Trip):
    '''
        Removes a trip from the database.

        ARGS:
            Trip (trip): The trip to remove
    '''
    trip_repo.delete(trip)
    trip_repo.commit()


def get_response_body(response) -> dict:
    '''
        Parses and returns the response body
        
        ARGS:
            response: Response
        
        Returns:
            response body - dict
    '''
    return json.loads(response.data.decode('utf-8'))


sio = Client(logger=True, engineio_logger=True)
