#!/bin/bash

echo "🎥 Video Newsletter Generator - Setup Script"
echo "=============================================="
echo ""

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed!"
    echo "Please install FFmpeg first:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu: sudo apt install ffmpeg"
    exit 1
fi

echo "✅ FFmpeg is installed"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

echo "✅ Python 3 is installed"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    exit 1
fi

echo "✅ Node.js is installed"
echo ""

# Setup Backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your ANTHROPIC_API_KEY"
    echo ""
fi

cd ..

# Setup Frontend
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install --silent

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your ANTHROPIC_API_KEY"
echo "2. Run ./start.sh to start the application"
echo ""

