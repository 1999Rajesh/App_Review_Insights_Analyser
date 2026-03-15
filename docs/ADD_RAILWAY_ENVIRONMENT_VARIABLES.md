# 🚨 CRITICAL: Add All Environment Variables to Railway

**Error:** Missing required environment variables  
**Problem:** Only `PORT=8080` is set, but app needs 15+ variables  
**Solution:** Add ALL variables listed below

---

## ⚡ **QUICK FIX: Copy & Paste These Variables**

### **Go to Railway Dashboard → Your Project → Variables Tab**

Add these variables **ONE BY ONE**:

---

### **1. AI Configuration (REQUIRED)**

```env
GEMINI_API_KEY=AIzaSyBhjdXxsrtD4ahUSShI1iPPr8WxYewU1wY
```

```env
GEMINI_MODEL=gemini-2.5-flash
```

---

### **2. Email Configuration (REQUIRED)**

⚠️ **Replace with YOUR actual email and app password!**

```env
SMTP_SERVER=smtp.gmail.com
```

```env
SMTP_PORT=465
```

```env
SENDER_EMAIL=your.email@gmail.com
```

```env
SENDER_PASSWORD=YOUR_GMAIL_APP_PASSWORD_HERE
```

```env
RECIPIENT_EMAIL=your.email@gmail.com
```

**📧 How to Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Login with your Google account
3. Select 'Mail' and your device
4. Click 'Generate'
5. Copy the password (NO SPACES!)
6. Paste it above in `SENDER_PASSWORD`

---

### **3. CORS Configuration (REQUIRED)**

```env
BACKEND_CORS_ORIGINS=http://localhost:3001,https://your-app.vercel.app
```

⚠️ **For now use:** `http://localhost:3001`  
After deploying Vercel, update with your Vercel URL

---

### **4. Application Settings (REQUIRED)**

```env
MAX_THEMES=5
```

```env
MAX_WORDS=250
```

```env
REVIEW_WEEKS_RANGE=8
```

```env
MAX_REVIEWS_TO_FETCH=500
```

---

### **5. Play Store Configuration (REQUIRED)**

```env
PLAY_STORE_DEFAULT_APP_ID=in.groww
```

```env
PLAY_STORE_COUNTRY=in
```

```env
PLAY_STORE_LANGUAGE=en
```

---

### **6. Railway Configuration (REQUIRED)**

```env
PORT=8000
```

⚠️ **Change from 8080 to 8000!**

---

### **7. Scheduler Configuration (REQUIRED)**

```env
SCHEDULER_INTERVAL_MINUTES=10080
```

This is 7 days (1 week). Options:
- `5` = Every 5 minutes (testing)
- `60` = Every hour
- `1440` = Every day
- `10080` = Every week (default)

---

## ✅ **Complete Checklist**

Copy this and check off as you add each variable:

```
□ GEMINI_API_KEY
□ GEMINI_MODEL
□ SMTP_SERVER
□ SMTP_PORT
□ SENDER_EMAIL
□ SENDER_PASSWORD
□ RECIPIENT_EMAIL
□ BACKEND_CORS_ORIGINS
□ MAX_THEMES
□ MAX_WORDS
□ REVIEW_WEEKS_RANGE
□ MAX_REVIEWS_TO_FETCH
□ PLAY_STORE_DEFAULT_APP_ID
□ PLAY_STORE_COUNTRY
□ PLAY_STORE_LANGUAGE
□ PORT (set to 8000)
□ SCHEDULER_INTERVAL_MINUTES
```

**Total: 17 variables**

---

## 🎯 **Step-by-Step Instructions**

### **1. Open Railway Dashboard**
```
https://railway.app/
```

### **2. Select Your Project**
Click on `App_Review_Insights_Analyser`

### **3. Go to Variables Tab**

### **4. Add Variables One by One**
Click "New Variable" or "+" button for each variable above

### **5. Set Each Variable:**
- Variable name (e.g., `GEMINI_API_KEY`)
- Value (e.g., `AIzaSyBhjdXxsrtD4ahUSShI1iPPr8WxYewU1wY`)
- Click "Save" or "Add"

### **6. After Adding All Variables:**
- Click "Deployments" tab
- Click "Restart" or "Redeploy"
- Wait 2-3 minutes for deployment

---

## 🔍 **Verify Deployment Success**

After redeploying, check:

### **Test 1: API Documentation**
```
https://your-railway-url.up.railway.app/docs
```
✅ Should open without errors

### **Test 2: Reviews Stats**
```
https://your-railway-url.up.railway.app/api/reviews/stats
```
✅ Should return JSON (not error)

### **Test 3: Check Logs**
In Railway → Logs tab
✅ Should see "Application startup complete"
❌ No more Pydantic validation errors

---

## 🐛 **Common Mistakes**

### **Mistake 1: Using PORT=8080**
❌ WRONG: `PORT=8080`  
✅ CORRECT: `PORT=8000`

### **Mistake 2: Missing Gmail App Password**
❌ WRONG: Using regular Gmail password  
✅ CORRECT: Use app password from https://myaccount.google.com/apppasswords

### **Mistake 3: Spaces in App Password**
❌ WRONG: `abcd 1234 efgh 5678` (with spaces)  
✅ CORRECT: `abcd1234efgh5678` (no spaces)

### **Mistake 4: Not Restarting After Adding Variables**
❌ WRONG: Add variables but don't restart  
✅ CORRECT: Always restart/redeploy after adding variables

### **Mistake 5: Only Adding Some Variables**
❌ WRONG: Adding just PORT or just API key  
✅ CORRECT: Must add ALL 17 variables

---

## 📋 **Variable Reference Table**

| Variable | Example Value | Required? | Notes |
|----------|--------------|-----------|-------|
| `GEMINI_API_KEY` | `AIzaSy...` | ✅ YES | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | ✅ YES | AI model name |
| `SMTP_SERVER` | `smtp.gmail.com` | ✅ YES | Gmail SMTP server |
| `SMTP_PORT` | `465` | ✅ YES | Gmail SMTP port |
| `SENDER_EMAIL` | `test@gmail.com` | ✅ YES | Your Gmail address |
| `SENDER_PASSWORD` | `xyz123...` | ✅ YES | **App password** (not regular password) |
| `RECIPIENT_EMAIL` | `test@gmail.com` | ✅ YES | Where to send reports |
| `BACKEND_CORS_ORIGINS` | `http://localhost:3001` | ✅ YES | Frontend URLs |
| `MAX_THEMES` | `5` | ✅ YES | Max themes in report |
| `MAX_WORDS` | `250` | ✅ YES | Max words per theme |
| `REVIEW_WEEKS_RANGE` | `8` | ✅ YES | Weeks of reviews |
| `MAX_REVIEWS_TO_FETCH` | `500` | ✅ YES | Max reviews from Play Store |
| `PLAY_STORE_DEFAULT_APP_ID` | `in.groww` | ✅ YES | Default app to analyze |
| `PLAY_STORE_COUNTRY` | `in` | ✅ YES | Country code |
| `PLAY_STORE_LANGUAGE` | `en` | ✅ YES | Language code |
| `PORT` | `8000` | ✅ YES | **Must be 8000** |
| `SCHEDULER_INTERVAL_MINUTES` | `10080` | ✅ YES | 7 days in minutes |

---

## 🎉 **Success Indicators**

You'll know it's working when:

✅ Deployment completes without errors  
✅ No Pydantic validation errors in logs  
✅ Can access `/docs` endpoint  
✅ Logs show "Application startup complete"  
✅ No "Field required" errors  

---

## 🆘 **Still Getting Errors?**

### **Check These:**

1. **All 17 variables added?** Count them!
2. **PORT set to 8000?** Not 8080
3. **Gmail app password used?** Not regular password
4. **No spaces in passwords?** Remove all spaces
5. **Restarted after adding variables?** Must redeploy

### **If Still Failing:**

1. **Check Railway Logs:**
   - Go to Deployments tab
   - Click latest deployment
   - View full logs
   
2. **Look for Specific Error:**
   - Which variable is missing?
   - Add that variable
   - Redeploy

3. **Verify Variable Names:**
   - Must match EXACTLY (case-sensitive)
   - `GEMINI_API_KEY` not `GeminiApiKey`
   - `PORT` not `Port`

---

## 📞 **Quick Support Commands**

### **Test After Adding Variables:**

```bash
# Test if app starts
curl https://your-railway-url.up.railway.app/api/reviews/stats

# Check settings loaded
curl https://your-railway-url.up.railway.app/api/reviews/settings

# View API docs
curl https://your-railway-url.up.railway.app/docs
```

---

## ✅ **What to Do Right Now**

### **Immediate Actions (Next 10 Minutes):**

1. **Open Railway Dashboard**
   ```
   https://railway.app/
   ```

2. **Go to Your Project → Variables Tab**

3. **Add ALL 17 Variables** (use checklist above)

4. **Especially Important:**
   - `GEMINI_API_KEY` ← Your API key
   - `SENDER_EMAIL` ← Your Gmail
   - `SENDER_PASSWORD` ← Gmail app password
   - `PORT=8000` ← NOT 8080!

5. **Restart Deployment**
   - Click "Restart" or "Redeploy"
   - Wait 2-3 minutes

6. **Test**
   - Open `/docs` endpoint
   - Should work without errors!

---

**Status:** ⏳ WAITING FOR VARIABLES  
**Action Required:** Add all 17 environment variables  
**Estimated Time:** 10 minutes
