'''
    Creates an instance of the flask application.
'''
from flask import Flask, jsonify
from flask_migrate import Migrate
from app.routes import api_routes
from app.models import User
from config import get_environment
from database import db

migrate = Migrate()

def create_app(config=get_environment()):
    '''
        Creates an instance of the Flask App
    '''
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api_routes)
    register_error_routes(app)

    # Initialize Database
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db, compare_type=True)

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
