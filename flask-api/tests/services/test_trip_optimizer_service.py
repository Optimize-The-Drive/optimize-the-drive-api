'''
    Defines TripOptimizer Tests.
'''
import pytest
import requests_mock
from app.services.trip_optimizer import TripOptimizerService, Mode

@pytest.mark.usefixtures("app_ctx")
def test_set_points():
    '''
        Tests setting class points array.
    '''
    service = TripOptimizerService()
    test_points = [
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
    ]

    service.set_points(test_points)

    assert service._points == test_points

@pytest.mark.usefixtures("app_ctx")
def test_set_mode():
    '''
        Tests setting class mode.
    '''
    service = TripOptimizerService()
    test_mode = Mode.ROUND_TRIP

    service.set_mode(test_mode)

    assert service._mode == test_mode

@pytest.mark.usefixtures("app_ctx")
def test_generate_url():
    '''
        Tests Generating URL
    '''
    test_url_first_last = "http://localhost:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345?source=first&destination=last"
    test_url_round_trip = "http://localhost:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345"

    service = TripOptimizerService()

    #Set Test Points
    test_points = [
        {"lon":-83.12345, "lat":40.12345},
        {"lon":-83.12345, "lat":40.12345},
    ]
    service.set_points(test_points)

    #Set Test Mode
    test_mode = Mode.ROUND_TRIP
    service.set_mode(test_mode)

    round_trip_url = service._generate_url()

    assert test_url_round_trip == round_trip_url

    test_mode = Mode.FIRST_LAST
    service.set_mode(test_mode)

    first_last_trip_url = service._generate_url()

    assert test_url_first_last == first_last_trip_url

@pytest.mark.usefixtures("app_ctx")
def test_generate(requests_mock):
    ''' 
        Tests Generation of OSRM request
    '''
    test_url_first_last = "http://localhost:5050/trip/v1/driving/-83.12345,40.12345;-83.12345,40.12345?source=first&destination=last"
 
    service = TripOptimizerService()

    #Set Test Points
    test_points = [
        {"lon":-83.12345, "lat":40.12345},
        {"lon":-75.12345, "lat":35.12345},
    ]
    service.set_points(test_points)

    #Set Test Mode
    test_mode = Mode.FIRST_LAST
    service.set_mode(test_mode)

    requests_mock.get(test_url_first_last, json = {"code":"Ok","trips":[{"geometry":"eq{sFdajzN????","legs":[{"steps":[],"summary":"","weight":0,"duration":0,"distance":0},{"steps":[],"summary":"","weight":0,"duration":0,"distance":0}],"weight_name":"routability","weight":0,"duration":0,"distance":0}],"waypoints":[{"waypoint_index":1,"trips_index":0,"hint":"0cE1gOwBBYAjAAAADQAAAA8AAAAbAAAAnTkbQovoZUG_KoZBQWvyQSMAAAANAAAADwAAABsAAAAjAgAAnqIL-1s7ZAIGowv7OjxkAgEAHxLo1vtD","distance":26.300259889,"name":"Brandonway Drive","location":[-83.12345,40.12345]},{"waypoint_index":0,"trips_index":0,"hint":"0cE1gOwBBYAjAAAADQAAAA8AAAAbAAAAnTkbQovoZUG_KoZBQWvyQSMAAAANAAAADwAAABsAAAAjAgAAnqIL-1s7ZAIGowv7OjxkAgEAHxLo1vtD","distance":26.300259889,"name":"Brandonway Drive","location":[-75.12345,35.12345]}]})

    assert [{"lon":-75.12345, "lat":35.12345},
            {"lon":-83.12345, "lat":40.12345}] == service.generate()
    