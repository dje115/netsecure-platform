# Installation Guide

## Prerequisites

- **Windows 10/11** with Administrator access
- **8GB RAM minimum** (16GB recommended)
- **50GB free disk space**
- **Internet connection** for downloading tools and updates

## Quick Installation (Recommended)

### Step 1: Run the Automated Installer

1. Right-click `install-security-platform.bat` and select **"Run as Administrator"**
2. Follow the on-screen instructions
3. The installer will:
   - Enable and install WSL2
   - Install Kali Linux distribution
   - Set up Docker Desktop
   - Install all security tools
   - Configure the platform

### Step 2: Configure Environment

1. After installation, edit the `.env` file:
```bash
notepad .env
```

2. Add your API keys:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 3: Start the Platform

```bash
docker-compose up -d
```

Access the platform at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Installation

### 1. Install WSL2

```powershell
# Run as Administrator
wsl --install
```

Restart your computer after installation.

### 2. Install Kali Linux

```powershell
wsl --install -d kali-linux
```

Set up your Kali Linux username and password when prompted.

### 3. Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop
2. Install and restart
3. Open Docker Desktop Settings
4. Go to **Resources** → **WSL Integration**
5. Enable integration with **Kali Linux**

### 4. Set Up Security Tools in WSL2

```bash
# Open Kali Linux
wsl -d kali-linux

# Navigate to project directory
cd /mnt/c/Users/YOUR_USERNAME/Documents/Netsecure

# Make setup script executable
chmod +x wsl-setup.sh

# Run setup script
./wsl-setup.sh
```

This will install:
- Network discovery tools (nmap, arp-scan, masscan)
- Service enumeration tools (nikto, enum4linux, smbclient)
- Credential testing tools (hydra, crackmapexec)
- Web security tools (sqlmap, ffuf)
- TLS/SSL testing tools (sslscan, testssl.sh)
- Python security libraries

### 5. Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit configuration
notepad .env
```

### 6. Start Services

```bash
# Start all containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Verify Installation

### Check Services

1. **Backend API**: http://localhost:8000/health
2. **Frontend**: http://localhost:3000
3. **API Documentation**: http://localhost:8000/docs

### Check WSL2 Scanner Service

```bash
wsl -d kali-linux curl http://localhost:9000
```

Should return: `{"status": "online", "service": "Security Scanner Service"}`

### Test Scanner Tools

```bash
# SSH into WSL2
wsl -d kali-linux

# Test nmap
nmap --version

# Test scanner service
sudo systemctl status security-scanner
```

## Troubleshooting

### WSL2 Issues

**Problem**: WSL2 not installed
```powershell
# Check WSL status
wsl --status

# Update WSL
wsl --update
```

**Problem**: Can't access network from WSL2
```bash
# Check network connectivity
ping 8.8.8.8

# Restart WSL
wsl --shutdown
wsl -d kali-linux
```

### Docker Issues

**Problem**: Docker containers not starting
```bash
# Check Docker daemon
docker ps

# Restart Docker Desktop
# Open Docker Desktop and click "Restart"

# View container logs
docker-compose logs
```

**Problem**: Permission denied errors
```bash
# Run as administrator or add user to docker group
# In WSL2:
sudo usermod -aG docker $USER
```

### Scanner Service Issues

**Problem**: Scanner service not running
```bash
# Check service status
wsl -d kali-linux sudo systemctl status security-scanner

# Restart service
wsl -d kali-linux sudo systemctl restart security-scanner

# View service logs
wsl -d kali-linux journalctl -u security-scanner -f
```

**Problem**: Permission denied for scans
```bash
# Some tools require root privileges
# The service is configured to run with appropriate permissions
# If issues persist, check sudoers configuration
```

### Database Issues

**Problem**: Database connection failed
```bash
# Check PostgreSQL container
docker-compose logs security-db

# Restart database
docker-compose restart security-db

# Connect manually to test
docker exec -it security-db psql -U security_admin -d security_platform
```

## Network Configuration

### Allow Scanning on Local Network

The platform needs to perform network scans. Ensure:

1. **Firewall**: Allow Docker and WSL2 network access
2. **Antivirus**: Whitelist the project directory
3. **Network**: Run from a network where scanning is authorized

### Configure Scan Targets

**IMPORTANT**: Only scan networks you own or have explicit permission to test.

```bash
# Edit target ranges in .env or through the web interface
# Example: 192.168.1.0/24 for home network
```

## Post-Installation

### Create Admin User

1. Access frontend: http://localhost:3000
2. Click "Register"
3. Create your admin account

### Configure AI Services

1. Go to Settings
2. Add your API keys:
   - OpenAI API Key for GPT-4 analysis
   - Anthropic API Key for Claude analysis

### Start Your First Scan

1. Navigate to "Scans" page
2. Click "+ New Scan"
3. Configure:
   - **Name**: My First Scan
   - **Target Range**: 192.168.1.0/24
   - **Scan Type**: Quick Discovery
4. Click "Start Scan"

## Updating the Platform

```bash
# Pull latest changes
git pull origin master

# Rebuild containers
docker-compose down
docker-compose build
docker-compose up -d

# Update WSL2 tools
wsl -d kali-linux
cd /mnt/c/Users/YOUR_USERNAME/Documents/Netsecure
./wsl-setup.sh
```

## Uninstallation

### Stop Services

```bash
docker-compose down -v
```

### Remove WSL2 Distribution (Optional)

```powershell
wsl --unregister kali-linux
```

### Remove Docker Containers (Optional)

```bash
docker system prune -a --volumes
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/dje115/netsecure-platform/issues
- Documentation: https://github.com/dje115/netsecure-platform/tree/master/docs
