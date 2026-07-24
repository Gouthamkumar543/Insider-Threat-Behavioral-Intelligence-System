from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import (
    Employee,
    LoginActivity,
    FileAccess,
    Alert,
    Investigation,
    AnomalyResult
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/overview")
def report_overview(
    db: Session = Depends(get_db)
):
    total_employees = db.query(
        Employee
    ).count()

    total_login_activities = db.query(
        LoginActivity
    ).count()

    total_file_access = db.query(
        FileAccess
    ).count()

    total_anomalies = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.anomaly == 1
    ).count()

    total_alerts = db.query(
        Alert
    ).count()

    open_alerts = db.query(
        Alert
    ).filter(
        Alert.status == "Open"
    ).count()

    open_investigations = db.query(
        Investigation
    ).filter(
        Investigation.status == "Open"
    ).count()

    return {
        "generated_at": datetime.utcnow(),
        "employees": total_employees,
        "login_activities": total_login_activities,
        "file_access_events": total_file_access,
        "anomalies": total_anomalies,
        "alerts": total_alerts,
        "open_alerts": open_alerts,
        "open_investigations": open_investigations
    }


@router.get("/risk")
def risk_report(
    db: Session = Depends(get_db)
):
    employees = db.query(
        Employee
    ).order_by(
        Employee.risk_score.desc()
    ).all()

    return [
        {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department": employee.department,
            "risk_score": employee.risk_score,
            "risk_level": employee.risk_level
        }
        for employee in employees
    ]


@router.get("/anomalies")
def anomaly_report(
    db: Session = Depends(get_db)
):
    results = db.query(
        AnomalyResult
    ).order_by(
        AnomalyResult.risk_score.desc()
    ).all()

    return [
        {
            "user": result.user,
            "login_count": result.login_count,
            "unique_devices": result.unique_devices,
            "after_hours_logins": result.after_hours_logins,
            "weekend_logins": result.weekend_logins,
            "anomaly_score": result.anomaly_score,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level
        }
        for result in results
    ]


@router.get("/alerts")
def alert_report(
    db: Session = Depends(get_db)
):
    alerts = db.query(
        Alert
    ).order_by(
        Alert.created_at.desc()
    ).all()

    return [
        {
            "id": alert.id,
            "title": alert.title,
            "severity": alert.severity,
            "status": alert.status,
            "risk_score": alert.risk_score,
            "created_at": alert.created_at
        }
        for alert in alerts
    ]