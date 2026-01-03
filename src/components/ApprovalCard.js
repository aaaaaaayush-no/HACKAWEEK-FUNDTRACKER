import React from 'react';

function ApprovalCard({ progress, onApprove, onReject, projectName }) {
  return (
    <div className="approval-card">
      <div className="approval-header">
        <h4>{projectName}</h4>
        <span className="status-badge status-pending">{progress.status || 'Pending'}</span>
      </div>
      
      <div className="approval-details">
        <p><strong>Submitted by:</strong> {progress.submitted_by_username || 'Unknown'}</p>
        <p><strong>Date:</strong> {new Date(progress.date).toLocaleDateString()}</p>
        <p><strong>Physical Progress:</strong> {progress.physical_progress}%</p>
        <p><strong>Financial Progress:</strong> {progress.financial_progress}%</p>
      </div>

      <div className="approval-actions">
        <button 
          className="approve-btn"
          onClick={() => onApprove(progress.id)}
        >
          Approve
        </button>
        <button 
          className="reject-btn"
          onClick={() => onReject(progress.id)}
        >
          Reject
        </button>
      </div>
    </div>
  );
}

export default ApprovalCard;
