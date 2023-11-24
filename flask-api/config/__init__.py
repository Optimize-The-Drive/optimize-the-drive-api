'''
    Reads environment variables and creates a configuration
    object to be consumed by the flask application
'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

class Config():
    '''
        Shared config across all environments
    '''
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevConfig(Config):
    '''
        Config for Dev Environment
    '''
    POSTGRES_URL = os.getenv('POSTGRES_URL')

class TestConfig(Config):
    '''
        Config for Test Environment
    '''
    TESTING = True
    POSTGRES_URL = os.getenv('POSTGRES_URL')

def get_environment():
    '''
        Returns the appropriate environment configuration.
    '''
    env = os.getenv('ENV_TYPE')
    test = os.getenv('SECRET_1')
    test1 = os.getenv('SECRET_CI_KEY')
    print(test, test1)

    if env == 'dev':
        return DevConfig
    if env == 'test':
        return TestConfig
    return Config
