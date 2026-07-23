from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import jwt

from app.database.database import get_db
from app.models.models import User
from app.schemas.auth import RegisterRequest, LoginResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


SECRET_KEY = "insider-ai-secret-key-change-this-later"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


@router.post("/register")
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    hashed_password = hash_password(
        user_data.password
    )


    new_user = User(

        name=user_data.name,

        email=user_data.email,

        password=hashed_password,

        role=user_data.role

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {

        "message": "Account created successfully",

        "user": {

            "id": new_user.id,

            "name": new_user.name,

            "email": new_user.email,

            "role": new_user.role

        }

    }


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = (

        db.query(User)

        .filter(

            User.email == form_data.username

        )

        .first()

    )


    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password"

        )


    password_valid = verify_password(

        form_data.password,

        user.password

    )


    if not password_valid:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password"

        )


    access_token = create_access_token(

        data={

            "sub": str(user.id),

            "email": user.email,

            "role": user.role

        }

    )


    return {

        "access_token": access_token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role

        }

    }