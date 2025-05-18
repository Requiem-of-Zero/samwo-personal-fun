from sqlalchemy import Column, Integer, String
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
