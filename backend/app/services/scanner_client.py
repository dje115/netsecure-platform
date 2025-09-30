"""
Scanner Service Client - Communicates with WSL2 Scanner Service
"""

import httpx
import logging
from typing import Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class ScannerClient:
    """Client for WSL2 Scanner Service"""
    
    def __init__(self):
        self.base_url = settings.WSL_SCANNER_URL
        self.timeout = 300.0  # 5 minutes default timeout
    
    async def health_check(self) -> bool:
        """Check if scanner service is available"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Scanner service health check failed: {e}")
            return False
    
    async def nmap_scan(self, target: str, arguments: str = "-sn") -> Dict:
        """
        Execute nmap scan
        
        Args:
            target: Target IP or range (e.g., "192.168.1.0/24")
            arguments: Nmap arguments (e.g., "-sV -sC")
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/scan/nmap",
                    json={
                        "target": target,
                        "scan_type": "nmap",
                        "options": {"arguments": arguments}
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Nmap scan failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def get_scan_status(self, scan_id: str) -> Dict:
        """Get status of a running scan"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/scan/{scan_id}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get scan status: {e}")
            return {"status": "error", "error": str(e)}
    
    async def arp_scan(self, interface: str = "eth0") -> Dict:
        """Execute ARP scan for network discovery"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/scan/arp",
                    json={
                        "target": interface,
                        "scan_type": "arp",
                        "options": {}
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"ARP scan failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def nikto_scan(self, target: str) -> Dict:
        """Execute Nikto web server scan"""
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:  # 10 minutes
                response = await client.post(
                    f"{self.base_url}/scan/nikto",
                    json={
                        "target": target,
                        "scan_type": "nikto",
                        "options": {}
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Nikto scan failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def run_command(self, command: str, args: List[str], timeout: int = 300) -> Dict:
        """
        Execute arbitrary command on scanner service
        
        Args:
            command: Command to execute
            args: List of arguments
            timeout: Timeout in seconds
        """
        try:
            async with httpx.AsyncClient(timeout=float(timeout)) as client:
                response = await client.post(
                    f"{self.base_url}/execute",
                    json={
                        "command": command,
                        "args": args,
                        "timeout": timeout
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"status": "failed", "error": str(e)}


# Global scanner client instance
scanner_client = ScannerClient()
