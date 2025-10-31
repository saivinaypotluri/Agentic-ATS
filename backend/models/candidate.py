from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON
from datetime import datetime
from backend.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    resume_text = Column(Text, nullable=True)
    resume_filename = Column(String, nullable=True)
    
    # Extracted URLs
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    misc_links = Column(JSON, nullable=True)  # List of other URLs
    
    # Enriched data from profile intelligence agent
    linkedin_data = Column(JSON, nullable=True)
    github_data = Column(JSON, nullable=True)
    misc_data = Column(JSON, nullable=True)
    
    # Job matching
    job_description = Column(Text, nullable=True)
    match_score = Column(Float, nullable=True)
    
    # Skills and experience extracted from resume
    skills = Column(JSON, nullable=True)  # List of skills
    education = Column(JSON, nullable=True)  # Education details
    experience = Column(JSON, nullable=True)  # Work experience
    
    # Recruiter actions
    approved = Column(Boolean, default=False)
    rejected = Column(Boolean, default=False)
    
    # Interview scheduling
    scheduled_interview = Column(String, nullable=True)
    interview_notes = Column(Text, nullable=True)
    
    # Feedback
    feedback = Column(Text, nullable=True)
    feedback_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
