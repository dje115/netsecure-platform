import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// API endpoints
export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getRecentScans: () => api.get('/api/dashboard/recent-scans'),
  getOnlineDevices: () => api.get('/api/dashboard/devices/online'),
  getCriticalVulnerabilities: () => api.get('/api/dashboard/vulnerabilities/critical'),
};

export const scansAPI = {
  list: () => api.get('/api/scans'),
  get: (id) => api.get(`/api/scans/${id}`),
  create: (data) => api.post('/api/scans', data),
  start: (id) => api.post(`/api/scans/${id}/start`),
  stop: (id) => api.post(`/api/scans/${id}/stop`),
  delete: (id) => api.delete(`/api/scans/${id}`),
  getLogs: (id) => api.get(`/api/scans/${id}/logs`),
  getPhases: (id) => api.get(`/api/scans/${id}/phases`),
};

export const devicesAPI = {
  list: (params) => api.get('/api/devices', { params }),
  get: (id) => api.get(`/api/devices/${id}`),
  getPorts: (id) => api.get(`/api/devices/${id}/ports`),
  getServices: (id) => api.get(`/api/devices/${id}/services`),
  getVulnerabilities: (id) => api.get(`/api/devices/${id}/vulnerabilities`),
  getAttackPaths: (id) => api.get(`/api/devices/${id}/attack-paths`),
};

export const vulnerabilitiesAPI = {
  list: (params) => api.get('/api/vulnerabilities', { params }),
  get: (id) => api.get(`/api/vulnerabilities/${id}`),
  getStats: () => api.get('/api/vulnerabilities/stats'),
};

export const reportsAPI = {
  list: () => api.get('/api/reports'),
  get: (id) => api.get(`/api/reports/${id}`),
  create: (data) => api.post('/api/reports', data),
  download: (id) => api.get(`/api/reports/${id}/download`, { responseType: 'blob' }),
  delete: (id) => api.delete(`/api/reports/${id}`),
};

export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  getCurrentUser: () => api.get('/api/auth/me'),
};

export default api;
