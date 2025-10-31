from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple

class JobMatchAgent:
    """Agent for computing semantic similarity between resume and job description."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the job match agent with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Warning: Could not load model {model_name}. Using mock mode.")
            self.model = None
    
    def compute_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Compute semantic similarity between resume and job description.
        
        Args:
            resume_text: The candidate's resume text
            job_description: The job description text
            
        Returns:
            Similarity score between 0 and 100
        """
        if self.model is None:
            # Mock mode: return a score based on keyword overlap
            return self._mock_similarity(resume_text, job_description)
        
        try:
            # Generate embeddings
            resume_embedding = self.model.encode([resume_text])
            job_embedding = self.model.encode([job_description])
            
            # Compute cosine similarity
            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
            
            # Convert to 0-100 scale
            score = float(similarity * 100)
            
            return round(score, 2)
        
        except Exception as e:
            print(f"Error computing similarity: {str(e)}. Falling back to mock mode.")
            return self._mock_similarity(resume_text, job_description)
    
    def _mock_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Fallback method using simple keyword matching.
        
        Args:
            resume_text: The candidate's resume text
            job_description: The job description text
            
        Returns:
            Mock similarity score between 0 and 100
        """
        # Extract words from both texts
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                      'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
                      'could', 'should', 'may', 'might', 'must', 'can'}
        
        resume_words = resume_words - stop_words
        job_words = job_words - stop_words
        
        # Calculate Jaccard similarity
        if not job_words:
            return 0.0
        
        intersection = len(resume_words.intersection(job_words))
        union = len(resume_words.union(job_words))
        
        if union == 0:
            return 0.0
        
        jaccard_score = (intersection / union) * 100
        
        # Add bonus for keyword matches
        important_keywords = ['experience', 'skills', 'python', 'java', 'javascript', 
                             'react', 'node', 'sql', 'aws', 'docker', 'kubernetes',
                             'machine learning', 'data', 'api', 'backend', 'frontend']
        
        keyword_matches = sum(1 for keyword in important_keywords 
                             if keyword in resume_text.lower() and keyword in job_description.lower())
        
        bonus = min(keyword_matches * 5, 30)  # Max 30 bonus points
        
        final_score = min(jaccard_score + bonus, 100)
        
        return round(final_score, 2)
    
    def get_match_explanation(self, score: float) -> str:
        """
        Get a textual explanation of the match score.
        
        Args:
            score: The match score (0-100)
            
        Returns:
            String explanation of the score
        """
        if score >= 80:
            return "Excellent match - Candidate's profile strongly aligns with job requirements"
        elif score >= 60:
            return "Good match - Candidate has most of the required qualifications"
        elif score >= 40:
            return "Moderate match - Candidate has some relevant skills but may need training"
        elif score >= 20:
            return "Weak match - Candidate has limited relevant experience"
        else:
            return "Poor match - Candidate's profile does not align well with job requirements"
