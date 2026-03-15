# 📂 Project Structure - Clean Layout

**Last Updated:** March 15, 2026  
**Status:** ✅ Organized

---

## 🌳 **Root Directory Structure**

```
App_Review_Insights_Analyser/
│
├── 📁 docs/                      # All documentation (40+ files)
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT_VERCEL_RAILWAY.md
│   ├── ARCHITECTURE_OVERVIEW.md
│   ├── README.md                 # Documentation index
│   └── ... (all other .md files)
│
├── 📁 backend/                   # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Configuration
│   │   ├── models/
│   │   │   └── review.py        # Data models
│   │   ├── routes/
│   │   │   ├── reviews.py       # Review endpoints
│   │   │   ├── analysis.py      # AI analysis
│   │   │   ├── email.py         # Email endpoints
│   │   │   ├── reports.py       # Report endpoints
│   │   │   └── scheduler.py     # Scheduler endpoints
│   │   ├── services/
│   │   │   ├── gemini_analyzer.py    # AI analysis
│   │   │   ├── google_play_scraper.py # Review fetching
│   │   │   ├── review_importer.py    # CSV import
│   │   │   ├── email_sender.py       # Email service
│   │   │   └── weekly_pulse_scheduler.py # Scheduler
│   │   └── utils/
│   │       ├── pii_remover.py   # Privacy protection
│   │       └── quote_selector.py # Quote selection
│   ├── Dockerfile               # Backend Docker config
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   └── test_*.py                # Test scripts
│
├── 📁 frontend/                  # React Frontend
│   ├── src/
│   │   ├── App.tsx              # Main component
│   │   ├── main.tsx             # Entry point
│   │   ├── components/
│   │   │   ├── ReviewUploader.tsx
│   │   │   ├── WeeklyReport.tsx
│   │   │   ├── ThemeLegend.tsx
│   │   │   ├── SettingsPanel.tsx
│   │   │   └── PlayStoreFetcher.tsx
│   │   ├── services/
│   │   │   └── api.ts           # API integration
│   │   ├── App.css              # Styles
│   │   └── index.css            # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── vercel.json              # Vercel deployment config
│
├── 📁 architecture/              # Architecture documentation
│   ├── PHASE_01_Foundation_Setup.md
│   ├── PHASE_02_Data_Import_PII.md
│   ├── PHASE_03_API_Layer.md
│   ├── PHASE_04_AI_Analysis.md
│   ├── PHASE_05_Email_Automation.md
│   ├── PHASE_06_Frontend_Development.md
│   ├── PHASE_07_Testing_Validation.md
│   ├── PHASE_08_Automated_Scheduler.md
│   └── README_PHASES.md
│
├── 📁 sample_data/               # Sample CSV files
│   ├── app_store_reviews.csv
│   └── play_store_reviews.csv
│
├── 📁 .qoder/                    # IDE configuration
│   ├── agents/
│   └── skills/
│
├── 🔧 deploy.bat                 # Full deployment automation
├── 🔧 setup.bat                  # Setup automation
├── 🔧 start.bat                  # Local startup script
│
├── 🐳 Dockerfile                 # Root Dockerfile for Railway
├── ⚙️ railway.toml               # Railway configuration
├── 📄 .dockerignore              # Docker ignore rules
├── 📄 .gitignore                 # Git ignore rules
└── 📖 README.md                  # Main readme
```

---

## 📊 **File Count Summary**

| Category | Count | Location |
|----------|-------|----------|
| **Documentation** | 40+ files | `docs/` folder |
| **Backend Python Files** | 15 files | `backend/app/` |
| **Frontend TypeScript Files** | 9 files | `frontend/src/` |
| **Architecture Docs** | 18 files | `architecture/` |
| **Test Scripts** | 8 files | `backend/` |
| **Deployment Scripts** | 4 files | Root |
| **Configuration Files** | 6 files | Root + subdirs |
| **Sample Data** | 2 files | `sample_data/` |

---

## 🎯 **Key Files by Purpose**

### **🚀 Getting Started:**
- `README.md` - Main project overview
- `docs/QUICKSTART.md` - Quick start guide
- `setup.bat` - Automated setup
- `start.bat` - Local development startup

### **📦 Deployment:**
- `deploy.bat` - Full deployment automation
- `Dockerfile` - Railway deployment (root level)
- `railway.toml` - Railway configuration
- `backend/Dockerfile` - Backend-specific Docker config
- `frontend/vercel.json` - Vercel configuration

### **⚙️ Configuration:**
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules
- `.dockerignore` - Docker ignore rules
- `railway.toml` - Railway build config

### **📚 Documentation:**
- `docs/README.md` - Documentation index
- `docs/DEPLOYMENT_VERCEL_RAILWAY.md` - Production deployment guide
- `docs/ARCHITECTURE_OVERVIEW.md` - System architecture
- `architecture/` - Phase-wise architecture docs

### **🧪 Testing:**
- `backend/test_*.py` - Test scripts
- `backend/.env.example` - Test environment template

---

## 🔍 **What's Where**

### **Code Files:**
- **Backend Code:** `backend/app/`
- **Frontend Code:** `frontend/src/`
- **Tests:** `backend/test_*.py`

### **Documentation:**
- **All Guides:** `docs/` folder
- **Architecture:** `architecture/` folder
- **Main README:** Root level

### **Configuration:**
- **Environment:** `.env.example` (in backend/)
- **Git:** `.gitignore`
- **Docker:** `Dockerfile`, `.dockerignore`
- **Railway:** `railway.toml`
- **Vercel:** `frontend/vercel.json`

### **Scripts:**
- **Deploy:** `deploy.bat`
- **Setup:** `setup.bat`
- **Start:** `start.bat`

### **Data:**
- **Sample CSVs:** `sample_data/`

---

## 📋 **Before Cleanup vs After Cleanup**

### **❌ Before (Messy):**
```
Root/
├── 40+ .md files scattered everywhere
├── README.md
├── backend/
├── frontend/
└── [hard to find anything]
```

### **✅ After (Clean):**
```
Root/
├── docs/              ← All 40+ .md files organized here
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT_*.md
│   ├── ARCHITECTURE_*.md
│   └── README.md (index)
├── backend/           ← Code only
├── frontend/          ← Code only
├── architecture/      ← Architecture docs
├── README.md          ← Clean main readme
└── [deployment files] ← Easy to find
```

---

## 🎯 **How to Find Anything**

### **Looking for...**

#### **Quick Start Guide?**
→ `docs/QUICKSTART.md`

#### **Deployment Instructions?**
→ `docs/DEPLOYMENT_VERCEL_RAILWAY.md`

#### **Architecture Details?**
→ `docs/ARCHITECTURE_OVERVIEW.md` or `architecture/` folder

#### **Environment Variables?**
→ `backend/.env.example`

#### **How to Deploy?**
→ Run `.\deploy.bat` or read `docs/DEPLOYMENT_VERCEL_RAILWAY.md`

#### **How to Run Locally?**
→ Run `.\start.bat` or read `docs/QUICKSTART.md`

#### **API Documentation?**
→ `http://localhost:8000/docs` (when running)

#### **Test Scripts?**
→ `backend/test_*.py`

---

## ✅ **Benefits of New Structure**

### **Organization:**
- ✅ All documentation in one place (`docs/`)
- ✅ Code separated from docs
- ✅ Easy to navigate
- ✅ Clear hierarchy

### **Discoverability:**
- ✅ Single source of truth (`docs/README.md`)
- ✅ Logical grouping
- ✅ Consistent naming
- ✅ No duplicates

### **Maintenance:**
- ✅ Easy to update
- ✅ Clear ownership
- ✅ Scalable structure
- ✅ Professional appearance

---

## 📞 **Quick Reference**

### **Essential Files:**

| File | Purpose | Location |
|------|---------|----------|
| `README.md` | Main readme | Root |
| `docs/README.md` | Doc index | `docs/` |
| `docs/QUICKSTART.md` | Get started | `docs/` |
| `deploy.bat` | Deploy script | Root |
| `start.bat` | Run locally | Root |
| `Dockerfile` | Railway deploy | Root |
| `railway.toml` | Railway config | Root |
| `.env.example` | Env template | `backend/` |

---

## 🎉 **Clean Structure Complete!**

**Status:** ✅ Organized and Professional  
**Documentation:** All in `docs/` folder  
**Code:** Separated in `backend/` and `frontend/`  
**Config:** Centralized and clear  

**Find anything easily using:** `docs/README.md`
