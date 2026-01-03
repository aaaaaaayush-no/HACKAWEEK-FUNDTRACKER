import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from '../api/axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load auth state from localStorage on mount
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    const storedRole = localStorage.getItem('role');

    if (storedToken && storedUser && storedRole) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      setRole(storedRole);
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
    setLoading(false);
  }, []);

  const login = (userData, tokens) => {
    const { access } = tokens;
    const userRole = userData.role;

    setUser(userData);
    setToken(access);
    setRole(userRole);

    // Persist to localStorage
    localStorage.setItem('token', access);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('role', userRole);

    // Set default authorization header
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setRole(null);

    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('role');

    delete axios.defaults.headers.common['Authorization'];
  };

  const isAuthenticated = () => {
    return !!token;
  };

  const value = {
    user,
    token,
    role,
    login,
    logout,
    isAuthenticated,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
