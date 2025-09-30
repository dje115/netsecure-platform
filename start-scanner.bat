@echo off
echo Starting Security Scanner Service...
wsl -d kali-linux bash -c "cd /root/security-scanner && nohup python3 scanner_service.py > scanner.log 2>&1 &"
timeout /t 2 /nobreak > nul
echo Checking scanner status...
curl -s http://localhost:9000/health
echo.
echo Scanner service started!
echo Access at: http://localhost:9000
pause


