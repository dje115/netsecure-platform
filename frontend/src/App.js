import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Scans from './pages/Scans';
import Devices from './pages/Devices';
import Vulnerabilities from './pages/Vulnerabilities';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Navigation from './components/Navigation';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const location = useLocation();

  useEffect(() => {
    // Check authentication status whenever location changes
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, [location]);

  // Listen for storage events (when token is added/removed)
  useEffect(() => {
    const handleStorageChange = () => {
      const token = localStorage.getItem('token');
      setIsAuthenticated(!!token);
    };
    
    window.addEventListener('storage', handleStorageChange);
    // Also check on custom event
    window.addEventListener('authChange', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChange', handleStorageChange);
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      {isAuthenticated && <Navigation setIsAuthenticated={setIsAuthenticated} />}
      <main className={isAuthenticated ? "container mx-auto px-4 py-8" : ""}>
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/scans" element={
            <ProtectedRoute>
              <Scans />
            </ProtectedRoute>
          } />
          <Route path="/devices" element={
            <ProtectedRoute>
              <Devices />
            </ProtectedRoute>
          } />
          <Route path="/vulnerabilities" element={
            <ProtectedRoute>
              <Vulnerabilities />
            </ProtectedRoute>
          } />
          <Route path="/reports" element={
            <ProtectedRoute>
              <Reports />
            </ProtectedRoute>
          } />
          <Route path="/settings" element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          } />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;