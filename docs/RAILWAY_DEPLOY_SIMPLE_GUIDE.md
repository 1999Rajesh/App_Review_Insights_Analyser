# 🚀 Deploy to Railway - SIMPLE GUIDE

## ⚡ Quick Deploy (Choose ONE method)

### Method 1: Using Browser (EASIEST - Recommended)

**Follow these steps in your browser:**

---

#### Step 1: Go to Railway
👉 **Click here:** https://railway.app

Sign in with GitHub (recommended) or Google.

---

#### Step 2: Create New Project
1. Click the big **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Find and click: `1999Rajesh/App_Review_Insights_Analyser`
4. Railway will start building automatically

**Wait 2-3 minutes** for the build to complete.

You'll see: ✅ **"Deployment successful"**

---

#### Step 3: Add Environment Variables

Click on your service → **"Variables"** tab → **"New Variable"**

Add these variables one by one (copy-paste):

```
PLAY_STORE_DEFAULT_APP_ID = com.nextbillion.groww
PLAY_STORE_LANGUAGE = en
PLAY_STORE_COUNTRY = in
MAX_REVIEWS_TO_FETCH = 500
REVIEW_WEEKS_RANGE = 12
MIN_REVIEW_WORD_COUNT = 5
ALLOW_EMOJIS = false
REQUIRED_LANGUAGE = en
REVIEWS_DATA_DIR = data/reviews
CSV_DATA_DIR = weekly_reviews
```

Click **"Add"** after each variable.

---

#### Step 4: Add Email Variables (Optional but Recommended)

If you want weekly email reports, add these too:

```
SMTP_SENDER_EMAIL = your-email@gmail.com
SMTP_PASSWORD = xxxx-xxxx-xxxx-xxxx
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
WEEKLY_REPORT_EMAIL = your-email@gmail.com
SCHEDULER_INTERVAL_MINUTES = 5
```

**Important:** For `SMTP_PASSWORD`, use Gmail App Password, not your regular password.

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Create new app password for "Mail"
3. Copy the 16-character code (no spaces)
4. Paste it as `SMTP_PASSWORD`

---

#### Step 5: Create Weekly Schedule

1. In Railway dashboard, click **"New"** → **"Scheduled Task"**
2. Select your deployed service
3. Fill in:
   - **Name:** Weekly Review Pipeline
   - **Command:** `python -m services.railway_weekly_task`
   - **Schedule:** `0 10 * * 1`
4. Click **"Deploy"**

**What this means:** Runs every Monday at 10:00 AM IST

---

#### Step 6: Test It!

**Option A: Wait for Monday** (if today is before Monday 10 AM IST)

**Option B: Test manually right now:**

1. Click on your service → **"Settings"** → **"Shell"**
2. Type this command:
   ```bash
   python -m services.weekly_review_pipeline --no-email
   ```
3. Press Enter and watch it run!

Expected output:
```
✅ Reviews collected: 280
✅ Themes identified: 5
✅ Pipeline complete!
```

---

#### Step 7: Success! 🎉

You should now see:
- ✅ Service running (green dot)
- ✅ Latest deployment successful
- ✅ Scheduled task created
- ✅ Next run time displayed

**Bookmark this page:** Your Railway dashboard

---

### Method 2: Using Command Line (Advanced)

If you prefer terminal commands:

```bash
# Run the deployment script
.\deploy-to-railway.bat
```

This script will:
1. Install Railway CLI
2. Login to Railway
3. Link your GitHub repo
4. Start deployment

Then follow the on-screen instructions.

---

## 📊 What Happens After Deployment?

### Every Monday at 10 AM IST:

1. **10:00 AM** - Task triggers automatically
2. **10:01 AM** - Fetches latest reviews from Play Store
3. **10:03 AM** - Applies filters & removes PII
4. **10:05 AM** - Saves JSON + CSV files
5. **10:07 AM** - Generates weekly note with themes
6. **10:10 AM** - Emails you the report

### You Get:
- 📧 Email with top 3 themes
- 💬 3 user quotes per theme  
- ✅ 3 action items per theme
- 🔒 Zero PII (privacy protected)

---

## 🔍 How to Check If It's Working

### Check Service Status
1. Go to Railway dashboard
2. Your service should show **green dot** (running)
3. Click to see logs

### View Logs
1. Click your service → **"Logs"** tab
2. You should see startup messages

### Check Scheduled Tasks
1. Railway dashboard → **"Scheduled Tasks"**
2. Should show: "Weekly Review Pipeline"
3. Next run time displayed

### Test API
Railway gives you a URL like:
```
https://your-app-production.up.railway.app
```

Open in browser:
```
https://your-app-production.up.railway.app/api/reviews/stats
```

Should return JSON with review statistics.

---

## 🛠️ Troubleshooting

### "Build Failed"
- Click on failed deployment
- Read error message
- Common fix: Make sure all files are committed and pushed

### "Service Crashed"
- Check logs for error message
- Verify all environment variables are set correctly
- Especially `PLAY_STORE_DEFAULT_APP_ID`

### "No Reviews Found"
- Check app ID: should be `com.nextbillion.groww`
- Verify Railway has internet access (it does by default)
- Try manual trigger in shell

### "Email Not Sending"
- Verify SMTP_PASSWORD is Gmail App Password (not regular password)
- Check all SMTP variables are correct
- Ensure Gmail 2FA is enabled

---

## 📞 Need Help?

### Railway Resources
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

### Your Project
- GitHub: https://github.com/1999Rajesh/App_Review_Insights_Analyser
- Full Guide: See `docs/DEPLOY_TO_RAILWAY_STEP_BY_STEP.md`

---

## ✅ Deployment Checklist

Use this to track your progress:

- [ ] 1. Created Railway account
- [ ] 2. Deployed from GitHub
- [ ] 3. Build completed successfully
- [ ] 4. Added all environment variables
- [ ] 5. Created scheduled task
- [ ] 6. Tested manually (optional)
- [ ] 7. Verified service is running
- [ ] 8. Bookmarked Railway dashboard

---

## 🎯 That's It!

You now have an automated weekly review analysis pipeline running in the cloud!

**Every Monday**, you'll receive actionable insights from app reviews.

**Zero manual effort required** after setup.

---

**Questions?** Open an issue on GitHub or check the full documentation.

**Powered by App Review Insights Analyzer** 🚀
