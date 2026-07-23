from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.models import LoginActivity


router = APIRouter(
    prefix="/login",
    tags=["Login Activity"]
)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Record login activity
@router.post("/")
def create_login_activity(
    employee_id: str,
    ip_address: str,
    location: str,
    success: bool,
    db: Session = Depends(get_db)
):

    login = LoginActivity(
        employee_id=employee_id,
        ip_address=ip_address,
        location=location,
        success=success
    )

    db.add(login)
    db.commit()
    db.refresh(login)

    return login


# Get login history
@router.get("/")
def get_login_activity(
    db: Session = Depends(get_db)
):

    logs = db.query(LoginActivity).all()

    return logs