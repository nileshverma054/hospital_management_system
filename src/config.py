import os


class BaseConfig(object):
    DEBUG = bool(os.environ.get("DEBUG", False))
    DB_NAME = os.environ.get("DB_NAME")
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_URI}/{DATABASE_NAME}"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    PORT = int(os.environ.get("PORT", 5080))
    TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
