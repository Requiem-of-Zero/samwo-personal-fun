from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # This hashes the password so we never store raw passwords
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the raw password
    hashed_password = get_password_hash(user_data.password)

    # Create a new User instance (matches the SQLAlchemy model)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hashed_password
    )

    # Add and commit the new user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh gets the updated ID from the DB

    return db_user  # Return the created user object
