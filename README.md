# Video Newsletter Generator

A complete web application that converts English videos into Slovenian newsletter articles with AI-selected screenshots.

## ⚡ Quick Start

```bash
./setup.sh                    # Install dependencies
# Edit backend/.env with your ANTHROPIC_API_KEY
./start.sh                    # Launch application
# Visit http://localhost:3000
```

See [GET_STARTED.md](GET_STARTED.md) for the complete guide.

## ✨ Features

- 🎥 Drag-and-drop video upload interface
- 🔗 YouTube URL support - paste any YouTube link
- 🎙️ Audio transcription using Whisper
- 🤖 AI-powered content generation with Claude
- 🖼️ Intelligent screenshot selection (no people/faces for privacy)
- 🇸🇮 Automatic translation to Slovenian
- 🔍 AI Slovenian language teacher - proofreads and corrects the text
- 📝 Markdown output with embedded images
- 📊 Real-time progress tracking
- 💾 One-click download as ZIP

## Tech Stack

- **Frontend:** React with react-dropzone
- **Backend:** FastAPI (Python)
- **Video Processing:** FFmpeg
- **Audio Transcription:** Faster Whisper
- **AI:** Anthropic Claude Haiku 4.5

## Prerequisites

- Python 3.9+
- Node.js 16+
- FFmpeg installed on your system

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

From the `backend` directory:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### Start the Frontend

From the `frontend` directory:
```bash
npm start
```

The web app will open at http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Drag and drop a video file (or click to select)
3. Wait for the processing to complete (progress updates in real-time)
4. Preview the generated newsletter
5. Download the markdown file with images

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Project Structure

```
AutoNewsLetter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI server
│   │   ├── video_processor.py   # Video extraction logic
│   │   ├── ai_service.py        # Claude API integration
│   │   └── newsletter_generator.py  # Markdown generation
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoUploader.jsx
│   │   │   ├── ProgressTracker.jsx
│   │   │   └── NewsletterPreview.jsx
│   │   └── App.js
│   └── package.json
├── setup.sh                 # Automated setup script
├── start.sh                 # Start application
├── stop.sh                  # Stop application
├── README.md
├── QUICK_START.md
└── SETUP_GUIDE.md
```

## Configuration

Edit `.env` in the backend directory:

- `ANTHROPIC_API_KEY` - Your Claude API key (required)
- `MAX_VIDEO_SIZE` - Maximum upload size in bytes (default: 500MB)
- `FRAME_INTERVAL` - Seconds between frame extractions (default: 5)

## Additional Documentation

- [QUICK_START.md](QUICK_START.md) - Get started in 3 minutes
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- [TESTING.md](TESTING.md) - Testing and error handling guide

## Features Overview

### What Makes This Special

- **Multilingual**: Accepts English videos, outputs Slovenian articles
- **AI-Powered**: Uses Claude Haiku 4.5 for intelligent content generation
- **Smart Screenshots**: Automatically selects the most relevant frames (excludes people for privacy)
- **Professional Output**: Well-structured markdown suitable for newsletters
- **Easy to Use**: Simple drag-and-drop interface
- **Customizable**: Configurable frame extraction and article length

### Technical Highlights

- Asynchronous processing with real-time progress updates
- Automatic cleanup of temporary files
- Comprehensive error handling
- Static file serving for image preview
- RESTful API with interactive documentation
- Responsive modern UI with smooth animations

## Roadmap

Potential future enhancements:

- [ ] Support for multiple output languages
- [ ] Batch processing of multiple videos
- [ ] Custom article templates
- [ ] Video trimming in the UI
- [ ] Export to HTML/PDF formats
- [ ] Integration with email services
- [ ] User authentication and history
- [ ] Database storage for jobs
- [ ] Docker deployment

## Contributing

This is a demo project. Feel free to fork and customize for your needs!

## License

MIT

