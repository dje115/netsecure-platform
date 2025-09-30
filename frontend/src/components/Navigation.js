import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

function Navigation({ setIsAuthenticated }) {
  const location = useLocation();
  const navigate = useNavigate();
  
  const isActive = (path) => {
    return location.pathname === path;
  };
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.dispatchEvent(new Event('authChange'));
    if (setIsAuthenticated) {
      setIsAuthenticated(false);
    }
    navigate('/login');
  };
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/scans', label: 'Scans', icon: '🔍' },
    { path: '/devices', label: 'Devices', icon: '💻' },
    { path: '/vulnerabilities', label: 'Vulnerabilities', icon: '⚠️' },
    { path: '/reports', label: 'Reports', icon: '📄' },
  ];
  
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-blue-600">
              🛡️ Security Platform
            </Link>
          </div>
          
          <div className="flex space-x-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive(item.path)
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </div>
          
          <div className="flex items-center space-x-4">
            <button 
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;