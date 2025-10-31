from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from backend.database import get_db
from backend.models.candidate import Candidate
from backend.schemas import (
    ResumeUploadResponse,
    CandidateResponse,
    ApprovalRequest,
    ApprovalResponse,
    CandidateUpdate
)
from backend.agents.resume_parser import ResumeParser

router = APIRouter(prefix="/api", tags=["candidates"])

# Initialize agents
resume_parser = ResumeParser()

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload_resume", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and parse a resume file.
    Supports PDF, DOCX, and TXT formats.
    """
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload PDF, DOCX, or TXT files."
        )
    
    # Save file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse resume
        parsed_data = resume_parser.parse(file_path, file_extension)
        
        # Create candidate record
        candidate = Candidate(
            name=parsed_data.get('name'),
            email=parsed_data.get('email'),
            phone=parsed_data.get('phone'),
            resume_text=parsed_data.get('resume_text'),
            resume_filename=file.filename,
            skills=parsed_data.get('skills'),
            education=parsed_data.get('education'),
            experience=parsed_data.get('experience')
        )
        
        # Extract and store URLs
        urls = parsed_data.get('urls', [])
        misc_links = []
        
        for url in urls:
            if 'linkedin.com' in url.lower():
                candidate.linkedin_url = url
            elif 'github.com' in url.lower():
                candidate.github_url = url
            else:
                misc_links.append(url)
        
        candidate.misc_links = misc_links if misc_links else None
        
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        return ResumeUploadResponse(
            candidate_id=candidate.id,
            name=candidate.name,
            email=candidate.email,
            phone=candidate.phone,
            skills=candidate.skills,
            message="Resume uploaded and parsed successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/get_candidate/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a candidate's profile by ID.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate


@router.get("/get_all_candidates", response_model=List[CandidateResponse])
async def get_all_candidates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all candidates with pagination.
    """
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return candidates


@router.post("/approve_candidate", response_model=ApprovalResponse)
async def approve_candidate(
    approval: ApprovalRequest,
    db: Session = Depends(get_db)
):
    """
    Approve or reject a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == approval.candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate.approved = approval.approved
    candidate.rejected = not approval.approved
    
    db.commit()
    db.refresh(candidate)
    
    status = "approved" if approval.approved else "rejected"
    
    return ApprovalResponse(
        candidate_id=candidate.id,
        approved=candidate.approved,
        message=f"Candidate {status} successfully"
    )


@router.put("/update_candidate/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    update_data: CandidateUpdate,
    db: Session = Depends(get_db)
):
    """
    Update candidate information.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Update fields if provided
    if update_data.name is not None:
        candidate.name = update_data.name
    if update_data.email is not None:
        candidate.email = update_data.email
    if update_data.phone is not None:
        candidate.phone = update_data.phone
    if update_data.skills is not None:
        candidate.skills = update_data.skills
    
    db.commit()
    db.refresh(candidate)
    
    return candidate


@router.delete("/delete_candidate/{candidate_id}")
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Delete a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    db.delete(candidate)
    db.commit()
    
    return {"message": f"Candidate {candidate_id} deleted successfully"}
