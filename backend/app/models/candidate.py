from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class Candidate(Base):

    __tablename__ = "candidates"

    # ──────────────────────────────────────────────────────────────────────────
    # Primary Key
    # ──────────────────────────────────────────────────────────────────────────

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Resume Metadata
    # ──────────────────────────────────────────────────────────────────────────

    filename = Column(
        String(255),
        nullable=False
    )

    raw_text = Column(
        Text,
        nullable=False
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Basic Identity
    # ──────────────────────────────────────────────────────────────────────────

    full_name = Column(
        String(255),
        nullable=True
    )

    email = Column(
        String(255),
        nullable=True,
        index=True
    )

    phone = Column(
        String(100),
        nullable=True
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Career Information
    # ──────────────────────────────────────────────────────────────────────────

    current_title = Column(
        String(255),
        nullable=True
    )

    years_experience = Column(
        Integer,
        nullable=True,
        default=0
    )

    seniority_level = Column(
        String(50),
        nullable=True,
        default="junior"
    )

    location = Column(
        String(255),
        nullable=True
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Parsed Resume Intelligence
    # Stored as JSON strings
    # ──────────────────────────────────────────────────────────────────────────

    skills = Column(
        Text,
        nullable=True
    )

    tools = Column(
        Text,
        nullable=True
    )

    certifications = Column(
        Text,
        nullable=True
    )

    education = Column(
        Text,
        nullable=True
    )

    keywords = Column(
        Text,
        nullable=True
    )

    unified_keywords = Column(
        Text,
        nullable=True
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Metadata
    # ──────────────────────────────────────────────────────────────────────────

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )