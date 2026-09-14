from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import UserCreate, LoginRequest, RegisterResponse, TokenResponse, UserResponse
from app.services.auth import register_user, authenticate_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    user, token = register_user(db, data)
    return {
        "user": user,
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user, token = authenticate_user(db, data.email, data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user