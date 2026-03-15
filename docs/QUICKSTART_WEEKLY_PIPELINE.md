# 🚀 Quick Start: Weekly Review Pipeline

## 30-Second Overview

**What:** Automated pipeline that fetches Groww reviews → analyzes themes → emails insights  
**When:** Every week automatically (or run manually)  
**Output:** One-page note with top 3 themes, user quotes, action items  
**Privacy:** All PII removed (emails, phones, cards, PAN, Aadhaar)

---

## Run Locally (Right Now)

```bash
cd backend

# Option 1: Complete pipeline (no email)
python -m services.weekly_review_pipeline --no-email

# Option 2: Just generate note from existing data
python -m services.weekly_pulse_generator

# Option 3: Just collect reviews
python -m services.hybrid_review_collector
```

---

## Output Files

After running, you get:

1. **JSON:** `data/reviews/YYYY-MM-DD.json` - API-ready format
2. **CSV:** `weekly_reviews/reviews_year_week_N.csv` - Excel-friendly
3. **Note:** `weekly_pulse_note_YYYY-MM-DD.md` - Email content

---

## Deploy to Railway (Automate)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add hybrid weekly review pipeline"
git push origin main
```

### 2. Railway Setup
1. Connect Railway to your repo
2. Add environment variables (see below)
3. Create Scheduled Task
4. Set schedule: `0 10 * * 1` (Mondays at 10 AM IST)

### 3. Environment Variables
```bash
PLAY_STORE_DEFAULT_APP_ID=com.nextbillion.groww
REVIEW_WEEKS_RANGE=12
MAX_REVIEWS_TO_FETCH=500
MIN_REVIEW_WORD_COUNT=5
ALLOW_EMOJIS=false
REQUIRED_LANGUAGE=en
SMTP_SENDER_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
WEEKLY_REPORT_EMAIL=recipient@example.com
```

---

## What You Get Every Week

### Email Subject
```
Weekly App Review Pulse - Week 11, 2026
```

### Email Content Preview
```markdown
# 📊 Weekly App Review Pulse

## 🎯 Executive Summary
This week analyzed **280 reviews** across **5 key themes**.
- 😊 Positive: 150 reviews
- 😞 Negative: 80 reviews  
- 😐 Neutral: 50 reviews

## 📋 Top 3 Themes

### 1. KYC Verification 😞
**Impact:** 85 reviews (30.4%) | Avg Rating: 2.3/5 ⭐

**What Users Are Saying:**
- "KYC verification is taking too long"
- "Document approval needs improvement"
- "Support team not responding"

**Recommended Actions:**
1. Implement automated document verification
2. Add instant retry for rejected documents
3. Provide clear rejection reasons

[... continues for themes 2 & 3 ...]
```

---

## Test It Works

```bash
cd backend

# Run test suite
python test_weekly_pipeline.py --skip-collector

# Expected output:
# ✅ PASS - pii_protection
# ✅ PASS - pulse_generator
# ✅ PASS - complete_pipeline
```

---

## Pre-configured Themes

The AI automatically groups reviews into:
1. Onboarding
2. KYC Verification
3. Payments & Transactions
4. Account Statements
5. Withdrawals
6. Stock Trading
7. Mutual Funds
8. Customer Support
9. App Performance
10. UI/UX Experience

---

## Privacy Protection

All of these are automatically redacted:
- ✉️ Emails → `[EMAIL_REDACTED]`
- 📞 Phones → `[PHONE_REDACTED]`
- 💳 Cards → `[CARD_REDACTED]`
- 🆔 PAN → `[PAN_REDACTED]`
- 🔢 Aadhaar → `[AADHAAR_REDACTED]`
- 🌐 URLs → `[URL_REDACTED]`

---

## Configuration Quick Reference

| Variable | Default | What It Does |
|----------|---------|--------------|
| `REVIEW_WEEKS_RANGE` | 12 | How many weeks back to fetch |
| `MAX_REVIEWS_TO_FETCH` | 500 | Max reviews per run |
| `MIN_REVIEW_WORD_COUNT` | 5 | Filter out short reviews |
| `ALLOW_EMOJIS` | false | Allow emoji-heavy reviews |
| `REQUIRED_LANGUAGE` | en | Only English reviews |

---

## Troubleshooting

**No reviews fetched?**
→ Check app ID: `com.nextbillion.groww` (not `in.groww`)

**Email not sending?**
→ Use Gmail App Password (16 chars), not regular password

**Themes wrong?**
→ Edit keywords in `weekly_pulse_generator.py`

---

## Full Documentation

See [WEEKLY_REVIEW_AUTOMATION.md](file://c:\Users\Rajesh\Documents\App_Review_Insights_Analyser\docs\WEEKLY_REVIEW_AUTOMATION.md) for complete details.

---

**That's it! Set it up once, then get weekly insights automatically.** 🎉
