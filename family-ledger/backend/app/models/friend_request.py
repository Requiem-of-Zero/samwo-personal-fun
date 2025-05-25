from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.database import Base

class FriendRequest(Base):
  __tablename__= "friend_requests"

  id = Column(Integer, primary_key=True, index=True)
  from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  accepted = Column(Boolean, default=False)