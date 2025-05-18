from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI utilities
from sqlalchemy.orm import Session                              # For database access
from app.database import SessionLocal                           # DB session
from app.schemas.user import UserCreate                         # For typing/form parsing
from app.models.user import User                                # SQLAlchemy model
from app.auth.token import create_access_token                  # JWT creation
from passlib.context import CryptContext                        # For password hashing

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Setup password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password verification function
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

# Actual login route
@router.post("/auth/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Check if password matches
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate a JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
