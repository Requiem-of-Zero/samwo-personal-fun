from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User, friend_association, friend_visibility
from app.models.family import Family
from app.models.expense import Expense
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy import insert

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
user1 = User(email="sam@example.com", full_name="Sam Wong", password_hash=pwd_context.hash("dummy"))
user2 = User(email="jane@example.com", full_name="Jane Smith", password_hash=pwd_context.hash("dummy"))
user3 = User(email="bob@example.com", full_name="Bob Li", password_hash=pwd_context.hash("dummy"))
user4 = User(email="alice@example.com", full_name="Alice Tan", password_hash=pwd_context.hash("dummy"))
user5 = User(email="mike@example.com", full_name="Mike Doe", password_hash=pwd_context.hash("dummy"))

# Add users to families
user1.families.append(family1)
user2.families.append(family1)
user2.families.append(family2)
user3.families.append(family2)
user4.families.append(family3)
db.add_all([user1, user2, user3, user4, user5])
db.commit()

# Create friend relationships
user1.friends.extend([user2, user3])
user2.friends.append(user1)
user3.friends.append(user1)
user2.friends.append(user4)
user4.friends.extend([user2, user3])
user5.friends.append(user4)
user4.friends.append(user5)
db.commit()

# Add expense visibility settings
db.execute(insert(friend_visibility).values([
    {"user_id": user2.id, "friend_id": user1.id, "can_view_expenses": True},
    {"user_id": user3.id, "friend_id": user1.id, "can_view_expenses": False},
    {"user_id": user4.id, "friend_id": user2.id, "can_view_expenses": True},
    {"user_id": user4.id, "friend_id": user3.id, "can_view_expenses": True},
    {"user_id": user5.id, "friend_id": user4.id, "can_view_expenses": False},
]))
db.commit()

# --- Expenses ---
expenses = [
    Expense(amount=45.00, description="Grocery run", timestamp=datetime.now(timezone.utc) - timedelta(days=1), payer_id=user1.id, family_id=family1.id),
    Expense(amount=120.00, description="Netflix + Spotify", timestamp=datetime.now(timezone.utc) - timedelta(days=2), payer_id=user1.id, family_id=None),
    Expense(amount=75.50, description="Dinner", timestamp=datetime.now(timezone.utc), payer_id=user2.id, family_id=family2.id),
    Expense(amount=20.00, description="Protein powder", timestamp=datetime.now(timezone.utc) - timedelta(days=3), payer_id=user4.id, family_id=family3.id),
    Expense(amount=9.99, description="Coffee", timestamp=datetime.now(timezone.utc) - timedelta(hours=5), payer_id=user3.id, family_id=None)
]

db.add_all(expenses)
db.commit()

# Add more realistic and varied expenses
more_expenses = [
    Expense(
        amount=89.99,
        description="Weekly groceries",
        timestamp=datetime.now(timezone.utc) - timedelta(days=1),
        payer_id=user2.id,
        family_id=family1.id
    ),
    Expense(
        amount=23.45,
        description="Uber ride to meetup",
        timestamp=datetime.now(timezone.utc) - timedelta(days=2),
        payer_id=user3.id,
        family_id=None  # personal
    ),
    Expense(
        amount=300.00,
        description="New gaming monitor",
        timestamp=datetime.now(timezone.utc) - timedelta(days=5),
        payer_id=user1.id,
        family_id=None  # personal
    ),
    Expense(
        amount=150.00,
        description="Shared dinner at fancy restaurant",
        timestamp=datetime.now(timezone.utc) - timedelta(days=3),
        payer_id=user2.id,
        family_id=family2.id
    ),
    Expense(
        amount=10.00,
        description="Coffee beans",
        timestamp=datetime.now(timezone.utc) - timedelta(hours=20),
        payer_id=user4.id,
        family_id=family3.id
    ),
    Expense(
        amount=99.99,
        description="Gym shoes",
        timestamp=datetime.now(timezone.utc) - timedelta(days=4),
        payer_id=user4.id,
        family_id=None
    ),
    Expense(
        amount=49.00,
        description="Dinner with friends",
        timestamp=datetime.now(timezone.utc) - timedelta(days=2),
        payer_id=user1.id,
        family_id=family1.id
    ),
    Expense(
        amount=8.99,
        description="Bubble tea",
        timestamp=datetime.now(timezone.utc) - timedelta(hours=3),
        payer_id=user3.id,
        family_id=family2.id
    ),
    Expense(
        amount=12.49,
        description="Lunch at cafe",
        timestamp=datetime.now(timezone.utc) - timedelta(days=1),
        payer_id=user2.id,
        family_id=None
    ),
    Expense(
        amount=59.95,
        description="Books from bookstore",
        timestamp=datetime.now(timezone.utc) - timedelta(days=6),
        payer_id=user1.id,
        family_id=None
    ),
]

db.add_all(more_expenses)
db.commit()

print("✅ Seed data inserted.")
db.close()
