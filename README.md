# ?? HireWise - AI-Powered Recruiting Assistant

HireWise is a production-ready agentic AI recruiting assistant that automates parts of the hiring process while keeping **humans in the loop**. It intelligently parses resumes, evaluates candidate-job fit, gathers insights from LinkedIn and GitHub, and presents structured candidate summaries for recruiter approval.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-blue.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3+-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)

---

## ?? Key Features

### 1. ?? Resume Upload & Parsing Agent
- Upload PDF, DOCX, or TXT resumes
- Automatically extract: Name, Email, Phone, Skills, Education, Experience
- Uses **PyMuPDF** for text extraction and custom entity recognition

### 2. ?? Job Match Agent
- Semantic similarity scoring between resumes and job descriptions
- Uses **SentenceTransformers (all-MiniLM-L6-v2)** for embeddings
- Returns match scores from 0-100 with explanations

### 3. ?? Profile Intelligence Agent
- Detects and enriches URLs from resumes
- **LinkedIn**: Fetches experience, skills, endorsements (mock data due to API restrictions)
- **GitHub**: Real-time data via GitHub REST API (repos, languages, followers)
- **Other Links**: Extracts metadata using BeautifulSoup

### 4. ?? Human-in-the-Loop Dashboard
- Beautiful React + Tailwind CSS interface
- Review AI-generated insights
- ? Approve, ??? Edit, or ? Reject candidates
- Real-time updates and responsive design

### 5. ?? Interview Scheduler Agent
- Suggests optimal interview time slots
- Validates business hours and weekdays
- Stores scheduled interviews in database

### 6. ?? Feedback Agent
- Processes and summarizes interview notes
- Extracts strengths, weaknesses, and ratings
- Generates structured feedback summaries

---

## ??? Architecture

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18.2 + Tailwind CSS 3.3 + Vite |
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | SQLite + SQLAlchemy ORM |
| **AI/ML** | SentenceTransformers, LangChain, PyMuPDF |
| **Deployment** | Docker Compose |

### Project Structure

```
hirewise/
??? backend/
?   ??? main.py                      # FastAPI application entry point
?   ??? database.py                  # SQLAlchemy database configuration
?   ??? schemas.py                   # Pydantic schemas for validation
?   ??? utils.py                     # Utility functions
?   ??? requirements.txt             # Python dependencies
?   ??? models/
?   ?   ??? candidate.py             # SQLAlchemy ORM models
?   ??? routers/
?   ?   ??? candidates.py            # Candidate management endpoints
?   ?   ??? jobs.py                  # Job matching & scheduling endpoints
?   ?   ??? feedback.py              # Feedback endpoints
?   ??? agents/
?       ??? resume_parser.py         # Resume parsing agent
?       ??? job_match_agent.py       # Job matching agent
?       ??? profile_intelligence_agent.py  # Profile enrichment agent
?       ??? scheduler_agent.py       # Interview scheduling agent
?       ??? feedback_agent.py        # Feedback processing agent
??? frontend/
?   ??? src/
?   ?   ??? main.jsx                 # React entry point
?   ?   ??? App.jsx                  # Main application component
?   ?   ??? index.css                # Tailwind CSS imports
?   ?   ??? services/
?   ?   ?   ??? api.js               # API client
?   ?   ??? pages/
?   ?   ?   ??? HomePage.jsx         # Landing page
?   ?   ?   ??? UploadPage.jsx       # Resume upload interface
?   ?   ?   ??? CandidatesPage.jsx   # Candidates list
?   ?   ?   ??? CandidateDetailPage.jsx  # Candidate detail view
?   ?   ??? components/              # Reusable components
?   ??? package.json                 # Node dependencies
?   ??? vite.config.js               # Vite configuration
?   ??? tailwind.config.js           # Tailwind CSS configuration
?   ??? index.html                   # HTML entry point
??? docker-compose.yml               # Docker Compose configuration
??? Dockerfile.backend               # Backend Docker image
??? Dockerfile.frontend              # Frontend Docker image
??? .env.example                     # Environment variables template
??? .gitignore                       # Git ignore file
??? README.md                        # This file
```

---

## ?? Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Docker & Docker Compose** (optional)

### Option 1: Local Development (Without Docker)

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd hirewise
```

#### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
cd ..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 3. Set Up Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Option 2: Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

Services:
- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

To stop services:
```bash
docker-compose down
```

---

## ?? API Documentation

### Backend Endpoints

#### Candidate Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload_resume` | POST | Upload and parse a resume file |
| `/api/get_candidate/{id}` | GET | Retrieve candidate by ID |
| `/api/get_all_candidates` | GET | List all candidates with pagination |
| `/api/update_candidate/{id}` | PUT | Update candidate information |
| `/api/approve_candidate` | POST | Approve or reject a candidate |
| `/api/delete_candidate/{id}` | DELETE | Delete a candidate |

#### Job Matching & Intelligence

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/match_job` | POST | Compute semantic match score |
| `/api/fetch_profiles` | POST | Enrich profile with LinkedIn/GitHub data |
| `/api/schedule_interview` | POST | Get suggestions or schedule interview |
| `/api/get_interview_slots` | GET | Get available interview slots |

#### Feedback

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/feedback` | POST | Submit and summarize interview feedback |
| `/api/get_feedback/{id}` | GET | Retrieve candidate feedback |
| `/api/analyze_sentiment/{id}` | GET | Analyze feedback sentiment |

---

## ?? Frontend Features

### Pages

1. **Home Page** (`/`)
   - Feature overview
   - Quick navigation to upload and candidates

2. **Upload Page** (`/upload`)
   - Drag-and-drop file upload
   - Supports PDF, DOCX, TXT
   - Real-time parsing feedback

3. **Candidates Page** (`/candidates`)
   - List all candidates
   - Filter by status (All, Approved, Pending, Rejected)
   - Quick view of match scores and skills

4. **Candidate Detail Page** (`/candidate/:id`)
   - Complete candidate profile
   - Edit basic information
   - Job matching interface
   - Profile enrichment
   - Interview scheduling
   - Feedback submission

---

## ?? AI Agents Explained

### 1. Resume Parser Agent
- **Technology**: PyMuPDF (PDF), python-docx (DOCX)
- **Capabilities**:
  - Text extraction from multiple formats
  - Entity recognition (name, email, phone)
  - Skills extraction using keyword matching
  - Education and experience parsing

### 2. Job Match Agent
- **Technology**: SentenceTransformers (all-MiniLM-L6-v2)
- **Algorithm**:
  - Converts text to embeddings
  - Computes cosine similarity
  - Falls back to Jaccard similarity if model unavailable
- **Output**: Match score (0-100) with explanation

### 3. Profile Intelligence Agent
- **LinkedIn**: Mock data (LinkedIn API requires OAuth)
- **GitHub**: Real API integration with rate limiting
  - Fetches user profile, repos, languages
  - Extracts top programming languages
- **Misc URLs**: Web scraping with BeautifulSoup
- **Output**: Structured profile data + AI summary

### 4. Scheduler Agent
- **Capabilities**:
  - Generate time slots for next 5 business days
  - Validate business hours (9 AM - 5 PM)
  - Skip weekends
  - Calendar invite generation

### 5. Feedback Agent
- **Capabilities**:
  - Extract ratings from text
  - Identify strengths and weaknesses
  - Sentiment analysis
  - Generate structured summaries

---

## ?? Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Backend
BACKEND_PORT=8000

# Frontend
FRONTEND_PORT=3000

# Database
DATABASE_URL=sqlite:///./hirewise.db

# Optional: For enhanced features
OPENAI_API_KEY=your_key_here        # For real GPT integration
GITHUB_TOKEN=your_token_here         # For higher GitHub API rate limits
```

---

## ?? Testing

### Test the Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests (if test suite is added)
pytest backend/tests/

# Or test manually via API docs
# Visit: http://localhost:8000/docs
```

### Test the Frontend

```bash
cd frontend
npm run test  # If tests are configured
```

---

## ?? Database Schema

### Candidate Table

```sql
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    resume_text TEXT,
    resume_filename VARCHAR,
    
    -- URLs
    linkedin_url VARCHAR,
    github_url VARCHAR,
    misc_links JSON,
    
    -- Enriched data
    linkedin_data JSON,
    github_data JSON,
    misc_data JSON,
    
    -- Extracted info
    skills JSON,
    education JSON,
    experience JSON,
    
    -- Job matching
    job_description TEXT,
    match_score FLOAT,
    
    -- Status
    approved BOOLEAN DEFAULT FALSE,
    rejected BOOLEAN DEFAULT FALSE,
    
    -- Interview
    scheduled_interview VARCHAR,
    interview_notes TEXT,
    feedback TEXT,
    feedback_summary TEXT,
    
    -- Timestamps
    created_at DATETIME,
    updated_at DATETIME
);
```

---

## ?? Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'backend'`
```bash
# Make sure you're running from the project root
cd /path/to/hirewise
python -m uvicorn backend.main:app --reload
```

**Issue**: `SentenceTransformer model download fails`
```bash
# The first run will download the model (1.2GB)
# Ensure you have internet connection and disk space
```

### Frontend Issues

**Issue**: `Cannot connect to backend`
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/main.py`

**Issue**: `npm install fails`
```bash
# Clear npm cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## ?? Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ?? License

This project is licensed under the MIT License.

---

## ?? Acknowledgments

- **FastAPI** - Modern web framework for building APIs
- **React** - UI library for building user interfaces
- **Tailwind CSS** - Utility-first CSS framework
- **SentenceTransformers** - State-of-the-art text embeddings
- **PyMuPDF** - PDF processing library
- **GitHub API** - For profile enrichment

---

## ?? Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

## ??? Roadmap

- [ ] Add authentication and authorization
- [ ] Integrate real OpenAI GPT for summaries
- [ ] Add email notifications for scheduled interviews
- [ ] Implement bulk resume upload
- [ ] Add analytics dashboard
- [ ] Support for more file formats (PNG, JPG for image resumes)
- [ ] Export candidate reports as PDF
- [ ] Integration with ATS systems

---

**Built with ?? by AI Engineers**
