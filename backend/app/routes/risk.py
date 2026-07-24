from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Employee
from app.services.risk_engine import calculate_employee_risk

router = APIRouter(
    prefix="/risk",
    tags=["Risk Analysis"]
)


@router.get("/employees")
def get_employee_risks(
    db: Session = Depends(get_db)
):
    employees = db.query(
        Employee
    ).order_by(
        Employee.risk_score.desc()
    ).all()

    return [
        {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "designation": employee.designation,
            "risk_score": employee.risk_score,
            "risk_level": employee.risk_level
        }
        for employee in employees
    ]


@router.get("/employees/{employee_id}")
def get_employee_risk(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(
        Employee
    ).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return {
            "error": "Employee not found"
        }

    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "name": employee.name,
        "risk_score": employee.risk_score,
        "risk_level": employee.risk_level
    }


@router.post("/calculate/{employee_id}")
def calculate_risk(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(
        Employee
    ).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return {
            "error": "Employee not found"
        }

    anomaly_count = sum(
        1 for activity in employee.login_activities
        if activity.is_anomaly
    )

    file_access_count = sum(
        1 for activity in employee.file_accesses
        if activity.is_anomaly
    )

    failed_logins = sum(
        1 for activity in employee.login_activities
        if not activity.success
    )

    after_hours_activity = sum(
        1
        for activity in employee.login_activities
        if activity.login_time.hour < 7
        or activity.login_time.hour > 20
    )

    result = calculate_employee_risk(
        anomaly_count=anomaly_count,
        file_access_count=file_access_count,
        failed_logins=failed_logins,
        after_hours_activity=after_hours_activity
    )

    employee.risk_score = result["score"]
    employee.risk_level = result["level"]

    db.commit()
    db.refresh(employee)

    return {
        "employee_id": employee.id,
        "risk_score": employee.risk_score,
        "risk_level": employee.risk_level
    }


@router.get("/distribution")
def risk_distribution(
    db: Session = Depends(get_db)
):
    return {
        "critical": db.query(Employee).filter(
            Employee.risk_level == "Critical"
        ).count(),
        "high": db.query(Employee).filter(
            Employee.risk_level == "High"
        ).count(),
        "medium": db.query(Employee).filter(
            Employee.risk_level == "Medium"
        ).count(),
        "low": db.query(Employee).filter(
            Employee.risk_level == "Low"
        ).count()
    }