import enum


APP_NAME = "HOSPITAL_MANAGEMENT_SYSTEM"


class DoctorSpecialization(str, enum.Enum):
    """Doctor specialization"""

    GENERAL_MEDICINE = "GENERAL_MEDICINE"
    INTERNAL_MEDICINE = "INTERNAL_MEDICINE"
    SURGERY = "SURGERY"
    PSYCHIATRY = "PSYCHIATRY"
    OBSTETRICS_AND_GYNAECOLOGY = "OBSTETRICS_AND_GYNAECOLOGY"
    PEDIATRICS = "PEDIATRICS"
    DENTISTRY = "DENTISTRY"
    OPHTHALMY = "OPHTHALMY"
    PHYSICAL_THERAPY = "PHYSICAL_THERAPY"


class DayOfWeek(str, enum.Enum):
    """Day of week"""

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
