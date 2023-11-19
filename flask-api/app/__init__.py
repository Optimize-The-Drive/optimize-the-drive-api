from flask import Flask
from app.routes import api_routes

def create_app():
    '''
        Creates an instance of the Flask App
    '''
    app = Flask(__name__)
    app.register_blueprint(api_routes)

    return app
