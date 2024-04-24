from functools import wraps
from flask import request, current_app as app
from utils.resource_exceptions import AuthenticationError


def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if token != app.config["API_TOKEN"]:
            raise AuthenticationError("INVALID-TOKEN")
        return fn(*args, **kwargs)

    return wrapper
