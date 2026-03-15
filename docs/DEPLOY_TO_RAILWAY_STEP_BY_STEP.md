# 🚀 Railway Deployment Guide - Weekly Review Pipeline

## Quick Deploy (5 Minutes)

### Step 1: Go to Railway
👉 Visit: https://railway.app/

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: `App_Review_Insights_Analyser`
4. Railway will auto-detect the root `Dockerfile`

### Step 3: Configure Build
Railway will automatically:
- ✅ Detect Python environment
- ✅ Install dependencies from `requirements.txt`
- ✅ Build from root `Dockerfile`
- ✅ Deploy FastAPI backend

**Wait for build to complete** (~2-3 minutes)

---

## ⚙️ Step 4: Add Environment Variables

In Railway dashboard, go to your project → **Variables** → **Add Variable**

### Required Variables (Copy-Paste Ready)

```bash
# ===== PLAY STORE CONFIGURATION =====
PLAY_STORE_DEFAULT_APP_ID=com.nextbillion.groww
PLAY_STORE_LANGUAGE=en
PLAY_STORE_COUNTRY=in

# ===== REVIEW FILTERS =====
MAX_REVIEWS_TO_FETCH=500
REVIEW_WEEKS_RANGE=12
MIN_REVIEW_WORD_COUNT=5
ALLOW_EMOJIS=false
REQUIRED_LANGUAGE=en

# ===== DATA DIRECTORIES =====
REVIEWS_DATA_DIR=data/reviews
CSV_DATA_DIR=weekly_reviews

# ===== EMAIL CONFIGURATION (For Weekly Reports) =====
SMTP_SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
WEEKLY_REPORT_EMAIL=recipient@example.com

# ===== SCHEDULER CONFIGURATION =====
SCHEDULER_INTERVAL_MINUTES=5
```

### How to Add Each Variable:

1. Click **"New Variable"**
2. Enter variable name (e.g., `PLAY_STORE_DEFAULT_APP_ID`)
3. Enter value (e.g., `com.nextbillion.groww`)
4. Click **"Save"**
5. Repeat for all variables above

---

## 📧 Gmail App Password Setup (Required for Email)

If you want weekly email reports:

### Step 1: Enable 2FA on Gmail
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)

### Step 2: Generate App Password
1. Visit: https://myaccount.google.com/apppasswords
2. Select app: **"Mail"**
3. Select device: **"Other (Custom name)"**
4. Enter name: `"Railway Weekly Reports"`
5. Click **"Generate"**
6. Copy the **16-character password** (spaces removed)

### Step 3: Add to Railway
```bash
SMTP_SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # 16-char password (no spaces)
```

---

## ⏰ Step 5: Create Weekly Scheduled Task

### Option A: Using Railway Dashboard

1. Go to your Railway project
2. Click **"New"** → **"Scheduled Task"**
3. Select your deployed service
4. Configure:
   - **Command:** `python -m services.railway_weekly_task`
   - **Schedule:** `0 10 * * 1` (Every Monday at 10:00 AM IST)
   - **Name:** "Weekly Review Pipeline"
5. Click **"Deploy"**

### Option B: Using Railway CLI

```bash
# Install Railway CLI (if not installed)
npm i -g @railway/cli

# Login
railway login

# Create scheduled task
railway schedule create \
  --cmd "python -m services.railway_weekly_task" \
  --cron "0 10 * * 1"
```

---

## 🔍 Step 6: Verify Deployment

### Check Service Status

1. Go to Railway dashboard
2. Your service should show:
   - ✅ **Status:** Running
   - ✅ **Deployments:** Latest successful
   - ✅ **Logs:** No errors

### Test API Endpoint

Railway will provide a public URL like:
```
https://your-app-production.up.railway.app
```

Test the API:
```bash
# In browser or curl
curl https://your-app-production.up.railway.app/api/reviews/stats
```

Expected response:
```json
{
  "total_reviews": 0,
  "average_rating": 0,
  "last_updated": "2026-03-15T..."
}
```

---

## 🧪 Step 7: Test the Pipeline

### Manual Trigger (First Time)

Run the pipeline manually to verify everything works:

```bash
# In Railway dashboard → Settings → Shell
# Or use Railway CLI:
railway run python -m services.weekly_review_pipeline --no-email
```

Expected output:
```
======================================================================
🚀 WEEKLY REVIEW PIPELINE
⏰ Started at: 2026-03-15 17:30:00
======================================================================

📥 STEP 1/4: COLLECTING REVIEWS
...
✅ Reviews collected: 280

📝 STEP 2/4: GENERATING WEEKLY PULSE NOTE
...
✅ Themes identified: 5

✅ STEP 4/4: PIPELINE COMPLETE
```

---

## 📊 Step 8: Monitor Execution

### View Logs

In Railway dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. You should see:
   ```
   🤖 RAILWAY SCHEDULED TASK: WEEKLY REVIEW PIPELINE
   ✅ Environment variables configured
   🚀 Fetching reviews for com.nextbillion.groww...
   ✅ Successfully saved 280 reviews
   🎉 PIPELINE EXECUTION SUCCESSFUL
   ```

### Check Generated Files

After first run, verify files exist:
```bash
# In Railway shell
ls data/reviews/
# Should see: 2026-03-15.json

ls weekly_reviews/
# Should see: reviews_2026_week_11.csv
```

---

## 🛠️ Troubleshooting

### Issue: Build Failed

**Solution:** Check build logs
```
1. Go to Railway → Deployments → Latest
2. Click on failed deployment
3. Check for errors in:
   - Installing dependencies
   - Copying files
   - Building image
```

Common fixes:
- Ensure `requirements.txt` is in `backend/` folder
- Check Dockerfile paths are correct
- Verify no syntax errors in Python files

### Issue: Service Crashes on Start

**Solution:** Check startup logs
```
1. Railway dashboard → Logs
2. Look for errors like:
   - ModuleNotFoundError → Missing dependency
   - FileNotFoundError → Missing file/directory
   - ValidationError → Invalid .env variable
```

Fix:
```bash
# Add missing dependency to requirements.txt
# Or create missing directory in code
os.makedirs('data/reviews', exist_ok=True)
```

### Issue: Scheduled Task Not Running

**Solution:** Verify schedule configuration
```
1. Railway → Scheduled Tasks
2. Check task exists and is enabled
3. Verify cron expression: 0 10 * * 1
4. Check last run time
```

Manual trigger:
```bash
railway run python -m services.railway_weekly_task
```

### Issue: Email Not Sending

**Solution:** Verify SMTP configuration
```
1. Check all SMTP variables are set:
   - SMTP_SENDER_EMAIL
   - SMTP_PASSWORD (must be App Password, not regular password)
   - SMTP_HOST
   - SMTP_PORT

2. Test email manually:
   python -c "from app.services.email_sender import EmailSender; e = EmailSender(); print(e.send_test_email('test@example.com'))"
```

### Issue: No Reviews Fetched

**Solution:** Check Play Store scraper
```
1. Verify app ID is correct:
   echo $PLAY_STORE_DEFAULT_APP_ID
   # Should output: com.nextbillion.groww

2. Test scraper manually:
   python -c "from google_play_scraper import reviews_all; r = reviews_all('com.nextbillion.groww', count=10); print(len(r))"

3. Check network connectivity:
   - Railway has internet access by default
   - No proxy/firewall issues
```

---

## 📈 Success Metrics

After deployment, you should see:

### ✅ Week 1 (First Run)
- [ ] Service deployed successfully
- [ ] All environment variables set
- [ ] Manual test run completed
- [ ] First JSON file created
- [ ] First CSV file created
- [ ] First weekly note generated

### ✅ Week 2+ (Automated)
- [ ] Scheduled task runs automatically (Monday 10 AM IST)
- [ ] Weekly email received
- [ ] New CSV file added to `weekly_reviews/`
- [ ] JSON file updated with new data
- [ ] Logs show successful execution

### ✅ After 8-12 Weeks
- [ ] 8-12 weekly CSV files accumulated
- [ ] Trend analysis possible
- [ ] Historical dataset built
- [ ] Consistent weekly insights

---

## 🎯 Deployment Checklist

Use this checklist to ensure everything is set up correctly:

### Pre-Deployment
- [ ] Code pushed to GitHub ✅ (Already done!)
- [ ] Repository is public or Railway has access
- [ ] Root Dockerfile exists ✅
- [ ] railway.toml configured ✅

### Deployment
- [ ] Railway project created from GitHub
- [ ] Build completed successfully
- [ ] Service is running (green status)
- [ ] API endpoint accessible

### Configuration
- [ ] All environment variables added
- [ ] Gmail 2FA enabled (for email)
- [ ] Gmail App Password generated
- [ ] SMTP variables configured

### Automation
- [ ] Scheduled task created
- [ ] Cron expression set: `0 10 * * 1`
- [ ] Command configured: `python -m services.railway_weekly_task`
- [ ] Task is enabled and active

### Testing
- [ ] Manual pipeline run successful
- [ ] JSON file created
- [ ] CSV file created
- [ ] Weekly note generated
- [ ] (Optional) Email sent successfully

### Monitoring
- [ ] Logs accessible
- [ ] Health check passing
- [ ] No errors in logs
- [ ] Next scheduled run time noted

---

## 📞 Support Resources

### Railway Documentation
- [Deploying from GitHub](https://docs.railway.app/deploy/github)
- [Environment Variables](https://docs.railway.app/deploy/environment-variables)
- [Scheduled Tasks](https://docs.railway.app/deploy/cron-jobs)
- [Viewing Logs](https://docs.railway.app/guides/logs)

### Railway CLI
- [CLI Installation](https://docs.railway.app/cli)
- [CLI Commands](https://docs.railway.app/cli/commands)

### Community Help
- [Railway Discord](https://discord.gg/railway)
- [GitHub Issues](https://github.com/1999Rajesh/App_Review_Insights_Analyser/issues)

---

## 🎉 Post-Deployment

Once deployed successfully:

1. **Bookmark your Railway dashboard**
2. **Save the public API URL**
3. **Note the next scheduled run time**
4. **Set calendar reminder to check first email**

### Share Your Success

Your automated pipeline is now:
- ✅ Fetching reviews weekly
- ✅ Analyzing themes automatically
- ✅ Generating actionable insights
- ✅ Emailing reports hands-free
- ✅ Building historical dataset

**You're done! Sit back and let the automation work for you.** 🚀

---

**Powered by App Review Insights Analyzer**  
*Turning app store reviews into actionable weekly insights*
