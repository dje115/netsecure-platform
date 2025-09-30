# Ensure Scanner Service is Running
# This script checks if the scanner is running and starts it if needed

Write-Host "=" * 60
Write-Host "Checking Scanner Service Status..." -ForegroundColor Cyan
Write-Host "=" * 60

# Check if scanner is responding
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9000/health" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Scanner service is already running!" -ForegroundColor Green
        Write-Host "   Status: $($response.Content)" -ForegroundColor Gray
        exit 0
    }
}
catch {
    Write-Host "⚠️  Scanner service is not responding" -ForegroundColor Yellow
    Write-Host "   Starting scanner service..." -ForegroundColor Cyan
}

# Start the scanner service
try {
    Write-Host ""
    Write-Host "Starting scanner in WSL2..." -ForegroundColor Cyan
    
    # Start scanner in background
    wsl -d kali-linux bash -c "cd /root/security-scanner && nohup python3 scanner_service.py > scanner.log 2>&1 &"
    
    Write-Host "Waiting for scanner to initialize..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
    
    # Verify it started
    $response = Invoke-WebRequest -Uri "http://localhost:9000/health" -TimeoutSec 5
    
    if ($response.StatusCode -eq 200) {
        Write-Host ""
        Write-Host "=" * 60
        Write-Host "✅ Scanner service started successfully!" -ForegroundColor Green
        Write-Host "=" * 60
        Write-Host "   URL: http://localhost:9000" -ForegroundColor Gray
        Write-Host "   Status: $($response.Content)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "You can now run scans from the web interface!" -ForegroundColor Cyan
        Write-Host "   Web UI: http://localhost:3000" -ForegroundColor Gray
        Write-Host ""
    }
    else {
        Write-Host "❌ Scanner started but not responding correctly" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Failed to start scanner service" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Check if WSL2 is running: wsl --list --running" -ForegroundColor Gray
    Write-Host "   2. Check if Flask is installed: wsl -d kali-linux python3 -c 'import flask'" -ForegroundColor Gray
    Write-Host "   3. View scanner logs: wsl -d kali-linux cat /root/security-scanner/scanner.log" -ForegroundColor Gray
    exit 1
}


