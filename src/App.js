import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Login from "./pages/Login";
import Register from "./pages/Register";
import PublicDashboard from "./pages/PublicDashboard";
import ContractorDashboard from "./pages/ContractorDashboard";
import ContractorProfile from "./pages/ContractorProfile";
import GovernmentDashboard from "./pages/GovernmentDashboard";
import AuditLog from "./pages/AuditLog";
import ProjectDetail from "./pages/ProjectDetail";
import ProjectMaterials from "./pages/ProjectMaterials";
import IssueManagement from "./pages/IssueManagement";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main style={{ minHeight: "calc(100vh - 200px)", padding: "20px" }}>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<PublicDashboard />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/projects/:id" element={<ProjectDetail />} />
              <Route path="/projects/:id/materials" element={<ProjectMaterials />} />

              {/* Protected routes */}
              <Route 
                path="/contractor" 
                element={
                  <ProtectedRoute requiredRole="CONTRACTOR">
                    <ContractorDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/contractor/profile" 
                element={
                  <ProtectedRoute requiredRole="CONTRACTOR">
                    <ContractorProfile />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/government" 
                element={
                  <ProtectedRoute requiredRole="GOVERNMENT">
                    <GovernmentDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/issues" 
                element={
                  <ProtectedRoute requiredRole="GOVERNMENT">
                    <IssueManagement />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/audit-log" 
                element={
                  <ProtectedRoute requiredRole="AUDITOR">
                    <AuditLog />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
