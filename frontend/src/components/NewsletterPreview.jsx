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

  const handleDownloadFormat = async (format) => {
    try {
      const response = await axios.get(`/api/download/${jobId}/${format}`, {
        responseType: 'blob',
      });

      let extension;
      if (format === 'html') {
        extension = 'html';
      } else if (format === 'docx') {
        extension = 'docx';
      } else if (format === 'linkedin' || format === 'x') {
        extension = 'json';
      } else {
        extension = 'md';
      }

      const filename = format === 'linkedin' ? 'linkedin_post.json' :
                       format === 'x' ? 'x_post.json' :
                       `newsletter.${extension}`;

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      alert(`Failed to download ${format} format`);
    }
  };

  return (
    <div className="preview-container">
      <div className="preview-header">
        <h2>✅ Newsletter Generated!</h2>
        <div className="action-buttons">
          <button 
            className="download-button primary"
            onClick={handleDownload}
            disabled={downloading}
          >
            {downloading ? '⏳ Downloading...' : '📦 Download All (ZIP)'}
          </button>
        </div>
        <div className="format-buttons">
          <h3 style={{ width: '100%', textAlign: 'center', marginBottom: '10px', fontSize: '14px' }}>Newsletter Formats</h3>
          <button
            className="format-button"
            onClick={() => handleDownloadFormat('docx')}
          >
            📄 Word (DOCX)
          </button>
          <button
            className="format-button"
            onClick={() => handleDownloadFormat('html')}
          >
            🌐 HTML (Notion)
          </button>
          <button
            className="format-button"
            onClick={() => handleDownloadFormat('markdown')}
          >
            📝 Markdown
          </button>
        </div>
        <div className="format-buttons" style={{ marginTop: '15px' }}>
          <h3 style={{ width: '100%', textAlign: 'center', marginBottom: '10px', fontSize: '14px' }}>Social Media Formats</h3>
          <button
            className="format-button"
            onClick={() => handleDownloadFormat('linkedin')}
          >
            💼 LinkedIn Post
          </button>
          <button
            className="format-button"
            onClick={() => handleDownloadFormat('x')}
          >
            𝕏 X Thread
          </button>
        </div>
        <div className="action-buttons">
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

