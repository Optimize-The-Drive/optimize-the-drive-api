'''Service for handling OSRM interaction '''
from enum import Enum
from flask import current_app

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
        url = current_app.config['BASE_OSRM_URL']
        
        for i, p in enumerate(self._points):
            url += str(p["lat"]) + "," + str(p["lon"])
            if i < len(self._points) - 1:
                url += ";"

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
        return None

