# 🚀 Backend Deployment - Step by Step Guide

**Goal:** Deploy backend to Railway and verify it's working  
**Time:** 10-15 minutes  
**Status:** Ready to deploy

---

## 📋 **Step 1: Install Railway CLI**

### Command:
```bash
npm install -g @railway/cli
```

### Verify Installation:
```bash
railway --version
```

**Expected Output:** Should show version number (e.g., `3.8.0`)

---

## 📋 **Step 2: Login to Railway**

### Command:
```bash
railway login
```

**What Happens:**
- Opens browser automatically
- You login with GitHub account
- Browser shows "Successfully logged in"
- Terminal continues

**Expected Output:**
```
✓ Logged in as your-username
```

---

## 📋 **Step 3: Initialize Railway Project**

### Option A: Create New Project
```bash
cd backend
railway init
```

### Option B: Link Existing Project
```bash
cd backend
railway link
```

**What to Do:**
- Select your project from list, OR
- Create new project

**Expected Output:**
```
✓ Created new project: App Review Insights Analyzer
✓ Linked to project
```

---

## 📋 **Step 4: Set Environment Variables**

### Quick Method (All at Once):
```bash
cd backend

railway variables set \
  GEMINI_API_KEY=your_actual_gemini_api_key \
  GEMINI_MODEL=gemini-2.5-flash \
  SMTP_SERVER=smtp.gmail.com \
  SMTP_PORT=465 \
  SENDER_EMAIL=your.email@gmail.com \
  SENDER_PASSWORD=your_app_password_no_spaces \
  RECIPIENT_EMAIL=your.email@gmail.com \
  BACKEND_CORS_ORIGINS=https://your-app.vercel.app \
  MAX_THEMES=5 \
  MAX_WORDS=250 \
  REVIEW_WEEKS_RANGE=8 \
  MAX_REVIEWS_TO_FETCH=500 \
  PLAY_STORE_DEFAULT_APP_ID=in.groww \
  PLAY_STORE_COUNTRY=in \
  PLAY_STORE_LANGUAGE=en \
  PORT=8000 \
  SCHEDULER_INTERVAL_MINUTES=10080
```

### Interactive Method (One by One):
```bash
cd backend

# Add each variable separately
railway variables set GEMINI_API_KEY=your_key_here
railway variables set GEMINI_MODEL=gemini-2.5-flash
railway variables set SMTP_SERVER=smtp.gmail.com
railway variables set SMTP_PORT=465
railway variables set SENDER_EMAIL=your.email@gmail.com
railway variables set SENDER_PASSWORD=your_app_password_no_spaces
railway variables set RECIPIENT_EMAIL=your.email@gmail.com
railway variables set BACKEND_CORS_ORIGINS=https://placeholder.com
railway variables set MAX_THEMES=5
railway variables set MAX_WORDS=250
railway variables set REVIEW_WEEKS_RANGE=8
railway variables set MAX_REVIEWS_TO_FETCH=500
railway variables set PLAY_STORE_DEFAULT_APP_ID=in.groww
railway variables set PLAY_STORE_COUNTRY=in
railway variables set PLAY_STORE_LANGUAGE=en
railway variables set PORT=8000
railway variables set SCHEDULER_INTERVAL_MINUTES=10080
```

### Verify Variables:
```bash
railway variables
```

**Expected Output:** Should list all 17 environment variables

---

## 📋 **Step 5: Deploy with Docker**

### Deploy Command:
```bash
cd backend
railway up --dockerfile Dockerfile
```

**What Happens:**
1. Detects Dockerfile
2. Builds Docker image
3. Pushes to Railway
4. Starts container
5. Shows live logs

**Watch for These Messages:**
```
✓ Building docker image
✓ Pushing to registry
✓ Deploying...
✓ Service ready! https://your-app-production.up.railway.app
```

**Deployment takes:** 3-5 minutes first time

---

## 📋 **Step 6: Get Your Railway URL**

### Find URL:
```bash
railway domain
```

**OR** Check in dashboard:
```bash
railway open
```

**Your URL will be:**
```
https://your-app-production.up.railway.app
```

**Write this down!** You'll need it for frontend deployment.

---

## ✅ **Step 7: Verify Deployment (Testing)**

### Test 1: Check if Backend is Running

```bash
curl https://your-app-production.up.railway.app/api/reviews/stats
```

**Replace `your-app-production.up.railway.app` with your actual URL**

**Expected Response:**
```json
{
  "total": 0,
  "app_store": 0,
  "play_store": 0,
  "average_rating": 0
}
```

✅ **PASS** if you get JSON response  
❌ **FAIL** if connection error or timeout

---

### Test 2: Check API Documentation

Open in browser:
```
https://your-app-production.up.railway.app/docs
```

✅ **PASS** if Swagger UI loads  
❌ **FAIL** if page not found

---

### Test 3: Test Play Store Fetch

```bash
curl -X POST https://your-app-production.up.railway.app/api/reviews/fetch-play-store \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "com.whatsapp",
    "weeks": 4,
    "max_reviews": 50,
    "country": "us",
    "language": "en"
  }'
```

**Expected Response:**
```json
{
  "message": "Successfully fetched X reviews from Google Play Store",
  "fetched_count": X,
  "total_in_database": X
}
```

✅ **PASS** if reviews are fetched  
⚠️ **EXPECTED FAIL** if app not available in US store (try different app)

---

### Test 4: Generate Weekly Report

```bash
curl -X POST https://your-app-production.up.railway.app/api/analysis/generate-weekly-report
```

**Note:** This may take 15-20 seconds

**Expected Response:**
```json
{
  "id": "report_xxx",
  "week_start": "2026-...",
  "week_end": "2026-...",
  "total_reviews": X,
  "top_themes": [...],
  "generated_at": "..."
}
```

✅ **PASS** if report generated  
⚠️ **EXPECTED FAIL** if no reviews in database (fetch some first)

---

### Test 5: Check Scheduler Status

```bash
curl https://your-app-production.up.railway.app/api/scheduler/status
```

**Expected Response:**
```json
{
  "is_running": true,
  "recipient_email": "your.email@gmail.com",
  "schedule": "Every 10080 minutes",
  "next_run": "2026-...",
  "next_run_formatted": "..."
}
```

✅ **PASS** if scheduler is running  
❌ **FAIL** if not running (check logs)

---

## 🐛 **Troubleshooting Common Issues**

### Issue 1: "Command not found: railway"

**Problem:** Railway CLI not installed

**Solution:**
```bash
npm install -g @railway/cli
```

---

### Issue 2: "Authentication failed"

**Problem:** Not logged in

**Solution:**
```bash
railway login
```

---

### Issue 3: "No projects found"

**Problem:** No Railway project created yet

**Solution:**
```bash
railway init
```
Then select "Create new project"

---

### Issue 4: "Port not available" or "Address already in use"

**Problem:** PORT environment variable not set

**Solution:**
```bash
railway variables set PORT=8000
railway restart
```

---

### Issue 5: "Docker build failed"

**Problem:** Dockerfile issue or missing files

**Solution:**
1. Check Dockerfile exists:
   ```bash
   ls backend/Dockerfile
   ```
2. Check requirements.txt exists:
   ```bash
   ls backend/requirements.txt
   ```
3. Redeploy:
   ```bash
   railway up --dockerfile Dockerfile
   ```

---

### Issue 6: "CORS error when testing from frontend"

**Problem:** CORS not configured for your frontend domain

**Solution:**
```bash
railway variables set BACKEND_CORS_ORIGINS=https://your-app.vercel.app
railway restart
```

---

### Issue 7: "Gmail authentication failed"

**Problem:** Wrong Gmail password

**Solution:**
1. Get app password from https://myaccount.google.com/apppasswords
2. Copy WITHOUT SPACES
3. Update Railway:
   ```bash
   railway variables set SENDER_PASSWORD=your_password_no_spaces
   railway restart
   ```

---

## 📊 **Verification Checklist**

Use this checklist to confirm everything is working:

### Pre-Deployment ✅
- [ ] Node.js installed (`node --version`)
- [ ] Railway CLI installed (`railway --version`)
- [ ] Railway account created
- [ ] Gmail app password obtained
- [ ] Gemini API key obtained

### Deployment ✅
- [ ] Logged into Railway
- [ ] Project created/linked
- [ ] All 17 environment variables set
- [ ] Dockerfile deployed successfully
- [ ] Railway URL obtained

### Post-Deployment Tests ✅
- [ ] `/api/reviews/stats` returns data
- [ ] `/docs` loads Swagger UI
- [ ] Play Store fetch works
- [ ] Report generation works
- [ ] Scheduler is running
- [ ] No errors in Railway logs

---

## 🔍 **Monitoring After Deployment**

### View Live Logs:
```bash
railway logs --follow
```

### View Metrics:
```bash
railway metrics
```

### Open Dashboard:
```bash
railway open
```

### Restart if Needed:
```bash
railway restart
```

---

## 🎯 **Quick Verification Commands Summary**

After deployment, run these commands to check if backend is working:

```bash
# Replace YOUR_URL with your actual Railway URL
YOUR_URL="https://your-app-production.up.railway.app"

# Test 1: Health check
curl $YOUR_URL/api/reviews/stats

# Test 2: API docs
open $YOUR_URL/docs

# Test 3: Fetch reviews
curl -X POST $YOUR_URL/api/reviews/fetch-play-store \
  -H "Content-Type: application/json" \
  -d '{"app_id":"com.whatsapp","weeks":4}'

# Test 4: Generate report
curl -X POST $YOUR_URL/api/analysis/generate-weekly-report

# Test 5: Check scheduler
curl $YOUR_URL/api/scheduler/status
```

---

## ✅ **Success Indicators**

Your backend is successfully deployed and working when:

1. ✅ **API Accessible:** Can reach `/api/reviews/stats`
2. ✅ **Docs Load:** Swagger UI opens at `/docs`
3. ✅ **Fetch Works:** Can fetch Play Store reviews
4. ✅ **AI Works:** Can generate reports (may fail if no data)
5. ✅ **Scheduler Runs:** Status shows `is_running: true`
6. ✅ **No Errors:** Railway logs show no critical errors

---

## 📞 **Next Steps After Backend Deployment**

Once backend is verified working:

1. **Note Your Railway URL** (you'll need it for frontend)
2. **Deploy Frontend to Vercel** (separate guide)
3. **Update CORS** with Vercel URL
4. **Test End-to-End** integration

---

## 🆘 **Getting Help**

If you encounter issues:

1. **Check Logs:**
   ```bash
   railway logs
   ```

2. **View Dashboard:**
   ```bash
   railway open
   ```

3. **Restart Service:**
   ```bash
   railway restart
   ```

4. **Re-deploy:**
   ```bash
   railway up --dockerfile Dockerfile
   ```

---

**Ready to deploy!** 🚀

**Estimated Time:** 10-15 minutes  
**Difficulty:** Easy  
**Status:** ✅ PRODUCTION READY
