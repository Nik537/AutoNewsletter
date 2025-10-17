# Quick Start Guide

Get up and running in 3 minutes!

## Prerequisites Check

```bash
# Check if you have everything installed
python3 --version  # Should be 3.9+
node --version     # Should be 16+
ffmpeg -version    # Should show FFmpeg version
```

If any are missing:
- **Python**: https://www.python.org/downloads/
- **Node.js**: https://nodejs.org/
- **FFmpeg**: 
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`

## Installation

```bash
# 1. Clone or download the project
cd AutoNewsLetter

# 2. Run setup (installs dependencies)
chmod +x setup.sh start.sh stop.sh
./setup.sh

# 3. Add your Anthropic API key
# Edit backend/.env and add:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from: https://console.anthropic.com

## Run

```bash
./start.sh
```

The app will open automatically at http://localhost:3000

## Usage

1. **Upload**: Drag & drop a video file OR paste a YouTube URL
2. **Wait**: Processing takes 2-5 minutes (YouTube videos download first)
3. **Download**: Get your newsletter as a ZIP file

## Stop

```bash
./stop.sh
```

Or press `Ctrl+C`

## Troubleshooting

**"FFmpeg not found"**
```bash
brew install ffmpeg  # macOS
```

**"API key not set"**
- Make sure you edited `backend/.env` with your actual API key

**Port already in use**
```bash
./stop.sh
./start.sh
```

**Need help?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## Configuration

Edit `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-your-key    # Required
MAX_VIDEO_SIZE=524288000              # Optional: 500MB default
FRAME_INTERVAL=5                      # Optional: Extract frame every 5 seconds
```

## What It Does

1. 🎵 Extracts audio from your video
2. 📝 Transcribes the audio using Whisper AI
3. 🎬 Extracts frames from the video
4. 🤖 Uses Claude AI to:
   - Analyze frames and select key moments
   - Generate a comprehensive article in Slovenian
5. 📄 Creates a markdown file with images

## Output

You'll get a ZIP file containing:
- `newsletter.md` - The article in Slovenian
- `images/` - Selected screenshots from the video

## Example Workflow

```bash
# One-time setup
./setup.sh

# Edit backend/.env with your API key

# Start the app
./start.sh

# Use the web interface at http://localhost:3000

# When done
./stop.sh
```

That's it! 🎉

