'''Service for handling OSRM interaction '''
from json import JSONDecodeError
import requests

from flask import current_app

from app.common.errors import ServiceException, SchemaException, ModelException
from app.models import Trip
from app.schema.trip import TripOptimizeSchema, TripMode
from app.repos import trip_repo

class TripOptimizerService:
    ''' 
        TripOptimizerService definition. Loads the referenced
        trip from the DB. calls the optimizer service on the requested
        points and saves to the database.

        methods:
            set_trip
            generate
    
    '''
    _points = []
    _trip_ref: Trip = None
    _mode = TripMode.FIRST_LAST
    _base_url = ""
    _trip_repo = trip_repo

    def __init__(self):
        self._base_url = current_app.config['BASE_OSRM_URL']

    def set_trip(self, trip):
        '''
            Sets the trip to optimize.
            
            ARGS:
                trip (Trip): The trip to optimize
            
            THROWS:
                SchemaException - If trip is not formatted correctly.
                ServiceException - If trip is not found.
        '''
        trip_schema = TripOptimizeSchema()

        try:
            trip = trip_schema.load(trip)
        except SchemaException as error:
            raise ServiceException(f"Unable to decode trip: {error}") from error

        trip_id = trip["trip_id"]
        self._trip_ref = self._trip_repo.by_id(trip_id)

        if not self._trip_ref:
            raise ServiceException("Trip not found.")

        self._points = trip["points"]
        self._mode = trip["mode"]

    def generate(self):
        ''' 
            Sets the points array to be the given points.

            Returns:
                List: The Parsed and sorted List of Dictionaries containing Lon and Lat of points.
        '''
        if not self._trip_ref:
            raise ServiceException("Trip not found.")

        url = self._generate_url()

        try:
            response = requests.get(url, timeout=60)
        except Exception as error:
            raise ServiceException(
                f"Unable to make a request to the Optimizer service: {error}"
            ) from error

        if response.status_code != 200:
            raise ServiceException(
                f"Recived non 200 response from OSRM service: {response.status_code}")

        sorted_points = self._parse_osrm_result(response)
        self._save_points(sorted_points)

        return sorted_points

    def _generate_url(self):
        ''' 
            Uses the base url, points, and mode to generate the request URL.

            Returns:
                string: The generated url 
        '''
        url = self._base_url
        url += ";".join([f"{p['lon']},{p['lat']}" for p in self._points])

        if self._mode == TripMode.FIRST_LAST:
            url += "?source=first&destination=last"

        return url

    def _parse_osrm_result(self, res):
        '''
            Parses the OSRM response body into [{lat,lng}].
            Note: This could potentially break if their API changes.
            
            ARG:
                json_res (dict): The OSRM res body
            RETURNS:
                result: [{lat,lng}] - The reordered trip result.
        '''
        try:
            res_json = res.json()
            waypoints = res_json["waypoints"]
            waypoints.sort(key=lambda coord : coord["waypoint_index"])

            sorted_points = [{"lon":w["location"][0], "lat":w["location"][1]} for w in waypoints]
            return sorted_points

        except KeyError as error:
            raise ServiceException("Unable to parse response data") from error
        except JSONDecodeError as json_error:
            raise ServiceException("Unable to parse response data") from json_error

    def _save_points(self, points):
        '''
            Saves the result of the trip optimization to the database.
            
            ARGS:
                points: points to save
        '''
        try:
            self._trip_ref.set_points(points, self._mode)
        except ModelException as error:
            raise ServiceException("Unable to save trip points.") from error

        self._trip_repo.add(self._trip_ref)
        self._trip_repo.commit()
