from pydantic import BaseModel

# Base schema used for both input and output
class FamilyBase(BaseModel):
    name: str  # Family name is required
    description: str | None = None  # Description is optional

# Schema for creating a new family
class FamilyCreate(FamilyBase):
    pass

# Schema returned to the client (includes ID)
class FamilyOut(FamilyBase):
    id: int

    # ✅ Enables automatic conversion from SQLAlchemy model
    class Config:
        from_attributes = True  # (Pydantic v2+ replaces `orm_mode`)
