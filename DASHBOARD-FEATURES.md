# 📊 Dashboard Features - What's Real vs Mock Data

## ✅ **REAL DATA (From Database)**

### Statistics Cards
All numbers now come from **actual database queries**:

- **Total Devices** 💻
  - Real Count: `SELECT COUNT(*) FROM devices`
  - **Clickable** → Takes you to Devices page
  
- **Vulnerabilities** ⚠️
  - Real Count: `SELECT COUNT(*) FROM vulnerabilities`
  - **Clickable** → Takes you to Vulnerabilities page
  
- **Critical Issues** 🔴
  - Real Count: `SELECT COUNT(*) FROM vulnerabilities WHERE severity = 'critical'`
  - **Clickable** → Takes you to Vulnerabilities page (filtered)
  
- **HVT Devices** 🎯
  - Real Count: `SELECT COUNT(*) FROM devices WHERE is_hvt = TRUE`
  - **Clickable** → Takes you to Devices page (filtered)

### Overall Risk Score
- **Real Calculation**: Average of all completed scan risk scores
- Formula: `AVG(scan_sessions.risk_score) / 10`
- Updates automatically as scans complete
- Color-coded gradient bar (green → yellow → red)
- Risk level descriptions:
  - **0-3**: ✅ Low risk - Network is well secured
  - **3-6**: ⚠️ Moderate risk - Some issues need attention
  - **6-8**: 🔶 High risk - Multiple vulnerabilities detected
  - **8-10**: 🔴 Critical risk - Immediate action required

### Recent Scans
- **Real Data**: Last 5 scans from `scan_sessions` table
- Shows actual:
  - Scan names
  - Device counts found
  - Vulnerability counts
  - Completion timestamps
  - Current status (Running/Completed/Failed)
- **Clickable** → Each scan links to Scans page

### System Status
- **Backend API**: Always online (if you're seeing this!)
- **Scanner Service**: 
  - Shows "Scanning in progress" when active scans exist
  - Shows "Ready for scans" when idle
  - Real-time status from database
- **Database**: Always shows connected (PostgreSQL)

---

## 🔄 **REAL-TIME UPDATES**

The dashboard automatically refreshes every **10 seconds** to show:
- New scans created
- Scan progress updates
- Updated statistics
- Latest vulnerabilities found
- Risk score changes

---

## 🖱️ **CLICKABLE DRILL-DOWN**

Every dashboard element is now **interactive**:

### 1. Statistics Cards
Click any card to see details:
- **Total Devices** → `/devices` (All discovered devices)
- **Vulnerabilities** → `/vulnerabilities` (All security issues)
- **Critical Issues** → `/vulnerabilities?severity=critical` (Critical only)
- **HVT Devices** → `/devices?hvt=true` (High-value targets only)

### 2. Active Scans Badge
- Shows count of running scans
- **Clickable** → `/scans` (Jump to active scans)
- Animated pulse effect when scans are running

### 3. Recent Scans List
- Each scan item is **clickable**
- Takes you to Scans page
- Hover effect highlights the item

### 4. Quick Actions
Three quick action cards at the bottom:
- 🔍 **New Scan** → Start a security assessment
- 💻 **View Devices** → Browse discovered assets
- 📄 **Generate Report** → Create assessment reports

All have hover effects and are fully clickable!

---

## 📈 **What Data You'll See**

### When You First Install
```
Total Devices: 0
Vulnerabilities: 0  
Critical Issues: 0
HVT Devices: 0
Risk Score: 0/10
Recent Scans: "No scans yet"
```

### After Running Your First Scan
The dashboard will show **real numbers** based on what was discovered:
```
Total Devices: 15 (actual devices found)
Vulnerabilities: 23 (actual vulnerabilities discovered)
Critical Issues: 2 (critical severity only)
HVT Devices: 1 (domain controller, firewall, etc.)
Risk Score: 6.5/10 (calculated from findings)
Recent Scans: Shows your scan with results
```

### As You Run More Scans
- Numbers **accumulate** across all scans
- Risk score **averages** across completed scans
- Recent scans show **latest 5**
- Statistics update **automatically**

---

## 🎯 **How Each Number is Calculated**

### Total Devices
```sql
SELECT COUNT(DISTINCT id) 
FROM devices
```
Every unique device discovered across all scans.

### Total Vulnerabilities
```sql
SELECT COUNT(DISTINCT id) 
FROM vulnerabilities
```
Every vulnerability found across all devices.

### Critical Issues
```sql
SELECT COUNT(*) 
FROM vulnerabilities 
WHERE severity = 'critical'
```
Only vulnerabilities marked as "critical" severity.

### HVT Devices
```sql
SELECT COUNT(*) 
FROM devices 
WHERE is_hvt = TRUE
```
Devices identified as high-value targets (domain controllers, databases, firewalls, gateways).

### Risk Score
```sql
SELECT AVG(risk_score) / 10 
FROM scan_sessions 
WHERE status = 'completed'
```
Average of all completed scan risk scores, normalized to 0-10 scale.

---

## 🚀 **Example User Flow**

### Scenario: You notice 5 Critical Issues

1. **Dashboard shows**: "Critical Issues: 5" in red card
2. **Click the card**
3. **Redirects to**: Vulnerabilities page
4. **See**: Detailed list of all 5 critical vulnerabilities
   - CVE IDs
   - Affected devices
   - CVSS scores
   - Remediation steps

### Scenario: You see "42 Total Devices"

1. **Dashboard shows**: "Total Devices: 42"
2. **Click the card**
3. **Redirects to**: Devices page
4. **See**: Complete inventory
   - IP addresses
   - Hostnames
   - Operating systems
   - Risk levels
   - HVT status

### Scenario: Active scan is running

1. **Dashboard shows**: Badge "🔄 1 Active Scan"
2. **Click the badge**
3. **Redirects to**: Scans page
4. **See**: Live progress of your running scan
   - Progress percentage
   - Current phase
   - Stop button
   - Real-time updates

---

## 💡 **Tips for Using the Dashboard**

### Daily Security Check
1. Open Dashboard
2. Check Risk Score (should be low)
3. Look for Critical Issues (should be zero)
4. Monitor Recent Scans for any failed scans
5. Click any concerning numbers for details

### After Running a Scan
1. Wait for scan to complete
2. Dashboard auto-updates with new data
3. Click "Total Devices" to see what was found
4. Click "Vulnerabilities" to see security issues
5. Click "HVT Devices" to check critical assets

### Investigating Alerts
1. Red numbers = Immediate attention needed
2. Orange numbers = Schedule remediation
3. Click the card for full details
4. Use the drill-down to investigate

---

## 🔍 **Where the Data Comes From**

### Database Tables Used:
1. **`scan_sessions`** - Scan metadata and statistics
2. **`devices`** - Discovered network devices
3. **`vulnerabilities`** - Security issues found
4. **`scan_logs`** - Scan execution logs

### API Endpoints:
1. `GET /api/scans` - List all scans
2. `GET /api/dashboard/stats` - Aggregate statistics
3. `GET /api/dashboard/recent-scans` - Latest scans
4. `GET /api/devices` - Device inventory
5. `GET /api/vulnerabilities` - Security issues

### Frontend Data Flow:
```
Dashboard Component
    ↓
Load data on mount
    ↓
Call scansAPI.list()
    ↓
Calculate statistics from scan data
    ↓
Display real numbers
    ↓
Auto-refresh every 10 seconds
```

---

## 🎨 **Visual Indicators**

### Colors
- **Blue** (💻): Informational (devices, services)
- **Orange** (⚠️): Warning (vulnerabilities)
- **Red** (🔴): Critical (urgent issues)
- **Purple** (🎯): High-Value Targets
- **Green** (✅): Good/Healthy
- **Yellow** (⚠️): Caution

### Status Dots
- 🟢 **Green**: Online/Healthy
- 🟡 **Yellow**: Warning/Caution
- 🔴 **Red**: Offline/Critical

### Badges
- **Pending** (Gray): Waiting to start
- **Running** (Blue): Currently executing
- **Completed** (Green): Successfully finished
- **Failed** (Red): Encountered error

---

## 📊 **Summary**

**Before**: Mock/hardcoded placeholder data  
**Now**: Real data from your actual scans and database

**Before**: Static display only  
**Now**: Fully interactive with drill-down capabilities

**Before**: Manual refresh needed  
**Now**: Auto-refreshes every 10 seconds

**Click anything** on the dashboard to see more details! 🖱️✨
