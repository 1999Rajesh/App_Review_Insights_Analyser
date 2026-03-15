# 🔄 Weekly Review Automation Pipeline

**Complete end-to-end automation for fetching, analyzing, and emailing weekly app review insights.**

---

## 🎯 What This Pipeline Does

1. **Fetches reviews** from Google Play Store (last 8-12 weeks)
2. **Saves in hybrid format**: 
   - JSON (for fast API/Frontend)
   - Weekly CSV (for human browsing)
3. **Generates one-page weekly note** with:
   - Top 3 themes (from max 5 identified)
   - 3 user quotes per theme
   - 3 action ideas per theme
4. **Emails the report** automatically
5. **Runs on schedule** (weekly via Railway cron job)

**✅ NO PII included** - All emails, phones, card numbers redacted

---

## 📁 Files Created

```
backend/services/
├── hybrid_review_collector.py    # Fetches & saves reviews (JSON + CSV)
├── weekly_pulse_generator.py     # Analyzes themes & generates note
├── weekly_review_pipeline.py     # Complete end-to-end automation
└── railway_weekly_task.py        # Railway scheduled task runner
```

---

## 🚀 Quick Start

### Option 1: Run Locally (One-Time)

```bash
# Navigate to backend directory
cd backend

# Run complete pipeline (with email)
python -m services.weekly_review_pipeline

# Run without email (only generate files)
python -m services.weekly_review_pipeline --no-email

# Custom parameters
python -m services.weekly_review_pipeline --weeks 8 --max-reviews 200
```

### Option 2: Run on Railway (Automated Weekly)

See [Railway Setup](#railway-setup) below.

---

## 📊 Output Files

### 1. JSON Format (API-Ready)
**Location:** `backend/data/reviews/YYYY-MM-DD.json`

```json
{
  "metadata": {
    "scrapedAt": "2026-03-15T10:30:00",
    "packageId": "in.groww",
    "weeksRequested": 12,
    "totalFetched": 500,
    "afterDateFilter": 350,
    "totalAfterFilters": 280,
    "filterStats": {
      "too_short": 50,
      "has_emoji": 10,
      "wrong_language": 10,
      "pii_removed": 5
    }
  },
  "reviews": [...]
}
```

**Use Case:** Fast loading for frontend/API

### 2. Weekly CSV Format (Human-Readable)
**Location:** `backend/weekly_reviews/reviews_2026_week_11.csv`

```csv
review_id,score,content,date
review_001,5,"Great app for investing...",2026-03-10
review_002,3,"KYC took too long...",2026-03-09
```

**Use Case:** Easy browsing in Excel, stakeholder sharing

### 3. Weekly Pulse Note (Markdown)
**Location:** `weekly_pulse_note_2026-03-15.md`

```markdown
# 📊 Weekly App Review Pulse
**Week 11, 2026** | Generated: March 15, 2026

---

## 🎯 Executive Summary
This week analyzed **280 reviews** across **5 key themes**.

**Quick Stats:**
- 😊 Positive: 150 reviews
- 😞 Negative: 80 reviews  
- 😐 Neutral: 50 reviews

---

## 📋 Top 3 Themes This Week

### 1. KYC Verification 😞

**Impact:** 85 reviews (30.4%) | Avg Rating: 2.3/5 ⭐

**What Users Are Saying:**
- "KYC verification is taking too long"
- "Document approval needs improvement"
- "Support team not responding to queries"

**Recommended Actions:**
1. Implement automated document verification
2. Add instant retry for rejected documents
3. Provide clear rejection reasons with examples

---

[... continues for themes 2 and 3 ...]
```

**Use Case:** Email report, stakeholder updates

---

## 🔧 Configuration

### Environment Variables

Create/update `.env` file in `backend/` directory:

```bash
# Play Store Configuration
PLAY_STORE_DEFAULT_APP_ID=in.groww
PLAY_STORE_LANGUAGE=en
PLAY_STORE_COUNTRY=in

# Review Filters
MAX_REVIEWS_TO_FETCH=500
REVIEW_WEEKS_RANGE=12
MIN_REVIEW_WORD_COUNT=5
ALLOW_EMOJIS=false
REQUIRED_LANGUAGE=en

# Data Directories
REVIEWS_DATA_DIR=data/reviews
CSV_DATA_DIR=weekly_reviews

# Email Configuration (for sending reports)
SMTP_SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
WEEKLY_REPORT_EMAIL=recipient@example.com
```

### Filter Settings Explained

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_REVIEWS_TO_FETCH` | 500 | Maximum reviews to fetch from Play Store |
| `REVIEW_WEEKS_RANGE` | 12 | Look back period in weeks (8-12 recommended) |
| `MIN_REVIEW_WORD_COUNT` | 5 | Minimum words required (filters out "good", "nice") |
| `ALLOW_EMOJIS` | false | Allow emoji-heavy reviews |
| `REQUIRED_LANGUAGE` | en | Only English reviews |

---

## 🛠️ Railway Setup (Automated Weekly)

### Step 1: Deploy Backend to Railway

1. Push code to GitHub
2. Connect Railway to your repo
3. Deploy as usual (Dockerfile or Python buildpack)

### Step 2: Add Environment Variables

In Railway dashboard, add all variables from [Configuration](#configuration) section.

### Step 3: Create Scheduled Task

1. Go to Railway project → **New** → **Scheduled Task**
2. Select your deployed service
3. Set command: `python -m services.railway_weekly_task`
4. Set schedule: `0 10 * * 1` (Every Monday at 10:00 AM IST)
5. Click **Deploy**

### Step 4: Verify Execution

Check Railway logs after scheduled run:
```
🤖 RAILWAY SCHEDULED TASK: WEEKLY REVIEW PIPELINE
⏰ Execution time: 2026-03-18 10:00:00 IST
✅ Environment variables configured
🚀 WEEKLY REVIEW PIPELINE
...
✅ Email sent successfully to recipient@example.com
🎉 PIPELINE EXECUTION SUCCESSFUL
```

---

## 📈 Theme Analysis

### Pre-configured Themes for Groww App

The pipeline automatically groups reviews into these themes:

1. **Onboarding** - Signup, registration, first-time experience
2. **KYC Verification** - Document approval, PAN/Aadhaar verification
3. **Payments & Transactions** - UPI, bank transfers, failed payments
4. **Account Statements** - Download, export, transaction history
5. **Withdrawals** - Payouts, settlement, bank transfers
6. **Stock Trading** - Orders, portfolio, buying/selling
7. **Mutual Funds** - SIP, investments, NAV
8. **Customer Support** - Help desk, response time, complaints
9. **App Performance** - Speed, crashes, bugs, errors
10. **UI/UX Experience** - Design, navigation, ease of use

### How It Works

- **Keyword matching**: Reviews classified by keywords
- **Sentiment analysis**: Based on average rating per theme
- **Top 3 selection**: Themes sorted by review count
- **Max 5 themes**: Only top 5 shown to avoid information overload

---

## 📧 Email Automation

### What Gets Sent

- **Subject:** `Weekly App Review Pulse - Week 11, 2026`
- **Format:** Markdown email
- **Content:** One-page note with top 3 themes
- **Attachments:** None (content in email body)
- **Recipient:** Configured via `WEEKLY_REPORT_EMAIL`

### Gmail Setup (Required for SMTP)

1. Enable 2FA on your Gmail account
2. Generate an **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
3. Use this password in `.env` (NOT your regular Gmail password)

```bash
SMTP_SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # 16-char app password
```

---

## 🧪 Testing

### Test the Complete Pipeline

Run test script (included):

```bash
cd backend

# Test with sample data (no email)
python test_weekly_pipeline.py

# Test live fetch (with email)
python test_weekly_pipeline.py --live --email
```

### Expected Output

```
======================================================================
🚀 WEEKLY REVIEW PIPELINE
⏰ Started at: 2026-03-15 14:30:00
======================================================================

======================================================================
📥 STEP 1/4: COLLECTING REVIEWS
======================================================================
🚀 Fetching reviews for in.groww...
📊 Max reviews: 500, Weeks: 12
✅ Fetched 500 raw reviews
📅 After date filter (12 weeks): 350 reviews
🔍 Applying quality filters and PII removal...
✅ After quality filters: 280 reviews
💾 Saved JSON to data/reviews/2026-03-15.json
✅ Saved CSV to weekly_reviews/reviews_2026_week_11.csv

======================================================================
📝 STEP 2/4: GENERATING WEEKLY PULSE NOTE
======================================================================
📂 Loading reviews from: data/reviews/2026-03-15.json
✅ Loaded 280 reviews
🎯 Grouping 280 reviews into themes...
✅ Identified 5 themes
   - KYC Verification: 85 reviews (30.4%)
   - Payments & Transactions: 70 reviews (25.0%)
   - UI/UX Experience: 50 reviews (17.9%)
   - App Performance: 45 reviews (16.1%)
   - Customer Support: 30 reviews (10.7%)

✅ Saved weekly note to: weekly_pulse_note_2026-03-15.md

======================================================================
📧 STEP 3/4: SENDING EMAIL REPORT
======================================================================
✅ Email sent successfully to codeflex1999@gmail.com

======================================================================
✅ STEP 4/4: PIPELINE COMPLETE
======================================================================

📊 SUMMARY:
   ✅ Reviews collected: 280
   📄 JSON file: data/reviews/2026-03-15.json
   📊 CSV file: weekly_reviews/reviews_2026_week_11.csv
   🎯 Themes identified: 5
   📝 Note file: weekly_pulse_note_2026-03-15.md
   📧 Email sent: True
   📨 Sent to: codeflex1999@gmail.com

======================================================================
🎉 PIPELINE EXECUTION SUCCESSFUL
======================================================================
```

---

## 🔒 Privacy & PII Protection

### What Gets Redacted

The following PII is automatically removed:

- ✉️ **Email addresses** → `[EMAIL_REDACTED]`
- 📞 **Phone numbers** → `[PHONE_REDACTED]`
- 💳 **Card numbers** → `[CARD_REDACTED]`
- 🆔 **PAN cards** → `[PAN_REDACTED]`
- 🔢 **Aadhaar numbers** → `[AADHAAR_REDACTED]`
- 🌐 **URLs** → `[URL_REDACTED]`
- 🖥️ **IP addresses** → `[IP_REDACTED]`

### Quality Filters Applied

- ❌ Reviews with < 5 words (too short)
- ❌ Reviews with emojis (if disabled)
- ❌ Non-English reviews (if language filter enabled)
- ❌ Reviews with PII (redacted before storage)

---

## 📅 Weekly Schedule Example

### Timeline (Automatic)

**Every Monday at 10:00 AM IST:**

1. **10:00 AM** - Railway task triggers
2. **10:01 AM** - Fetch latest reviews (last 12 weeks)
3. **10:03 AM** - Apply filters & PII removal
4. **10:05 AM** - Save JSON + CSV files
5. **10:07 AM** - Generate weekly pulse note
6. **10:10 AM** - Email sent to stakeholders

### Result

By 10:15 AM every Monday, you receive:
- ✅ Email with top 3 themes
- ✅ 3 user quotes per theme
- ✅ 3 action ideas per theme
- ✅ Zero PII included

---

## 🎯 Success Metrics

After 8-12 weeks, you'll have:

- 📁 **8-12 weekly CSV files** (one per week)
- 📊 **Consistent JSON dataset** (all reviews in one file)
- 📈 **Trend analysis capability** (compare week-over-week)
- 🎯 **Actionable insights** (AI-generated recommendations)
- ✉️ **Automated reporting** (hands-free operation)

---

## 🛠️ Troubleshooting

### Issue: No reviews fetched

**Solution:** Check app ID
```bash
# Verify app ID is correct
echo $PLAY_STORE_DEFAULT_APP_ID
# Should output: in.groww
```

### Issue: Email not sending

**Solution:** Use Gmail App Password (not regular password)
```bash
# Generate at: https://myaccount.google.com/apppasswords
SMTP_PASSWORD="16-char-app-password"
```

### Issue: Themes not relevant

**Solution:** Customize theme keywords in `weekly_pulse_generator.py`
```python
theme_keywords = {
    "Your Theme": ["keyword1", "keyword2", "keyword3"]
}
```

---

## 🚀 Next Steps

1. ✅ **Run locally once** to test configuration
2. 📦 **Deploy to Railway** for automation
3. ⏰ **Set weekly schedule** in Railway dashboard
4. 📧 **Verify email delivery** after first run
5. 📊 **Review weekly notes** every Monday

---

## 📞 Support

For issues or questions:
- Check Railway logs for execution errors
- Verify environment variables are set correctly
- Ensure Gmail 2FA is enabled for SMTP

---

**Powered by App Review Insights Analyzer**  
*Turning app store reviews into actionable weekly insights*
