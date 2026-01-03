import React from 'react';

function AuditTimeline({ logs }) {
  const getActionColor = (action) => {
    switch (action) {
      case 'CREATE': return '#10b981';
      case 'UPDATE': return '#3b82f6';
      case 'DELETE': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="audit-timeline">
      {logs.map((log) => (
        <div key={log.id} className="audit-item">
          <div className="audit-marker" style={{ backgroundColor: getActionColor(log.action) }}></div>
          <div className="audit-content">
            <div className="audit-header">
              <span className="audit-action" style={{ color: getActionColor(log.action) }}>
                {log.action}
              </span>
              <span className="audit-time">
                {new Date(log.timestamp).toLocaleString()}
              </span>
            </div>
            <div className="audit-details">
              <p><strong>User:</strong> {log.username || 'System'}</p>
              <p><strong>Model:</strong> {log.model_name}</p>
              <p><strong>Object ID:</strong> {log.object_id}</p>
              {log.description && (
                <p className="audit-description">{log.description}</p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default AuditTimeline;
