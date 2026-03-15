# 🎬 3-Minute Demo Video Script

## App Review Insights Analyzer - Demo Flow

**Total Duration:** 3:00 minutes  
**Target Audience:** Product managers, leadership, evaluation committee

---

## Pre-Recording Setup Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Sample CSVs ready in `sample_data/` folder
- [ ] `.env` configured with working Groq API key
- [ ] Email credentials configured and tested
- [ ] Screen recording software ready (OBS, Loom, etc.)
- [ ] Browser at 1920x1080 resolution
- [ ] Clean desktop (hide unnecessary icons)
- [ ] Notifications turned off
- [ ] Audio levels checked (if doing voiceover)

---

## Script Breakdown

### Scene 1: Introduction (0:00-0:30)

**Visual:** Landing page with purple gradient background

**Narration:**
> "Hi, I'm [Your Name], and today I'll show you the App Review Insights Analyzer—a tool that turns hundreds of app store reviews into a one-page weekly pulse in under 15 seconds."

**Actions:**
- Show full screen of http://localhost:3000
- Point to header: "App Review Insights Analyzer"
- Highlight subtitle: "Turn app store reviews into actionable weekly insights"

**Key Points:**
- Problem: Product teams drown in reviews but starve for insights
- Solution: Automated AI-powered analysis
- Result: Actionable weekly report in seconds

**Transition:**
> "Let me show you how it works."

---

### Scene 2: Upload Reviews (0:30-1:00)

**Visual:** Upload interface with two drop zones

**Narration:**
> "First, we export reviews from both app stores as CSV files. I have 50 reviews from the App Store and 50 from the Play Store—covering the last 8 weeks."

**Actions:**
- Navigate to sample_data folder
- Show app_store_reviews.csv
- Show play_store_reviews.csv
- Drag App Store CSV to left drop zone
- Drag Play Store CSV to right drop zone
- Click "Upload & Process Reviews" button

**On-Screen Text:**
- "100 reviews uploaded"
- "App Store: 50 | Play Store: 50"
- "Date range: Last 8 weeks"
- "PII removed automatically"

**Key Points:**
- Supports both standard CSV formats
- Automatic date filtering
- PII sanitization before processing

**Transition:**
> "Now that our reviews are uploaded, let's generate the weekly report."

---

### Scene 3: Generate Report (1:00-1:30)

**Visual:** Upload success message, ready to generate

**Narration:**
> "With one click, we'll trigger our Groq-powered AI to analyze all 100 reviews. It will identify the top themes, select the best user quotes, and generate actionable recommendations—all in about 10 seconds."

**Actions:**
- Click "✨ Generate Weekly Report" button
- Show loading indicator
- Brief pause (5-10 seconds)

**On-Screen Text:**
- "Analyzing with Groq LLM..."
- "Model: Llama 3.1 70B"
- "Processing time: ~10 seconds"

**Key Points:**
- Ultra-fast Groq inference (10-100x faster)
- Groups into max 5 themes
- Enforces 250-word limit

**Transition:**
> "And here's our weekly pulse report!"

---

### Scene 4: Review Report (1:30-2:00)

**Visual:** Generated weekly report displayed

**Narration:**
> "Our report shows the top 3 themes this week. For each theme, we see the percentage of reviews, sentiment analysis, real user quotes word-for-word, and three specific action ideas our team can implement."

**Actions:**
- Scroll through report sections slowly
- Highlight Theme #1 (e.g., "Withdrawals - 35%")
- Point to user quotes
- Show action ideas
- Show word count badge

**On-Screen Text:**
- "Top 3 Themes by Volume"
- "Real User Quotes (verbatim)"
- "Actionable Recommendations"
- "Word Count: 245/250"

**Example Callouts:**
> "Notice this theme: 'Withdrawal Issues' at 35%—that's clearly our biggest pain point. The AI even selected this powerful quote: 'Been waiting 5 days for my withdrawal...' This is exactly what leadership needs to see."

**Key Points:**
- Scannable in 30 seconds
- Real quotes provide context
- Action items are specific and implementable

**Transition:**
> "Now let's send this report to our team via email."

---

### Scene 5: Send Email (2:00-2:30)

**Visual:** Report with email button visible

**Narration:**
> "With one click, we can send this formatted report as an HTML email. Perfect for our weekly product sync or leadership update."

**Actions:**
- Click "📧 Send Email Digest" button
- Show confirmation message
- Switch to email client (Gmail/Outlook)
- Open received email
- Show formatted HTML version

**On-Screen Text:**
- "Email sent successfully!"
- "Subject: Weekly App Review Pulse - [Date]"
- "Recipient: product-team@company.com"

**Key Points:**
- SMTP integration (Gmail/Outlook)
- HTML + plain text versions
- Professional formatting
- Ready to forward to stakeholders

**Example Callouts:**
> "The email arrives instantly, beautifully formatted and ready to share. No manual copy-pasting, no formatting issues."

**Transition:**
> "Let me wrap up with a quick look under the hood."

---

### Scene 6: Code Walkthrough (2:30-3:00)

**Visual:** Split screen - code editor + API docs

**Narration:**
> "Built with FastAPI and React, powered by Groq's ultra-fast LLM. The entire workflow—from upload to email—takes less than 15 seconds and costs fractions of a cent in API credits."

**Actions:**
- Quick switch to API docs (http://localhost:8000/docs)
- Show list of endpoints
- Brief glimpse at code structure
- Return to main app

**On-Screen Text:**
- "Tech Stack: FastAPI + React + Groq"
- "12 API Endpoints"
- "Open Source Available"
- "Cost: ~$0.50/week in API credits"

**Key Points:**
- Modern, scalable architecture
- Auto-generated API documentation
- Production-ready codebase
- Extremely cost-effective

**Closing Statement:**
> "That's the App Review Insights Analyzer—turning review chaos into clarity in record time. Thanks for watching!"

**End Screen:**
- Project logo/title
- Your name/contact
- GitHub repo link (if applicable)
- "Questions?" text

---

## Recording Tips

### Audio Quality
- Use a quiet room with minimal echo
- Speak clearly and at moderate pace
- Consider using a lapel mic or headset
- Do a 10-second test recording first

### Visual Quality
- Set browser to 1920x1080 resolution
- Use browser's full-screen mode (F11)
- Hide bookmarks bar and extensions
- Increase font size slightly for visibility (Ctrl +)

### Pacing
- Practice the script 2-3 times before recording
- Use a timer to stay within 3 minutes
- Pause briefly between sections
- Don't rush—viewers need time to absorb visuals

### Editing (Optional)
- Add smooth transitions between scenes
- Include subtle background music (royalty-free)
- Add text overlays for key points
- Speed up loading/waiting segments (1.5x)

### Common Mistakes to Avoid
- ❌ Speaking too fast
- ❌ Skipping over important UI elements
- ❌ Not testing audio levels
- ❌ Going over 3 minutes
- ❌ Showing personal information
- ❌ Background noise/distractions

---

## Backup Plan

If live demo fails during recording:

**Option 1: Screenshots**
- Take screenshots of each step
- Create slideshow with narration
- More controlled, less dynamic

**Option 2: Screen Recording Software**
- Use Loom, OBS, or Camtasia
- Record multiple takes
- Edit together best segments

**Option 3: Pre-recorded Segments**
- Record each scene separately
- Stitch together in editing
- Easier to get perfect takes

---

## Post-Production

### File Export Settings
- **Format:** MP4 (H.264 codec)
- **Resolution:** 1920x1080 (Full HD)
- **Frame Rate:** 30 fps
- **Bitrate:** 8-10 Mbps
- **Audio:** AAC, 128 kbps

### Distribution
- Upload to YouTube (unlisted or public)
- Share via Google Drive/Dropbox
- Embed in presentation slides
- Include link in README

---

## Alternative Versions

### 1-Minute Elevator Pitch
- Scene 1: 10 sec (intro)
- Scene 2: 15 sec (upload)
- Scene 3: 20 sec (generate)
- Scene 4: 15 sec (result)

### 5-Minute Deep Dive
- Extend Scene 6 to 1 minute
- Show code structure
- Explain technical decisions
- Demonstrate error handling

---

## Rehearsal Checklist

- [ ] Script memorized (or printed nearby)
- [ ] All files and pages pre-loaded
- [ ] Sample data ready to upload
- [ ] Email inbox ready to show
- [ ] Transitions practiced
- [ ] Timer visible during recording
- [ ] Water bottle nearby (stay hydrated!)

---

## Final Quality Check

Before publishing, verify:

- ✅ Audio is clear and consistent
- ✅ All text is readable
- ✅ No typos in on-screen text
- ✅ Transitions are smooth
- ✅ Total duration is 2:50-3:10
- ✅ No background noise
- ✅ Lighting is adequate (if on camera)
- ✅ Links work in description

---

**Good luck with your recording! 🎬**

Remember: The goal is to show value quickly and clearly. Focus on the problem you're solving and the time you're saving.

You've got this! 💪
