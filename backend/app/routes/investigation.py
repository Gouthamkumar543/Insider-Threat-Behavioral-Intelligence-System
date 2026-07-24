from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Investigation
from app.schemas.investigation import (
    InvestigationCreate,
    InvestigationUpdate,
    InvestigationResponse
)

router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"]
)


@router.get(
    "/",
    response_model=list[InvestigationResponse]
)
def get_investigations(
    db: Session = Depends(get_db)
):
    return db.query(
        Investigation
    ).order_by(
        Investigation.created_at.desc()
    ).all()


@router.get(
    "/{investigation_id}",
    response_model=InvestigationResponse
)
def get_investigation(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    investigation = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    if not investigation:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found"
        )

    return investigation


@router.post(
    "/",
    response_model=InvestigationResponse
)
def create_investigation(
    request: InvestigationCreate,
    db: Session = Depends(get_db)
):
    investigation = Investigation(
        employee_id=request.employee_id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        assigned_to=request.assigned_to,
        status="Open"
    )

    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    return investigation


@router.put(
    "/{investigation_id}",
    response_model=InvestigationResponse
)
def update_investigation(
    investigation_id: int,
    request: InvestigationUpdate,
    db: Session = Depends(get_db)
):
    investigation = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    if not investigation:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found"
        )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            investigation,
            key,
            value
        )

    db.commit()
    db.refresh(investigation)

    return investigation


@router.delete(
    "/{investigation_id}"
)
def delete_investigation(
    investigation_id: int,
    db: Session = Depends(get_db)
):
    investigation = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    if not investigation:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found"
        )

    db.delete(investigation)
    db.commit()

    return {
        "message": "Investigation deleted successfully"
    }


@router.get(
    "/summary/counts"
)
def investigation_summary(
    db: Session = Depends(get_db)
):
    investigations = db.query(
        Investigation
    ).all()

    return {
        "total": len(investigations),
        "open": sum(
            1 for item in investigations
            if item.status == "Open"
        ),
        "in_progress": sum(
            1 for item in investigations
            if item.status == "In Progress"
        ),
        "closed": sum(
            1 for item in investigations
            if item.status == "Closed"
        ),
        "critical": sum(
            1 for item in investigations
            if item.priority == "Critical"
        ),
        "high": sum(
            1 for item in investigations
            if item.priority == "High"
        ),
        "medium": sum(
            1 for item in investigations
            if item.priority == "Medium"
        ),
        "low": sum(
            1 for item in investigations
            if item.priority == "Low"
        )
    }