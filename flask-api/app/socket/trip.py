'''Trip socket definitions.'''
from flask import current_app
from flask_socketio import emit

from app.common.errors import ServiceException
from app.common.utility import create_socket_res, SocketStatus
from app.extensions import socketio
from app.services.trip_optimizer import TripOptimizerService

@socketio.on('generate_trip')
def generate_trip(json_trip):
    """
        Calls the trip optimizer service (OSRM interface)
        and ties the points to a trip.
    """
    res_event = "generate_trip_res"
    optimizer_service = TripOptimizerService()

    try:
        optimizer_service.set_trip(json_trip)
        optimizer_service.generate()
        emit(res_event, create_socket_res("Trip points updated.", SocketStatus.SUCCESS))
    except ServiceException as error:
        current_app.logger.error(f"Error optimizing route: {error.args}")
        emit(
            res_event,
            create_socket_res("Error optimizing route", SocketStatus.ERROR)
        )
