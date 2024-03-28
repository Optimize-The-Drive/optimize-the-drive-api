'''
    All routes are assigned to the base API blueprint in
    this file.
'''
from flask import Blueprint

import app.routes.socket
from app.common.utility import create_server_res
from app.routes.auth import auth_routes
from app.routes.user import user_routes
from app.routes.trip import trip_routes

api_routes = Blueprint("api", __name__, url_prefix="/api")
api_routes.register_blueprint(auth_routes)
api_routes.register_blueprint(user_routes)
api_routes.register_blueprint(trip_routes)
