from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Alert
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "/",
    response_model=list[AlertResponse]
)
def get_alerts(
    db: Session = Depends(get_db)
):
    return db.query(
        Alert
    ).order_by(
        Alert.created_at.desc()
    ).all()


@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(
        Alert
    ).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.post(
    "/",
    response_model=AlertResponse
)
def create_alert(
    request: AlertCreate,
    db: Session = Depends(get_db)
):
    alert = Alert(
        employee_id=request.employee_id,
        title=request.title,
        description=request.description,
        severity=request.severity,
        risk_score=request.risk_score,
        alert_type=request.alert_type,
        status="Open"
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


@router.put(
    "/{alert_id}",
    response_model=AlertResponse
)
def update_alert(
    alert_id: int,
    request: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = db.query(
        Alert
    ).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(alert, key, value)

    if request.status == "Resolved":
        from datetime import datetime
        alert.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(alert)

    return alert


@router.delete(
    "/{alert_id}"
)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(
        Alert
    ).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    db.delete(alert)
    db.commit()

    return {
        "message": "Alert deleted successfully"
    }


@router.get(
    "/summary/counts"
)
def alert_summary(
    db: Session = Depends(get_db)
):
    alerts = db.query(Alert).all()

    return {
        "total": len(alerts),
        "open": sum(
            1 for alert in alerts
            if alert.status == "Open"
        ),
        "investigating": sum(
            1 for alert in alerts
            if alert.status == "Investigating"
        ),
        "resolved": sum(
            1 for alert in alerts
            if alert.status == "Resolved"
        ),
        "critical": sum(
            1 for alert in alerts
            if alert.severity == "Critical"
        ),
        "high": sum(
            1 for alert in alerts
            if alert.severity == "High"
        ),
        "medium": sum(
            1 for alert in alerts
            if alert.severity == "Medium"
        ),
        "low": sum(
            1 for alert in alerts
            if alert.severity == "Low"
        )
    }