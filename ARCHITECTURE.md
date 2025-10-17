# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    http://localhost:3000                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ HTTP/REST
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                    REACT FRONTEND                                │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │VideoUploader│  │ProgressTracker│ │NewsletterPreview │       │
│  └─────────────┘  └──────────────┘  └──────────────────┘       │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Axios HTTP Requests
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                  FASTAPI BACKEND                                 │
│                 http://localhost:8000                            │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                  API Routes                           │       │
│  │  POST /api/upload        GET /api/status              │       │
│  │  GET  /api/preview       GET /api/download            │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │            Background Job Processor                   │       │
│  │  • Job Queue Management                              │       │
│  │  • Progress Tracking                                 │       │
│  │  • Error Handling                                    │       │
│  └──────────────────────────────────────────────────────┘       │
└──────────┬───────────────┬────────────────┬────────────────────┘
           │               │                │
    ┌──────▼──────┐ ┌─────▼──────┐  ┌─────▼──────┐
    │VideoProcessor│ │ AIService  │  │NewsletterGen│
    └──────┬───────┘ └─────┬──────┘  └─────┬──────┘
           │               │                │
    ┌──────▼──────┐ ┌─────▼──────┐  ┌─────▼──────┐
    │   FFmpeg    │ │Claude API  │  │  Markdown  │
    │   Whisper   │ │ Vision API │  │  Generator │
    └─────────────┘ └────────────┘  └────────────┘
```

## Data Flow

### 1. Upload Phase

```
User selects video
    ↓
VideoUploader.jsx validates file
    ↓
POST /api/upload
    ↓
main.py saves to uploads/
    ↓
Creates job entry
    ↓
Starts background task
    ↓
Returns job_id to frontend
```

### 2. Processing Phase

```
Background Task Starts
    ↓
┌─────────────────────────────────────┐
│ video_processor.py                  │
│  1. Extract audio (FFmpeg)          │
│     video.mp4 → audio.wav           │
│                                     │
│  2. Extract frames (FFmpeg)         │
│     video.mp4 → frame_0001.jpg...   │
│                                     │
│  3. Transcribe audio (Whisper)      │
│     audio.wav → English text        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ ai_service.py                       │
│  4. Analyze frames (Claude Vision)  │
│     All frames → Key moments        │
│                                     │
│  5. Generate article (Claude)       │
│     Transcript + Frames → Slovenian │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ newsletter_generator.py             │
│  6. Create markdown file            │
│  7. Copy selected images            │
│  8. Package output                  │
└─────────────────────────────────────┘
```

### 3. Progress Updates

```
Frontend polls GET /api/status/{job_id} every 2 seconds
    ↓
Backend returns:
{
  "status": "processing",
  "progress": 45,
  "message": "Analyzing frames..."
}
    ↓
ProgressTracker.jsx updates UI
```

### 4. Completion & Download

```
Processing completes
    ↓
Status → "completed"
    ↓
Frontend fetches GET /api/preview/{job_id}
    ↓
NewsletterPreview.jsx displays markdown
    ↓
User clicks download
    ↓
GET /api/download/{job_id}
    ↓
Backend creates ZIP
    ↓
Browser downloads newsletter_{job_id}.zip
```

## Component Responsibilities

### Frontend Components

#### **VideoUploader.jsx**
- Drag-and-drop interface
- File validation (type, size)
- Upload to backend
- Error display

#### **ProgressTracker.jsx**
- Poll job status
- Display progress bar
- Show current stage
- Handle errors

#### **NewsletterPreview.jsx**
- Render markdown content
- Display images from backend
- Download button
- Reset to upload new video

### Backend Modules

#### **main.py** (FastAPI Server)
- HTTP request handling
- Job management
- Background task orchestration
- Static file serving
- CORS configuration

#### **video_processor.py**
- FFmpeg audio extraction
- FFmpeg frame extraction
- Whisper transcription
- File cleanup

#### **ai_service.py**
- Claude API integration
- Frame analysis with vision
- Key moment selection
- Slovenian article generation

#### **newsletter_generator.py**
- Markdown file creation
- Image organization
- Caption formatting
- Asset packaging

## File Organization

### Runtime Directories

```
AutoNewsLetter/
├── backend/
│   ├── uploads/              [Created at runtime]
│   │   └── {job_id}_{filename}.mp4
│   │
│   └── output/               [Created at runtime]
│       └── {job_id}/
│           ├── newsletter.md
│           └── images/
│               ├── frame_1.jpg
│               ├── frame_2.jpg
│               └── ...
│
└── frontend/
    └── build/                [Created by npm run build]
```

### Job Lifecycle

```
1. Upload:
   uploads/{job_id}_video.mp4
   uploads/{job_id}_audio.wav
   uploads/{job_id}_frames/frame_*.jpg

2. Processing:
   • Audio and frames extracted
   • Transcription generated (in memory)
   • AI analysis (API calls)

3. Output:
   output/{job_id}/newsletter.md
   output/{job_id}/images/frame_*.jpg

4. Cleanup:
   • Delete uploads/{job_id}_*
   • Keep output/{job_id}/ for download
```

## API Contract

### Request/Response Formats

#### Upload Video
```http
POST /api/upload
Content-Type: multipart/form-data

file: [video file]

Response:
{
  "job_id": "uuid",
  "message": "Video uploaded successfully"
}
```

#### Check Status
```http
GET /api/status/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "processing",  // queued|processing|completed|failed
  "progress": 45,          // 0-100
  "message": "Analyzing frames...",
  "error": null            // or error message if failed
}
```

#### Preview Newsletter
```http
GET /api/preview/{job_id}

Response:
{
  "content": "# Newsletter Title\n\n...",
  "job_id": "uuid"
}
```

#### Download
```http
GET /api/download/{job_id}

Response: application/zip
  newsletter_{job_id}.zip containing:
    - newsletter.md
    - images/frame_*.jpg
```

## Technology Choices

### Why FastAPI?
- Modern async Python framework
- Automatic API documentation
- Type validation with Pydantic
- Easy background tasks
- Fast development

### Why React?
- Component-based architecture
- Rich ecosystem (dropzone, markdown)
- Virtual DOM for efficient updates
- Great developer experience

### Why Claude?
- State-of-the-art vision capabilities
- Excellent multilingual support
- High-quality content generation
- Good API documentation

### Why Whisper?
- Best-in-class transcription accuracy
- Free and open source
- Multiple model sizes
- Good English support

### Why FFmpeg?
- Industry standard for video processing
- Powerful and flexible
- Wide format support
- Command-line interface

## Configuration Flow

```
Environment Variables (.env)
    ↓
python-dotenv loads at startup
    ↓
os.getenv() in Python modules
    ↓
Used throughout application
```

### Key Configuration Points

```python
# Backend (main.py)
MAX_VIDEO_SIZE = os.getenv("MAX_VIDEO_SIZE", 524288000)
FRAME_INTERVAL = os.getenv("FRAME_INTERVAL", 5)

# AI Service (ai_service.py)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
model = "claude-haiku-4-5-20251001"

# Video Processor (video_processor.py)
whisper_model = WhisperModel("base", ...)
```

## Error Handling Strategy

### Validation Layer
```
Frontend validation
    ↓
Backend validation
    ↓
Process with try/except
    ↓
Return user-friendly errors
```

### Error Propagation
```
Low-level error (FFmpeg, API)
    ↓
Caught in module (video_processor, ai_service)
    ↓
Exception with context
    ↓
Background task catches
    ↓
Updates job status to "failed"
    ↓
Frontend displays error
```

## Performance Considerations

### Bottlenecks
1. **Video Processing** - CPU intensive (FFmpeg)
2. **Transcription** - CPU intensive (Whisper)
3. **AI Calls** - Network latency (Claude API)

### Optimizations
1. **Async Processing** - Background tasks don't block uploads
2. **Frame Sampling** - Don't analyze every frame
3. **Efficient Models** - Whisper "base" balances speed/accuracy
4. **Cleanup** - Remove temporary files immediately

### Scalability Path
```
Current: In-memory job queue
    ↓
Next: Redis + Celery
    ↓
Then: Multiple workers
    ↓
Finally: Kubernetes cluster
```

## Security Considerations

### Implemented
✅ File type validation
✅ File size limits
✅ CORS configuration
✅ API key in environment (not code)
✅ Path traversal prevention

### For Production
- Rate limiting
- Authentication/Authorization
- Input sanitization
- HTTPS enforcement
- API key rotation
- Audit logging

## Deployment Architecture

### Development (Current)
```
localhost:3000 (React dev server)
    ↓
localhost:8000 (FastAPI with uvicorn)
```

### Production (Recommended)
```
nginx (reverse proxy, SSL)
    ↓
├─→ React build (static files)
└─→ FastAPI (gunicorn + uvicorn workers)
    ↓
    Redis (job queue)
    ↓
    Celery workers
```

## Monitoring Points

### Health Checks
- GET / → API health
- Disk space (uploads/, output/)
- API key validity
- FFmpeg availability

### Metrics to Track
- Upload success rate
- Processing time per video
- Error rates by type
- API costs (Claude API usage)
- Storage usage

### Logging
- Backend: print() → stdout → backend.log
- Frontend: console.log() → browser console
- Production: Structured logging (JSON)

## Summary

This architecture provides:

✅ **Separation of Concerns** - Clear module boundaries
✅ **Scalability** - Can evolve from simple to complex
✅ **Maintainability** - Well-organized, documented code
✅ **Reliability** - Comprehensive error handling
✅ **Performance** - Async processing, efficient algorithms
✅ **Security** - Input validation, safe file handling

The design supports both current needs and future growth.

