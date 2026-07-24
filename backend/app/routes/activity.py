from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import (
    LoginActivity,
    FileAccess
)

router = APIRouter(
    prefix="/activity",
    tags=["Activity Monitoring"]
)


@router.get("/login")
def get_login_activities(
    db: Session = Depends(get_db)
):
    return db.query(
        LoginActivity
    ).order_by(
        LoginActivity.login_time.desc()
    ).limit(1000).all()


@router.get("/files")
def get_file_activities(
    db: Session = Depends(get_db)
):
    return db.query(
        FileAccess
    ).order_by(
        FileAccess.access_time.desc()
    ).limit(1000).all()


@router.get("/all")
def get_all_activities(
    db: Session = Depends(get_db)
):
    login_activities = db.query(
        LoginActivity
    ).order_by(
        LoginActivity.login_time.desc()
    ).limit(500).all()

    file_activities = db.query(
        FileAccess
    ).order_by(
        FileAccess.access_time.desc()
    ).limit(500).all()

    activities = []

    for activity in login_activities:
        activities.append({
            "id": activity.id,
            "type": "Login",
            "username": activity.username,
            "pc": activity.pc,
            "activity": activity.activity,
            "timestamp": activity.login_time,
            "is_anomaly": activity.is_anomaly,
            "anomaly_score": activity.anomaly_score
        })

    for activity in file_activities:
        activities.append({
            "id": activity.id,
            "type": "File Access",
            "username": activity.username,
            "pc": activity.pc,
            "activity": activity.action,
            "filename": activity.filename,
            "timestamp": activity.access_time,
            "is_anomaly": activity.is_anomaly,
            "anomaly_score": activity.anomaly_score
        })

    activities.sort(
        key=lambda item: item["timestamp"],
        reverse=True
    )

    return activities[:1000]