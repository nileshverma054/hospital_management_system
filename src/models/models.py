from src.api import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_information = db.Column(db.String(255))
    medical_history = db.Column(db.Text)
    appointments = db.relationship("Appointment", backref="patient", lazy=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    contact_information = db.Column(db.String(255))
    availability_schedule = db.Column(db.String(255))
    assigned_patients = db.relationship(
        "Patient", secondary="doctor_patient", backref="doctor", lazy=True
    )
    departments = db.relationship(
        "Department", secondary="doctor_department", backref="doctors", lazy=True
    )


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    services_offered = db.Column(db.Text)


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


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
