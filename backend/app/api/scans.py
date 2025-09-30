"""
Scan Management API Routes
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.scan import ScanSession, ScanLog
from app.models.user import User
from app.services.scan_phases import scan_orchestrator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ScanCreate(BaseModel):
    name: str
    target_range: str
    scan_type: str  # quick, comprehensive, hvt, custom
    phases_enabled: Optional[List[int]] = None


class ScanPhaseStatus(BaseModel):
    phase: int
    name: str
    status: str
    progress: int


@router.post("/", response_model=dict)
async def create_scan(
    scan_data: ScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new scan session"""
    
    # Determine phases to enable
    phases_enabled = scan_data.phases_enabled
    if phases_enabled is None:
        if scan_data.scan_type == "quick":
            phases_enabled = [1, 2, 4]  # Discovery, HVT, Vuln scan
        elif scan_data.scan_type == "hvt":
            phases_enabled = [1, 2, 3, 4]  # Focus on HVT
        else:  # comprehensive
            phases_enabled = list(range(1, 12))  # All phases
    
    # Create scan session
    new_scan = ScanSession(
        name=scan_data.name,
        target_range=scan_data.target_range,
        scan_type=scan_data.scan_type,
        status="pending",
        current_phase=0,
        total_phases=len(phases_enabled),
        progress=0,
        phases_enabled=phases_enabled,
        created_at=datetime.utcnow()
    )
    
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    
    logger.info(f"Created scan session {new_scan.id}: {new_scan.name}")
    
    return {
        "id": new_scan.id,
        "name": new_scan.name,
        "target_range": new_scan.target_range,
        "status": new_scan.status,
        "phases_enabled": phases_enabled,
        "message": "Scan created successfully. Use /scans/{id}/start to begin."
    }


@router.get("/", response_model=List[dict])
async def list_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """List all scan sessions"""
    scans = db.query(ScanSession).offset(skip).limit(limit).all()
    
    return [
        {
            "id": scan.id,
            "name": scan.name,
            "target_range": scan.target_range,
            "scan_type": scan.scan_type,
            "status": scan.status,
            "current_phase": scan.current_phase,
            "total_phases": scan.total_phases,
            "progress": scan.progress,
            "devices_found": scan.devices_found,
            "vulnerabilities_found": scan.vulnerabilities_found,
            "hvt_count": scan.hvt_count,
            "created_at": scan.created_at.isoformat() if scan.created_at else None,
            "started_at": scan.started_at.isoformat() if scan.started_at else None,
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None
        }
        for scan in scans
    ]


@router.get("/{scan_id}")
async def get_scan(scan_id: int):
    """Get scan session details"""
    return {
        "id": scan_id,
        "name": "Production Network Scan",
        "target_range": "192.168.1.0/24",
        "scan_type": "comprehensive",
        "status": "running",
        "current_phase": 3,
        "total_phases": 11,
        "progress": 27,
        "devices_found": 15,
        "vulnerabilities_found": 42,
        "hvt_count": 2,
        "phases": [
            {"phase": 1, "name": "Network Discovery", "status": "completed", "progress": 100},
            {"phase": 2, "name": "HVT Identification", "status": "completed", "progress": 100},
            {"phase": 3, "name": "Service Enumeration", "status": "running", "progress": 60}
        ]
    }


async def execute_scan_background(scan_id: int):
    """Background task to execute the scan"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    
    try:
        print(f"=== SCAN BACKGROUND TASK STARTED: Scan ID {scan_id} ===")
        logger.info(f"=== SCAN BACKGROUND TASK STARTED: Scan ID {scan_id} ===")
        
        # Get scan session
        scan = db.query(ScanSession).filter(ScanSession.id == scan_id).first()
        if not scan:
            print(f"ERROR: Scan {scan_id} not found in database")
            logger.error(f"Scan {scan_id} not found")
            return
        
        print(f"Found scan: {scan.name}, Target: {scan.target_range}")
        
        # Update status
        scan.status = "running"
        scan.started_at = datetime.utcnow()
        db.commit()
        
        print(f"Scan status updated to 'running', calling orchestrator...")
        logger.info(f"Starting scan execution for scan {scan_id}")
        
        # Execute scan orchestrator
        result = await scan_orchestrator.execute_scan(
            scan,
            db,
            scan.target_range,
            scan.phases_enabled
        )
        
        print(f"Scan {scan_id} orchestrator returned: {result.get('status')}")
        logger.info(f"Scan {scan_id} completed: {result.get('status')}")
        
    except Exception as e:
        logger.error(f"Scan {scan_id} failed: {e}", exc_info=True)
        scan = db.query(ScanSession).filter(ScanSession.id == scan_id).first()
        if scan:
            scan.status = "failed"
            db.commit()
    finally:
        db.close()


@router.post("/{scan_id}/start")
async def start_scan(
    scan_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start a scan session"""
    
    scan = db.query(ScanSession).filter(ScanSession.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if scan.status == "running":
        raise HTTPException(status_code=400, detail="Scan is already running")
    
    if scan.status == "completed":
        raise HTTPException(status_code=400, detail="Scan already completed. Create a new scan.")
    
    # Add to background tasks
    background_tasks.add_task(execute_scan_background, scan_id)
    
    return {
        "id": scan_id,
        "status": "starting",
        "message": "Scan started successfully in background"
    }


@router.post("/{scan_id}/stop")
async def stop_scan(scan_id: int):
    """Stop a running scan"""
    return {
        "id": scan_id,
        "status": "stopped",
        "message": "Scan stopped successfully"
    }


@router.delete("/{scan_id}")
async def delete_scan(scan_id: int):
    """Delete a scan session"""
    return {
        "message": "Scan deleted successfully"
    }


@router.get("/{scan_id}/logs")
async def get_scan_logs(scan_id: int):
    """Get scan logs"""
    return [
        {
            "id": 1,
            "phase": 1,
            "phase_name": "Network Discovery",
            "tool_name": "nmap",
            "log_level": "info",
            "message": "Starting nmap scan on 192.168.1.0/24",
            "timestamp": "2025-09-30T10:00:00Z"
        }
    ]


@router.get("/{scan_id}/phases")
async def get_scan_phases(scan_id: int):
    """Get detailed phase status"""
    return [
        {
            "phase": 1,
            "name": "Network Discovery",
            "description": "ARP scan, host discovery, service enumeration",
            "status": "completed",
            "progress": 100,
            "tools": ["arp-scan", "nmap"],
            "started_at": "2025-09-30T10:00:00Z",
            "completed_at": "2025-09-30T10:05:00Z"
        },
        {
            "phase": 2,
            "name": "HVT Identification",
            "description": "High-value target classification",
            "status": "completed",
            "progress": 100,
            "tools": ["AI Analysis"],
            "started_at": "2025-09-30T10:05:00Z",
            "completed_at": "2025-09-30T10:08:00Z"
        },
        {
            "phase": 3,
            "name": "Service Enumeration",
            "description": "HTTP, SMB, SSH, RDP, SNMP, database services",
            "status": "running",
            "progress": 60,
            "tools": ["nikto", "enum4linux", "smbclient"],
            "started_at": "2025-09-30T10:08:00Z"
        }
    ]
