# 🚀 Railway Deployment Guide

**App Review Insights Analyzer - Production Deployment**

---

## 📋 Executive Summary

### AI Model Phases
- **Phase 2:** Groq (DEPRECATED)
- **Phase 3:** Gemini (CURRENT) ✅
- **Future:** Claude or OpenAI (Optional)

### Key Configuration Points
1. ✅ Use `google-play-scraper` for downloading reviews automatically
2. ✅ Maximum **200 reviews** for AI classification
3. ✅ Gmail integration with App Password
4. ✅ Railway deployment with PORT=8000

---

## 🎯 Pre-Deployment Checklist

### 1. Get Gmail App Password

**CRITICAL:** You need a Gmail App Password to send emails. Follow these steps:

#### Step-by-Step Instructions:

1. **Go to Google Account Settings**
   ```
   https://myaccount.google.com/apppasswords
   ```

2. **Enable 2-Factor Authentication (if not already enabled)**
   - Go to Security → 2-Step Verification
   - Set it up with your phone

3. **Create App Password**
   - Click on "App passwords"
   - Under "Select app", choose "Mail"
   - Under "Select device", choose your device (e.g., "Windows Computer")
   - Click "Generate"

4. **Copy Password**
   - Google will show a 16-character password
   - **IMPORTANT:** Copy it WITHOUT SPACES
   - Example: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

5. **Save in .env file**
   ```env
   SENDER_PASSWORD=abcdefghijklmnop  # No spaces!
   ```

---

### 2. Configure Environment Variables

Create or update `backend/.env` file:

```env
# ==========================================
# Executive Summary: AI Model Phases
# ==========================================
# Phase 2 = Groq (DEPRECATED)
# Phase 3 = Gemini (CURRENT) ✅
# Future: Claude or OpenAI (Optional)

# ==========================================
# Google Gemini API Configuration (Phase 3)
# ==========================================
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# ==========================================
# SMTP Email Configuration (Gmail)
# ==========================================
# Get App Password from: https://myaccount.google.com/apppasswords
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=YOUR_16_CHAR_APP_PASSWORD_NO_SPACES
RECIPIENT_EMAIL=your.email@gmail.com

# ==========================================
# Application Settings
# ==========================================
BACKEND_CORS_ORIGINS=https://your-domain.com
MAX_THEMES=5
MAX_WORDS=250
REVIEW_WEEKS_RANGE=8
MAX_REVIEWS_TO_FETCH=500

# ==========================================
# Google Play Store Settings - Groww App
# ==========================================
PLAY_STORE_DEFAULT_APP_ID=in.groww
PLAY_STORE_COUNTRY=in
PLAY_STORE_LANGUAGE=en

# ==========================================
# Railway Deployment Configuration
# ==========================================
PORT=8000

# ==========================================
# Scheduler Settings (Production)
# ==========================================
# Change to weekly in production (10080 minutes = 7 days)
SCHEDULER_INTERVAL_MINUTES=10080
SCHEDULER_LOG_FILE=logs/scheduler.log
```

---

## 🛤️ Railway Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure all files are committed:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Verify requirements.txt includes:**
   ```txt
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   google-generativeai==0.3.2
   google-play-scraper==1.2.4
   python-dotenv==1.0.0
   pydantic==2.5.3
   pydantic-settings==2.1.0
   aiofiles==23.2.1
   apscheduler==3.10.4
   pytz==2023.3
   requests==2.31.0
   ```

---

### Step 2: Deploy to Railway

1. **Go to Railway**
   ```
   https://railway.app/
   ```

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `App_Review_Insights_Analyser`

3. **Configure Service**
   - Click on your service
   - Go to "Settings" tab
   - Set Root Directory: `backend`

4. **Add Environment Variables**
   
   In Railway dashboard, go to "Variables" tab and add:

   | Variable Name | Value |
   |---------------|-------|
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `GEMINI_MODEL` | `gemini-2.5-flash` |
   | `SMTP_SERVER` | `smtp.gmail.com` |
   | `SMTP_PORT` | `465` |
   | `SENDER_EMAIL` | Your Gmail address |
   | `SENDER_PASSWORD` | Your 16-char app password (NO SPACES) |
   | `RECIPIENT_EMAIL` | Recipient email |
   | `BACKEND_CORS_ORIGINS` | `https://your-domain.com` |
   | `MAX_THEMES` | `5` |
   | `MAX_WORDS` | `250` |
   | `REVIEW_WEEKS_RANGE` | `8` |
   | `MAX_REVIEWS_TO_FETCH` | `500` |
   | `PLAY_STORE_DEFAULT_APP_ID` | `in.groww` |
   | `PLAY_STORE_COUNTRY` | `in` |
   | `PLAY_STORE_LANGUAGE` | `en` |
   | `PORT` | `8000` ⚠️ **CRITICAL** |
   | `SCHEDULER_INTERVAL_MINUTES` | `10080` (weekly) |

---

### Step 3: Verify Deployment

1. **Check Build Logs**
   - Watch the build process in Railway dashboard
   - Ensure no errors in build logs

2. **Get Your Railway URL**
   - Railway will provide a URL like:
   ```
   https://your-app-production.up.railway.app
   ```

3. **Test Health Check**
   ```bash
   curl https://your-app-production.up.railway.app/api/reviews/stats
   ```

4. **Test API Documentation**
   ```
   https://your-app-production.up.railway.app/docs
   ```

---

## 🔧 Post-Deployment Configuration

### Update Frontend API Base URL

In your frontend code, update the API base URL:

**File:** `frontend/src/services/api.ts`

```typescript
const API_BASE_URL = 'https://your-app-production.up.railway.app/api';
```

Or use environment variable:

**File:** `frontend/.env`
```env
VITE_API_BASE_URL=https://your-app-production.up.railway.app/api
```

---

### Test Play Store Auto-Fetch

Test that `google-play-scraper` is working in production:

```bash
curl -X POST https://your-app-production.up.railway.app/api/reviews/fetch-play-store \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "in.groww",
    "weeks": 8,
    "max_reviews": 500,
    "country": "us",
    "language": "en"
  }'
```

Expected response:
```json
{
  "message": "Successfully fetched X reviews from Google Play Store",
  "fetched_count": X,
  "total_in_database": Y
}
```

---

### Test Weekly Report Generation

Test that AI analysis with max 200 reviews is working:

```bash
curl -X POST https://your-app-production.up.railway.app/api/analysis/generate-weekly-report
```

Expected behavior:
- Uses maximum 200 reviews for classification
- Generates report with Gemini (Phase 3)
- Returns top themes with quotes and action ideas

---

### Test Email Delivery

Test Gmail integration:

```bash
curl -X POST https://your-app-production.up.railway.app/api/email/send-draft \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "your.email@gmail.com"
  }'
```

Check your inbox for the weekly pulse report!

---

## 📊 Monitoring & Maintenance

### View Scheduler Logs

In Railway dashboard:
1. Go to your service
2. Click "Deployments"
3. Click on latest deployment
4. View logs in real-time

Look for:
```
🤖 WEEKLY PULSE SCHEDULER STARTED
✅ Scheduler Status: RUNNING
📧 Recipient: your.email@gmail.com
⏰ Schedule: Every 10080 minutes (weekly)
```

### Set Up Alerts

1. **Railway Notifications:**
   - Go to Project Settings → Notifications
   - Connect Slack or Discord
   - Enable deployment alerts

2. **Email Monitoring:**
   - Check scheduler logs regularly
   - Monitor email delivery success rate

---

## 🐛 Troubleshooting

### Issue 1: Port Not Listening

**Error:**
```
Error: listen EADDRNOTAVAIL: address not available: 0.0.0.0:8000
```

**Solution:**
Ensure PORT environment variable is set in Railway:
```
PORT=8000
```

---

### Issue 2: Gmail App Password Fails

**Error:**
```
SMTP Authentication failed
```

**Solutions:**
1. Verify you copied password WITHOUT SPACES
2. Ensure 2FA is enabled on Gmail account
3. Regenerate app password if needed
4. Check SENDER_EMAIL matches the Gmail account

---

### Issue 3: google-play-scraper Not Working

**Error:**
```
ModuleNotFoundError: No module named 'google_play_scraper'
```

**Solution:**
Ensure `requirements.txt` includes:
```txt
google-play-scraper==1.2.4
```

Then redeploy:
```bash
git add backend/requirements.txt
git commit -m "Add google-play-scraper dependency"
git push origin main
```

---

### Issue 4: AI Analysis Timeout

**Error:**
```
Request timeout after 60 seconds
```

**Solution:**
The system now uses maximum 200 reviews for classification (as per hint). This should reduce processing time to ~15-20 seconds.

If still timing out:
1. Reduce `MAX_REVIEWS_TO_FETCH` to 300
2. Reduce `REVIEW_WEEKS_RANGE` to 4
3. Consider upgrading Gemini API quota

---

## 📈 Performance Optimization

### Current Configuration (Optimized)

| Setting | Value | Reason |
|---------|-------|--------|
| Max Reviews for Classification | 200 | As per hint - optimal for speed |
| Max Reviews to Fetch | 500 | Can fetch more, classify fewer |
| Review Weeks Range | 8 | Good balance of recency |
| Max Themes | 5 | Comprehensive but concise |
| Scheduler Interval | 10080 min (7 days) | Weekly in production |

### Scaling Recommendations

**For Higher Volumes:**

1. **Database Migration:**
   - Move from in-memory to PostgreSQL
   - Railway provides free PostgreSQL addon

2. **Caching:**
   - Add Redis for caching AI results
   - Railway Redis addon available

3. **Background Jobs:**
   - Use Celery for async processing
   - Railway supports worker services

---

## 🎉 Deployment Success Criteria

Your deployment is successful when:

- ✅ Backend accessible at Railway URL
- ✅ `/api/reviews/stats` returns data
- ✅ `/docs` shows interactive API documentation
- ✅ Play Store auto-fetch works with `google-play-scraper`
- ✅ AI analysis uses maximum 200 reviews
- ✅ Weekly reports generated with Gemini (Phase 3)
- ✅ Emails delivered successfully via Gmail
- ✅ Scheduler runs weekly (every 10080 minutes)
- ✅ PORT=8000 configured correctly

---

## 📞 Support Resources

### Documentation Files
- `BACKEND_TEST_RESULTS.md` - API test results
- `DATA_MODELS_DOCUMENTATION.md` - Data structures
- `GROWW_WEEKLY_PULSE_SETUP.md` - Groww app setup
- `WEEKLY_EMAIL_AUTOMATION_GROWW.md` - Email automation

### External Links
- **Railway Docs:** https://docs.railway.app/
- **Gemini API Docs:** https://ai.google.dev/docs
- **Gmail App Password:** https://support.google.com/accounts/answer/185833
- **google-play-scraper:** https://github.com/facundoolano/google-play-scraper

---

## 🎯 Quick Reference Commands

### Local Testing Before Deployment
```bash
# Test with 200 review limit
cd backend
python test_simple_backend.py

# Check environment variables
python -c "from app.config import settings; print(settings.model_dump())"

# Run locally with production settings
uvicorn app.main:app --reload --port 8000
```

### Railway CLI (Optional)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# View logs
railway logs

# Open dashboard
railway open
```

---

**Ready for production deployment!** 🚀

**Last Updated:** March 15, 2026  
**Status:** ✅ PRODUCTION READY  
**AI Model:** Gemini (Phase 3)  
**Max Reviews for Classification:** 200  
**Email:** Gmail with App Password  
**Deployment Platform:** Railway (PORT=8000)
