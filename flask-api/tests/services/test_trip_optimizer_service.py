'''
    Defines TripOptimizer Tests.
'''
import pytest
from app.services.trip_optimizer import TripOptimizerService, Mode


def test_set_points():
    '''
        Tests setting class points array.
    '''
    service = TripOptimizerService()
    testPoints = [
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
    ]

    service.set_points(testPoints)

    assert service._points == testPoints

def test_set_mode():
    '''
        Tests setting class mode.
    '''
    service = TripOptimizerService()
    testMode = Mode.ROUND_TRIP

    service.set_mode(testMode)

    assert service._mode == testMode

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
        {"lat":-83.12345, "lon":40.12345},
        {"lat":-83.12345, "lon":40.12345},
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

def test_generate():
    ''' 
        Tests Generation of OSRM request
    '''
    assert False