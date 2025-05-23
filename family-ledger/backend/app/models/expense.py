from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.database import Base

class Expense(Base):
  __tablename__ = "expenses"

  id = Column(Integer, primary_key=True, index=True) # Unique ID
  amount = Column(Float, nullable=False) # Amount spent
  description = Column(Text, nullable=True) # Optional description
  timestamp = Column(DateTime(timezone=True), server_default=func.now()) # When the expense happened

  payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  family_id = Column(Integer, ForeignKey("families.id"), nullable=True)

  payer = relationship("User", back_populates="expenses_paid")
  family = relationship("Family", back_populates="expenses")