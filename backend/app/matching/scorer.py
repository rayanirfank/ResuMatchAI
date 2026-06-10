import json
import re
from typing import Optional
from app.parsing.resume_parser import (
    extract_skills_and_tools
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _parse_json_field(value) -> list[str]:
    """Safely parse JSON list fields from SQLite."""
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        parsed = json.loads(value)

        if isinstance(parsed, list):
            return parsed

        return []

    except (json.JSONDecodeError, TypeError):
        return []


def _normalize(text: str) -> set[str]:
    """Normalize text into lowercase word tokens."""
    return set(
        re.findall(r"\b\w+\b", text.lower())
    )


def _extract_required_experience(
    description: str
) -> Optional[int]:

    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"(\d+)\+?\s*years?\s+experience",
        r"minimum\s+(\d+)\s*years?",
        r"at\s+least\s+(\d+)\s*years?",
        r"(\d+)\s*[-–]\s*\d+\s*years?",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            description,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


# ──────────────────────────────────────────────────────────────────────────────
# Seniority Logic
# ──────────────────────────────────────────────────────────────────────────────

SENIORITY_RANK = {
    "intern": 0,
    "junior": 1,
    "mid": 2,
    "senior": 3,
    "lead": 4,
    "manager": 4,
    "vp": 5,
    "director": 5,
    "c-level": 6,
}


def _detect_job_seniority(
    job_title: str,
    job_desc: str
) -> int:

    combined = (
        f"{job_title} {job_desc}"
    ).lower()

    detected_level = 2  # default mid-level

    labels = [
        "c-level",
        "director",
        "vp",
        "lead",
        "manager",
        "senior",
        "mid",
        "junior",
        "intern",
    ]

    for label in labels:

        pattern = rf"\b{re.escape(label)}\b"

        if re.search(pattern, combined):
            detected_level = SENIORITY_RANK[label]
            break

    return detected_level


def _seniority_score(
    candidate_seniority: str,
    job_title: str,
    job_desc: str
) -> float:

    candidate_level = SENIORITY_RANK.get(
        (candidate_seniority or "mid").lower(),
        2
    )

    job_level = _detect_job_seniority(
        job_title,
        job_desc
    )

    gap = abs(candidate_level - job_level)

    if gap == 0:
        return 1.0

    if gap == 1:
        return 0.6

    if gap == 2:
        return 0.2

    return 0.0


# ──────────────────────────────────────────────────────────────────────────────
# Main Scoring Engine
# ──────────────────────────────────────────────────────────────────────────────

def compute_match(candidate, job) -> dict:

    # ── Candidate ────────────────────────────────────────────────────────────

    candidate_skills = _parse_json_field(
        candidate.skills
    )

    candidate_keywords = _parse_json_field(
        candidate.keywords
    )

    candidate_seniority = (
        candidate.seniority_level or "mid"
    )

    candidate_years = (
        candidate.years_experience or 0
    )

    all_candidate_terms = set(
        term.lower().strip()
        for term in (
            candidate_skills +
            candidate_keywords
        )
        if term.strip()
    )

    # ── Job ──────────────────────────────────────────────────────────────────

    job_title = job.title or ""
    job_desc = job.description or ""
    job_location = job.location or ""

    job_full_text = (
        f"{job_title} {job_desc}"
    ).lower()

    job_skills, job_tools = (
    extract_skills_and_tools(
        job_full_text
    )
    )
    print("\nJOB:", job.title)
    print("JOB SKILLS:", job_skills)
    print("JOB TOOLS:", job_tools)  
    
    job_terms = set(
    term.lower().strip()
    for term in (
        job_skills +
        job_tools
    )
    )

    # ── Skill Matching ───────────────────────────────────────────────────────
    matched_skills = sorted(
    all_candidate_terms &
    job_terms
    )

    unmatched_candidate_skills = sorted(
    all_candidate_terms -
    job_terms
    )
    
    # ── Factor 1: Skill Match (55%) ─────────────────────────────────────────

    if len(job_terms) >= 4:
        raw_skill_score = len(matched_skills) / len(job_terms)
    elif len(job_terms) > 0:
    # Too few skills extracted — score is unreliable, cap it
        raw_skill_score = min(len(matched_skills) / len(job_terms), 0.40)
    else:
        raw_skill_score = 0.0

    # Minimum match gate: penalize hard if fewer than 2 skills matched
    if len(matched_skills) == 0:
        skill_score = 0.0
    elif len(matched_skills) == 1:
        skill_score = min(raw_skill_score, 0.35)  # cap single-match at 35%
    else:
        skill_score = raw_skill_score

    # ── Factor 2: Keyword Alignment (10%) ───────────────────────────────────
    # Measures candidate keywords (from keywords file) overlap with job description words
    job_desc_words = _normalize(job_full_text)
    candidate_keyword_terms = set(
        kw.lower().strip() for kw in candidate_keywords if kw.strip()
    )
    if candidate_keyword_terms:
        kw_hits = candidate_keyword_terms & job_desc_words
        keyword_alignment_score = len(kw_hits) / len(candidate_keyword_terms)
    else:
        keyword_alignment_score = skill_score  # fallback if no keywords file

    # ── Factor 3: Seniority (20%) ───────────────────────────────────────────

    seniority_score = _seniority_score(
        candidate_seniority,
        job_title,
        job_desc
    )

    # ── Factor 4: Experience (10%) ──────────────────────────────────────────

    required_exp = _extract_required_experience(
        job_desc
    )

    if required_exp is None:

        experience_score = 1.0

    else:

        gap = (
            candidate_years -
            required_exp
        )

        if gap >= 0:
            experience_score = 1.0

        elif gap >= -2:
            experience_score = 0.5

        else:
            experience_score = 0.0

    # ── Factor 5: Location (5%) ─────────────────────────────────────────────

    candidate_location_terms = _normalize(
        candidate.location or ""
    )

    job_location_terms = _normalize(
        job_location
    )

    if (
        not candidate_location_terms or
        not job_location_terms
    ):
        location_score = 0.5

    elif (
        candidate_location_terms &
        job_location_terms
    ):
        location_score = 1.0

    elif (
        "remote" in job_location_terms or
        "anywhere" in job_location_terms
    ):
        location_score = 0.9

    else:
        location_score = 0.0

    # ── Final Weighted Score ────────────────────────────────────────────────

# ── Final Weighted Score ────────────────────────────────────────────────
    final_score = (
        skill_score            * 0.55 +
        keyword_alignment_score * 0.10 +
        seniority_score        * 0.20 +
        experience_score       * 0.10 +
        location_score         * 0.05
    )
    final_score_pct = round(final_score * 100, 1)
    # ── Explanation ─────────────────────────────────────────────────────────

    explanation = _build_explanation(
        score=final_score_pct,
        matched=matched_skills,
        unmatched=unmatched_candidate_skills,
        seniority_score=seniority_score,
        experience_score=experience_score,
        candidate_seniority=candidate_seniority,
        required_exp=required_exp,
        candidate_years=candidate_years
    )

    return {
        "score": final_score_pct,

        "breakdown": {
            "skill_match_pct": round(
                skill_score * 100,
                1
            ),

            "keyword_alignment_pct": round(
                keyword_alignment_score * 100,
                1
            ),

            "seniority_alignment_pct": round(
                seniority_score * 100,
                1
            ),

            "experience_score_pct": round(
                experience_score * 100,
                1
            ),

            "location_score_pct": round(
                location_score * 100,
                1
            ),
        },
            "required_skills": sorted(job_terms),
            
        "matched_skills": sorted(
            matched_skills
        ),

        "unmatched_candidate_skills": sorted(
            unmatched_candidate_skills[:10]
        ),

        "explanation": explanation,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Human Explanation Builder
# ──────────────────────────────────────────────────────────────────────────────

def _build_explanation(
    score,
    matched,
    unmatched,
    seniority_score,
    experience_score,
    candidate_seniority,
    required_exp,
    candidate_years
) -> str:

    lines = []

    # ── Overall Verdict ──────────────────────────────────────────────────────

    if score >= 75:

        lines.append(
            f"Strong match ({score}%) — your profile aligns well with this role."
        )

    elif score >= 50:

        lines.append(
            f"Moderate match ({score}%) — you meet many requirements but have gaps."
        )

    elif score >= 25:

        lines.append(
            f"Weak match ({score}%) — partial alignment detected."
        )

    else:

        lines.append(
            f"Poor match ({score}%) — this role differs significantly from your profile."
        )

    # ── Skill Notes ─────────────────────────────────────────────────────────

    if matched:

        lines.append(
            f"Matched skills: {', '.join(matched[:5])}"
            f"{'...' if len(matched) > 5 else ''}."
        )

    if unmatched:

        lines.append(
            f"Additional candidate skills not referenced in this job: "
            f"{', '.join(unmatched[:4])}"
            f"{'...' if len(unmatched) > 4 else ''}."
        )

    # ── Seniority / Experience ──────────────────────────────────────────────

    if seniority_score < 0.5:

        lines.append(
            f"Seniority mismatch detected for '{candidate_seniority}' level."
        )

    if (
        experience_score == 0.0 and
        required_exp is not None
    ):

        lines.append(
            f"Role requires approximately {required_exp} years experience; "
            f"candidate has {candidate_years}."
        )

    return " ".join(lines)