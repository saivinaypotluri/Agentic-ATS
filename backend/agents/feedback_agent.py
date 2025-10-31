from typing import Dict, Optional
import re

class FeedbackAgent:
    """Agent for processing and summarizing interview feedback."""
    
    def __init__(self):
        self.rating_keywords = {
            'excellent': 5,
            'outstanding': 5,
            'exceptional': 5,
            'great': 4,
            'good': 4,
            'solid': 4,
            'satisfactory': 3,
            'average': 3,
            'adequate': 3,
            'below average': 2,
            'poor': 2,
            'weak': 2,
            'unsatisfactory': 1,
            'unacceptable': 1
        }
        
        self.skill_categories = [
            'technical skills',
            'communication',
            'problem solving',
            'teamwork',
            'leadership',
            'cultural fit'
        ]
    
    def extract_rating(self, text: str) -> Optional[int]:
        """
        Extract overall rating from feedback text.
        
        Args:
            text: Feedback text
            
        Returns:
            Rating from 1-5, or None if not found
        """
        text_lower = text.lower()
        
        # Look for explicit ratings like "rating: 4/5" or "score: 8/10"
        rating_patterns = [
            r'rating[:\s]+(\d+)[/\s]*(?:out of\s*)?[5]',
            r'score[:\s]+(\d+)[/\s]*(?:out of\s*)?[5]',
            r'(\d+)[/\s]*(?:out of\s*)?[5]'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, text_lower)
            if match:
                rating = int(match.group(1))
                if 1 <= rating <= 5:
                    return rating
        
        # Fallback: use keyword analysis
        max_rating = 0
        for keyword, rating in self.rating_keywords.items():
            if keyword in text_lower:
                max_rating = max(max_rating, rating)
        
        return max_rating if max_rating > 0 else 3  # Default to 3
    
    def extract_strengths_and_weaknesses(self, text: str) -> Dict[str, list]:
        """
        Extract strengths and weaknesses from feedback text.
        
        Args:
            text: Feedback text
            
        Returns:
            Dictionary with 'strengths' and 'weaknesses' lists
        """
        strengths = []
        weaknesses = []
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect section headers
            if any(word in line_lower for word in ['strength', 'positive', 'pros', 'advantages']):
                current_section = 'strengths'
                continue
            elif any(word in line_lower for word in ['weakness', 'area for improvement', 'concerns', 'cons', 'disadvantages']):
                current_section = 'weaknesses'
                continue
            
            # Extract bullet points or numbered items
            if line.strip() and (line.strip().startswith('-') or 
                                line.strip().startswith('?') or 
                                line.strip()[0].isdigit()):
                cleaned_line = re.sub(r'^[-?\d.)\s]+', '', line).strip()
                
                if cleaned_line:
                    if current_section == 'strengths':
                        strengths.append(cleaned_line)
                    elif current_section == 'weaknesses':
                        weaknesses.append(cleaned_line)
        
        # If no explicit sections found, use keyword analysis
        if not strengths and not weaknesses:
            sentences = text.split('.')
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                
                if any(word in sentence_lower for word in ['strong', 'good', 'excellent', 'impressive', 'skilled']):
                    strengths.append(sentence.strip())
                elif any(word in sentence_lower for word in ['weak', 'struggle', 'lack', 'need improvement', 'concern']):
                    weaknesses.append(sentence.strip())
        
        return {
            'strengths': strengths[:5],  # Limit to top 5
            'weaknesses': weaknesses[:5]
        }
    
    def generate_summary(self, interview_notes: str, candidate_name: str = "Candidate") -> str:
        """
        Generate a structured summary of interview feedback.
        
        Args:
            interview_notes: Raw interview notes
            candidate_name: Name of the candidate
            
        Returns:
            Structured feedback summary
        """
        # Extract information
        rating = self.extract_rating(interview_notes)
        sw = self.extract_strengths_and_weaknesses(interview_notes)
        
        # Generate summary
        summary_parts = [
            f"Interview Feedback Summary for {candidate_name}",
            "=" * 50,
            f"\n?? Overall Rating: {rating}/5",
            f"\n{'?' * rating}{'?' * (5 - rating)}",
        ]
        
        # Add strengths
        if sw['strengths']:
            summary_parts.append("\n? Key Strengths:")
            for i, strength in enumerate(sw['strengths'], 1):
                summary_parts.append(f"  {i}. {strength}")
        
        # Add weaknesses
        if sw['weaknesses']:
            summary_parts.append("\n??  Areas for Improvement:")
            for i, weakness in enumerate(sw['weaknesses'], 1):
                summary_parts.append(f"  {i}. {weakness}")
        
        # Add recommendation
        summary_parts.append("\n?? Recommendation:")
        if rating >= 4:
            summary_parts.append("  Strong candidate. Recommend moving forward to next round.")
        elif rating >= 3:
            summary_parts.append("  Qualified candidate. Consider for further evaluation.")
        else:
            summary_parts.append("  May not meet current requirements. Consider other candidates.")
        
        # Add original notes
        summary_parts.append("\n?? Original Notes:")
        summary_parts.append("  " + interview_notes[:500])  # First 500 chars
        
        return "\n".join(summary_parts)
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze the sentiment of the feedback.
        
        Args:
            text: Feedback text
            
        Returns:
            Sentiment label: 'Positive', 'Neutral', or 'Negative'
        """
        text_lower = text.lower()
        
        positive_words = ['excellent', 'great', 'good', 'strong', 'impressive', 
                         'outstanding', 'skilled', 'proficient', 'capable']
        negative_words = ['poor', 'weak', 'lacking', 'concern', 'struggle', 
                         'inadequate', 'insufficient', 'below']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count + 2:
            return 'Positive'
        elif negative_count > positive_count + 2:
            return 'Negative'
        else:
            return 'Neutral'
