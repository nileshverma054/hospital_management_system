from flask import current_app as app
from flask_restful import Resource
from marshmallow import Schema
from webargs import fields
from webargs.flaskparser import use_kwargs

from src.api import db
from src.functionality.departments import (
    add_services_to_department,
    remove_services_from_department,
)
from src.models.models import Department, DepartmentService
from src.utils.decorators import handle_exceptions
from src.utils.resource_exceptions import ResourceNotFoundError


class DepartmentSchema(Schema):
    name = fields.Str(required=True)
    services_offered = fields.List(fields.Str(), required=False, default=[])

    class Meta:
        # this attribute will raise error if user sends extra fields
        strict = True


class DepartmentSchemaPatch(Schema):
    name = fields.Str(required=True)
    add_services = fields.List(fields.Str(), required=False, default=[])
    remove_services = fields.List(fields.Str(), required=False, default=[])

    class Meta:
        strict = True


class DepartmentResource(Resource):
    @handle_exceptions
    @use_kwargs(DepartmentSchema)
    def post(self, **kwargs):
        app.logger.debug(f"DepartmentResource.post: {kwargs}")

        department_name = kwargs.get("name")
        services_offered = kwargs.get("services_offered")

        # check if department with name already exists
        existing_department = Department.query.filter_by(name=department_name).first()
        if existing_department:
            app.logger.info("department already exists")
            raise ValueError(f"Department {department_name} already exists")
        else:
            # create new department
            department = Department(name=department_name)
            department.save()
            app.logger.info(f"department created: {department}")
            department_services = [
                DepartmentService(department_id=department.id, service=service_name)
                for service_name in services_offered
            ]
            db.session.bulk_save_objects(department_services)
            db.session.flush()
            app.logger.info("created services")
            db.session.commit()
            return {"id": department.id}, 201

    @handle_exceptions
    @use_kwargs({"name": fields.Str(required=False)}, location="query")
    def get(self, **kwargs):
        app.logger.debug(f"DepartmentResource.get: kwargs: {kwargs}")
        department_id = kwargs.get("department_id")
        department_name = kwargs.get("name")
        if department_id:
            department = Department.get_by_id(department_id)
            app.logger.debug(f"department: {department}")
            if department:
                return department.to_json_structured(), 200
            else:
                raise ResourceNotFoundError(f"Department {department_id} doesn't exist")
        elif department_name:
            department = Department.get_by_name(department_name)
            app.logger.debug(f"department: {department}")
            if department:
                return department.to_json_structured(), 200
            else:
                raise ResourceNotFoundError(
                    f"Department {department_name} doesn't exist"
                )
        else:
            departments = Department.get_all(limit=10)
            app.logger.debug(f"departments: {departments}")
            if not departments:
                raise ResourceNotFoundError("No records found")
            records = [department.to_json_structured() for department in departments]
            app.logger.debug(f"records: {records}")
            return {"records": records}, 200

    @handle_exceptions
    @use_kwargs(DepartmentSchemaPatch)
    def patch(self, department_id, **kwargs):
        app.logger.debug(
            f"DepartmentResource.patch: department_id: {department_id}, kwargs: {kwargs}"
        )
        department = Department.query.get(department_id)
        if not department:
            raise ResourceNotFoundError(f"Department {department_id} doesn't exist")
        department.name = kwargs.get("name")
        add_services = kwargs.get("add_services")
        if add_services:
            add_services_to_department(department_id, add_services)
        remove_services = kwargs.get("remove_services")
        if remove_services:
            remove_services_from_department(department_id, remove_services)
        db.session.commit()
        return {}, 204

    @handle_exceptions
    def delete(self, department_id):
        app.logger.debug(f"DepartmentResource.delete: {department_id}")
        count = Department.query.filter_by(id=department_id).delete()
        if not count:
            raise ResourceNotFoundError(f"Department {department_id} doesn't exist")
        db.session.commit()
        app.logger.info(f"department with id: {department_id} deleted successfully")
        return {}, 204
