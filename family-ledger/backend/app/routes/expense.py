from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal, get_db
from app.auth.session_auth import get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseOut
from app.models.association import friend_visibility

router = APIRouter()

@router.post("/expenses/create", response_model=ExpenseOut)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # check if user has a primary family, otherwise allow personal expense
    family_id = current_user.primary_family_id

    new_expense = Expense(
        amount = expense_data.amount,
        description=expense_data.description,
        payer_id=current_user.id,
        family_id=family_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/me/expenses/", response_model=List[ExpenseOut])
def get_my_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return(
        db.query(Expense).filter(Expense.payer_id == current_user.id).order_by(Expense.timestamp.desc()).all()
    )

@router.get("/friends/{friend_id}/expenses", response_model=List[ExpenseOut])
def get_friend_expenses(friend_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    friend = db.query(User).filter(User.id == friend_id).first()
    print("Current user ID:", current_user.id)
    print("Friend ID:", friend.id if friend else None)
    print("Current user's friends:", [f.id for f in current_user.friends])
    # print("=== EXPENSES ROUTE HIT ===")
    # return []
    if not friend or friend.id not in [f.id for f in current_user.friends]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not friends with this user")

    row = db.execute(
        friend_visibility.select().where(
            (friend_visibility.c.user_id == friend_id) &
            (friend_visibility.c.friend_id == current_user.id)
        )
    ).first()

    if not row or not row.can_view_expenses:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user does not share their expenses with you")

    return db.query(Expense).filter(Expense.payer_id == friend_id).all()