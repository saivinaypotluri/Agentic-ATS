import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  User, Mail, Phone, FileText, TrendingUp, Calendar, 
  CheckCircle, XCircle, Edit2, Save, X, Github, Linkedin,
  ExternalLink, Brain, Clock, MessageSquare, ArrowLeft
} from 'lucide-react';
import { candidateAPI, jobAPI, feedbackAPI } from '../services/api';

function CandidateDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // UI States
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({});
  
  // Job Match
  const [jobDescription, setJobDescription] = useState('');
  const [matchingJob, setMatchingJob] = useState(false);
  const [matchResult, setMatchResult] = useState(null);
  
  // Profile Intelligence
  const [enrichingProfile, setEnrichingProfile] = useState(false);
  const [profileResult, setProfileResult] = useState(null);
  
  // Scheduling
  const [schedulingInterview, setSchedulingInterview] = useState(false);
  const [suggestedSlots, setSuggestedSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState('');
  
  // Feedback
  const [interviewNotes, setInterviewNotes] = useState('');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackResult, setFeedbackResult] = useState(null);

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  const fetchCandidate = async () => {
    try {
      const data = await candidateAPI.getCandidate(id);
      setCandidate(data);
      setEditData({
        name: data.name || '',
        email: data.email || '',
        phone: data.phone || '',
        skills: data.skills || []
      });
    } catch (err) {
      setError('Failed to load candidate');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    try {
      const updated = await candidateAPI.updateCandidate(id, editData);
      setCandidate(updated);
      setIsEditing(false);
    } catch (err) {
      alert('Error updating candidate');
    }
  };

  const handleApprove = async (approved) => {
    try {
      await candidateAPI.approveCandidate(id, approved);
      fetchCandidate();
    } catch (err) {
      alert('Error updating approval status');
    }
  };

  const handleMatchJob = async () => {
    if (!jobDescription.trim()) {
      alert('Please enter a job description');
      return;
    }
    
    setMatchingJob(true);
    try {
      const result = await jobAPI.matchJob(id, jobDescription);
      setMatchResult(result);
      fetchCandidate(); // Refresh to get updated match score
    } catch (err) {
      alert('Error matching job');
    } finally {
      setMatchingJob(false);
    }
  };

  const handleEnrichProfile = async () => {
    setEnrichingProfile(true);
    try {
      const result = await jobAPI.fetchProfiles(id);
      setProfileResult(result);
      fetchCandidate(); // Refresh to get enriched data
    } catch (err) {
      alert(err.response?.data?.detail || 'Error enriching profile');
    } finally {
      setEnrichingProfile(false);
    }
  };

  const handleGetSuggestions = async () => {
    setSchedulingInterview(true);
    try {
      const result = await jobAPI.scheduleInterview(id, null);
      setSuggestedSlots(result.suggested_slots);
    } catch (err) {
      alert('Error getting interview suggestions');
    } finally {
      setSchedulingInterview(false);
    }
  };

  const handleScheduleInterview = async () => {
    if (!selectedSlot) {
      alert('Please select a time slot');
      return;
    }
    
    try {
      await jobAPI.scheduleInterview(id, selectedSlot);
      alert('Interview scheduled successfully!');
      fetchCandidate();
      setSuggestedSlots([]);
      setSelectedSlot('');
    } catch (err) {
      alert('Error scheduling interview');
    }
  };

  const handleSubmitFeedback = async () => {
    if (!interviewNotes.trim()) {
      alert('Please enter interview notes');
      return;
    }
    
    setSubmittingFeedback(true);
    try {
      const result = await feedbackAPI.submitFeedback(id, interviewNotes);
      setFeedbackResult(result);
      fetchCandidate();
    } catch (err) {
      alert('Error submitting feedback');
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const getMatchScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
        {error || 'Candidate not found'}
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Link to="/candidates" className="text-primary-600 hover:text-primary-800 flex items-center mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Candidates
        </Link>
        
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              {candidate.name || 'Unknown Candidate'}
            </h1>
            <p className="text-gray-600">Candidate ID: {candidate.id}</p>
          </div>
          
          <div className="flex gap-3">
            {!candidate.approved && !candidate.rejected && (
              <>
                <button
                  onClick={() => handleApprove(true)}
                  className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center"
                >
                  <CheckCircle className="h-5 w-5 mr-2" />
                  Approve
                </button>
                <button
                  onClick={() => handleApprove(false)}
                  className="bg-red-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors flex items-center"
                >
                  <XCircle className="h-5 w-5 mr-2" />
                  Reject
                </button>
              </>
            )}
            
            {candidate.approved && (
              <div className="bg-green-100 text-green-800 px-6 py-2 rounded-lg font-semibold flex items-center">
                <CheckCircle className="h-5 w-5 mr-2" />
                Approved
              </div>
            )}
            
            {candidate.rejected && (
              <div className="bg-red-100 text-red-800 px-6 py-2 rounded-lg font-semibold flex items-center">
                <XCircle className="h-5 w-5 mr-2" />
                Rejected
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Main Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">Basic Information</h2>
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="text-primary-600 hover:text-primary-800 flex items-center"
                >
                  <Edit2 className="h-4 w-4 mr-2" />
                  Edit
                </button>
              ) : (
                <div className="flex gap-2">
                  <button
                    onClick={handleSaveEdit}
                    className="bg-primary-600 text-white px-4 py-1 rounded flex items-center text-sm"
                  >
                    <Save className="h-4 w-4 mr-1" />
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditData({
                        name: candidate.name || '',
                        email: candidate.email || '',
                        phone: candidate.phone || '',
                        skills: candidate.skills || []
                      });
                    }}
                    className="bg-gray-300 text-gray-700 px-4 py-1 rounded flex items-center text-sm"
                  >
                    <X className="h-4 w-4 mr-1" />
                    Cancel
                  </button>
                </div>
              )}
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 flex items-center mb-1">
                  <User className="h-4 w-4 mr-2" />
                  Name
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    value={editData.name}
                    onChange={(e) => setEditData({...editData, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900">{candidate.name || 'Not provided'}</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 flex items-center mb-1">
                  <Mail className="h-4 w-4 mr-2" />
                  Email
                </label>
                {isEditing ? (
                  <input
                    type="email"
                    value={editData.email}
                    onChange={(e) => setEditData({...editData, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900">{candidate.email || 'Not provided'}</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 flex items-center mb-1">
                  <Phone className="h-4 w-4 mr-2" />
                  Phone
                </label>
                {isEditing ? (
                  <input
                    type="tel"
                    value={editData.phone}
                    onChange={(e) => setEditData({...editData, phone: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900">{candidate.phone || 'Not provided'}</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-1 block">Skills</label>
                {candidate.skills && candidate.skills.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {candidate.skills.map((skill, index) => (
                      <span
                        key={index}
                        className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500">No skills identified</p>
                )}
              </div>
            </div>
          </div>

          {/* Job Matching */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
              <TrendingUp className="h-6 w-6 mr-2 text-primary-600" />
              Job Matching
            </h2>

            {candidate.match_score !== null && candidate.match_score !== undefined && (
              <div className={`mb-4 p-4 rounded-lg border ${getMatchScoreColor(candidate.match_score)}`}>
                <div className="flex items-center justify-between">
                  <span className="font-semibold">Current Match Score:</span>
                  <span className="text-2xl font-bold">{candidate.match_score}%</span>
                </div>
              </div>
            )}

            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste job description here..."
                rows="6"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <button
                onClick={handleMatchJob}
                disabled={matchingJob}
                className={`mt-3 bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors ${
                  matchingJob ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {matchingJob ? 'Computing...' : 'Compute Match Score'}
              </button>
            </div>

            {matchResult && (
              <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-900">{matchResult.message}</p>
              </div>
            )}
          </div>

          {/* Profile Intelligence */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
              <Brain className="h-6 w-6 mr-2 text-purple-600" />
              Profile Intelligence
            </h2>

            <div className="mb-4">
              <button
                onClick={handleEnrichProfile}
                disabled={enrichingProfile || (!candidate.linkedin_url && !candidate.github_url && (!candidate.misc_links || candidate.misc_links.length === 0))}
                className={`bg-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors ${
                  (enrichingProfile || (!candidate.linkedin_url && !candidate.github_url && (!candidate.misc_links || candidate.misc_links.length === 0))) 
                    ? 'opacity-50 cursor-not-allowed' 
                    : ''
                }`}
              >
                {enrichingProfile ? 'Enriching...' : 'Enrich Profile from URLs'}
              </button>
              
              {!candidate.linkedin_url && !candidate.github_url && (!candidate.misc_links || candidate.misc_links.length === 0) && (
                <p className="text-sm text-gray-500 mt-2">No URLs found in resume</p>
              )}
            </div>

            {/* LinkedIn Data */}
            {candidate.linkedin_data && (
              <div className="mb-4 border border-blue-200 rounded-lg p-4 bg-blue-50">
                <h3 className="font-semibold text-blue-900 mb-2 flex items-center">
                  <Linkedin className="h-5 w-5 mr-2" />
                  LinkedIn Profile
                </h3>
                <div className="space-y-1 text-sm text-blue-800">
                  <p><strong>Headline:</strong> {candidate.linkedin_data.headline}</p>
                  <p><strong>Location:</strong> {candidate.linkedin_data.location}</p>
                  <p><strong>Connections:</strong> {candidate.linkedin_data.connections}</p>
                  {candidate.linkedin_data.skills && (
                    <p><strong>Top Skills:</strong> {candidate.linkedin_data.skills.join(', ')}</p>
                  )}
                </div>
              </div>
            )}

            {/* GitHub Data */}
            {candidate.github_data && (
              <div className="mb-4 border border-gray-300 rounded-lg p-4 bg-gray-50">
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <Github className="h-5 w-5 mr-2" />
                  GitHub Profile
                </h3>
                <div className="space-y-1 text-sm text-gray-800">
                  <p><strong>Username:</strong> {candidate.github_data.username}</p>
                  <p><strong>Public Repos:</strong> {candidate.github_data.public_repos}</p>
                  <p><strong>Followers:</strong> {candidate.github_data.followers}</p>
                  {candidate.github_data.top_languages && (
                    <p><strong>Top Languages:</strong> {candidate.github_data.top_languages.join(', ')}</p>
                  )}
                  {candidate.github_data.bio && candidate.github_data.bio !== 'N/A' && (
                    <p><strong>Bio:</strong> {candidate.github_data.bio}</p>
                  )}
                </div>
              </div>
            )}

            {profileResult && (
              <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-semibold text-green-900 mb-2">Profile Enrichment Summary</h3>
                <pre className="text-sm text-green-800 whitespace-pre-wrap">{profileResult.summary}</pre>
              </div>
            )}
          </div>

          {/* Feedback Section */}
          {candidate.scheduled_interview && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                <MessageSquare className="h-6 w-6 mr-2 text-green-600" />
                Interview Feedback
              </h2>

              {candidate.feedback_summary ? (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Feedback Summary</h3>
                  <pre className="text-sm text-gray-800 whitespace-pre-wrap">{candidate.feedback_summary}</pre>
                </div>
              ) : (
                <>
                  <div>
                    <label className="text-sm font-medium text-gray-700 mb-2 block">
                      Interview Notes
                    </label>
                    <textarea
                      value={interviewNotes}
                      onChange={(e) => setInterviewNotes(e.target.value)}
                      placeholder="Enter interview notes here..."
                      rows="6"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                    <button
                      onClick={handleSubmitFeedback}
                      disabled={submittingFeedback}
                      className={`mt-3 bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors ${
                        submittingFeedback ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                    >
                      {submittingFeedback ? 'Processing...' : 'Generate Feedback Summary'}
                    </button>
                  </div>

                  {feedbackResult && (
                    <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
                      <h3 className="font-semibold text-green-900 mb-2">Generated Summary</h3>
                      <pre className="text-sm text-green-800 whitespace-pre-wrap">{feedbackResult.feedback_summary}</pre>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>

        {/* Right Column - Actions & Schedule */}
        <div className="space-y-6">
          {/* Interview Scheduling */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-orange-600" />
              Interview Scheduling
            </h2>

            {candidate.scheduled_interview ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-sm font-medium text-green-900 mb-1">Interview Scheduled</p>
                <p className="text-lg font-bold text-green-800">{candidate.scheduled_interview}</p>
              </div>
            ) : (
              <>
                <button
                  onClick={handleGetSuggestions}
                  disabled={schedulingInterview}
                  className={`w-full bg-orange-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-orange-700 transition-colors mb-4 ${
                    schedulingInterview ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  {schedulingInterview ? 'Loading...' : 'Get Suggested Slots'}
                </button>

                {suggestedSlots.length > 0 && (
                  <div>
                    <label className="text-sm font-medium text-gray-700 mb-2 block">
                      Select a time slot:
                    </label>
                    <div className="space-y-2 mb-4">
                      {suggestedSlots.map((slot, index) => (
                        <label
                          key={index}
                          className="flex items-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer"
                        >
                          <input
                            type="radio"
                            name="slot"
                            value={slot}
                            checked={selectedSlot === slot}
                            onChange={(e) => setSelectedSlot(e.target.value)}
                            className="mr-3"
                          />
                          <Clock className="h-4 w-4 mr-2 text-gray-600" />
                          <span className="text-sm">{slot}</span>
                        </label>
                      ))}
                    </div>
                    <button
                      onClick={handleScheduleInterview}
                      disabled={!selectedSlot}
                      className={`w-full bg-primary-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors ${
                        !selectedSlot ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                    >
                      Schedule Interview
                    </button>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Resume File */}
          {candidate.resume_filename && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <FileText className="h-5 w-5 mr-2 text-gray-600" />
                Resume File
              </h2>
              <p className="text-sm text-gray-600">{candidate.resume_filename}</p>
            </div>
          )}

          {/* Profile Links */}
          {(candidate.linkedin_url || candidate.github_url || (candidate.misc_links && candidate.misc_links.length > 0)) && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <ExternalLink className="h-5 w-5 mr-2 text-gray-600" />
                Profile Links
              </h2>
              <div className="space-y-2">
                {candidate.linkedin_url && (
                  <a
                    href={candidate.linkedin_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    <Linkedin className="h-4 w-4 mr-2" />
                    LinkedIn Profile
                  </a>
                )}
                {candidate.github_url && (
                  <a
                    href={candidate.github_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-gray-800 hover:text-gray-900 transition-colors"
                  >
                    <Github className="h-4 w-4 mr-2" />
                    GitHub Profile
                  </a>
                )}
                {candidate.misc_links && candidate.misc_links.map((link, index) => (
                  <a
                    key={index}
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center text-primary-600 hover:text-primary-800 transition-colors text-sm"
                  >
                    <ExternalLink className="h-3 w-3 mr-2" />
                    Other Link {index + 1}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CandidateDetailPage;
