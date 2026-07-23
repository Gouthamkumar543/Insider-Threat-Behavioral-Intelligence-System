from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.models import LoginActivity, FileAccess
from app.services.risk_engine import calculate_risk_score

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{employee_id}")
def get_alert(employee_id: str, db: Session = Depends(get_db)):
    login_logs = db.query(LoginActivity).filter(
        LoginActivity.employee_id == employee_id
    ).all()

    file_logs = db.query(FileAccess).filter(
        FileAccess.employee_id == employee_id
    ).all()

    score = calculate_risk_score(login_logs, file_logs)

    if score >= 70:
        return {
            "employee_id": employee_id,
            "alert": True,
            "severity": "HIGH",
            "risk_score": score,
            "message": "High insider threat detected."
        }

    elif score >= 40:
        return {
            "employee_id": employee_id,
            "alert": True,
            "severity": "MEDIUM",
            "risk_score": score,
            "message": "Suspicious activity detected."
        }

    return {
        "employee_id": employee_id,
        "alert": False,
        "severity": "LOW",
        "risk_score": score,
        "message": "No suspicious activity."
    }