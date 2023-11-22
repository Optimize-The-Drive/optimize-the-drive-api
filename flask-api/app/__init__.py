'''
    Creates an instance of the flask application
'''
from flask import Flask, jsonify
from app.routes import api_routes
from config import get_environment

def create_app(config=get_environment()):
    '''
        Creates an instance of the Flask App
    '''
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api_routes)
    register_error_routes(app)

    return app

def register_error_routes(app):
    '''
        Assigns handlers for common API error codes.
    '''
    @app.errorhandler(404)
    def not_found(_e):
        response_data = {
            'res': 'not found'
        }
        return jsonify(response_data), 404