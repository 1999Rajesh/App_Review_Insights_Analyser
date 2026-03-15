# ⚡ Quick Vercel Deployment Card

**Goal:** Deploy frontend to Vercel and connect to Railway backend  
**Time:** 10 minutes

---

## 🎯 **Essential Steps**

### **1. Get Your Railway URL**
```
https://your-app-production.up.railway.app
```
📋 **Copy this!** You'll need it.

---

### **2. Go to Vercel**
```
https://vercel.com/
```
- Login with GitHub
- Click "Add New..." → "Project"

---

### **3. Import Repository**
- Select: `App_Review_Insights_Analyser`
- Click "Import"

---

### **4. Configure Build**

| Setting | Value |
|---------|-------|
| Framework Preset | **Vite** |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | `npm install` |

---

### **5. Add Environment Variable** ⭐

Click "Environment Variables" → "Add New":

```env
Key: VITE_API_BASE_URL
Value: https://YOUR-RAILWAY-URL.up.railway.app/api
```

⚠️ **Replace YOUR-RAILWAY-URL with actual Railway URL!**

---

### **6. Deploy**
- Click **"Deploy"** button
- Wait 2-3 minutes
- Get your Vercel URL

Example:
```
https://app-review-insights-analyser.vercel.app
```

---

### **7. Update Railway CORS** 🔑

In Railway Dashboard → Variables:

Find `BACKEND_CORS_ORIGINS` and update:

```env
BACKEND_CORS_ORIGINS=http://localhost:3001,https://YOUR-VERCEL-URL.vercel.app
```

⚠️ **Replace YOUR-VERCEL-URL with actual Vercel URL!**

**Restart Railway deployment.**

---

### **8. Test Integration**

Open Vercel URL in browser:
```
https://your-app.vercel.app
```

✅ Should see beautiful UI

Try these features:
1. Fetch Play Store Reviews
2. Generate Weekly Report
3. Check no console errors (F12)

---

## ✅ **Quick Checklist**

Print and check off:

```
□ Got Railway URL
□ Logged into Vercel with GitHub
□ Imported App_Review_Insights_Analyser
□ Set Framework to Vite
□ Added VITE_API_BASE_URL environment variable
□ Deployed successfully
□ Got Vercel URL
□ Updated Railway CORS with Vercel URL
□ Restarted Railway
□ Tested Vercel frontend
□ All features working
```

---

## 🐛 **If Something Fails**

### **CORS Error:**
```
Access to fetch blocked by CORS policy
```

**Fix:**
1. Railway → Update `BACKEND_CORS_ORIGINS`
2. Add your Vercel URL
3. Restart Railway

---

### **Network Error:**
```
TypeError: Failed to fetch
```

**Check:**
1. Railway URL correct in VITE_API_BASE_URL?
2. Railway backend running?
3. Test: `https://your-railway-url.up.railway.app/docs`

---

### **Blank Page:**
- Check browser console (F12)
- Look for errors
- Verify VITE_API_BASE_URL is set correctly

---

## 🎯 **What Goes Where**

### **In Vercel:**
```
VITE_API_BASE_URL = https://railway-url.up.railway.app/api
```

### **In Railway:**
```
BACKEND_CORS_ORIGINS = http://localhost:3001,https://vercel-url.vercel.app
```

---

## 📊 **Expected Result**

After deployment:

```
✅ Vercel shows "Ready"
✅ Can open: https://your-app.vercel.app
✅ Beautiful glassmorphic UI loads
✅ Can fetch reviews
✅ Can generate reports
✅ No console errors
✅ Network calls to Railway API
```

---

## 🔄 **Auto-Deploy**

After initial setup:

**Every push to GitHub:**
- Vercel auto-deploys
- Same URL
- No manual action needed

**When you change code:**
```bash
git add .
git commit -m "Changes"
git push
```
→ Vercel rebuilds automatically!

---

## 📞 **Quick Reference**

### **Your URLs:**

| Service | URL Pattern |
|---------|-------------|
| Railway Backend | `https://xxx-production.up.railway.app` |
| Vercel Frontend | `https://xxx.vercel.app` |
| API Docs | `https://railway-url.up.railway.app/docs` |

---

## ⚡ **Speed Run**

**Fastest path (for experienced users):**

1. Vercel → Import repo
2. Add env var: `VITE_API_BASE_URL=railway-url/api`
3. Deploy
4. Update Railway CORS
5. Test

**Time:** ~5 minutes

---

**Status:** ✅ READY TO DEPLOY  
**Estimated Time:** 10 minutes  
**Difficulty:** Easy
