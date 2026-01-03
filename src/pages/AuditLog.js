import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getAuditLogs } from '../api/audit.api';

function AuditLog() {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const { user } = useAuth();

  useEffect(() => {
    fetchAuditLogs();
  }, []);

  const fetchAuditLogs = async () => {
    try {
      const data = await getAuditLogs();
      setAuditLogs(data);
    } catch (error) {
      console.error('Error fetching audit logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = filter === 'all' 
    ? auditLogs 
    : auditLogs.filter(log => log.action === filter);

  const getActionColor = (action) => {
    switch (action) {
      case 'CREATE': return '#10b981';
      case 'UPDATE': return '#3b82f6';
      case 'DELETE': return '#ef4444';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return <div className="loading">Loading audit logs...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <div className="dashboard-header">
        <h2>Audit Log</h2>
        <p className="subtitle">Complete system activity trail</p>
      </div>

      <div className="filter-container">
        <label>Filter by action: </label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="filter-select">
          <option value="all">All Actions</option>
          <option value="CREATE">Create</option>
          <option value="UPDATE">Update</option>
          <option value="DELETE">Delete</option>
        </select>
      </div>

      {filteredLogs.length === 0 ? (
        <p>No audit logs found.</p>
      ) : (
        <div className="audit-timeline">
          {filteredLogs.map((log) => (
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
      )}
    </div>
  );
}

export default AuditLog;
