'''
    Defines Trip Repo Tests.
'''

import pytest

from app.models.trip import Trip
from tests.helpers import trip_repo


@pytest.mark.usefixtures("app_ctx")
def test_by_user_id(db_user):
    '''
        Tests that a Trip can be queried its user's id
    '''
    trip = Trip(name="trip_one", user_id=db_user.id)
    trip_two = Trip(name="trip_two", user_id=db_user.id)

    trip_repo.add([trip, trip_two])
    trip_repo.commit()

    trips = trip_repo.by_user_id(db_user.id)
    trips_none = trip_repo.by_user_id(123123123)

    assert len(trips) == 2
    assert trips[0].name == trip.name
    assert trips[1].name == trip_two.name
    assert len(trips_none) == 0


@pytest.mark.usefixtures("app_ctx")
def test_by_id(db_user):
    '''
        Tests that a Trip can be queried by its id
    '''
    trip = Trip(name="trip_one", user_id=db_user.id)
    trip_repo.add(trip)
    trip_repo.commit()

    queried_trip = trip_repo.by_id(trip.id)

    assert trip.id == queried_trip.id
