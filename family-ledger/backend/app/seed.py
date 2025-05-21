from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.family import Family
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔁 Create the tables
Base.metadata.create_all(bind=engine)

# Get a new DB session
db: Session = SessionLocal()

# Create sample families
family1 = Family(name="Wong Family", description="Family of Samuel Wong")
family2 = Family(name="Tech Enthusiasts", description="A tech-savvy group")
family3 = Family(name="Gym Bros", description="A gym family")

db.add_all([family1, family2, family3])
db.commit()

# Create sample users
user1 = User(
    email="sam@example.com",
    full_name="Sam Wong",
    password_hash=pwd_context.hash("dummy"),
)
user2 = User(
    email="jane@example.com",
    full_name="Jane Smith",
    password_hash=pwd_context.hash("dummy"),
)
user3 = User(
    email="bob@example.com", full_name="Bob Li", password_hash=pwd_context.hash("dummy")
)

# Join users to families (many-to-many)
user1.families.append(family1)
user2.families.append(family1)
user2.families.append(family2)
user3.families.append(family2)

db.add_all([user1, user2, user3])
db.commit()

print("Seed data inserted.")
db.close()
