import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getProjectById } from "../api/projects.api";
import ProgressBar from "../components/ProgressBar";

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const { role } = useAuth();

  useEffect(() => {
    fetchProject();
  }, [id]);

  const fetchProject = async () => {
    try {
      const data = await getProjectById(id);
      setProject(data);
    } catch (error) {
      console.error('Error fetching project:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading project details...</div>;
  if (!project) return <div className="loading">Project not found.</div>;

  const totalFunds = project.funds?.reduce((sum, fund) => sum + parseFloat(fund.amount), 0) || 0;
  const latestProgress = project.progress?.[project.progress.length - 1];
  const progressPercentage = latestProgress?.physical_progress || 0;

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="card" style={{ marginBottom: '20px' }}>
        <h1>{project.name}</h1>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginTop: '20px' }}>
          <div>
            <p><strong>Location:</strong> {project.location}</p>
            <p><strong>Ministry:</strong> {project.ministry}</p>
            <p><strong>Contractor:</strong> {project.contractor}</p>
          </div>
          <div>
            <p><strong>Total Budget:</strong> ₹{parseFloat(project.total_budget).toLocaleString()}</p>
            <p><strong>Funds Released:</strong> ₹{totalFunds.toLocaleString()}</p>
            <p><strong>Start Date:</strong> {project.start_date}</p>
            <p><strong>End Date:</strong> {project.end_date}</p>
          </div>
        </div>

        <div style={{ marginTop: '30px' }}>
          <h3>Project Progress</h3>
          <ProgressBar percentage={progressPercentage} height="30px" />
        </div>
      </div>

      {project.progress && project.progress.length > 0 && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>Progress Timeline</h3>
          <div className="audit-timeline">
            {project.progress.slice().reverse().map((prog, idx) => (
              <div key={idx} className="audit-item">
                <div className="audit-marker" style={{ 
                  backgroundColor: prog.status === 'APPROVED' ? '#10b981' : 
                                 prog.status === 'REJECTED' ? '#ef4444' : '#f59e0b' 
                }}></div>
                <div className="audit-content">
                  <div className="audit-header">
                    <span><strong>Progress Update</strong></span>
                    <span className={`status-badge status-${prog.status?.toLowerCase() || 'pending'}`}>
                      {prog.status || 'PENDING'}
                    </span>
                  </div>
                  <div className="audit-details">
                    <p><strong>Date:</strong> {new Date(prog.date).toLocaleDateString()}</p>
                    <p><strong>Physical Progress:</strong> {prog.physical_progress}%</p>
                    <p><strong>Financial Progress:</strong> {prog.financial_progress}%</p>
                    {prog.submitted_by_username && (
                      <p><strong>Submitted by:</strong> {prog.submitted_by_username}</p>
                    )}
                    {prog.reviewed_by_username && (
                      <p><strong>Reviewed by:</strong> {prog.reviewed_by_username} on {new Date(prog.reviewed_at).toLocaleDateString()}</p>
                    )}
                    
                    {prog.images && prog.images.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <strong>Evidence Images:</strong>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '10px', marginTop: '10px' }}>
                          {prog.images.map((img, imgIdx) => (
                            <img 
                              key={imgIdx} 
                              src={img.image} 
                              alt={`Progress ${imgIdx + 1}`}
                              style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: '6px' }}
                            />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {project.funds && project.funds.length > 0 && (
        <div className="card">
          <h3>Fund Release History</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
            <thead>
              <tr style={{ backgroundColor: '#f3f4f6', textAlign: 'left' }}>
                <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Amount</th>
                <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Released At</th>
              </tr>
            </thead>
            <tbody>
              {project.funds.map((fund, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '12px' }}>₹{parseFloat(fund.amount).toLocaleString()}</td>
                  <td style={{ padding: '12px' }}>{new Date(fund.released_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ProjectDetail;
