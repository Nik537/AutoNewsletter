# Testing & Error Handling Guide

## Built-in Error Handling

The application includes comprehensive error handling at multiple levels:

### Backend Error Handling

1. **File Upload Validation**
   - File type checking (video/* only)
   - File size limits (configurable via MAX_VIDEO_SIZE)
   - Proper error messages returned to frontend

2. **Video Processing**
   - FFmpeg error capture and reporting
   - Audio extraction failure handling
   - Frame extraction failure handling
   - Cleanup of temporary files even on failure

3. **AI Service**
   - API key validation on startup
   - API call error handling with retries
   - Fallback frame selection if AI fails
   - JSON parsing error handling

4. **Background Job Management**
   - Job status tracking (queued, processing, completed, failed)
   - Progress updates at each step
   - Error messages stored with job for user feedback

### Frontend Error Handling

1. **Upload Validation**
   - File type validation before upload
   - Size limit warnings
   - Network error handling with user-friendly messages

2. **Progress Tracking**
   - Status polling with error recovery
   - Failed job detection and display
   - Retry capability

3. **Download Handling**
   - Network error handling
   - Missing file detection

## Testing the Application

### Manual Testing Checklist

#### 1. Basic Workflow Test

```bash
# Start the application
./start.sh

# In browser (http://localhost:3000):
# 1. Upload a short video (< 1 minute)
# 2. Verify progress updates appear
# 3. Wait for completion
# 4. Check newsletter preview loads
# 5. Download ZIP file
# 6. Verify ZIP contains newsletter.md and images/
```

#### 2. Error Scenarios

**Test Invalid File Type:**
- Try uploading a PDF or image
- Expected: Error message "File must be a video"

**Test Large File:**
- Try uploading a video > 500MB
- Expected: Error message about size limit

**Test Without API Key:**
```bash
# Remove API key from .env
./start.sh
# Upload a video
# Expected: Processing fails with API key error
```

**Test Network Interruption:**
- Upload a video
- Stop backend during processing: `./stop.sh`
- Expected: Frontend shows connection error

**Test Invalid Video File:**
- Rename a text file to .mp4
- Upload it
- Expected: FFmpeg processing fails with clear error

#### 3. Load Testing

**Multiple Files:**
- Upload 3 videos in quick succession
- Expected: Jobs queue and process sequentially

**Large Video:**
- Upload a 10-minute video
- Expected: Processing completes successfully
- Note: May take 5-10 minutes

### Automated Testing Commands

```bash
# Test backend API directly
curl http://localhost:8000/
# Expected: {"message":"Video Newsletter Generator API","status":"running"}

# Check backend health
curl http://localhost:8000/docs
# Expected: Opens API documentation

# Test file upload
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/video.mp4"
# Expected: {"job_id":"...","message":"Video uploaded successfully"}
```

## Known Limitations

1. **Processing Time**
   - Long videos (> 10 minutes) may take 10+ minutes to process
   - Solution: Use shorter clips or be patient

2. **Memory Usage**
   - Large videos use significant RAM during processing
   - Solution: Close other applications or upgrade RAM

3. **API Rate Limits**
   - Anthropic API has rate limits
   - Solution: Wait between requests if you hit limits

4. **Concurrent Processing**
   - Current implementation processes one video at a time
   - Solution: Wait for current job to finish

5. **Storage**
   - Videos and outputs consume disk space
   - Solution: Regularly clean uploads/ and output/ directories

## Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| "File must be a video" | Wrong file type | Upload MP4, MOV, AVI, MKV, or WebM |
| "Video size exceeds maximum" | File too large | Use smaller video or increase MAX_VIDEO_SIZE |
| "ANTHROPIC_API_KEY not set" | Missing API key | Add key to backend/.env |
| "FFmpeg failed" | FFmpeg not installed or video corrupted | Install FFmpeg or try different video |
| "Job not found" | Invalid job ID | Use correct job ID from upload response |
| "Failed to transcribe" | Audio extraction failed | Check video has audio track |
| Network error | Backend not running | Run ./start.sh |

## Debugging Tips

### Check Backend Logs

```bash
tail -f backend.log
```

### Check Job Status

```bash
curl http://localhost:8000/api/status/YOUR_JOB_ID
```

### Check Temporary Files

```bash
# Check uploaded videos
ls -lh backend/uploads/

# Check output files
ls -lh backend/output/
```

### Clear Cache and Restart

```bash
./stop.sh
rm -rf backend/uploads/* backend/output/*
./start.sh
```

## Performance Optimization

### For Faster Processing

1. **Reduce Frame Extraction:**
   ```env
   # In backend/.env
   FRAME_INTERVAL=10  # Extract frames every 10 seconds
   ```

2. **Use Smaller Whisper Model:**
   ```python
   # In backend/app/video_processor.py, line 58
   model = WhisperModel("tiny", device="cpu", compute_type="int8")
   ```

3. **Pre-process Videos:**
   - Compress videos before upload
   - Use lower resolution (720p instead of 4K)

### For Better Quality

1. **More Frames:**
   ```env
   # In backend/.env
   FRAME_INTERVAL=3  # Extract frames every 3 seconds
   ```

2. **Better Whisper Model:**
   ```python
   # In backend/app/video_processor.py, line 58
   model = WhisperModel("medium", device="cpu", compute_type="int8")
   ```

3. **More Tokens for Article:**
   ```python
   # In backend/app/ai_service.py, line 117
   max_tokens=6000  # Longer articles
   ```

## Maintenance

### Regular Cleanup

```bash
# Clean up old jobs (older than 7 days)
find backend/uploads -type f -mtime +7 -delete
find backend/output -type d -mtime +7 -exec rm -rf {} +
```

### Monitor Disk Space

```bash
du -sh backend/uploads backend/output
```

### Update Dependencies

```bash
# Backend
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

## Reporting Issues

When reporting issues, please include:

1. Error message (exact text)
2. Contents of backend.log
3. Browser console errors (if frontend issue)
4. Video file details (format, size, duration)
5. Steps to reproduce

## Additional Notes

- The application has been tested with MP4, MOV, and AVI formats
- Slovenian translation quality depends on Claude's training data
- Screenshots are automatically selected based on visual interest
- All processing is done locally except AI API calls

