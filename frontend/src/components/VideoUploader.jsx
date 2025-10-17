import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './VideoUploader.css';

function VideoUploader({ onUploadComplete }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('file'); // 'file' or 'url'
  const [youtubeUrl, setYoutubeUrl] = useState('');

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    
    if (!file) {
      setError('No file selected');
      return;
    }

    if (!file.type.startsWith('video/')) {
      setError('Please upload a video file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onUploadComplete(response.data.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload video');
      setUploading(false);
    }
  }, [onUploadComplete]);

  const handleYoutubeSubmit = async (e) => {
    e.preventDefault();
    
    if (!youtubeUrl.trim()) {
      setError('Please enter a YouTube URL');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const response = await axios.post('/api/upload-youtube', {
        url: youtubeUrl.trim()
      });

      onUploadComplete(response.data.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process YouTube URL');
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    },
    multiple: false,
    disabled: uploading
  });

  return (
    <div className="uploader-container">
      <div className="mode-selector">
        <button 
          className={`mode-button ${mode === 'file' ? 'active' : ''}`}
          onClick={() => setMode('file')}
          disabled={uploading}
        >
          📁 Upload File
        </button>
        <button 
          className={`mode-button ${mode === 'url' ? 'active' : ''}`}
          onClick={() => setMode('url')}
          disabled={uploading}
        >
          🔗 YouTube URL
        </button>
      </div>

      {mode === 'file' ? (
        <div
          {...getRootProps()}
          className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
        >
          <input {...getInputProps()} />
          
          {uploading ? (
            <div className="upload-status">
              <div className="spinner"></div>
              <p>Uploading video...</p>
            </div>
          ) : (
            <div className="upload-prompt">
              <div className="upload-icon">📹</div>
              {isDragActive ? (
                <p>Drop the video here</p>
              ) : (
                <>
                  <p className="primary-text">Drag & drop a video here</p>
                  <p className="secondary-text">or click to select</p>
                  <p className="format-text">Supported: MP4, MOV, AVI, MKV, WebM</p>
                </>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="url-input-container">
          {uploading ? (
            <div className="upload-status">
              <div className="spinner"></div>
              <p>Processing YouTube video...</p>
            </div>
          ) : (
            <form onSubmit={handleYoutubeSubmit} className="youtube-form">
              <div className="upload-icon">🎬</div>
              <p className="primary-text">Enter YouTube URL</p>
              <input
                type="text"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
                className="youtube-input"
                disabled={uploading}
              />
              <button type="submit" className="submit-button" disabled={uploading}>
                Process Video
              </button>
              <p className="format-text">Paste any YouTube video URL</p>
            </form>
          )}
        </div>
      )}

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}

export default VideoUploader;

