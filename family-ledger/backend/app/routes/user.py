from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user
from app.auth.session_auth import get_current_user
from app.models.user import User

router = APIRouter()  # Create a FastAPI router for user-related endpoints


# Dependency that gives us a database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Gives the route access to the DB
    finally:
        db.close()  # Always close the session after use


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
