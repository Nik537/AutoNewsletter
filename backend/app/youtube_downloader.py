import os
from pathlib import Path
from typing import Optional
import yt_dlp


class YouTubeDownloader:
    """Handles downloading videos from YouTube URLs"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def download(self, url: str, job_id: str) -> Path:
        """
        Download video from YouTube URL

        Args:
            url: YouTube video URL
            job_id: Unique job identifier for filename

        Returns:
            Path to downloaded video file
        """
        output_template = str(self.output_dir / f"{job_id}_%(title)s.%(ext)s")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': False,
            'merge_output_format': 'mp4',
            # Add headers to bypass 403 errors
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            # Use alternative player clients to avoid 403 errors - prioritize android_creator
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator', 'android', 'ios', 'web'],
                    'player_skip': ['webpage', 'configs'],
                    'skip': ['hls', 'dash'],
                }
            },
            # Add retry options
            'retries': 10,
            'fragment_retries': 10,
            # Add geo bypass
            'geo_bypass': True,
            # Force IPv4 to avoid IPv6 issues
            'source_address': '0.0.0.0',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video')
                
                # Download the video
                ydl.download([url])
                
                # Find the downloaded file
                # yt-dlp sanitizes the title, so we need to find the actual file
                downloaded_files = list(self.output_dir.glob(f"{job_id}_*"))
                
                if not downloaded_files:
                    raise FileNotFoundError("Downloaded video file not found")
                
                # Return the first matching file (should be only one)
                return downloaded_files[0]
                
        except Exception as e:
            raise Exception(f"Failed to download YouTube video: {str(e)}")
    
    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        youtube_domains = [
            'youtube.com',
            'youtu.be',
            'www.youtube.com',
            'm.youtube.com'
        ]
        return any(domain in url.lower() for domain in youtube_domains)
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate YouTube URL format"""
        if not YouTubeDownloader.is_youtube_url(url):
            return False
        
        # Basic URL validation
        try:
            # Check if it's a valid URL structure
            if not (url.startswith('http://') or url.startswith('https://')):
                return False
            return True
        except Exception:
            return False

