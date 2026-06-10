from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

import json

from app.core.database import get_db

from app.models.candidate import Candidate
from app.models.job import Job as JobModel

from app.services.candidate_service import (
    process_and_store_candidate,
    get_all_candidates,
    get_candidate_by_id,
    delete_candidate,
    attach_keywords
)

from app.services.job_service import (
    fetch_and_store_jobs
)

from app.matching.scorer import (
    compute_match
)


router = APIRouter(
    prefix="/api/candidates",
    tags=["Candidates"]
)

from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_data
# ──────────────────────────────────────────────────────────────────────────────
# Upload Resume
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB"
        )

    candidate = process_and_store_candidate(
        db,
        file_bytes,
        file.filename
    )

    return {
        "message": "Resume processed successfully",

        "candidate_id": candidate.id,

        "profile": {
            "full_name": candidate.full_name,
            "email": candidate.email,
            "current_title": candidate.current_title,
            "years_experience": candidate.years_experience,
            "seniority_level": candidate.seniority_level,

            "skills": (
                json.loads(candidate.skills)
                if candidate.skills
                else []
            ),

            "tools": (
                json.loads(candidate.tools)
                if candidate.tools
                else []
            ),

            "certifications": (
                json.loads(candidate.certifications)
                if candidate.certifications
                else []
            ),

            "education": candidate.education
        }
    }


# ──────────────────────────────────────────────────────────────────────────────
# List Candidates
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/")
def list_candidates(
    db: Session = Depends(get_db)
):

    candidates = get_all_candidates(db)

    return {
        "candidates": [
            {
                "id": c.id,
                "name": c.full_name,
                "title": c.current_title,

                "unified_keywords": (
                    json.loads(c.unified_keywords)
                    if c.unified_keywords
                    else []
                )
            }
            for c in candidates
        ]
    }


# ──────────────────────────────────────────────────────────────────────────────
# Get Candidate
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = get_candidate_by_id(
        db,
        candidate_id
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "id": candidate.id,
        "full_name": candidate.full_name,
        "email": candidate.email,
        "phone": candidate.phone,
        "current_title": candidate.current_title,
        "years_experience": candidate.years_experience,
        "seniority_level": candidate.seniority_level,

        "skills": (
            json.loads(candidate.skills)
            if candidate.skills
            else []
        ),

        "tools": (
            json.loads(candidate.tools)
            if candidate.tools
            else []
        ),

        "certifications": (
            json.loads(candidate.certifications)
            if candidate.certifications
            else []
        ),

        "education": candidate.education,

        "unified_keywords": (
            json.loads(candidate.unified_keywords)
            if candidate.unified_keywords
            else []
        )
    }


# ──────────────────────────────────────────────────────────────────────────────
# Delete Candidate
# ──────────────────────────────────────────────────────────────────────────────

@router.delete("/{candidate_id}")
def remove_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = delete_candidate(
        db,
        candidate_id
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "message": f"Candidate {candidate_id} deleted"
    }


# ──────────────────────────────────────────────────────────────────────────────
# Upload Keywords
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/{candidate_id}/keywords")
async def upload_keywords(
    candidate_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith((".txt", ".csv")):
        raise HTTPException(
            status_code=400,
            detail="Only .txt or .csv files accepted."
        )

    file_bytes = await file.read()

    candidate = attach_keywords(
        db,
        candidate_id,
        file_bytes,
        file.filename
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    unified_keywords = (
        json.loads(candidate.unified_keywords)
        if candidate.unified_keywords
        else []
    )

    return {
        "candidate_id": candidate_id,
        "unified_keywords": unified_keywords,
        "total_keywords": len(unified_keywords)
    }


# ──────────────────────────────────────────────────────────────────────────────
# Fetch Jobs
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/{candidate_id}/fetch-jobs")
def fetch_jobs_for_candidate(
    candidate_id: int,
    location: str = "London",
    country_code: str = "gb",
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    try:
        keywords = json.loads(
            candidate.unified_keywords
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No unified keywords found. Upload keywords first."
        )

    if not keywords:
        raise HTTPException(
            status_code=400,
            detail="Keyword list is empty."
        )

    result = fetch_and_store_jobs(
        candidate_id=candidate_id,
        keywords=keywords,
        location=location,
        country_code=country_code,
        db=db
    )

    return {
        "candidate_id": candidate_id,
        "location": location,
        "country_code": country_code,
        **result
    }


# ──────────────────────────────────────────────────────────────────────────────
# Get Candidate Jobs
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/{candidate_id}/jobs")
def get_jobs_for_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    jobs = (
        db.query(JobModel)
        .filter(
            JobModel.candidate_id == candidate_id
        )
        .order_by(
            JobModel.created_at.desc()
        )
        .all()
    )

    return [
    {
        "id": j.id,
        "title": j.title,
        "company": j.company,
        "location": j.location,
        "country": j.country,
        "salary_min": j.salary_min,
        "salary_max": j.salary_max,
        "posted_at": j.posted_at,
        "job_url": j.job_url,
        "match_score": j.match_score,

        "description_preview": (
            j.description[:200]
            if j.description
            else ""
        ),
    }
    for j in jobs
]


# ──────────────────────────────────────────────────────────────────────────────
# Score Jobs
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/{candidate_id}/score-jobs")
def score_jobs(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    jobs = (
        db.query(JobModel)
        .filter(
            JobModel.candidate_id == candidate_id
        )
        .all()
    )

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail="No jobs found. Run fetch-jobs first."
        )

    results = []

    for job in jobs:

        match = compute_match(
            candidate,
            job
        )

        # Save score + explanation
        job.match_score = match["score"]
        job.match_explanation = match["explanation"]
        job.matched_keywords = json.dumps(match["matched_skills"])
        job.required_skills = json.dumps(
        match["required_skills"]
        )
        print("\nJOB:", job.title)
    print("REQUIRED SKILLS:",
        match["required_skills"]
        )
    results.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "url": job.job_url,

            "posted_at": (
                str(job.posted_at)
                if job.posted_at
                else None
            ),

            **match,
        })

    # Single commit after loop
    db.commit()
    saved_jobs = (
    db.query(JobModel)
    .filter(
        JobModel.candidate_id == candidate_id
    )
    .limit(3)
    .all()
)

    for job in saved_jobs:
        print(
        "DB STORED:",
        job.required_skills
    )
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "candidate_id": candidate_id,
        "total_jobs": len(results),
        "jobs": results
    }


# ──────────────────────────────────────────────────────────────────────────────
# Ranked Jobs
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/{candidate_id}/ranked-jobs")
def ranked_jobs(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    jobs = (
        db.query(JobModel)
        .filter(
            JobModel.candidate_id == candidate_id,
            JobModel.match_score.isnot(None)
        )
        .order_by(
            JobModel.match_score.desc()
        )
        .all()
    )

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail="No scored jobs found. Run score-jobs first."
        )

    return [
        {
            "job_id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "match_score": j.match_score,
            "explanation": j.match_explanation,
            "url": j.job_url,
        }
        for j in jobs
    ]

@router.get(
    "/{candidate_id}/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    data = get_dashboard_data(
        candidate_id,
        db
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return data