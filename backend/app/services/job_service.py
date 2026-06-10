import httpx
import os

from sqlalchemy.orm import Session

from app.models.job import Job


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

ADZUNA_BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs"
)


# ──────────────────────────────────────────────────────────────────────────────
# Query Builder
# ──────────────────────────────────────────────────────────────────────────────

def _build_queries(
    keywords: list[str]
) -> list[str]:

    keywords = [
        k.lower().strip()
        for k in keywords
        if k and k.strip()
    ]

    role_queries = []

    # ──────────────────────────────────────────────────────────────────────
    # Role Inference Map
    # ──────────────────────────────────────────────────────────────────────

    ROLE_MAP = {

        # AI / ML
        "machine learning": [
            "machine learning engineer",
            "junior machine learning engineer",
            "ai engineer"
        ],

        "scikit-learn": [
            "machine learning engineer"
        ],

        "predictive modeling": [
            "data scientist"
        ],

        # Data
        "python": [
            "python developer",
            "backend python developer"
        ],

        "sql": [
            "data analyst",
            "sql developer"
        ],

        "data": [
            "data analyst",
            "junior data analyst",
            "data engineer"
        ],

        "bigquery": [
            "data engineer"
        ],

        "gcp": [
            "cloud engineer",
            "data engineer"
        ],

        # Frontend
        "react": [
            "react developer",
            "frontend developer"
        ],

        "javascript": [
            "javascript developer",
            "frontend developer"
        ],

        # Backend
        "java": [
            "java developer",
            "backend developer"
        ],

        "php": [
            "php developer"
        ]
    }

    # ──────────────────────────────────────────────────────────────────────
    # Build Queries From Skills
    # ──────────────────────────────────────────────────────────────────────

    for keyword in keywords:

        for trigger, roles in ROLE_MAP.items():

            if trigger in keyword:

                role_queries.extend(roles)

    # ──────────────────────────────────────────────────────────────────────
    # Strong Defaults
    # ──────────────────────────────────────────────────────────────────────

    if not role_queries:

        role_queries = [
            "python developer",
            "data analyst",
            "machine learning engineer",
            "software engineer"
        ]

    # ──────────────────────────────────────────────────────────────────────
    # Deduplicate
    # ──────────────────────────────────────────────────────────────────────

    seen = set()
    unique_queries = []

    for query in role_queries:

        q = query.lower().strip()

        if q not in seen:
            seen.add(q)
            unique_queries.append(query)

    return unique_queries[:8]


# ──────────────────────────────────────────────────────────────────────────────
# Fetch + Store Jobs
# ──────────────────────────────────────────────────────────────────────────────

SUPPORTED_COUNTRIES = [
    {"country_code": "gb", "location": "London"},
    {"country_code": "us", "location": "New York"},
    {"country_code": "ca", "location": "Toronto"},
    {"country_code": "au", "location": "Sydney"},
    {"country_code": "in", "location": "Bangalore"},
    {"country_code": "sg", "location": "Singapore"},
]

def fetch_and_store_jobs(
    candidate_id: int,
    keywords: list[str],
    location: str,
    country_code: str,
    db: Session
) -> dict:

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise Exception("Missing Adzuna API credentials.")

    queries = _build_queries(keywords)
    print(f"[DEBUG] Final Queries: {queries}")

    stored_count = 0
    skipped_count = 0
    seen_external_ids = set()

    # Load existing jobs for this candidate to avoid duplicates
    existing_jobs = (
        db.query(Job.external_id)
        .filter(Job.candidate_id == candidate_id)
        .all()
    )
    for (external_id,) in existing_jobs:
        if external_id:
            seen_external_ids.add(str(external_id))

    # Loop every query across every supported country
    for country in SUPPORTED_COUNTRIES:
        for query in queries:

            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "results_per_page": 10,
                "what": query,
                "where": country["location"],
            }

            try:
                response = httpx.get(
                    f"{ADZUNA_BASE_URL}/{country['country_code']}/search/1",
                    params=params,
                    timeout=20.0
                )
                response.raise_for_status()
                data = response.json()
                print(
                    f"[DEBUG] {country['country_code'].upper()} | "
                    f"Query '{query}' → {data.get('count', 0)} results"
                )

            except Exception as e:
                print(f"[job_service] Failed: {country['country_code']} / '{query}': {e}")
                continue

            for item in data.get("results", []):
                external_id = str(item.get("id", ""))

                if not external_id or external_id in seen_external_ids:
                    skipped_count += 1
                    continue

                seen_external_ids.add(external_id)

                job = Job(
                    candidate_id=candidate_id,
                    external_id=external_id,
                    title=item.get("title", ""),
                    company=item.get("company", {}).get("display_name", ""),
                    location=item.get("location", {}).get("display_name", ""),
                    country=country["country_code"],
                    description=item.get("description", ""),
                    salary_min=item.get("salary_min"),
                    salary_max=item.get("salary_max"),
                    job_url=item.get("redirect_url", ""),
                    posted_at=item.get("created", ""),
                )

                db.add(job)
                stored_count += 1

    db.commit()

    return {
        "queries_run": queries,
        "jobs_stored": stored_count,
        "jobs_skipped_duplicate": skipped_count,
    }

    # ──────────────────────────────────────────────────────────────────────
    # Validate API Credentials
    # ──────────────────────────────────────────────────────────────────────

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:

        raise Exception(
            "Missing Adzuna API credentials in environment variables."
        )

    # ──────────────────────────────────────────────────────────────────────
    # Build Search Queries
    # ──────────────────────────────────────────────────────────────────────

    queries = _build_queries(keywords)

    print(f"[DEBUG] Final Queries: {queries}")

    stored_count = 0
    skipped_count = 0

    seen_external_ids = set()

    # ──────────────────────────────────────────────────────────────────────
    # Load Existing Jobs For Candidate
    # ──────────────────────────────────────────────────────────────────────

    existing_jobs = (
        db.query(Job.external_id)
        .filter(
            Job.candidate_id == candidate_id
        )
        .all()
    )

    for (external_id,) in existing_jobs:

        if external_id:
            seen_external_ids.add(
                str(external_id)
            )

    # ──────────────────────────────────────────────────────────────────────
    # Query Adzuna
    # ──────────────────────────────────────────────────────────────────────

    for query in queries:

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": 20,
            "what": query,
            "where": location,
        }

        try:

            response = httpx.get(
                f"{ADZUNA_BASE_URL}/{country_code}/search/1",
                params=params,
                timeout=20.0
            )

            response.raise_for_status()

            data = response.json()

            print(
                f"[DEBUG] Query '{query}' "
                f"returned {data.get('count', 0)} results"
            )

        except Exception as e:

            print(
                f"[job_service] Query failed "
                f"for '{query}': {e}"
            )

            continue

        results = data.get("results", [])

        # ──────────────────────────────────────────────────────────────
        # Parse Jobs
        # ──────────────────────────────────────────────────────────────

        for item in results:

            external_id = str(
                item.get("id", "")
            )

            # Skip invalid / duplicate jobs
            if (
                not external_id or
                external_id in seen_external_ids
            ):
                skipped_count += 1
                continue

            seen_external_ids.add(
                external_id
            )

            company_data = item.get(
                "company",
                {}
            )

            location_data = item.get(
                "location",
                {}
            )

            job = Job(

                candidate_id=candidate_id,

                external_id=external_id,

                title=item.get(
                    "title",
                    ""
                ),

                company=company_data.get(
                    "display_name",
                    ""
                ),

                location=location_data.get(
                    "display_name",
                    ""
                ),

                country=country_code,

                description=item.get(
                    "description",
                    ""
                ),

                salary_min=item.get(
                    "salary_min"
                ),

                salary_max=item.get(
                    "salary_max"
                ),

                job_url=item.get(
                    "redirect_url",
                    ""
                ),

                posted_at=item.get(
                    "created",
                    ""
                ),
            )

            db.add(job)

            stored_count += 1

    # ──────────────────────────────────────────────────────────────────────
    # Persist Jobs
    # ──────────────────────────────────────────────────────────────────────

    db.commit()

    return {

        "queries_run": queries,

        "jobs_stored": stored_count,

        "jobs_skipped_duplicate": skipped_count,
    }