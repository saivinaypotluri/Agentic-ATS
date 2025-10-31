# 🚀 HireWise Installation Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher

### Software Dependencies
- Git
- Python 3.10+
- Node.js 18+ with npm
- (Optional) Docker Desktop

---

## Installation Methods

Choose one of the following installation methods:

### Method 1: Quick Start Script (Recommended for macOS/Linux)

```bash
# Clone repository
git clone <repository-url>
cd hirewise

# Make start script executable
chmod +x start.sh

# Run the application
./start.sh
```

The script will automatically:
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Start both servers

**Access the application:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Method 2: Manual Installation (All Platforms)

#### Step 1: Clone Repository

```bash
git clone <repository-url>
cd hirewise
```

#### Step 2: Set Up Backend

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

# Return to project root
cd ..

# Start backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Keep this terminal open. The backend will be running on http://localhost:8000

#### Step 3: Set Up Frontend (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be running on http://localhost:3000

---

### Method 3: Docker Installation (Recommended for Production)

```bash
# Clone repository
git clone <repository-url>
cd hirewise

# Build and start containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Stop containers:**
```bash
docker-compose down
```

---

## Post-Installation Setup

### 1. Verify Backend

Open your browser and go to:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

You should see the interactive API documentation.

### 2. Verify Frontend

Open your browser and go to:
- Home Page: http://localhost:3000

You should see the HireWise landing page.

### 3. Test Upload Feature

1. Go to http://localhost:3000/upload
2. Upload the provided `sample_resume.txt`
3. Verify that candidate information is extracted correctly

---

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
# Copy example file
cp .env.example .env

# Edit with your settings
nano .env  # or use any text editor
```

**Available variables:**

```bash
# Backend Configuration
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_PORT=3000

# Database
DATABASE_URL=sqlite:///./hirewise.db

# Optional: OpenAI API Key
OPENAI_API_KEY=your_key_here

# Optional: GitHub Token (for higher rate limits)
GITHUB_TOKEN=your_token_here
```

---

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue 1: Port 8000 already in use**

```bash
# Find process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Issue 2: ModuleNotFoundError**

```bash
# Make sure virtual environment is activated
cd backend
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue 3: SentenceTransformers model download fails**

```bash
# The first run downloads ~1.2GB model
# Ensure you have:
# - Internet connection
# - At least 2GB free disk space
# - Wait for download to complete (may take 5-10 minutes)
```

#### Frontend Issues

**Issue 1: Port 3000 already in use**

```bash
# Option 1: Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Option 2: Use different port
# Edit frontend/vite.config.js:
server: {
  port: 3001  // Change to any available port
}
```

**Issue 2: npm install fails**

```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue 3: Cannot connect to backend**

```bash
# Verify backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy","service":"HireWise API"}

# If not, check backend terminal for errors
```

#### Docker Issues

**Issue 1: Docker build fails**

```bash
# Ensure Docker Desktop is running
docker --version

# Clean up and rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

**Issue 2: Containers start but can't access**

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Restart containers
docker-compose restart
```

---

## Verification Checklist

After installation, verify everything is working:

- [ ] Backend health check returns success
- [ ] API docs accessible at /docs
- [ ] Frontend loads home page
- [ ] Can navigate to upload page
- [ ] Can upload sample resume
- [ ] Resume parsing works
- [ ] Candidate list shows uploaded candidate
- [ ] Can view candidate details
- [ ] Job matching works
- [ ] Profile enrichment works (if GitHub URL provided)
- [ ] Interview scheduling works
- [ ] Feedback submission works

---

## Development Tools

### Recommended IDE Extensions

**VS Code:**
- Python (Microsoft)
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Docker
- ESLint
- Prettier

**PyCharm:**
- JavaScript and TypeScript
- Docker
- Tailwind CSS

### Database Tools

**View SQLite Database:**

```bash
# Install sqlite3
# macOS:
brew install sqlite3

# Ubuntu:
sudo apt-get install sqlite3

# View database
sqlite3 hirewise.db
.tables
SELECT * FROM candidates;
.exit
```

Or use GUI tools:
- DB Browser for SQLite
- DBeaver
- DataGrip

---

## Updating the Application

### Update Backend Dependencies

```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Update Frontend Dependencies

```bash
cd frontend
npm update
```

### Pull Latest Changes

```bash
git pull origin main
# Then reinstall dependencies if needed
```

---

## Uninstallation

### Remove Application

```bash
# Stop running services
# Ctrl+C in terminals or:
docker-compose down

# Remove project directory
cd ..
rm -rf hirewise
```

### Clean Up Docker (if used)

```bash
# Remove images
docker rmi hirewise-backend hirewise-frontend

# Remove volumes
docker volume prune

# Remove networks
docker network prune
```

---

## Production Deployment

For production deployment, see:
- [Deployment Guide](DEPLOYMENT.md) - Coming soon
- Use PostgreSQL instead of SQLite
- Set up proper authentication
- Use environment variables for secrets
- Enable HTTPS
- Set up monitoring and logging

---

## Getting Help

### Resources

1. **Documentation**
   - [README.md](README.md) - Complete documentation
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

2. **API Documentation**
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Community**
   - GitHub Issues
   - Stack Overflow (tag: hirewise)

### Support Channels

- 📧 Email: support@hirewise.dev
- 💬 Discord: discord.gg/hirewise
- 🐛 Bug Reports: GitHub Issues

---

## Next Steps

After successful installation:

1. Read the [QUICKSTART.md](QUICKSTART.md) for usage guide
2. Try uploading the `sample_resume.txt`
3. Explore the API documentation
4. Check out the [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
5. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for demo script

---

**Happy Hiring! 🎉**

Last Updated: 2024-10-31
