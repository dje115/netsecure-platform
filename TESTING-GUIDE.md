# 🧪 Testing Guide - Security Platform

## Quick Test Steps

### 1. Open Test Page
Open this file in your browser:
```
C:\Users\david\Documents\Netsecure\test-auth.html
```

Or navigate to: `file:///C:/Users/david/Documents/Netsecure/test-auth.html`

### 2. Register a User (First Time Only)
1. Enter username: `testuser`
2. Enter email: `test@example.com`
3. Enter password: `testpass123`
4. Click **Register**
5. Check output - should show success message

### 3. Login
1. Enter username: `testuser` (or the username you registered)
2. Enter password: `testpass123`
3. Click **Login**
4. Check output - should show:
   ```json
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "token_type": "bearer"
   }
   ```
5. Should also see: "Token saved to localStorage"

### 4. Test Scans API
1. Click **Get Scans** - Should show empty array `[]` if no scans yet
2. Click **Create Test Scan** - Should create a scan for `192.168.22.1`
3. Click **Get Scans** again - Should now show the scan

### 5. Use Main Application
1. Navigate to: `http://localhost:3000`
2. Login with same credentials
3. Go to **Scans** page
4. Click **+ New Scan**
5. Enter:
   - Name: `Home Network Test`
   - Target: `192.168.22.0/24` or `192.168.22.1`
   - Type: Quick Scan
6. Click **Start Scan**

---

## Expected Test Results

### ✅ Success Indicators

#### Registration
```json
{
  "message": "User registered successfully",
  "username": "testuser",
  "role": "analyst"
}
```

#### Login
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTcwMTM...",
  "token_type": "bearer"
}
```

#### Get Scans (Empty)
```json
[]
```

#### Create Scan
```json
{
  "id": 1,
  "name": "Test Scan",
  "target_range": "192.168.22.1",
  "status": "starting",
  "message": "Scan started successfully in background"
}
```

### ❌ Common Errors

#### 401 Unauthorized
**Problem**: Token not included or invalid
**Solution**: 
1. Make sure you logged in successfully
2. Check localStorage for token: `localStorage.getItem('token')`
3. Try logging in again

#### CORS Error
**Problem**: Frontend can't connect to backend
**Console Shows**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`
**Solution**:
1. Check if backend is running: `docker-compose ps`
2. Restart services: `docker-compose restart`

#### Connection Refused
**Problem**: Backend API not running
**Console Shows**: `Failed to fetch` or `net::ERR_CONNECTION_REFUSED`
**Solution**:
```bash
docker-compose up -d
docker-compose logs security-api
```

---

## Debugging Commands

### Check if Services are Running
```powershell
docker-compose ps
```

Should show:
```
NAME                    STATUS
security-api            Up
security-frontend       Up
security-db             Up
security-redis          Up
security-celery         Up
```

### Check Backend Logs
```powershell
docker-compose logs security-api --tail=50
```

### Check Frontend Logs
```powershell
docker-compose logs security-frontend --tail=50
```

### Check if API is Responding
```powershell
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "scanner": "ready"
}
```

### Restart Everything
```powershell
docker-compose down
docker-compose up -d --build
```

---

## Test Targets

### For Testing Scans

#### Single IP
```
192.168.22.1
```

#### IP Range (CIDR)
```
192.168.22.0/24
```

#### Multiple IPs
```
192.168.22.1,192.168.22.10,192.168.22.20
```

---

## Browser Console Debugging

### Open Browser Console
- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I`
- **Firefox**: Press `F12` or `Ctrl+Shift+K`

### Check for Errors
Look for red error messages in the Console tab

### Common Console Errors

#### "Failed to load scans"
**Check**:
1. Network tab - is the request going to `http://localhost:8000/api/scans/`?
2. What's the response status? (200, 401, 500?)
3. Click on the request - check Headers tab for Authorization header

#### "401 Unauthorized"
**Check**:
1. Run in console: `localStorage.getItem('token')`
2. Should show a long string starting with `eyJ...`
3. If null, you need to login again

#### "TypeError: Cannot read properties of undefined"
**Cause**: API response format mismatch
**Fix**: Check backend logs for errors

---

## API Endpoints Reference

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info

### Scans
- `GET /api/scans/` - List all scans
- `POST /api/scans/` - Create new scan
- `GET /api/scans/{id}` - Get scan details
- `POST /api/scans/{id}/start` - Start a scan
- `POST /api/scans/{id}/stop` - Stop a scan

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/recent-scans` - Get recent scans

### Devices
- `GET /api/devices/` - List all devices
- `GET /api/devices/{id}` - Get device details

### Vulnerabilities
- `GET /api/vulnerabilities/` - List all vulnerabilities
- `GET /api/vulnerabilities/{id}` - Get vulnerability details

---

## Settings Page

### Access Settings
1. Login to platform
2. Click **⚙️ Settings** in top right navigation
3. Configure:
   - OpenAI API Key (for GPT-4 analysis)
   - Anthropic API Key (for Claude analysis)
   - Scan timeout settings
   - Feature toggles

### Settings are Stored
- **Location**: Browser localStorage
- **Key**: `platform_settings`
- **View in Console**: `localStorage.getItem('platform_settings')`

---

## Quick Troubleshooting

### "Failed to load scans" Error

**Step 1**: Check if you're logged in
```javascript
// Run in browser console
console.log(localStorage.getItem('token'))
// Should show a token, not null
```

**Step 2**: Check if API is running
```powershell
curl http://localhost:8000/health
```

**Step 3**: Check backend logs
```powershell
docker-compose logs security-api --tail=20
```

**Step 4**: Try logging out and back in
1. Click Logout
2. Login again
3. Try creating a scan

### Scan Gets Created but Doesn't Run

**Cause**: Scanner service or Celery worker not running

**Check**:
```powershell
docker-compose ps
```

Look for `security-celery` - should be "Up"

**Fix**:
```powershell
docker-compose restart security-celery
docker-compose logs security-celery --tail=20
```

### Settings Not Saving

**Cause**: Browser localStorage disabled or full

**Check**:
```javascript
// Run in browser console
try {
    localStorage.setItem('test', 'test');
    console.log('localStorage works');
} catch(e) {
    console.error('localStorage error:', e);
}
```

---

## Test Checklist

- [ ] Services are all running (`docker-compose ps`)
- [ ] Can register a user
- [ ] Can login and receive token
- [ ] Token is saved to localStorage
- [ ] Can access Dashboard
- [ ] Can access Settings page
- [ ] Can create a scan
- [ ] Scan appears in Active Scans
- [ ] Can stop a scan
- [ ] Scan moves to History
- [ ] Dashboard shows updated statistics

---

## Need Help?

### Check Logs
```powershell
# All logs
docker-compose logs

# Specific service
docker-compose logs security-api
docker-compose logs security-celery
docker-compose logs security-frontend
```

### Restart Services
```powershell
# Restart specific service
docker-compose restart security-api

# Restart all
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up -d --build
```

### Database Issues
```powershell
# Connect to database
docker-compose exec security-db psql -U security_user -d security_db

# Check tables
\dt

# Check users
SELECT * FROM users;

# Check scans
SELECT * FROM scan_sessions;

# Exit
\q
```

