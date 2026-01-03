import React, { useState, useEffect } from 'react';
import { getProjects } from '../api/projects.api';

function PublicDashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProjects = projects.filter(project =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.ministry.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const calculateProgress = (project) => {
    if (!project.progress || project.progress.length === 0) return 0;
    const latestProgress = project.progress[project.progress.length - 1];
    return latestProgress.physical_progress || 0;
  };

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <div className="dashboard-header">
        <h2>Public Dashboard</h2>
        <p className="subtitle">View all government funded projects</p>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search projects by name, location, or ministry..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {filteredProjects.length === 0 ? (
        <p>No projects found.</p>
      ) : (
        <div className="project-grid">
          {filteredProjects.map((project) => (
            <div key={project.id} className="card">
              <h3>{project.name}</h3>
              <p><strong>Location:</strong> {project.location}</p>
              <p><strong>Ministry:</strong> {project.ministry}</p>
              <p><strong>Contractor:</strong> {project.contractor}</p>
              <p><strong>Budget:</strong> ₹{parseFloat(project.total_budget).toLocaleString()}</p>
              <p><strong>Duration:</strong> {project.start_date} to {project.end_date}</p>
              
              <div className="progress-section">
                <p><strong>Progress: {calculateProgress(project)}%</strong></p>
                <div className="progress-bar-container">
                  <div 
                    className="progress-bar-fill" 
                    style={{ width: `${calculateProgress(project)}%` }}
                  ></div>
                </div>
              </div>
              
              <a href={`/projects/${project.id}`}>View Details</a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PublicDashboard;
