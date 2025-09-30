# WSL2 Setup Guide for Security Tools

## Why WSL2?

WSL2 (Windows Subsystem for Linux 2) provides:
- **Full Linux kernel** for running native security tools
- **Raw socket access** for network scanning
- **Better performance** than WSL1
- **Network access** to scan local networks
- **Native tool compatibility** with Kali Linux tools

## Architecture Overview

```
┌─────────────────────────────────────────┐
│           Windows Host                   │
│  ┌─────────────────────────────────┐   │
│  │     Docker Containers            │   │
│  │  ┌──────────┐  ┌──────────┐    │   │
│  │  │ Frontend │  │ Backend  │    │   │
│  │  │  React   │  │  FastAPI │    │   │
│  │  └──────────┘  └──────────┘    │   │
│  │       ↓              ↓          │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │     PostgreSQL DB       │   │   │
│  │  └─────────────────────────┘   │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│  ┌──────────────▼──────────────────┐   │
│  │         WSL2 (Kali Linux)       │   │
│  │  ┌──────────────────────────┐  │   │
│  │  │   Scanner Service API    │  │   │
│  │  │   (Port 9000)            │  │   │
│  │  └──────────────────────────┘  │   │
│  │  ┌──────────────────────────┐  │   │
│  │  │   Security Tools         │  │   │
│  │  │   • nmap                 │  │   │
│  │  │   • nikto                │  │   │
│  │  │   • hydra                │  │   │
│  │  │   • crackmapexec         │  │   │
│  │  │   • sqlmap               │  │   │
│  │  │   • sslscan              │  │   │
│  │  └──────────────────────────┘  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Installation Steps

### 1. Enable WSL2

**Option A: Using PowerShell (Recommended)**
```powershell
# Run as Administrator
wsl --install
```

**Option B: Manual Installation**
```powershell
# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer

# Set WSL2 as default
wsl --set-default-version 2
```

### 2. Install Kali Linux

```powershell
# Install Kali Linux distribution
wsl --install -d kali-linux

# Or download from Microsoft Store
# Search for "Kali Linux" and install
```

### 3. Initial Kali Setup

```bash
# First time launch will prompt for username/password
# Create your Linux user account

# Update package lists
sudo apt-get update
sudo apt-get upgrade -y
```

### 4. Run Automated Setup Script

```bash
# Navigate to project directory
cd /mnt/c/Users/YOUR_USERNAME/Documents/Netsecure

# Make script executable
chmod +x wsl-setup.sh

# Run setup (installs all tools and configures scanner service)
./wsl-setup.sh
```

## What Gets Installed

### Network Discovery Tools
- **nmap**: Network mapper and port scanner
- **arp-scan**: ARP-based network discovery
- **nbtscan**: NetBIOS name scanner
- **avahi-utils**: mDNS/DNS-SD discovery
- **masscan**: Fast port scanner

### Service Enumeration Tools
- **nikto**: Web server scanner
- **enum4linux**: Windows/SMB enumeration
- **smbclient**: SMB/CIFS client
- **rpcclient**: RPC client for Windows
- **snmp**: SNMP tools

### Credential Testing Tools
- **hydra**: Network authentication cracker
- **medusa**: Parallel login brute-forcer
- **crackmapexec**: Swiss army knife for pentesting networks

### Web Security Tools
- **sqlmap**: SQL injection tool
- **ffuf**: Fast web fuzzer
- **dirb**: Web content scanner
- **gobuster**: Directory/file brute-forcer

### SSL/TLS Testing Tools
- **sslscan**: SSL/TLS scanner
- **testssl.sh**: SSL/TLS testing script
- **sslyze**: SSL/TLS analyzer

### Python Security Libraries
- **python-nmap**: Python nmap library
- **impacket**: Network protocol tools
- **pwntools**: CTF and exploit development
- **scapy**: Packet manipulation

### Wordlists
- **SecLists**: Comprehensive wordlist collection
- **rockyou.txt**: Common password list
- **Common usernames**: Custom username list
- **Common passwords**: Custom password list

## Scanner Service

### Service Architecture

The scanner service is a FastAPI application running in WSL2 that:
- Provides REST API for security tools
- Runs on port 9000
- Handles scan requests from the main backend
- Executes security tools with proper privileges
- Returns results in JSON format

### Service Management

```bash
# Check service status
sudo systemctl status security-scanner

# Start service
sudo systemctl start security-scanner

# Stop service
sudo systemctl stop security-scanner

# Restart service
sudo systemctl restart security-scanner

# Enable on boot
sudo systemctl enable security-scanner

# View logs
journalctl -u security-scanner -f
```

### Test Scanner Service

```bash
# Test basic connectivity
curl http://localhost:9000

# Should return:
# {"status": "online", "service": "Security Scanner Service"}

# Test from Windows PowerShell
curl http://localhost:9000
```

## Network Configuration

### WSL2 Network Modes

**Mirrored Mode (Windows 11 22H2+)**
- WSL2 has same IP as Windows
- Direct network access
- Better for scanning local networks

**NAT Mode (Default)**
- WSL2 has different IP
- Works through NAT
- May require port forwarding

### Configure Mirrored Mode

Create/edit `.wslconfig` in Windows user home:
```ini
[wsl2]
networkingMode=mirrored
```

Restart WSL2:
```powershell
wsl --shutdown
wsl
```

### Firewall Configuration

Allow scanner service in Windows Firewall:
```powershell
New-NetFirewallRule -DisplayName "WSL2 Scanner" -Direction Inbound -LocalPort 9000 -Protocol TCP -Action Allow
```

## Tool Usage Examples

### Nmap Scans

```bash
# Basic host discovery
nmap -sn 192.168.1.0/24

# Service version detection
nmap -sV 192.168.1.1

# OS detection (requires root)
sudo nmap -O 192.168.1.1

# Full scan with scripts
sudo nmap -sS -sV -sC -O 192.168.1.1
```

### Web Scanning

```bash
# Nikto web scan
nikto -h http://192.168.1.1

# Directory enumeration
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -u http://192.168.1.1/FUZZ

# SQL injection test
sqlmap -u "http://192.168.1.1/page?id=1" --batch
```

### SMB Enumeration

```bash
# Enumerate shares
smbclient -L //192.168.1.1

# Enum4linux full scan
enum4linux -a 192.168.1.1

# CrackMapExec
crackmapexec smb 192.168.1.1
```

### Credential Testing

```bash
# SSH brute force
hydra -l admin -P /usr/share/wordlists/common_passwords.txt ssh://192.168.1.1

# RDP brute force
hydra -l administrator -P /usr/share/wordlists/common_passwords.txt rdp://192.168.1.1

# Multiple protocols
medusa -h 192.168.1.1 -u admin -P /usr/share/wordlists/common_passwords.txt -M ssh
```

### SSL/TLS Testing

```bash
# SSL scan
sslscan 192.168.1.1:443

# Comprehensive SSL test
testssl.sh https://192.168.1.1
```

## Troubleshooting

### WSL2 Won't Start

```powershell
# Check WSL status
wsl --status

# Update WSL
wsl --update

# Restart WSL
wsl --shutdown
wsl
```

### Network Issues

```bash
# Check network connectivity
ping 8.8.8.8

# Check DNS
nslookup google.com

# Reset network
sudo ip addr flush dev eth0
sudo dhclient eth0
```

### Permission Errors

```bash
# Some tools need root
sudo nmap -O 192.168.1.1

# Add user to sudo group
sudo usermod -aG sudo $USER

# Configure passwordless sudo for scanner (done by setup script)
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/nmap" | sudo tee /etc/sudoers.d/scanner
```

### Service Not Starting

```bash
# Check logs
journalctl -u security-scanner -n 50

# Test manually
cd ~/security-platform/scanner
source venv/bin/activate
python scanner_service.py

# Check port conflicts
sudo lsof -i :9000
```

### Tool Installation Issues

```bash
# Update package cache
sudo apt-get update

# Fix broken packages
sudo apt-get install -f

# Reinstall specific tool
sudo apt-get install --reinstall nmap
```

## Performance Optimization

### Resource Allocation

Edit `.wslconfig`:
```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
```

### Scan Performance

```bash
# Fast scan (fewer checks)
nmap -T5 -F 192.168.1.0/24

# Parallel scanning
nmap --min-parallelism 100 192.168.1.0/24

# Masscan for fast port discovery
sudo masscan -p1-65535 192.168.1.0/24 --rate=1000
```

## Security Considerations

### Legal and Ethical

⚠️ **IMPORTANT**: Only scan networks you own or have explicit permission to test.

- Unauthorized scanning is illegal
- Always get written permission
- Follow responsible disclosure practices
- Respect privacy and data protection laws

### Tool Safety

```bash
# Use non-intrusive scans first
nmap -sn 192.168.1.0/24  # Safe host discovery

# Avoid aggressive scans on production
nmap -T2 192.168.1.1  # Slower, less intrusive

# Test on isolated networks first
# Set up a lab environment for practice
```

### Data Protection

```bash
# Secure scan results
chmod 600 ~/security-platform/scan_results/*

# Encrypt sensitive data
gpg -c sensitive_scan.txt

# Clean up after testing
rm -rf ~/security-platform/scan_results/*
```

## Advanced Configuration

### Custom Tool Integration

Add your own tools to the scanner service:

```python
# Edit ~/security-platform/scanner/scanner_service.py

@app.post("/scan/custom-tool")
async def custom_tool_scan(request: ScanRequest):
    try:
        result = subprocess.run(
            ['your-tool', '--option', request.target],
            capture_output=True,
            text=True,
            timeout=300
        )
        return {"status": "completed", "output": result.stdout}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
```

### Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc

# Custom wordlist location
export WORDLISTS=/usr/share/wordlists

# Scanner API configuration
export SCANNER_HOST=0.0.0.0
export SCANNER_PORT=9000

# Tool timeouts
export SCAN_TIMEOUT=600
```

## Backup and Restore

### Backup WSL2 Distribution

```powershell
# Export WSL2 distribution
wsl --export kali-linux C:\Backups\kali-backup.tar

# Import on new machine
wsl --import kali-linux C:\WSL\kali C:\Backups\kali-backup.tar
```

### Backup Scanner Configuration

```bash
# Backup configuration
tar -czf scanner-config-backup.tar.gz ~/security-platform/scanner/

# Restore
tar -xzf scanner-config-backup.tar.gz -C ~/
```

## Additional Resources

- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Kali Linux Documentation](https://www.kali.org/docs/)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---

**Need help?** Check the [Troubleshooting](#troubleshooting) section or open an issue on GitHub.

