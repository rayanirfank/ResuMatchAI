# app/schemas/dashboard.py

from pydantic import BaseModel
from typing import List, Dict


class TopJob(BaseModel):
    title: str
    company: str
    score: float


class DashboardResponse(BaseModel):
    top_match_score: float
    average_match_score: float
    jobs_found: int

    match_distribution: Dict[str, int]

    top_jobs: List[TopJob]