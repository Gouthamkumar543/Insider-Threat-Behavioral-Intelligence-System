from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.models import FileAccess


router = APIRouter(
    prefix="/files",
    tags=["File Access"]
)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Record file access activity
@router.post("/")
def create_file_access(
    employee_id: str,
    file_name: str,
    action: str,
    db: Session = Depends(get_db)
):

    file_activity = FileAccess(
        employee_id=employee_id,
        file_name=file_name,
        action=action
    )

    db.add(file_activity)
    db.commit()
    db.refresh(file_activity)

    return file_activity


# Get all file activities
@router.get("/")
def get_file_access(
    db: Session = Depends(get_db)
):

    files = db.query(FileAccess).all()

    return files