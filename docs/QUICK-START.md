# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install (Windows)

Run as Administrator:
```powershell
install-security-platform.bat
```

### 2. Configure API Keys

Edit `.env` file:
```
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### 3. Start Platform

```bash
docker-compose up -d
```

### 4. Access Web Interface

Open browser: **http://localhost:3000**

### 5. Run Your First Scan

1. Click **"Scans"** → **"+ New Scan"**
2. Enter target: `192.168.1.0/24` (or your network)
3. Select: **"Quick Discovery"**
4. Click **"Start Scan"**

## 📊 What You'll Get

### Network Discovery
- All devices on your network
- IP addresses, hostnames, vendors
- Operating system detection
- Open ports and services

### High-Value Target (HVT) Detection
- Domain controllers
- Gateways and firewalls
- Database servers
- Web servers

### Vulnerability Assessment
- CVE identification
- CVSS severity scores
- Exploitability analysis
- Remediation recommendations

### AI-Powered Analysis
- Device purpose classification
- Risk assessment
- Security recommendations
- Attack surface analysis

### Professional Reports
- Executive summary
- Technical details
- Remediation steps
- Network topology

## 🎯 Scan Types

### Quick Discovery (5-10 minutes)
- Network host discovery
- Basic port scanning
- Service identification
- Quick vulnerability check

### Comprehensive Assessment (2-4 hours)
- All 11 phases
- Deep service enumeration
- Complete vulnerability scanning
- Attack path analysis
- Credential testing

### HVT Focus (30-60 minutes)
- High-value target identification
- Critical vulnerability scanning
- Attack path mapping
- Focused analysis

### Custom Assessment
- Select specific phases
- Choose target tools
- Configure depth

## 📖 Understanding Results

### Dashboard Overview
- **Total Devices**: All discovered network devices
- **Vulnerabilities**: Total security issues found
- **Critical Issues**: Requires immediate attention
- **HVT Devices**: High-value targets identified
- **Risk Score**: Overall security posture (0-10)

### Status Indicators
- 🟢 **Green**: Secure, no issues
- 🟡 **Yellow**: Minor issues or warnings
- 🔴 **Red**: Critical issues requiring attention

### Device Details
Each device shows:
- Network information (IP, MAC, hostname)
- Operating system and type
- HVT classification (if applicable)
- Open ports and services
- Vulnerabilities detected
- AI-powered recommendations

### Vulnerability Severity
- **Critical (9.0-10.0)**: Immediate action required
- **High (7.0-8.9)**: Fix as soon as possible
- **Medium (4.0-6.9)**: Schedule for remediation
- **Low (0.1-3.9)**: Monitor and fix when convenient

## 🔧 Common Tasks

### View All Devices
1. Navigate to **"Devices"**
2. Filter by HVT or risk level
3. Click device for details

### Check Vulnerabilities
1. Navigate to **"Vulnerabilities"**
2. Filter by severity
3. Sort by CVSS score
4. Click for remediation steps

### Generate Report
1. Navigate to **"Reports"**
2. Click **"+ Generate Report"**
3. Select scan and format
4. Download when ready

### Schedule Scans
1. Go to **"Scans"** → **"Scheduled"**
2. Click **"+ New Schedule"**
3. Configure frequency
4. Save schedule

## 🔒 Security Best Practices

### Before Scanning
✅ Only scan networks you own or have permission to test  
✅ Inform network administrators  
✅ Schedule scans during low-traffic periods  
✅ Start with non-intrusive scans  

### During Scanning
✅ Monitor scan progress  
✅ Watch for network impact  
✅ Review preliminary results  
✅ Stop scan if issues occur  

### After Scanning
✅ Review all findings carefully  
✅ Validate critical vulnerabilities  
✅ Plan remediation priorities  
✅ Document changes made  
✅ Re-scan after fixes  

## 🛠️ Troubleshooting

### Scan Not Starting
- Check WSL2 scanner service: `wsl -d kali-linux sudo systemctl status security-scanner`
- Verify network connectivity
- Check target range is valid

### No Devices Found
- Verify target network range
- Check network permissions
- Ensure devices are online
- Try different discovery method

### Slow Scanning
- Large networks take longer
- Reduce scan intensity
- Use Quick Discovery for initial assessment
- Schedule comprehensive scans for off-hours

### Permission Errors
- Some tools require elevated privileges
- Scanner service runs with sudo
- Check firewall settings
- Whitelist in antivirus

## 📚 Next Steps

1. **Explore Features**: Try different scan types and options
2. **Review Documentation**: Read detailed guides in `/docs`
3. **Generate Reports**: Create professional security reports
4. **Schedule Regular Scans**: Set up automated assessments
5. **Join Community**: Get help and share feedback

## 🆘 Getting Help

- **Documentation**: Check `/docs` folder
- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: Report bugs or request features
- **Logs**: `docker-compose logs -f`

## 🎓 Learning Resources

### Understanding Results
- [CVSS Scoring Guide](https://www.first.org/cvss/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Security Tools
- [Nmap Documentation](https://nmap.org/docs.html)
- [Nikto Scanner](https://cirt.net/Nikto2)
- [OWASP ZAP](https://www.zaproxy.org/docs/)

### Best Practices
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls/)
- [SANS Security Resources](https://www.sans.org/security-resources/)

---

**Ready to scan?** Go to http://localhost:3000 and start discovering your network!
