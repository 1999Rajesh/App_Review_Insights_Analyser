# 🔧 Fix Frontend "Failed to Fetch Reviews" Error

## Problem
Frontend shows: **"Failed to fetch reviews from Play Store"**

## Cause
The frontend API URL is pointing to Railway's **internal DNS** which doesn't work from browsers.

---

## ✅ Quick Fix (2 Steps)

### Step 1: Get Your Public Railway URL

1. Go to https://railway.app
2. Click your project
3. Click **"Settings"** tab
4. Scroll to **"Domains"** section
5. Copy the **Public Domain** URL

It looks like:
```
https://your-app-production.up.railway.app
```

or

```
https://abc123-xyz-production.up.railway.app
```

---

### Step 2: Update Frontend API URL

Open this file:
```
frontend/src/services/api.ts
```

Find line 4:
```typescript
const API_BASE_URL = 'https://your-app-production.up.railway.app/api';
```

Replace `your-app-production.up.railway.app` with YOUR actual Railway URL.

Example:
```typescript
// If your Railway URL is: https://myapp-production.up.railway.app
const API_BASE_URL = 'https://myapp-production.up.railway.app/api';
```

---

## 🚀 Deploy Frontend Update

After updating the URL:

### Option A: Deploy to Vercel (Recommended)

```bash
cd frontend
git add .
git commit -m "fix: Update Railway API URL to public domain"
git push origin main
```

Vercel will auto-deploy. Wait 1-2 minutes, then refresh your frontend.

### Option B: Test Locally First

```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

Test the "Fetch Play Store Reviews" button.

---

## 🧪 Verify It Works

After deploying:

1. Open your frontend (Vercel URL or localhost)
2. Click **"Fetch Play Store Reviews"** button
3. Should see:
   ```
   ✅ Successfully fetched 280 reviews from Play Store
   ```

Instead of the error.

---

## 🛠️ Still Not Working?

### Check CORS Issues

If you still get errors, verify CORS is configured in backend:

In Railway dashboard → Logs, look for:
```
CORS request allowed from: https://your-vercel-app.vercel.app
```

If you see CORS errors, we need to add your frontend URL to backend CORS settings.

### Check Railway Service Status

Make sure backend is running:
1. Railway dashboard → Your service
2. Should show **green dot** (running)
3. Logs should show no errors

### Test Backend Directly

Open browser and visit:
```
https://YOUR-RAILWAY-URL.up.railway.app/health
```

Should return JSON:
```json
{
  "status": "healthy",
  "scheduler_running": true,
  ...
}
```

If this doesn't work, backend isn't deployed correctly.

---

## 📋 Common Mistakes

### ❌ Mistake 1: Wrong Protocol
```typescript
// WRONG (http instead of https)
const API_BASE_URL = 'http://myapp-production.up.railway.app/api';

// CORRECT
const API_BASE_URL = 'https://myapp-production.up.railway.app/api';
```

### ❌ Mistake 2: Missing /api Path
```typescript
// WRONG (missing /api)
const API_BASE_URL = 'https://myapp-production.up.railway.app';

// CORRECT
const API_BASE_URL = 'https://myapp-production.up.railway.app/api';
```

### ❌ Mistake 3: Using Internal DNS
```typescript
// WRONG (internal DNS only works inside Railway network)
const API_BASE_URL = 'http://app-review-insights-analyser.railway.internal/api';

// CORRECT (public URL)
const API_BASE_URL = 'https://myapp-production.up.railway.app/api';
```

---

## 💡 How to Find Your Railway URL

If you can't find it in Railway dashboard, use CLI:

```bash
railway domain
```

Output:
```
https://myapp-production.up.railway.app
```

Or check Railway dashboard:
1. Click your project
2. Click **"Settings"**
3. Scroll to **"Domains"**
4. You'll see: `myapp-production.up.railway.app`

Add `https://` prefix when using in code.

---

## ✅ Success Checklist

After fixing:

- [ ] Updated `api.ts` with correct Railway URL
- [ ] Pushed changes to GitHub
- [ ] Vercel deployed successfully
- [ ] Opened frontend (Vercel or localhost)
- [ ] Clicked "Fetch Play Store Reviews"
- [ ] Saw success message (not error)
- [ ] Reviews displayed in table

---

## 🎯 What Changed

**Before:**
```typescript
const API_BASE_URL = 'http://app-review-insights-analyser.railway.internal/api';
```

**After:**
```typescript
const API_BASE_URL = 'https://YOUR-ACTUAL-RAILWAY-URL.up.railway.app/api';
```

This changes from internal Railway DNS (only works within Railway network) to public URL (works from any browser).

---

## 📞 Need Help?

If still not working, share:

1. Your Railway URL (from Settings → Domains)
2. Screenshot of frontend error
3. Browser console errors (F12 → Console tab)
4. Railway logs (if any errors)

Then I can give specific troubleshooting steps!

---

**Next step:** Get your Railway URL and update `frontend/src/services/api.ts` now! 🚀
