import React, { useState } from 'react';

interface Props {
  sessionId: string;
  onJobAnalysisStart: () => void;
}

const JobDetailsForm: React.FC<Props> = ({ sessionId, onJobAnalysisStart }) => {
  const [jobUrl, setJobUrl] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [personalWriteup, setPersonalWriteup] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<{ tailored_resume?: string; interview_materials?: string } | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setResults(null);
    onJobAnalysisStart();

    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/analyze-job?session_id=${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': import.meta.env.VITE_API_KEY || '',
        },
        body: JSON.stringify({
          job_posting_url: jobUrl,
          github_url: githubUrl,
          personal_writeup: personalWriteup,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        alert(data.detail || 'Job analysis failed');
        setLoading(false);
        return;
      }

      // Begin polling results after analysis starts
      const pollResults = async () => {
        try {
          const resultRes = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/results/${sessionId}`, {
            headers: {
              'x-api-key': import.meta.env.VITE_API_KEY || '',
            },
          });

          const resultData = await resultRes.json();

          if (resultData.status === 'completed') {
            setResults(resultData.results);
            setLoading(false);
          } else {
            setTimeout(pollResults, 3000); // Retry in 3 seconds
          }
        } catch (pollErr) {
          console.error('Polling error:', pollErr);
          setTimeout(pollResults, 3000);
        }
      };

      pollResults();
    } catch (err) {
      alert('Network error during analysis');
      setLoading(false);
    }
  };

  const download = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-2">Job Details</h2>

      <input
        type="text"
        placeholder="Job Posting URL"
        className="block w-full mb-2 p-2 border rounded"
        value={jobUrl}
        onChange={(e) => setJobUrl(e.target.value)}
      />
      <input
        type="text"
        placeholder="GitHub URL (optional)"
        className="block w-full mb-2 p-2 border rounded"
        value={githubUrl}
        onChange={(e) => setGithubUrl(e.target.value)}
      />
      <textarea
        placeholder="Personal Writeup (optional)"
        className="block w-full mb-2 p-2 border rounded"
        rows={3}
        value={personalWriteup}
        onChange={(e) => setPersonalWriteup(e.target.value)}
      />
      <button
        className="px-4 py-2 bg-black text-white rounded disabled:opacity-50"
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Analyze Job'}
      </button>

      {loading && (
        <p className="mt-4 text-gray-600 italic">Analyzing job and generating results… Please wait ⏳</p>
      )}

      {results && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-4">Results</h2>

          {results.tailored_resume && (
            <div className="mb-4">
              <h3 className="font-semibold">Tailored Resume</h3>
              <pre className="bg-gray-100 p-2 overflow-x-auto whitespace-pre-wrap text-sm">
                {results.tailored_resume}
              </pre>
              <button
                className="mt-2 px-4 py-1 bg-blue-500 text-white rounded"
                onClick={() => download('tailored_resume.md', results.tailored_resume!)}
              >
                Download Resume
              </button>
            </div>
          )}

          {results.interview_materials && (
            <div>
              <h3 className="font-semibold">Interview Questions</h3>
              <pre className="bg-gray-100 p-2 overflow-x-auto whitespace-pre-wrap text-sm">
                {results.interview_materials}
              </pre>
              <button
                className="mt-2 px-4 py-1 bg-blue-500 text-white rounded"
                onClick={() => download('interview_materials.md', results.interview_materials!)}
              >
                Download Questions
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default JobDetailsForm;
