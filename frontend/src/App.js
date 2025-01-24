import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [organizationName, setOrganizationName] = useState('');
  const [pdfUrl, setPdfUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerateResume = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://localhost:8000/generate_resume', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      const { resume_id, organization_name } = data;
      setOrganizationName(organization_name);
      setPdfUrl(`http://localhost:8000/download_resume/${resume_id}`);
    } catch (error) {
      console.error('Error generating resume:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <main>
        <div className="form-container">
          <h1>Resume Enhancer</h1>
          <div className="form-group">
            <label htmlFor="file">Upload your PDF Resume:</label>
            <input
              type="file"
              id="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>
          <div className="form-group">
            <label htmlFor="jobDescription">Paste the Job Description:</label>
            <textarea
              id="jobDescription"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows="10"
              cols="50"
              placeholder="Paste the job description here..."
            />
          </div>
          <button onClick={handleGenerateResume} disabled={loading || !file} className="generate-button">
            {loading ? 'Generating...' : 'Generate Resume'}
          </button>
        </div>
        {pdfUrl && (
          <div className="pdf-preview">
            <h2>Preview PDF</h2>
            <iframe src={pdfUrl} width="100%" height="500px" title="PDF Preview"></iframe>
            <a href={pdfUrl} download={`${organizationName}_resume.pdf`} className="download-link">
              Download PDF
            </a>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
