# 🔌 Scanner API Reference - Control Everything from UI

## ✨ What You Now Have

A **complete REST API** running in WSL2 Kali that you can call from your frontend to:
- ✅ Check scanner status
- ✅ Get service statistics
- ✅ Run network scans
- ✅ Discover devices
- ✅ Port scanning
- ✅ Service detection
- ✅ Vulnerability scanning
- ✅ Get scan results

**Scanner URL**: `http://localhost:9000`

---

## 🎯 Management APIs (NEW!)

### **1. Service Status** 
```http
GET /service/status
```

**What it does**: Get detailed scanner service information

**Response**:
```json
{
  "service": "Security Scanner Service",
  "status": "running",
  "version": "1.0.0",
  "pid": 3855,
  "uptime_seconds": 145,
  "memory_usage_mb": 45.2,
  "cpu_percent": 2.5,
  "system_memory_percent": 42.3,
  "active_scans": 2,
  "scan_list": ["abc123", "def456"],
  "network_info": "eth0: 172.29.86.68",
  "timestamp": "2025-09-30T20:58:00"
}
```

**Use in UI**: Display scanner status in Dashboard

---

### **2. Service Statistics**
```http
GET /service/stats
```

**What it does**: Get statistics about available tools

**Response**:
```json
{
  "total_tools": 7,
  "tools_available": 5,
  "tools": {
    "nmap": true,
    "nikto": true,
    "masscan": true,
    "sqlmap": false,
    "hydra": false,
    "curl": true,
    "ping": true
  },
  "active_scans": 2,
  "python_version": "Python 3.13.7",
  "timestamp": "2025-09-30T20:58:00"
}
```

**Use in UI**: Show available tools in Settings page

---

### **3. Health Check**
```http
GET /health
```

**What it does**: Quick health check

**Response**:
```json
{
  "status": "healthy"
}
```

**Use in UI**: Auto-check every 30 seconds to show green/red indicator

---

### **4. Service Info**
```http
GET /
```

**What it does**: Basic service information

**Response**:
```json
{
  "status": "online",
  "service": "Security Scanner Service",
  "version": "1.0.0",
  "timestamp": "2025-09-30T20:58:00"
}
```

---

## 🔍 Scanning APIs

### **1. Network Discovery**
```http
POST /scan/discovery
Content-Type: application/json

{
  "target": "192.168.22.0/24"
}
```

**What it does**: Discover hosts on the network

**Response**:
```json
{
  "status": "completed",
  "target": "192.168.22.0/24",
  "hosts_found": 5,
  "hosts": [
    "192.168.22.1",
    "192.168.22.10",
    "192.168.22.50"
  ],
  "raw_output": "Nmap scan report for..."
}
```

**Use in UI**: Phase 1 - Network Discovery

---

### **2. Port Scanning**
```http
POST /scan/ports
Content-Type: application/json

{
  "target": "192.168.22.1",
  "ports": "1-1000"
}
```

**What it does**: Scan ports on a host

**Response**:
```json
{
  "status": "completed",
  "target": "192.168.22.1",
  "ports_scanned": "1-1000",
  "output": "PORT     STATE SERVICE\n22/tcp   open  ssh\n80/tcp   open  http"
}
```

**Use in UI**: Phase 2 - Port Discovery

---

### **3. Service Detection**
```http
POST /scan/service
Content-Type: application/json

{
  "target": "192.168.22.1"
}
```

**What it does**: Detect services and versions

**Response**:
```json
{
  "status": "completed",
  "target": "192.168.22.1",
  "output": "PORT     STATE SERVICE VERSION\n22/tcp   open  ssh     OpenSSH 8.2\n80/tcp   open  http    Apache 2.4.41"
}
```

**Use in UI**: Phase 3 - Service Enumeration

---

### **4. Vulnerability Scanning**
```http
POST /scan/vulnerability
Content-Type: application/json

{
  "target": "192.168.22.1"
}
```

**What it does**: Run vulnerability scripts

**Response**:
```json
{
  "status": "completed",
  "target": "192.168.22.1",
  "output": "Host script results:\n|_sslv2: SSLv2 supported - VULNERABLE"
}
```

**Use in UI**: Phase 4 - Vulnerability Assessment

---

### **5. Ping Check**
```http
POST /scan/ping
Content-Type: application/json

{
  "target": "192.168.22.1"
}
```

**What it does**: Quick check if host is up

**Response**:
```json
{
  "target": "192.168.22.1",
  "is_up": true,
  "output": "PING 192.168.22.1 (192.168.22.1) 56(84) bytes of data..."
}
```

**Use in UI**: Pre-scan validation

---

### **6. Nmap Scan (Advanced)**
```http
POST /scan/nmap
Content-Type: application/json

{
  "target": "192.168.22.1",
  "arguments": "-sV -sC -T4"
}
```

**What it does**: Run nmap with custom arguments

**Arguments Examples**:
- `-sn`: Ping scan (no port scan)
- `-sV`: Service version detection
- `-sC`: Default scripts
- `-p 22,80,443`: Specific ports
- `-T4`: Timing template (faster)
- `--script vuln`: Vulnerability scripts

**Response**:
```json
{
  "scan_id": "abc-123-def",
  "status": "completed",
  "target": "192.168.22.1",
  "command": "sudo nmap -sV -sC -T4 192.168.22.1",
  "output": "Starting Nmap...",
  "error": null,
  "return_code": 0
}
```

---

## 📊 How to Use from Frontend

### **Example 1: Dashboard Scanner Status**

```javascript
// In Dashboard.js
useEffect(() => {
  const checkScanner = async () => {
    try {
      const response = await fetch('http://localhost:9000/health');
      const data = await response.json();
      setScannerStatus(data.status === 'healthy' ? 'online' : 'offline');
    } catch (error) {
      setScannerStatus('offline');
    }
  };
  
  checkScanner();
  const interval = setInterval(checkScanner, 30000); // Every 30 seconds
  return () => clearInterval(interval);
}, []);
```

---

### **Example 2: Run Discovery Scan**

```javascript
// In Scans.js
const runDiscoveryScan = async (target) => {
  try {
    const response = await fetch('http://localhost:9000/scan/discovery', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target })
    });
    
    const data = await response.json();
    console.log(`Found ${data.hosts_found} hosts`);
    return data.hosts;
  } catch (error) {
    console.error('Scan failed:', error);
  }
};
```

---

### **Example 3: Get Scanner Stats**

```javascript
// In Settings.js
const getScannerStats = async () => {
  try {
    const response = await fetch('http://localhost:9000/service/stats');
    const data = await response.json();
    
    setToolsAvailable(data.tools_available);
    setToolsList(data.tools);
  } catch (error) {
    console.error('Failed to get stats:', error);
  }
};
```

---

## 🎯 Integration Points for UI

### **Dashboard Page**
- [ ] Add scanner status indicator (green/red dot)
- [ ] Show active scans count from `/service/status`
- [ ] Display scanner uptime
- [ ] Show memory/CPU usage

### **Scans Page**
- [ ] Use `/scan/discovery` for Phase 1
- [ ] Use `/scan/ports` for Phase 2
- [ ] Use `/scan/service` for Phase 3
- [ ] Use `/scan/vulnerability` for Phase 4
- [ ] Poll scan results while running

### **Settings Page**
- [ ] Show available tools from `/service/stats`
- [ ] Display scanner version and stats
- [ ] Add "Test Scanner" button using `/health`
- [ ] Show network info from `/service/status`

### **New: Scanner Management Page**
Create a new page: `/scanner-management`
- Scanner status (online/offline)
- Uptime and resource usage
- Active scans list
- Available tools
- Start/Stop/Restart buttons

---

## 🚀 Quick Start Script

To start the scanner automatically with the platform:

**File**: `start-platform.bat`
```batch
@echo off
echo Starting Security Platform...

REM Start scanner
powershell -ExecutionPolicy Bypass -File ensure-scanner-running.ps1

REM Start Docker
docker-compose up -d

REM Open browser
start http://localhost:3000

echo Platform started!
pause
```

---

## 📝 Test Commands

### Test from PowerShell:

```powershell
# Health check
curl http://localhost:9000/health

# Get status
curl http://localhost:9000/service/status | ConvertFrom-Json

# Get stats
curl http://localhost:9000/service/stats | ConvertFrom-Json

# Run discovery scan
$body = @{target="192.168.22.1"} | ConvertTo-Json
curl -Method POST -Uri http://localhost:9000/scan/discovery -ContentType "application/json" -Body $body | ConvertFrom-Json

# Ping check
$body = @{target="192.168.22.1"} | ConvertTo-Json
curl -Method POST -Uri http://localhost:9000/scan/ping -ContentType "application/json" -Body $body | ConvertFrom-Json
```

---

## 🎨 UI Components to Add

### 1. **Scanner Status Widget** (Dashboard)
```jsx
<div className="scanner-status">
  <span className={scannerOnline ? 'status-green' : 'status-red'}>
    {scannerOnline ? '● Scanner Online' : '● Scanner Offline'}
  </span>
  {scannerStats && (
    <div className="scanner-info">
      <span>Uptime: {formatUptime(scannerStats.uptime_seconds)}</span>
      <span>Active Scans: {scannerStats.active_scans}</span>
    </div>
  )}
</div>
```

### 2. **Tools Available Badge** (Settings)
```jsx
<div className="tools-badge">
  <h3>Security Tools</h3>
  <div className="tools-list">
    {Object.entries(tools).map(([tool, available]) => (
      <span key={tool} className={available ? 'tool-available' : 'tool-missing'}>
        {available ? '✓' : '✗'} {tool}
      </span>
    ))}
  </div>
</div>
```

### 3. **Scan Progress** (Scans Page)
```jsx
<div className="scan-progress">
  <h4>Phase 1: Network Discovery</h4>
  <ProgressBar percent={scanProgress} />
  <p>Found {hostsFound} hosts so far...</p>
</div>
```

---

## 🔧 Troubleshooting

### Scanner Returns "Connection Refused"
```powershell
# Check if scanner is running
wsl -d kali-linux ps aux | grep scanner_service

# If not, start it
.\ensure-scanner-running.ps1
```

### CORS Errors in Browser
The scanner already has CORS enabled (`CORS(app)`), so it should work from `localhost:3000`.

If issues persist, check browser console for specific error.

### Scans Timeout
Some scans take time. Adjust timeout in frontend:
```javascript
const response = await fetch(url, {
  method: 'POST',
  body: JSON.stringify(data),
  signal: AbortSignal.timeout(300000) // 5 minutes
});
```

---

## 📈 Next Steps

1. **Add Scanner Status to Dashboard**
   - Show green/red indicator
   - Display uptime and active scans

2. **Integrate Scan APIs**
   - Use `/scan/discovery` in scan orchestrator
   - Add real-time progress updates

3. **Create Scanner Management Page**
   - View detailed stats
   - Start/stop scanner
   - View logs

4. **Add Error Handling**
   - Gracefully handle scanner offline
   - Show helpful error messages
   - Retry logic

---

## ✨ Summary

You now have a **complete REST API** in WSL2 that can:
- ✅ Be called from your React frontend
- ✅ Run real network scans on `192.168.22.0/24`
- ✅ Return structured JSON data
- ✅ Provide service status and statistics
- ✅ Handle multiple concurrent scans

**No more command line needed!** Everything can be controlled from the web UI! 🎉

---

**Scanner is running at**: `http://localhost:9000`  
**Test it now**: `curl http://localhost:9000/service/stats`
