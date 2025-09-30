import React from 'react';

function Vulnerabilities() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Vulnerabilities</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-red-50 rounded-lg shadow-md p-6 border-l-4 border-red-500">
          <p className="text-sm text-red-600 mb-1">Critical</p>
          <p className="text-3xl font-bold text-red-700">0</p>
        </div>
        <div className="bg-orange-50 rounded-lg shadow-md p-6 border-l-4 border-orange-500">
          <p className="text-sm text-orange-600 mb-1">High</p>
          <p className="text-3xl font-bold text-orange-700">0</p>
        </div>
        <div className="bg-yellow-50 rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
          <p className="text-sm text-yellow-600 mb-1">Medium</p>
          <p className="text-3xl font-bold text-yellow-700">0</p>
        </div>
        <div className="bg-blue-50 rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <p className="text-sm text-blue-600 mb-1">Low</p>
          <p className="text-3xl font-bold text-blue-700">0</p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Vulnerability List</h2>
          <div className="flex space-x-2">
            <select className="px-4 py-2 border border-gray-300 rounded-md text-sm">
              <option>All Severities</option>
              <option>Critical</option>
              <option>High</option>
              <option>Medium</option>
              <option>Low</option>
            </select>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  CVE ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Severity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  CVSS Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Affected Devices
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                  No vulnerabilities detected yet. Run a vulnerability scan.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Vulnerabilities;

