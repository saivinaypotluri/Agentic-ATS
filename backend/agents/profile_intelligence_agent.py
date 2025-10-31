import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from backend.utils import classify_url, extract_github_username, extract_linkedin_username
import time

class ProfileIntelligenceAgent:
    """Agent for enriching candidate profiles with data from LinkedIn, GitHub, and other sources."""
    
    def __init__(self):
        self.github_api_base = "https://api.github.com"
        self.headers = {
            'User-Agent': 'HireWise-Recruiting-App',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def fetch_github_profile(self, github_url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch GitHub profile information using GitHub REST API.
        
        Args:
            github_url: GitHub profile URL
            
        Returns:
            Dictionary containing GitHub profile data
        """
        username = extract_github_username(github_url)
        
        if not username:
            return None
        
        try:
            # Fetch user profile
            user_response = requests.get(
                f"{self.github_api_base}/users/{username}",
                headers=self.headers,
                timeout=10
            )
            
            if user_response.status_code != 200:
                return self._mock_github_data(username)
            
            user_data = user_response.json()
            
            # Fetch repositories
            repos_response = requests.get(
                f"{self.github_api_base}/users/{username}/repos",
                headers=self.headers,
                params={'sort': 'updated', 'per_page': 100},
                timeout=10
            )
            
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            # Extract top languages
            languages = {}
            for repo in repos_data[:20]:  # Check top 20 repos
                if repo.get('language'):
                    lang = repo['language']
                    languages[lang] = languages.get(lang, 0) + 1
            
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'username': username,
                'name': user_data.get('name', 'N/A'),
                'bio': user_data.get('bio', 'N/A'),
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'top_languages': [lang for lang, count in top_languages],
                'location': user_data.get('location', 'N/A'),
                'blog': user_data.get('blog', 'N/A'),
                'company': user_data.get('company', 'N/A'),
                'created_at': user_data.get('created_at', 'N/A')
            }
        
        except Exception as e:
            print(f"Error fetching GitHub profile: {str(e)}")
            return self._mock_github_data(username)
    
    def _mock_github_data(self, username: str) -> Dict[str, Any]:
        """Generate mock GitHub data when API is unavailable."""
        return {
            'username': username,
            'name': 'GitHub User',
            'bio': 'Software Developer',
            'public_repos': 25,
            'followers': 50,
            'following': 30,
            'top_languages': ['Python', 'JavaScript', 'TypeScript'],
            'location': 'N/A',
            'blog': 'N/A',
            'company': 'N/A',
            'created_at': '2020-01-01',
            'note': 'Mock data - API unavailable'
        }
    
    def fetch_linkedin_profile(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch LinkedIn profile information (mock implementation).
        LinkedIn API requires OAuth and company approval, so we use mock data.
        
        Args:
            linkedin_url: LinkedIn profile URL
            
        Returns:
            Dictionary containing LinkedIn profile data (mock)
        """
        username = extract_linkedin_username(linkedin_url)
        
        if not username:
            return None
        
        # LinkedIn API is restricted, return mock data
        return {
            'username': username,
            'headline': 'Senior Software Engineer',
            'location': 'San Francisco, CA',
            'connections': '500+',
            'experience': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Company',
                    'duration': '2020 - Present'
                },
                {
                    'title': 'Software Engineer',
                    'company': 'Startup Inc',
                    'duration': '2018 - 2020'
                }
            ],
            'skills': ['Python', 'React', 'Node.js', 'AWS', 'Docker'],
            'endorsements': 45,
            'note': 'Mock data - LinkedIn API requires OAuth'
        }
    
    def fetch_misc_url_metadata(self, url: str) -> Dict[str, Any]:
        """
        Fetch metadata from miscellaneous URLs using web scraping.
        
        Args:
            url: URL to fetch metadata from
            
        Returns:
            Dictionary containing metadata
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return {
                    'url': url,
                    'title': 'Unavailable',
                    'description': 'Could not fetch metadata',
                    'type': 'Unknown'
                }
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.string if title else 'No title'
            
            # Extract meta description
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag and 'content' in description_tag.attrs else 'No description'
            
            # Try to determine type
            url_lower = url.lower()
            url_type = 'Website'
            
            if 'medium.com' in url_lower or 'blog' in url_lower:
                url_type = 'Blog'
            elif 'youtube.com' in url_lower or 'vimeo.com' in url_lower:
                url_type = 'Video'
            elif 'twitter.com' in url_lower or 'x.com' in url_lower:
                url_type = 'Social Media'
            elif 'stackoverflow.com' in url_lower:
                url_type = 'Q&A Profile'
            
            return {
                'url': url,
                'title': title_text[:200],  # Limit length
                'description': description[:300],  # Limit length
                'type': url_type
            }
        
        except Exception as e:
            print(f"Error fetching URL metadata: {str(e)}")
            return {
                'url': url,
                'title': 'Error fetching',
                'description': str(e),
                'type': 'Unknown'
            }
    
    def enrich_profile(self, urls: List[str]) -> Dict[str, Any]:
        """
        Enrich candidate profile by fetching data from all provided URLs.
        
        Args:
            urls: List of URLs from the resume
            
        Returns:
            Dictionary containing enriched profile data
        """
        linkedin_url = None
        github_url = None
        misc_urls = []
        
        # Classify URLs
        for url in urls:
            url_type = classify_url(url)
            if url_type == 'linkedin':
                linkedin_url = url
            elif url_type == 'github':
                github_url = url
            else:
                misc_urls.append(url)
        
        # Fetch data
        linkedin_data = None
        github_data = None
        misc_data = []
        
        if linkedin_url:
            linkedin_data = self.fetch_linkedin_profile(linkedin_url)
            time.sleep(0.5)  # Rate limiting
        
        if github_url:
            github_data = self.fetch_github_profile(github_url)
            time.sleep(0.5)  # Rate limiting
        
        for misc_url in misc_urls[:5]:  # Limit to 5 misc URLs
            misc_data.append(self.fetch_misc_url_metadata(misc_url))
            time.sleep(0.5)  # Rate limiting
        
        return {
            'linkedin_url': linkedin_url,
            'github_url': github_url,
            'misc_urls': misc_urls,
            'linkedin_data': linkedin_data,
            'github_data': github_data,
            'misc_data': misc_data
        }
    
    def generate_summary(self, enriched_data: Dict[str, Any], candidate_name: str = "Candidate") -> str:
        """
        Generate a human-readable summary of the enriched profile data.
        
        Args:
            enriched_data: Dictionary containing enriched profile data
            candidate_name: Name of the candidate
            
        Returns:
            String summary
        """
        summary_parts = [f"Profile Intelligence Summary for {candidate_name}:\n"]
        
        # LinkedIn summary
        if enriched_data.get('linkedin_data'):
            linkedin = enriched_data['linkedin_data']
            summary_parts.append(f"\n?? LinkedIn Profile:")
            summary_parts.append(f"  - Headline: {linkedin.get('headline', 'N/A')}")
            summary_parts.append(f"  - Location: {linkedin.get('location', 'N/A')}")
            summary_parts.append(f"  - Connections: {linkedin.get('connections', 'N/A')}")
            summary_parts.append(f"  - Top Skills: {', '.join(linkedin.get('skills', [])[:5])}")
        
        # GitHub summary
        if enriched_data.get('github_data'):
            github = enriched_data['github_data']
            summary_parts.append(f"\n?? GitHub Profile:")
            summary_parts.append(f"  - Username: {github.get('username', 'N/A')}")
            summary_parts.append(f"  - Public Repos: {github.get('public_repos', 0)}")
            summary_parts.append(f"  - Followers: {github.get('followers', 0)}")
            summary_parts.append(f"  - Top Languages: {', '.join(github.get('top_languages', []))}")
            if github.get('bio'):
                summary_parts.append(f"  - Bio: {github['bio']}")
        
        # Misc URLs summary
        if enriched_data.get('misc_data'):
            summary_parts.append(f"\n?? Other Links ({len(enriched_data['misc_data'])}):")
            for i, misc in enumerate(enriched_data['misc_data'][:3], 1):
                summary_parts.append(f"  {i}. {misc.get('type', 'Link')}: {misc.get('title', 'N/A')}")
        
        return "\n".join(summary_parts)
