#!/bin/bash

echo "🛑 Stopping Video Newsletter Generator..."

# Kill backend
pkill -f "uvicorn app.main:app"

# Kill frontend
pkill -f "react-scripts start"

# Kill any node processes from the frontend
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

echo "✅ All servers stopped"

