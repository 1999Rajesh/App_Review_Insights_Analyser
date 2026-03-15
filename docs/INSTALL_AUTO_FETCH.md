# ⚡ Quick Install - Auto-Fetch Feature

## Step 1: Install Python Package

Open terminal in backend directory:

```bash
cd c:\Users\Rajesh\Documents\App_Review_Insights_Analyser\backend
pip install google-play-scraper==1.2.4
```

**Or update all dependencies:**
```bash
pip install -r requirements.txt
```

---

## Step 2: Restart Backend Server

Stop current server (Ctrl+C) and restart:

```bash
python -m uvicorn app.main:app --reload
```

**Look for this in logs:**
```
✅ Google Play scraper loaded
```

---

## Step 3: Test the Feature

1. Open frontend: http://localhost:3000
2. Look for **"🤖 Auto-Fetch from Google Play Store"** section
3. Enter test app ID: `com.whatsapp`
4. Click **"🚀 Fetch Play Store Reviews"**
5. Wait 5-10 seconds
6. See success message!

---

## Step 4: Configure Settings (Optional)

Click **⚙️ Settings** button (top-right):

**Recommended defaults:**
- Weeks: 8
- Max Reviews: 500
- Country: us (or your country)
- Language: en

**Save settings** and they'll apply to all future fetches!

---

## ✅ You're Ready!

Now you can:
- ✅ Auto-fetch Play Store reviews (no CSV needed!)
- ✅ Still upload CSVs manually if needed
- ✅ Adjust settings on the fly
- ✅ Generate reports automatically

---

## 🎯 Try These Popular Apps:

| App | App ID |
|-----|--------|
| WhatsApp | `com.whatsapp` |
| Instagram | `com.instagram.android` |
| Spotify | `com.spotify.music` |
| Telegram | `org.telegram.messenger` |
| Snapchat | `com.snapchat.android` |

---

## 🐛 Issues?

### "Module not found" error:
```bash
pip install google-play-scraper==1.2.4
```

### "Invalid app ID" error:
- Must be lowercase
- Example format: `com.example.app`

### No reviews fetched:
- Try different app (WhatsApp always has reviews)
- Increase max_reviews limit
- Expand weeks range

---

**Need help?** Check `AUTO_FETCH_PLAY_STORE.md` for detailed guide!
