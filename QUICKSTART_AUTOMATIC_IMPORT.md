# 🚀 Quick Start - Automatic Review Import

## Overview

The App Review Insights Analyzer now **automatically loads** sample review data on startup. No manual upload required!

---

## 🎯 Quick Commands

### 1. Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
✅ Auto-imported 100 sample reviews from sample_data directory
🤖 WEEKLY PULSE SCHEDULER STARTED
INFO:     Application startup complete.
```

### 2. Verify Reviews Loaded

```bash
# Check health status
curl http://localhost:8000/health

# Response shows:
{
  "reviews_loaded": 100,
  "auto_import_enabled": true,
  "scheduler_running": true,
  ...
}
```

### 3. View Review Statistics

```bash
curl http://localhost:8000/api/reviews/stats

# Response:
{
  "total": 100,
  "app_store": 50,
  "play_store": 50,
  "average_rating": 2.96,
  "oldest_review": "2026-01-20T00:00:00",
  "newest_review": "2026-03-11T00:00:00"
}
```

---

## 📁 Sample Data Location

Sample review files are located in:
```
App_Review_Insights_Analyser/sample_data/
├── app_store_reviews.csv      (50 reviews)
└── play_store_reviews.csv     (50 reviews)
```

These files are **automatically loaded** every time the server starts.

---

## 🔧 Configuration

### Change Date Range

By default, only reviews from the last **8 weeks** are loaded. To change this:

**Option 1:** Edit `.env` file
```bash
# backend/.env
REVIEW_WEEKS_RANGE=12    # Load last 12 weeks instead
```

**Option 2:** Use manual import endpoint with custom weeks parameter

---

## 🎛️ Manual Control

### Re-import Sample Data

Clear all reviews and re-import:

```bash
# Step 1: Clear existing reviews
curl -X DELETE http://localhost:8000/api/reviews

# Step 2: Re-import with default settings (8 weeks)
curl -X POST http://localhost:8000/api/reviews/import-sample-data

# Step 3: Or import with custom date range (4 weeks)
curl -X POST "http://localhost:8000/api/reviews/import-sample-data?weeks=4"
```

**Response:**
```json
{
  "message": "Sample data imported successfully",
  "app_store_count": 23,
  "play_store_count": 24,
  "total_imported": 47,
  "total_in_database": 47,
  "date_range_weeks": 4
}
```

---

## ✅ Features

### What Happens Automatically:

1. ✅ **Auto-Load on Startup**
   - Loads `app_store_reviews.csv`
   - Loads `play_store_reviews.csv`
   - Filters to last 8 weeks (configurable)
   - Adds to reviews database

2. ✅ **Scheduler Integration**
   - Weekly pulse scheduler starts automatically
   - Runs every Monday at 3:35 PM IST
   - Uses auto-loaded reviews for analysis

3. ✅ **Health Monitoring**
   - Health endpoint shows review count
   - Shows auto-import status
   - Complete system status

---

## 🐛 Troubleshooting

### Issue: No reviews loaded

**Check logs for:**
```
⚠️ No sample reviews found in sample_data directory
```

**Solutions:**
1. Verify CSV files exist in `sample_data/` folder
2. Check file names match exactly:
   - `app_store_reviews.csv`
   - `play_store_reviews.csv`
3. Ensure CSV format is correct (see below)

### Issue: Fewer reviews than expected

**Possible causes:**
- Reviews older than 8 weeks are filtered out
- Reviews with less than 5 words in text are excluded

**Solutions:**
1. Increase `REVIEW_WEEKS_RANGE` in `.env`
2. Check CSV date format
3. Verify review text length

---

## 📊 CSV Format Reference

### App Store Format

```csv
Date,Rating,Title,Review
2026-03-10,5,"Great App","This app is amazing! Love the features."
2026-03-09,4,"Good","Overall good experience but needs work."
```

### Play Store Format

```csv
Date,Star Rating,Title,Text
2026-03-10,5,"Perfect","Works flawlessly on my device."
2026-03-09,3,"Okay","Decent but has performance issues."
```

---

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Console shows: `✅ Auto-imported 100 sample reviews`
2. ✅ Health endpoint shows: `"reviews_loaded": 100`
3. ✅ Stats endpoint shows total reviews
4. ✅ Scheduler running (check `/health`)
5. ✅ No error messages in logs

---

## 📝 Next Steps

After reviews are loaded, you can:

1. **View Reviews:** `GET /api/reviews`
2. **Analyze Themes:** `POST /api/analyze/gemini`
3. **Generate Report:** `POST /api/reports/generate`
4. **Send Email:** `POST /api/email/send-weekly-digest`
5. **Trigger Scheduler:** `POST /api/scheduler/trigger-now`

---

## 🔗 Related Documentation

- [Full Feature Documentation](../AUTOMATIC_REVIEW_IMPORT.md)
- [API Documentation](../backend/API_REFERENCE.md)
- [Scheduler Setup](../architecture/PHASE_08_Automated_Scheduler.md)

---

**Last Updated:** March 15, 2026  
**Status:** ✅ Production Ready
