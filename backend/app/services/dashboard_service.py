from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job import Job


def get_dashboard_data(candidate_id: int, db: Session):

    # Get candidate
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        return None

    # Get jobs
    jobs = (
        db.query(Job)
        .filter(Job.candidate_id == candidate_id)
        .all()
    )

    # No jobs case
    if not jobs:
        return {
            "top_match_score": 0,
            "average_match_score": 0,
            "jobs_found": 0,
            "matched_skills": 0,
            "match_distribution": {
                "80-100": 0,
                "60-79": 0,
                "40-59": 0,
                "20-39": 0,
                "0-19": 0
            },
            "top_jobs": []
        }

    # Debug null scores
    for job in jobs:
        if job.match_score is None:
            print(f"NULL SCORE FOUND: {job.title}")

    # Keep only jobs with valid scores
    valid_jobs = [
        job
        for job in jobs
        if job.match_score is not None
    ]

    # If every score is null
    if not valid_jobs:
        return {
            "top_match_score": 0,
            "average_match_score": 0,
            "jobs_found": len(jobs),
            "matched_skills": 0,
            "match_distribution": {
                "80-100": 0,
                "60-79": 0,
                "40-59": 0,
                "20-39": 0,
                "0-19": 0
            },
            "top_jobs": []
        }

    scores = [job.match_score for job in valid_jobs]

    # Metrics
    top_match_score = max(scores)

    average_match_score = round(
        sum(scores) / len(scores),
        2
    )

    jobs_found = len(jobs)

    # Distribution
    distribution = {
        "80-100": 0,
        "60-79": 0,
        "40-59": 0,
        "20-39": 0,
        "0-19": 0
    }

    for score in scores:

        if score >= 80:
            distribution["80-100"] += 1

        elif score >= 60:
            distribution["60-79"] += 1

        elif score >= 40:
            distribution["40-59"] += 1

        elif score >= 20:
            distribution["20-39"] += 1

        else:
            distribution["0-19"] += 1

   # Top 5 jobs
    top_jobs = sorted(
        valid_jobs,
        key=lambda job: job.match_score,
        reverse=True
    )[:5]

    top_jobs_data = [
        {
            "title": job.title,
            "company": job.company,
            "score": job.match_score
        }
        for job in top_jobs
    ]

    return {
        "top_match_score": top_match_score,
        "average_match_score": average_match_score,
        "jobs_found": jobs_found,
        "match_distribution": distribution,
        "top_jobs": top_jobs_data
    }