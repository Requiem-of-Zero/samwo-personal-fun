from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.association import user_family_association, friend_association, friend_visibility
# These are SQLAlchemy column types you use to define your DB schema.

from app.database import Base

# You inherit from Base to register this class as a database table.


class User(Base):  # This class maps to the "users" table
    __tablename__ = "users"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    # Primary key; "index=True" speeds up lookups by ID

    email = Column(String, unique=True, index=True, nullable=False)
    # Required field; indexed for fast lookup; must be unique
    
    full_name = Column(String, nullable=True)
    # Optional field — a user doesn't have to provide this

    password_hash = Column(String, nullable=False)
    # Required field — used to store the hashed password
    primary_family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    primary_family = relationship("Family", foreign_keys=[primary_family_id])

    families = relationship(
        "Family",
        secondary=user_family_association,
        back_populates="members"
    )

    friends = relationship(
        "User",
        secondary=friend_association,
        primaryjoin=id==friend_association.c.user_id,
        secondaryjoin=id==friend_association.c.friend_id,
        backref="friend_of"
    )

    visible_to = relationship(
        "User",
        secondary=friend_visibility,
        primaryjoin=id == friend_visibility.c.user_id,
        secondaryjoin=id == friend_visibility.c.friend_id,
        viewonly=True
    )

    expenses_paid = relationship("Expense", back_populates="payer")
