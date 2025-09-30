"""
Vulnerability Management API Routes
"""

from fastapi import APIRouter
from typing import List, Optional

router = APIRouter()


@router.get("/")
async def list_vulnerabilities(
    severity: Optional[str] = None,
    exploitable: Optional[bool] = None,
    scan_id: Optional[int] = None
):
    """List all vulnerabilities with optional filters"""
    return [
        {
            "id": 1,
            "cve_id": "CVE-2021-44228",
            "title": "Apache Log4j2 Remote Code Execution (Log4Shell)",
            "severity": "critical",
            "cvss_score": 10.0,
            "exploitable": True,
            "exploit_available": True,
            "affected_devices": 3,
            "devices": [
                {"id": 5, "ip_address": "192.168.1.50", "hostname": "web-server-01"},
                {"id": 8, "ip_address": "192.168.1.80", "hostname": "app-server-01"}
            ]
        },
        {
            "id": 2,
            "cve_id": "CVE-2021-23017",
            "title": "nginx DNS Resolver Off-by-One Heap Write",
            "severity": "high",
            "cvss_score": 8.1,
            "exploitable": True,
            "exploit_available": False,
            "affected_devices": 2
        }
    ]


@router.get("/{vuln_id}")
async def get_vulnerability(vuln_id: int):
    """Get detailed vulnerability information"""
    return {
        "id": vuln_id,
        "cve_id": "CVE-2021-44228",
        "title": "Apache Log4j2 Remote Code Execution (Log4Shell)",
        "description": "Apache Log4j2 2.0-beta9 through 2.15.0 JNDI features used in configuration...",
        "severity": "critical",
        "cvss_score": 10.0,
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "exploitable": True,
        "exploit_available": True,
        "exploit_db_id": "50592",
        "metasploit_module": "exploit/multi/http/log4shell_header_injection",
        "affected_service": "Apache Tomcat",
        "affected_port": 8080,
        "remediation": "Update Log4j2 to version 2.17.1 or later",
        "patch_available": True,
        "patch_info": "Apache Log4j 2.17.1 contains the fix for CVE-2021-44228",
        "references": [
            "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
            "https://logging.apache.org/log4j/2.x/security.html"
        ],
        "cwe_ids": ["CWE-502", "CWE-917"],
        "discovered_at": "2025-09-30T10:15:00Z"
    }


@router.get("/stats")
async def get_vulnerability_stats():
    """Get vulnerability statistics"""
    return {
        "total": 127,
        "by_severity": {
            "critical": 8,
            "high": 23,
            "medium": 56,
            "low": 40
        },
        "exploitable": 15,
        "with_exploits": 8,
        "patched": 45,
        "unpatched": 82
    }

