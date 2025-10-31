#!/bin/bash

# HireWise Quick Start Script

echo "?? Starting HireWise - AI Recruiting Assistant"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "? Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "? Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "? Prerequisites check passed"
echo ""

# Start backend
echo "?? Starting Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "?? Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

cd ..
echo "? Backend dependencies installed"
echo "?? Starting FastAPI server on http://localhost:8000"
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo ""
echo "?? Starting Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "?? Installing frontend dependencies..."
    npm install
fi

echo "? Frontend dependencies installed"
echo "?? Starting Vite dev server on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=============================================="
echo "? HireWise is now running!"
echo "=============================================="
echo "?? Frontend: http://localhost:3000"
echo "?? Backend:  http://localhost:8000"
echo "?? API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=============================================="

# Wait for Ctrl+C
trap "echo ''; echo '?? Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
