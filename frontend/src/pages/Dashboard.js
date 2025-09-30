import React, { useEffect, useState } from 'react';
import { dashboardAPI } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadDashboardData();
  }, []);
  
  const loadDashboardData = async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setLoading(false);
    }
  };
  
  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Security Dashboard</h1>
      
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Devices"
          value={stats?.total_devices || 0}
          icon="💻"
          color="blue"
        />
        <StatCard
          title="Vulnerabilities"
          value={stats?.total_vulnerabilities || 0}
          icon="⚠️"
          color="orange"
        />
        <StatCard
          title="Critical Issues"
          value={stats?.critical_vulnerabilities || 0}
          icon="🔴"
          color="red"
        />
        <StatCard
          title="HVT Devices"
          value={stats?.hvt_devices || 0}
          icon="🎯"
          color="purple"
        />
      </div>
      
      {/* Risk Score */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Overall Risk Score</h2>
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="h-8 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500"
                style={{ width: `${(stats?.overall_risk_score || 0) * 10}%` }}
              />
            </div>
          </div>
          <span className="text-3xl font-bold text-gray-900">
            {stats?.overall_risk_score || 0}/10
          </span>
        </div>
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
            status="online"
            message="WSL2 scanner ready"
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
        <h2 className="text-xl font-semibold mb-4">Recent Scans</h2>
        <div className="space-y-3">
          <ActivityItem
            title="Production Network Scan"
            status="Completed"
            time="2 hours ago"
            devices={42}
            vulnerabilities={127}
          />
          <ActivityItem
            title="DMZ Assessment"
            status="Running"
            time="30 minutes ago"
            devices={15}
            vulnerabilities={0}
          />
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color }) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-800',
    orange: 'bg-orange-100 text-orange-800',
    red: 'bg-red-100 text-red-800',
    purple: 'bg-purple-100 text-purple-800',
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`text-4xl p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function StatusIndicator({ service, status, message }) {
  const statusColors = {
    online: 'status-green',
    offline: 'status-red',
    warning: 'status-yellow',
  };
  
  return (
    <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
      <span className={`status-indicator ${statusColors[status]}`}></span>
      <div>
        <p className="font-medium text-gray-900">{service}</p>
        <p className="text-sm text-gray-600">{message}</p>
      </div>
    </div>
  );
}

function ActivityItem({ title, status, time, devices, vulnerabilities }) {
  return (
    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
      <div className="flex-1">
        <p className="font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{time}</p>
      </div>
      <div className="flex items-center space-x-4">
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-900">{devices}</p>
          <p className="text-xs text-gray-600">Devices</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-900">{vulnerabilities}</p>
          <p className="text-xs text-gray-600">Vulns</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
          status === 'Completed' 
            ? 'bg-green-100 text-green-800' 
            : 'bg-blue-100 text-blue-800'
        }`}>
          {status}
        </span>
      </div>
    </div>
  );
}

export default Dashboard;
