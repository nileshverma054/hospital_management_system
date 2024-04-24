from flask import current_app as app
from flask_restful import Resource, abort
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from src.api import db
from src.models.models import Department
from src.utils.resource_exceptions import ResourceNotFoundError
from src.utils.decorators import handle_exceptions


class DepartmentSchema(Schema):
    name = fields.Str(required=True)
    services_offered = fields.Str(required=False, default="")

    class Meta:
        # this attribute will raise error if user sends extra fields
        strict = True


class DepartmentResource(Resource):
    @handle_exceptions
    @use_kwargs(DepartmentSchema)
    def post(self, **kwargs):
        app.logger.debug(f"DepartmentResource.post: {kwargs}")
        department = Department(**kwargs)
        department.save()
        db.session.commit()
        return department.to_json(), 200

    @handle_exceptions
    @use_args({"id": fields.Int(required=False)}, location="query")
    def get(self, args):
        app.logger.debug(f"DepartmentResource.get: args: {args}")
        department_id = args.get("id")
        if department_id:
            department = Department.get_by_id(department_id)
            app.logger.debug(f"department: {department}")
            if department:
                return department.to_json(), 200
            else:
                raise ResourceNotFoundError(f"Department {args} doesn't exist")
        if not department_id:
            departments = Department.get_all(limit=10)
            app.logger.debug(f"departments: {departments}")
            records = [department.to_json() for department in departments]
            app.logger.debug(f"records: {records}")
            return records, 200
        return {}, 200

    @handle_exceptions
    @use_kwargs(DepartmentSchema)
    def put(self, department_id, **kwargs):
        department = Department.query.get(department_id)
        if department:
            for key, value in kwargs.items():
                setattr(department, key, value)
            department.save()
            return department.to_json()
        else:
            abort(404, message=f"Department {department_id} doesn't exist")

    @handle_exceptions
    @use_kwargs(DepartmentSchema)
    def delete(self, department_id, **kwargs):
        department = Department.query.get(department_id)
        if department:
            department.delete()
            return {"message": f"Department {department_id} deleted"}
        else:
            abort(404, message=f"Department {department_id} doesn't exist")
