import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getIssues, verifyIssue, forgiveIssue, penalizeIssue, createIssue } from '../api/issues.api';
import { getProjects } from '../api/projects.api';

function IssueManagement() {
  const [issues, setIssues] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [forgiveReason, setForgiveReason] = useState('');
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [newIssue, setNewIssue] = useState({
    project: '',
    title: '',
    description: '',
    issue_type: 'CONTRACTOR_FAULT',
    severity: 'MEDIUM'
  });
  const { role } = useAuth();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [issuesData, projectsData] = await Promise.all([
        getIssues(),
        getProjects()
      ]);
      setIssues(issuesData);
      setProjects(projectsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (issueId) => {
    try {
      await verifyIssue(issueId);
      setMessage('Issue verified successfully!');
      fetchData();
    } catch (error) {
      setMessage('Error verifying issue.');
      console.error(error);
    }
  };

  const handleForgive = async (issueId) => {
    try {
      await forgiveIssue(issueId, forgiveReason);
      setMessage('Issue forgiven successfully!');
      setForgiveReason('');
      setSelectedIssue(null);
      fetchData();
    } catch (error) {
      setMessage(error.response?.data?.error || 'Error forgiving issue.');
      console.error(error);
    }
  };

  const handlePenalize = async (issueId) => {
    if (!window.confirm('Are you sure you want to penalize the contractor for this issue?')) {
      return;
    }
    try {
      const result = await penalizeIssue(issueId);
      setMessage(`Contractor penalized! Rating impact: -${result.penalty_applied}. New rating: ${result.new_contractor_rating}`);
      fetchData();
    } catch (error) {
      setMessage(error.response?.data?.error || 'Error penalizing contractor.');
      console.error(error);
    }
  };

  const handleCreateIssue = async (e) => {
    e.preventDefault();
    try {
      await createIssue(newIssue);
      setMessage('Issue reported successfully!');
      setShowCreateForm(false);
      setNewIssue({
        project: '',
        title: '',
        description: '',
        issue_type: 'CONTRACTOR_FAULT',
        severity: 'MEDIUM'
      });
      fetchData();
    } catch (error) {
      setMessage('Error creating issue report.');
      console.error(error);
    }
  };

  const getProjectName = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    return project ? project.name : 'Unknown Project';
  };

  const getStatusColor = (status) => {
    const colors = {
      'REPORTED': '#f59e0b',
      'UNDER_REVIEW': '#3b82f6',
      'VERIFIED': '#8b5cf6',
      'FORGIVEN': '#10b981',
      'PENALIZED': '#ef4444',
      'RESOLVED': '#10b981',
      'CLOSED': '#6b7280'
    };
    return colors[status] || '#6b7280';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      'LOW': '#10b981',
      'MEDIUM': '#f59e0b',
      'HIGH': '#ef4444',
      'CRITICAL': '#7f1d1d'
    };
    return colors[severity] || '#6b7280';
  };

  if (loading) return <div className="loading">Loading issues...</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      <div className="dashboard-header">
        <h2>Issue Management</h2>
        <p className="subtitle">Report and manage project issues</p>
      </div>

      {message && (
        <div className={message.includes('Error') ? 'error-message' : 'success-message'}>
          {message}
        </div>
      )}

      {/* Stats */}
      <div className="stats-container" style={{ marginBottom: '30px' }}>
        <div className="stat-card">
          <h3>{issues.length}</h3>
          <p>Total Issues</p>
        </div>
        <div className="stat-card">
          <h3>{issues.filter(i => i.status === 'REPORTED' || i.status === 'UNDER_REVIEW').length}</h3>
          <p>Pending Review</p>
        </div>
        <div className="stat-card">
          <h3>{issues.filter(i => i.is_forgiven).length}</h3>
          <p>Forgiven</p>
        </div>
        <div className="stat-card">
          <h3>{issues.filter(i => i.status === 'PENALIZED').length}</h3>
          <p>Penalized</p>
        </div>
      </div>

      {/* Create Issue Button */}
      <button 
        className="submit-btn" 
        onClick={() => setShowCreateForm(!showCreateForm)}
        style={{ marginBottom: '20px' }}
      >
        {showCreateForm ? 'Cancel' : '+ Report New Issue'}
      </button>

      {/* Create Issue Form */}
      {showCreateForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>Report New Issue</h3>
          <form onSubmit={handleCreateIssue}>
            <div className="form-group">
              <label>Project</label>
              <select
                value={newIssue.project}
                onChange={(e) => setNewIssue({ ...newIssue, project: e.target.value })}
                required
              >
                <option value="">Select a project</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>{project.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={newIssue.title}
                onChange={(e) => setNewIssue({ ...newIssue, title: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={newIssue.description}
                onChange={(e) => setNewIssue({ ...newIssue, description: e.target.value })}
                rows="4"
                required
              ></textarea>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label>Issue Type</label>
                <select
                  value={newIssue.issue_type}
                  onChange={(e) => setNewIssue({ ...newIssue, issue_type: e.target.value })}
                >
                  <option value="NATURAL_DISASTER">Natural Disaster</option>
                  <option value="CONTRACTOR_FAULT">Contractor Fault</option>
                  <option value="DESIGN_FLAW">Design Flaw</option>
                  <option value="MATERIAL_DEFECT">Material Defect</option>
                  <option value="VANDALISM">Vandalism</option>
                  <option value="NORMAL_WEAR">Normal Wear and Tear</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label>Severity</label>
                <select
                  value={newIssue.severity}
                  onChange={(e) => setNewIssue({ ...newIssue, severity: e.target.value })}
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
            </div>
            <button type="submit" className="submit-btn">Submit Report</button>
          </form>
        </div>
      )}

      {/* Forgive Modal */}
      {selectedIssue && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div className="card" style={{ maxWidth: '500px', width: '90%' }}>
            <h3>Forgive Issue</h3>
            <p>Provide a reason for forgiving this issue:</p>
            <div className="form-group">
              <textarea
                value={forgiveReason}
                onChange={(e) => setForgiveReason(e.target.value)}
                rows="4"
                placeholder="e.g., Natural disaster verified - earthquake damage"
                required
              ></textarea>
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button 
                className="approve-btn"
                onClick={() => handleForgive(selectedIssue.id)}
              >
                Confirm Forgive
              </button>
              <button 
                className="reject-btn"
                onClick={() => { setSelectedIssue(null); setForgiveReason(''); }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Issues List */}
      {issues.length === 0 ? (
        <div className="card">
          <p>No issues reported yet.</p>
        </div>
      ) : (
        <div className="card">
          <h3>All Issues</h3>
          <div className="approval-list">
            {issues.map((issue) => (
              <div key={issue.id} className="approval-card">
                <div className="approval-header">
                  <h4>{issue.title}</h4>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <span 
                      className="status-badge" 
                      style={{ backgroundColor: getSeverityColor(issue.severity), color: 'white' }}
                    >
                      {issue.severity}
                    </span>
                    <span 
                      className="status-badge" 
                      style={{ backgroundColor: getStatusColor(issue.status), color: 'white' }}
                    >
                      {issue.status}
                    </span>
                  </div>
                </div>
                
                <div className="approval-details">
                  <p><strong>Project:</strong> {getProjectName(issue.project)}</p>
                  <p><strong>Type:</strong> {issue.issue_type.replace('_', ' ')}</p>
                  <p><strong>Description:</strong> {issue.description}</p>
                  <p><strong>Reported:</strong> {new Date(issue.reported_at).toLocaleString()}</p>
                  
                  {issue.is_forgivable && (
                    <p style={{ color: '#10b981' }}>
                      <strong>✅ Forgivable:</strong> This issue type can be forgiven
                    </p>
                  )}
                  
                  {issue.is_forgiven && (
                    <div style={{ backgroundColor: '#f0fdf4', padding: '10px', borderRadius: '6px', marginTop: '10px' }}>
                      <p><strong>Forgiven Reason:</strong> {issue.forgiveness_reason}</p>
                      <p><strong>Forgiven at:</strong> {new Date(issue.forgiven_at).toLocaleString()}</p>
                    </div>
                  )}
                  
                  {issue.rating_impact && (
                    <p style={{ color: '#ef4444' }}>
                      <strong>Rating Impact:</strong> -{issue.rating_impact} points
                    </p>
                  )}
                </div>

                {role === 'GOVERNMENT' && issue.status !== 'FORGIVEN' && issue.status !== 'PENALIZED' && issue.status !== 'CLOSED' && (
                  <div className="approval-actions">
                    {issue.status === 'REPORTED' && (
                      <button 
                        className="submit-btn"
                        onClick={() => handleVerify(issue.id)}
                        style={{ backgroundColor: '#8b5cf6' }}
                      >
                        Verify
                      </button>
                    )}
                    {issue.is_forgivable && !issue.is_forgiven && (
                      <button 
                        className="approve-btn"
                        onClick={() => setSelectedIssue(issue)}
                      >
                        Forgive
                      </button>
                    )}
                    {issue.issue_type === 'CONTRACTOR_FAULT' && !issue.is_forgiven && (
                      <button 
                        className="reject-btn"
                        onClick={() => handlePenalize(issue.id)}
                      >
                        Penalize Contractor
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default IssueManagement;
