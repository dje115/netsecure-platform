# **Professional Security Assessment Platform - Complete Development Prompt**

## **Project Overview**
Create a comprehensive, enterprise-grade security assessment platform that provides multi-phase network discovery, vulnerability scanning, AI-powered analysis, and professional reporting capabilities. This should be a professional tool suitable for security consultants and penetration testers with advanced workflow capabilities.

## **Core Architecture Requirements**

### **Technology Stack**
- **Backend**: FastAPI (Python) with PostgreSQL database
- **Frontend**: React.js with Tailwind CSS for modern, responsive UI
- **Infrastructure**: Docker Compose with WSL2 on Windows for optimal network access
- **OS**: Kali Linux (WSL2) for comprehensive security tools
- **AI Integration**: OpenAI GPT-4 and Anthropic Claude API support

### **Database Schema Requirements**
- **Users**: Authentication, roles, permissions
- **Scan Sessions**: Track all scanning activities with timestamps and phases
- **Devices**: IP, MAC, vendor, hostname, OS, services, ports, HVT classification
- **Vulnerabilities**: CVE integration, severity, CVSS scores, remediation, exploitability
- **Services**: Detailed service enumeration results
- **Credentials**: Weak credential testing results
- **Attack Paths**: Lateral movement and persistence simulation results
- **AI Analysis**: Risk assessments, device classification, recommendations
- **Reports**: Generated reports with executive and technical summaries

## **Multi-Phase Security Assessment Workflow**

### **Phase 1: Initial Network Discovery**
```bash
# Step 1: ARP Scan for local network discovery
arp-scan -l --interface eth0

# Step 2: Nmap host discovery with hostname resolution
nmap -sn -R <target_range>

# Step 3: Service and OS detection on live hosts
nmap -sS -sV -O -A <live_hosts>

# Step 4: Additional hostname discovery
nbtscan <network_range>
avahi-browse -a -t
```

### **Phase 2: High-Value Target (HVT) Identification**
- **Domain Controllers**: Active Directory servers
- **DMZ Servers**: Internet-facing infrastructure
- **Gateway/Firewalls**: Network perimeter devices
- **Credential Storage**: Systems with PII and authentication data
- **Critical Services**: Database servers, file shares, authentication systems

### **Phase 3: Service-Level Enumeration**
```bash
# HTTP Services
nikto -h <target>
wpscan --url <target>
ffuf -w wordlist.txt -u <target>/FUZZ

# SMB/Windows Services
enum4linux -a <target>
smbclient -L <target>
crackmapexec smb <target>

# SSH Services
nmap --script ssh-* <target>

# RDP Services
nmap --script rdp-* <target>

# SNMP Services
snmpwalk -c public <target>
nmap --script snmp-* <target>

# Database Services
nmap --script mysql-*,postgresql-*,mssql-* <target>
```

### **Phase 4: Vulnerability Scanning**
```bash
# Nmap vulnerability scripts
nmap --script vuln <target>

# OpenVAS/GVM integration
# Nessus integration (if licensed)

# Custom vulnerability checks
sslscan <target>
testssl.sh <target>
```

### **Phase 5: Authentication & Password Testing**
```bash
# SSH brute force
hydra -l admin -P passwords.txt ssh://<target>

# RDP brute force
hydra -l administrator -P passwords.txt rdp://<target>

# SMB brute force
crackmapexec smb <target> -u users.txt -p passwords.txt

# Web application login testing
hydra -l admin -P passwords.txt <target> http-post-form "/login:username=^USER^&password=^PASS^:Invalid"
```

### **Phase 6: Web Application Security**
```bash
# Burp Suite integration
# OWASP ZAP integration

# Hidden endpoint discovery
ffuf -w wordlist.txt -u <target>/FUZZ

# SQL injection testing
sqlmap -u <target> --batch

# WordPress security
wpscan --url <target> --enumerate u,p,t
```

### **Phase 7: Active Directory & Windows Environment**
```bash
# AD enumeration
enum4linux -a <target>
ldapsearch -x -H ldap://<target>

# BloodHound data collection
bloodhound-python -d <domain> -u <user> -p <pass> -gc <dc> -c all

# SMB exploitation
smbclient //<target>/share
rpcclient -U "" <target>
```

### **Phase 8: IoT & Network Device Security**
```bash
# SNMP enumeration
snmpwalk -c public <target>
snmp-check <target>

# Network device specific checks
nmap --script snmp-* <target>
```

### **Phase 9: TLS & Configuration Security**
```bash
# SSL/TLS testing
sslscan <target>
testssl.sh <target>
nmap --script ssl-* <target>

# Certificate analysis
openssl s_client -connect <target>:443
```

### **Phase 10: Exploit Validation (Controlled)**
```bash
# Metasploit integration (non-destructive)
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target>
check

# Custom proof-of-concept validation
# Only with explicit permission
```

### **Phase 11: Lateral Movement Simulation**
```bash
# Pass-the-Hash attacks
crackmapexec smb <target> -u <user> -H <hash>

# RDP pivoting
xfreerdp /v:<target> /u:<user> /p:<pass>

# SMB abuse
smbclient //<target>/share -U <user>%<pass>
```

## **Required Data Collection**

### **Device Information**
- **IP Address**: Primary identifier
- **MAC Address**: Hardware identification
- **Vendor**: OUI lookup for manufacturer
- **Hostname**: DNS, NetBIOS, mDNS resolution
- **OS Detection**: Operating system and version
- **Open Ports**: Services and versions
- **HVT Classification**: High-value target identification
- **Risk Assessment**: AI-powered security evaluation

### **Service Enumeration**
- **HTTP Services**: Web applications, frameworks, versions
- **SMB Services**: Shares, users, permissions
- **SSH Services**: Configuration, key types, versions
- **RDP Services**: Authentication methods, encryption
- **SNMP Services**: Community strings, OIDs, sensitive data
- **Database Services**: Types, versions, authentication

### **Vulnerability Data**
- **CVE Information**: CVSS scores, exploitability
- **Configuration Issues**: Misconfigurations, weak settings
- **Authentication Weaknesses**: Default credentials, weak passwords
- **Network Vulnerabilities**: Protocol weaknesses, encryption issues

### **Attack Path Analysis**
- **Lateral Movement**: Potential attack vectors
- **Privilege Escalation**: Local and remote escalation paths
- **Persistence**: Methods for maintaining access
- **Data Exfiltration**: Sensitive data access paths

## **User Interface Requirements**

### **Dashboard Page**
- **Status Indicators**: Green/Red/Yellow lights for service status
- **Live Device List**: Real-time network device discovery
- **HVT Indicators**: High-value target identification
- **Scan Progress**: Visual progress bars and status updates
- **Phase Tracking**: Current assessment phase
- **Quick Actions**: Start scan, generate report, view vulnerabilities
- **Metrics Cards**: Total devices, vulnerabilities, risk score, HVTs

### **Scan Management**
- **Phase Selection**: Choose assessment phases
- **Target Configuration**: Network ranges, specific hosts
- **Tool Selection**: Enable/disable specific tools
- **Credential Management**: Password lists, user accounts
- **Live Results**: Real-time discovery during scans
- **Progress Tracking**: Phase-by-phase progress

### **Device Details View**
- **Device Information**: IP, MAC, vendor, hostname, OS
- **HVT Status**: High-value target classification
- **Ports & Services**: Open ports with service details
- **Vulnerabilities**: CVE data with severity indicators
- **Attack Paths**: Potential lateral movement vectors
- **AI Insights**: Device purpose, security recommendations
- **Network Topology**: Visual network map with attack paths

### **Vulnerability Management**
- **Severity Filtering**: Critical, High, Medium, Low
- **Exploitability**: Known exploits, proof-of-concept
- **Remediation**: Step-by-step fixes
- **Validation**: Exploit testing results
- **Trending**: Vulnerability patterns over time

### **Attack Path Visualization**
- **Network Graph**: Visual attack path mapping
- **Privilege Escalation**: Local and remote escalation
- **Lateral Movement**: Cross-system attack vectors
- **Data Access**: Sensitive information access paths
- **Persistence**: Long-term access methods

## **AI Integration Requirements**

### **Device Classification**
- **Purpose Detection**: Server, workstation, IoT device, network equipment
- **HVT Identification**: Critical infrastructure, credential storage
- **Risk Assessment**: Security posture evaluation
- **Attack Surface**: Potential attack vectors
- **Recommendations**: Specific security improvements

### **Vulnerability Analysis**
- **Exploitability Prediction**: Likelihood of successful exploitation
- **Impact Assessment**: Potential damage from exploitation
- **Remediation Priority**: Order of security fixes
- **Threat Modeling**: Attack scenario development

### **API Key Management**
- **OpenAI Integration**: GPT-4 for analysis and recommendations
- **Anthropic Claude**: Alternative AI provider support
- **Configuration UI**: Easy API key management
- **Fallback Logic**: Multiple AI provider support

## **Professional Features**

### **Visual Design**
- **Status Lights**: Green/Red/Yellow indicators for all services
- **Progress Bars**: Real-time scan progress by phase
- **Data Tables**: Sortable, filterable device and vulnerability lists
- **Charts**: Risk distribution, vulnerability trends, attack paths
- **Network Graphs**: Visual attack path mapping
- **Responsive Design**: Works on desktop and tablet

### **Scan Types**
- **Quick Discovery**: Fast network discovery (5-10 minutes)
- **Comprehensive Assessment**: Full multi-phase assessment (2-4 hours)
- **HVT Focus**: High-value target specific assessment
- **Vulnerability Scan**: CVE and misconfiguration focused
- **Custom Assessment**: User-defined phases and tools
- **Scheduled Scans**: Automated recurring assessments

### **CVE Integration**
- **Real-time Lookup**: Service and vendor-based CVE matching
- **Severity Scoring**: CVSS v3.1 integration
- **Exploitability**: Known exploit availability
- **Remediation**: Patch and mitigation guidance
- **Validation**: Controlled exploit testing

## **Technical Implementation**

### **Docker Services**
```yaml
services:
  - security-db (PostgreSQL)
  - security-api (FastAPI backend)
  - security-frontend (React.js)
  - network-scanner (Kali Linux with tools)
  - service-enumerator (Service-specific enumeration)
  - vulnerability-scanner (CVE and misconfiguration scanning)
  - credential-tester (Password and authentication testing)
  - web-scanner (Web application security testing)
  - ad-scanner (Active Directory and Windows testing)
  - iot-scanner (IoT and network device testing)
  - tls-scanner (SSL/TLS configuration testing)
  - exploit-validator (Controlled exploit validation)
  - lateral-movement (Attack path simulation)
  - ai-advisor (AI analysis service)
  - cve-intelligence (CVE lookup service)
  - report-generator (Report creation service)
```

### **Security Tools Integration**
- **Network Discovery**: nmap, arp-scan, nbtscan, avahi-browse, masscan
- **Service Enumeration**: nmap NSE, nikto, wpscan, enum4linux, smbclient, rpcclient
- **Vulnerability Scanning**: nmap vuln scripts, OpenVAS, Nessus
- **Credential Testing**: hydra, medusa, crackmapexec
- **Web Security**: Burp Suite, OWASP ZAP, ffuf, sqlmap
- **AD Security**: bloodhound, impacket, crackmapexec
- **IoT Security**: snmpwalk, snmp-check
- **TLS Security**: sslscan, testssl.sh
- **Exploit Validation**: Metasploit, custom PoCs

### **Database Schema**
```sql
-- Core tables
users, scan_sessions, devices, ports, services, vulnerabilities, cves
-- HVT and attack path tables
hvt_classifications, attack_paths, lateral_movement, persistence
-- Service enumeration tables
service_enumerations, credential_tests, web_apps, ad_objects
-- AI and reporting tables
ai_analysis, reports, remediation_guides
```

## **Installation & Deployment**

### **Windows WSL2 Setup**
- **One-click installer**: Automated WSL2 + Kali Linux setup
- **Docker Desktop**: Integrated container management
- **Network Access**: Host network mode for scanning
- **Tool Installation**: All security tools pre-installed
- **Credential Lists**: Common password and username lists

### **Easy Installation**
```bash
# Windows batch file
install-security-platform.bat
# Automated setup of WSL2, Docker, and platform
```

## **Professional Output Requirements**

### **Reports Must Include**
- **Executive Summary**: Business-focused risk overview
- **Technical Details**: Comprehensive vulnerability data
- **HVT Analysis**: High-value target identification and risks
- **Attack Paths**: Visual attack path mapping
- **Device Inventory**: Complete asset list with AI classifications
- **Network Topology**: Visual network map with attack vectors
- **Remediation Steps**: Actionable security improvements
- **Compliance**: Industry standard formatting

### **Visual Elements**
- **Charts**: Risk distribution, vulnerability trends, attack paths
- **Tables**: Sortable device and vulnerability lists
- **Status Indicators**: Service and security status
- **Progress Tracking**: Real-time scan progress by phase
- **Network Graphs**: Attack path visualization
- **Export Options**: Multiple format support

## **Quality Standards**

### **Performance**
- **Fast Scanning**: Optimized for speed and accuracy
- **Real-time Updates**: Live results during scans
- **Responsive UI**: Smooth user experience
- **Efficient Database**: Optimized queries and indexing
- **Parallel Processing**: Multi-threaded scanning

### **Reliability**
- **Error Handling**: Graceful failure management
- **Data Validation**: Input sanitization and verification
- **Backup Systems**: Data persistence and recovery
- **Logging**: Comprehensive audit trails
- **Phase Recovery**: Resume interrupted scans

### **Security**
- **Authentication**: Secure user management
- **API Security**: Token-based authentication
- **Data Protection**: Encrypted sensitive information
- **Network Security**: Secure scanning practices
- **Credential Safety**: Secure storage of test credentials

## **Success Criteria**

The platform should provide:
1. **Professional Interface**: Enterprise-grade UI/UX
2. **Comprehensive Scanning**: Multi-phase network discovery and analysis
3. **HVT Identification**: High-value target classification
4. **Attack Path Mapping**: Visual lateral movement analysis
5. **AI-Powered Insights**: Intelligent device classification and recommendations
6. **Quality Reports**: Professional, actionable security reports
7. **Easy Deployment**: One-click installation on Windows
8. **Scalable Architecture**: Support for large network environments
9. **Real-time Feedback**: Live scanning progress and results
10. **Status Visibility**: Clear indicators for all system components
11. **Phase Management**: Controlled multi-phase assessment workflow
12. **Credential Testing**: Safe and responsible password testing
13. **Exploit Validation**: Controlled vulnerability confirmation
14. **Lateral Movement**: Attack path simulation and mapping

This platform should be a professional-grade tool that security consultants would be proud to use with clients, providing comprehensive network assessment capabilities with AI-enhanced analysis, attack path mapping, and beautiful, actionable reporting.
