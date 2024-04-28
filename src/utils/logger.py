import logging
import logging.config
import uuid

import flask

request_id = str(uuid.uuid4())


def get_request_id():
    """
    Retrieves the request ID for the current Flask request.

    Returns:
        str: The request ID.

    Raises:
        None.
    """
    if flask.has_request_context():
        if getattr(flask.g, "request_id", None):
            return getattr(flask.g, "request_id", "")
        headers = flask.request.headers
        # if we are using AWS ELB then the "X-Amzn-Trace-Id" is already set which
        # can be used to trace the API request lifecycle
        flask.g.request_id = headers.get("X-Amzn-Trace-Id") or str(uuid.uuid4())
        return flask.g.request_id
    return request_id


class RequestIdFilter(logging.Filter):
    """
    A logging filter which adds a request ID to each log record.

    This filter is used to add a request ID to each log record. The request ID
    is taken from the current Flask request context, if available. If not
    available, a new request ID is generated.

    Attributes:
        None.
    """

    def filter(self, record):
        record.request_id = get_request_id()
        return True


def config_logger(app):
    """
    Configures the application logger.

    This function configures the application logger with a filter to add a request ID to each log record.

    Args:
        app (Flask): The Flask application..

    Returns:
        None.

    Raises:
        None.
    """
    log_config = dict(
        version=1,
        disable_existing_loggers=True,
        filters={
            "request_id": {"()": RequestIdFilter},
        },
        formatters={
            "console": {
                "format": "%(request_id)s - %(asctime)s - %(levelname)s - %(filename)s:%(lineno)s -  %(message)s"
            }
        },
        handlers={
            "console": {
                "level": app.config.get("LOG_LEVEL", "DEBUG"),
                "class": "logging.StreamHandler",
                "formatter": "console",
                "filters": ["request_id"],
            }
        },
        loggers={
            "console": {
                "handlers": ["console"],
                "level": app.config.get("LOG_LEVEL", "DEBUG"),
                "propagate": False,
            }
        },
    )

    logging.config.dictConfig(log_config)
    app.logger = logging.getLogger("console")
    app.logger.info("logger configured successfully")
