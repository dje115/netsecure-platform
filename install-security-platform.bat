@echo off
REM Security Platform - Windows Installation Script
REM This script sets up WSL2, Kali Linux, Docker, and the Security Platform

echo ====================================
echo Security Assessment Platform Setup
echo ====================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo [Step 1/6] Checking WSL2...
wsl --status >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing WSL2...
    wsl --install
    echo.
    echo WSL2 has been installed. Please restart your computer.
    echo After restart, run this script again to continue setup.
    pause
    exit /b 0
)

echo [Step 2/6] Checking Kali Linux...
wsl -l | findstr "kali-linux" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing Kali Linux...
    wsl --install -d kali-linux
    echo.
    echo Kali Linux installed. Please set up your username and password.
    pause
)

echo [Step 3/6] Checking Docker Desktop...
where docker >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Docker Desktop is not installed.
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    echo After installation, enable WSL2 integration:
    echo 1. Open Docker Desktop Settings
    echo 2. Go to Resources ^> WSL Integration
    echo 3. Enable integration with Kali Linux
    echo.
    pause
    exit /b 1
)

echo [Step 4/6] Setting up security tools in WSL2...
wsl -d kali-linux bash -c "cd /mnt/c/Users/%USERNAME%/Documents/Netsecure && chmod +x wsl-setup.sh && ./wsl-setup.sh"

echo [Step 5/6] Creating environment file...
if not exist .env (
    echo Creating .env file...
    (
        echo # Security Platform Configuration
        echo DB_PASSWORD=SecurePassword123!
        echo SECRET_KEY=your-secret-key-change-in-production
        echo OPENAI_API_KEY=your-openai-api-key-here
        echo ANTHROPIC_API_KEY=your-anthropic-api-key-here
        echo.
        echo # Scanner Service (WSL2)
        echo WSL_SCANNER_URL=http://localhost:9000
    ) > .env
    echo .env file created. Please edit it with your API keys.
)

echo [Step 6/6] Starting Docker services...
docker-compose up -d

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo Services:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   Database:  localhost:5432
echo   Scanner:   http://localhost:9000 (WSL2)
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo Next Steps:
echo 1. Edit .env file with your API keys
echo 2. Access the web interface at http://localhost:3000
echo 3. Create an admin account
echo 4. Start your first security scan
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
echo.
echo WSL2 Scanner Service:
echo   Status: wsl -d kali-linux sudo systemctl status security-scanner
echo   Logs:   wsl -d kali-linux journalctl -u security-scanner -f
echo.
pause
