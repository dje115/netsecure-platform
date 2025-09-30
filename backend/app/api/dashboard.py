"""
Dashboard API Routes
"""

from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_devices": 42,
        "total_vulnerabilities": 127,
        "critical_vulnerabilities": 8,
        "hvt_devices": 5,
        "overall_risk_score": 7.5,
        "active_scans": 1,
        "completed_scans": 15
    }


@router.get("/recent-scans")
async def get_recent_scans():
    """Get recent scan sessions"""
    return [
        {
            "id": 1,
            "name": "Production Network Scan",
            "status": "completed",
            "devices_found": 42,
            "vulnerabilities_found": 127,
            "created_at": "2025-09-30T10:00:00Z"
        }
    ]


@router.get("/devices/online")
async def get_online_devices():
    """Get currently online devices"""
    return [
        {
            "id": 1,
            "ip_address": "192.168.1.1",
            "hostname": "gateway",
            "device_type": "network",
            "is_hvt": True,
            "risk_level": "high"
        }
    ]


@router.get("/vulnerabilities/critical")
async def get_critical_vulnerabilities():
    """Get critical vulnerabilities"""
    return [
        {
            "id": 1,
            "cve_id": "CVE-2021-44228",
            "title": "Log4Shell - Remote Code Execution",
            "severity": "critical",
            "cvss_score": 10.0,
            "affected_devices": 3
        }
    ]
