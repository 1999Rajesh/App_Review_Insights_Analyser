"""
Simple test to verify google-play-scraper is working
"""

from google_play_scraper import reviews_all, Sort

# Test with Groww app
app_id = "in.groww"

print(f"Testing google-play-scraper with app: {app_id}")
print("=" * 60)

try:
    result = reviews_all(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=10  # Just fetch 10 for testing
    )
    
    print(f"✅ Successfully fetched {len(result)} reviews")
    
    if result:
        print(f"\nFirst review:")
        first_review = result[0]
        print(f"   Review ID: {first_review.get('reviewId')}")
        print(f"   Score: {first_review.get('score')}/5")
        print(f"   Content: {first_review.get('content', '')[:100]}...")
        print(f"   Date: {first_review.get('at')}")
    else:
        print("⚠️ No reviews returned (app might not have recent reviews)")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Also test with WhatsApp as backup
print("\n" + "=" * 60)
print("Testing with WhatsApp (com.whatsapp) as backup...")
print("=" * 60)

try:
    result = reviews_all(
        "com.whatsapp",
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=5
    )
    
    print(f"✅ Successfully fetched {len(result)} reviews from WhatsApp")
    
    if result:
        print(f"\nFirst review:")
        first_review = result[0]
        print(f"   Review ID: {first_review.get('reviewId')}")
        print(f"   Score: {first_review.get('score')}/5")
        print(f"   Content: {first_review.get('content', '')[:100]}...")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
