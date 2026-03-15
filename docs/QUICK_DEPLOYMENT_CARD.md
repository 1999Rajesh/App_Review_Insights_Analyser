# 🚀 Quick Deployment Reference Card

**Frontend:** Vercel | **Backend:** Railway with Docker

---

## ⚡ Quick Deploy (5 Minutes)

### Backend to Railway
```bash
cd backend
railway login
railway link
railway up --dockerfile Dockerfile
```

### Frontend to Vercel
```bash
cd frontend
vercel login
vercel link
vercel --prod
```

---

## 🔑 Required Environment Variables

### Railway (Backend)
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=app_password_no_spaces
RECIPIENT_EMAIL=your.email@gmail.com
BACKEND_CORS_ORIGINS=https://your-app.vercel.app
PORT=8000
SCHEDULER_INTERVAL_MINUTES=10080
```

### Vercel (Frontend)
```env
VITE_API_BASE_URL=https://your-backend-production.up.railway.app/api
```

---

## 📋 Pre-Deployment Checklist

- [ ] Get Gmail App Password from https://myaccount.google.com/apppasswords
- [ ] Copy password WITHOUT SPACES
- [ ] Have Gemini API key ready
- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Install Vercel CLI: `npm install -g vercel`

---

## 🎯 Deployment Steps

### 1. Deploy Backend (Railway)
```bash
cd backend
railway login
railway link
railway variables set GEMINI_API_KEY=xxx SENDER_PASSWORD=xxx PORT=8000
railway up --dockerfile Dockerfile
```
✅ Get URL: `https://your-app-production.up.railway.app`

### 2. Update CORS
In Railway dashboard, update:
```
BACKEND_CORS_ORIGINS=https://your-app.vercel.app
```

### 3. Deploy Frontend (Vercel)
```bash
cd frontend
vercel login
vercel link
vercel env add VITE_API_BASE_URL https://your-railway-url.up.railway.app/api
vercel --prod
```
✅ Get URL: `https://your-app.vercel.app`

### 4. Test Everything
```bash
# Backend health
curl https://your-railway-url.up.railway.app/api/reviews/stats

# Frontend
open https://your-app.vercel.app
```

---

## 🔍 Testing Commands

### Backend Tests
```bash
# Health check
curl https://your-railway-url.up.railway.app/api/reviews/stats

# Fetch reviews
curl -X POST https://your-railway-url.up.railway.app/api/reviews/fetch-play-store \
  -H "Content-Type: application/json" \
  -d '{"app_id":"com.whatsapp","weeks":4}'

# Generate report
curl -X POST https://your-railway-url.up.railway.app/api/analysis/generate-weekly-report

# Send email
curl -X POST https://your-railway-url.up.railway.app/api/email/send-draft \
  -H "Content-Type: application/json" \
  -d '{"recipient_email":"test@example.com"}'
```

### Frontend Tests
```bash
# Open in browser
open https://your-app.vercel.app

# Check console for errors (F12)
# Test all UI features
```

---

## 🐛 Common Issues & Fixes

### CORS Error
**Error:** Access blocked by CORS policy  
**Fix:** Update `BACKEND_CORS_ORIGINS` in Railway with your Vercel URL

### Backend Not Starting
**Error:** Port not available  
**Fix:** Set `PORT=8000` in Railway environment variables

### Frontend Can't Connect
**Error:** Network requests failing  
**Fix:** Update `VITE_API_BASE_URL` in Vercel with correct Railway URL

### Gmail Authentication Failed
**Error:** SMTP authentication failed  
**Fix:** Use app password from https://myaccount.google.com/apppasswords (NO SPACES)

---

## 📊 URLs Reference

| Service | Pattern | Example |
|---------|---------|---------|
| Backend | `https://*.up.railway.app` | `https://app-production.up.railway.app` |
| Frontend | `https://*.vercel.app` | `https://app.vercel.app` |
| API Docs | `*/docs` | `https://app-production.up.railway.app/docs` |

---

## 🔄 Continuous Deployment

Both platforms auto-deploy on git push:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

✅ Railway will auto-deploy backend  
✅ Vercel will auto-deploy frontend

---

## 📞 CLI Quick Reference

### Railway CLI
```bash
railway login           # Login
railway link            # Link project
railway up              # Deploy
railway logs            # View logs
railway open            # Open dashboard
railway variables set   # Set env vars
```

### Vercel CLI
```bash
vercel login            # Login
vercel link             # Link project
vercel --prod           # Deploy to production
vercel ls               # List deployments
vercel env add          # Add env var
```

---

## ✅ Success Criteria

### Backend ✅
- [ ] Accessible at Railway URL
- [ ] `/api/reviews/stats` works
- [ ] `/docs` shows API docs
- [ ] Play Store fetch works
- [ ] Email sending works

### Frontend ✅
- [ ] Accessible at Vercel URL
- [ ] Page loads without errors
- [ ] Can fetch reviews
- [ ] Can generate reports
- [ ] No console errors

### Integration ✅
- [ ] Frontend ↔ Backend working
- [ ] CORS configured
- [ ] Real-time data flowing

---

## 📚 Full Documentation

- **Complete Guide:** `DEPLOYMENT_VERCEL_RAILWAY.md`
- **Docker Setup:** `backend/Dockerfile`
- **Vercel Config:** `frontend/vercel.json`
- **Environment:** `backend/.env.example`

---

**Deploy Time:** ~5 minutes  
**Status:** ✅ PRODUCTION READY  
**Last Updated:** March 15, 2026
