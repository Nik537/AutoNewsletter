# 🎥 Get Started with Video Newsletter Generator

Welcome! This guide will get you up and running in just a few minutes.

## What You're About to Use

A powerful AI tool that:
- Takes English videos 🎬
- Generates Slovenian newsletter articles 📝
- Automatically selects the best screenshots 📸
- Outputs professional markdown with images 📄

## Prerequisites (5 minutes)

### 1. Install Required Software

**Python 3.9+**
```bash
python3 --version
# If not installed: https://www.python.org/downloads/
```

**Node.js 16+**
```bash
node --version
# If not installed: https://nodejs.org/
```

**FFmpeg** (for video processing)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### 2. Get Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Create an API key
4. Copy it (starts with `sk-ant-...`)

## Installation (2 minutes)

```bash
# Navigate to the project
cd AutoNewsLetter

# Make scripts executable
chmod +x setup.sh start.sh stop.sh

# Run setup
./setup.sh
```

## Configuration (1 minute)

Edit `backend/.env` and add your API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
MAX_VIDEO_SIZE=524288000
FRAME_INTERVAL=5
```

## Launch (30 seconds)

```bash
./start.sh
```

The app will automatically open at http://localhost:3000

## Using the Application

### Step 1: Upload Video
- Drag and drop a video file
- Or click to select
- Supported: MP4, MOV, AVI, MKV, WebM

### Step 2: Wait for Processing
- Watch real-time progress updates
- Typically takes 2-5 minutes
- Stages:
  1. 📤 Uploading
  2. 🎵 Extracting audio
  3. 🎬 Extracting frames
  4. 🤖 AI analysis
  5. 📝 Generating newsletter

### Step 3: Preview & Download
- Preview the article in Slovenian
- Check the selected screenshots
- Download ZIP file containing:
  - `newsletter.md` - Article in markdown
  - `images/` - Selected screenshots

### Step 4: Use Your Newsletter
- Open newsletter.md in any markdown editor
- Images are referenced relatively
- Perfect for publishing or emailing

## Example Output

For a 5-minute tech talk video, you'll get:

```markdown
# [Generated Title in Slovenian]

[Introduction paragraph...]

![Screenshot description](images/frame_1.jpg)
*Caption in Slovenian*

[Content sections...]

![Another key moment](images/frame_2.jpg)
*Another caption*

[More content...]
```

## Troubleshooting

### "FFmpeg not found"
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu
```

### "API key not set"
- Make sure you edited `backend/.env`
- Check the key starts with `sk-ant-`
- Restart the server: `./stop.sh && ./start.sh`

### "Port already in use"
```bash
./stop.sh
./start.sh
```

### Processing takes too long
- Longer videos take more time (10-15 min for 20+ min video)
- This is normal - AI analysis takes time
- You can reduce `FRAME_INTERVAL` for faster processing

## Tips for Best Results

### Video Selection
✅ Clear audio (good microphone)
✅ Visual content (not just talking head)
✅ 2-10 minutes is optimal
✅ English language

### Quality Settings
- Default settings work well for most videos
- Adjust `FRAME_INTERVAL` in `.env`:
  - `3` = More screenshots, slower
  - `5` = Balanced (default)
  - `10` = Fewer screenshots, faster

## What's Next?

### Explore More
- 📚 [README.md](README.md) - Full documentation
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
- 🔧 [TESTING.md](TESTING.md) - Testing guide

### Customize
- Edit prompts in `backend/app/ai_service.py`
- Adjust styling in `frontend/src/`
- Configure video processing in `backend/app/video_processor.py`

### Get Help
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed help
- Visit http://localhost:8000/docs for API documentation
- Review [TESTING.md](TESTING.md) for common issues

## Stopping the Application

```bash
./stop.sh
```

Or press `Ctrl+C` in the terminal.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./setup.sh` | Install dependencies |
| `./start.sh` | Start the application |
| `./stop.sh` | Stop the application |
| http://localhost:3000 | Web interface |
| http://localhost:8000/docs | API documentation |

## Project Structure

```
AutoNewsLetter/
├── backend/        # Python FastAPI server
├── frontend/       # React web application
├── setup.sh        # Setup script
├── start.sh        # Start script
├── stop.sh         # Stop script
└── [docs]         # Documentation files
```

## File Locations

| Type | Location |
|------|----------|
| Configuration | `backend/.env` |
| Uploaded videos | `backend/uploads/` |
| Generated newsletters | `backend/output/` |
| Logs | `backend.log` |

## Support

Need help? Check these resources:

1. **Quick Questions**: [QUICK_START.md](QUICK_START.md)
2. **Setup Issues**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. **How It Works**: [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Testing & Debugging**: [TESTING.md](TESTING.md)
5. **Complete Overview**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## Success!

If you can see the drag-and-drop interface at http://localhost:3000, you're all set! 🎉

Try uploading a short video to see the magic happen.

---

**Built with:** Claude AI, Whisper, React, and FastAPI
**Processing Time:** ~2-5 minutes per video
**Output:** Professional Slovenian newsletter articles

