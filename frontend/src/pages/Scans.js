import React, { useState, useEffect } from 'react';
import { scansAPI } from '../services/api';

function Scans() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewScanModal, setShowNewScanModal] = useState(false);
  const [newScan, setNewScan] = useState({
    name: '',
    target_range: '',
    scan_type: 'quick'
  });
  const [error, setError] = useState('');

  // Load scans on component mount
  useEffect(() => {
    loadScans();
    // Refresh every 5 seconds
    const interval = setInterval(loadScans, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadScans = async () => {
    try {
      const response = await scansAPI.list();
      setScans(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load scans:', err);
      setError('Failed to load scans');
      setLoading(false);
    }
  };

  const handleCreateScan = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await scansAPI.create(newScan);
      console.log('Scan created:', response.data);
      
      // Start the scan immediately
      await scansAPI.start(response.data.id);
      
      // Close modal and refresh
      setShowNewScanModal(false);
      setNewScan({ name: '', target_range: '', scan_type: 'quick' });
      loadScans();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create scan');
    }
  };

  const handleStopScan = async (scanId) => {
    try {
      await scansAPI.stop(scanId);
      loadScans();
    } catch (err) {
      console.error('Failed to stop scan:', err);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: 'bg-gray-100 text-gray-800',
      running: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800'
    };
    return badges[status] || badges.pending;
  };

  const getStatusIcon = (status) => {
    const icons = {
      pending: '⏳',
      running: '🔄',
      completed: '✅',
      failed: '❌'
    };
    return icons[status] || '⏳';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-gray-600">Loading scans...</div>
      </div>
    );
  }

  const activeScans = scans.filter(s => s.status === 'running' || s.status === 'pending');
  const completedScans = scans.filter(s => s.status === 'completed' || s.status === 'failed');

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Security Scans</h1>
        <button
          onClick={() => setShowNewScanModal(true)}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium transition-colors"
        >
          + New Scan
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Active Scans */}
      {activeScans.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Active Scans</h2>
          <div className="space-y-4">
            {activeScans.map(scan => (
              <div key={scan.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold">{scan.name}</h3>
                    <p className="text-sm text-gray-600">Target: {scan.target_range}</p>
                    <div className="mt-2 flex items-center space-x-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusBadge(scan.status)}`}>
                        {getStatusIcon(scan.status)} {scan.status.toUpperCase()}
                      </span>
                      <span className="text-sm text-gray-600">
                        Phase {scan.current_phase}/{scan.total_phases}
                      </span>
                    </div>
                  </div>
                  {scan.status === 'running' && (
                    <button
                      onClick={() => handleStopScan(scan.id)}
                      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
                    >
                      Stop
                    </button>
                  )}
                </div>
                
                {/* Progress Bar */}
                <div className="mt-4">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${scan.progress}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">{scan.progress}% complete</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeScans.length === 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Active Scans</h2>
          <p className="text-gray-600">No active scans. Start a new scan to begin security assessment.</p>
        </div>
      )}

      {/* Scan History */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Scan History</h2>
        {completedScans.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Target
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Findings
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Completed
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {completedScans.map(scan => (
                  <tr key={scan.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{scan.name}</div>
                      <div className="text-xs text-gray-500">{scan.scan_type}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.target_range}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusBadge(scan.status)}`}>
                        {getStatusIcon(scan.status)} {scan.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>{scan.devices_found || 0} devices</div>
                      <div className="text-red-600">{scan.vulnerabilities_found || 0} vulnerabilities</div>
                      <div className="text-orange-600">{scan.hvt_count || 0} HVTs</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {scan.completed_at ? new Date(scan.completed_at).toLocaleString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-600">No completed scans yet</p>
        )}
      </div>

      {/* New Scan Modal */}
      {showNewScanModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold mb-4">Create New Scan</h2>
            
            <form onSubmit={handleCreateScan} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scan Name
                </label>
                <input
                  type="text"
                  required
                  value={newScan.name}
                  onChange={(e) => setNewScan({ ...newScan, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Production Network Scan"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Range
                </label>
                <input
                  type="text"
                  required
                  value={newScan.target_range}
                  onChange={(e) => setNewScan({ ...newScan, target_range: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 192.168.1.0/24"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scan Type
                </label>
                <select
                  value={newScan.scan_type}
                  onChange={(e) => setNewScan({ ...newScan, scan_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="quick">Quick Scan (Network Discovery + Vulnerabilities)</option>
                  <option value="hvt">HVT Focused (Discovery + HVT + Services + Vulns)</option>
                  <option value="comprehensive">Comprehensive (All 11 Phases)</option>
                </select>
              </div>

              {error && (
                <div className="text-red-600 text-sm">
                  {error}
                </div>
              )}

              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowNewScanModal(false);
                    setError('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Start Scan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Scans;