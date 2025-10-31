import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text."""
    # Various phone number patterns
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US/International
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\d{3}-\d{3}-\d{4}',  # XXX-XXX-XXXX
        r'\d{10}',  # 10 digits
    ]
    
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    
    return list(set(phones))  # Remove duplicates

def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)

def classify_url(url: str) -> str:
    """Classify URL by platform."""
    url_lower = url.lower()
    
    if 'linkedin.com' in url_lower:
        return 'linkedin'
    elif 'github.com' in url_lower:
        return 'github'
    else:
        return 'misc'

def extract_github_username(url: str) -> Optional[str]:
    """Extract GitHub username from URL."""
    pattern = r'github\.com/([a-zA-Z0-9-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_linkedin_username(url: str) -> Optional[str]:
    """Extract LinkedIn username/ID from URL."""
    pattern = r'linkedin\.com/in/([a-zA-Z0-9-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def generate_interview_slots(num_slots: int = 5) -> List[str]:
    """Generate suggested interview time slots."""
    slots = []
    current_date = datetime.now()
    
    # Start from next business day
    days_ahead = 1
    while len(slots) < num_slots:
        future_date = current_date + timedelta(days=days_ahead)
        
        # Skip weekends
        if future_date.weekday() < 5:  # Monday = 0, Friday = 4
            # Morning slot
            morning = future_date.replace(hour=10, minute=0, second=0, microsecond=0)
            slots.append(morning.strftime("%Y-%m-%d %H:%M"))
            
            if len(slots) < num_slots:
                # Afternoon slot
                afternoon = future_date.replace(hour=14, minute=0, second=0, microsecond=0)
                slots.append(afternoon.strftime("%Y-%m-%d %H:%M"))
        
        days_ahead += 1
    
    return slots[:num_slots]

def extract_name_from_text(text: str) -> Optional[str]:
    """Extract potential name from resume text (first few lines)."""
    lines = text.strip().split('\n')
    
    # Usually name is in the first 5 lines
    for line in lines[:5]:
        line = line.strip()
        # Simple heuristic: name is usually 2-4 words, capitalized, no special chars
        if line and len(line.split()) <= 4 and len(line.split()) >= 2:
            if line[0].isupper() and not any(char in line for char in ['@', 'http', ':', '/']):
                return line
    
    return None

def extract_skills_keywords(text: str) -> List[str]:
    """Extract potential skills from text using common keywords."""
    common_skills = [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring boot',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'git', 'ci/cd', 'jenkins', 'terraform',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'data analysis', 'pandas', 'numpy', 'data visualization', 'tableau', 'power bi',
        'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'devops',
        'html', 'css', 'sass', 'tailwind', 'bootstrap', 'redux', 'next.js',
        'c++', 'c#', '.net', 'ruby', 'rails', 'php', 'laravel', 'go', 'rust',
        'elasticsearch', 'kafka', 'rabbitmq', 'nginx', 'linux', 'bash'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            # Capitalize properly
            found_skills.append(skill.title() if skill.islower() else skill)
    
    return list(set(found_skills))  # Remove duplicates
