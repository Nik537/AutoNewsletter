import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ProgressTracker.css';

function ProgressTracker({ jobId, onStatusUpdate, onComplete }) {
  const [status, setStatus] = useState({
    status: 'queued',
    progress: 0,
    message: 'Starting...'
  });

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await axios.get(`/api/status/${jobId}`);
        const newStatus = response.data;
        setStatus(newStatus);
        onStatusUpdate(newStatus);

        if (newStatus.status === 'completed') {
          // Fetch the newsletter content
          const previewResponse = await axios.get(`/api/preview/${jobId}`);
          onComplete(previewResponse.data.content);
        } else if (newStatus.status === 'failed') {
          // Handle error
          console.error('Processing failed:', newStatus.error);
        }
      } catch (err) {
        console.error('Failed to fetch status:', err);
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, [jobId, onStatusUpdate, onComplete]);

  const getStageInfo = () => {
    if (status.progress < 20) return { stage: 'Uploading', icon: '📤' };
    if (status.progress < 30) return { stage: 'Extracting Audio', icon: '🎵' };
    if (status.progress < 50) return { stage: 'Extracting Frames', icon: '🎬' };
    if (status.progress < 70) return { stage: 'Analyzing with AI', icon: '🤖' };
    if (status.progress < 100) return { stage: 'Generating Newsletter', icon: '📝' };
    return { stage: 'Complete', icon: '✅' };
  };

  const stageInfo = getStageInfo();

  return (
    <div className="progress-container">
      <div className="progress-card">
        <div className="stage-icon">{stageInfo.icon}</div>
        <h2>{stageInfo.stage}</h2>
        <p className="status-message">{status.message}</p>

        <div className="progress-bar-container">
          <div 
            className="progress-bar"
            style={{ width: `${status.progress}%` }}
          >
            <span className="progress-text">{status.progress}%</span>
          </div>
        </div>

        <div className="progress-details">
          <div className="detail-item">
            <span className="detail-label">Job ID:</span>
            <span className="detail-value">{jobId.slice(0, 8)}...</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Status:</span>
            <span className={`detail-value status-${status.status}`}>
              {status.status}
            </span>
          </div>
        </div>

        {status.status === 'failed' && (
          <div className="error-box">
            <strong>Error:</strong> {status.error}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProgressTracker;

