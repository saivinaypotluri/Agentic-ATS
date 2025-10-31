# ?? HireWise Quick Start Guide

Get HireWise up and running in under 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git

## Quick Start (Local Development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd hirewise
```

### 2. Start Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload
```

Backend will be running at `http://localhost:8000`

### 3. Start Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be running at `http://localhost:3000`

## Quick Start (Docker)

```bash
docker-compose up --build
```

That's it! Visit `http://localhost:3000`

## First Steps

1. **Upload a Resume**
   - Go to http://localhost:3000/upload
   - Upload a PDF, DOCX, or TXT resume
   - Watch as HireWise automatically extracts candidate information

2. **View Candidates**
   - Go to http://localhost:3000/candidates
   - See all uploaded candidates
   - Click "View Details" on any candidate

3. **Match with Job**
   - On candidate detail page, paste a job description
   - Click "Compute Match Score"
   - See AI-powered match score (0-100)

4. **Enrich Profile**
   - If the resume has LinkedIn or GitHub URLs
   - Click "Enrich Profile from URLs"
   - Get detailed profile intelligence

5. **Schedule Interview**
   - Click "Get Suggested Slots"
   - Select a time slot
   - Click "Schedule Interview"

6. **Submit Feedback**
   - After interview, enter notes
   - Click "Generate Feedback Summary"
   - Get AI-generated structured feedback

## Sample Resume

Create a sample resume (save as `sample_resume.txt`):

```
John Doe
john.doe@email.com
(555) 123-4567

PROFESSIONAL SUMMARY
Senior Software Engineer with 5+ years of experience in full-stack development.

SKILLS
Python, JavaScript, React, Node.js, FastAPI, Docker, PostgreSQL, AWS, Git

EXPERIENCE
Senior Software Engineer | Tech Company | 2020 - Present
- Developed microservices using Python and FastAPI
- Built responsive web applications with React
- Implemented CI/CD pipelines

Software Engineer | Startup Inc | 2018 - 2020
- Created REST APIs using Node.js and Express
- Worked with MongoDB and PostgreSQL databases

EDUCATION
Bachelor of Science in Computer Science
University Name | 2014 - 2018

LINKS
https://linkedin.com/in/johndoe
https://github.com/johndoe
```

## Troubleshooting

**Backend not starting?**
```bash
# Make sure you're in the right directory
cd /path/to/hirewise
python -m uvicorn backend.main:app --reload
```

**Frontend not starting?**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Can't connect to backend from frontend?**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API_BASE_URL in `frontend/src/services/api.js`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API docs at http://localhost:8000/docs
- Check out the agent implementations in `backend/agents/`
- Customize the UI in `frontend/src/pages/`

## Support

Issues? Questions? Open an issue on GitHub!

Happy Recruiting! ??
