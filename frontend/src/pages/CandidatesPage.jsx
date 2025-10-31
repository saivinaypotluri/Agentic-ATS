import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { User, Mail, Phone, TrendingUp, CheckCircle, XCircle, Calendar, ExternalLink } from 'lucide-react';
import { candidateAPI } from '../services/api';

function CandidatesPage() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, approved, pending, rejected

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const data = await candidateAPI.getAllCandidates();
      setCandidates(data);
    } catch (err) {
      setError('Failed to load candidates');
    } finally {
      setLoading(false);
    }
  };

  const getFilteredCandidates = () => {
    switch (filter) {
      case 'approved':
        return candidates.filter(c => c.approved);
      case 'pending':
        return candidates.filter(c => !c.approved && !c.rejected);
      case 'rejected':
        return candidates.filter(c => c.rejected);
      default:
        return candidates;
    }
  };

  const getMatchScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-blue-600 bg-blue-50';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
        {error}
      </div>
    );
  }

  const filteredCandidates = getFilteredCandidates();

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-4xl font-bold text-gray-800">Candidates</h1>
        <Link
          to="/upload"
          className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
        >
          Upload New Resume
        </Link>
      </div>

      {/* Filter Tabs */}
      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="flex border-b">
          {[
            { key: 'all', label: 'All Candidates', count: candidates.length },
            { key: 'approved', label: 'Approved', count: candidates.filter(c => c.approved).length },
            { key: 'pending', label: 'Pending', count: candidates.filter(c => !c.approved && !c.rejected).length },
            { key: 'rejected', label: 'Rejected', count: candidates.filter(c => c.rejected).length },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setFilter(tab.key)}
              className={`px-6 py-3 font-medium transition-colors ${
                filter === tab.key
                  ? 'border-b-2 border-primary-600 text-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.label} ({tab.count})
            </button>
          ))}
        </div>
      </div>

      {/* Candidates List */}
      {filteredCandidates.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <User className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No candidates found</h3>
          <p className="text-gray-600 mb-6">
            {filter === 'all' 
              ? 'Upload a resume to get started'
              : `No ${filter} candidates yet`
            }
          </p>
          {filter === 'all' && (
            <Link
              to="/upload"
              className="inline-block bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Upload Resume
            </Link>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {filteredCandidates.map((candidate) => (
            <div key={candidate.id} className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow">
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <h2 className="text-2xl font-bold text-gray-800">
                        {candidate.name || 'Unknown Candidate'}
                      </h2>
                      {candidate.approved && (
                        <CheckCircle className="h-6 w-6 text-green-600 ml-3" />
                      )}
                      {candidate.rejected && (
                        <XCircle className="h-6 w-6 text-red-600 ml-3" />
                      )}
                    </div>
                    
                    <div className="flex flex-wrap gap-4 text-gray-600 mb-4">
                      {candidate.email && (
                        <div className="flex items-center">
                          <Mail className="h-4 w-4 mr-2" />
                          <span>{candidate.email}</span>
                        </div>
                      )}
                      {candidate.phone && (
                        <div className="flex items-center">
                          <Phone className="h-4 w-4 mr-2" />
                          <span>{candidate.phone}</span>
                        </div>
                      )}
                      {candidate.scheduled_interview && (
                        <div className="flex items-center text-primary-600">
                          <Calendar className="h-4 w-4 mr-2" />
                          <span>Interview: {candidate.scheduled_interview}</span>
                        </div>
                      )}
                    </div>

                    {/* Skills */}
                    {candidate.skills && candidate.skills.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {candidate.skills.slice(0, 8).map((skill, index) => (
                          <span
                            key={index}
                            className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                        {candidate.skills.length > 8 && (
                          <span className="text-gray-500 text-sm px-3 py-1">
                            +{candidate.skills.length - 8} more
                          </span>
                        )}
                      </div>
                    )}

                    {/* Match Score */}
                    {candidate.match_score !== null && candidate.match_score !== undefined && (
                      <div className="flex items-center mb-4">
                        <TrendingUp className="h-5 w-5 mr-2 text-gray-600" />
                        <span className="text-gray-700 mr-2">Job Match Score:</span>
                        <span className={`font-bold px-3 py-1 rounded-full ${getMatchScoreColor(candidate.match_score)}`}>
                          {candidate.match_score}%
                        </span>
                      </div>
                    )}

                    {/* Profile Links */}
                    <div className="flex gap-4">
                      {candidate.linkedin_url && (
                        <a
                          href={candidate.linkedin_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 flex items-center text-sm"
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          LinkedIn
                        </a>
                      )}
                      {candidate.github_url && (
                        <a
                          href={candidate.github_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-gray-800 hover:text-gray-900 flex items-center text-sm"
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          GitHub
                        </a>
                      )}
                    </div>
                  </div>

                  <Link
                    to={`/candidate/${candidate.id}`}
                    className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 transition-colors ml-4"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CandidatesPage;
