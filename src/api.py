import time

from flask import Flask, g, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from src.common.constants import APP_NAME
from src.config import BaseConfig
from src.utils.logger import config_logger

# Initialize the Flask App
app = Flask(APP_NAME)

# Initialize app config
app.config.from_object(BaseConfig)

# Initialize Database and ORM
db = SQLAlchemy()

# Initialize Flask RESTful API Framework
api = Api(app, prefix="/api/v1")

# Initialize the application logger
config_logger(app)


@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.after_request
def after_request(response):
    response.headers["X-Request-Id"] = getattr(g, "request_id", "")
    diff = f"{(time.time() - g.request_start_time):2.4f}s"
    app.logger.debug(
        f"{request.method} {request.path} {response.status} " f"| Time taken: {diff}"
    )
    return response
