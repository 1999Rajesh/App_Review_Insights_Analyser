# 🚨 Railway Crashed Error - FIX NOW!

**Status:** Deployment shows "Crashed"  
**Problem:** Application won't start or crashes immediately  
**Solution:** Follow steps below

---

## 🔍 **Step 1: Check Railway Logs**

### **Go to Railway Dashboard:**
```
https://railway.app/
```

1. **Select your project**
2. **Click on "Deployments" tab**
3. **Click latest deployment**
4. **View full logs**

### **Look for these errors:**

#### **Error A: Pydantic Validation Error**
```
pydantic_core._pydantic_core.ValidationError: 
Field required [type=missing, input_value={'PORT': '8080'}]
GEMINI_API_KEY - Field required
SENDER_EMAIL - Field required
```

✅ **FIX:** Add ALL environment variables (see Step 2)

---

#### **Error B: Port Not Available**
```
OSError: [Errno 98] Address already in use
or
Port 8080 not found
```

✅ **FIX:** Change PORT to 8000 (see Step 2)

---

#### **Error C: Module Not Found**
```
ModuleNotFoundError: No module named 'xxx'
```

✅ **FIX:** Check requirements.txt has all packages

---

#### **Error D: Import Error**
```
ImportError: cannot import name 'xxx' from 'app'
```

✅ **FIX:** Check file paths in Dockerfile

---

## ✅ **Step 2: Fix Environment Variables**

### **Most Common Issue: Missing Variables!**

Railway needs ALL these variables:

### **Add These in Railway → Variables Tab:**

```env
# 1. AI Configuration (REQUIRED!)
GEMINI_API_KEY=AIzaSyBhjdXxsrtD4ahUSShI1iPPr8WxYewU1wY
GEMINI_MODEL=gemini-2.5-flash

# 2. Email Configuration (REQUIRED!)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=YOUR_GMAIL_APP_PASSWORD_HERE
RECIPIENT_EMAIL=your.email@gmail.com

# 3. CORS (REQUIRED!)
BACKEND_CORS_ORIGINS=http://localhost:3001

# 4. App Settings (REQUIRED!)
MAX_THEMES=5
MAX_WORDS=250
REVIEW_WEEKS_RANGE=8
MAX_REVIEWS_TO_FETCH=500

# 5. Play Store (REQUIRED!)
PLAY_STORE_DEFAULT_APP_ID=in.groww
PLAY_STORE_COUNTRY=in
PLAY_STORE_LANGUAGE=en

# 6. Railway (CRITICAL!)
PORT=8000

# 7. Scheduler (REQUIRED!)
SCHEDULER_INTERVAL_MINUTES=10080
```

### **⚠️ CRITICAL CHECKLIST:**

- [ ] `PORT=8000` (NOT 8080!)
- [ ] `GEMINI_API_KEY` is set
- [ ] `SENDER_EMAIL` is YOUR email
- [ ] `SENDER_PASSWORD` is Gmail APP PASSWORD (not regular password)
- [ ] All 17 variables added
- [ ] No typos in variable names
- [ ] Restarted after adding variables

### **Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Login with Google account
3. Select 'Mail' and device
4. Click 'Generate'
5. Copy password **WITHOUT SPACES**
6. Paste in Railway

---

## 🔄 **Step 3: Restart Deployment**

After adding variables:

1. **In Railway Dashboard**
2. **Click "Deployments"**
3. **Click "Restart"** or **"Redeploy"**
4. **Wait 2-3 minutes**

---

## 🐛 **Step 4: Common Crash Causes & Fixes**

### **Cause 1: Incomplete Environment Variables**

**Symptom:** Pydantic validation error  
**Fix:** Add ALL 17 variables listed above

### **Cause 2: Wrong PORT**

**Symptom:** Port binding error  
**Fix:** Set `PORT=8000` (not 8080!)

### **Cause 3: Invalid API Key**

**Symptom:** Gemini API initialization error  
**Fix:** Verify GEMINI_API_KEY is correct

### **Cause 4: Gmail Password Issue**

**Symptom:** SMTP authentication error  
**Fix:** Use Gmail APP PASSWORD, not regular password

### **Cause 5: Docker Build Context**

**Symptom:** File not found errors  
**Fix:** Verify Dockerfile copies from `backend/`

### **Cause 6: Missing Dependencies**

**Symptom:** ModuleNotFoundError  
**Fix:** Check requirements.txt is complete

---

## 📊 **Step 5: Verify Deployment Health**

### **After Restart, Check:**

#### **Test 1: Can Access API Docs?**
```
https://your-railway-url.up.railway.app/docs
```

✅ **Success:** Swagger UI opens  
❌ **Still Crashed:** Check logs again

---

#### **Test 2: Stats Endpoint Works?**
```
https://your-railway-url.up.railway.app/api/reviews/stats
```

✅ **Success:** Returns JSON  
❌ **Error:** Check error message

---

#### **Test 3: Check Railway Logs**

Look for:
```
✅ INFO:     Application startup complete
✅ INFO:     Uvicorn running on http://0.0.0.0:8000
```

If you see:
```
❌ ERROR: Application failed to start
❌ CRITICAL: Shutting down
```
→ Check what error came before

---

## 🎯 **Step 6: Quick Diagnostic Commands**

### **In Railway Dashboard → Logs:**

Search for these keywords:

| Keyword | Meaning | Action |
|---------|---------|--------|
| `ValidationError` | Missing env vars | Add all variables |
| `Address already in use` | Port conflict | Set PORT=8000 |
| `ModuleNotFoundError` | Missing package | Update requirements.txt |
| `KeyError` | Code bug | Check analysis.py |
| `SMTP` error | Email config wrong | Fix Gmail settings |
| `Gemini` error | API key issue | Verify API key |

---

## ⚡ **Step 7: Emergency Recovery**

If still crashing after trying everything:

### **Option A: Complete Reset**

1. **Delete Railway project entirely**
2. **Wait 30 seconds**
3. **Create fresh project from GitHub**
4. **Add ALL environment variables immediately**
5. **Deploy**

### **Option B: Force Rebuild**

1. **In Railway → Settings**
2. **Click "Clear Build Cache"**
3. **Click "Redeploy"**

### **Option C: Manual Debug Mode**

1. **Temporarily add this to Railway Variables:**
   ```
   LOG_LEVEL=DEBUG
   ```

2. **Redeploy**

3. **Check detailed logs**

4. **Find exact crash point**

---

## 📋 **Step 8: Pre-Flight Checklist**

Before deploying, verify:

### **Environment Variables:**
- [ ] All 17 variables present
- [ ] PORT = 8000 (not 8080!)
- [ ] GEMINI_API_KEY is valid
- [ ] SENDER_EMAIL is real email
- [ ] SENDER_PASSWORD is app password (no spaces)
- [ ] Variable names match exactly (case-sensitive)

### **Docker Configuration:**
- [ ] Root Dockerfile exists
- [ ] railway.toml points to Dockerfile
- [ ] Dockerfile copies from `backend/`

### **Code Integrity:**
- [ ] backend/app/main.py exists
- [ ] backend/requirements.txt complete
- [ ] No syntax errors in code

### **Railway Settings:**
- [ ] Project linked to GitHub repo
- [ ] Auto-deploy enabled
- [ ] Region selected (asia-southeast1)

---

## 🎉 **Success Indicators**

You know it's working when:

✅ Deployment shows "Running" (not "Crashed")  
✅ Logs show "Application startup complete"  
✅ Can access /docs endpoint  
✅ No errors in logs  
✅ Uvicorn running on port 8000  

---

## 📞 **Quick Fix Summary**

### **Most Likely Issues (90% of crashes):**

1. **Missing Environment Variables** (60%)
   - Add ALL 17 variables
   - Especially GEMINI_API_KEY, SENDER_EMAIL, PORT

2. **Wrong PORT** (20%)
   - Set PORT=8000 (not 8080!)

3. **Invalid Gmail Password** (10%)
   - Use Gmail APP PASSWORD
   - No spaces in password

### **Less Common (10%):**
- Code errors
- Missing dependencies
- Docker build issues

---

## 🔧 **Step 9: After Fix - Test Everything**

Once deployed successfully:

### **Test 1: API Documentation**
```
https://your-railway-url.up.railway.app/docs
```

### **Test 2: Reviews Endpoint**
```
https://your-railway-url.up.railway.app/api/reviews/stats
```

### **Test 3: Settings Endpoint**
```
https://your-railway-url.up.railway.app/api/reviews/settings
```

### **Test 4: Scheduler Status**
```
https://your-railway-url.up.railway.app/api/scheduler/status
```

All should work without errors!

---

## 📊 **Log Analysis Examples**

### **Good Logs (What You Want to See):**
```
╭─────────────────╮
│ Railpack X.X.X  │
╰─────────────────╯

Building Docker image...
✓ FROM python:3.11-slim
✓ COPY backend/requirements.txt .
✓ RUN pip install
✓ COPY backend/app/ ./app/
✓ EXPOSE 8000

Starting application...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Bad Logs (Crash Indicators):**

#### **Pattern 1: Missing Variables**
```
pydantic_core.ValidationError: 4 validation errors
GEMINI_API_KEY - Field required
SENDER_EMAIL - Field required
```

#### **Pattern 2: Port Error**
```
OSError: [Errno 98] Address already in use
Port 8080 not available
```

#### **Pattern 3: Import Error**
```
ModuleNotFoundError: No module named 'fastapi'
```

---

## ⚠️ **Important Notes**

### **About PORT:**
- Railway automatically sets PORT environment variable
- Your app MUST use this variable
- Default should be 8000
- Don't hardcode 8080!

### **About Gmail Password:**
- Regular Gmail password WON'T work
- Must use APP PASSWORD from Google
- Get it at: https://myaccount.google.com/apppasswords
- Remove ALL spaces when copying

### **About Environment Variables:**
- ALL variables are REQUIRED
- App won't start with partial config
- Add all 17 before deploying
- Restart after adding variables

---

## 🎯 **What to Do RIGHT NOW**

### **Immediate Actions (Next 5 Minutes):**

1. **Open Railway Dashboard**
   ```
   https://railway.app/
   ```

2. **Go to Your Project → Deployments**

3. **Click Latest Deployment**

4. **Read Error Logs Carefully**
   - What's the first error?
   - Which file/line caused crash?

5. **Match Error to Solutions Above**

6. **Apply Fix**

7. **Restart Deployment**

8. **Test /docs Endpoint**

---

## 📈 **Monitoring After Fix**

Once running:

1. **Keep Dashboard Open**
   - Watch for 5 minutes
   - Ensure stays "Running"

2. **Test Endpoints Periodically**
   - Every few minutes
   - Verify still responding

3. **Check Logs Occasionally**
   - No new errors appearing
   - Requests being processed

---

**Status:** ⏳ NEEDS DIAGNOSIS  
**Action Required:** Check logs and apply fix  
**Estimated Time:** 5-15 minutes to fix
