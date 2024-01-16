'''
    Creates an instance of the flask application.
'''
import traceback

from flask import Flask
from marshmallow import ValidationError

from app.routes import api_routes
from app.models.user import User
from app.models.jwt import JWT
from app.common.errors import SchemaException
from app.common.logger import configure_logger
from app.common.utility import create_server_res
from app.extensions import db, jwt, migrate
from config import get_environment


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

    # Initialize JWT
    jwt.init_app(app)

    # Configure logger
    configure_logger(app)

    return app


def register_error_routes(app: Flask):
    '''
        Assigns handlers for common API error codes.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return create_server_res(error.description), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return create_server_res(error.description), 401

    @app.errorhandler(404)
    def not_found(error):
        return create_server_res(error.description), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return create_server_res(error.description), 405

    @app.errorhandler(409)
    def resource_conflict(error):
        return create_server_res(error.description), 409

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return create_server_res(error.description), 422

    @app.errorhandler(SchemaException)
    def schema_error(error):
        return create_server_res(error.args), 422

    @app.errorhandler(Exception)
    def server_error(error):
        '''
            Catch-all error handler. Catches any error that is not handled above.
        '''
        app.logger.error(type(error))
        app.logger.error(''.join(traceback.format_exception(None, error, error.__traceback__)))

        return create_server_res('Internal server error.'), 500
