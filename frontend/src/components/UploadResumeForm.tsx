import React, { useState } from 'react';

interface Props {
  onUploadComplete: (sessionId: string) => void;
}

const UploadResumeForm: React.FC<Props> = ({ onUploadComplete }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/upload-resume`, {
        method: 'POST',
        headers: {
          'x-api-key': import.meta.env.VITE_API_KEY || '',
        },
        body: formData,
      });

      const data = await response.json();
      if (response.ok && data.session_id) {
        onUploadComplete(data.session_id);
      } else {
        alert(data.detail || 'Upload failed');
      }
    } catch (err) {
      alert('Upload error');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-2">Upload Resume</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-2"
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? 'Uploading...' : 'Upload Resume'}
      </button>
    </div>
  );
};

export default UploadResumeForm;
