from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user
from app.auth.session_auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()  # Create a FastAPI router for user-related endpoints

@router.post("/users/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Optional: Check if user already exists (not yet implemented)

    # Create the user using the CRUD logic
    new_user = create_user(db, user)

    return new_user


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    # Return current user's data (can shape this however you want)
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    """
    Return all users in the system.
    """
    return db.query(User).all()