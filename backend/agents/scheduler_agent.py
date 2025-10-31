from datetime import datetime, timedelta
from typing import List, Optional, Dict
from backend.utils import generate_interview_slots

class SchedulerAgent:
    """Agent for suggesting and managing interview schedules."""
    
    def __init__(self):
        self.business_hours_start = 9  # 9 AM
        self.business_hours_end = 17   # 5 PM
    
    def suggest_slots(self, num_slots: int = 5, preferred_days: Optional[List[int]] = None) -> List[str]:
        """
        Suggest available interview time slots.
        
        Args:
            num_slots: Number of slots to suggest
            preferred_days: List of preferred weekdays (0=Monday, 6=Sunday)
            
        Returns:
            List of suggested time slots in format "YYYY-MM-DD HH:MM"
        """
        return generate_interview_slots(num_slots)
    
    def validate_slot(self, slot: str) -> bool:
        """
        Validate if a given slot is valid (future date, business hours, weekday).
        
        Args:
            slot: Time slot string in format "YYYY-MM-DD HH:MM"
            
        Returns:
            Boolean indicating if slot is valid
        """
        try:
            slot_datetime = datetime.strptime(slot, "%Y-%m-%d %H:%M")
            
            # Check if in future
            if slot_datetime <= datetime.now():
                return False
            
            # Check if weekday
            if slot_datetime.weekday() >= 5:  # Saturday or Sunday
                return False
            
            # Check if during business hours
            if not (self.business_hours_start <= slot_datetime.hour < self.business_hours_end):
                return False
            
            return True
        
        except ValueError:
            return False
    
    def schedule_interview(self, candidate_id: int, slot: str) -> Dict[str, any]:
        """
        Schedule an interview for a candidate.
        
        Args:
            candidate_id: ID of the candidate
            slot: Selected time slot
            
        Returns:
            Dictionary with scheduling information
        """
        if not self.validate_slot(slot):
            return {
                'success': False,
                'message': 'Invalid time slot. Must be a future weekday during business hours.',
                'scheduled_slot': None
            }
        
        return {
            'success': True,
            'message': f'Interview scheduled successfully for {slot}',
            'scheduled_slot': slot,
            'candidate_id': candidate_id
        }
    
    def get_calendar_invite_text(self, candidate_name: str, slot: str, 
                                 recruiter_email: str = "recruiter@hirewise.com") -> str:
        """
        Generate calendar invite text.
        
        Args:
            candidate_name: Name of the candidate
            slot: Scheduled time slot
            recruiter_email: Email of the recruiter
            
        Returns:
            Calendar invite text
        """
        slot_datetime = datetime.strptime(slot, "%Y-%m-%d %H:%M")
        end_datetime = slot_datetime + timedelta(hours=1)  # 1-hour interview
        
        invite_text = f"""
Interview Invitation
====================
Candidate: {candidate_name}
Date: {slot_datetime.strftime("%A, %B %d, %Y")}
Time: {slot_datetime.strftime("%I:%M %p")} - {end_datetime.strftime("%I:%M %p")}
Duration: 1 hour

Meeting Link: https://meet.hirewise.com/interview-{candidate_name.lower().replace(' ', '-')}

Organizer: {recruiter_email}

Please join the meeting at the scheduled time.
"""
        return invite_text
    
    def suggest_rescheduling(self, original_slot: str, num_alternatives: int = 3) -> List[str]:
        """
        Suggest alternative slots for rescheduling.
        
        Args:
            original_slot: Original scheduled slot
            num_alternatives: Number of alternative slots to suggest
            
        Returns:
            List of alternative time slots
        """
        try:
            original_datetime = datetime.strptime(original_slot, "%Y-%m-%d %H:%M")
            alternatives = []
            
            # Suggest +1 day, +2 days, +3 days at same time
            for i in range(1, num_alternatives + 1):
                new_datetime = original_datetime + timedelta(days=i)
                
                # Skip weekends
                while new_datetime.weekday() >= 5:
                    new_datetime += timedelta(days=1)
                
                alternatives.append(new_datetime.strftime("%Y-%m-%d %H:%M"))
            
            return alternatives
        
        except ValueError:
            # If original slot is invalid, just return new suggestions
            return self.suggest_slots(num_alternatives)
