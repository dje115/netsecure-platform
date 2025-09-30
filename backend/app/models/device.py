"""
Device Models
"""

from sqlalchemy import Column, Integer, String, Boolean, JSON, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_session_id = Column(Integer, ForeignKey("scan_sessions.id"))
    
    # Network Information
    ip_address = Column(String, index=True, nullable=False)
    mac_address = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    
    # System Information
    os_name = Column(String, nullable=True)
    os_version = Column(String, nullable=True)
    os_family = Column(String, nullable=True)
    device_type = Column(String, nullable=True)  # server, workstation, iot, network
    
    # Security Classification
    is_hvt = Column(Boolean, default=False)
    hvt_type = Column(String, nullable=True)  # domain_controller, dmz, gateway, credential_storage
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, nullable=True)  # critical, high, medium, low
    
    # Discovery Data
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="online")  # online, offline, unknown
    
    # AI Analysis
    ai_classification = Column(JSON, nullable=True)
    ai_recommendations = Column(Text, nullable=True)
    ai_attack_surface = Column(JSON, nullable=True)
    
    # Raw Data
    nmap_data = Column(JSON, nullable=True)
    additional_data = Column(JSON, nullable=True)
    
    # Relationships
    scan_session = relationship("ScanSession", back_populates="devices")
    ports = relationship("Port", back_populates="device", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="device", cascade="all, delete-orphan")
    vulnerabilities = relationship("Vulnerability", back_populates="device", cascade="all, delete-orphan")
    attack_paths = relationship("AttackPath", back_populates="device", cascade="all, delete-orphan")


class Port(Base):
    __tablename__ = "ports"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    
    port_number = Column(Integer, nullable=False)
    protocol = Column(String, default="tcp")  # tcp, udp
    state = Column(String, default="open")  # open, closed, filtered
    service_name = Column(String, nullable=True)
    service_version = Column(String, nullable=True)
    service_product = Column(String, nullable=True)
    
    # Additional Info
    banner = Column(Text, nullable=True)
    script_output = Column(JSON, nullable=True)
    
    # Relationships
    device = relationship("Device", back_populates="ports")


class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    
    service_type = Column(String, nullable=False)  # http, smb, ssh, rdp, snmp, database
    service_name = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    version = Column(String, nullable=True)
    
    # Enumeration Results
    enumeration_data = Column(JSON, nullable=True)
    configuration = Column(JSON, nullable=True)
    users_found = Column(JSON, nullable=True)
    shares_found = Column(JSON, nullable=True)
    
    # Security Status
    is_vulnerable = Column(Boolean, default=False)
    weak_config = Column(Boolean, default=False)
    default_creds = Column(Boolean, default=False)
    
    # Relationships
    device = relationship("Device", back_populates="services")

