'''
    Define socket trip tests.
'''

from unittest.mock import patch, MagicMock
import pytest
import requests

from app.schema.trip import TripMode
from app.common.utility import SocketStatus

CHANNEL = 'generate_trip'

@pytest.mark.usefixtures("app_ctx")
def test_trip_optimize_invalid(auth_sio_client):
    '''
        Test that trip optimize message sends back errors
        when invalid data is passed.
    '''

    # Note: All validation is tested along with the
    # test_trip_optimizer service, so only doing one here
    invalid_trip = {
        "trip_id": -1,
        "points": [],
        "mode": -121121
    }

    auth_sio_client.emit(CHANNEL, invalid_trip)
    received = auth_sio_client.get_received()

    assert received[0]['args'][0]["status"] == SocketStatus.ERROR


@pytest.mark.usefixtures("app_ctx")
def test_trip_optimize_osrm_non_200(auth_sio_client, db_trip):
    '''
        Test that trip optimize message sends back errors
        when the osrm server returns non-200 codes.
    '''

    valid_trip = {
        "trip_id": db_trip.id,
        "points": [
            {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}
        ],
        "mode": TripMode.FIRST_LAST
    }

    mock_response = MagicMock()
    mock_response.status_code = 500
    with patch("requests.get", return_value=mock_response):
        auth_sio_client.emit(CHANNEL, valid_trip)
        received = auth_sio_client.get_received()

        assert received[0]['args'][0]["status"] == SocketStatus.ERROR


@pytest.mark.usefixtures("app_ctx")
def test_trip_optimize_osrm_timeout(auth_sio_client, db_trip):
    '''
        Test that trip optimize message sends back errors
        when osrm service calls timeout
    '''
    valid_trip = {
        "trip_id": db_trip.id,
        "points": [
            {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}
        ],
        "mode": TripMode.FIRST_LAST
    }

    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        auth_sio_client.emit(CHANNEL, valid_trip)
        received = auth_sio_client.get_received()

        assert received[0]['args'][0]["status"] == SocketStatus.ERROR


@pytest.mark.usefixtures("app_ctx")
def test_trip_optimize_works(auth_sio_client, db_trip):
    '''
        Test that trip optimize message sends back success.
    '''
    valid_trip = {
        "trip_id": db_trip.id,
        "points": [
            {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}, {"lat": 1, "lon": 1}
        ],
        "mode": TripMode.FIRST_LAST
    }

    mock_osrm_res = {
        "waypoints": [
            {"waypoint_index": 0, "trips_index": 0, "hint": "hint1", "distance": 26.3, "name": "", "location": [1, 1]},
            {"waypoint_index": 1, "trips_index": 0, "hint": "hint2", "distance": 26.3, "name": "", "location": [1, 1]},
            {"waypoint_index": 2, "trips_index": 0, "hint": "hint3", "distance": 26.3, "name": "", "location": [1, 1]}
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = mock_osrm_res
    mock_response.status_code = 200

    with patch("requests.get", return_value=mock_response):
        mock_response = MagicMock()
        mock_response.json.return_value = mock_osrm_res
        mock_response.status_code = 200

        auth_sio_client.emit(CHANNEL, valid_trip)
        received = auth_sio_client.get_received()

        assert received[0]['args'][0]["status"] == SocketStatus.SUCCESS
