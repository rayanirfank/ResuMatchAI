from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CandidateResponse(BaseModel):
    id: int
    filename: str
    full_name: Optional[str]
    email: Optional[str]
    current_title: Optional[str]
    years_experience: Optional[int]
    seniority_level: Optional[str]
    skills: Optional[List[str]]
    tools: Optional[List[str]]
    certifications: Optional[List[str]]
    education: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True