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
from app.models.friend_request import FriendRequest

# Initialize a new router for friend-related endpoints
router = APIRouter()

# Send a friend request
@router.post("/users/{to_user_id}/send-friend-request")
def send_request(to_user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Prevent self-friend request
    if current_user.id == to_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot send request to yourself")

    # Prevent duplicates
    existing = db.query(FriendRequest).filter_by(from_user_id=current_user.id, to_user_id=to_user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Friend request already sent")

    req = FriendRequest(from_user_id=current_user.id, to_user_id=to_user_id)
    db.add(req)
    db.commit()
    return {"message": "Friend request sent"}

# Accept a friend request
@router.post("/friend-requests/{request_id}/accept")
def accept_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    req = db.query(FriendRequest).filter_by(id=request_id).first()
    if not req or req.to_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    # Create mutual friendship
    user_from = db.query(User).filter(User.id == req.from_user_id).first()
    user_to = db.query(User).filter(User.id == req.to_user_id).first()

    user_from.friends.append(user_to)
    user_to.friends.append(user_from)

    req.accepted = True
    db.commit()

    return {"message": "Friend request accepted"}

# Get my friend requests
@router.get("/me/friend-requests")
def incoming_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    requests = db.query(FriendRequest).filter_by(to_user_id=current_user.id, accepted=False).all()
    return requests


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

