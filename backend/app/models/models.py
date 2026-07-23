from sqlalchemy import Column, String, Integer, Text, Float
from app.database import Base


# =========================
# EMPLOYEES
# =========================

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True)
    name = Column(String)
    department = Column(String)
    designation = Column(String)
    manager = Column(String)


# =========================
# LOGIN ACTIVITY
# =========================

class LoginActivity(Base):
    __tablename__ = "login_activity"

    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)
    pc = Column(String)
    activity = Column(String)


# =========================
# FILE ACCESS
# =========================

class FileAccess(Base):
    __tablename__ = "file_access"

    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)
    pc = Column(String)
    filename = Column(String)


# =========================
# EMAIL ACTIVITY
# =========================

class EmailActivity(Base):
    __tablename__ = "email_activity"

    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)
    pc = Column(String)
    to = Column(String)
    cc = Column(String)
    bcc = Column(String)
    from_email = Column(String)
    size = Column(Integer)


# =========================
# DEVICE ACTIVITY
# =========================

class DeviceActivity(Base):
    __tablename__ = "device_activity"

    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)
    pc = Column(String)
    activity = Column(String)


# =========================
# HTTP ACTIVITY
# =========================

class HttpActivity(Base):
    __tablename__ = "http_activity"

    id = Column(String, primary_key=True)
    date = Column(String)
    user = Column(String)
    pc = Column(String)
    url = Column(Text)


# =========================
# ANOMALY RESULTS
# =========================

class AnomalyResult(Base):
    __tablename__ = "anomaly_results"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user = Column(
        String,
        unique=True,
        nullable=False
    )

    login_count = Column(Integer)

    unique_devices = Column(Integer)

    after_hours_logins = Column(Integer)

    weekend_logins = Column(Integer)

    after_hours_ratio = Column(Float)

    weekend_ratio = Column(Float)

    anomaly_prediction = Column(Integer)

    anomaly_score = Column(Float)

    anomaly = Column(Integer)

    risk_score = Column(Float)

    risk_level = Column(String)


# =========================
# APPLICATION USERS
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )