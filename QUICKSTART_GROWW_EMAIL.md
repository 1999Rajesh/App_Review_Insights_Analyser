# 🚀 Quick Start: Groww Weekly Email Reports

**Goal:** Get weekly email insights for Groww app reviews in 3 easy steps!

---

## ⚡ 3-Step Setup (5 Minutes)

### Step 1: Fetch Groww Reviews (1 minute)

**Via UI:**
1. Open http://localhost:3001
2. Find "🤖 Auto-Fetch from Google Play Store"
3. Enter App ID: **`in.groww`**
4. Click **"🚀 Fetch Play Store Reviews"**
5. Wait 5-10 seconds

**You'll see:**
```
✅ Successfully fetched 250 reviews from Google Play Store
```

---

### Step 2: Generate Report (1 minute)

**Still in UI:**
1. Scroll to "✨ Generate Weekly Report"
2. Click **"Generate Weekly Report"**
3. Wait 15-20 seconds

**AI will analyze:**
- All reviews (currently 350 total)
- Identify top 5 themes
- Extract real user quotes
- Create 3 action ideas

---

### Step 3: Send Email (1 minute)

**Final step:**
1. Scroll to "📧 Email Weekly Report"
2. Verify recipient email
3. Click **"📧 Send Email Report"**
4. Check your inbox!

**Email arrives with:**
```
Subject: 📊 Weekly Pulse: Groww App Reviews (Mar 9-15, 2026)

Contents:
✅ Top 5 themes with percentages
✅ Real user quotes (verbatim)
✅ 3 prioritized action items
✅ Statistics snapshot
✅ Trending indicators
```

---

## 🎯 That's It!

You now have automated weekly insights for Groww app reviews!

---

## 🔄 Make It Automatic (Optional)

### Change Scheduler from Testing to Production:

**Current:** Every 5 minutes (for testing)  
**Production:** Every Monday at 3:35 PM IST

**How to Change:**

1. Open `backend/.env`
2. Find this line:
   ```
   SCHEDULER_INTERVAL_MINUTES=5
   ```
3. Change to:
   ```
   SCHEDULER_INTERVAL_MINUTES=10080
   ```
   *(10080 minutes = 7 days)*

4. Restart backend server

**Now emails arrive automatically every Monday!**

---

## 📊 What You Get Each Week

### Email Preview:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SNAPSHOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reviews Analyzed: 350
Average Rating: 4.3/5.0
Period: Last 8 weeks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TOP THEMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Easy to Use (45% positive)
   💬 "Super intuitive interface!"
   💬 "Best investing app I've used"
   
2️⃣ Customer Support Issues (32% negative)
   💬 "Support takes too long to respond"
   💬 "Need better phone support"
   
3️⃣ Fast Execution (28% positive)
   💬 "Orders execute instantly"
   💬 "Never faced any lag"
   
... (2 more themes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 ACTION IDEAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority Actions for This Week:

1. 🎯 Enhance Customer Support
   • Hire 2-3 additional support staff
   • Implement chatbot for common queries
   
2. 🎯 Improve Notification System
   • Add granular notification controls
   • Allow users to choose categories
   
3. 🎯 Expand Educational Content
   • Create beginner video tutorials
   • Add weekly market insights

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keep up the great work! 🚀
```

---

## 🛠️ Troubleshooting

### Problem: No reviews found

**Solution:** Try different country
- Change Country selector to "United States"
- Click fetch again

---

### Problem: Email not arriving

**Solutions:**
1. Check spam folder
2. Verify email address is correct
3. For production: Configure real Gmail credentials

---

### Problem: Report generation slow

**Solutions:**
1. Reduce number of reviews (try 200 instead of 500)
2. Shorten date range (try 4 weeks instead of 8)
3. Check internet connection (Gemini API needs connectivity)

---

## 📁 Files Created

Your system automatically creates:

1. **JSON Report:** `backend/reports/weekly_report_YYYY-Www.json`
2. **Scheduler Log:** `backend/logs/scheduler.log`
3. **Email Draft:** In your inbox!

---

## 🎉 Success Checklist

- [ ] ✅ Reviews fetched from Play Store
- [ ] ✅ Report generated with 5 themes
- [ ] ✅ Email received with real quotes
- [ ] ✅ 3 action ideas provided
- [ ] ✅ Formatting looks professional
- [ ] ✅ Can read in under 5 minutes

---

## 📞 Need Help?

**Quick Commands:**

Check review count:
```bash
curl http://localhost:8000/api/reviews/stats
```

View scheduler logs:
```bash
tail -f backend/logs/scheduler.log
```

Test email:
```bash
curl -X POST http://localhost:8000/api/email/send-report
```

---

## 🔗 Full Documentation

For complete details, see:
- `GROWW_WEEKLY_PULSE_SETUP.md` (comprehensive guide)
- `WEEKLY_EMAIL_AUTOMATION_GROWW.md` (email setup details)
- `DATA_MODELS_DOCUMENTATION.md` (data structures)

---

**Ready to receive weekly Groww insights!** 🚀

**Time to Complete:** 3-5 minutes  
**Difficulty:** Easy  
**Status:** ✅ PRODUCTION READY
