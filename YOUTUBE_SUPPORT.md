# YouTube Support Guide

## Overview

The Video Newsletter Generator now supports downloading videos directly from YouTube URLs in addition to file uploads. This feature allows you to process any publicly accessible YouTube video without manually downloading it first.

## How to Use

### 1. Access the YouTube URL Mode

1. Open the application at http://localhost:3000
2. Click the **"🔗 YouTube URL"** button at the top
3. The interface switches to URL input mode

### 2. Enter YouTube URL

1. Paste any YouTube video URL in the input field
2. Supported URL formats:
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://m.youtube.com/watch?v=VIDEO_ID`
   - Any standard YouTube video URL

### 3. Process the Video

1. Click **"Process Video"** button
2. The system will:
   - Download the video from YouTube (5-15% progress)
   - Extract audio and frames (15-30% progress)
   - Transcribe and analyze (30-70% progress)
   - Generate Slovenian newsletter (70-100% progress)

### 4. Download Results

Once processing is complete:
- Preview the generated article
- Download as ZIP file with markdown + images

## Features

✅ **Automatic Download**: No need to manually download videos  
✅ **Quality Selection**: Automatically selects best available quality  
✅ **Format Conversion**: Converts to MP4 format automatically  
✅ **Progress Tracking**: Shows download and processing progress  
✅ **Error Handling**: Clear error messages if download fails  

## Technical Details

### Backend Implementation

The backend uses `yt-dlp` (a fork of youtube-dl) to download videos:

```python
# New endpoint: POST /api/upload-youtube
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

### Download Process

1. **Validation**: Checks if URL is a valid YouTube URL
2. **Download**: Uses yt-dlp to download best quality MP4
3. **Storage**: Saves to uploads directory with job ID
4. **Processing**: Continues with normal video processing pipeline

### Configuration

Downloaded videos are stored temporarily in `backend/uploads/` and cleaned up after processing completes.

## Supported Videos

✅ **Public videos**: Any publicly accessible YouTube video  
✅ **Unlisted videos**: Videos with a direct link  
❌ **Private videos**: Requires authentication (not supported)  
❌ **Age-restricted**: May require additional setup  
❌ **Live streams**: Only completed videos are supported  

## Troubleshooting

### "Invalid YouTube URL"
- **Cause**: URL format not recognized
- **Solution**: Copy the full URL from YouTube's address bar

### "Failed to download YouTube video"
**Possible causes:**
- Video is private or restricted
- Network connection issues
- Video was removed
- yt-dlp needs updating

**Solutions:**
1. Verify the video is publicly accessible
2. Check your internet connection
3. Try a different video
4. Update yt-dlp: `pip install -U yt-dlp`

### Download Takes Too Long
**Causes:**
- Large video file
- Slow internet connection
- High quality video (4K/8K)

**Solutions:**
- Be patient - downloads can take 1-5 minutes
- Check backend.log for progress
- Consider using file upload for very large videos

### "Connection refused" or Network Errors
**Causes:**
- YouTube rate limiting
- IP restrictions
- Firewall blocking yt-dlp

**Solutions:**
- Wait a few minutes and try again
- Check firewall settings
- Use a VPN if region-restricted

## API Usage

### Upload YouTube Video

**Endpoint:** `POST /api/upload-youtube`

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "job_id": "uuid-here",
  "message": "YouTube video download started"
}
```

### Check Status

**Endpoint:** `GET /api/status/{job_id}`

**Response:**
```json
{
  "job_id": "uuid-here",
  "status": "downloading",  // or "processing", "completed", "failed"
  "progress": 10,
  "message": "Downloading video from YouTube..."
}
```

## Performance Notes

### Download Times (approximate)

| Video Length | File Size | Download Time |
|--------------|-----------|---------------|
| 2-5 minutes  | 50-150MB  | 30-90 seconds |
| 5-10 minutes | 150-300MB | 1-3 minutes   |
| 10-20 minutes| 300-600MB | 3-6 minutes   |
| 20+ minutes  | 600MB+    | 5+ minutes    |

*Times vary based on internet speed and video quality*

### Total Processing Time

- **YouTube Download**: 1-5 minutes
- **Video Processing**: 2-5 minutes
- **Total**: 3-10 minutes (depending on video length)

## Privacy & Legal

### Privacy
- Videos are downloaded temporarily
- Automatically deleted after processing
- No videos stored long-term
- No data sent to third parties (except Anthropic API for processing)

### Legal Considerations
- Only use videos you have permission to process
- Respect copyright and YouTube's Terms of Service
- This tool is for personal/educational use
- Commercial use may require additional permissions

## Updates

The YouTube downloader (`yt-dlp`) is actively maintained. To update:

```bash
cd backend
source venv/bin/activate
pip install -U yt-dlp
```

## Alternative: Manual Upload

If YouTube download fails or is not available, you can still:

1. Download the video manually using any YouTube downloader
2. Switch to "Upload File" mode
3. Drag & drop the downloaded video file

## Support

For issues specific to YouTube downloads:

1. Check backend.log for detailed error messages
2. Verify the URL is accessible in your browser
3. Try updating yt-dlp
4. Use manual upload as fallback

For general issues, see [TESTING.md](TESTING.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md).

---

**Note:** YouTube's structure and policies change frequently. If downloads stop working, updating `yt-dlp` usually resolves the issue.

