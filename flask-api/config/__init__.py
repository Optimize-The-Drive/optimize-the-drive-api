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
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')

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
    env = os.getenv('ENV_TYPE')

    if env == 'dev':
        return DevConfig
    elif env == 'test':
        return TestConfig 
    