# FastAPI utilities for dependency injection and error handling
from fastapi import Depends, HTTPException, status

# Reads the token from the Authorization header ("Bearer <token>")
from fastapi.security import OAuth2PasswordBearer

# Used to decode JWTs and handle errors
from jose import JWTError, jwt

# SQLAlchemy session type for interacting with the database
from sqlalchemy.orm import Session

# Our database session factory
from app.database import SessionLocal

# Our User ORM model (SQLAlchemy)
from app.models.user import User

# Schema that defines the token payload shape we expect (email as `sub`)
from app.schemas.token_data import TokenData

# This defines how the token will be extracted from requests
# FastAPI will automatically parse the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Secret used to sign JWTs (must match the secret used in create_access_token)
SECRET_KEY = "supersecretkey123"
# Algorithm used to sign the JWT (must also match)
ALGORITHM = "HS256"


# Dependency that provides a database session for each request
def get_db():
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide session to the route that depends on it
    finally:
        db.close()  # Ensure session is always closed


# Dependency to retrieve the current logged-in user from a JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme),  # Extract the token from the request
    db: Session = Depends(get_db),  # Get a DB session for querying
) -> User:
    # Custom HTTPException to raise if token is invalid or user is not found
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # 401 = unauthorized
        detail="Could not validate credentials",  # User-facing error message
        headers={
            "WWW-Authenticate": "Bearer"
        },  # Informs the client to send a Bearer token
    )

    try:
        # Decode the JWT using the same secret and algorithm used when issuing it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the "sub" field from the payload — we use it to store the email
        email: str = payload.get("sub")

        # If no email was found in the token, treat it as invalid
        if email is None:
            raise credentials_exception

        # Store it in a TokenData object for type-checking and validation
        token_data = TokenData(sub=email)

    except JWTError:
        # If token is expired, malformed, or unverifiable
        raise credentials_exception

    # Look up the user in the database using the email from the token
    user = db.query(User).filter(User.email == token_data.sub).first()

    # If no user found, raise error
    if user is None:
        raise credentials_exception

    # ✅ Return the authenticated user to the route that needs it
    return user
