from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_family_association = Table(
  "user_family_association",
  Base.metadata,
  Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
  Column("family_id", Integer, ForeignKey("families.id"), primary_key=True)
)