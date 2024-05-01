from functools import wraps

from flask import current_app as app
from flask import request
from werkzeug.exceptions import UnprocessableEntity

from src.api import db
from src.utils.resource_exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
)


def authenticate(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if token != app.config["API_TOKEN"]:
            raise AuthenticationError("INVALID-TOKEN")
        return fn(*args, **kwargs)

    return wrapper


def handle_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        status = False
        try:
            res, status_code = fn(*args, **kwargs)
            status = True
            return res, status_code
        except AuthenticationError as e:
            return {"message": str(e)}, 401
        except UnprocessableEntity as e:
            app.logger.error(f"UnprocessableEntity: {e.__dict__}")
            error_msg = e.data.get("messages").get("json")
            error = {"error": error_msg}
            return {"message": error}, 422
        except ValueError as e:
            app.logger.error(f"API ValueError: {e}")
            return {"message": str(e)}, 400
        except ResourceNotFoundError as e:
            return {"message": str(e)}, 404
        except Exception as exc:
            app.logger.exception(
                f"UnknownException {request.method} {request.path}: {exc}"
            )
            return {"message": "Internal Server Error"}, 500
        finally:
            try:
                if not status:
                    db.session.rollback()
                    app.logger.debug("Databse session rolled back")
            except Exception as e:
                app.logger.exception(
                    f"UnknownException while completing db session: {e}"
                )

    return wrapper


def function_logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        app.logger.debug(
            f"function {fn.__name__} called with args: {args}, kwargs: {kwargs}"
        )
        result = fn(*args, **kwargs)
        app.logger.debug(f"function {fn.__name__} returned: {result}")
        return result

    return wrapper
