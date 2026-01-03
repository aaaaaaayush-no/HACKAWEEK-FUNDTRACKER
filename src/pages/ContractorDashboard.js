import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getProjects } from "../api/projects.api";
import { submitProgress } from "../api/progress.api";

const ContractorDashboard = () => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
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
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Error fetching projects:', error);
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

      <div className="progress-form-container">
        <h3>Submit Progress Update</h3>
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
