'''
   Houses the application logger configuration.
'''
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
import uuid

from flask import Flask, request, g
from flask.logging import default_handler
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def log_details(log):
    '''
        Returns a formatted string for log details.
        
        RETURNS:
            formatted log detail string
    '''
    user_id = g.get('user_id', None)
    req_id =g.get('req_id', None)

    strings = [f'user: {user_id}' if user_id else '', f'request: {req_id}' if req_id else '']
    details=', '.join([x for x in strings if x])

    return f'{log} [{details}]' if details else log


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
        # Maybe we add this to our prod setup script? I don't feel
        # like it is a great idea to be handled by Flask.
        try:
            os.mkdir('/var/log/otd')
        except OSError:
            pass

        rotation_handler = RotatingFileHandler(
            '/var/log/otd/otd-server.log',
            maxBytes=1_000_000,
            backupCount=100
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

        # attach a unique log identifier to the request for other logs to use.
        g.req_id = str(uuid.uuid4())
        g.req_url = url

        verify_jwt_in_request(optional=True, verify_type=False)
        g.user_id = get_jwt_identity()

        app.logger.info(log_details(f'{method} {url} from {source}'))


    @app.after_request
    def add_res_log(response):
        '''
            logs relevant request info each time a request is fired.
        '''
        code = response.status_code
        app.logger.info(log_details(f'Response - {code}'))

        return response
