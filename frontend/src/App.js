import React, { useState } from 'react';
import './App.css';
import VideoUploader from './components/VideoUploader';
import ProgressTracker from './components/ProgressTracker';
import NewsletterPreview from './components/NewsletterPreview';

function App() {
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [newsletter, setNewsletter] = useState(null);

  const handleUploadComplete = (newJobId) => {
    setJobId(newJobId);
    setStatus({ status: 'queued', progress: 0, message: 'Starting...' });
  };

  const handleStatusUpdate = (newStatus) => {
    setStatus(newStatus);
  };

  const handleComplete = (newsletterContent) => {
    setNewsletter(newsletterContent);
  };

  const handleReset = () => {
    setJobId(null);
    setStatus(null);
    setNewsletter(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎥 Video Newsletter Generator</h1>
        <p>Convert English videos to Slovenian newsletter articles with AI</p>
      </header>

      <main className="App-main">
        {!jobId && (
          <VideoUploader onUploadComplete={handleUploadComplete} />
        )}

        {jobId && !newsletter && (
          <ProgressTracker 
            jobId={jobId}
            onStatusUpdate={handleStatusUpdate}
            onComplete={handleComplete}
          />
        )}

        {newsletter && (
          <NewsletterPreview 
            jobId={jobId}
            content={newsletter}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by Claude AI & Whisper</p>
      </footer>
    </div>
  );
}

export default App;

