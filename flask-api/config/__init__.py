'''
    Reads environment variables and creates a configuration
    object to be consumed by the flask application.
'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

class Config():
    ''' Shared config across all environments. '''

    SECRET_KEY = os.getenv('SECRET_KEY')

    POSTGRES_USER = os.getenv('POSTGRES_USER', 'otd')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5342')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_DB_NAME = os.getenv('POSTGRES_DB', 'otd-dev')

    # pylint: disable-next=C0301
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '900'))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '2592000'))

    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/auth/refresh'
    JWT_SESSION_COOKIE = True
    JWT_COOKIE_SECURE = os.getenv('JWT_COOKIE_SECURE')

class DevConfig(Config):
    ''' Config for Dev Environment. '''
    
    DEBUG = True

class TestConfig(Config):
    ''' Config for Test Environment. '''
    TESTING = True

def get_environment():
    ''' Returns the appropriate environment configuration. '''

    env = os.getenv('ENV_TYPE')

    if env == 'test':
        return TestConfig

    return DevConfig
