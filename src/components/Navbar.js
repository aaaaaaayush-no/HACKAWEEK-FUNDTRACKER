import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, role, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getDashboardLink = () => {
    switch (role) {
      case 'CONTRACTOR':
        return '/contractor';
      case 'GOVERNMENT':
        return '/government';
      case 'AUDITOR':
        return '/audit-log';
      default:
        return '/';
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <h2>Government Fund Tracker</h2>
          <span className="subtitle">Transparency in Public Infrastructure</span>
        </Link>

        <button 
          className="mobile-menu-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          ☰
        </button>

        <div className={`navbar-links ${mobileMenuOpen ? 'active' : ''}`}>
          <Link to="/" onClick={() => setMobileMenuOpen(false)}>Home</Link>
          
          {isAuthenticated() ? (
            <>
              <Link to={getDashboardLink()} onClick={() => setMobileMenuOpen(false)}>
                Dashboard
              </Link>
              
              {role === 'AUDITOR' && (
                <Link to="/audit-log" onClick={() => setMobileMenuOpen(false)}>
                  Audit Log
                </Link>
              )}
              
              <div className="navbar-user">
                <span className="user-badge">{user?.username} ({role})</span>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setMobileMenuOpen(false)}>Login</Link>
              <Link to="/register" onClick={() => setMobileMenuOpen(false)}>Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
