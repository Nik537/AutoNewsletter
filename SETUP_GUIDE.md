# Setup Guide - Video Newsletter Generator

## Quick Start

### 1. Prerequisites

Make sure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **FFmpeg** - Required for video processing
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html)

### 2. Get Your API Key

1. Sign up for an Anthropic account at [console.anthropic.com](https://console.anthropic.com)
2. Create an API key
3. Save it - you'll need it in the next step

### 3. Run Setup

```bash
# Make scripts executable
chmod +x setup.sh start.sh stop.sh

# Run setup
./setup.sh
```

### 4. Configure API Key

Edit the file `backend/.env` and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MAX_VIDEO_SIZE=524288000
FRAME_INTERVAL=5
```

### 5. Start the Application

```bash
./start.sh
```

The application will automatically open in your browser at http://localhost:3000

## Manual Setup (Alternative)

If the automated scripts don't work, you can set up manually:

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## Usage

1. Open http://localhost:3000 in your browser
2. Drag and drop a video file (or click to select)
3. Wait for processing (typically 2-5 minutes depending on video length)
4. Preview the generated newsletter
5. Download the markdown file with images as a ZIP

## Troubleshooting

### FFmpeg not found

**Error:** `FFmpeg audio extraction failed`

**Solution:** Install FFmpeg:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`
- Windows: Download from ffmpeg.org and add to PATH

### API Key Error

**Error:** `ANTHROPIC_API_KEY environment variable not set`

**Solution:** 
1. Check that `backend/.env` exists
2. Verify the API key is correctly set: `ANTHROPIC_API_KEY=sk-ant-...`
3. Restart the backend server

### Port Already in Use

**Error:** `Port 8000 is already in use`

**Solution:**
```bash
# Find and kill the process using the port
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Video Upload Fails

**Error:** `Video size exceeds maximum`

**Solution:** Edit `backend/.env` and increase `MAX_VIDEO_SIZE`:
```
MAX_VIDEO_SIZE=1048576000  # 1GB
```

### Frontend Can't Connect to Backend

**Error:** Network errors in browser console

**Solution:**
1. Verify backend is running: `curl http://localhost:8000`
2. Check `backend.log` for errors
3. Ensure CORS is configured (already done in code)

## Configuration

### Environment Variables (backend/.env)

- `ANTHROPIC_API_KEY` - Your Claude API key (required)
- `MAX_VIDEO_SIZE` - Maximum upload size in bytes (default: 500MB)
- `FRAME_INTERVAL` - Seconds between frame extractions (default: 5)

### Performance Tuning

**For faster processing:**
- Increase `FRAME_INTERVAL` to 10 (extracts fewer frames)
- Use shorter videos for testing

**For better quality:**
- Decrease `FRAME_INTERVAL` to 3 (extracts more frames)
- Edit `video_processor.py` to use larger Whisper model

## Project Structure

```
AutoNewsLetter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI server
│   │   ├── video_processor.py   # Video/audio processing
│   │   ├── ai_service.py        # Claude API integration
│   │   └── newsletter_generator.py  # Markdown generation
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoUploader.jsx
│   │   │   ├── ProgressTracker.jsx
│   │   │   └── NewsletterPreview.jsx
│   │   └── App.js
│   └── package.json
├── setup.sh
├── start.sh
└── stop.sh
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Support

For issues, check:
1. `backend.log` for backend errors
2. Browser console for frontend errors
3. Ensure all prerequisites are installed
4. Verify API key is valid and has credits

## Stopping the Application

```bash
./stop.sh
```

Or press `Ctrl+C` in the terminal running the servers.

