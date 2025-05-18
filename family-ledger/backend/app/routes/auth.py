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
def login(user_data: UserCreate, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    # Check if user exists or password doesn't matches
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    # Generate a JWT token for storing individual JWT locally
    # access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(key="session", value=str(user.id), httponly=True, secure=False)

    return {"message": "Logged in successfully"}

@router.post("/auth/logout")
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="session")

    return {"message": f"Logged out {current_user.email} successfully"}