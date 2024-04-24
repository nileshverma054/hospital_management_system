from functools import wraps
from flask import current_app as app, request
from marshmallow import ValidationError
import ast
from api import db
from webargs.flaskparser import parser


class AuthenticationError(Exception):
    pass


def handle_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        status = False
        try:
            res, status_code = fn(*args, **kwargs)
            status = True
            return res, status_code
        except AuthenticationError as e:
            return {'message': str(e)}, 401
        except ValidationError as e:
            app.logger.error(f"ValidationError: {e}")
            error = ast.literal_eval(str(e))
            return {'message': error}, 400
        except ValueError as e:
            app.logger.error(f"API ValueError: {e}")
            return {'message': str(e)}, 400
        except (Exception) as exc:
            app.logger.exception(
                f"UnknownException {request.method} {request.path}: {exc}")
            return {'message': "Internal Server Error"}, 500
        finally:
            try:
                if not status:
                    db.session.rollback()
            except Exception as e:
                app.logger.exception(
                    f'UnknownException while completing db session: {e}')
    return wrapper


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise ValidationError(error)
