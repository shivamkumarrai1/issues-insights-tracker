import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, issues, users, sse
from app.core.config import settings
from app.db.session import engine
from app.models import base  # Ensure models are registered
from app.worker.jobs import start_scheduler
from app.api import users
from app.api import sse 
from app.jobs.scheduler import start_scheduler

app = FastAPI(title="Issues & Insights Tracker")
origins = [
    "http://localhost:5173",  # Svelte dev server
    "https://your-frontend-url.vercel.app"  # Update later for production
]

# CORS (adjust for frontend URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can lock this down to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
# Routers under /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(sse.router, prefix="/api/stream", tags=["Realtime"])

# Create DB tables on startup
base.Base.metadata.create_all(bind=engine)

# Start background scheduler
start_scheduler()
@app.get("/")
def root():
    return {"message": "Backend running successfully"}


# Include the streaming route



