# 📖 User Guide - Security Assessment Platform

## 🚀 Getting Started

### Step 1: Access the Platform

Open your web browser and navigate to:
```
http://localhost:3000
```

### Step 2: Create Your Account

1. Click the **"Sign Up"** button or link
2. Fill in your details:
   - **Username**: Your desired username (e.g., "admin")
   - **Email**: Your email address
   - **Password**: A secure password (min 8 characters)
3. Click **"Sign Up"**

**Important**: The first user to register automatically becomes an **administrator** with full access!

### Step 3: Login

1. Enter your username and password
2. Click **"Sign In"**
3. You'll be redirected to the dashboard

---

## 🎯 How to Run Your First Scan

### Creating a New Scan

1. Navigate to the **"Scans"** page from the sidebar
2. Click the **"+ New Scan"** button (top right)
3. Fill in the scan details:

#### Scan Configuration

**Scan Name**
```
Example: "Office Network Scan"
```
A descriptive name for your scan

**Target Range**
```
Examples:
- Single IP: 192.168.1.100
- IP Range: 192.168.1.1-192.168.1.254  
- CIDR: 192.168.1.0/24
- Multiple: 192.168.1.0/24,10.0.0.0/24
```

**Scan Type** (Choose one)
- **Quick Scan** - Fast discovery + vulnerabilities (~5-10 min)
  - Phase 1: Network Discovery
  - Phase 2: HVT Identification  
  - Phase 4: Vulnerability Scanning
  
- **HVT Focused** - High-Value Targets analysis (~15-20 min)
  - Phase 1: Network Discovery
  - Phase 2: HVT Identification
  - Phase 3: Service Enumeration
  - Phase 4: Vulnerability Scanning
  
- **Comprehensive** - Complete assessment (~30-60 min)
  - All 11 phases including:
    - Network Discovery
    - HVT Identification
    - Service Enumeration
    - Vulnerability Scanning
    - Credential Testing
    - Web Application Security
    - Active Directory Assessment
    - IoT & Network Devices
    - TLS Configuration
    - Exploit Validation
    - Lateral Movement Analysis

4. Click **"Start Scan"**

---

## 📊 Monitoring Your Scan

### Real-Time Updates

The Scans page automatically refreshes every 5 seconds to show:

- **Active Scans**: Currently running scans
  - Progress bar showing completion percentage
  - Current phase number (e.g., "Phase 2/11")
  - Status indicator (🔄 Running, ⏳ Pending)
  
- **Scan History**: Completed and failed scans
  - Total devices found
  - Vulnerabilities discovered
  - High-Value Targets identified
  - Completion timestamp

### Scan Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| ⏳ | Pending | Scan queued, waiting to start |
| 🔄 | Running | Scan in progress |
| ✅ | Completed | Scan finished successfully |
| ❌ | Failed | Scan encountered an error |

### Stopping a Scan

If you need to stop a running scan:
1. Find the scan in the "Active Scans" section
2. Click the **"Stop"** button
3. The scan will halt and save partial results

---

## 🔍 Understanding Scan Results

### Dashboard Overview

After a scan completes, view the Dashboard for:

- **Total Devices**: Number of devices discovered on the network
- **Vulnerabilities**: Security issues found
- **High-Value Targets**: Critical assets identified
- **Risk Score**: Overall network security score (0-100)

### Device Information

Each discovered device shows:
- **IP Address**: Device network address
- **Hostname**: Device name (if available)
- **Device Type**: Classification (server, workstation, router, etc.)
- **Operating System**: Detected OS version
- **HVT Status**: Whether it's a high-value target
- **Risk Level**: Low, Medium, High, or Critical

### Vulnerability Details

For each vulnerability discovered:
- **CVE ID**: Official vulnerability identifier
- **Severity**: Critical, High, Medium, or Low
- **CVSS Score**: Industry standard score (0-10)
- **Affected Service**: Which service is vulnerable
- **Remediation**: How to fix the issue
- **Exploitability**: Whether known exploits exist

---

## 📈 Example Scan Workflow

### Scenario: Scanning Your Home/Office Network

**1. Determine Your Network Range**
```bash
# On Windows, open Command Prompt:
ipconfig

# Look for "IPv4 Address" - if it's 192.168.1.x, your network is likely 192.168.1.0/24
```

**2. Create the Scan**
- Name: "Home Network Security Scan"
- Target: "192.168.1.0/24"
- Type: "Quick Scan" (for first time)

**3. Wait for Results** (5-10 minutes)
The scan will:
- Discover all active devices
- Identify device types
- Check for common vulnerabilities
- Assess risk levels

**4. Review Findings**
- Check the Dashboard for summary statistics
- Navigate to "Devices" to see all discovered hosts
- Go to "Vulnerabilities" to see security issues
- Generate a report for detailed analysis

---

## 🎨 User Interface Guide

### Navigation Bar

| Menu Item | Description |
|-----------|-------------|
| **Dashboard** | Overview of all scans, devices, and vulnerabilities |
| **Scans** | Create, manage, and monitor security scans |
| **Devices** | View discovered devices and their details |
| **Vulnerabilities** | List of security issues found |
| **Reports** | Generate and download assessment reports |

### Dashboard Widgets

**Active Scans Widget**
- Shows currently running scans
- Real-time progress updates
- Quick stop button

**Statistics Cards**
- Total Devices Found
- Critical Vulnerabilities
- High-Value Targets
- Overall Risk Score

**Recent Activity**
- Latest scan completions
- New vulnerabilities discovered
- HVT identifications

---

## 🛡️ Security Best Practices

### Before Scanning

✅ **Get Permission**
- Only scan networks you own or have explicit authorization to test
- Unauthorized network scanning is illegal in most jurisdictions

✅ **Plan Your Scan**
- Choose appropriate scan times (off-hours for production networks)
- Start with Quick Scans to test
- Use Comprehensive scans for thorough assessments

✅ **Backup Important Data**
- While scans are non-destructive, always have backups
- Ensure critical systems are stable before scanning

### During Scanning

✅ **Monitor Progress**
- Watch for any network disruptions
- Stop scans if you notice issues
- Check logs for errors or warnings

✅ **Network Impact**
- Scans generate network traffic
- Quick scans: Low impact
- Comprehensive scans: Moderate impact

### After Scanning

✅ **Review Results Carefully**
- Not all findings are critical
- Verify false positives
- Prioritize by severity and exploitability

✅ **Take Action**
- Fix Critical and High vulnerabilities first
- Patch systems regularly
- Secure High-Value Targets with extra protection

✅ **Generate Reports**
- Document your findings
- Share with IT/security teams
- Track remediation progress

---

## 🔑 Advanced Features

### API Access

You can interact with the platform programmatically:

**Get API Token**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

**Create Scan via API**
```bash
curl -X POST http://localhost:8000/api/scans \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Scan",
    "target_range": "192.168.1.0/24",
    "scan_type": "quick"
  }'
```

**List All Scans**
```bash
curl http://localhost:8000/api/scans \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### API Documentation

Access interactive API docs:
```
http://localhost:8000/docs
```

Test all endpoints directly from your browser!

---

## 📊 Report Generation

### Creating Reports

1. Navigate to **"Reports"** page
2. Click **"Generate Report"**
3. Select:
   - Scan to report on
   - Report type (Executive, Technical, Compliance)
   - Format (HTML, PDF, DOCX)
4. Click **"Generate"**

### Report Types

**Executive Summary**
- High-level overview
- Risk assessment
- Key findings
- Recommendations
- Ideal for management/executives

**Technical Report**
- Detailed vulnerability information
- Exploitation steps
- Remediation procedures
- Technical details
- For IT/Security teams

**Compliance Report**
- Compliance status
- Gap analysis
- Regulatory requirements
- Audit trail
- For compliance officers

---

## ❓ Troubleshooting

### "Scan Won't Start"

**Check:**
1. Is the target range valid?
2. Do you have network connectivity?
3. Is the WSL2 scanner service running?
4. Check logs in the API container

**Solution:**
```bash
# Check scanner service status
docker-compose logs security-api | grep scanner
```

### "No Devices Found"

**Possible Causes:**
1. Incorrect network range
2. Firewall blocking scan traffic
3. Devices not responding to probes

**Solution:**
- Verify network range with `ipconfig` or `ifconfig`
- Test connectivity: `ping <target_ip>`
- Try scanning a single known-active IP first

### "Authentication Failed"

**Solution:**
1. Clear browser cache and cookies
2. Logout and login again
3. Check that your password is correct
4. Verify the API is running: `docker-compose ps`

### "Scan Stuck/Not Progressing"

**Solution:**
1. Wait a few minutes (some phases take time)
2. Check if the scanner service is responding
3. Stop and restart the scan
4. Check container logs:
```bash
docker-compose logs security-api
docker-compose logs security-celery
```

---

## 💡 Tips & Tricks

### Faster Scans
- Use Quick Scan for initial discovery
- Scan smaller network ranges
- Schedule comprehensive scans during off-hours

### Better Results
- Keep the scanner tools updated
- Configure AI API keys for enhanced analysis
- Run regular scans to track changes over time

### Organization
- Use descriptive scan names
- Tag scans with dates or purposes
- Generate reports after each scan

### Security
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Logout when not using the platform
- Regularly review scan history
- Delete old scans to free space

---

## 📞 Getting Help

### Documentation
- **Installation Guide**: `INSTALLATION.md`
- **Quick Start**: `QUICK-START.md`
- **WSL2 Setup**: `WSL2-SETUP.md`
- **Test Results**: `TEST-RESULTS.md`

### API Reference
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### GitHub Repository
https://github.com/dje115/netsecure-platform

### Common Commands

**Restart Services**
```bash
docker-compose restart
```

**View Logs**
```bash
docker-compose logs -f security-api
```

**Stop All Services**
```bash
docker-compose down
```

**Start All Services**
```bash
docker-compose up -d
```

---

## 🎉 You're Ready!

You now have everything you need to:
✅ Run security scans
✅ Discover network devices
✅ Find vulnerabilities
✅ Identify high-value targets
✅ Generate professional reports

**Start by running a Quick Scan on a small network range and explore the results!**

---

**Remember**: Always scan responsibly and only on networks you're authorized to assess. 🛡️

