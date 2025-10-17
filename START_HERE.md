# 🎬 START HERE - Video Newsletter Generator

## Welcome! 👋

You now have a complete, production-ready application that converts English videos into Slovenian newsletter articles using AI.

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Install Prerequisites

You need these three things installed:

```bash
# Check what you have:
python3 --version    # Need 3.9+
node --version       # Need 16+
ffmpeg -version      # Need any version
```

**Don't have them?**
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- FFmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Ubuntu)

### 2️⃣ Get API Key

1. Visit https://console.anthropic.com
2. Sign up/login
3. Create API key
4. Copy it (starts with `sk-ant-`)

### 3️⃣ Setup

```bash
cd AutoNewsLetter
./setup.sh
```

### 4️⃣ Configure

Edit `backend/.env` and paste your API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5️⃣ Launch

```bash
./start.sh
```

Visit http://localhost:3000 🚀

## 🎯 How It Works

1. **Drag** a video file into the interface
2. **Wait** 2-5 minutes while AI processes it
3. **Preview** the generated Slovenian article
4. **Download** ZIP with markdown + images

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[GET_STARTED.md](GET_STARTED.md)** | Complete setup guide | First time setup |
| **[QUICK_START.md](QUICK_START.md)** | 3-minute quickstart | Experienced devs |
| **[README.md](README.md)** | Full documentation | Anytime |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Troubleshooting | Having issues |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Technical details | Understanding code |
| **[TESTING.md](TESTING.md)** | Testing guide | Debugging |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Overview | Big picture |
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Navigation | Lost? Start here |

## ✨ What You Get

✅ **Full-Stack Application**
- Modern React frontend
- FastAPI backend
- Real-time updates

✅ **AI-Powered Processing**
- Claude Haiku 4.5 (content)
- Whisper (transcription)
- Vision AI (frame analysis)

✅ **Professional Output**
- Slovenian newsletter articles
- AI-selected screenshots
- Markdown format
- Ready to publish

✅ **Great Developer Experience**
- One-command setup
- Automated scripts
- Comprehensive docs
- Error handling

## 🎓 Next Steps

**First Time?**
1. Read [GET_STARTED.md](GET_STARTED.md) (10 min)
2. Follow the setup steps
3. Try with a short video
4. Explore the features

**Experienced Developer?**
1. Skim [QUICK_START.md](QUICK_START.md) (3 min)
2. Run setup and configure
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for details

**Having Issues?**
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Look at [TESTING.md](TESTING.md)
3. Review backend.log

## 🔧 Common Issues

**"FFmpeg not found"**
```bash
brew install ffmpeg  # macOS
```

**"API key not set"**
- Edit `backend/.env`
- Add `ANTHROPIC_API_KEY=sk-ant-...`
- Restart: `./stop.sh && ./start.sh`

**"Port in use"**
```bash
./stop.sh
./start.sh
```

## 💡 Pro Tips

- Start with short videos (2-5 minutes)
- Good audio quality = better transcription
- Visual content = better screenshots
- Check backend.log if issues occur

## 🚀 You're Ready!

Everything is set up and ready to use. Just:

1. Get your API key
2. Run `./setup.sh`
3. Edit `backend/.env`
4. Run `./start.sh`
5. Start creating newsletters!

## 📞 Need Help?

- **Setup**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Usage**: [GET_STARTED.md](GET_STARTED.md)
- **API**: http://localhost:8000/docs (when running)
- **Errors**: [TESTING.md](TESTING.md)

---

**Let's get started!** Open [GET_STARTED.md](GET_STARTED.md) for detailed instructions.

Built with ❤️ using AI • October 17, 2025

