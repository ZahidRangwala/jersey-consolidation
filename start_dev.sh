#!/bin/bash

# New Jersey Consolidation Analysis - Development Startup Script

echo "🏗️ Starting New Jersey Consolidation Analysis Development Environment"
echo "================================================================"

# Check if we're in the right directory
if [ ! -f "src/tiger_boundaries.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Create necessary directories
mkdir -p backend
mkdir -p frontend
mkdir -p visualizations

echo "📦 Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "🚀 Starting backend server on http://localhost:8000..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

echo "🚀 Starting frontend development server on http://localhost:3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Development environment started successfully!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
