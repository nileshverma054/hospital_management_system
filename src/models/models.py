import datetime

from src.api import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
    )
    modified_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
    )

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.flush()

    def delete(self):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.flush()

    @classmethod
    def get_all(cls, limit=10):
        """Get all records from the table."""
        return cls.query.limit(limit).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


class Patient(BaseModel):
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(255))
    medical_history = db.Column(db.Text)
    appointments = db.relationship("Appointment", backref="patient", lazy=True)

    def to_json(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d")
            if self.date_of_birth
            else None,
            "gender": self.gender,
            "email": self.email,
            "medical_history": self.medical_history,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Doctor(BaseModel):
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    email = db.Column(db.String(255))
    availability_schedule = db.Column(db.String(255))
    assigned_patients = db.relationship(
        "Patient", secondary="doctor_patient", backref="doctors", lazy=True
    )
    departments = db.relationship(
        "Department", secondary="doctor_department", backref="doctors", lazy=True
    )

    def to_json(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "email": self.email,
            "availability_schedule": self.availability_schedule,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Department(BaseModel):
    name = db.Column(db.String(100))
    services = db.relationship("DepartmentService", backref="department", lazy=True)

    def __repr__(self):
        return f"<Department {self.id} {self.name} {self.services}>"

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def to_json(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "id": self.id,
            "name": self.name,
            "services_offered": self.services,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def to_json_structured(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "id": self.id,
            "name": self.name,
            "services_offered": [service.service for service in self.services],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class DepartmentService(BaseModel):
    """Model to store services offered by a department."""

    service = db.Column(db.String(100))
    department_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id", ondelete="CASCADE"),
    )

    def __repr__(self):
        return f"<DepartmentService {self.department_id} {self.service}>"

    def to_json(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "department_id": self.department_id,
            "service": self.service,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


doctor_patient = db.Table(
    "doctor_patient",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctor.id"), primary_key=True),
    db.Column("patient_id", db.Integer, db.ForeignKey("patient.id"), primary_key=True),
)

doctor_department = db.Table(
    "doctor_department",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctor.id"), primary_key=True),
    db.Column(
        "department_id", db.Integer, db.ForeignKey("department.id"), primary_key=True
    ),
)


class Appointment(BaseModel):
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        """Serialize the object to a JSON-friendly format."""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
