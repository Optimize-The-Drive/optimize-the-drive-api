'''
    Defines Trip Repo Tests.
'''

import pytest

from app.models.trip import Trip
from tests.helpers import add_user_to_db, trip_repo, remove_user_from_db


@pytest.mark.usefixtures("app_ctx")
def test_by_user_id():
    '''
        Tests that a Trip can be queried it's users
    '''
    user = add_user_to_db('user_test_trip', 'user_test_trip@email.com', 'testpassword')

    trip = Trip(name="trip_one", user_id=user.id)
    trip_two = Trip(name="trip_two", user_id=user.id)

    trip_repo.add([trip, trip_two])
    trip_repo.commit()

    trips = trip_repo.by_user_id(user.id)
    trips_none = trip_repo.by_user_id(123123123)

    assert len(trips) == 2
    assert trips[0].name == trip.name
    assert trips[1].name == trip_two.name
    assert len(trips_none) == 0

    remove_user_from_db(user)
