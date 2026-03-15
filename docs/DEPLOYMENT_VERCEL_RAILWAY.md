# 🚀 Complete Deployment Guide - Vercel + Railway

**Frontend:** Vercel (Vite/React)  
**Backend:** Railway with Docker  
**Date:** March 15, 2026

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Railway)](#backend-deployment-railway)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Post-Deployment Testing](#post-deployment-testing)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Prerequisites

### Required Accounts
- ✅ [GitHub](https://github.com) account
- ✅ [Railway](https://railway.app) account
- ✅ [Vercel](https://vercel.com) account

### Required CLI Tools

#### Install Node.js & npm
```bash
# Download from https://nodejs.org/
# Or use nvm (Node Version Manager)
```

#### Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Install Vercel CLI
```bash
npm install -g vercel
```

#### Verify Installations
```bash
node --version    # Should show v16+ 
npm --version     # Should show 8+
railway --version # Should show latest
vercel --version  # Should show latest
```

---

## 🛤️ Backend Deployment (Railway with Docker)

### Step 1: Prepare Backend for Railway

#### 1.1 Verify Dockerfile Exists
Check that `backend/Dockerfile` exists (created in previous step)

#### 1.2 Update Environment Variables in .env

**File:** `backend/.env`

```env
# ==========================================
# Production Configuration
# ==========================================

# Google Gemini API (Phase 3)
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

# Gmail SMTP (Get app password from https://myaccount.google.com/apppasswords)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=YOUR_16_CHAR_APP_PASSWORD_NO_SPACES
RECIPIENT_EMAIL=your.email@gmail.com

# CORS - IMPORTANT: Add your Vercel domain here
BACKEND_CORS_ORIGINS=https://your-app.vercel.app

# Application Settings
MAX_THEMES=5
MAX_WORDS=250
REVIEW_WEEKS_RANGE=8
MAX_REVIEWS_TO_FETCH=500

# Google Play Store Settings
PLAY_STORE_DEFAULT_APP_ID=in.groww
PLAY_STORE_COUNTRY=in
PLAY_STORE_LANGUAGE=en

# Railway Deployment
PORT=8000

# Scheduler (Weekly in production = 10080 minutes)
SCHEDULER_INTERVAL_MINUTES=10080
SCHEDULER_LOG_FILE=logs/scheduler.log
```

---

### Step 2: Deploy to Railway

#### Option A: Using Railway CLI (Recommended)

```bash
# Navigate to backend directory
cd backend

# Login to Railway
railway login

# Initialize new project
railway init

# Or link to existing project
railway link

# Set environment variables
railway variables set \
  GEMINI_API_KEY=your_gemini_api_key \
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

# Deploy with Docker
railway up --dockerfile Dockerfile

# View logs
railway logs

# Open dashboard
railway open
```

#### Option B: Using Railway Dashboard (Manual)

1. **Go to Railway Dashboard**
   ```
   https://railway.app/
   ```

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose repository: `App_Review_Insights_Analyser`

3. **Configure Service**
   - Click on your service
   - Go to "Settings" tab
   - Set **Root Directory**: `backend`

4. **Add Environment Variables**
   
   In Railway dashboard → "Variables" tab, add all variables from `.env` file above

5. **Enable Docker**
   - Railway automatically detects Dockerfile
   - No additional configuration needed

6. **Deploy**
   - Push to main branch to trigger deployment
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

---

### Step 3: Get Railway URL

After deployment completes:

1. **Find Your URL**
   - In Railway dashboard
   - Click "Settings" → "Domains"
   - You'll see: `https://your-app-production.up.railway.app`

2. **Test Backend Health**
   ```bash
   curl https://your-app-production.up.railway.app/api/reviews/stats
   ```

3. **Test API Documentation**
   ```
   https://your-app-production.up.railway.app/docs
   ```

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Vercel

#### 1.1 Update API Base URL

**File:** `frontend/src/services/api.ts`

Update the API base URL to use environment variable:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
```

Or hardcode your Railway URL:

```typescript
const API_BASE_URL = 'https://your-app-production.up.railway.app/api';
```

#### 1.2 Verify vercel.json Exists

Check that `frontend/vercel.json` exists with proper rewrites:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-production.up.railway.app/api/$1"
    }
  ],
  "env": {
    "VITE_API_BASE_URL": "https://your-backend-production.up.railway.app/api"
  }
}
```

**⚠️ IMPORTANT:** Replace `your-backend-production.up.railway.app` with your actual Railway URL!

---

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

```bash
# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Link to existing project or create new
vercel link

# Deploy to production
vercel --prod

# View deployment
vercel ls
```

#### Option B: Using Vercel Dashboard (Manual)

1. **Go to Vercel Dashboard**
   ```
   https://vercel.com/dashboard
   ```

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository: `App_Review_Insights_Analyser`

3. **Configure Project**

   **Framework Preset:** Vite
   
   **Build Command:** `npm run build`
   
   **Output Directory:** `dist`
   
   **Install Command:** `npm install`

4. **Set Environment Variables**
   
   In Vercel dashboard → Settings → Environment Variables:
   
   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://your-app-production.up.railway.app/api` |

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)

---

### Step 3: Get Vercel URL

After deployment completes:

1. **Find Your URL**
   - In Vercel dashboard
   - You'll see: `https://your-app.vercel.app`

2. **Test Frontend**
   - Open browser to your Vercel URL
   - Test all features

---

## 🔗 Connect Frontend and Backend

### Update CORS Settings

Once you have both URLs:

1. **Copy Vercel URL**
   ```
   https://your-app.vercel.app
   ```

2. **Update Railway Backend CORS**
   
   In Railway dashboard → Variables:
   ```
   BACKEND_CORS_ORIGINS=https://your-app.vercel.app
   ```

3. **Redeploy Backend**
   ```bash
   cd backend
   git add .
   git commit -m "Update CORS for Vercel frontend"
   git push origin main
   ```

---

## ✅ Post-Deployment Testing

### Test Checklist

#### 1. Backend Tests

```bash
# Test health check
curl https://your-backend-production.up.railway.app/api/reviews/stats

# Test Play Store fetch
curl -X POST https://your-backend-production.up.railway.app/api/reviews/fetch-play-store \
  -H "Content-Type: application/json" \
  -d '{"app_id":"com.whatsapp","weeks":4,"max_reviews":50}'

# Test report generation
curl -X POST https://your-backend-production.up.railway.app/api/analysis/generate-weekly-report

# Test email sending
curl -X POST https://your-backend-production.up.railway.app/api/email/send-draft \
  -H "Content-Type: application/json" \
  -d '{"recipient_email":"your.email@gmail.com"}'
```

#### 2. Frontend Tests

Visit: `https://your-app.vercel.app`

- ✅ Page loads successfully
- ✅ Can fetch Play Store reviews
- ✅ Can generate weekly report
- ✅ Can send email report
- ✅ All UI components working
- ✅ No console errors

#### 3. Integration Tests

- ✅ Frontend calls backend API successfully
- ✅ CORS headers working correctly
- ✅ Email delivery working
- ✅ Scheduler running (check Railway logs)

---

## 🐛 Troubleshooting

### Issue 1: CORS Errors

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' from origin 'https://your-app.vercel.app' has been blocked by CORS policy
```

**Solution:**
1. Update `BACKEND_CORS_ORIGINS` in Railway:
   ```
   BACKEND_CORS_ORIGINS=https://your-app.vercel.app
   ```
2. Redeploy backend

---

### Issue 2: API Calls Failing from Frontend

**Symptoms:**
- Backend works when tested directly
- Frontend shows network errors

**Solutions:**

**Option A:** Use absolute URLs in frontend

Update `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://your-backend-production.up.railway.app/api';
```

**Option B:** Configure Vercel rewrites

Ensure `frontend/vercel.json` has rewrites:
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-production.up.railway.app/api/$1"
    }
  ]
}
```

---

### Issue 3: Backend Not Starting

**Symptoms:**
```
Error: listen EADDRNOTAVAIL: address not available: 0.0.0.0:8000
```

**Solution:**
Ensure PORT environment variable is set in Railway:
```
PORT=8000
```

---

### Issue 4: Docker Build Fails

**Symptoms:**
```
ERROR: failed to solve: requirements.txt not found
```

**Solution:**
Verify Dockerfile path and requirements.txt location:
```
backend/
├── Dockerfile          ← Must exist
├── requirements.txt    ← Must exist
└── app/
    ├── main.py
    └── ...
```

---

### Issue 5: Frontend Build Fails on Vercel

**Symptoms:**
```
Error: Build failed with exit code 1
```

**Solution:**
1. Check Node version (should be 16+)
2. Verify `package.json` scripts
3. Check build logs in Vercel dashboard
4. Test build locally:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

---

## 📊 Monitoring

### Railway Monitoring

1. **View Logs**
   ```bash
   railway logs
   ```

2. **Dashboard**
   - Go to Railway dashboard
   - View metrics, logs, deployments

3. **Alerts**
   - Set up Slack/Discord notifications
   - Configure deployment alerts

### Vercel Monitoring

1. **View Analytics**
   - Vercel dashboard → Analytics
   - Track page views, performance

2. **View Deployments**
   - Vercel dashboard → Deployments
   - Check build status, logs

3. **Performance**
   - Vercel provides automatic performance monitoring
   - Core Web Vitals tracking

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ **Backend:**
- [ ] Accessible at Railway URL
- [ ] `/api/reviews/stats` returns data
- [ ] `/docs` shows API documentation
- [ ] Play Store fetch works
- [ ] AI analysis works (max 200 reviews)
- [ ] Email sending works
- [ ] Scheduler runs weekly

✅ **Frontend:**
- [ ] Accessible at Vercel URL
- [ ] Page loads without errors
- [ ] Can fetch Play Store reviews
- [ ] Can generate reports
- [ ] Can send emails
- [ ] All UI components functional
- [ ] No console errors

✅ **Integration:**
- [ ] Frontend ↔ Backend communication working
- [ ] CORS configured correctly
- [ ] Real-time data flowing
- [ ] End-to-end workflow functional

---

## 📞 Quick Reference

### Commands

#### Backend (Railway)
```bash
cd backend
railway login
railway link
railway up --dockerfile Dockerfile
railway logs
railway open
```

#### Frontend (Vercel)
```bash
cd frontend
vercel login
vercel link
vercel --prod
vercel ls
```

### Important URLs

| Service | URL Pattern | Example |
|---------|-------------|---------|
| Backend API | `https://*.up.railway.app` | `https://your-app-production.up.railway.app` |
| Frontend Web | `https://*.vercel.app` | `https://your-app.vercel.app` |
| Backend Docs | `*/docs` | `https://your-app-production.up.railway.app/docs` |

---

## 🔄 Continuous Deployment

Both Railway and Vercel support automatic deployments:

### Railway Auto-Deploy
- Push to main branch → Automatic deployment
- Configure in Railway dashboard

### Vercel Auto-Deploy
- Push to main branch → Automatic deployment
- Configure in Vercel dashboard

**Git Flow:**
```bash
# Make changes
git add .
git commit -m "Your changes"

# Push to deploy
git push origin main

# Both frontend and backend will auto-deploy!
```

---

## 📈 Performance Optimization

### Backend Optimizations

1. **Use 200 Review Limit** ✅ (Already implemented)
2. **Enable Caching** (Future: Add Redis)
3. **Database Migration** (Future: PostgreSQL)
4. **Background Jobs** (Future: Celery)

### Frontend Optimizations

1. **Lazy Loading** Components
2. **Code Splitting** Routes
3. **Image Optimization** (Vercel does this automatically)
4. **Edge Caching** (Vercel CDN)

---

## 🎯 Next Steps After Deployment

1. **Monitor First Week**
   - Check logs daily
   - Monitor error rates
   - Track user feedback

2. **Gather Feedback**
   - Share with stakeholders
   - Collect improvement suggestions
   - Iterate on features

3. **Scale as Needed**
   - Upgrade Railway plan if needed
   - Add database (PostgreSQL)
   - Add caching (Redis)
   - Implement CDN

4. **Maintain**
   - Regular dependency updates
   - Security patches
   - Performance monitoring
   - Backup strategy

---

**Ready for production deployment!** 🚀

**Last Updated:** March 15, 2026  
**Status:** ✅ PRODUCTION READY  
**Frontend:** Vercel (Vite/React)  
**Backend:** Railway with Docker  
**AI Model:** Gemini (Phase 3)  
**Max Reviews for Classification:** 200
