from flask import current_app as app
from flask_restful import Resource
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_kwargs

from src.api import db
from src.common.constants import DayOfWeek, DoctorSpecialization
from src.models.models import Doctor
from src.utils.decorators import handle_exceptions
from src.utils.resource_exceptions import ResourceNotFoundError


class AvailabilityScheduleSchema(Schema):
    day = fields.Enum(enum=DayOfWeek, required=True)
    start = fields.Time(required=True)
    end = fields.Time(required=True)
    capacity = fields.Int(required=True)


class DoctorCreateSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    department_id = fields.Int(required=True)
    specialization = fields.Enum(enum=DoctorSpecialization, required=True)
    availability_schedule = fields.Nested(AvailabilityScheduleSchema, many=True)

    class Meta:
        # this attribute will raise error if user sends extra fields
        strict = True


class DoctorResource(Resource):
    @handle_exceptions
    @use_kwargs(DoctorCreateSchema)
    def post(self, **kwargs):
        app.logger.debug(f"{self.__class__.__name__}.post: {kwargs}")
        return {}, 201
