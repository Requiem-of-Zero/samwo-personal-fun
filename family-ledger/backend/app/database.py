from sqlalchemy import create_engine
# This creates a connection to the database using your DATABASE_URL.

from sqlalchemy.ext.declarative import declarative_base
# This is used to define a base class that all your ORM models will extend.

from sqlalchemy.orm import sessionmaker
# This is used to create "session" objects that handle queries, inserts, updates.
# Connection string to SQLite database — later you'll swap this with PostgreSQL
DATABASE_URL = "sqlite:///./test.db"

# Create the engine that handles the actual connection
# The SQLite-specific option "check_same_thread" allows us to use the same connection across threads (only needed for SQLite)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# This is a factory that will create new DB sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is used as a superclass for all your ORM models
Base = declarative_base()