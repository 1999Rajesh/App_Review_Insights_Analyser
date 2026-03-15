# 🍎 App Review Insights Analyzer

**Automated weekly insights from app store reviews using AI**

[![Deployment Status](https://img.shields.io/badge/deployment-ready-success)](docs/DEPLOYMENT_VERCEL_RAILWAY.md)
[![Backend](https://img.shields.io/badge/backend-FastAPI-blue)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/frontend-React-purple)](https://react.dev/)
[![AI](https://img.shields.io/badge/AI-Gemini-green)](https://ai.google.dev/)

---

## 🚀 **Quick Start**

### **Try It Locally (5 minutes):**

```bash
# Install dependencies
npm install

# Start backend
cd backend
python -m uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

Open http://localhost:3001

📖 **Full Guide:** [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## ✨ **Features**

- 📊 **Auto-fetch Reviews** - Google Play Store integration
- 🤖 **AI Analysis** - Gemini-powered theme extraction
- 📧 **Weekly Emails** - Automated insights delivered to inbox
- 🎨 **Modern UI** - Beautiful glassmorphic design
- ⏰ **Scheduler** - Runs automatically every week
- 🔒 **PII Removal** - Privacy-focused data handling

---

## 📦 **Deployment**

### **Production Ready:**

```bash
# Deploy to Railway + Vercel
.\deploy.bat
```

📋 **Complete Guide:** [docs/DEPLOYMENT_VERCEL_RAILWAY.md](docs/DEPLOYMENT_VERCEL_RAILWAY.md)

---

## 🛠️ **Tech Stack**

**Backend:**
- FastAPI (Python 3.11)
- Gemini AI (Phase 3)
- APScheduler
- google-play-scraper

**Frontend:**
- React 18 + TypeScript
- Vite
- Modern CSS (Glassmorphism)

**Deployment:**
- Railway (Backend with Docker)
- Vercel (Frontend CDN)

---

## 📂 **Project Structure**

```
App_Review_Insights_Analyser/
├── docs/              ← All documentation
├── backend/           ← FastAPI backend
├── frontend/          ← React frontend
├── architecture/      ← Architecture docs
├── sample_data/       ← Sample CSV files
├── Dockerfile         ← Railway deployment
├── railway.toml       ← Railway config
└── deploy.bat         ← Deployment script
```

📚 **All Documentation:** [docs/README.md](docs/README.md)

---

## 🎯 **Key Features**

### **1. Auto-Fetch Reviews**
```python
# Fetch from Google Play Store
reviews = fetch_play_store_reviews(
    app_id="in.groww",
    weeks=8,
    max_reviews=200
)
```

### **2. AI Analysis**
```python
# Analyze with Gemini AI
themes = analyze_themes(
    reviews,
    max_themes=5,
    max_words=250
)
```

### **3. Weekly Email**
```python
# Send automated email
send_weekly_report(
    themes=themes,
    recipient="your@email.com"
)
```

---

## 🔧 **Configuration**

### **Environment Variables:**

Create `backend/.env`:

```env
# AI Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=your.email@gmail.com

# Application Settings
MAX_THEMES=5
MAX_WORDS=250
PORT=8000
```

📋 **Full Config:** [docs/ADD_RAILWAY_ENVIRONMENT_VARIABLES.md](docs/ADD_RAILWAY_ENVIRONMENT_VARIABLES.md)

---

## 🧪 **Testing**

### **Test Backend API:**

```bash
# Health check
curl http://localhost:8000/api/reviews/stats

# Generate report
curl -X POST http://localhost:8000/api/analysis/generate-weekly-report
```

📊 **Test Results:** [docs/BACKEND_TEST_RESULTS.md](docs/BACKEND_TEST_RESULTS.md)

---

## 📈 **Live Demo**

### **Production URLs:**

- **Backend:** https://your-app-production.up.railway.app
- **Frontend:** https://your-app.vercel.app
- **API Docs:** https://your-app-production.up.railway.app/docs

*(Replace with your actual URLs after deployment)*

---

## 🐛 **Troubleshooting**

### **Common Issues:**

| Issue | Solution |
|-------|----------|
| Railway build fails | Read [docs/RAILWAY_DOCKERFILE_FIX.md](docs/RAILWAY_DOCKERFILE_FIX.md) |
| Missing env variables | Read [docs/ADD_RAILWAY_ENVIRONMENT_VARIABLES.md](docs/ADD_RAILWAY_ENVIRONMENT_VARIABLES.md) |
| No reviews found | Check app ID and country code |
| Email not sending | Use Gmail app password |

🛠️ **More Help:** [docs/README.md](docs/README.md)

---

## 📝 **Documentation**

All documentation is in the `docs/` folder:

- 🚀 **Getting Started:** `docs/QUICKSTART.md`
- 📦 **Deployment:** `docs/DEPLOYMENT_VERCEL_RAILWAY.md`
- 🏗️ **Architecture:** `docs/ARCHITECTURE_OVERVIEW.md`
- 🎯 **Features:** See individual feature docs
- 🧪 **Testing:** `docs/BACKEND_TEST_RESULTS.md`

📚 **Full Index:** [docs/README.md](docs/README.md)

---

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test locally
5. Submit PR

---

## 📄 **License**

MIT License - See LICENSE file for details

---

## 🙏 **Acknowledgments**

- [Gemini AI](https://ai.google.dev/) - AI analysis
- [google-play-scraper](https://github.com/facundoolano/google-play-scraper) - Review scraping
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [React](https://react.dev/) - Frontend framework
- [Railway](https://railway.app/) - Backend hosting
- [Vercel](https://vercel.com/) - Frontend hosting

---

## 📞 **Support**

- 📚 **Documentation:** [docs/README.md](docs/README.md)
- 🐛 **Issues:** GitHub Issues
- 💬 **Questions:** GitHub Discussions

---

**Built with ❤️ using FastAPI + React**  
**Last Updated:** March 15, 2026
