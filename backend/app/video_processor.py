import os
import subprocess
from pathlib import Path
from typing import List, Tuple
import asyncio
import whisper


class VideoProcessor:
    """Handles video processing: audio extraction, frame extraction, and transcription"""
    
    def __init__(self, video_path: Path):
        self.video_path = video_path
        self.frame_interval = int(os.getenv("FRAME_INTERVAL", 5))
        self.work_dir = video_path.parent
        
    async def extract_audio(self) -> Path:
        """Extract audio from video as WAV file"""
        audio_path = self.work_dir / f"{self.video_path.stem}_audio.wav"
        
        cmd = [
            "ffmpeg",
            "-i", str(self.video_path),
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # PCM 16-bit
            "-ar", "16000",  # 16kHz sample rate
            "-ac", "1",  # Mono
            "-y",  # Overwrite
            str(audio_path)
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg audio extraction failed: {stderr.decode()}")
        
        return audio_path
    
    async def extract_frames(self) -> List[Tuple[float, Path]]:
        """Extract frames at regular intervals"""
        frames_dir = self.work_dir / f"{self.video_path.stem}_frames"
        frames_dir.mkdir(exist_ok=True)
        
        # Extract frames at interval
        cmd = [
            "ffmpeg",
            "-i", str(self.video_path),
            "-vf", f"fps=1/{self.frame_interval}",
            "-q:v", "2",  # High quality
            "-y",
            str(frames_dir / "frame_%04d.jpg")
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg frame extraction failed: {stderr.decode()}")
        
        # Collect frame paths with timestamps
        frames = []
        for i, frame_path in enumerate(sorted(frames_dir.glob("frame_*.jpg"))):
            timestamp = i * self.frame_interval
            frames.append((timestamp, frame_path))
        
        return frames
    
    async def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio using Whisper"""
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        transcript = await loop.run_in_executor(
            None, 
            self._transcribe_sync, 
            audio_path
        )
        
        # Clean up audio file
        audio_path.unlink(missing_ok=True)
        
        return transcript
    
    def _transcribe_sync(self, audio_path: Path) -> str:
        """Synchronous transcription using Whisper"""
        # Use base model for balance of speed and accuracy
        # Options: tiny, base, small, medium, large
        model = whisper.load_model("base")
        
        result = model.transcribe(
            str(audio_path),
            language="en"
        )
        
        return result["text"].strip()

