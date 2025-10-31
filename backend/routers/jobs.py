from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.candidate import Candidate
from backend.schemas import (
    JobMatchRequest,
    JobMatchResponse,
    ProfileIntelligenceRequest,
    ProfileIntelligenceResponse,
    ScheduleInterviewRequest,
    ScheduleInterviewResponse
)
from backend.agents.job_match_agent import JobMatchAgent
from backend.agents.profile_intelligence_agent import ProfileIntelligenceAgent
from backend.agents.scheduler_agent import SchedulerAgent

router = APIRouter(prefix="/api", tags=["jobs"])

# Initialize agents
job_match_agent = JobMatchAgent()
profile_intelligence_agent = ProfileIntelligenceAgent()
scheduler_agent = SchedulerAgent()


@router.post("/match_job", response_model=JobMatchResponse)
async def match_job(
    request: JobMatchRequest,
    db: Session = Depends(get_db)
):
    """
    Compare resume with job description and compute match score.
    """
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if not candidate.resume_text:
        raise HTTPException(status_code=400, detail="No resume text available for this candidate")
    
    # Compute match score
    match_score = job_match_agent.compute_similarity(
        candidate.resume_text,
        request.job_description
    )
    
    # Update candidate record
    candidate.job_description = request.job_description
    candidate.match_score = match_score
    
    db.commit()
    db.refresh(candidate)
    
    # Get explanation
    explanation = job_match_agent.get_match_explanation(match_score)
    
    return JobMatchResponse(
        candidate_id=candidate.id,
        match_score=match_score,
        message=f"Match score: {match_score}%. {explanation}"
    )


@router.post("/fetch_profiles", response_model=ProfileIntelligenceResponse)
async def fetch_profiles(
    request: ProfileIntelligenceRequest,
    db: Session = Depends(get_db)
):
    """
    Enrich candidate profile with data from LinkedIn, GitHub, and other URLs.
    """
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Collect all URLs
    urls = []
    if candidate.linkedin_url:
        urls.append(candidate.linkedin_url)
    if candidate.github_url:
        urls.append(candidate.github_url)
    if candidate.misc_links:
        urls.extend(candidate.misc_links)
    
    if not urls:
        raise HTTPException(
            status_code=400,
            detail="No URLs found in candidate's resume"
        )
    
    # Enrich profile
    enriched_data = profile_intelligence_agent.enrich_profile(urls)
    
    # Update candidate record
    if enriched_data.get('linkedin_url'):
        candidate.linkedin_url = enriched_data['linkedin_url']
    if enriched_data.get('github_url'):
        candidate.github_url = enriched_data['github_url']
    if enriched_data.get('misc_urls'):
        candidate.misc_links = enriched_data['misc_urls']
    
    candidate.linkedin_data = enriched_data.get('linkedin_data')
    candidate.github_data = enriched_data.get('github_data')
    candidate.misc_data = enriched_data.get('misc_data')
    
    db.commit()
    db.refresh(candidate)
    
    # Generate summary
    summary = profile_intelligence_agent.generate_summary(
        enriched_data,
        candidate.name or "Candidate"
    )
    
    return ProfileIntelligenceResponse(
        candidate_id=candidate.id,
        linkedin_data=candidate.linkedin_data,
        github_data=candidate.github_data,
        misc_data=candidate.misc_data,
        summary=summary
    )


@router.post("/schedule_interview", response_model=ScheduleInterviewResponse)
async def schedule_interview(
    request: ScheduleInterviewRequest,
    db: Session = Depends(get_db)
):
    """
    Suggest interview slots or schedule an interview for a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # If no slot provided, return suggestions
    if not request.interview_slot:
        suggested_slots = scheduler_agent.suggest_slots(num_slots=5)
        
        return ScheduleInterviewResponse(
            candidate_id=candidate.id,
            suggested_slots=suggested_slots,
            scheduled_slot=None,
            message="Here are suggested interview slots"
        )
    
    # Schedule the interview
    result = scheduler_agent.schedule_interview(
        candidate.id,
        request.interview_slot
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    
    # Update candidate record
    candidate.scheduled_interview = request.interview_slot
    
    db.commit()
    db.refresh(candidate)
    
    # Generate calendar invite
    calendar_invite = scheduler_agent.get_calendar_invite_text(
        candidate.name or "Candidate",
        request.interview_slot
    )
    
    return ScheduleInterviewResponse(
        candidate_id=candidate.id,
        suggested_slots=None,
        scheduled_slot=candidate.scheduled_interview,
        message=f"Interview scheduled successfully. {calendar_invite}"
    )


@router.get("/get_interview_slots")
async def get_interview_slots(num_slots: int = 5):
    """
    Get suggested interview time slots without candidate context.
    """
    suggested_slots = scheduler_agent.suggest_slots(num_slots=num_slots)
    
    return {
        "suggested_slots": suggested_slots,
        "message": f"Generated {len(suggested_slots)} available slots"
    }
