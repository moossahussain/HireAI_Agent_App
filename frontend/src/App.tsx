import React, { useState } from 'react';
import UploadResumeForm from './components/UploadResumeForm';
import JobDetailsForm from './components/JobDetailsForm';

const App: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>('');

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">HireAI Resume Analyzer</h1>

      {/* Upload Resume */}
      <UploadResumeForm onUploadComplete={setSessionId} />

      {/* Show Job Details Form when sessionId is available */}
      {sessionId && (
        <JobDetailsForm
          sessionId={sessionId}
          onJobAnalysisStart={() => console.log('Job analysis started')}
        />
      )}
    </div>
  );
};

export default App;
