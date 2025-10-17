import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import './NewsletterPreview.css';

function NewsletterPreview({ jobId, content, onReset }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const response = await axios.get(`/api/download/${jobId}`, {
        responseType: 'blob',
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `newsletter_${jobId}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      alert('Failed to download newsletter');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="preview-container">
      <div className="preview-header">
        <h2>✅ Newsletter Generated!</h2>
        <div className="action-buttons">
          <button 
            className="download-button"
            onClick={handleDownload}
            disabled={downloading}
          >
            {downloading ? '⏳ Downloading...' : '⬇️ Download ZIP'}
          </button>
          <button 
            className="new-button"
            onClick={onReset}
          >
            🔄 Process Another Video
          </button>
        </div>
      </div>

      <div className="preview-content">
        <ReactMarkdown
          components={{
            img: ({node, ...props}) => (
              <img 
                {...props} 
                alt={props.alt || 'Newsletter image'}
                src={`http://localhost:8000/output/${jobId}/${props.src}`}
              />
            )
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default NewsletterPreview;

