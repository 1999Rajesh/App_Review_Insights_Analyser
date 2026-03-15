# 🚀 Quick Start Guide

## Get Running in 5 Minutes

### Step 1: Prerequisites Check

Make sure you have:
- ✅ Python 3.9+ installed ([Download](https://www.python.org/))
- ✅ Node.js 16+ installed ([Download](https://nodejs.org/))
- ✅ Groq API key ([Get Free](https://console.groq.com))
- ✅ Gmail/Outlook account

### Step 2: One-Command Setup

**Windows:**
```bash
.\setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

**Backend:**
```bash
cd backend
python -m pip install fastapi uvicorn python-multipart groq pandas python-dotenv pydantic pydantic-settings aiofiles email-validator
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 3: Configure Environment

1. Go to `backend` folder
2. Copy `.env.example` to `.env`
3. Edit `.env` with your credentials:

```env
# Get your Groq API key from https://console.groq.com
GROQ_API_KEY=gsk_your_actual_key_here

# For Gmail: Create App Password at https://myaccount.google.com/apppasswords
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

**Important for Gmail Users:**
- You MUST use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password
- Regular passwords won't work due to 2FA

### Step 4: Start the Application

**Windows:**
```bash
.\start.bat
```

**Manual Start:**

Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Step 5: Open the App

Navigate to: **http://localhost:3000**

You should see the beautiful purple gradient interface! 🎉

## Testing with Sample Data

We've included sample CSV files so you can test immediately:

1. On the upload page, drag these files:
   - `sample_data/app_store_reviews.csv` → Left box
   - `sample_data/play_store_reviews.csv` → Right box

2. Click **"Upload & Process Reviews"**

3. Click **"✨ Generate Weekly Report"**

4. Watch the AI analyze 100 reviews in seconds! ⚡

5. Click **"📧 Send Email Digest"** to receive the report

## First Time User Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000  
- [ ] `.env` file configured with real API keys
- [ ] Tested connection (button in UI)
- [ ] Uploaded sample CSVs successfully
- [ ] Generated first weekly report
- [ ] Received test email

## Common Issues & Fixes

### "Module not found" errors
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd frontend
npm install
```

### "Port already in use" error
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or change port in backend/app/main.py
```

### Groq API errors
- Check your API key is correct in `.env`
- Verify you have credits at https://console.groq.com
- Try switching model to `mixtral-8x7b-32768`

### Email not sending
- Use App Password for Gmail (not regular password)
- Check SMTP settings:
  - Gmail: `smtp.gmail.com`, Port 465
  - Outlook: `smtp.office365.com`, Port 587

### CSV upload errors
- Verify CSV has required columns:
  - App Store: `Date, Rating, Title, Review`
  - Play Store: `Date, Star Rating, Title, Text`
- Check date format is valid (YYYY-MM-DD recommended)

## Next Steps

Once everything is working:

1. **Export your real app reviews** from:
   - [App Store Connect](https://appstoreconnect.apple.com)
   - [Google Play Console](https://play.google.com/console)

2. **Configure your preferences** in `.env`:
   ```env
   REVIEW_WEEKS_RANGE=8        # Analyze last 8 weeks
   MAX_THEMES=5                # Max 5 themes
   MAX_WORDS=250               # Keep report under 250 words
   ```

3. **Set up weekly automation** (optional):
   - Use Windows Task Scheduler or cron job
   - Schedule script to run every Monday at 9 AM
   - Automatically email yourself weekly pulse

4. **Customize themes** for your product:
   - Edit the theme list in `backend/app/services/groq_analyzer.py`
   - Add your specific feature areas

## Getting Help

- 📖 Full documentation: See [README.md](README.md)
- 🔧 API reference: http://localhost:8000/docs
- 💬 Issues: Check README troubleshooting section

## What's Next?

Try these advanced features:

1. **Historical Analysis** - Upload multiple weeks of data
2. **Custom Themes** - Modify prompt for your industry
3. **Team Sharing** - Send reports to multiple recipients
4. **PDF Export** - Generate PDF versions of reports

---

**Congratulations!** You're now ready to turn app reviews into actionable insights! 🎯

Happy analyzing! 📊
