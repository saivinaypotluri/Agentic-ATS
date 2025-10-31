import re
from typing import List, Tuple

def extract_urls(text: str) -> List[str]:
    """Extract all URLs from text"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    return urls

def classify_url(url: str) -> Tuple[str, str]:
    """Classify URL as LinkedIn, GitHub, or Misc"""
    url_lower = url.lower()
    if 'linkedin.com' in url_lower:
        return 'linkedin', url
    elif 'github.com' in url_lower:
        return 'github', url
    else:
        return 'misc', url

def extract_github_username(url: str) -> str:
    """Extract GitHub username from URL"""
    pattern = r'github\.com/([^/\s]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_linkedin_username(url: str) -> str:
    """Extract LinkedIn username from URL"""
    pattern = r'linkedin\.com/in/([^/\s]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_email(text: str) -> str:
    """Extract email from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    # Match various phone formats
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None
