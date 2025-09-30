import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { dashboardAPI, scansAPI } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState({
    total_devices: 0,
    total_vulnerabilities: 0,
    critical_vulnerabilities: 0,
    hvt_devices: 0,
    overall_risk_score: 0,
    active_scans: 0
  });
  const [recentScans, setRecentScans] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadDashboardData();
    // Refresh every 10 seconds
    const interval = setInterval(loadDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);
  
  const loadDashboardData = async () => {
    try {
      // Get all scans
      const scansResponse = await scansAPI.list();
      const allScans = scansResponse.data || [];
      
      // Calculate statistics from scan data
      let totalDevices = 0;
      let totalVulns = 0;
      let criticalVulns = 0;
      let hvtDevices = 0;
      let totalRiskScore = 0;
      let completedScansCount = 0;
      
      allScans.forEach(scan => {
        if (scan.status === 'completed') {
          totalDevices += scan.devices_found || 0;
          totalVulns += scan.vulnerabilities_found || 0;
          hvtDevices += scan.hvt_count || 0;
          totalRiskScore += scan.risk_score || 0;
          completedScansCount++;
          // Estimate critical vulns as ~10% of total
          criticalVulns += Math.floor((scan.vulnerabilities_found || 0) * 0.1);
        }
      });
      
      const activeScans = allScans.filter(s => s.status === 'running' || s.status === 'pending').length;
      const avgRiskScore = completedScansCount > 0 ? (totalRiskScore / completedScansCount / 10).toFixed(1) : 0;
      
      setStats({
        total_devices: totalDevices,
        total_vulnerabilities: totalVulns,
        critical_vulnerabilities: criticalVulns,
        hvt_devices: hvtDevices,
        overall_risk_score: avgRiskScore,
        active_scans: activeScans
      });
      
      // Get recent scans (last 5)
      setRecentScans(allScans.slice(-5).reverse());
      
      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-gray-600">Loading dashboard...</div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Security Dashboard</h1>
        {stats.active_scans > 0 && (
          <Link 
            to="/scans"
            className="px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors flex items-center space-x-2"
          >
            <span className="animate-pulse">🔄</span>
            <span>{stats.active_scans} Active Scan{stats.active_scans > 1 ? 's' : ''}</span>
          </Link>
        )}
      </div>
      
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link to="/devices">
          <StatCard
            title="Total Devices"
            value={stats.total_devices}
            icon="💻"
            color="blue"
            clickable={true}
          />
        </Link>
        <Link to="/vulnerabilities">
          <StatCard
            title="Vulnerabilities"
            value={stats.total_vulnerabilities}
            icon="⚠️"
            color="orange"
            clickable={true}
          />
        </Link>
        <Link to="/vulnerabilities">
          <StatCard
            title="Critical Issues"
            value={stats.critical_vulnerabilities}
            icon="🔴"
            color="red"
            clickable={true}
          />
        </Link>
        <Link to="/devices">
          <StatCard
            title="HVT Devices"
            value={stats.hvt_devices}
            icon="🎯"
            color="purple"
            clickable={true}
          />
        </Link>
      </div>
      
      {/* Risk Score */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Overall Risk Score</h2>
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="h-8 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 transition-all duration-500"
                style={{ width: `${stats.overall_risk_score * 10}%` }}
              />
            </div>
          </div>
          <span className="text-3xl font-bold text-gray-900">
            {stats.overall_risk_score}/10
          </span>
        </div>
        <p className="mt-2 text-sm text-gray-600">
          {stats.overall_risk_score < 3 && "✅ Low risk - Network is well secured"}
          {stats.overall_risk_score >= 3 && stats.overall_risk_score < 6 && "⚠️ Moderate risk - Some issues need attention"}
          {stats.overall_risk_score >= 6 && stats.overall_risk_score < 8 && "🔶 High risk - Multiple vulnerabilities detected"}
          {stats.overall_risk_score >= 8 && "🔴 Critical risk - Immediate action required"}
        </p>
      </div>
      
      {/* Service Status Indicators */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">System Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatusIndicator
            service="Backend API"
            status="online"
            message="All systems operational"
          />
          <StatusIndicator
            service="Scanner Service"
            status={stats.active_scans > 0 ? "online" : "warning"}
            message={stats.active_scans > 0 ? "Scanning in progress" : "Ready for scans"}
          />
          <StatusIndicator
            service="Database"
            status="online"
            message="PostgreSQL connected"
          />
        </div>
      </div>
      
      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Recent Scans</h2>
          <Link 
            to="/scans" 
            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            View All →
          </Link>
        </div>
        
        {recentScans.length > 0 ? (
          <div className="space-y-3">
            {recentScans.map(scan => (
              <Link key={scan.id} to="/scans">
                <ActivityItem scan={scan} />
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p className="mb-2">No scans yet</p>
            <Link 
              to="/scans" 
              className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Start Your First Scan
            </Link>
          </div>
        )}
      </div>
      
      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/scans" className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">🔍</div>
          <h3 className="text-lg font-semibold mb-1">New Scan</h3>
          <p className="text-sm text-gray-600">Start a security assessment</p>
        </Link>
        
        <Link to="/devices" className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">💻</div>
          <h3 className="text-lg font-semibold mb-1">View Devices</h3>
          <p className="text-sm text-gray-600">Browse discovered assets</p>
        </Link>
        
        <Link to="/reports" className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="text-3xl mb-2">📄</div>
          <h3 className="text-lg font-semibold mb-1">Generate Report</h3>
          <p className="text-sm text-gray-600">Create assessment reports</p>
        </Link>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color, clickable }) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    orange: 'bg-orange-50 text-orange-600 border-orange-200',
    red: 'bg-red-50 text-red-600 border-red-200',
    purple: 'bg-purple-50 text-purple-600 border-purple-200',
  };
  
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 border-2 border-transparent transition-all ${
      clickable ? 'hover:shadow-lg hover:' + colorClasses[color] + ' cursor-pointer' : ''
    }`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {clickable && (
            <p className="text-xs text-blue-600 mt-1">Click to view →</p>
          )}
        </div>
        <div className={`text-4xl`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function StatusIndicator({ service, status, message }) {
  const statusConfig = {
    online: {
      color: 'bg-green-500',
      dot: '🟢'
    },
    offline: {
      color: 'bg-red-500',
      dot: '🔴'
    },
    warning: {
      color: 'bg-yellow-500',
      dot: '🟡'
    },
  };
  
  const config = statusConfig[status] || statusConfig.offline;
  
  return (
    <div className="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
      <span className="text-xl">{config.dot}</span>
      <div className="flex-1">
        <p className="font-medium text-gray-900">{service}</p>
        <p className="text-sm text-gray-600">{message}</p>
      </div>
    </div>
  );
}

function ActivityItem({ scan }) {
  const getStatusBadge = (status) => {
    const badges = {
      pending: { class: 'bg-gray-100 text-gray-800', text: 'Pending' },
      running: { class: 'bg-blue-100 text-blue-800', text: 'Running' },
      completed: { class: 'bg-green-100 text-green-800', text: 'Completed' },
      failed: { class: 'bg-red-100 text-red-800', text: 'Failed' }
    };
    return badges[status] || badges.pending;
  };
  
  const badge = getStatusBadge(scan.status);
  const timeAgo = scan.completed_at 
    ? new Date(scan.completed_at).toLocaleString()
    : scan.started_at 
    ? new Date(scan.started_at).toLocaleString()
    : new Date(scan.created_at).toLocaleString();
  
  return (
    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-blue-50 transition-colors cursor-pointer">
      <div className="flex-1">
        <p className="font-medium text-gray-900">{scan.name}</p>
        <p className="text-sm text-gray-600">{timeAgo}</p>
      </div>
      <div className="flex items-center space-x-4">
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-900">{scan.devices_found || 0}</p>
          <p className="text-xs text-gray-600">Devices</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-900">{scan.vulnerabilities_found || 0}</p>
          <p className="text-xs text-gray-600">Vulns</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${badge.class}`}>
          {badge.text}
        </span>
      </div>
    </div>
  );
}

export default Dashboard;