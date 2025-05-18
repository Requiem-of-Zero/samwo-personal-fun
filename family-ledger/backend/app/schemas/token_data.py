from pydantic import BaseModel # Imported to create a token data model

class TokenData(BaseModel):
  sub: str # Usually the email (or user ID) stored in the token