'''
    All routes are assigned to the base API blueprint in
    this file.
'''
from flask import Blueprint, jsonify
from app.routes.session import session_routes

api_routes = Blueprint("api", __name__, url_prefix="/api")
api_routes.register_blueprint(session_routes)

@api_routes.get('/')
def index():
    '''Root API ROUTE

    Returns:
        String: Home endpoint
    '''
    return jsonify({'res': 'Hellow from flawsk swerver'}), 200
