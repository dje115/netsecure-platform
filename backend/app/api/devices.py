"""
Device Management API Routes
"""

from fastapi import APIRouter
from typing import List, Optional

router = APIRouter()


@router.get("/")
async def list_devices(
    scan_id: Optional[int] = None,
    is_hvt: Optional[bool] = None,
    risk_level: Optional[str] = None
):
    """List all devices with optional filters"""
    return [
        {
            "id": 1,
            "ip_address": "192.168.1.1",
            "mac_address": "00:11:22:33:44:55",
            "hostname": "gateway",
            "vendor": "Cisco",
            "os_name": "Cisco IOS",
            "device_type": "network",
            "is_hvt": True,
            "hvt_type": "gateway",
            "risk_score": 85,
            "risk_level": "high",
            "status": "online",
            "open_ports": 15,
            "vulnerabilities": 8
        },
        {
            "id": 2,
            "ip_address": "192.168.1.10",
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "hostname": "dc01",
            "vendor": "Microsoft",
            "os_name": "Windows Server 2019",
            "device_type": "server",
            "is_hvt": True,
            "hvt_type": "domain_controller",
            "risk_score": 90,
            "risk_level": "critical",
            "status": "online",
            "open_ports": 25,
            "vulnerabilities": 12
        }
    ]


@router.get("/{device_id}")
async def get_device(device_id: int):
    """Get detailed device information"""
    return {
        "id": device_id,
        "ip_address": "192.168.1.1",
        "mac_address": "00:11:22:33:44:55",
        "hostname": "gateway",
        "vendor": "Cisco",
        "os_name": "Cisco IOS",
        "os_version": "15.2",
        "device_type": "network",
        "is_hvt": True,
        "hvt_type": "gateway",
        "risk_score": 85,
        "risk_level": "high",
        "status": "online",
        "first_seen": "2025-09-30T10:00:00Z",
        "last_seen": "2025-09-30T15:00:00Z",
        "ai_classification": {
            "purpose": "Network Gateway",
            "criticality": "High",
            "recommended_actions": [
                "Update firmware to latest version",
                "Review firewall rules",
                "Enable intrusion detection"
            ]
        }
    }


@router.get("/{device_id}/ports")
async def get_device_ports(device_id: int):
    """Get device open ports"""
    return [
        {
            "id": 1,
            "port_number": 22,
            "protocol": "tcp",
            "state": "open",
            "service_name": "ssh",
            "service_version": "OpenSSH 7.4",
            "banner": "SSH-2.0-OpenSSH_7.4"
        },
        {
            "id": 2,
            "port_number": 443,
            "protocol": "tcp",
            "state": "open",
            "service_name": "https",
            "service_version": "nginx 1.20.1"
        }
    ]


@router.get("/{device_id}/services")
async def get_device_services(device_id: int):
    """Get device services and enumeration results"""
    return [
        {
            "id": 1,
            "service_type": "http",
            "service_name": "nginx",
            "port": 443,
            "version": "1.20.1",
            "is_vulnerable": True,
            "weak_config": False,
            "default_creds": False,
            "enumeration_data": {
                "server_header": "nginx/1.20.1",
                "technologies": ["PHP", "MySQL"],
                "endpoints": ["/admin", "/login", "/api"]
            }
        }
    ]


@router.get("/{device_id}/vulnerabilities")
async def get_device_vulnerabilities(device_id: int):
    """Get device vulnerabilities"""
    return [
        {
            "id": 1,
            "cve_id": "CVE-2021-23017",
            "title": "nginx DNS Resolver Off-by-One Heap Write",
            "description": "A security issue in nginx resolver can be triggered by a forged UDP DNS response",
            "severity": "high",
            "cvss_score": 8.1,
            "exploitable": True,
            "affected_service": "nginx",
            "affected_port": 443,
            "remediation": "Update nginx to version 1.20.2 or later"
        }
    ]


@router.get("/{device_id}/attack-paths")
async def get_device_attack_paths(device_id: int):
    """Get possible attack paths from/to device"""
    return [
        {
            "id": 1,
            "path_type": "lateral_movement",
            "source_device": "192.168.1.100",
            "target_device": "192.168.1.10",
            "attack_vector": "SMB Relay Attack",
            "technique_id": "T1021.002",
            "technique_name": "SMB/Windows Admin Shares",
            "difficulty": "medium",
            "impact_level": "high"
        }
    ]
