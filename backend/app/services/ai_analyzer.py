"""
AI Analysis Service
Provides device classification, risk assessment, and recommendations
"""

import logging
from typing import Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI-powered security analysis using GPT-4 or Claude"""
    
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.provider = None
        
        # Initialize provider based on available keys
        if self.openai_key:
            self.provider = "openai"
            logger.info("AI Analyzer initialized with OpenAI")
        elif self.anthropic_key:
            self.provider = "anthropic"
            logger.info("AI Analyzer initialized with Anthropic")
        else:
            logger.warning("No AI API keys configured")
    
    async def classify_device(
        self,
        ip_address: str,
        hostname: Optional[str],
        os_info: Optional[str],
        open_ports: List[int],
        services: List[Dict]
    ) -> Dict:
        """
        Classify device type and purpose using AI
        
        Returns:
            {
                "device_type": "server" | "workstation" | "iot" | "network",
                "purpose": "Description of likely purpose",
                "criticality": "high" | "medium" | "low",
                "confidence": float (0-1)
            }
        """
        
        # Rule-based classification (fallback if no AI)
        device_classification = self._rule_based_classification(
            hostname, os_info, open_ports, services
        )
        
        if not self.provider:
            return device_classification
        
        # AI-enhanced classification
        try:
            prompt = self._build_device_classification_prompt(
                ip_address, hostname, os_info, open_ports, services
            )
            
            if self.provider == "openai":
                ai_result = await self._openai_classify(prompt)
            else:
                ai_result = await self._anthropic_classify(prompt)
            
            # Merge AI results with rule-based
            device_classification.update(ai_result)
            
        except Exception as e:
            logger.error(f"AI classification failed: {e}")
        
        return device_classification
    
    def _rule_based_classification(
        self,
        hostname: Optional[str],
        os_info: Optional[str],
        open_ports: List[int],
        services: List[Dict]
    ) -> Dict:
        """Rule-based device classification"""
        
        device_type = "unknown"
        purpose = "Unknown device"
        criticality = "low"
        is_hvt = False
        hvt_type = None
        
        # Analyze hostname
        if hostname:
            hostname_lower = hostname.lower()
            if any(x in hostname_lower for x in ["dc", "domain", "ad"]):
                device_type = "server"
                purpose = "Domain Controller"
                criticality = "high"
                is_hvt = True
                hvt_type = "domain_controller"
            elif any(x in hostname_lower for x in ["web", "www", "http"]):
                device_type = "server"
                purpose = "Web Server"
                criticality = "medium"
            elif any(x in hostname_lower for x in ["db", "sql", "mysql", "postgres"]):
                device_type = "server"
                purpose = "Database Server"
                criticality = "high"
                is_hvt = True
                hvt_type = "credential_storage"
            elif any(x in hostname_lower for x in ["gw", "gateway", "router", "firewall"]):
                device_type = "network"
                purpose = "Network Gateway"
                criticality = "high"
                is_hvt = True
                hvt_type = "gateway"
        
        # Analyze open ports
        if device_type == "unknown":
            # Domain Controller indicators
            if 88 in open_ports or 389 in open_ports:
                device_type = "server"
                purpose = "Domain Controller / LDAP Server"
                criticality = "high"
                is_hvt = True
                hvt_type = "domain_controller"
            # Web server
            elif 80 in open_ports or 443 in open_ports:
                device_type = "server"
                purpose = "Web Server"
                criticality = "medium"
                if 443 in open_ports and 80 not in open_ports:
                    purpose += " (HTTPS only)"
            # Database server
            elif any(p in open_ports for p in [3306, 5432, 1433, 1521]):
                device_type = "server"
                purpose = "Database Server"
                criticality = "high"
                is_hvt = True
                hvt_type = "credential_storage"
            # File server
            elif 445 in open_ports or 139 in open_ports:
                device_type = "server"
                purpose = "File Server (SMB)"
                criticality = "medium"
            # SSH server
            elif 22 in open_ports and len(open_ports) < 5:
                device_type = "server"
                purpose = "SSH Server / Linux Host"
                criticality = "medium"
            # Network device
            elif 161 in open_ports:  # SNMP
                device_type = "network"
                purpose = "Network Device (SNMP enabled)"
                criticality = "medium"
            # IoT device
            elif len(open_ports) <= 3:
                device_type = "iot"
                purpose = "IoT Device or Appliance"
                criticality = "low"
        
        # Analyze OS
        if os_info:
            if "windows server" in os_info.lower():
                if device_type == "unknown":
                    device_type = "server"
                    purpose = "Windows Server"
            elif "windows" in os_info.lower():
                if device_type == "unknown":
                    device_type = "workstation"
                    purpose = "Windows Workstation"
            elif "linux" in os_info.lower():
                if device_type == "unknown":
                    device_type = "server"
                    purpose = "Linux Server"
        
        return {
            "device_type": device_type,
            "purpose": purpose,
            "criticality": criticality,
            "is_hvt": is_hvt,
            "hvt_type": hvt_type,
            "confidence": 0.7,
            "method": "rule_based"
        }
    
    def _build_device_classification_prompt(
        self,
        ip_address: str,
        hostname: Optional[str],
        os_info: Optional[str],
        open_ports: List[int],
        services: List[Dict]
    ) -> str:
        """Build prompt for AI classification"""
        
        prompt = f"""Analyze this network device and classify it:

IP Address: {ip_address}
Hostname: {hostname or "Unknown"}
Operating System: {os_info or "Unknown"}
Open Ports: {", ".join(map(str, open_ports))}
Services: {len(services)} detected

Based on this information, provide:
1. Device type (server, workstation, network device, or IoT)
2. Likely purpose and role
3. Security criticality (high, medium, low)
4. Whether it's a High-Value Target (HVT)
5. Recommended security measures

Format as JSON."""
        
        return prompt
    
    async def _openai_classify(self, prompt: str) -> Dict:
        """Use OpenAI GPT-4 for classification"""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.openai_key)
            
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing network devices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            # Parse JSON response
            import json
            result = json.loads(content)
            result["method"] = "openai"
            result["confidence"] = 0.9
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI classification failed: {e}")
            return {"method": "openai", "error": str(e)}
    
    async def _anthropic_classify(self, prompt: str) -> Dict:
        """Use Anthropic Claude for classification"""
        try:
            from anthropic import AsyncAnthropic
            
            client = AsyncAnthropic(api_key=self.anthropic_key)
            
            response = await client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            # Parse JSON response
            import json
            result = json.loads(content)
            result["method"] = "anthropic"
            result["confidence"] = 0.9
            
            return result
            
        except Exception as e:
            logger.error(f"Anthropic classification failed: {e}")
            return {"method": "anthropic", "error": str(e)}
    
    async def assess_risk(
        self,
        device_info: Dict,
        vulnerabilities: List[Dict],
        services: List[Dict]
    ) -> Dict:
        """
        Assess device risk score and provide recommendations
        
        Returns:
            {
                "risk_score": int (0-100),
                "risk_level": "critical" | "high" | "medium" | "low",
                "factors": List[str],
                "recommendations": List[str]
            }
        """
        
        risk_score = 0
        factors = []
        recommendations = []
        
        # Base risk on device type
        if device_info.get("is_hvt"):
            risk_score += 30
            factors.append("High-Value Target")
            recommendations.append("Implement additional monitoring and access controls")
        
        # Risk from vulnerabilities
        critical_vulns = sum(1 for v in vulnerabilities if v.get("severity") == "critical")
        high_vulns = sum(1 for v in vulnerabilities if v.get("severity") == "high")
        
        risk_score += critical_vulns * 20
        risk_score += high_vulns * 10
        
        if critical_vulns > 0:
            factors.append(f"{critical_vulns} critical vulnerabilities")
            recommendations.append("Patch critical vulnerabilities immediately")
        
        if high_vulns > 0:
            factors.append(f"{high_vulns} high severity vulnerabilities")
            recommendations.append("Schedule high-severity vulnerability remediation")
        
        # Risk from exposed services
        dangerous_services = ["telnet", "ftp", "rlogin", "rsh"]
        for service in services:
            if service.get("name", "").lower() in dangerous_services:
                risk_score += 15
                factors.append(f"Insecure service: {service['name']}")
                recommendations.append(f"Disable or replace {service['name']} with secure alternative")
        
        # Cap at 100
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = "critical"
        elif risk_score >= 60:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": factors,
            "recommendations": recommendations
        }
    
    async def generate_recommendations(
        self,
        device_info: Dict,
        vulnerabilities: List[Dict],
        risk_assessment: Dict
    ) -> List[str]:
        """Generate security recommendations for a device"""
        
        recommendations = []
        
        # Add risk-based recommendations
        recommendations.extend(risk_assessment.get("recommendations", []))
        
        # Device-specific recommendations
        if device_info.get("is_hvt"):
            recommendations.append("Enable comprehensive logging and monitoring")
            recommendations.append("Implement network segmentation")
            recommendations.append("Require multi-factor authentication")
        
        # Service-specific recommendations
        device_type = device_info.get("device_type")
        if device_type == "server":
            recommendations.append("Ensure regular security updates")
            recommendations.append("Harden server configuration")
            recommendations.append("Implement intrusion detection")
        
        return list(set(recommendations))  # Remove duplicates


# Global AI analyzer instance
ai_analyzer = AIAnalyzer()

