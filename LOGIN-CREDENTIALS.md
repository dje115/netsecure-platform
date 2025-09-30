# 🔐 Login Credentials

## Default Admin Account

**Username:** `admin`  
**Password:** `admin123`

---

## Quick Test

### Option 1: Debug Page (RECOMMENDED)
1. Open: `C:\Users\david\Documents\Netsecure\debug-auth.html`
2. Username: `admin`
3. Password: `admin123`
4. Click **Login**
5. Click **Test GET /api/scans/**
6. Click **Create Test Scan**

### Option 2: Main Application
1. Go to: `http://localhost:3000`
2. Login with `admin` / `admin123`
3. Go to Scans page
4. Create new scan

---

## Other Users in Database

Check existing users:
```powershell
docker-compose exec security-db psql -U security_admin -d security_platform -c "SELECT id, username, email, role, is_active FROM users;"
```

---

## Create New User

### Via Application
1. Go to `http://localhost:3000/login`
2. Click "Register"
3. Fill in details
4. Login with new credentials

### Via Database
```powershell
# Generate password hash first
docker-compose exec security-api python -c "from app.core.security import get_password_hash; print(get_password_hash('your_password_here'))"

# Then insert user (replace HASH with the output above)
docker-compose exec security-db psql -U security_admin -d security_platform -c "INSERT INTO users (username, email, hashed_password, role, is_active) VALUES ('newuser', 'user@example.com', 'HASH', 'analyst', true);"
```

---

## Reset Admin Password

If you forget the admin password, run:
```powershell
# Generate new hash
docker-compose exec security-api python -c "from app.core.security import get_password_hash; print(get_password_hash('new_password'))"

# Update in database (replace HASH with output)
docker-compose exec security-db psql -U security_admin -d security_platform -c "UPDATE users SET hashed_password = 'HASH' WHERE username = 'admin';"
```

---

## Troubleshooting

### "401 Unauthorized" Errors

**Cause**: Not logged in or token expired

**Fix**:
1. Logout and login again
2. Check token in browser console:
   ```javascript
   localStorage.getItem('token')
   ```
3. If null, login again
4. Use debug page to verify auth works

### "Failed to load scans"

**Cause**: Authentication issue

**Fix**:
1. Open `debug-auth.html`
2. Login
3. Click **Test GET /api/scans/**
4. Check what error appears

### Can't Login

**Cause**: Wrong password or user doesn't exist

**Fix**:
1. Reset password using commands above
2. Or create new user via register page

---

## API Testing

Use `debug-auth.html` to test:
- ✅ Login endpoint
- ✅ Scans API
- ✅ Dashboard API
- ✅ Current user endpoint
- ✅ Create scan endpoint

All with detailed error messages and token inspection!

---

## Security Notes

**⚠️ IMPORTANT**: 
- Change the default `admin123` password in production!
- Use strong passwords for all accounts
- The SECRET_KEY in .env should be changed
- Database password should be changed from default

### Change Passwords in Production

1. Update `.env` file:
   ```
   SECRET_KEY=your_strong_random_key_here
   DB_PASSWORD=your_strong_db_password_here
   ```

2. Restart services:
   ```powershell
   docker-compose down
   docker-compose up -d --build
   ```

3. Reset all user passwords via the application or database
