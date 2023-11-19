from flask import Blueprint
from app.routes.session import session_routes

api_routes = Blueprint("api", __name__, url_prefix="/api")
api_routes.register_blueprint(session_routes)

@api_routes.get('/')
def index():
    """Root API ROUTE

    Returns:
        String: Home endpoint
    """
    return '<h1>Hello from our flask server!</h1>'
