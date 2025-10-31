import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, Users, Brain, Calendar, FileCheck, TrendingUp } from 'lucide-react';

function HomePage() {
  const features = [
    {
      icon: Upload,
      title: 'Resume Upload & Parsing',
      description: 'Upload PDF, DOCX, or TXT resumes and automatically extract candidate information',
      color: 'bg-blue-500',
    },
    {
      icon: TrendingUp,
      title: 'Job Match Scoring',
      description: 'AI-powered semantic matching between resumes and job descriptions',
      color: 'bg-green-500',
    },
    {
      icon: Brain,
      title: 'Profile Intelligence',
      description: 'Enrich profiles with data from LinkedIn, GitHub, and other professional networks',
      color: 'bg-purple-500',
    },
    {
      icon: Calendar,
      title: 'Interview Scheduling',
      description: 'Smart scheduling assistant that suggests optimal interview time slots',
      color: 'bg-orange-500',
    },
    {
      icon: FileCheck,
      title: 'Feedback Summarization',
      description: 'AI-powered interview feedback analysis and structured summaries',
      color: 'bg-pink-500',
    },
    {
      icon: Users,
      title: 'Human-in-the-Loop',
      description: 'Recruiter dashboard for reviewing, approving, and editing AI-generated insights',
      color: 'bg-indigo-500',
    },
  ];

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg shadow-xl p-12 mb-8 text-white">
        <h1 className="text-5xl font-bold mb-4">Welcome to HireWise</h1>
        <p className="text-xl mb-8 text-primary-100">
          AI-Powered Recruiting Assistant with Human-in-the-Loop Decision Making
        </p>
        <div className="flex space-x-4">
          <Link
            to="/upload"
            className="bg-white text-primary-700 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors shadow-lg"
          >
            Upload Resume
          </Link>
          <Link
            to="/candidates"
            className="bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-800 transition-colors border-2 border-white"
          >
            View Candidates
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
              >
                <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">How It Works</h2>
        <div className="space-y-6">
          <div className="flex items-start">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4 flex-shrink-0">
              1
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Upload Resume</h3>
              <p className="text-gray-600">
                Upload candidate resumes in PDF, DOCX, or TXT format. Our AI parser automatically extracts key information.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4 flex-shrink-0">
              2
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">AI Analysis</h3>
              <p className="text-gray-600">
                Our AI agents analyze the resume, compute job match scores, and enrich profiles with data from LinkedIn and GitHub.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4 flex-shrink-0">
              3
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Human Review</h3>
              <p className="text-gray-600">
                Recruiters review AI-generated insights, make final decisions, and can edit or approve candidate profiles.
              </p>
            </div>
          </div>
          
          <div className="flex items-start">
            <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4 flex-shrink-0">
              4
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-1">Schedule & Feedback</h3>
              <p className="text-gray-600">
                Schedule interviews with suggested time slots and generate structured feedback summaries after interviews.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
