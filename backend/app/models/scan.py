"""
Scan Models
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ScanSession(Base):
    __tablename__ = "scan_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    target_range = Column(String, nullable=False)
    scan_type = Column(String)  # quick, comprehensive, hvt, custom
    status = Column(String, default="pending")  # pending, running, completed, failed
    current_phase = Column(Integer, default=1)
    total_phases = Column(Integer, default=11)
    progress = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Configuration
    phases_enabled = Column(JSON, default=list)  # List of enabled phase numbers
    tools_config = Column(JSON, default=dict)
    
    # Results summary
    devices_found = Column(Integer, default=0)
    vulnerabilities_found = Column(Integer, default=0)
    hvt_count = Column(Integer, default=0)
    risk_score = Column(Integer, default=0)
    
    # Relationships
    devices = relationship("Device", back_populates="scan_session", cascade="all, delete-orphan")
    scan_logs = relationship("ScanLog", back_populates="scan_session", cascade="all, delete-orphan")
    

class ScanLog(Base):
    __tablename__ = "scan_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_session_id = Column(Integer, ForeignKey("scan_sessions.id"))
    phase = Column(Integer)
    phase_name = Column(String)
    tool_name = Column(String)
    log_level = Column(String)  # info, warning, error
    message = Column(Text)
    output = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scan_session = relationship("ScanSession", back_populates="scan_logs")

