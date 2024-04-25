import http

from flask import current_app as app
from flask_restful import Resource
from sqlalchemy import text

from src.api import db


class HealthCheck(Resource):
    @staticmethod
    def get():
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as err:
            app.logger.exception(f"Database connection error: {err}")
            return {
                "message": "Database connection error"
            }, http.HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, http.HTTPStatus.NO_CONTENT
