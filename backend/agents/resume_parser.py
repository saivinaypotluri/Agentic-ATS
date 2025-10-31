import fitz  # PyMuPDF
from docx import Document
from typing import Dict, Optional, List
import re
from backend.utils import (
    extract_emails, 
    extract_phone_numbers, 
    extract_urls,
    extract_name_from_text,
    extract_skills_keywords
)

class ResumeParser:
    """Agent for parsing resumes and extracting structured information."""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def extract_text(self, file_path: str, file_extension: str) -> str:
        """Extract text based on file extension."""
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information from resume text."""
        education = []
        
        # Common education keywords
        edu_keywords = ['education', 'academic', 'qualification', 'degree']
        degree_types = ['bachelor', 'master', 'phd', 'mba', 'b.s.', 'b.a.', 'm.s.', 'm.a.', 'ph.d.']
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Find education section
        edu_section_start = -1
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in edu_keywords):
                edu_section_start = i
                break
        
        # Extract degrees
        if edu_section_start != -1:
            # Look at next 10 lines after education section
            for line in lines[edu_section_start:edu_section_start + 10]:
                if any(degree in line.lower() for degree in degree_types):
                    education.append({
                        'degree': line.strip(),
                        'field': 'Not specified'
                    })
        
        return education if education else [{'degree': 'Not found', 'field': 'Not found'}]
    
    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience from resume text."""
        experience = []
        
        # Common experience keywords
        exp_keywords = ['experience', 'employment', 'work history', 'professional experience']
        
        lines = text.split('\n')
        
        # Find experience section
        exp_section_start = -1
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in exp_keywords):
                exp_section_start = i
                break
        
        # Extract job titles (simple heuristic)
        if exp_section_start != -1:
            for line in lines[exp_section_start:exp_section_start + 15]:
                # Look for lines with years (e.g., 2020-2023)
                if re.search(r'\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*present', line.lower()):
                    experience.append({
                        'title': 'Position',
                        'duration': line.strip()
                    })
        
        return experience if experience else [{'title': 'Not found', 'duration': 'N/A'}]
    
    def parse(self, file_path: str, file_extension: str) -> Dict:
        """
        Parse resume and extract structured information.
        
        Returns:
            Dict containing extracted information
        """
        # Extract raw text
        resume_text = self.extract_text(file_path, file_extension)
        
        # Extract basic info
        emails = extract_emails(resume_text)
        phones = extract_phone_numbers(resume_text)
        urls = extract_urls(resume_text)
        name = extract_name_from_text(resume_text)
        skills = extract_skills_keywords(resume_text)
        education = self.extract_education(resume_text)
        experience = self.extract_experience(resume_text)
        
        return {
            'resume_text': resume_text,
            'name': name,
            'email': emails[0] if emails else None,
            'phone': phones[0] if phones else None,
            'urls': urls,
            'skills': skills,
            'education': education,
            'experience': experience
        }
