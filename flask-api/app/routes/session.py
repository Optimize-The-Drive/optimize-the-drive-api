from flask import Blueprint


session_routes = Blueprint("session", __name__, url_prefix="/session")

@session_routes.get('/login')
def login():
    """
        TODO: MAKE ACTUAL REQUEST A POST REQ
    """
    return '<p>You hit the login route</p>'
