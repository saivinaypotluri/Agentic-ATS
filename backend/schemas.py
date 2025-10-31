from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class CandidateBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    resume_filename: Optional[str] = None
    resume_text: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    misc_links: Optional[List[str]] = []
    linkedin_data: Optional[Dict[str, Any]] = None
    github_data: Optional[Dict[str, Any]] = None
    misc_data: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = []
    education: Optional[List[Dict[str, Any]]] = []
    experience: Optional[List[Dict[str, Any]]] = []
    match_score: Optional[float] = None
    job_description: Optional[str] = None
    approved: bool = False
    recruiter_notes: Optional[str] = None
    interview_scheduled: bool = False
    interview_date: Optional[datetime] = None
    interview_notes: Optional[str] = None
    feedback_summary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class JobMatchRequest(BaseModel):
    candidate_id: int
    job_description: str

class JobMatchResponse(BaseModel):
    candidate_id: int
    match_score: float
    analysis: str

class ProfileFetchRequest(BaseModel):
    candidate_id: int

class ProfileFetchResponse(BaseModel):
    candidate_id: int
    linkedin_data: Optional[Dict[str, Any]] = None
    github_data: Optional[Dict[str, Any]] = None
    misc_data: Optional[List[Dict[str, Any]]] = None
    summary: str

class ApprovalRequest(BaseModel):
    candidate_id: int
    approved: bool
    recruiter_notes: Optional[str] = None

class ScheduleInterviewRequest(BaseModel):
    candidate_id: int
    interview_date: datetime
    notes: Optional[str] = None

class FeedbackRequest(BaseModel):
    candidate_id: int
    interview_notes: str

class FeedbackResponse(BaseModel):
    candidate_id: int
    feedback_summary: str
