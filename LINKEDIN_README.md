# 🚀 App Review Insights Analyzer - Complete Setup Guide

**Build Time:** 2 days  
**Tech Stack:** FastAPI + React + Groq AI  
**Status:** Production Ready ✅  
**Demo Ready:** Instant loading (2-3 seconds)  

---

## 📋 What This Does

Automated system that:
1. **Fetches** app reviews from Play Store/App Store
2. **Analyzes** themes using AI (Groq Llama 3.3 70B)
3. **Generates** weekly pulse reports automatically
4. **Emails** insights to stakeholders every Monday
5. **Displays** interactive dashboard with glassmorphic UI

**Perfect for:** Product managers, growth teams, and anyone who needs to understand user feedback at scale.

---

## ⚡ Quick Start (Re-run for New Week)

### **Prerequisites:**
- Python 3.9+ installed
- Node.js 16+ installed
- Groq API key (free from https://console.groq.com/keys)

### **Step 1: Clone & Install**

```bash
# Clone repository
git clone https://github.com/1999Rajesh/App_Review_Insights_Analyser.git
cd App_Review_Insights_Analyser

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### **Step 2: Configure Environment**

**Edit `backend/.env`:**

```env
# Groq API (Required - Get free key from groq.com)
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Gmail SMTP (For automated emails)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password  # From myaccount.google.com/apppasswords
RECIPIENT_EMAIL=manager@company.com

# App Settings
PLAY_STORE_DEFAULT_APP_ID=in.groww
MAX_THEMES=5
MAX_WORDS=250
```

### **Step 3: Run Locally**

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Expected output:
```
✅ Auto-imported 100 sample reviews from sample_data directory
INFO: Application startup complete.
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Expected output:
```
➜  Local:   http://localhost:3001/
```

### **Step 4: Test the System**

1. **Open browser:** http://localhost:3001
2. **Click:** "📥 Fetch Play Store Reviews" (takes 2-3 seconds)
3. **Click:** "✨ Generate Weekly Report" (takes 5-10 seconds)
4. **View:** Interactive dashboard with top themes, quotes, and insights!

**Success Criteria:**
- ✅ Reviews load instantly
- ✅ Report generates without errors
- ✅ Themes display with sentiment colors
- ✅ User quotes visible
- ✅ Action ideas suggested

---

## 🔄 How to Re-run for a New Week

### **Option A: Fresh Data from Play Store (Live)**

```bash
# Make sure backend is running
cd backend
python -m uvicorn app.main:app --reload --port 8000

# In frontend, click "Fetch Play Store Reviews"
# This will scrape latest reviews from Google Play Store
# Takes 30-60 seconds for live scraping
```

### **Option B: Use Sample Data (Fast Demo)**

```bash
# Already configured to auto-load on startup
# Just restart backend:
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Or use fast endpoint via frontend button
# Click "📥 Fetch Play Store Reviews" (demo mode)
# Loads in 2-3 seconds!
```

### **Option C: Upload Your Own CSV**

1. Prepare CSV with columns: `Star Rating`, `Title`, `Text`, `Date`
2. Open http://localhost:3001
3. Click "Upload CSV" tab
4. Drag & drop your file
5. Click "Generate Report"

---

## 🎨 Theme Legend (Color Coding)

The system uses intuitive color coding for theme sentiments:

| Color | Sentiment | Meaning | Emoji |
|-------|-----------|---------|-------|
| 🔴 **Red** | Negative | Critical issues needing immediate attention | 😠 |
| 🟡 **Yellow/Orange** | Mixed | Neutral or balanced feedback | 😐 |
| 🟢 **Green** | Positive | Strengths to maintain and celebrate | 😊 |

### **In the UI:**
- **Theme cards** show colored left border
- **Sentiment badge** displays emoji + text
- **Progress bars** use matching colors
- **Legend component** explains color scheme

---

## 📂 Sample Files Included

### **Reviews CSV:**
- `sample_data/play_store_reviews.csv` - 50 real reviews
- `sample_data/app_store_reviews.csv` - Alternative format
- Both formats supported for upload

### **Reports Generated:**
- `weekly_report_sample.md` - Full markdown report
- `email_draft_sample.txt` - Email template
- `backend/weekly_pulse_note_*.md` - Auto-generated notes

---

## 🛠️ Architecture Overview

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend   │────▶│  Groq AI API │
│ React + TS   │     │   FastAPI   │     │ Llama 3.3 70B│
│ http://:3001 │     │ http://:8000│     │ 10-100x faster│
└──────────────┘     └─────────────┘     └──────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │ Sample Data │
                     │ or Live Scraper│
                     └─────────────┘
```

### **Key Components:**

1. **Frontend (React):**
   - Glassmorphic UI design
   - Real-time status updates
   - Interactive theme exploration
   - Responsive layout

2. **Backend (FastAPI):**
   - RESTful API endpoints
   - CSV parsing & validation
   - Review deduplication
   - Report generation logic

3. **AI Analysis (Groq):**
   - Theme extraction
   - Sentiment classification
   - Quote selection
   - Action item suggestions

4. **Data Pipeline:**
   - Auto-import on startup
   - Fast demo mode (2-3 sec)
   - Live scraper option (30-60 sec)
   - PII removal optional

---

## 🚀 Deployment Options

### **Current Setup (Local):**
```bash
# Backend
python -m uvicorn app.main:app --reload --port 8000

# Frontend
npm run dev
```

### **Production Deployment:**

**Backend → Railway:**
```bash
cd backend
railway login
railway deploy
# Add GROQ_API_KEY in Railway dashboard
```

**Frontend → Vercel:**
```bash
cd frontend
vercel
# Set VITE_API_BASE_URL to Railway URL
```

**See docs/DEPLOYMENT_VERCEL_RAILWAY.md for detailed steps**

---

## 📊 Configuration Options

### **Environment Variables:**

| Variable | Purpose | Example |
|----------|---------|---------|
| `GROQ_API_KEY` | AI analysis engine | `gsk_...` |
| `GROQ_MODEL` | LLM model selection | `llama-3.3-70b-versatile` |
| `SMTP_*` | Automated email sending | `smtp.gmail.com` |
| `PLAY_STORE_DEFAULT_APP_ID` | Default app to scrape | `in.groww` |
| `MAX_THEMES` | Max themes in report | `5` |
| `MAX_WORDS` | Word limit for summary | `250` |
| `SCHEDULER_ENABLED` | Auto-run weekly task | `true/false` |

---

## 🧪 Testing & Validation

### **Quick Tests:**

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Fast Endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/reviews/fetch-play-store-fast
   ```

3. **Report Generation:**
   ```bash
   curl -X POST http://localhost:8000/api/analysis/generate-weekly-report
   ```

### **Expected Performance:**

- **Review Loading (Demo Mode):** 2-3 seconds
- **Report Generation:** 5-10 seconds
- **Total Demo Time:** <15 seconds
- **Live Scraping (if used):** 30-60 seconds

---

## 📈 Success Metrics

Track these to measure system effectiveness:

1. **Speed:**
   - Time to fetch reviews
   - Time to generate report
   - Total workflow duration

2. **Quality:**
   - Theme accuracy (manual review)
   - Sentiment correctness
   - Actionability of insights

3. **Reliability:**
   - Uptime percentage
   - Error rate
   - Successful email delivery

4. **User Adoption:**
   - Dashboard visits per week
   - Email open rate
   - Feature requests received

---

## 🐛 Troubleshooting

### **"Reviews not loading"**
- Check backend logs for errors
- Verify `sample_data/play_store_reviews.csv` exists
- Test health endpoint: `http://localhost:8000/health`

### **"Groq API quota exceeded"**
- Verify API key in `.env` is correct
- Check usage at https://console.groq.com/usage
- Upgrade plan if needed

### **"Frontend shows Not Found"**
- Ensure backend is running on port 8000
- Check `frontend/.env` has correct API URL
- Restart frontend after backend changes

### **"Report generation hangs"**
- Reduce `MAX_THEMES` to 3 temporarily
- Check Groq API status
- Verify network connectivity

---

## 📞 Support & Resources

### **Documentation:**
- `QUICK_DEMO_GUIDE.md` - Presentation script
- `GROQ_API_SETUP.md` - AI configuration
- `FAST_DEMO_MODE.md` - Speed optimization guide
- `docs/ARCHITECTURE_INDEX.md` - Technical deep dive

### **GitHub Issues:**
Report bugs or request features at:
https://github.com/1999Rajesh/App_Review_Insights_Analyser/issues

### **LinkedIn:**
Follow my #LearnInPublic journey:
https://linkedin.com/in/yourprofile

---

## 🎯 Next Steps After Setup

1. ✅ **Run local demo** - Verify everything works
2. ✅ **Customize settings** - Update app ID, themes, word limits
3. ✅ **Add your data** - Upload CSV or configure live scraping
4. ✅ **Deploy to cloud** - Railway + Vercel for production
5. ✅ **Enable automation** - Turn on scheduler for weekly emails
6. ✅ **Share with team** - Show stakeholders the dashboard

---

## 💡 Pro Tips

### **For Demos:**
- Use fast demo mode (instant loading)
- Have sample report pre-generated
- Keep browser console open to show API calls
- Explain architecture while waiting for results

### **For Production:**
- Enable scheduler for automatic weekly runs
- Monitor Groq API usage monthly
- Customize email templates for your brand
- Set up alerts for failed jobs

### **For Scaling:**
- Increase `MAX_REVIEWS_TO_FETCH` gradually
- Consider paid Groq tier for higher limits
- Add database persistence (currently in-memory)
- Implement caching for repeated analyses

---

## 🏆 What You'll Learn

By studying this project, you'll understand:

✅ **Full-stack development** - React + FastAPI integration  
✅ **AI/LLM integration** - Groq API, prompt engineering  
✅ **Data pipelines** - CSV parsing, ETL workflows  
✅ **Automation** - Scheduled tasks, email delivery  
✅ **Deployment** - Railway, Vercel, environment management  
✅ **Error handling** - Quota limits, API failures, retries  
✅ **UI/UX design** - Glassmorphism, responsive layouts  

---

**Built with ❤️ by Rajesh**  
**#LearnInPublic Series - Project 3/4**  
**March 2026**

*Feel free to fork, modify, and use for your own projects!*
