import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  getContractorProfiles, 
  checkContractorEligibility,
  getContractorCertificates,
  getContractorSkills
} from '../api/contractor.api';

function ContractorProfile() {
  const [profile, setProfile] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchContractorData();
  }, []);

  const fetchContractorData = async () => {
    try {
      const profiles = await getContractorProfiles();
      if (profiles && profiles.length > 0) {
        const myProfile = profiles[0];
        setProfile(myProfile);
        
        // Fetch eligibility
        const eligibilityData = await checkContractorEligibility(myProfile.id);
        setEligibility(eligibilityData);
      }
      
      // Fetch certificates and skills
      const certsData = await getContractorCertificates();
      setCertificates(certsData);
      
      const skillsData = await getContractorSkills();
      setSkills(skillsData);
    } catch (error) {
      console.error('Error fetching contractor data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading contractor profile...</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div className="dashboard-header">
        <h2>Contractor Profile</h2>
        <p className="subtitle">Welcome, {user?.username}</p>
      </div>

      {profile ? (
        <>
          {/* Suspension Warning */}
          {profile.is_suspended && (
            <div className="error-message" style={{ marginBottom: '20px' }}>
              <h3>⚠️ Account Suspended</h3>
              <p><strong>Reason:</strong> {profile.suspension_reason}</p>
              <p><strong>Suspended on:</strong> {new Date(profile.suspended_at).toLocaleString()}</p>
            </div>
          )}

          {/* Rating Card */}
          <div className="card" style={{ marginBottom: '20px' }}>
            <h3>Rating & Performance</h3>
            <div className="stats-container">
              <div className="stat-card">
                <h3>{parseFloat(profile.rating || 0).toFixed(2)}</h3>
                <p>Current Rating</p>
                <div className="progress-bar-container" style={{ marginTop: '10px' }}>
                  <div 
                    className="progress-bar-fill" 
                    style={{ 
                      width: `${(parseFloat(profile.rating || 0) / 5) * 100}%`,
                      backgroundColor: parseFloat(profile.rating || 0) >= 3.8 ? '#10b981' : '#ef4444'
                    }}
                  ></div>
                </div>
              </div>
              <div className="stat-card">
                <h3>{profile.total_projects_completed || 0}</h3>
                <p>Projects Completed</p>
              </div>
              <div className="stat-card">
                <h3>{profile.total_projects_failed || 0}</h3>
                <p>Projects Failed</p>
              </div>
              <div className="stat-card">
                <h3>{profile.years_of_experience || 0}</h3>
                <p>Years Experience</p>
              </div>
            </div>

            {/* AI Rating (if available) */}
            {profile.ai_rating && (
              <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f9ff', borderRadius: '8px' }}>
                <p><strong>🤖 AI Rating:</strong> {parseFloat(profile.ai_rating || 0).toFixed(2)}</p>
                {profile.ai_risk_score && (
                  <p><strong>📊 AI Risk Score:</strong> {parseFloat(profile.ai_risk_score || 0).toFixed(2)}%</p>
                )}
              </div>
            )}
          </div>

          {/* Eligibility Card */}
          {eligibility && (
            <div className="card" style={{ marginBottom: '20px' }}>
              <h3>Contract Eligibility</h3>
              <div className="project-grid">
                {Object.entries(eligibility.eligibility).map(([size, result]) => (
                  <div 
                    key={size} 
                    className="card" 
                    style={{ 
                      backgroundColor: result.eligible ? '#f0fdf4' : '#fef2f2',
                      borderLeft: `4px solid ${result.eligible ? '#10b981' : '#ef4444'}`
                    }}
                  >
                    <h4>{size} Contracts</h4>
                    <p className={`status-badge ${result.eligible ? 'status-approved' : 'status-rejected'}`}>
                      {result.eligible ? '✅ Eligible' : '❌ Not Eligible'}
                    </p>
                    <p style={{ marginTop: '10px', fontSize: '14px', color: '#6b7280' }}>
                      {result.reason}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Certificates */}
          <div className="card" style={{ marginBottom: '20px' }}>
            <h3>Certificates</h3>
            {certificates.length === 0 ? (
              <p>No certificates uploaded yet.</p>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f3f4f6', textAlign: 'left' }}>
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Certificate</th>
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Issuing Authority</th>
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Issue Date</th>
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Expiry</th>
                    <th style={{ padding: '12px', borderBottom: '2px solid #e5e7eb' }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {certificates.map((cert) => (
                    <tr key={cert.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                      <td style={{ padding: '12px' }}>{cert.name}</td>
                      <td style={{ padding: '12px' }}>{cert.issuing_authority}</td>
                      <td style={{ padding: '12px' }}>{cert.issue_date}</td>
                      <td style={{ padding: '12px' }}>{cert.expiry_date || 'N/A'}</td>
                      <td style={{ padding: '12px' }}>
                        <span className={`status-badge ${cert.verified ? 'status-approved' : 'status-pending'}`}>
                          {cert.verified ? 'Verified' : 'Pending'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Skills */}
          <div className="card">
            <h3>Skills</h3>
            {skills.length === 0 ? (
              <p>No skills recorded yet.</p>
            ) : (
              <div className="project-grid">
                {skills.map((skill) => (
                  <div key={skill.id} className="card" style={{ textAlign: 'center' }}>
                    <h4>{skill.skill_name}</h4>
                    <div style={{ marginTop: '10px' }}>
                      <p>Proficiency Level</p>
                      <div className="progress-bar-container">
                        <div 
                          className="progress-bar-fill" 
                          style={{ width: `${skill.proficiency_level * 10}%` }}
                        ></div>
                      </div>
                      <span>{skill.proficiency_level}/10</span>
                    </div>
                    <p style={{ marginTop: '10px', fontSize: '14px', color: '#6b7280' }}>
                      {skill.years_of_practice} years practice
                    </p>
                    <span className={`status-badge ${skill.verified ? 'status-approved' : 'status-pending'}`}>
                      {skill.verified ? 'Verified' : 'Unverified'}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      ) : (
        <div className="card">
          <p>No contractor profile found. Please contact an administrator to set up your contractor profile.</p>
        </div>
      )}
    </div>
  );
}

export default ContractorProfile;
