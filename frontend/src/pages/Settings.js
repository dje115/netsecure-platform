import React, { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

function Settings() {
  const [settings, setSettings] = useState({
    openai_api_key: '',
    anthropic_api_key: '',
    scan_timeout: 3600,
    max_concurrent_scans: 3,
    enable_ai_analysis: true,
    enable_hvt_detection: true,
  });
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');
  const [showKeys, setShowKeys] = useState({
    openai: false,
    anthropic: false,
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = () => {
    // Load from localStorage for now
    const savedSettings = localStorage.getItem('platform_settings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  };

  const handleChange = (field, value) => {
    setSettings({ ...settings, [field]: value });
    setSaved(false);
  };

  const handleSave = () => {
    try {
      // Save to localStorage
      localStorage.setItem('platform_settings', JSON.stringify(settings));
      setSaved(true);
      setError('');
      
      // Auto-hide success message after 3 seconds
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError('Failed to save settings');
    }
  };

  const toggleShowKey = (keyType) => {
    setShowKeys({ ...showKeys, [keyType]: !showKeys[keyType] });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Settings</h1>

      {/* Success Message */}
      {saved && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Success!</strong>
          <span className="block sm:inline"> Settings saved successfully.</span>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
        </div>
      )}

      {/* AI Configuration */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          🤖 AI Configuration
        </h2>
        <p className="text-sm text-gray-600 mb-4">
          Configure AI API keys for automated device classification, vulnerability analysis, and security recommendations.
        </p>

        <div className="space-y-4">
          {/* OpenAI API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              OpenAI API Key (GPT-4)
            </label>
            <div className="flex space-x-2">
              <input
                type={showKeys.openai ? "text" : "password"}
                className="flex-1 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="sk-..."
                value={settings.openai_api_key}
                onChange={(e) => handleChange('openai_api_key', e.target.value)}
              />
              <button
                type="button"
                onClick={() => toggleShowKey('openai')}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
              >
                {showKeys.openai ? '👁️ Hide' : '👁️ Show'}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Get your API key from: <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">https://platform.openai.com/api-keys</a>
            </p>
          </div>

          {/* Anthropic API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Anthropic API Key (Claude)
            </label>
            <div className="flex space-x-2">
              <input
                type={showKeys.anthropic ? "text" : "password"}
                className="flex-1 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="sk-ant-..."
                value={settings.anthropic_api_key}
                onChange={(e) => handleChange('anthropic_api_key', e.target.value)}
              />
              <button
                type="button"
                onClick={() => toggleShowKey('anthropic')}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
              >
                {showKeys.anthropic ? '👁️ Hide' : '👁️ Show'}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Get your API key from: <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">https://console.anthropic.com/settings/keys</a>
            </p>
          </div>
        </div>
      </div>

      {/* Scan Configuration */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          🔍 Scan Configuration
        </h2>

        <div className="space-y-4">
          {/* Scan Timeout */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Scan Timeout (seconds)
            </label>
            <input
              type="number"
              min="60"
              max="7200"
              className="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              value={settings.scan_timeout}
              onChange={(e) => handleChange('scan_timeout', parseInt(e.target.value))}
            />
            <p className="text-xs text-gray-500 mt-1">
              Maximum time allowed for a single scan (60-7200 seconds)
            </p>
          </div>

          {/* Max Concurrent Scans */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Concurrent Scans
            </label>
            <input
              type="number"
              min="1"
              max="10"
              className="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              value={settings.max_concurrent_scans}
              onChange={(e) => handleChange('max_concurrent_scans', parseInt(e.target.value))}
            />
            <p className="text-xs text-gray-500 mt-1">
              Number of scans that can run simultaneously (1-10)
            </p>
          </div>
        </div>
      </div>

      {/* Feature Toggles */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          ⚙️ Features
        </h2>

        <div className="space-y-4">
          {/* Enable AI Analysis */}
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Enable AI Analysis</p>
              <p className="text-sm text-gray-600">Use AI for device classification and vulnerability analysis</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                className="sr-only peer"
                checked={settings.enable_ai_analysis}
                onChange={(e) => handleChange('enable_ai_analysis', e.target.checked)}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          {/* Enable HVT Detection */}
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Enable HVT Detection</p>
              <p className="text-sm text-gray-600">Automatically identify high-value targets</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                className="sr-only peer"
                checked={settings.enable_hvt_detection}
                onChange={(e) => handleChange('enable_hvt_detection', e.target.checked)}
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      {/* About */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          ℹ️ About
        </h2>
        <div className="space-y-2 text-sm text-gray-600">
          <p><strong>Platform:</strong> Professional Security Assessment Platform</p>
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Environment:</strong> Docker + WSL2</p>
          <p><strong>Database:</strong> PostgreSQL</p>
          <p><strong>Scanner:</strong> Kali Linux Tools (Nmap, Nikto, etc.)</p>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end space-x-3">
        <button
          onClick={loadSettings}
          className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 font-medium"
        >
          Reset
        </button>
        <button
          onClick={handleSave}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
        >
          Save Settings
        </button>
      </div>
    </div>
  );
}

export default Settings;
