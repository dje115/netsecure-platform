"""
Dashboard API Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.scan import ScanSession
from app.models.device import Device
from app.models.vulnerability import Vulnerability
from app.models.user import User
from typing import List, Dict

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get real-time dashboard statistics from database"""
    
    # Count total devices
    total_devices = db.query(Device).count()
    
    # Count total vulnerabilities
    total_vulnerabilities = db.query(Vulnerability).count()
    
    # Count critical vulnerabilities
    critical_vulnerabilities = db.query(Vulnerability).filter(
        Vulnerability.severity == "critical"
    ).count()
    
    # Count HVT devices
    hvt_devices = db.query(Device).filter(Device.is_hvt == True).count()
    
    # Calculate average risk score
    avg_risk = db.query(func.avg(ScanSession.risk_score)).filter(
        ScanSession.status == "completed"
    ).scalar()
    overall_risk_score = round(avg_risk / 10, 1) if avg_risk else 0
    
    # Count active scans
    active_scans = db.query(ScanSession).filter(
        ScanSession.status.in_(["running", "pending"])
    ).count()
    
    # Count completed scans
    completed_scans = db.query(ScanSession).filter(
        ScanSession.status == "completed"
    ).count()
    
    return {
        "total_devices": total_devices,
        "total_vulnerabilities": total_vulnerabilities,
        "critical_vulnerabilities": critical_vulnerabilities,
        "hvt_devices": hvt_devices,
        "overall_risk_score": overall_risk_score,
        "active_scans": active_scans,
        "completed_scans": completed_scans
    }


@router.get("/recent-scans")
async def get_recent_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 5
):
    """Get recent scan sessions"""
    scans = db.query(ScanSession).order_by(
        ScanSession.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": scan.id,
            "name": scan.name,
            "status": scan.status,
            "devices_found": scan.devices_found or 0,
            "vulnerabilities_found": scan.vulnerabilities_found or 0,
            "hvt_count": scan.hvt_count or 0,
            "risk_score": scan.risk_score or 0,
            "created_at": scan.created_at.isoformat() if scan.created_at else None,
            "started_at": scan.started_at.isoformat() if scan.started_at else None,
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None
        }
        for scan in scans
    ]


@router.get("/devices/online")
async def get_online_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 10
):
    """Get recently discovered devices"""
    devices = db.query(Device).order_by(
        Device.discovered_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": device.id,
            "ip_address": device.ip_address,
            "hostname": device.hostname,
            "device_type": device.device_type,
            "os_name": device.os_name,
            "is_hvt": device.is_hvt,
            "risk_level": device.risk_level,
            "risk_score": device.risk_score
        }
        for device in devices
    ]


@router.get("/vulnerabilities/critical")
async def get_critical_vulnerabilities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 10
):
    """Get critical vulnerabilities"""
    vulns = db.query(Vulnerability).filter(
        Vulnerability.severity == "critical"
    ).order_by(Vulnerability.cvss_score.desc()).limit(limit).all()
    
    return [
        {
            "id": vuln.id,
            "cve_id": vuln.cve_id,
            "title": vuln.title,
            "severity": vuln.severity,
            "cvss_score": vuln.cvss_score,
            "device_id": vuln.device_id,
            "exploitable": vuln.exploitable
        }
        for vuln in vulns
    ]


@router.get("/risk-trend")
async def get_risk_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get risk score trend over time"""
    scans = db.query(ScanSession).filter(
        ScanSession.status == "completed"
    ).order_by(ScanSession.completed_at.desc()).limit(10).all()
    
    return [
        {
            "date": scan.completed_at.isoformat() if scan.completed_at else None,
            "risk_score": scan.risk_score or 0,
            "scan_name": scan.name
        }
        for scan in reversed(scans)
    ]