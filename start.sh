#!/bin/bash

echo "🎥 Video Newsletter Generator - Starting Application"
echo "====================================================="
echo ""

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env not found!"
    echo "Please run ./setup.sh first and configure your API key"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" backend/.env 2>/dev/null; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY may not be configured in backend/.env"
    echo "Make sure to add your API key before processing videos"
    echo ""
fi

# Create directories if they don't exist
mkdir -p backend/uploads
mkdir -p backend/output

# Start backend in background
echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ Backend failed to start. Check backend.log for errors"
    exit 1
fi

echo "✅ Backend running on http://localhost:8000"

# Start frontend
echo "🚀 Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Application is starting!"
echo ""
echo "📝 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend: backend.log"
echo ""
echo "To stop the application, press Ctrl+C or run ./stop.sh"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Kill any remaining processes
    pkill -f "uvicorn app.main:app" 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait

