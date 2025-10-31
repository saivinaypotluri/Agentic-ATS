from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.candidate import Candidate
from backend.schemas import FeedbackRequest, FeedbackResponse
from backend.agents.feedback_agent import FeedbackAgent

router = APIRouter(prefix="/api", tags=["feedback"])

# Initialize agent
feedback_agent = FeedbackAgent()


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit and summarize interview feedback for a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Generate feedback summary
    summary = feedback_agent.generate_summary(
        request.interview_notes,
        candidate.name or "Candidate"
    )
    
    # Store feedback
    candidate.interview_notes = request.interview_notes
    candidate.feedback_summary = summary
    
    db.commit()
    db.refresh(candidate)
    
    return FeedbackResponse(
        candidate_id=candidate.id,
        feedback_summary=summary,
        message="Feedback processed and stored successfully"
    )


@router.get("/get_feedback/{candidate_id}")
async def get_feedback(candidate_id: int, db: Session = Depends(get_db)):
    """
    Retrieve feedback for a specific candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if not candidate.feedback_summary:
        raise HTTPException(
            status_code=404,
            detail="No feedback available for this candidate"
        )
    
    return {
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "interview_notes": candidate.interview_notes,
        "feedback_summary": candidate.feedback_summary
    }


@router.get("/analyze_sentiment/{candidate_id}")
async def analyze_sentiment(candidate_id: int, db: Session = Depends(get_db)):
    """
    Analyze the sentiment of feedback for a candidate.
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if not candidate.interview_notes:
        raise HTTPException(
            status_code=404,
            detail="No interview notes available for sentiment analysis"
        )
    
    sentiment = feedback_agent.analyze_sentiment(candidate.interview_notes)
    rating = feedback_agent.extract_rating(candidate.interview_notes)
    
    return {
        "candidate_id": candidate.id,
        "sentiment": sentiment,
        "rating": rating,
        "message": f"Sentiment analysis: {sentiment} (Rating: {rating}/5)"
    }
