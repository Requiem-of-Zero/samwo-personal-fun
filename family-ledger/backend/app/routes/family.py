from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.family import Family
from app.schemas.family import FamilyCreate, FamilyOut
from app.auth.session_auth import get_current_user
from app.schemas.user import UserOut
from app.models.user import User
from app.models.expense import Expense
from app.schemas.expense import ExpenseOut
from typing import List

router = APIRouter()


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new family (public route for now)
@router.post("/create/family", response_model=FamilyOut)
def create_family(family_data: FamilyCreate, db: Session = Depends(get_db)):
    # Check if family name already exists (unique constraint)
    existing = db.query(Family).filter(Family.id == family_data.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Family already exists"
        )

    # Create new Family object
    new_family = Family(name=family_data.name, description=family_data.description)

    # Add and commit to DB
    db.add(new_family)
    db.commit()
    db.refresh(new_family)  # Load DB-generated values like `id`

    return new_family


# Authenticated user joins a family by ID
@router.post("/families/{family_id}/join", response_model=FamilyOut)
def join_family(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Find the family by ID
    family = db.query(Family).filter(Family.id == family_id).first()

    # If it doesn't exist, raise 404
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Family not found"
        )
    
    if family in current_user.families:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already a member of this family")

    # Update the user's family_id
    current_user.families.append(family)
    db.commit()

    return family  # Return the family the user joined

@router.post("/me/set-primary-family/{family_id}")
def set_primary_family(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if family_id not in [f.id for f in current_user.families]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this family")
    
    current_user.primary_family_id = family_id
    db.commit()

    return {"message": f"Primary family set to ID {family_id}"}

@router.get("/families/{family_id}", response_model=FamilyOut)
def get_family(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    family = db.query(Family).filter(Family.id == family_id).first()

    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No family found")

    if family_id not in [f.id for f in current_user.families]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this family")
        
    return family

# Get all member of the logged-in user's families
@router.get("/families/me/members", response_model=List[UserOut])
def get_my_family_members(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if not current_user.families:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not in a family"
        )

    members_set = set()
    for family in current_user.families:
        members_set.update(family.members)

    return list(members_set)

# Get all the logged-in user's family members
@router.get("/families/{family_id}/members", response_model=List[UserOut])
def get_family_members(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    family = db.query(Family).filter(Family.id == family_id).first()

    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No family found")
    
    print("User families:", [f.name for f in current_user.families])
    
    if family.id not in [f.id for f in current_user.families]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this family's members")
    

    return family.members

@router.get("/families/{family_id}/expenses", response_model=List[ExpenseOut])
def get_family_expenses(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the user belongs to this family
    if family_id not in [f.id for f in current_user.families]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this family's expenses")

    return (
        db.query(Expense)
        .filter(Expense.family_id == family_id)
        .order_by(Expense.timestamp.desc())
        .all()
    )
