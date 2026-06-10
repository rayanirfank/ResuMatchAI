from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.sql import func

from app.core.database import Base


class Job(Base):

    __tablename__ = "jobs"

    __table_args__ = (
        # A candidate cannot store the same external job twice,
        # but different candidates CAN store the same job.
        UniqueConstraint(
            "candidate_id",
            "external_id",
            name="uq_candidate_external_job"
        ),
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Primary Key
    # ──────────────────────────────────────────────────────────────────────────

    id = Column(Integer, primary_key=True, index=True)

    # ──────────────────────────────────────────────────────────────────────────
    # Candidate Association
    # ──────────────────────────────────────────────────────────────────────────

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True
    )

    # ──────────────────────────────────────────────────────────────────────────
    # External Job Source
    # ──────────────────────────────────────────────────────────────────────────

    external_id = Column(
        String(255),
        index=True,
        nullable=False
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Core Job Data
    # ──────────────────────────────────────────────────────────────────────────

    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_url = Column(Text, nullable=True)
    posted_at = Column(String(100), nullable=True)

    # ──────────────────────────────────────────────────────────────────────────
    # Matching Intelligence
    # ──────────────────────────────────────────────────────────────────────────

    match_score = Column(Float, nullable=True, index=True)
    matched_keywords = Column(Text, nullable=True, default="[]")
    required_skills = Column(
    Text,
    nullable=True,
    default="[]"
)
    unmatched_candidate_skills = Column(Text, nullable=True, default="[]")
    match_explanation = Column(Text, nullable=True)

    # ──────────────────────────────────────────────────────────────────────────
    # Metadata
    # ──────────────────────────────────────────────────────────────────────────

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )