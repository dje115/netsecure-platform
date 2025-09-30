@echo off
cls
echo ================================================================
echo   Security Assessment Platform - Startup
echo ================================================================
echo.

echo [1/3] Checking Scanner Service...
powershell -ExecutionPolicy Bypass -File ensure-scanner-running.ps1
if errorlevel 1 (
    echo.
    echo ERROR: Scanner service failed to start
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Docker Services...
docker-compose up -d
if errorlevel 1 (
    echo.
    echo ERROR: Docker services failed to start
    pause
    exit /b 1
)

echo.
echo [3/3] Waiting for services to initialize...
timeout /t 5 /nobreak > nul

echo.
echo ================================================================
echo   Platform Started Successfully!
echo ================================================================
echo.
echo   Web Interface:  http://localhost:3000
echo   API Backend:    http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Scanner:        http://localhost:9000
echo.
echo   Login:          admin / admin123
echo.
echo ================================================================
echo.
echo Opening web interface...
start http://localhost:3000

pause


