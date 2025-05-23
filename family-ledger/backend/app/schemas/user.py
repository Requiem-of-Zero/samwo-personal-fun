from pydantic import BaseModel, EmailStr

# This schema defines what the client sends when creating a user
class UserCreate(BaseModel):
    email: EmailStr               # Validates email format
    password: str                 # Raw password (will be hashed)
    full_name: str | None = None  # Optional full name

# This schema defines what we return back to the client
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    family_id: int | None = None

    class Config:
        # orm_mode = True  # Tells Pydantic to convert SQLAlchemy objects to dicts
        from_attributes = True

class FriendOut(UserOut):
    can_view_expenses: bool