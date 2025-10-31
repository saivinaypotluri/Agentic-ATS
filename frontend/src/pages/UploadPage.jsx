import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { candidateAPI } from '../services/api';

function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      
      if (!validTypes.includes(selectedFile.type) && !selectedFile.name.match(/\.(pdf|docx|txt)$/i)) {
        setError('Please upload a PDF, DOCX, or TXT file');
        setFile(null);
        return;
      }
      
      setFile(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const response = await candidateAPI.uploadResume(file);
      setResult(response);
      
      // Redirect to candidate detail page after 2 seconds
      setTimeout(() => {
        navigate(`/candidate/${response.candidate_id}`);
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading resume. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    
    if (droppedFile) {
      const event = { target: { files: [droppedFile] } };
      handleFileChange(event);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">Upload Resume</h1>
      
      <div className="bg-white rounded-lg shadow-md p-8">
        <div
          className="border-3 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-primary-500 transition-colors cursor-pointer"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => document.getElementById('file-input').click()}
        >
          <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          
          {!file ? (
            <>
              <p className="text-lg text-gray-600 mb-2">
                Drag and drop your resume here, or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supported formats: PDF, DOCX, TXT
              </p>
            </>
          ) : (
            <div className="flex items-center justify-center">
              <FileText className="h-8 w-8 text-primary-600 mr-2" />
              <span className="text-lg text-gray-800 font-medium">{file.name}</span>
            </div>
          )}
          
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        {file && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className={`mt-6 w-full bg-primary-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-primary-700 transition-colors ${
              uploading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            {uploading ? 'Uploading...' : 'Upload and Parse Resume'}
          </button>
        )}

        {error && (
          <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-red-800 font-semibold mb-1">Error</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-start mb-4">
              <CheckCircle className="h-5 w-5 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-green-800 font-semibold mb-1">Success!</h3>
                <p className="text-green-700">{result.message}</p>
              </div>
            </div>
            
            <div className="bg-white rounded p-4 space-y-2">
              <div className="flex justify-between">
                <span className="font-medium text-gray-700">Candidate ID:</span>
                <span className="text-gray-900">{result.candidate_id}</span>
              </div>
              {result.name && (
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Name:</span>
                  <span className="text-gray-900">{result.name}</span>
                </div>
              )}
              {result.email && (
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Email:</span>
                  <span className="text-gray-900">{result.email}</span>
                </div>
              )}
              {result.phone && (
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Phone:</span>
                  <span className="text-gray-900">{result.phone}</span>
                </div>
              )}
              {result.skills && result.skills.length > 0 && (
                <div>
                  <span className="font-medium text-gray-700">Skills:</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {result.skills.slice(0, 10).map((skill, index) => (
                      <span
                        key={index}
                        className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <p className="text-sm text-gray-600 mt-4">
              Redirecting to candidate profile...
            </p>
          </div>
        )}
      </div>

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">What happens next?</h3>
        <ul className="space-y-2 text-blue-800">
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">?</span>
            <span>Resume is parsed and candidate information is extracted</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">?</span>
            <span>Skills, education, and experience are automatically identified</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">?</span>
            <span>LinkedIn and GitHub URLs are detected for profile enrichment</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">?</span>
            <span>You can then match the candidate with a job description and enrich their profile</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default UploadPage;
