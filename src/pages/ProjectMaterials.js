import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getProjectMaterials, verifyMaterial } from '../api/materials.api';

function ProjectMaterials() {
  const { id } = useParams();
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const { role } = useAuth();

  useEffect(() => {
    fetchMaterials();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchMaterials = async () => {
    try {
      const data = await getProjectMaterials(id);
      setMaterials(data);
    } catch (error) {
      console.error('Error fetching materials:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (materialId) => {
    try {
      await verifyMaterial(materialId);
      setMessage('Material verified successfully!');
      fetchMaterials();
    } catch (error) {
      setMessage('Error verifying material.');
      console.error(error);
    }
  };

  const calculateTotals = () => {
    const totalPlanned = materials.reduce((sum, m) => sum + parseFloat(m.total_planned_cost || 0), 0);
    const totalActual = materials.reduce((sum, m) => sum + parseFloat(m.total_actual_cost || 0), 0);
    return { totalPlanned, totalActual };
  };

  if (loading) return <div className="loading">Loading materials...</div>;

  const { totalPlanned, totalActual } = calculateTotals();

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      <div className="dashboard-header">
        <h2>Material Transparency</h2>
        <p className="subtitle">Project Materials & Pricing Details</p>
        <a href={`/projects/${id}`} style={{ color: '#3b82f6' }}>← Back to Project</a>
      </div>

      {message && <div className="success-message">{message}</div>}

      {/* Summary Stats */}
      <div className="stats-container" style={{ marginBottom: '30px' }}>
        <div className="stat-card">
          <h3>{materials.length}</h3>
          <p>Total Materials</p>
        </div>
        <div className="stat-card">
          <h3>₹{totalPlanned.toLocaleString()}</h3>
          <p>Total Planned Cost</p>
        </div>
        <div className="stat-card">
          <h3>₹{totalActual.toLocaleString()}</h3>
          <p>Total Actual Cost</p>
        </div>
        <div className="stat-card">
          <h3 style={{ color: totalActual - totalPlanned > 0 ? '#ef4444' : '#10b981' }}>
            {totalActual - totalPlanned > 0 ? '+' : ''}₹{(totalActual - totalPlanned).toLocaleString()}
          </h3>
          <p>Cost Variance</p>
        </div>
      </div>

      {materials.length === 0 ? (
        <div className="card">
          <p>No materials recorded for this project yet.</p>
        </div>
      ) : (
        <div className="card">
          <h3>Material Details</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
              <thead>
                <tr style={{ backgroundColor: '#f3f4f6', textAlign: 'left' }}>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Material</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Unit</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Unit Price</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Planned Qty</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Actual Qty</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Planned Cost</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Actual Cost</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Supplier</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Grade</th>
                  <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Status</th>
                  {role === 'GOVERNMENT' && (
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Actions</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {materials.map((material) => {
                  const variance = material.total_actual_cost 
                    ? parseFloat(material.total_actual_cost) - parseFloat(material.total_planned_cost)
                    : null;
                  
                  return (
                    <tr key={material.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                      <td style={{ padding: '12px' }}>
                        <strong>{material.name}</strong>
                        {material.description && (
                          <p style={{ fontSize: '12px', color: '#6b7280', margin: '4px 0 0' }}>
                            {material.description}
                          </p>
                        )}
                      </td>
                      <td style={{ padding: '12px' }}>{material.unit}</td>
                      <td style={{ padding: '12px' }}>₹{parseFloat(material.unit_price).toLocaleString()}</td>
                      <td style={{ padding: '12px' }}>{parseFloat(material.planned_quantity).toLocaleString()}</td>
                      <td style={{ padding: '12px' }}>
                        {material.actual_quantity 
                          ? parseFloat(material.actual_quantity).toLocaleString() 
                          : '-'}
                      </td>
                      <td style={{ padding: '12px' }}>₹{parseFloat(material.total_planned_cost).toLocaleString()}</td>
                      <td style={{ padding: '12px' }}>
                        {material.total_actual_cost 
                          ? `₹${parseFloat(material.total_actual_cost).toLocaleString()}`
                          : '-'}
                        {variance !== null && (
                          <span style={{ 
                            display: 'block', 
                            fontSize: '12px', 
                            color: variance > 0 ? '#ef4444' : '#10b981' 
                          }}>
                            ({variance > 0 ? '+' : ''}₹{variance.toLocaleString()})
                          </span>
                        )}
                      </td>
                      <td style={{ padding: '12px' }}>{material.supplier_name || '-'}</td>
                      <td style={{ padding: '12px' }}>{material.quality_grade || '-'}</td>
                      <td style={{ padding: '12px' }}>
                        <span className={`status-badge ${material.verified ? 'status-approved' : 'status-pending'}`}>
                          {material.verified ? 'Verified' : 'Unverified'}
                        </span>
                      </td>
                      {role === 'GOVERNMENT' && (
                        <td style={{ padding: '12px' }}>
                          {!material.verified && (
                            <button 
                              className="approve-btn"
                              onClick={() => handleVerify(material.id)}
                              style={{ padding: '6px 12px', fontSize: '12px' }}
                            >
                              Verify
                            </button>
                          )}
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectMaterials;
