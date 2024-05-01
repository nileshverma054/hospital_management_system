from flask import current_app as app
from pydantic import BaseModel

from src.api import db
from src.models.models import Department, Doctor, DoctorDepartment
from src.utils.decorators import function_logger


class CreateDoctorService(BaseModel):
    name: str
    email: str
    specialization: str
    availability_schedule: dict
    department_id: int

    def validate_email(self):
        if bool(Doctor.query.filter_by(email=self.email).first()):
            raise ValueError(f"Doctor already exists with email {self.email}")

    def validate_department(self):
        if not Department.query.filter_by(id=self.department_id).first():
            raise ValueError(f"Department with id {self.department_id} doesn't exist")

    def add_to_department(self, doctor: Doctor, department_id: int) -> None:
        doctor_department = DoctorDepartment(
            doctor_id=doctor.id, department_id=department_id
        )
        doctor_department.save()
        app.logger.info(f"doctor added to department: {doctor_department}")

    def parse_availability_schedule(self) -> dict:
        def format_time(time_obj):
            return f"{time_obj.hour}:{time_obj.minute}"

        app.logger.debug(f"availability schedule before: {self.availability_schedule}")
        schedule = {}
        for day in self.availability_schedule.keys():
            schedule[day] = {
                "start": format_time(self.availability_schedule[day]["start"]),
                "end": format_time(self.availability_schedule[day]["end"]),
                "capacity": self.availability_schedule[day]["capacity"],
            }
        self.availability_schedule = schedule
        app.logger.debug(f"schedule: {self.availability_schedule}")

    def validate(self):
        self.validate_email()
        self.validate_department()

    def create(self) -> Doctor.id:
        self.validate()
        self.parse_availability_schedule()
        doctor = Doctor(
            name=self.name,
            email=self.email,
            specialization=self.specialization,
            availability_schedule=self.availability_schedule,
        )
        doctor.save()
        app.logger.info(f"doctor created: {doctor}")
        self.add_to_department(doctor, self.department_id)
        return doctor.id
