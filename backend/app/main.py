from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import auth, tasks, notes
from .routers.users import router as users_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    # Don't redirect when URLs have trailing slashes
    redirect_slashes=False
)

# Configure CORS
origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",  # React development server alternative
    "http://localhost:5173",  # Vite development server
    "http://127.0.0.1:5173",  # Vite development server alternative
    "http://localhost:8000",  # Backend server
    "http://127.0.0.1:8000",  # Backend server alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API"} 