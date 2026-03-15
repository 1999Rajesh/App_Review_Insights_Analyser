# 🚀 Quick Reference - 5-Minute Scheduler

## Current Configuration ✅

```
Schedule:        Every 5 minutes
Next Run:        :00, :05, :10, :15, :20, :25, :30, :35, :40, :45, :50, :55
Log File:        backend/logs/scheduler.log
Recipient Email: codeflex1999@gmail.com
Reviews Loaded:  100 (auto-imported)
```

---

## 🔍 Monitor in Real-Time

### Option 1: Watch Logs (PowerShell)
```powershell
cd backend
Get-Content logs/scheduler.log -Wait -Tail 20
```

### Option 2: Check Status API
```powershell
Invoke-WebRequest http://localhost:8000/api/scheduler/status | ConvertFrom-Json
```

### Option 3: View Console
Scheduler logs appear in the terminal running the backend server.

---

## ⏱️ What to Expect

### Every 5 Minutes:
```
[XX:00] Scheduler triggers
[XX:00] Analyzing 100 reviews...
[XX:03] Identified 5 themes
[XX:03] Creating report...
[XX:03] Sending email...
[XX:07] ✅ Email sent to codeflex1999@gmail.com
[XX:07] 🎉 WEEKLY PULSE COMPLETE
```

### Check Email:
- **To:** codeflex1999@gmail.com
- **Subject:** Weekly App Review Pulse - March 15, 2026 01:53
- **Frequency:** Every 5 minutes while server runs

---

## 🎛️ Quick Commands

### Start Server
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Check Health
```bash
curl http://localhost:8000/health
```

### Trigger Manually
```bash
curl -X POST http://localhost:8000/api/scheduler/trigger-now
```

### Stop Scheduler
```bash
curl -X POST http://localhost:8000/api/scheduler/stop
```

### Start Scheduler
```bash
curl -X POST http://localhost:8000/api/scheduler/start
```

---

## 🔧 Change Interval

### Edit `backend/.env`:
```bash
# Every 10 minutes
SCHEDULER_INTERVAL_MINUTES=10

# Every hour
SCHEDULER_INTERVAL_MINUTES=60

# Weekly (production)
SCHEDULER_INTERVAL_MINUTES=10080
```

**Then restart server.**

---

## 📊 Log File Location

```
backend/
└── logs/
    └── scheduler.log  ← All scheduler events logged here
```

### View Recent Logs:
```powershell
# Last 30 lines
Get-Content logs/scheduler.log -Tail 30

# Search for errors
Select-String -Path logs/scheduler.log -Pattern "ERROR"

# Count successful runs
Select-String -Path logs/scheduler.log -Pattern "WEEKLY PULSE COMPLETE" | Measure-Object
```

---

## 🐛 Troubleshooting

### No emails received?
1. Check SMTP settings in `.env`
2. Verify logs show "Email sent successfully"
3. Check spam folder

### Scheduler not running?
```powershell
# Check status
curl http://localhost:8000/api/scheduler/status

# Start manually
curl -X POST http://localhost:8000/api/scheduler/start
```

### Need to see what's happening?
```powershell
# Watch logs in real-time
Get-Content logs/scheduler.log -Wait -Tail 20
```

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Console shows: `🤖 WEEKLY PULSE SCHEDULER STARTED`
2. ✅ Status shows: `"scheduler_running": true`
3. ✅ Logs appear every 5 minutes
4. ✅ Emails arrive at codeflex1999@gmail.com
5. ✅ Log file grows with each run

---

## 📝 Files Modified

| File | Purpose |
|------|---------|
| `backend/app/services/weekly_pulse_scheduler.py` | Main scheduler logic |
| `backend/app/config.py` | Configuration settings |
| `backend/.env` | Environment variables |
| `backend/logs/scheduler.log` | Auto-created log file |

---

**Last Updated:** March 15, 2026  
**Status:** ✅ OPERATIONAL  
**Next Run:** Check `/api/scheduler/status` endpoint
