'''
    Defines trip model tests.
'''
import pytest

from app.models.trip import Trip
from app.common.errors import ModelException


TRIP_NAME = 'tripOne'
TRIP_POINTS = [1,2]
USER_ID = 11

def test_create():
    '''
        Tests that trip model creation works as expected.
    '''
    trip = Trip.create(name=TRIP_NAME, user_id=USER_ID)

    assert trip.name == TRIP_NAME
    assert trip.user_id == USER_ID


def test_set_points():
    '''
        Tests that setting trip model points works as expected.
    '''
    trip = Trip.create(name=TRIP_NAME, user_id=USER_ID)
    trip.set_points(TRIP_POINTS)

    assert trip.points['points'] == TRIP_POINTS


def test_no_attribute():
    '''
        Tests that trip creation throws when no name or user_id is passed
    '''
    with pytest.raises(ModelException):
        _user = Trip.create(name=TRIP_NAME)
    with pytest.raises(ModelException):
        _user = Trip.create(user_id=USER_ID)
