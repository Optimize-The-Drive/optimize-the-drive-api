'''
    Defines TripOptimizer Tests.
'''
import pytest
import requests_mock

from app.common.errors import ServiceException, SchemaException
from app.services.trip_optimizer import TripOptimizerService
from app.schema.trip import TripMode, TripOptimizeSchema


test_points = [
    {"lon":-83.12345, "lat":40.12345},
    {"lon":-83.12345, "lat":40.12345},
    {"lon":-83.12345, "lat":40.12345},
]
test_mode = TripMode.FIRST_LAST

@pytest.mark.usefixtures("app_ctx")
def test_set_points(db_trip):
    '''
        Tests set_trip
    '''
    service = TripOptimizerService()
    test_id = db_trip.id

    test_trip = {"points": test_points, "mode": test_mode, "trip_id": test_id}

    service.set_trip(test_trip)

    assert service._points == test_points
    assert service._mode == test_mode
    assert service._trip_ref is not None


@pytest.mark.usefixtures("app_ctx")
def test_set_points_throws(db_trip):
    '''
        Tests that the set_trip function throws errors.
    '''
    service = TripOptimizerService()
    test_id = db_trip.id
    test_trip = {"points": [], "mode": 123, "trip_id": test_id}
    test_trip1 = {"points": test_points, "mode": TripMode.FIRST_LAST, "trip_id": -1}

    # less than 3 points, mode incorrect
    with pytest.raises(ServiceException):
        service.set_trip(test_trip)

    # Invalid user
    with pytest.raises(ServiceException):
        service.set_trip(test_trip1)


@pytest.mark.usefixtures("app_ctx")
def test_generate_url(db_trip):
    '''
        Tests Generating URL
    '''
    test_url_first_last = \
        "http://osrm:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345;-83.12345,40.12345?source=first&destination=last"
    test_url_round_trip =\
        "http://osrm:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345;-83.12345,40.12345"

    service = TripOptimizerService()

    #Set Test Points
    test_trip = {
        "points": test_points,
        "mode": test_mode,
        "trip_id": db_trip.id
    }

    service.set_trip(test_trip)

    first_last_trip_url = service._generate_url()
    assert test_url_first_last == first_last_trip_url

    test_trip["mode"] = TripMode.ROUND_TRIP
    service.set_trip(test_trip)

    round_trip_url = service._generate_url()
    assert test_url_round_trip == round_trip_url


@pytest.mark.usefixtures("app_ctx")
def test_generate_throws():
    """
        Tests that generate throws if no trip has been loaded.
    """
    service = TripOptimizerService()

    with pytest.raises(ServiceException):
        service.generate()


@pytest.mark.usefixtures("app_ctx")
def test_generate(requests_mock, db_trip):
    ''' 
        Tests generate
    '''
    test_url_first_last = "http://osrm:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345;-83.12345,40.12345?source=first&destination=last"
    service = TripOptimizerService()

    test_trip = {
        "points": test_points,
        "mode": test_mode,
        "trip_id": db_trip.id
    }

    service.set_trip(test_trip)
    requests_mock.get(test_url_first_last, json = {"code":"Ok","trips":[{"geometry":"eq{sFdajzN??????","legs":[{"steps":[],"summary":"","weight":0,"duration":0,"distance":0},{"steps":[],"summary":"","weight":0,"duration":0,"distance":0},{"steps":[],"summary":"","weight":0,"duration":0,"distance":0}],"weight_name":"routability","weight":0,"duration":0,"distance":0}],"waypoints":[{"waypoint_index":0,"trips_index":0,"hint":"4l01gKn3BIAjAAAADQAAAA8AAAAbAAAAnTkbQovoZUG_KoZBQWvyQSMAAAANAAAADwAAABsAAAAgAgAAnqIL-1s7ZAIGowv7OjxkAgEAHxIbWzSG","distance":26.300259889,"name":"Brandonway Drive","location":[-83.12345,40.12345]},{"waypoint_index":1,"trips_index":0,"hint":"4l01gKn3BIAjAAAADQAAAA8AAAAbAAAAnTkbQovoZUG_KoZBQWvyQSMAAAANAAAADwAAABsAAAAgAgAAnqIL-1s7ZAIGowv7OjxkAgEAHxIbWzSG","distance":26.300259889,"name":"Brandonway Drive","location":[-83.12345,40.12345]},{"waypoint_index":2,"trips_index":0,"hint":"4l01gKn3BIAjAAAADQAAAA8AAAAbAAAAnTkbQovoZUG_KoZBQWvyQSMAAAANAAAADwAAABsAAAAgAgAAnqIL-1s7ZAIGowv7OjxkAgEAHxIbWzSG","distance":26.300259889,"name":"Brandonway Drive","location":[-83.12345,40.12345]}]})

    assert [{"lon":-83.12345, "lat":40.12345},
            {"lon":-83.12345, "lat":40.12345},
            {"lon":-83.12345, "lat":40.12345}] == service.generate()

    trip_points = db_trip.get_points()

    assert len(trip_points["points"]) == 3
    assert trip_points["mode"] == test_mode
    