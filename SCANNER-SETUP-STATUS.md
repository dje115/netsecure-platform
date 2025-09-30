# 🔍 Scanner Setup Status

## ✅ What's Working

1. **✅ Authentication** - Login works (`admin` / `admin123`)
2. **✅ Frontend** - React app loads and displays correctly
3. **✅ Database** - PostgreSQL is connected and working
4. **✅ Scan Creation** - Can create scans through UI
5. **✅ WSL2** - Kali Linux is installed and running
6. **✅ Network Access** - Kali can ping your network (192.168.22.1)
7. **✅ Nmap** - Installed and working in Kali
   ```bash
   wsl -d kali-linux nmap --version
   # Nmap version 7.95
   ```

## ❌ What's NOT Working

1. **❌ Scanner Service** - Flask REST API not starting
2. **❌ Device Discovery** - Scans complete but find 0 devices
3. **❌ Real Scanning** - Backend can't communicate with scanner

---

## 🔍 The Problem

### Current Situation:
```
[Frontend] → [Backend API (Docker)] → [WSL2 Scanner Service] → [Your Network]
                                            ❌ NOT RUNNING
```

The scan you ran shows:
- **Status**: COMPLETED  
- **Devices Found**: 0  
- **Why**: Backend couldn't reach scanner service

### What Happens When You Click "Start Scan":
1. ✅ Frontend sends request to backend
2. ✅ Backend creates scan in database
3. ❌ Backend tries to call WSL2 scanner at `http://host.docker.internal:9000`
4. ❌ Scanner service not running → No response
5. ✅ Scan marks as "completed" (but with no results)

---

## 🛠️ Quick Fix Options

### **Option 1: Manual Scan (Test Network Access)**

Run this in PowerShell to verify Kali can scan your network:

```powershell
wsl -d kali-linux sudo nmap -sn 192.168.22.0/24
```

Expected output:
```
Nmap scan report for 192.168.22.1
Host is up (0.00052s latency).
Nmap done: 256 IP addresses (X hosts up) scanned in Y seconds
```

### **Option 2: Start Scanner Service Manually**

1. **In PowerShell:**
   ```powershell
   wsl -d kali-linux
   ```

2. **In WSL (Kali):**
   ```bash
   cd /root/security-scanner
   python3 scanner_service.py
   ```

3. **Test it** (in another PowerShell):
   ```powershell
   curl http://localhost:9000/
   ```

   Should return:
   ```json
   {
     "status": "online",
     "service": "Security Scanner Service"
   }
   ```

4. **Leave it running** in that terminal

5. **Run a scan** from the web UI

### **Option 3: Use Docker-Based Scanning (Simpler)**

Instead of WSL2, use a Docker container with network access.

**Edit** `docker-compose.yml` - Add network mode:

```yaml
security-api:
  network_mode: "host"  # <-- Add this line
```

This lets the Docker container scan your host network directly.

---

## 📋 Complete Setup Steps (If Starting Fresh)

### Step 1: Start Scanner Service

```powershell
# Open a dedicated PowerShell window for the scanner
wsl -d kali-linux bash -c "cd /root/security-scanner && python3 scanner_service.py"
```

**Leave this window open!**

### Step 2: Verify Scanner is Running

```powershell
# In a NEW PowerShell window
curl http://localhost:9000/health
```

Expected: `{"status": "healthy"}`

### Step 3: Test Scanning from Scanner

```powershell
curl -X POST http://localhost:9000/scan/discovery `
  -H "Content-Type: application/json" `
  -d '{\"target\": \"192.168.22.0/24\"}'
```

Should return hosts found on your network.

### Step 4: Run Scan from Web UI

1. Go to `http://localhost:3000`
2. Login (`admin` / `admin123`)
3. Go to Scans
4. Click "+ New Scan"
5. Enter:
   - Name: `Home Network Scan`
   - Target: `192.168.22.0/24`
   - Type: Quick Scan
6. Click "Start Scan"

### Step 5: Check Results

Wait 1-2 minutes, then refresh the page. You should see:
- **Devices Found**: > 0
- **Status**: COMPLETED

---

## 🔧 Troubleshooting

### Scanner Service Won't Start

**Check Python and Flask:**
```powershell
wsl -d kali-linux python3 --version
wsl -d kali-linux python3 -c "import flask; print('Flask OK')"
```

**If Flask not found:**
```powershell
wsl -d kali-linux sudo pip3 install flask flask-cors
```

### Can't Connect to Scanner from Docker

**Test connectivity:**
```powershell
docker-compose exec security-api curl http://host.docker.internal:9000/health
```

If fails, the Docker container can't reach WSL2.

**Solution**: Use `host.docker.internal` or WSL's IP address.

**Get WSL IP:**
```powershell
wsl -d kali-linux hostname -I
```

**Update backend** `scanner_client.py`:
```python
SCANNER_URL = "http://172.29.86.68:9000"  # Use actual WSL IP
```

### Scans Find 0 Devices

**Verify nmap works directly:**
```powershell
wsl -d kali-linux sudo nmap -sn 192.168.22.1
```

**Check if WSL can reach your network:**
```powershell
wsl -d kali-linux ping -c 2 192.168.22.1
```

Both should work (you tested this already).

---

## 🎯 Next Steps

### Immediate (To Get Scans Working):

1. **Start scanner service manually** (keep window open)
   ```powershell
   wsl -d kali-linux bash -c "cd /root/security-scanner && python3 scanner_service.py"
   ```

2. **Run a test scan** from web UI

3. **Verify it finds devices**

### Long-term (Proper Setup):

1. **Create systemd service** in WSL so scanner auto-starts
2. **Configure port forwarding** for reliability  
3. **Add scanner health check** in backend
4. **Add scanner status** to dashboard

---

## 📝 Files Created

1. **`scanner_service.py`** - Flask REST API for running scans
   - Location in WSL: `/root/security-scanner/scanner_service.py`
   - Location on Windows: `C:\Users\david\Documents\Netsecure\scanner_service.py`

2. **Installed in Kali:**
   - `nmap` - Network scanner
   - `nikto` - Web vulnerability scanner
   - `masscan` - Fast port scanner
   - `python3-flask` - Web framework
   - `python3-flask-cors` - CORS support

---

## 🧪 Quick Test Commands

### Test 1: Can Kali Scan Your Network?
```powershell
wsl -d kali-linux sudo nmap -sn 192.168.22.1-10
```
**Expected**: Should find at least 1 host

### Test 2: Is Scanner Service Running?
```powershell
curl http://localhost:9000/
```
**Expected**: JSON response with "status": "online"

### Test 3: Can Scanner Discover Hosts?
```powershell
$body = '{"target": "192.168.22.1"}'
curl -X POST http://localhost:9000/scan/ping -H "Content-Type: application/json" -d $body
```
**Expected**: `"is_up": true`

### Test 4: Can Backend Reach Scanner?
```powershell
docker-compose exec security-api curl http://host.docker.internal:9000/health
```
**Expected**: `{"status": "healthy"}`

---

## 💡 Quick Win

**To see scans actually work RIGHT NOW:**

1. Open PowerShell, run:
   ```powershell
   wsl -d kali-linux bash -c "cd /root/security-scanner && python3 scanner_service.py"
   ```

2. **Keep that window open**

3. In web browser, create and run a scan

4. Should find devices this time!

**Note**: Scanner will stop when you close the PowerShell window. For permanent solution, set up systemd service.

---

## 📞 Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Kali Linux (WSL2) | ✅ Running | `wsl --list --verbose` |
| Nmap | ✅ Installed | Version 7.95 |
| Network Access | ✅ Working | Can ping 192.168.22.1 |
| Scanner Service | ❌ Not Running | Needs manual start |
| Backend API | ✅ Running | Port 8000 |
| Frontend | ✅ Running | Port 3000 |
| Database | ✅ Running | PostgreSQL |
| Authentication | ✅ Working | admin/admin123 |

**Bottom Line**: Everything is installed and configured. Just need to start the scanner service to make scans work!

