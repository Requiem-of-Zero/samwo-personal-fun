from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import update, insert, delete
from app.models.user import User
from app.schemas.user import FriendOut
from app.database import SessionLocal, get_db
from app.auth.session_auth import get_current_user
from app.models.association import friend_visibility
from typing import List
from random import randint, choice
from decimal import Decimal

# Initialize a new router for friend-related endpoints
router = APIRouter()

# Add a user as a friend
@router.post("/users/{friend_id}/add-friend", response_model=FriendOut)
def add_friend(friend_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if friend_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot add yourself as a friend")

    friend = db.query(User).filter(User.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if friend in current_user.friends:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already friends")

    current_user.friends.append(friend)

    # Grant expense visibility both ways
    db.execute(insert(friend_visibility).values([
        {"user_id": friend.id, "friend_id": current_user.id, "can_view_expenses": True},
        {"user_id": current_user.id, "friend_id": friend.id, "can_view_expenses": True}
    ]))
    db.commit()
    db.refresh(current_user)

    return FriendOut(**friend.__dict__, can_view_expenses=False)

# List friends with visibility flags
@router.get("/me/friends", response_model=List[FriendOut])
def list_friends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    friends = []
    for friend in current_user.friends:
        row = db.execute(
            friend_visibility.select().where(
                (friend_visibility.c.user_id == friend.id) &
                (friend_visibility.c.friend_id == current_user.id)
            )
        ).first()
        can_view = row.can_view_expenses if row else False
        friends.append(FriendOut(**friend.__dict__, can_view_expenses=can_view)) # Appened every friend
    return friends

# Update a specific friend's visibility permission
@router.patch("/me/friends/{friend_id}/toggle-expense-visibility")
def toggle_friend_expense_visibility(friend_id: int, visible: bool, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if friend_id not in [f.id for f in current_user.friends]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not friends with this user")

    result = db.execute(
        update(friend_visibility)
        .where((friend_visibility.c.user_id == friend_id) & (friend_visibility.c.friend_id == current_user.id))
        .values(can_view_expenses=visible)
    )
    if result.rowcount == 0:
        db.execute(
            insert(friend_visibility).values(user_id=friend_id, friend_id=current_user.id, can_view_expenses=visible)
        )

    db.commit()
    return {"message": "Visibility updated."}

