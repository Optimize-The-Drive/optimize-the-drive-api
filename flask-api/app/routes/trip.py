"""Defines the Trip routes"""
from flask import abort, current_app
from flask_jwt_extended import jwt_required, get_current_user
from flask_smorest import Blueprint

from app.common.utility import create_server_res
from app.common.logger import log_details
from app.schema.trip import TripCreateSchema, TripResultSchema, TripEditSchema
from app.models.trip import Trip
from app.repos import trip_repo


trip_routes = Blueprint("trip", __name__, url_prefix="/trip")


@trip_routes.post('/')
@jwt_required()
@trip_routes.arguments(TripCreateSchema)
@trip_routes.response(201, TripResultSchema)
def create_route(trip_data):
    """
        Creates a route, without the points.
    
        Returns 201, Trip
    """

    # We can utilize assigning the route to the user that made
    # the request by reading the JWT identity. Otherwise, we
    # could pass the user_id in the request payload.
    user = get_current_user()

    if not user:
        abort(401, "Unauthorized")

    trip_name = trip_data["name"]
    trip_description = trip_data.get('description', None)
    new_trip = Trip.create(name=trip_name, description=trip_description, user_id=user.id)

    trip_repo.add(new_trip)
    trip_repo.commit()

    return  {"trip": new_trip}


@trip_routes.patch('/<int:trip_id>')
@jwt_required()
@trip_routes.arguments(TripEditSchema)
@trip_routes.response(200, TripResultSchema)
def edit_route(trip_data, trip_id):
    """
        Edits a route, without the points.
    
        Returns 200, Trip
    """
    user = get_current_user()
    trip: Trip = trip_repo.by_id(trip_id)

    if not trip:
        abort(404, description="Trip not found.")

    if trip.user_id != user.id:
        abort(403, description="You don't have access to this resource.")

    new_name = trip_data.get("name", None)
    new_desc = trip_data.get("description", None)

    if new_name:
        trip.name = new_name
    if new_desc:
        trip.description = new_desc

    trip_repo.add(trip)
    trip_repo.commit()

    return {"trip": trip}

@trip_routes.delete('/<int:trip_id>')
@jwt_required()
def delete_route(trip_id):
    """
        Deletes a route.
        
        Returns 200
    Args:
        trip_id (_type_): _description_
    """
    user = get_current_user()
    trip: Trip = trip_repo.by_id(trip_id)

    if not trip:
        abort(404, description="Trip not found.")

    if trip.user_id != user.id:
        abort(403, description="You don't have access to this resource.")

    trip_repo.delete(trip)
    trip_repo.commit()
    current_app.logger.info(log_details('User deleted trip.'))

    return create_server_res('Trip deleted successfully.', 200)
