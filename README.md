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

### Input Formats
- 🎥 **Video File Upload** - Drag-and-drop video upload interface
- 🔗 **YouTube** - Paste any YouTube link
- 💼 **LinkedIn Posts** - Import content from LinkedIn posts with videos
- 𝕏 **X (Twitter) Posts** - Import content from X/Twitter posts with videos

### Processing
- 🎙️ Audio transcription using Whisper
- 🤖 AI-powered content generation with Claude
- 🖼️ Intelligent screenshot selection (no people/faces for privacy)
- 🇸🇮 Automatic translation to Slovenian
- 🔍 AI Slovenian language teacher - proofreads and corrects the text

### Output Formats
- 📝 **Markdown** - Clean markdown format
- 🌐 **HTML** - Styled HTML for web/Notion
- 📄 **DOCX** - Microsoft Word document
- 💼 **LinkedIn Post** - AI-optimized post (3000 char limit, engagement-focused)
- 𝕏 **X Thread** - AI-generated thread (280 char tweets, 5-10 tweets)

### Other Features
- 📊 Real-time progress tracking
- 💾 One-click download - choose your format

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

### Input Options

1. Open http://localhost:3000 in your browser
2. Choose your input format:
   - **Upload File**: Drag and drop a video file (or click to select)
   - **YouTube**: Paste a YouTube video URL
   - **LinkedIn**: Paste a LinkedIn post URL (with video content)
   - **X/Twitter**: Paste an X/Twitter post URL (with video content)

### Processing

3. Wait for the processing to complete (progress updates in real-time)
4. Preview the generated newsletter

### Download Options

5. Choose your preferred output format:
   - **Newsletter Formats**: Download as Word (DOCX), HTML (for Notion), or Markdown
   - **Social Media Formats**: Download LinkedIn post or X thread (as JSON files)

### Social Media Post Usage

- **LinkedIn Post**: Open the downloaded JSON file and copy the "text" field directly into LinkedIn
- **X Thread**: Open the downloaded JSON file and post each tweet in the "tweets" array sequentially

### API Notes

Currently, LinkedIn and X post downloads require API access:
- For production use, implement LinkedIn API authentication
- For X posts, obtain X API v2 bearer token
- See the downloader modules for integration details

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Project Structure

```
AutoNewsLetter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI server & API endpoints
│   │   ├── video_processor.py   # Video extraction logic
│   │   ├── ai_service.py        # Claude API integration
│   │   ├── newsletter_generator.py  # Newsletter generation
│   │   ├── export_formatter.py  # Multi-format exports (MD, HTML, DOCX, LinkedIn, X)
│   │   ├── youtube_downloader.py    # YouTube video downloader
│   │   ├── linkedin_downloader.py   # LinkedIn content downloader
│   │   └── x_downloader.py          # X/Twitter content downloader
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoUploader.jsx     # Multi-source upload UI
│   │   │   ├── ProgressTracker.jsx
│   │   │   └── NewsletterPreview.jsx # Multi-format download UI
│   │   └── App.js
│   └── package.json
├── setup.sh                 # Automated setup script
├── start.sh                 # Start application
├── stop.sh                  # Stop application
├── README.md
├── GET_STARTED.md
└── DEPLOYMENT.md
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

## New Features (Latest Update)

### Multiple Input Formats
- Added LinkedIn post support for importing content
- Added X (Twitter) post support for importing content
- Maintained existing YouTube and file upload support

### Social Media Export Formats
- LinkedIn Post generator with AI optimization (character limits, hashtags, engagement focus)
- X Thread generator creating 5-10 tweet threads with proper formatting
- Both exports use Claude AI to adapt newsletter content for each platform

### Implementation Notes

**LinkedIn & X Input (Placeholder Implementation)**:
The LinkedIn and X downloaders are implemented with placeholder logic. For production use, you'll need to:

1. **LinkedIn Integration**:
   - Register a LinkedIn Developer app
   - Implement OAuth 2.0 authentication
   - Use LinkedIn Marketing Developer Platform API
   - Or use third-party services like PhantomBuster or Apify

2. **X (Twitter) Integration**:
   - Register for X API v2 access
   - Obtain API keys and bearer token
   - Implement tweet retrieval endpoints
   - Or use alternative services like Nitter

**Social Media Output (Fully Functional)**:
The LinkedIn and X output generators are fully functional and use Claude AI to:
- Transform newsletter content into platform-optimized posts
- Handle character limits (LinkedIn: 3000, X: 280 per tweet)
- Add relevant hashtags
- Create engaging hooks and calls-to-action
- Maintain the original content's language (Slovenian/English)

## Roadmap

Potential future enhancements:

- [x] Multiple input formats (YouTube, LinkedIn, X)
- [x] Social media export formats (LinkedIn, X)
- [ ] Full LinkedIn API integration with OAuth
- [ ] Full X API integration with bearer token support
- [ ] Support for multiple output languages
- [ ] Batch processing of multiple videos
- [ ] Custom article templates
- [ ] Video trimming in the UI
- [ ] Integration with email services
- [ ] User authentication and history
- [ ] Database storage for jobs
- [ ] Docker deployment

## Contributing

This is a demo project. Feel free to fork and customize for your needs!

## License

MIT

