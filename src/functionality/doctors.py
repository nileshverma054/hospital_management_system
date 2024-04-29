from flask import current_app as app


class DoctorService:
    def __init__(self, **kwargs):
        # TODO: use pydantic
        app.logger.debug(f"DoctorService init: kwargs: {kwargs}")
        self.kwargs = kwargs
