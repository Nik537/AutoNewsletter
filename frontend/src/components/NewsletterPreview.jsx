import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import './NewsletterPreview.css';

function NewsletterPreview({ jobId, content, onReset }) {
  const [downloading, setDownloading] = useState(false);
  const [activeTab, setActiveTab] = useState('newsletter');

  // Parse the content to extract newsletter and LinkedIn post
  const newsletterContent = content.content || content;
  const linkedinPost = content.linkedin_post || '';

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

      const extension = format === 'html' ? 'html' : format === 'docx' ? 'docx' : 'md';
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `newsletter.${extension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      alert(`Failed to download ${format} format`);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy:', err);
    });
  };

  return (
    <div className="preview-container">
      <div className="preview-header">
        <h2>✅ Content Generated!</h2>

        <div className="tab-selector">
          <button
            className={`tab-button ${activeTab === 'newsletter' ? 'active' : ''}`}
            onClick={() => setActiveTab('newsletter')}
          >
            📰 Newsletter
          </button>
          <button
            className={`tab-button ${activeTab === 'linkedin' ? 'active' : ''}`}
            onClick={() => setActiveTab('linkedin')}
          >
            💼 LinkedIn Post
          </button>
        </div>

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
        <div className="action-buttons">
          <button
            className="new-button"
            onClick={onReset}
          >
            🔄 Process Another Video
          </button>
        </div>
      </div>

      {activeTab === 'newsletter' ? (
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
            {newsletterContent}
          </ReactMarkdown>
        </div>
      ) : (
        <div className="preview-content linkedin-content">
          <div className="linkedin-header">
            <h3>LinkedIn Post (Slovenian)</h3>
            <button
              className="copy-button"
              onClick={() => copyToClipboard(linkedinPost)}
            >
              📋 Copy to Clipboard
            </button>
          </div>
          <div className="linkedin-post">
            {linkedinPost.split('\n').map((line, idx) => (
              <p key={idx}>{line}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default NewsletterPreview;

