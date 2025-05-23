from fastapi import FastAPI
# This is the core class used to initialize your FastAPI app.
from starlette.middleware.sessions import SessionMiddleware # Middleware for session tokens
from app.database import engine, Base
# These are used to create the database tables at startup with Base.metadata.create_all.

from app.models import user
# This makes sure the User model is loaded and registered when the app starts.

from app.routes import user as user_router
from app.routes import auth as auth_router
from app.routes import family as family_router
from app.routes import expense as expenses_router
from app.routes import friend as friends_router
# This includes the route handlers you’ll define in app/routes/user.py (like POST /users).

app = FastAPI()  # Initializes the FastAPI app


app.add_middleware(SessionMiddleware, secret_key="your-session-secret-key")

# This creates all tables defined by your Base subclasses (e.g., User)
# If the tables already exist, it does nothing
Base.metadata.create_all(bind=engine) 

app.include_router(user_router.router) # Register the /users route
app.include_router(auth_router.router) # Register the /auth routes
app.include_router(family_router.router) # Register the /family routes
app.include_router(expenses_router.router) # Register the /expenses routes
app.include_router(friends_router.router) # Register the /friends routes

@app.get("/health")
def health():
    return {"status": "ok"}
# Simple test route — you can open http://localhost:8000/health to see if the API is running
