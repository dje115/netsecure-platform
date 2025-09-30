# Scanner Status Fix - September 30, 2025

## Problem Identified

The scans were completing with "0 devices found" because the backend (running in Docker) couldn't communicate with the WSL2 scanner service.

### Root Cause

The backend was configured to connect to `http://localhost:9000`, but from inside a Docker container, `localhost` refers to the container itself, not the Windows host where the WSL2 scanner service is running.

## Solution Applied

### 1. Fixed Backend Scanner Configuration

**File**: `backend/app/core/config.py`

**Changed**:
```python
# Before
WSL_SCANNER_URL: str = "http://localhost:9000"
WSL_SCANNER_HOST: str = "localhost"

# After
WSL_SCANNER_URL: str = "http://host.docker.internal:9000"
WSL_SCANNER_HOST: str = "host.docker.internal"
```

**Why This Works**:
- `host.docker.internal` is a special DNS name that Docker provides
- It resolves to the host machine's IP address from within the container
- This allows the backend container to reach services running on Windows (like the WSL2 scanner)

### 2. Added Scanner Status Indicator to Dashboard

**File**: `frontend/src/pages/Dashboard.js`

**Added Features**:
- Real-time scanner status monitoring
- Checks scanner health every 30 seconds
- Displays scanner statistics (Python version, available tools)
- Shows visual indicator: green (online), yellow (checking), red (offline)

**New UI Elements**:
- "Scanner Service" status card in "System Status" section
- Shows "Ready for scans" when scanner is online
- Shows "Checking..." during status check
- Shows "Offline" when scanner is unreachable

## Testing Steps

### 1. Verify Scanner is Running

```powershell
# Check scanner status
curl http://localhost:9000/health

# Check scanner statistics
curl http://localhost:9000/service/stats
```

Expected output from `/service/stats`:
```json
{
  "service": "WSL2 Kali Security Scanner",
  "version": "1.0.0",
  "python_version": "3.11.x",
  "available_tools": {
    "nmap": "/usr/bin/nmap",
    "masscan": "/usr/bin/masscan",
    "nikto": "/usr/bin/nikto"
  }
}
```

### 2. Verify Backend Can Reach Scanner

```powershell
cd C:\Users\david\Documents\Netsecure

# Check backend logs
docker-compose logs security-api | Select-String -Pattern "scanner"

# Restart backend to pick up new config
docker-compose restart security-api
```

### 3. Test Scan Execution

1. Go to Dashboard (http://localhost:3000)
2. Check "System Status" section - Scanner Service should show "Ready for scans" with green indicator
3. Navigate to "Scans" page
4. Click "New Scan"
5. Enter:
   - Name: `Network Test`
   - Target: `192.168.22.0/24` (or your network range)
   - Select desired phases
6. Click "Start Scan"
7. Watch the scan progress in real-time

**Expected Results**:
- Scan should start immediately
- Progress bar should update
- Devices should be discovered and shown in the results
- Scanner Service on dashboard should remain green/online

## Scanner Service Management

### Start Scanner
```powershell
.\start-scanner.bat
```

### Check Scanner Status
```powershell
curl http://localhost:9000/service/status
```

### View Scanner Logs
```powershell
wsl -d kali-linux cat /root/security-scanner/scanner.log
```

### Restart Scanner
```powershell
# Via API
curl -X POST http://localhost:9000/service/restart

# Or manually
wsl -d kali-linux pkill -f scanner_service.py
.\start-scanner.bat
```

## Network Diagram

```
┌─────────────────────────────────────────────────┐
│             Windows Host                        │
│                                                 │
│  ┌─────────────────┐      ┌─────────────────┐ │
│  │   React App     │      │   WSL2 Kali     │ │
│  │  localhost:3000 │      │  Scanner :9000  │ │
│  └────────┬────────┘      └────────┬────────┘ │
│           │                        │          │
│           │                        │          │
│  ┌────────▼──────────────────────┬─┘          │
│  │    Docker Network             │            │
│  │                               │            │
│  │  ┌────────────────────┐       │            │
│  │  │  Backend API       │       │            │
│  │  │   :8000            │       │            │
│  │  └────────┬───────────┘       │            │
│  │           │                   │            │
│  │  ┌────────▼───────────┐       │            │
│  │  │  PostgreSQL :5432  │       │            │
│  │  └────────────────────┘       │            │
│  │                               │            │
│  └───────────────────────────────┘            │
│                                                │
└─────────────────────────────────────────────────┘

Connection Flow:
1. React App → Backend API: http://localhost:8000
2. Backend → Scanner: http://host.docker.internal:9000 ✅
3. Scanner → Target Network: Direct network access via WSL2
```

## What Changed

### Before (Not Working)
- Backend tried to reach scanner at `localhost:9000`
- Inside Docker, `localhost` = the container itself
- Scanner running on Windows host was unreachable
- Scans failed with "0 devices found"

### After (Working)
- Backend reaches scanner at `host.docker.internal:9000`
- Docker resolves this to Windows host IP
- Scanner is accessible from backend container
- Scans can now discover devices on the network

## Verification Checklist

- [x] Scanner service running in WSL2 Kali
- [x] Scanner accessible from Windows host (localhost:9000)
- [x] Backend configuration updated to use host.docker.internal
- [x] Backend restarted to load new configuration
- [x] Dashboard shows scanner status indicator
- [x] Scanner status updates every 30 seconds
- [ ] Test scan executed successfully (needs testing)
- [ ] Devices discovered on target network (needs testing)

## Next Steps

1. **Test a Real Scan**:
   - Create a new scan with target `192.168.22.0/24`
   - Verify devices are discovered
   - Check scan results show correct device information

2. **Monitor Scan Progress**:
   - Watch dashboard for real-time updates
   - Check backend logs: `docker-compose logs -f security-api`
   - Check scanner logs: `wsl -d kali-linux cat /root/security-scanner/scanner.log`

3. **If Scan Still Fails**:
   - Check scanner logs for errors
   - Verify Kali can reach target network: `wsl -d kali-linux ping 192.168.22.1`
   - Check if Nmap is working: `wsl -d kali-linux nmap -sn 192.168.22.0/24`

## Documentation Updated

- ✅ `SCANNER-API-REFERENCE.md` - Complete scanner API documentation
- ✅ `SCANNER-STATUS-FIXED.md` - This file
- ✅ `COMPLETE-SETUP.md` - Already has scanner setup instructions
- ✅ Backend configuration fixed
- ✅ Frontend dashboard updated with status indicator

## Support Information

If scans are still not working after this fix:

1. **Check Network Connectivity**:
   ```bash
   wsl -d kali-linux ping 192.168.22.1
   wsl -d kali-linux nmap -sn 192.168.22.1
   ```

2. **Verify WSL2 Network Mode**:
   - WSL2 should have mirrored networking mode for full network access
   - Check `%USERPROFILE%\.wslconfig` for network settings

3. **Check Firewall**:
   - Windows Firewall may block WSL2 network scans
   - Temporarily disable to test

4. **View Live Logs**:
   ```powershell
   # Backend
   docker-compose logs -f security-api
   
   # Scanner
   wsl -d kali-linux tail -f /root/security-scanner/scanner.log
   ```


