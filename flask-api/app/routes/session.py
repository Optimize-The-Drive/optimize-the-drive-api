from flask import Blueprint, jsonify


session_routes = Blueprint("session", __name__, url_prefix="/session")

@session_routes.get('/login')
def login():
    """
        TODO: MAKE ACTUAL REQUEST A POST REQ
    """
    return jsonify({'res': 'you hit the login!'})
