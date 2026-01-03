import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getPendingProgress, approveProgress, rejectProgress } from '../api/progress.api';
import { getProjects } from '../api/projects.api';

function GovernmentDashboard() {
  const [pendingProgress, setPendingProgress] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [progressData, projectsData] = await Promise.all([
        getPendingProgress(),
        getProjects()
      ]);
      setPendingProgress(progressData);
      setProjects(projectsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (progressId) => {
    try {
      await approveProgress(progressId);
      setMessage('Progress approved successfully!');
      fetchData();
    } catch (error) {
      setMessage('Error approving progress.');
      console.error(error);
    }
  };

  const handleReject = async (progressId) => {
    try {
      await rejectProgress(progressId);
      setMessage('Progress rejected.');
      fetchData();
    } catch (error) {
      setMessage('Error rejecting progress.');
      console.error(error);
    }
  };

  const getProjectName = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    return project ? project.name : 'Unknown Project';
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <div className="dashboard-header">
        <h2>Government Dashboard</h2>
        <p className="subtitle">Welcome, {user?.username}</p>
      </div>

      {message && <div className="success-message">{message}</div>}

      <div className="stats-container">
        <div className="stat-card">
          <h3>{projects.length}</h3>
          <p>Total Projects</p>
        </div>
        <div className="stat-card">
          <h3>{pendingProgress.length}</h3>
          <p>Pending Approvals</p>
        </div>
      </div>

      <div style={{ marginTop: '30px' }}>
        <h3>Pending Progress Approvals</h3>
        {pendingProgress.length === 0 ? (
          <p>No pending approvals.</p>
        ) : (
          <div className="approval-list">
            {pendingProgress.map((progress) => (
              <div key={progress.id} className="approval-card">
                <div className="approval-header">
                  <h4>{getProjectName(progress.project)}</h4>
                  <span className="status-badge status-pending">Pending</span>
                </div>
                
                <div className="approval-details">
                  <p><strong>Submitted by:</strong> {progress.submitted_by_username || 'Unknown'}</p>
                  <p><strong>Date:</strong> {new Date(progress.date).toLocaleDateString()}</p>
                  <p><strong>Physical Progress:</strong> {progress.physical_progress}%</p>
                  <p><strong>Financial Progress:</strong> {progress.financial_progress}%</p>
                  
                  {progress.images && progress.images.length > 0 && (
                    <p><strong>Evidence Images:</strong> {progress.images.length} file(s)</p>
                  )}
                </div>

                <div className="approval-actions">
                  <button 
                    className="approve-btn"
                    onClick={() => handleApprove(progress.id)}
                  >
                    Approve
                  </button>
                  <button 
                    className="reject-btn"
                    onClick={() => handleReject(progress.id)}
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={{ marginTop: '40px' }}>
        <h3>All Projects Overview</h3>
        <div className="project-grid">
          {projects.map((project) => {
            const totalFunds = project.funds?.reduce((sum, fund) => sum + parseFloat(fund.amount), 0) || 0;
            const latestProgress = project.progress?.[project.progress.length - 1];
            
            return (
              <div key={project.id} className="card">
                <h3>{project.name}</h3>
                <p><strong>Location:</strong> {project.location}</p>
                <p><strong>Total Budget:</strong> ₹{parseFloat(project.total_budget).toLocaleString()}</p>
                <p><strong>Funds Released:</strong> ₹{totalFunds.toLocaleString()}</p>
                
                {latestProgress && (
                  <div className="progress-section">
                    <p><strong>Latest Progress:</strong> {latestProgress.physical_progress}%</p>
                    <div className="progress-bar-container">
                      <div 
                        className="progress-bar-fill" 
                        style={{ width: `${latestProgress.physical_progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
                
                <a href={`/projects/${project.id}`}>View Details</a>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default GovernmentDashboard;
