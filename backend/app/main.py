import os
import uuid
import shutil
from pathlib import Path
from typing import Dict, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

from app.video_processor import VideoProcessor
from app.ai_service import AIService
from app.newsletter_generator import NewsletterGenerator
from app.youtube_downloader import YouTubeDownloader

load_dotenv()

app = FastAPI(title="Video Newsletter Generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 524288000))  # 500MB default

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files for serving images
app.mount("/output", StaticFiles(directory="output"), name="output")

# Job storage (in production, use a database)
jobs: Dict[str, dict] = {}


class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    error: Optional[str] = None
    result_path: Optional[str] = None


class YouTubeUpload(BaseModel):
    url: str


async def process_video_task(job_id: str, video_path: Path):
    """Background task to process video"""
    try:
        # Update status
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Extracting audio and frames..."
        
        # Initialize processors
        video_processor = VideoProcessor(video_path)
        ai_service = AIService()
        newsletter_gen = NewsletterGenerator()
        
        # Step 1: Extract audio and frames
        audio_path = await video_processor.extract_audio()
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Audio extracted, extracting frames..."
        
        frames = await video_processor.extract_frames()
        jobs[job_id]["progress"] = 30
        jobs[job_id]["message"] = f"Extracted {len(frames)} frames, transcribing audio..."
        
        # Step 2: Transcribe audio
        transcript = await video_processor.transcribe_audio(audio_path)
        jobs[job_id]["progress"] = 50
        jobs[job_id]["message"] = "Transcription complete, analyzing frames with AI..."
        
        # Step 3: Analyze frames and select key moments
        key_frames = await ai_service.select_key_frames(frames, transcript)
        jobs[job_id]["progress"] = 70
        jobs[job_id]["message"] = f"Selected {len(key_frames)} key frames, generating newsletter..."
        
        # Step 4: Generate newsletter
        output_path = OUTPUT_DIR / job_id
        output_path.mkdir(exist_ok=True)
        
        jobs[job_id]["progress"] = 75
        jobs[job_id]["message"] = "Generating Slovenian article..."
        
        newsletter_path = await newsletter_gen.generate(
            transcript=transcript,
            key_frames=key_frames,
            output_dir=output_path,
            ai_service=ai_service
        )
        
        jobs[job_id]["progress"] = 95
        jobs[job_id]["message"] = "Proofreading completed, finalizing..."
        
        jobs[job_id]["progress"] = 100
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Newsletter generated successfully!"
        jobs[job_id]["result_path"] = str(newsletter_path)
        
        # Cleanup uploaded video
        video_path.unlink(missing_ok=True)
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Error: {str(e)}"
        print(f"Error processing video {job_id}: {e}")


@app.get("/")
async def root():
    return {"message": "Video Newsletter Generator API", "status": "running"}


@app.post("/api/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload a video file and start processing"""
    
    # Validate file
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(400, "File must be a video")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    video_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    
    try:
        with video_path.open("wb") as buffer:
            content = await file.read()
            if len(content) > MAX_VIDEO_SIZE:
                raise HTTPException(400, f"Video size exceeds maximum ({MAX_VIDEO_SIZE} bytes)")
            buffer.write(content)
    except Exception as e:
        raise HTTPException(500, f"Failed to save video: {str(e)}")
    
    # Initialize job
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Video uploaded, starting processing...",
        "filename": file.filename
    }
    
    # Start background processing
    background_tasks.add_task(process_video_task, job_id, video_path)
    
    return {"job_id": job_id, "message": "Video uploaded successfully"}


@app.post("/api/upload-youtube")
async def upload_youtube(
    background_tasks: BackgroundTasks,
    data: YouTubeUpload
):
    """Upload a video from YouTube URL and start processing"""
    
    # Validate URL
    if not YouTubeDownloader.validate_url(data.url):
        raise HTTPException(400, "Invalid YouTube URL")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Downloading video from YouTube...",
        "url": data.url
    }
    
    # Start background processing with YouTube download
    background_tasks.add_task(process_youtube_task, job_id, data.url)
    
    return {"job_id": job_id, "message": "YouTube video download started"}


async def process_youtube_task(job_id: str, youtube_url: str):
    """Background task to download and process YouTube video"""
    try:
        # Update status
        jobs[job_id]["status"] = "downloading"
        jobs[job_id]["progress"] = 5
        jobs[job_id]["message"] = "Downloading video from YouTube..."
        
        # Download video
        downloader = YouTubeDownloader(UPLOAD_DIR)
        video_path = downloader.download(youtube_url, job_id)
        
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Video downloaded, starting processing..."
        
        # Continue with normal video processing
        await process_video_task(job_id, video_path)
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Error downloading video: {str(e)}"
        print(f"Error processing YouTube video {job_id}: {e}")


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status for a job"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    return jobs[job_id]


@app.get("/api/preview/{job_id}")
async def preview_newsletter(job_id: str):
    """Get the markdown content for preview"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(400, "Job not completed yet")
    
    result_path = Path(job["result_path"])
    if not result_path.exists():
        raise HTTPException(404, "Newsletter file not found")
    
    content = result_path.read_text(encoding="utf-8")
    return {"content": content, "job_id": job_id}


@app.get("/api/download/{job_id}")
async def download_newsletter(job_id: str):
    """Download the generated newsletter as a zip file"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(400, "Job not completed yet")
    
    # Create zip file
    output_dir = OUTPUT_DIR / job_id
    if not output_dir.exists():
        raise HTTPException(404, "Output directory not found")
    
    zip_path = OUTPUT_DIR / f"{job_id}_newsletter"
    shutil.make_archive(str(zip_path), "zip", output_dir)
    
    return FileResponse(
        f"{zip_path}.zip",
        media_type="application/zip",
        filename=f"newsletter_{job_id}.zip"
    )


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its associated files"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    # Delete output directory
    output_dir = OUTPUT_DIR / job_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # Delete uploaded video if still exists
    for video_file in UPLOAD_DIR.glob(f"{job_id}_*"):
        video_file.unlink(missing_ok=True)
    
    # Remove from jobs
    del jobs[job_id]
    
    return {"message": "Job deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

