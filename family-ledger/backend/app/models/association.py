from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from app.database import Base

user_family_association = Table(
  "user_family_association",
  Base.metadata,
  Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
  Column("family_id", Integer, ForeignKey("families.id"), primary_key=True)
)

friend_association = Table(
  "friend_association",
  Base.metadata,
  Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
  Column("friend_id", Integer, ForeignKey("users.id"), primary_key=True)
)

friend_visibility = Table(
    "friend_visibility",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("can_view_expenses", Boolean, default=True)
)