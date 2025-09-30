# Deployment Guide

## 🚀 Quick Deployment

### Prerequisites
- Windows 10/11 with WSL2
- Docker Desktop
- Git
- 8GB RAM minimum

### One-Command Setup

```bash
# Run as Administrator
install-security-platform.bat
```

This will:
1. Install/verify WSL2
2. Install Kali Linux
3. Set up Docker Desktop
4. Install security tools
5. Start all services

## 📋 Step-by-Step Deployment

### 1. Clone Repository

```bash
git clone https://github.com/dje115/netsecure-platform.git
cd netsecure-platform
```

### 2. Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit with your settings
notepad .env
```

Required configuration:
```ini
# Database
DB_PASSWORD=YourSecurePassword123!

# Security
SECRET_KEY=your-secret-key-min-32-chars

# AI Services (Optional)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Scanner Service
WSL_SCANNER_URL=http://localhost:9000
```

### 3. Set Up WSL2 Scanner

```bash
# Open WSL2 (Kali Linux)
wsl -d kali-linux

# Navigate to project
cd /mnt/c/Users/YOUR_USERNAME/path/to/netsecure-platform

# Run setup script
chmod +x wsl-setup.sh
./wsl-setup.sh
```

This installs:
- nmap, arp-scan, masscan
- nikto, sqlmap, ffuf
- hydra, crackmapexec
- sslscan, testssl.sh
- Python security libraries
- Scanner service (port 9000)

### 4. Run Database Migrations

```bash
# From project root
cd backend

# Run migrations
alembic upgrade head
```

### 5. Start Services

```bash
# Start all Docker containers
docker-compose up -d

# Verify services
docker-compose ps
```

Expected services:
- security-db (PostgreSQL) - Port 5432
- security-api (FastAPI) - Port 8000
- security-frontend (React) - Port 3000
- redis (Task queue) - Port 6379
- celery-worker (Background tasks)

### 6. Verify Deployment

```bash
# Check backend
curl http://localhost:8000/health

# Check scanner service
wsl -d kali-linux curl http://localhost:9000

# Check frontend
# Open browser: http://localhost:3000
```

## 👤 First User Setup

### Create Admin Account

1. Open browser: http://localhost:3000/login
2. Click "Sign Up"
3. Enter details:
   - Username: admin
   - Email: admin@your domain.com
   - Password: SecurePassword123!
4. Click "Sign Up"

**Note:** First user automatically becomes admin!

### Login

1. Enter credentials
2. Click "Sign In"
3. You'll be redirected to dashboard

## 🔧 Configuration

### Database Configuration

Edit `.env`:
```ini
DATABASE_URL=postgresql://security_admin:password@localhost:5432/security_platform
```

Or update `docker-compose.yml`:
```yaml
environment:
  POSTGRES_DB: security_platform
  POSTGRES_USER: security_admin
  POSTGRES_PASSWORD: your_password
```

### Scanner Service Configuration

Edit WSL2 scanner service:
```bash
wsl -d kali-linux
nano ~/security-platform/scanner/scanner_service.py
```

Configure:
- Scan timeouts
- Tool paths
- Wordlist locations
- Custom tools

### AI Configuration

Add API keys to `.env`:
```ini
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

Or configure per-user in UI:
1. Go to Settings
2. Enter API keys
3. Save

## 🔒 Security Hardening

### Production Deployment

1. **Change Default Passwords**
```ini
DB_PASSWORD=Generate-Strong-Password
SECRET_KEY=Generate-Min-32-Char-Key
```

2. **Enable HTTPS**
```yaml
# docker-compose.yml
services:
  security-frontend:
    environment:
      - HTTPS=true
```

3. **Restrict Network Access**
```yaml
# docker-compose.yml
services:
  security-db:
    networks:
      - internal
# Don't expose to external network
```

4. **Configure Firewall**
```bash
# Allow only necessary ports
# 3000 (Frontend), 8000 (API)
# Block 5432 (Database), 6379 (Redis)
```

5. **Enable Authentication**
Already implemented with JWT tokens!

6. **Regular Updates**
```bash
# Pull latest changes
git pull origin master

# Rebuild containers
docker-compose down
docker-compose build
docker-compose up -d

# Update scanner tools
wsl -d kali-linux
cd ~/security-platform
./wsl-setup.sh
```

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f security-api
docker-compose logs -f security-frontend

# Scanner service (WSL2)
wsl -d kali-linux journalctl -u security-scanner -f
```

### Check Service Status

```bash
# Docker services
docker-compose ps

# Scanner service
wsl -d kali-linux sudo systemctl status security-scanner

# Database
docker exec -it security-db psql -U security_admin -d security_platform
```

### Monitor Resources

```bash
# Docker stats
docker stats

# WSL2 resources
wsl -d kali-linux htop
```

## 🔄 Backup & Restore

### Database Backup

```bash
# Backup
docker exec security-db pg_dump -U security_admin security_platform > backup.sql

# Restore
docker exec -i security-db psql -U security_admin security_platform < backup.sql
```

### WSL2 Backup

```powershell
# Export WSL distribution
wsl --export kali-linux C:\Backups\kali-backup.tar

# Import on new system
wsl --import kali-linux C:\WSL\kali C:\Backups\kali-backup.tar
```

### Configuration Backup

```bash
# Backup all configurations
tar -czf config-backup.tar.gz .env docker-compose.yml backend/alembic.ini
```

## 🚨 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose down
docker-compose build
docker-compose up -d
```

### Database Connection Failed

```bash
# Check database is running
docker-compose ps security-db

# Check connection
docker exec -it security-db psql -U security_admin -d security_platform

# Reset database
docker-compose down -v
docker-compose up -d
cd backend && alembic upgrade head
```

### Scanner Service Not Responding

```bash
# Check service status
wsl -d kali-linux sudo systemctl status security-scanner

# Restart service
wsl -d kali-linux sudo systemctl restart security-scanner

# Check logs
wsl -d kali-linux journalctl -u security-scanner -n 100
```

### Frontend Can't Connect to API

1. Check API is running: http://localhost:8000/docs
2. Check CORS settings in `backend/app/main.py`
3. Verify API URL in `frontend/src/services/api.js`
4. Check browser console for errors

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  security-api:
    deploy:
      replicas: 3
  
  celery-worker:
    deploy:
      replicas: 5
```

### Database Scaling

```yaml
# Use external PostgreSQL
services:
  security-api:
    environment:
      DATABASE_URL: postgresql://user:pass@external-db:5432/db
```

### Load Balancing

```yaml
# Add nginx reverse proxy
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## 🌐 Production Deployment

### AWS Deployment

1. **EC2 Instance**
   - Ubuntu 22.04 or newer
   - t3.large minimum (2 vCPU, 8GB RAM)
   - Security group: ports 80, 443

2. **RDS Database**
   - PostgreSQL 15
   - db.t3.medium minimum

3. **Deploy**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone <repo>
cd netsecure-platform
./install-security-platform.sh  # Linux version
```

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml security-platform
```

### Kubernetes

```bash
# Convert to Kubernetes
kompose convert -f docker-compose.yml

# Deploy
kubectl apply -f .
```

## 📞 Support

- **GitHub Issues**: https://github.com/dje115/netsecure-platform/issues
- **Documentation**: https://github.com/dje115/netsecure-platform/tree/master/docs

---

**Important**: Only scan networks you own or have explicit permission to test. Unauthorized scanning is illegal.
