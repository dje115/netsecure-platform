#!/usr/bin/env python3
"""
Security Scanner Service for WSL2
Provides REST API interface to security tools running in Kali Linux
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import uuid
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store active scans in memory
active_scans = {}

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "status": "online",
        "service": "Security Scanner Service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/service/status', methods=['GET'])
def service_status():
    """Get detailed service status"""
    import os
    import psutil
    
    # Get process info
    pid = os.getpid()
    process = psutil.Process(pid)
    
    # Get system info
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    # Get network interface info
    try:
        net_result = subprocess.run(['ip', 'addr', 'show', 'eth0'], 
                                   capture_output=True, text=True, timeout=5)
        network_info = net_result.stdout
    except:
        network_info = "Unable to get network info"
    
    return jsonify({
        "service": "Security Scanner Service",
        "status": "running",
        "version": "1.0.0",
        "pid": pid,
        "uptime_seconds": int(time.time() - process.create_time()),
        "memory_usage_mb": round(process.memory_info().rss / 1024 / 1024, 2),
        "cpu_percent": cpu_percent,
        "system_memory_percent": memory.percent,
        "active_scans": len(active_scans),
        "scan_list": list(active_scans.keys()),
        "network_info": network_info,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/service/restart', methods=['POST'])
def service_restart():
    """Restart the scanner service"""
    import os
    import signal
    
    pid = os.getpid()
    
    # Send SIGHUP to self (graceful restart)
    os.kill(pid, signal.SIGHUP)
    
    return jsonify({
        "status": "restarting",
        "message": "Service restart initiated",
        "pid": pid
    })

@app.route('/service/stats', methods=['GET'])
def service_stats():
    """Get service statistics"""
    import os
    
    # Count tools available
    tools_available = 0
    tools_list = ['nmap', 'nikto', 'masscan', 'sqlmap', 'hydra', 'curl', 'ping']
    available_tools = {}
    
    for tool in tools_list:
        result = subprocess.run(['which', tool], capture_output=True)
        is_available = result.returncode == 0
        available_tools[tool] = is_available
        if is_available:
            tools_available += 1
    
    return jsonify({
        "total_tools": len(tools_list),
        "tools_available": tools_available,
        "tools": available_tools,
        "active_scans": len(active_scans),
        "python_version": subprocess.run(['python3', '--version'], 
                                        capture_output=True, text=True).stdout.strip(),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/scan/nmap', methods=['POST'])
def nmap_scan():
    """Run an Nmap scan"""
    data = request.json
    target = data.get('target')
    arguments = data.get('arguments', '-sn')  # Default: ping scan
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    scan_id = str(uuid.uuid4())
    
    try:
        # Run nmap
        cmd = ['sudo', 'nmap'] + arguments.split() + [target]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return jsonify({
            "scan_id": scan_id,
            "status": "completed",
            "target": target,
            "command": ' '.join(cmd),
            "output": result.stdout,
            "error": result.stderr if result.stderr else None,
            "return_code": result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            "scan_id": scan_id,
            "status": "timeout",
            "error": "Scan timed out after 5 minutes"
        }), 408
    except Exception as e:
        return jsonify({
            "scan_id": scan_id,
            "status": "failed",
            "error": str(e)
        }), 500

@app.route('/scan/ping', methods=['POST'])
def ping_scan():
    """Quick ping to check if host is up"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    try:
        result = subprocess.run(
            ['ping', '-c', '2', target],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        is_up = result.returncode == 0
        
        return jsonify({
            "target": target,
            "is_up": is_up,
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({
            "target": target,
            "is_up": False,
            "error": str(e)
        }), 500

@app.route('/scan/discovery', methods=['POST'])
def discovery_scan():
    """Network discovery scan"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    try:
        # Use nmap for host discovery
        result = subprocess.run(
            ['sudo', 'nmap', '-sn', '-T4', target],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        # Parse output
        hosts_up = []
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Nmap scan report for' in line:
                # Extract IP/hostname
                parts = line.split('for ')
                if len(parts) > 1:
                    host_info = parts[1].strip()
                    hosts_up.append(host_info)
        
        return jsonify({
            "status": "completed",
            "target": target,
            "hosts_found": len(hosts_up),
            "hosts": hosts_up,
            "raw_output": result.stdout
        })
        
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

@app.route('/scan/ports', methods=['POST'])
def port_scan():
    """Port scanning"""
    data = request.json
    target = data.get('target')
    ports = data.get('ports', '1-1000')  # Default: top 1000 ports
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    try:
        # Run nmap port scan
        result = subprocess.run(
            ['sudo', 'nmap', '-p', ports, '-T4', target],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return jsonify({
            "status": "completed",
            "target": target,
            "ports_scanned": ports,
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

@app.route('/scan/service', methods=['POST'])
def service_scan():
    """Service and version detection"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    try:
        # Run nmap with service detection
        result = subprocess.run(
            ['sudo', 'nmap', '-sV', '-T4', target],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        return jsonify({
            "status": "completed",
            "target": target,
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

@app.route('/scan/vulnerability', methods=['POST'])
def vulnerability_scan():
    """Basic vulnerability scanning with nmap scripts"""
    data = request.json
    target = data.get('target')
    
    if not target:
        return jsonify({"error": "Target required"}), 400
    
    try:
        # Run nmap with vuln scripts
        result = subprocess.run(
            ['sudo', 'nmap', '--script', 'vuln', '-T4', target],
            capture_output=True,
            text=True,
            timeout=900
        )
        
        return jsonify({
            "status": "completed",
            "target": target,
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

@app.route('/tools/installed', methods=['GET'])
def list_tools():
    """List installed security tools"""
    tools = {}
    
    tool_list = ['nmap', 'nikto', 'masscan', 'sqlmap', 'hydra']
    
    for tool in tool_list:
        try:
            result = subprocess.run(
                ['which', tool],
                capture_output=True,
                text=True
            )
            tools[tool] = {
                "installed": result.returncode == 0,
                "path": result.stdout.strip() if result.returncode == 0 else None
            }
        except:
            tools[tool] = {"installed": False}
    
    return jsonify({"tools": tools})

if __name__ == '__main__':
    print("=" * 50)
    print("Security Scanner Service Starting...")
    print("=" * 50)
    print("Listening on: http://0.0.0.0:9000")
    print("Test with: curl http://localhost:9000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=9000, debug=False)

