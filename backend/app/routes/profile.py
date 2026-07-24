from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import User
from app.schemas.auth import (
    ProfileUpdateRequest,
    UserResponse
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/{user_id}", response_model=UserResponse)
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_profile(
    user_id: int,
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db)
):
    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if request.email:
        existing_user = db.query(
            User
        ).filter(
            User.email == request.email,
            User.id != user_id
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            user,
            key,
            value
        )

    db.commit()
    db.refresh(user)

    return user