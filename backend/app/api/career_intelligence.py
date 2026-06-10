import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.skill_gap_service import SkillGapService
from app.services.resume_suggestion_service import (
    ResumeSuggestionService
)
from app.services.career_recommendation_service import (
    CareerRecommendationService
)
from app.services.salary_intelligence_service import (
    SalaryIntelligenceService
)
from app.services.ats_analysis_service import (
    ATSAnalysisService
)
router = APIRouter(
    prefix="/api/career-intelligence",
    tags=["Career Intelligence"]
)


@router.get("/{candidate_id}/skill-gap")
def get_skill_gap(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate skill gap analysis
    for a candidate.
    """

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
    db.query(Job)
    .filter(
        Job.candidate_id == candidate_id,
        Job.match_score.isnot(None)
    )
    .order_by(
        Job.match_score.desc()
    )
    .limit(10)
    .all()
)

    skills = candidate.skills

    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except Exception:
            skills = []

    analysis = SkillGapService.analyze(
        candidate_skills=skills,
        jobs=jobs
    )

    return {
        "candidate_id": candidate_id,
        "analysis": analysis
    }
@router.get("/{candidate_id}/resume-suggestions")
def get_resume_suggestions(
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
        db.query(Job)
        .filter(
            Job.candidate_id == candidate_id,
            Job.match_score.isnot(None)
        )
        .order_by(
            Job.match_score.desc()
        )
        .limit(10)
        .all()
    )

    skills = candidate.skills

    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except Exception:
            skills = []

    skill_gap_analysis = (
        SkillGapService.analyze(
            candidate_skills=skills,
            jobs=jobs
        )
    )

    suggestions = (
        ResumeSuggestionService.generate(
            skill_gap_analysis
        )
    )

    return {
    "candidate_id": candidate_id,

    "top_missing_skills": (
        skill_gap_analysis.get(
            "missing_skills",
            []
        )[:5]
    ),

    "resume_suggestions": suggestions
}
@router.get("/{candidate_id}/career-recommendations")
def get_career_recommendations(
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
        db.query(Job)
        .filter(
            Job.candidate_id == candidate_id,
            Job.match_score.isnot(None)
        )
        .order_by(
            Job.match_score.desc()
        )
        .limit(10)
        .all()
    )

    skills = candidate.skills

    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except Exception:
            skills = []

    recommendations = (
        CareerRecommendationService.generate(
            candidate_skills=skills,
            jobs=jobs
        )
    )

    return {
        "candidate_id": candidate_id,
        **recommendations
    }
@router.get("/{candidate_id}/salary-intelligence")
def get_salary_intelligence(
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
        db.query(Job)
        .filter(
            Job.candidate_id == candidate_id,
            Job.match_score.isnot(None)
        )
        .order_by(
            Job.match_score.desc()
        )
        .limit(10)
        .all()
    )

    intelligence = (
        SalaryIntelligenceService.generate(
            jobs
        )
    )

    return {
        "candidate_id": candidate_id,
        **intelligence
    }
@router.get("/{candidate_id}/ats-score")
def get_ats_score(
    candidate_id: int,
    db: Session = Depends(get_db)
):

    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "candidate_id": candidate_id,
        **ATSAnalysisService.analyze(
            candidate
        )
    }