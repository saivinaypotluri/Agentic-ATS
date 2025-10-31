import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const candidateAPI = {
  // Upload resume
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload_resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get candidate by ID
  getCandidate: async (candidateId) => {
    const response = await api.get(`/get_candidate/${candidateId}`);
    return response.data;
  },

  // Get all candidates
  getAllCandidates: async () => {
    const response = await api.get('/get_all_candidates');
    return response.data;
  },

  // Update candidate
  updateCandidate: async (candidateId, updateData) => {
    const response = await api.put(`/update_candidate/${candidateId}`, updateData);
    return response.data;
  },

  // Approve/reject candidate
  approveCandidate: async (candidateId, approved) => {
    const response = await api.post('/approve_candidate', {
      candidate_id: candidateId,
      approved: approved,
    });
    return response.data;
  },

  // Delete candidate
  deleteCandidate: async (candidateId) => {
    const response = await api.delete(`/delete_candidate/${candidateId}`);
    return response.data;
  },
};

export const jobAPI = {
  // Match job
  matchJob: async (candidateId, jobDescription) => {
    const response = await api.post('/match_job', {
      candidate_id: candidateId,
      job_description: jobDescription,
    });
    return response.data;
  },

  // Fetch profiles (LinkedIn, GitHub, etc.)
  fetchProfiles: async (candidateId) => {
    const response = await api.post('/fetch_profiles', {
      candidate_id: candidateId,
    });
    return response.data;
  },

  // Schedule interview
  scheduleInterview: async (candidateId, interviewSlot = null) => {
    const response = await api.post('/schedule_interview', {
      candidate_id: candidateId,
      interview_slot: interviewSlot,
    });
    return response.data;
  },

  // Get interview slots
  getInterviewSlots: async (numSlots = 5) => {
    const response = await api.get('/get_interview_slots', {
      params: { num_slots: numSlots },
    });
    return response.data;
  },
};

export const feedbackAPI = {
  // Submit feedback
  submitFeedback: async (candidateId, interviewNotes) => {
    const response = await api.post('/feedback', {
      candidate_id: candidateId,
      interview_notes: interviewNotes,
    });
    return response.data;
  },

  // Get feedback
  getFeedback: async (candidateId) => {
    const response = await api.get(`/get_feedback/${candidateId}`);
    return response.data;
  },

  // Analyze sentiment
  analyzeSentiment: async (candidateId) => {
    const response = await api.get(`/analyze_sentiment/${candidateId}`);
    return response.data;
  },
};

export default api;
