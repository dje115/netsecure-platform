# Professional Security Assessment Platform

A comprehensive, enterprise-grade security assessment platform that provides multi-phase network discovery, vulnerability scanning, AI-powered analysis, and professional reporting capabilities.

## Features

- **Multi-Phase Security Assessment**: 11-phase comprehensive network security evaluation
- **AI-Powered Analysis**: GPT-4 and Claude integration for intelligent device classification
- **High-Value Target (HVT) Identification**: Automated critical infrastructure detection
- **Attack Path Mapping**: Visual lateral movement and privilege escalation analysis
- **Professional Reporting**: Executive and technical reports with actionable recommendations
- **Real-time Dashboard**: Live scanning progress with status indicators
- **Comprehensive Tool Integration**: 50+ security tools in unified platform

## Architecture

- **Backend**: FastAPI (Python) with PostgreSQL database
- **Frontend**: React.js with Tailwind CSS
- **Infrastructure**: Docker Compose with WSL2 on Windows
- **Security Tools**: Kali Linux container with comprehensive toolset
- **AI Integration**: OpenAI GPT-4 and Anthropic Claude API support

## Quick Start

### Windows Installation (One-Click Setup)
```bash
# Run the automated installer
install-security-platform.bat
```

### Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd security-platform

# Start all services
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# API: http://localhost:8000
```

## Security Assessment Phases

1. **Network Discovery**: ARP scan, host discovery, service enumeration
2. **HVT Identification**: Domain controllers, DMZ servers, critical services
3. **Service Enumeration**: HTTP, SMB, SSH, RDP, SNMP, database services
4. **Vulnerability Scanning**: CVE detection, configuration issues
5. **Authentication Testing**: Password and credential validation
6. **Web Application Security**: OWASP testing, hidden endpoints
7. **Active Directory Assessment**: AD enumeration, BloodHound analysis
8. **IoT & Network Devices**: SNMP, device-specific security checks
9. **TLS & Configuration**: SSL/TLS testing, certificate analysis
10. **Exploit Validation**: Controlled vulnerability confirmation
11. **Lateral Movement**: Attack path simulation and mapping

## Professional Features

- **Status Indicators**: Green/Red/Yellow lights for all services
- **Real-time Progress**: Live scanning updates by phase
- **HVT Classification**: AI-powered high-value target identification
- **Attack Path Visualization**: Network graph with attack vectors
- **Professional Reports**: Executive summaries and technical details
- **Credential Testing**: Safe password and authentication validation
- **CVE Integration**: Real-time vulnerability lookup and scoring

## Technology Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: React.js, Tailwind CSS, Chart.js
- **Security Tools**: nmap, nikto, hydra, crackmapexec, bloodhound
- **AI Services**: OpenAI GPT-4, Anthropic Claude
- **Infrastructure**: Docker, WSL2, Kali Linux

## Documentation

- [Installation Guide](docs/installation.md)
- [User Manual](docs/user-manual.md)
- [API Documentation](docs/api.md)
- [Security Tools](docs/security-tools.md)
- [Report Templates](docs/reports.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support

For support and questions, please open an issue or contact the development team.
