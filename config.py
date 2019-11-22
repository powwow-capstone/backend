import os
# from dotenv import load_dotenv
# from pathlib import Path  # python3 only

basedir = os.path.abspath(os.path.dirname(__file__))
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['FLASK_SECRET']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
