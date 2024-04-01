'''
    Creates an instance of the flask application.
'''
import traceback

from flask import Flask, request, g
from werkzeug.exceptions import default_exceptions

import app.models
import app.socket

from app.routes import api_routes
from app.common.errors import SchemaException
from app.common.logger import configure_logger, log_details
from app.common.utility import create_server_res
from app.extensions import db, jwt, migrate, socketio
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

    # Configure SockerIO
    socketio.init_app(app)

    return app


def register_error_routes(app: Flask):
    '''
        Assigns handlers for common API error codes.
    '''

    # Handles 4XX, 5XX codes
    def handle_http_error(err):
        app.logger.error(log_details(f'{err.description}'))
        return create_server_res(err.description, err.code)

    for code in default_exceptions:
        app.errorhandler(code)(handle_http_error)

    # Overwrites default handler for jwt extended errors we care about logging.
    @jwt.token_verification_failed_loader
    def verified_token_failed(_param, _param1):
        app.logger.error(log_details('Could not verify token.'))
        return create_server_res('Could not verify token.', 401)

    @jwt.unauthorized_loader
    def unauthorized(_param1):
        app.logger.error(log_details('Unauthorized.'))
        return create_server_res('Unauthorized.', 401)

    @jwt.revoked_token_loader
    def revoked_token(_param1, _param2):
        app.logger.error(log_details('Token revoked.'))
        return create_server_res('Token revoked', 401)

    @jwt.expired_token_loader
    def expired_token(_param1, _param2):
        app.logger.error(log_details('Token has expired.'))
        return create_server_res('Token has expired.', 401)

    @jwt.invalid_token_loader
    def invalid_token(_param1):
        app.logger.error(log_details('Invalid token.'))
        return create_server_res('Invalid token.', 401)

    @jwt.user_lookup_error_loader
    def user_lookup_error(_param1, _param2):
        app.logger.error(log_details('Unauthorized.'))
        return create_server_res('Unauthorized.', 401)

    # schema errors
    @app.errorhandler(SchemaException)
    def schema_error(error):
        app.logger.error(log_details(f'{error.args}'))
        return create_server_res(error.args, 422)

    @socketio.on_error()
    def error_handler(error):
        '''
            Catch-all error handler for socket io. Catches any error that is not handled above.
        '''
        app.logger.error(type(error))
        app.logger.error(''.join(traceback.format_exception(None, error, error.__traceback__)))

    @app.errorhandler(Exception)
    def server_error(error):
        '''
            Catch-all error handler. Catches any error that is not handled above.
        '''
        app.logger.error(type(error))
        app.logger.error(''.join(traceback.format_exception(None, error, error.__traceback__)))

        return create_server_res('Internal server error.', 500)
