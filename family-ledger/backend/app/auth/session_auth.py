# FastAPI utilities for dependency injection and error handling
from fastapi import Depends, HTTPException, status, Request
# SQLAlchemy session type for interacting with the database
from sqlalchemy.orm import Session
# Our database session factory
from app.database import SessionLocal
# Our User ORM model (SQLAlchemy)
from app.models.user import User

# Dependency that provides a database session for each request
def get_db():
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide session to the route that depends on it
    finally:
        db.close()  # Ensure session is always closed


# Dependency to retrieve the current logged-in user from a JWT token
def get_current_user(
    request: Request,  # Extract the payload from the request
    db: Session = Depends(get_db),  # Get a DB session for querying
) -> User:
    # Read the session cookie (we stored the user ID in login())
    user_id = request.cookies.get("session")

    # If there's no session, the user is not logged in
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="User not found")
    
    return user
