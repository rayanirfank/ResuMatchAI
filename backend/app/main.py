from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.candidates import router as candidates_router
from app.api.career_intelligence import router as career_router

# FastAPI app instance — must be created FIRST
app = FastAPI(
    title="ResuMatch API",
    description="AI-powered job matching platform",
    version="1.0.0"
)

# CORS middleware — must be added BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(candidates_router)

# Health check
@app.get("/")
def health_check():
    return {"status": "ResuMatch API is running"}

app.include_router(career_router)