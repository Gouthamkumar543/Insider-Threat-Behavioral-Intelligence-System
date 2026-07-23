from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.models import (
    Employee,
    LoginActivity,
    FileAccess,
    EmailActivity,
    DeviceActivity,
    AnomalyResult
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db)
):

    total_employees = db.query(
        func.count(Employee.employee_id)
    ).scalar() or 0

    login_activities = db.query(
        func.count(LoginActivity.id)
    ).scalar() or 0

    file_access_events = db.query(
        func.count(FileAccess.id)
    ).scalar() or 0

    email_activities = db.query(
        func.count(EmailActivity.id)
    ).scalar() or 0

    device_activities = db.query(
        func.count(DeviceActivity.id)
    ).scalar() or 0

    total_anomalies = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.anomaly == -1
    ).count()

    critical_risk = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.risk_level == "Critical"
    ).count()

    high_risk = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.risk_level == "High"
    ).count()

    medium_risk = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.risk_level == "Medium"
    ).count()

    low_risk = db.query(
        AnomalyResult
    ).filter(
        AnomalyResult.risk_level == "Low"
    ).count()

    top_risk_users = db.query(
        AnomalyResult
    ).order_by(
        AnomalyResult.risk_score.desc()
    ).limit(10).all()

    recent_logins = db.query(
        LoginActivity
    ).order_by(
        LoginActivity.date.desc()
    ).limit(10).all()

    recent_file_access = db.query(
        FileAccess
    ).order_by(
        FileAccess.date.desc()
    ).limit(10).all()

    return {
        "stats": {
            "totalEmployees": total_employees,
            "loginActivities": login_activities,
            "fileAccessEvents": file_access_events,
            "emailActivities": email_activities,
            "deviceActivities": device_activities,
            "totalAnomalies": total_anomalies,
            "criticalRisk": critical_risk,
            "highRisk": high_risk,
            "mediumRisk": medium_risk,
            "lowRisk": low_risk
        },

        "riskDistribution": {
            "critical": critical_risk,
            "high": high_risk,
            "medium": medium_risk,
            "low": low_risk
        },

        "anomalyDistribution": {
            "anomalies": total_anomalies,
            "normal": max(
                total_employees - total_anomalies,
                0
            )
        },

        "topRiskUsers": [
            {
                "user": user.user,
                "risk_score": user.risk_score,
                "risk_level": user.risk_level,
                "anomaly_score": user.anomaly_score,
                "login_count": user.login_count,
                "after_hours_ratio": user.after_hours_ratio,
                "weekend_ratio": user.weekend_ratio
            }
            for user in top_risk_users
        ],

        "recentLogins": [
            {
                "id": login.id,
                "user": login.user,
                "pc": login.pc,
                "date": login.date,
                "activity": login.activity
            }
            for login in recent_logins
        ],

        "recentFileAccess": [
            {
                "id": file.id,
                "user": file.user,
                "pc": file.pc,
                "date": file.date,
                "filename": file.filename
            }
            for file in recent_file_access
        ]
    }