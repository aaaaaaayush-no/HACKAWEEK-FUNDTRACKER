import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getProjects } from "../api/projects.api";
import { submitProgress } from "../api/progress.api";
import { getContractorProfiles } from "../api/contractor.api";

const ContractorDashboard = () => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [contractorProfile, setContractorProfile] = useState(null);
  const [progressData, setProgressData] = useState({
    physical_progress: '',
    financial_progress: '',
    images: []
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchProjects();
    fetchContractorProfile();
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchContractorProfile = async () => {
    try {
      const profiles = await getContractorProfiles();
      if (profiles && profiles.length > 0) {
        setContractorProfile(profiles[0]);
      }
    } catch (error) {
      console.error('Error fetching contractor profile:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      await submitProgress(selectedProject, progressData);
      setMessage('Progress submitted successfully! Awaiting approval.');
      setProgressData({ physical_progress: '', financial_progress: '', images: [] });
      setSelectedProject(null);
      fetchProjects();
    } catch (error) {
      setMessage('Error submitting progress. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (e) => {
    setProgressData({
      ...progressData,
      images: Array.from(e.target.files)
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <div className="dashboard-header">
        <h2>Contractor Dashboard</h2>
        <p className="subtitle">Welcome, {user?.username}</p>
      </div>

      {/* Contractor Profile Summary */}
      {contractorProfile && (
        <div className="stats-container" style={{ marginBottom: '30px' }}>
          <div className="stat-card">
            <h3 style={{ color: contractorProfile.rating >= 3.8 ? '#10b981' : '#ef4444' }}>
              {parseFloat(contractorProfile.rating).toFixed(2)}
            </h3>
            <p>Current Rating</p>
          </div>
          <div className="stat-card">
            <h3>{contractorProfile.total_projects_completed}</h3>
            <p>Completed Projects</p>
          </div>
          <div className="stat-card">
            <h3>{contractorProfile.is_suspended ? '⚠️ Yes' : '✅ No'}</h3>
            <p>Suspended</p>
          </div>
          <div className="stat-card">
            <Link to="/contractor/profile" className="submit-btn" style={{ textDecoration: 'none' }}>
              View Full Profile
            </Link>
          </div>
        </div>
      )}

      {/* Suspension Warning */}
      {contractorProfile?.is_suspended && (
        <div className="error-message" style={{ marginBottom: '20px' }}>
          <h3>⚠️ Account Suspended</h3>
          <p><strong>Reason:</strong> {contractorProfile.suspension_reason}</p>
          <p>You cannot submit progress updates while suspended.</p>
        </div>
      )}

      <div className="progress-form-container">
        <h3>Submit Progress Update</h3>
        <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '15px' }}>
          ⏰ Note: Progress reports can only be submitted after 5:00 PM
        </p>
        {message && <div className={message.includes('Error') ? 'error-message' : 'success-message'}>{message}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="project">Select Project</label>
            <select
              id="project"
              value={selectedProject || ''}
              onChange={(e) => setSelectedProject(e.target.value)}
              required
            >
              <option value="">-- Select a Project --</option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="physical_progress">Physical Progress (%)</label>
            <input
              type="number"
              id="physical_progress"
              min="0"
              max="100"
              value={progressData.physical_progress}
              onChange={(e) => setProgressData({ ...progressData, physical_progress: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="financial_progress">Financial Progress (%)</label>
            <input
              type="number"
              id="financial_progress"
              min="0"
              max="100"
              value={progressData.financial_progress}
              onChange={(e) => setProgressData({ ...progressData, financial_progress: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="images">Upload Evidence Images</label>
            <input
              type="file"
              id="images"
              multiple
              accept="image/*"
              onChange={handleImageChange}
            />
            <small>You can upload multiple images</small>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Progress'}
          </button>
        </form>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h3>My Projects</h3>
        <div className="project-grid">
          {projects.map((project) => (
            <div key={project.id} className="card">
              <h3>{project.name}</h3>
              <p><strong>Location:</strong> {project.location}</p>
              <p><strong>Budget:</strong> ₹{parseFloat(project.total_budget).toLocaleString()}</p>
              
              {project.progress && project.progress.length > 0 && (
                <div className="progress-history">
                  <h4>Recent Submissions:</h4>
                  {project.progress.slice(-3).map((prog, idx) => (
                    <div key={idx} className="progress-item">
                      <p>Physical: {prog.physical_progress}% | Financial: {prog.financial_progress}%</p>
                      <p className={`status-badge status-${prog.status?.toLowerCase()}`}>
                        Status: {prog.status || 'PENDING'}
                      </p>
                    </div>
                  ))}
                </div>
              )}
              
              <a href={`/projects/${project.id}`}>View Details</a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ContractorDashboard;
