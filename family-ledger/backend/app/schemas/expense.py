from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema for creation
class ExpenseCreate(BaseModel):
  amount: float
  description: str | None = None

class ExpenseOut(BaseModel):
  id: int
  amount: float
  description: str | None
  timestamp: datetime
  payer_id: int
  family_id: Optional[int] = None

  class Config:
    from_attributes = True