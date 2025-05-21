from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.database import get_db

router = APIRouter()

@router.post("/users/")
async def create_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    try:
        user = UserService.create_user(db, username, email, password)
        return user.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"message": "Login successful"}