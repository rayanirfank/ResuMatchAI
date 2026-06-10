import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

# __init__ files
write_file('app/__init__.py', '')
write_file('app/api/__init__.py', '')
write_file('app/core/__init__.py', '')
write_file('app/models/__init__.py', '')
write_file('app/schemas/__init__.py', '')
write_file('app/services/__init__.py', '')
write_file('app/parsing/__init__.py', '')
write_file('app/matching/__init__.py', '')

# config.py
write_file('app/core/config.py', '''from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID", "0b7e6266")
    ADZUNA_APP_KEY: str = os.getenv("ADZUNA_APP_KEY", "b26cfc1fe8b398176d7466875f0ce53b")
    DATABASE_URL: str = "sqlite:///./resumatch.db"

settings = Settings()
''')

# database.py
write_file('app/core/database.py', '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

# models
write_file('app/models/__init__.py', '''from app.models.candidate import Candidate
from app.models.job import Job
''')

write_file('app/models/candidate.py', '''from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(100), nullable=True)
    current_title = Column(String(255), nullable=True)
    years_experience = Column(Integer, nullable=True)
    seniority_level = Column(String(50), nullable=True)
    skills = Column(Text, nullable=True)
    tools = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')

write_file('app/models/job.py', '''from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, nullable=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    seniority_level = Column(String(50), nullable=True)
    url = Column(String(500), nullable=True)
    source = Column(String(100), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')

# resume_parser.py
write_file('app/parsing/resume_parser.py', '''import fitz
import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

SKILLS_MASTER = [
    "python", "sql", "java", "scala", "r", "javascript", "typescript",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analysis", "data engineering", "data science", "statistics",
    "feature engineering", "model deployment", "etl", "data pipelines",
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "aws", "gcp", "azure", "bigquery", "redshift", "snowflake",
    "spark", "hadoop", "kafka", "airflow", "dbt", "luigi",
    "docker", "kubernetes", "terraform", "git", "ci/cd",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "power bi", "tableau", "looker", "excel",
    "communication", "leadership", "teamwork", "problem solving",
    "agile", "scrum", "project management"
]

TOOLS_MASTER = [
    "bigquery", "redshift", "snowflake", "databricks", "spark",
    "airflow", "dbt", "kafka", "luigi", "prefect",
    "docker", "kubernetes", "terraform", "jenkins", "github actions",
    "aws", "gcp", "azure", "s3", "ec2", "lambda",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "power bi", "tableau", "looker", "excel", "google sheets",
    "jira", "confluence", "slack", "git", "github", "gitlab"
]

SENIORITY_KEYWORDS = {
    "vp": ["vp", "vice president", "head of", "director"],
    "lead": ["lead", "principal", "staff", "architect", "manager"],
    "senior": ["senior", "sr.", "sr "],
    "mid": ["mid", "intermediate", "associate"],
    "junior": ["junior", "jr.", "jr ", "entry", "graduate", "intern"]
}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def extract_email(text: str):
    match = re.search(r"[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text: str):
    match = re.search(r"[\\+]?[\\d][\\d\\s\\-\\.\\(\\)]{7,}[\\d]", text)
    return match.group(0).strip() if match else None

def extract_name(text: str):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text: str):
    text_lower = text.lower()
    found = []
    for skill in SKILLS_MASTER:
        if skill in text_lower and skill not in found:
            found.append(skill)
    return found

def extract_tools(text: str):
    text_lower = text.lower()
    found = []
    for tool in TOOLS_MASTER:
        if tool in text_lower and tool not in found:
            found.append(tool)
    return found

def extract_years_experience(text: str):
    patterns = [
        r"(\\d+)\\+?\\s*years? of experience",
        r"(\\d+)\\+?\\s*years? experience",
        r"experience of (\\d+)\\+?\\s*years?",
        r"(\\d+)\\+?\\s*yrs? of experience",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0

def extract_seniority(text: str, years: int):
    text_lower = text.lower()
    for level, keywords in SENIORITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return level
    if years >= 12:
        return "vp"
    elif years >= 8:
        return "lead"
    elif years >= 5:
        return "senior"
    elif years >= 2:
        return "mid"
    else:
        return "junior"

def extract_current_title(text: str):
    lines = text.strip().split("\\n")
    title_keywords = [
        "engineer", "analyst", "scientist", "developer", "manager",
        "architect", "consultant", "director", "lead", "vp", "head"
    ]
    for line in lines[:15]:
        line_clean = line.strip()
        if 3 < len(line_clean) < 80:
            if any(kw in line_clean.lower() for kw in title_keywords):
                return line_clean
    return None

def extract_certifications(text: str):
    cert_keywords = [
        "aws certified", "google certified", "azure certified",
        "pmp", "cfa", "cissp", "cpa", "gcp certified",
        "tensorflow certificate", "databricks certified",
        "professional certificate", "certification"
    ]
    text_lower = text.lower()
    found = []
    for cert in cert_keywords:
        if cert in text_lower:
            found.append(cert.title())
    return found

def extract_education(text: str):
    edu_keywords = [
        "phd", "ph.d", "doctorate",
        "master", "msc", "mba", "m.s", "m.eng",
        "bachelor", "bsc", "b.s", "b.eng", "b.tech",
        "associate", "diploma"
    ]
    text_lower = text.lower()
    for kw in edu_keywords:
        if kw in text_lower:
            return kw.title()
    return None

def parse_resume_with_ai(raw_text: str) -> dict:
    years = extract_years_experience(raw_text)
    return {
        "full_name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "current_title": extract_current_title(raw_text),
        "years_experience": years,
        "seniority_level": extract_seniority(raw_text, years),
        "skills": extract_skills(raw_text),
        "tools": extract_tools(raw_text),
        "certifications": extract_certifications(raw_text),
        "education": extract_education(raw_text)
    }
''')

# candidate_service.py
write_file('app/services/candidate_service.py', '''from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.parsing.resume_parser import extract_text_from_pdf, parse_resume_with_ai
import json

def process_and_store_candidate(db: Session, file_bytes: bytes, filename: str) -> Candidate:
    raw_text = extract_text_from_pdf(file_bytes)
    parsed = parse_resume_with_ai(raw_text)
    candidate = Candidate(
        filename=filename,
        raw_text=raw_text,
        full_name=parsed.get("full_name"),
        email=parsed.get("email"),
        phone=parsed.get("phone"),
        current_title=parsed.get("current_title"),
        years_experience=parsed.get("years_experience"),
        seniority_level=parsed.get("seniority_level"),
        skills=json.dumps(parsed.get("skills", [])),
        tools=json.dumps(parsed.get("tools", [])),
        certifications=json.dumps(parsed.get("certifications", [])),
        education=parsed.get("education")
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def get_all_candidates(db: Session):
    return db.query(Candidate).all()

def get_candidate_by_id(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def delete_candidate(db: Session, candidate_id: int):
    candidate = get_candidate_by_id(db, candidate_id)
    if candidate:
        db.delete(candidate)
        db.commit()
    return candidate
''')

# candidates.py API route
write_file('app/api/candidates.py', '''from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.candidate_service import (
    process_and_store_candidate,
    get_all_candidates,
    get_candidate_by_id,
    delete_candidate
)
import json

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")
    candidate = process_and_store_candidate(db, file_bytes, file.filename)
    return {
        "message": "Resume processed successfully",
        "candidate_id": candidate.id,
        "profile": {
            "full_name": candidate.full_name,
            "email": candidate.email,
            "current_title": candidate.current_title,
            "years_experience": candidate.years_experience,
            "seniority_level": candidate.seniority_level,
            "skills": json.loads(candidate.skills) if candidate.skills else [],
            "tools": json.loads(candidate.tools) if candidate.tools else [],
            "certifications": json.loads(candidate.certifications) if candidate.certifications else [],
            "education": candidate.education
        }
    }

@router.get("/")
def list_candidates(db: Session = Depends(get_db)):
    candidates = get_all_candidates(db)
    return {"candidates": [{"id": c.id, "name": c.full_name, "title": c.current_title} for c in candidates]}

@router.delete("/{candidate_id}")
def remove_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = delete_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": f"Candidate {candidate_id} deleted"}
''')

# main.py
write_file('app/main.py', '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.candidates import router as candidates_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ResuMatch API",
    description="AI-powered job matching platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates_router)

@app.get("/")
def health_check():
    return {"status": "ResuMatch API is running"}
''')

print("\nAll files created successfully.")