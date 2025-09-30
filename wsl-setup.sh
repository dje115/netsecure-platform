#!/bin/bash

# WSL2 Security Tools Setup Script
# This script sets up Kali Linux in WSL2 with all required security tools

set -e

echo "=================================="
echo "Security Platform - WSL2 Setup"
echo "=================================="

# Update system
echo "[+] Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install essential tools
echo "[+] Installing essential packages..."
sudo apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    net-tools \
    iputils-ping

# Install network discovery tools
echo "[+] Installing network discovery tools..."
sudo apt-get install -y \
    nmap \
    arp-scan \
    nbtscan \
    avahi-utils \
    masscan

# Install service enumeration tools
echo "[+] Installing service enumeration tools..."
sudo apt-get install -y \
    nikto \
    enum4linux \
    smbclient \
    rpcclient \
    snmp \
    snmp-mibs-downloader

# Install credential testing tools
echo "[+] Installing credential testing tools..."
sudo apt-get install -y \
    hydra \
    medusa \
    crackmapexec

# Install web security tools
echo "[+] Installing web security tools..."
sudo apt-get install -y \
    sqlmap \
    ffuf \
    dirb \
    gobuster

# Install TLS/SSL testing tools
echo "[+] Installing TLS/SSL testing tools..."
sudo apt-get install -y \
    sslscan \
    sslyze

# Install Python security libraries
echo "[+] Installing Python security libraries..."
pip3 install --upgrade pip
pip3 install \
    python-nmap \
    impacket \
    pwntools \
    scapy \
    requests \
    beautifulsoup4

# Install additional tools via pip
echo "[+] Installing additional Python tools..."
pip3 install wpscan-python

# Download testssl.sh
echo "[+] Installing testssl.sh..."
cd /opt
sudo git clone --depth 1 https://github.com/drwetter/testssl.sh.git || true
sudo chmod +x /opt/testssl.sh/testssl.sh
sudo ln -sf /opt/testssl.sh/testssl.sh /usr/local/bin/testssl.sh || true

# Download common wordlists
echo "[+] Downloading common wordlists..."
sudo mkdir -p /usr/share/wordlists
cd /usr/share/wordlists

# Download SecLists if not present
if [ ! -d "SecLists" ]; then
    sudo git clone https://github.com/danielmiessler/SecLists.git
fi

# Download rockyou.txt if not present
if [ ! -f "rockyou.txt" ]; then
    sudo wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt || true
fi

# Create common username list
cat <<EOF | sudo tee /usr/share/wordlists/common_users.txt > /dev/null
admin
administrator
root
user
test
guest
backup
postgres
mysql
oracle
sa
system
EOF

# Create common password list
cat <<EOF | sudo tee /usr/share/wordlists/common_passwords.txt > /dev/null
admin
password
123456
12345678
Password1
Admin123
root
toor
changeme
password123
welcome
letmein
qwerty
abc123
EOF

# Create scan results directory
echo "[+] Creating scan results directory..."
mkdir -p ~/security-platform/scan_results
chmod 777 ~/security-platform/scan_results

# Install Python scanner service
echo "[+] Setting up Python scanner service..."
mkdir -p ~/security-platform/scanner
cat <<'EOF' > ~/security-platform/scanner/requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
python-nmap==0.7.1
python-dotenv==1.0.0
requests==2.31.0
psycopg2-binary==2.9.9
scapy==2.5.0
impacket==0.11.0
EOF

# Create Python virtual environment for scanner
cd ~/security-platform/scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create scanner service script
cat <<'EOF' > ~/security-platform/scanner/scanner_service.py
#!/usr/bin/env python3
"""
Security Scanner Service for WSL2
Provides REST API interface to security tools
"""

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import subprocess
import json
import os
from typing import List, Optional
import nmap
import uuid

app = FastAPI(title="Security Scanner Service")

class ScanRequest(BaseModel):
    target: str
    scan_type: str
    options: Optional[dict] = {}

class ScanResult(BaseModel):
    scan_id: str
    status: str
    results: Optional[dict] = None

# Store active scans
active_scans = {}

@app.get("/")
async def root():
    return {"status": "online", "service": "Security Scanner Service"}

@app.post("/scan/nmap")
async def nmap_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    active_scans[scan_id] = {"status": "running", "type": "nmap"}
    
    # Run nmap scan in background
    background_tasks.add_task(run_nmap_scan, scan_id, request.target, request.options)
    
    return {"scan_id": scan_id, "status": "started"}

def run_nmap_scan(scan_id: str, target: str, options: dict):
    try:
        nm = nmap.PortScanner()
        arguments = options.get('arguments', '-sV -sC')
        nm.scan(target, arguments=arguments)
        
        results = {}
        for host in nm.all_hosts():
            results[host] = nm[host]
        
        active_scans[scan_id] = {
            "status": "completed",
            "results": results
        }
    except Exception as e:
        active_scans[scan_id] = {
            "status": "failed",
            "error": str(e)
        }

@app.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str):
    if scan_id not in active_scans:
        return {"error": "Scan not found"}
    return active_scans[scan_id]

@app.post("/scan/arp")
async def arp_scan(request: ScanRequest):
    try:
        result = subprocess.run(
            ['sudo', 'arp-scan', '-l', '-I', 'eth0'],
            capture_output=True,
            text=True,
            timeout=60
        )
        return {"status": "completed", "output": result.stdout}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/scan/nikto")
async def nikto_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    active_scans[scan_id] = {"status": "running", "type": "nikto"}
    background_tasks.add_task(run_nikto_scan, scan_id, request.target)
    return {"scan_id": scan_id, "status": "started"}

def run_nikto_scan(scan_id: str, target: str):
    try:
        result = subprocess.run(
            ['nikto', '-h', target, '-Format', 'json'],
            capture_output=True,
            text=True,
            timeout=600
        )
        active_scans[scan_id] = {
            "status": "completed",
            "output": result.stdout
        }
    except Exception as e:
        active_scans[scan_id] = {
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
EOF

chmod +x ~/security-platform/scanner/scanner_service.py

# Create systemd service for scanner
echo "[+] Creating systemd service..."
sudo tee /etc/systemd/system/security-scanner.service > /dev/null <<EOF
[Unit]
Description=Security Scanner Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/security-platform/scanner
ExecStart=$HOME/security-platform/scanner/venv/bin/python scanner_service.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable security-scanner.service
sudo systemctl start security-scanner.service

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Scanner Service: http://localhost:9000"
echo "Service Status: sudo systemctl status security-scanner"
echo ""
echo "Installed Tools:"
echo "  - nmap, arp-scan, masscan"
echo "  - nikto, sqlmap, ffuf"
echo "  - hydra, crackmapexec"
echo "  - sslscan, testssl.sh"
echo ""
echo "Wordlists: /usr/share/wordlists/"
echo "Scan Results: ~/security-platform/scan_results/"
echo ""
echo "To test the scanner service:"
echo "  curl http://localhost:9000"
echo ""

