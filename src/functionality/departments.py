from flask import current_app as app

from src.api import db
from src.models.models import DepartmentService


def add_services_to_department(department_id, services):
    """
    Add a list of services to a department.

    Args:
        department_id (int): The id of the department.
        services (List[str]): A list of service names to add.

    Raises:
        ValueError: If any of the services already exists in the department.

    Returns:
        None
    """
    db_result = (
        db.session.query(DepartmentService)
        .filter(
            DepartmentService.department_id == department_id,
            DepartmentService.service.in_(services),
        )
        .all()
    )
    app.logger.debug(f"existing services: {db_result}")
    if db_result:
        services = [service.service for service in db_result]
        raise ValueError(f"Services {services} already exists")
    else:
        department_services = [
            DepartmentService(department_id=department_id, service=service_name)
            for service_name in services
        ]
        db.session.bulk_save_objects(department_services)
        app.logger.info(f"added services: {services}")


def remove_services_from_department(department_id, services):
    """
    Remove services from department.

    Args:
        department_id (int): The id of the department.
        services (List[str]): A list of service names to remove.

    Raises:
        ValueError: If any of the services does not exist in the department.

    Returns:
        None
    """
    rows = (
        db.session.query(DepartmentService)
        .filter(
            DepartmentService.department_id == department_id,
            DepartmentService.service.in_(services),
        )
        .delete()
    )
    app.logger.debug(f"removed services: {services}, rows affected: {rows}")
