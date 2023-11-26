'''
    Reads environment variables and creates a configuration
    object to be consumed by the flask application
'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

class Config(object):
    '''
        Shared config across all environments
    '''
    SECRET_KEY = os.getenv('SECRET_KEY')

    POSTGRES_USER = os.getenv('POSTGRES_USER', 'otd')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5342')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_DB_NAME=os.getenv('POSTGRES_DB_NAME', 'otd-dev')

    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}'    # pylint: disable=C0301

class DevConfig(Config):
    '''
        Config for Dev Environment
    '''
    DEBUG = True

class TestConfig(Config):
    '''
        Config for Test Environment
    '''
    TESTING = True

def get_environment():
    '''
        Returns the appropriate environment configuration.
    '''
    env = os.getenv('ENV_TYPE', 'dev')

    if env == 'dev':
        return DevConfig
    elif env == 'test':
        return TestConfig    