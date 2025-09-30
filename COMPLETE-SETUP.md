# 🚀 Complete Setup Guide - Everything From the UI

## ✅ Current Status

**SCANNER IS NOW RUNNING!** ✨

- ✅ Scanner Service: http://localhost:9000
- ✅ Can scan your network: Found `192.168.22.1` (unifi.localdomain)
- ✅ Backend API: Running
- ✅ Frontend UI: Running
- ✅ Database: Connected
- ✅ Authentication: Working (admin/admin123)

---

## 🎯 **Quick Start** (Simplest Way)

### **Option 1: One-Click Startup** (RECOMMENDED)

**Double-click:** `start-platform.bat`

This will:
1. ✅ Check and start scanner service
2. ✅ Start all Docker services
3. ✅ Open your browser to the web interface

**Then:**
- Login: `admin` / `admin123`
- Go to **Scans** page
- Click **+ New Scan**
- Target: `192.168.22.0/24`
- Click **Start Scan**
- **IT WILL NOW FIND DEVICES!** ✨

---

### **Option 2: Manual Steps**

If you prefer step-by-step:

**1. Start Scanner (PowerShell):**
```powershell
.\ensure-scanner-running.ps1
```

**2. Start Docker:**
```powershell
docker-compose up -d
```

**3. Open Browser:**
```
http://localhost:3000
```

---

## 📊 **Everything is Managed from the UI**

### **Dashboard** (`http://localhost:3000`)
- 📊 View statistics (devices, vulnerabilities, risk score)
- 🎯 See active scans
- 📈 Monitor system status
- 🚨 View critical issues

### **Scans Page** (`http://localhost:3000/scans`)
- ➕ **Create new scans** (+ New Scan button)
- ▶️ **Start/Stop scans**
- 📊 **View progress** (real-time updates)
- 📜 **See scan history**
- 🔄 **Auto-refreshes** every 5 seconds

### **Devices Page** (`http://localhost:3000/devices`)
- 💻 View all discovered devices
- 🔍 Filter by HVT status
- 📊 See device details
- ⚠️ View vulnerabilities per device

### **Vulnerabilities Page** (`http://localhost:3000/vulnerabilities`)
- ⚠️ See all vulnerabilities found
- 🔴 Filter by severity (Critical, High, Medium, Low)
- 📋 View CVE details
- 🛠️ Get remediation steps

### **Reports Page** (`http://localhost:3000/reports`)
- 📄 Generate reports (PDF, HTML, DOCX)
- 📊 Executive summary
- 🔬 Technical details
- 📋 Compliance reports

### **Settings Page** (`http://localhost:3000/settings`)
- 🤖 Configure AI API keys (OpenAI, Anthropic)
- ⚙️ Scan settings (timeout, concurrency)
- 🎚️ Feature toggles
- ℹ️ Platform information

---

## 🔍 **How to Run a Scan** (From UI Only)

### Step 1: Open Web Interface
```
http://localhost:3000
```

### Step 2: Login
- Username: `admin`
- Password: `admin123`

### Step 3: Go to Scans
Click **Scans** in the navigation

### Step 4: Create New Scan
1. Click **+ New Scan** button
2. Fill in details:
   - **Name**: `My Network Scan`
   - **Target**: `192.168.22.0/24` (or `192.168.22.1` for single IP)
   - **Scan Type**: 
     - **Quick Scan**: Fast (Discovery + Vulnerabilities)
     - **HVT Focused**: Focus on high-value targets
     - **Comprehensive**: Full 11-phase scan
3. Click **Start Scan**

### Step 5: Watch Progress
- Scan appears in "Active Scans" section
- Progress bar shows completion
- Phase info updates in real-time
- Auto-refreshes every 5 seconds

### Step 6: View Results
- When complete, scan moves to "Scan History"
- Shows:
  - **Devices Found**: Number of hosts discovered
  - **Vulnerabilities**: Security issues found
  - **HVT Count**: High-value targets identified
  - **Completion Time**: When scan finished

### Step 7: Drill Down
- Click on **Devices** to see what was found
- Click on **Vulnerabilities** to see security issues
- Generate a **Report** for management

---

## 🎨 **Scan Types Explained**

### **Quick Scan** (Recommended for First Run)
**Duration**: 2-5 minutes  
**Phases**:
1. Network Discovery (find hosts)
2. HVT Identification (identify important systems)
3. Vulnerability Scan (check for security issues)

**Use for**: Regular network checks, quick assessments

### **HVT Focused**
**Duration**: 5-10 minutes  
**Phases**:
1. Network Discovery
2. HVT Identification
3. Service Enumeration (what services are running)
4. Vulnerability Scan (detailed)

**Use for**: When you want to focus on critical systems (servers, firewalls, databases)

### **Comprehensive**
**Duration**: 15-30 minutes  
**Phases**: All 11 phases including:
- Discovery
- Port scanning
- Service detection
- Vulnerability scanning
- SSL/TLS testing
- Web application scanning
- Credential testing
- Exploit analysis
- Risk assessment
- Attack path mapping
- Reporting

**Use for**: Full security audit, compliance requirements

---

## 🛠️ **Troubleshooting** (From UI)

### **Scan Finds 0 Devices**

**Check Scanner Status:**
1. Go to Dashboard
2. Look at "System Status" section
3. Check "Scanner Service" indicator
   - 🟢 Green = Scanner is running
   - 🔴 Red = Scanner is offline

**If Scanner is Offline:**
```powershell
# Run this in PowerShell
.\ensure-scanner-running.ps1
```

**Then refresh the page and try again.**

### **"Failed to Load Scans" Error**

**Solution:**
1. Click **Logout**
2. Login again: `admin` / `admin123`
3. Try creating a scan again

### **Scan Stuck at "Pending"**

**Check:**
1. Dashboard → System Status → Scanner Service
2. If red, restart scanner:
   ```powershell
   .\ensure-scanner-running.ps1
   ```

### **Can't Login**

**Credentials:**
- Username: `admin`
- Password: `admin123`

**If still fails:**
```powershell
# Reset password
docker-compose exec security-api python reset_password.py
```

---

## 📈 **Real-Time Features**

### **Auto-Refresh**
- **Scans Page**: Refreshes every 5 seconds
- **Dashboard**: Refreshes every 10 seconds
- No need to manually refresh!

### **Live Progress**
- Progress bars update automatically
- Phase information shows current activity
- Device count increases as discovered

### **Instant Notifications**
- Red badges for critical issues
- Status indicators for scan progress
- Active scan counter in navigation

---

## 🔐 **Security Features**

### **Authentication**
- JWT-based authentication
- Secure password hashing (bcrypt)
- Session management
- Auto-logout on token expiration

### **Authorization**
- Role-based access control (admin, analyst, viewer)
- Protected API endpoints
- Secure scanner communication

### **Data Protection**
- API keys stored securely
- Database credentials in environment variables
- Scanner service isolated in WSL2

---

## 📊 **What Gets Scanned**

### **Quick Scan Discovers:**
- 💻 **Devices**: IP addresses, hostnames, MAC addresses
- 🌐 **Network**: Online status, response times
- ⚠️ **Vulnerabilities**: Known security issues
- 🎯 **HVTs**: Servers, firewalls, databases, domain controllers

### **Comprehensive Scan Also Finds:**
- 🔌 **Open Ports**: Which ports are accessible
- 🔧 **Services**: What software is running (Apache, MySQL, SSH, etc.)
- 🔒 **SSL/TLS**: Certificate issues, weak ciphers
- 🌐 **Web Apps**: Web server vulnerabilities
- 🔑 **Weak Credentials**: Default passwords, weak authentication
- 📊 **Risk Assessment**: Overall security posture
- 🎯 **Attack Paths**: How an attacker could compromise systems

---

## 🎯 **Quick Reference**

### **URLs**
- **Web Interface**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Scanner**: http://localhost:9000

### **Credentials**
- **Username**: `admin`
- **Password**: `admin123`

### **Commands**
```powershell
# Start everything
.\start-platform.bat

# Check scanner
.\ensure-scanner-running.ps1

# Start Docker only
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs security-api
docker-compose logs security-frontend

# Restart frontend
docker-compose restart security-frontend
```

### **Test Targets**
- **Single IP**: `192.168.22.1`
- **IP Range**: `192.168.22.0/24` (your whole network)
- **Multiple IPs**: `192.168.22.1,192.168.22.10,192.168.22.20`

---

## ✨ **Pro Tips**

### **1. Use Quick Scan First**
Start with a quick scan to see what's on your network, then run comprehensive scans on specific targets.

### **2. Check Dashboard Regularly**
The dashboard shows at-a-glance security status. Check it daily!

### **3. Generate Reports**
After scans, generate reports for documentation and compliance.

### **4. Configure AI**
Add OpenAI or Anthropic API keys in Settings for AI-powered analysis and recommendations.

### **5. Monitor HVTs**
Pay special attention to high-value targets - these are your most critical systems.

---

## 🚀 **You're All Set!**

Everything is now managed from the web interface:
- ✅ Create and manage scans
- ✅ View discovered devices
- ✅ Analyze vulnerabilities
- ✅ Generate reports
- ✅ Configure settings
- ✅ Monitor system health

**No command line needed for normal operation!**

---

## 📞 **Quick Help**

### **Scanner Not Running?**
```powershell
.\ensure-scanner-running.ps1
```

### **Need to Restart Everything?**
```powershell
docker-compose restart
.\ensure-scanner-running.ps1
```

### **Fresh Start?**
```powershell
docker-compose down
.\start-platform.bat
```

---

**Now go create your first scan! 🎯**

1. Open: http://localhost:3000
2. Login: admin / admin123
3. Scans → + New Scan
4. Target: 192.168.22.0/24
5. Start Scan!

**Watch it discover your network in real-time!** ✨

