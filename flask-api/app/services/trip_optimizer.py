'''Service for handling OSRM interaction '''
from enum import Enum
from flask import current_app
import requests

from app.common.errors import ServiceException


class Mode(Enum):
    ''' 
        Enum defining the Mode of the trip
    '''
    FIRST_LAST = "first_last"
    ROUND_TRIP = "round_trip"

class TripOptimizerService:
    ''' 
        TripOptimizerService definition.

        attributes:
            _points - 
            _mode - 

        methods:
            set_points
            set_mode
            _generate_url
            generate
    
    '''
    _points = None
    _mode = Mode.FIRST_LAST
    _base_url = ""

    def __init__(self):
        self._base_url = current_app.config['BASE_OSRM_URL']

    def set_points(self, points):
        ''' 
            Sets the points array to be the given points

            ARGS:
                var (type): desc
            Returns:
                None
        '''
        self._points = points

    def set_mode(self, mode):
        ''' 
            Sets the points array to be the given points

            ARGS:
                var (type): desc
            Returns:
                None
        '''
        self._mode = mode

    def _generate_url(self):
        ''' 
            Uses the base url, points, and mode to generate the request URL.

            Returns:
                string: The generated url 
        '''
        url = self._base_url
        url += ";".join([f"{p['lon']},{p['lat']}" for p in self._points])

        if self._mode == Mode.FIRST_LAST:
            url += "?source=first&destination=last"

        return url

    def generate(self):
        ''' 
            Sets the points array to be the given points

            ARGS:
                var (type): desc
            Returns:
                None
        '''
        url = self._generate_url()
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            raise ServiceException(
                f"Recived non 200 response from OSRM service: {response.status_code}")
        try:
            response_json = response.json()
            waypoints = response_json["waypoints"]
            waypoints.sort(key=lambda coord : coord["waypoint_index"])

            sorted_points = [{"lon":w["location"][0], "lat":w["location"][1]} for w in waypoints]
        except KeyError as error:
            raise ServiceException("Unable to parse response data") from error

        return sorted_points
