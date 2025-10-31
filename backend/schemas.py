from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Resume Upload Schemas
class ResumeUploadResponse(BaseModel):
    candidate_id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: Optional[List[str]]
    message: str

# Job Match Schemas
class JobMatchRequest(BaseModel):
    candidate_id: int
    job_description: str

class JobMatchResponse(BaseModel):
    candidate_id: int
    match_score: float
    message: str

# Profile Intelligence Schemas
class ProfileIntelligenceRequest(BaseModel):
    candidate_id: int

class ProfileIntelligenceResponse(BaseModel):
    candidate_id: int
    linkedin_data: Optional[Dict[str, Any]]
    github_data: Optional[Dict[str, Any]]
    misc_data: Optional[List[Dict[str, Any]]]
    summary: str

# Candidate Schemas
class CandidateBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class CandidateResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    resume_filename: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    misc_links: Optional[List[str]]
    linkedin_data: Optional[Dict[str, Any]]
    github_data: Optional[Dict[str, Any]]
    misc_data: Optional[List[Dict[str, Any]]]
    skills: Optional[List[str]]
    education: Optional[List[Dict[str, Any]]]
    experience: Optional[List[Dict[str, Any]]]
    match_score: Optional[float]
    approved: bool
    rejected: bool
    scheduled_interview: Optional[str]
    feedback_summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Approval Schemas
class ApprovalRequest(BaseModel):
    candidate_id: int
    approved: bool

class ApprovalResponse(BaseModel):
    candidate_id: int
    approved: bool
    message: str

# Interview Scheduling Schemas
class ScheduleInterviewRequest(BaseModel):
    candidate_id: int
    interview_slot: Optional[str] = None  # If None, return suggestions

class ScheduleInterviewResponse(BaseModel):
    candidate_id: int
    suggested_slots: Optional[List[str]]
    scheduled_slot: Optional[str]
    message: str

# Feedback Schemas
class FeedbackRequest(BaseModel):
    candidate_id: int
    interview_notes: str

class FeedbackResponse(BaseModel):
    candidate_id: int
    feedback_summary: str
    message: str

# Update Candidate Schema
class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
