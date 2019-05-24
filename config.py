import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "015026567c29fdffe31d91edbe7ba1b17728db79194fca1f21"
    # SECRET_KEY = os.urandom(24)
    SESSION_TYPE = 'filesystem'
    MAIL_PORT = 2525
    MAIL_USE_TLS = False
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_USERNAME = "1914dfba898b6f"
    MAIL_PASSWORD = "22cf98bcf4e60e"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL = "localhost"


class TestingConfig(Config):
    TESTING = True