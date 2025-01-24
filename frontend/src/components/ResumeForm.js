import React, { useState } from 'react';
import './ResumeForm.css';

function ResumeForm() {
  const [jobDescription, setJobDescription] = useState('');
  const [role, setRole] = useState('');
  const [experience, setExperience] = useState('');
  const [keywords, setKeywords] = useState('');
  const [message, setMessage] = useState('');
  const [resumeId, setResumeId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const resumeData = {
      job_description: jobDescription,
      role: role,
      experience: experience,
      keywords: keywords.split(','),
    };

    try {
      const response = await fetch('http://localhost:8000/generate_resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(resumeData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate resume');
      }

      const data = await response.json();
      setMessage(`Resume Generated Successfully! ID: ${data.resume_id}`);
      setResumeId(data.resume_id);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="resume-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Job Description:</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label>Target Role:</label>
        <input
          type="text"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label>Years of Experience:</label>
        <input
          type="number"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label>Keywords (comma separated):</label>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={isLoading}>Generate Resume</button>
      {isLoading && <div className="loading">Generating your resume...</div>}
      {message && <div className="message">{message}</div>}
      {resumeId && (
        <div className="resume-download">
          <a href={`http://localhost:8000/download_resume/${resumeId}`} target="_blank" rel="noopener noreferrer">
            Download Resume
          </a>
        </div>
      )}
    </form>
  );
}

export default ResumeForm;
