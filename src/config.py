import os


class BaseConfig(object):
    DEBUG = bool(os.environ.get("DEBUG", False))
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    PORT = int(os.environ.get("PORT", 5080))
    TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
