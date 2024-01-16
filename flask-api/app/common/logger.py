'''
   Houses the application logger configuration.
'''
import logging
import os
from logging.handlers import RotatingFileHandler
from logging import Formatter

from flask import Flask, request
from flask.logging import default_handler
from flask_jwt_extended import verify_jwt_in_request, get_current_user

def configure_logger(app: Flask):
    '''
        Configures the application's logger.
    '''
    log_format = Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s'
    )

    if app.config['TESTING'] or app.config['DEBUG']:
        default_handler.setFormatter(log_format)
        app.logger.info('Logger setup using DEBUG level')
        app.logger.setLevel(logging.DEBUG)
    else:
        # create log directory if it doesn't exist
        try:
            os.mkdir('/var/log/otd')
        except OSError:
            pass

        rotation_handler = RotatingFileHandler(
            '/var/log/otd/otd-server.log',
            maxBytes=500_000,
            backupCount=10
        )
        rotation_handler.setFormatter(log_format)
        rotation_handler.setLevel(logging.INFO)

        app.logger.addHandler(rotation_handler)
        app.logger.info('Logger using INFO level')

    # Middleware for logging request data
    @app.before_request
    def add_req_log():
        '''
            logs relevant request info each time a request is fired.
        '''
        method = request.method
        url = request.path
        source = request.remote_addr

        verify_jwt_in_request(optional=True, verify_type=False)
        user = get_current_user()

        username = user.username if user else ''
        user_id = user.id if user else ''

        app.logger.info(f'{method} {url} from {source} ({username}:{user_id})')
