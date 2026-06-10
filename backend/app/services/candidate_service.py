import json
from sqlalchemy.orm import Session

from app.models.candidate import Candidate

from app.parsing.resume_parser import (
    extract_text_from_pdf,
    parse_resume_with_ai,
)

from app.parsing.keywords_parser import (
    parse_keywords_file,
    merge_keywords
)


def process_and_store_candidate(
    db: Session,
    file_bytes: bytes,
    filename: str
) -> Candidate:

    # Extract raw resume text
    raw_text = extract_text_from_pdf(file_bytes)

    # Parse structured resume data
    parsed = parse_resume_with_ai(raw_text)

    # Create candidate object
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
    return (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )


def delete_candidate(db: Session, candidate_id: int):

    candidate = get_candidate_by_id(db, candidate_id)

    if not candidate:
        return None

    db.delete(candidate)
    db.commit()

    return candidate


def attach_keywords(
    db: Session,
    candidate_id: int,
    file_bytes: bytes,
    filename: str
):

    # Find candidate
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        return None

    # Parse uploaded keywords file
    file_keywords = parse_keywords_file(
        file_bytes,
        filename
    )

    # Load existing resume skills
    existing_skills = []

    if candidate.skills:
        try:
            existing_skills = json.loads(candidate.skills)
        except json.JSONDecodeError:
            existing_skills = []

    # Merge + deduplicate
    unified_keywords = merge_keywords(
        existing_skills,
        file_keywords
    )

    # Store merged keywords
    candidate.unified_keywords = json.dumps(unified_keywords)

    db.commit()
    db.refresh(candidate)

    return candidate