# Import SQLAlchemy tools to define models and columns
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.association import user_family_association
from app.database import Base  # Import the declarative base class


# Define a Family model/table
class Family(Base):
    __tablename__ = "families"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique family ID
    name = Column(String, unique=True, index=True)  # Family name (e.g. "Wong Family")
    description = Column(String, nullable=True)  # Optional description or tagline

    members = relationship(
        "User",
        secondary=user_family_association,
        back_populates="families"
    )