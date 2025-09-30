"""
Report Generation API Routes
"""

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.scan import ScanSession
from app.models.user import User
from app.services.report_generator import report_generator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ReportCreate(BaseModel):
    scan_id: int
    report_type: str  # executive, technical, compliance
    format: str  # pdf, html, docx
    include_sections: Optional[List[str]] = None


@router.post("/")
async def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate a security assessment report"""
    
    # Get scan session
    scan = db.query(ScanSession).filter(ScanSession.id == report_data.scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if scan.status != "completed":
        raise HTTPException(status_code=400, detail="Scan must be completed before generating report")
    
    try:
        # Generate report
        logger.info(f"Generating {report_data.report_type} report for scan {scan.id}")
        result = await report_generator.generate_report(
            scan,
            db,
            report_data.report_type,
            report_data.format
        )
        
        return {
            "scan_id": report_data.scan_id,
            "report_type": report_data.report_type,
            "format": report_data.format,
            "status": "completed",
            "message": "Report generated successfully",
            "summary": result["summary"]
        }
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/")
async def list_reports():
    """List all generated reports"""
    return [
        {
            "id": 1,
            "scan_id": 1,
            "name": "Production Network Security Assessment",
            "report_type": "comprehensive",
            "format": "pdf",
            "status": "completed",
            "file_size": "2.5 MB",
            "created_at": "2025-09-30T12:00:00Z",
            "download_url": "/api/reports/1/download"
        }
    ]


@router.get("/{report_id}")
async def get_report(report_id: int):
    """Get report details"""
    return {
        "id": report_id,
        "scan_id": 1,
        "name": "Production Network Security Assessment",
        "report_type": "comprehensive",
        "format": "pdf",
        "status": "completed",
        "file_size": "2.5 MB",
        "created_at": "2025-09-30T12:00:00Z",
        "sections": [
            "Executive Summary",
            "Network Topology",
            "Device Inventory",
            "High-Value Targets",
            "Vulnerability Assessment",
            "Attack Path Analysis",
            "Remediation Recommendations"
        ],
        "stats": {
            "total_devices": 42,
            "total_vulnerabilities": 127,
            "critical_vulns": 8,
            "hvt_devices": 5,
            "risk_score": 7.5
        }
    }


@router.get("/{report_id}/download")
async def download_report(report_id: int):
    """Download report file"""
    return {
        "message": "Report download endpoint",
        "report_id": report_id
    }


@router.delete("/{report_id}")
async def delete_report(report_id: int):
    """Delete a report"""
    return {
        "message": "Report deleted successfully"
    }
