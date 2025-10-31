from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from backend.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    resume_text = Column(Text, nullable=True)
    resume_filename = Column(String, nullable=True)
    
    # Profile URLs
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    misc_links = Column(JSON, default=[])
    
    # Extracted profile data
    linkedin_data = Column(JSON, nullable=True)
    github_data = Column(JSON, nullable=True)
    misc_data = Column(JSON, nullable=True)
    
    # Parsed resume data
    skills = Column(JSON, default=[])
    education = Column(JSON, default=[])
    experience = Column(JSON, default=[])
    
    # Job matching
    match_score = Column(Float, nullable=True)
    job_description = Column(Text, nullable=True)
    
    # Human-in-the-loop
    approved = Column(Boolean, default=False)
    recruiter_notes = Column(Text, nullable=True)
    
    # Interview scheduling
    interview_scheduled = Column(Boolean, default=False)
    interview_date = Column(DateTime, nullable=True)
    interview_notes = Column(Text, nullable=True)
    feedback_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
