"""
Test script to fetch Groww app reviews from Google Play Store
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.google_play_scraper import get_play_scraper


async def fetch_groww_reviews():
    """Fetch Groww app reviews for testing"""
    
    print("=" * 60)
    print("🚀 Fetching Groww App Reviews from Google Play Store")
    print("=" * 60)
    
    try:
        scraper = get_play_scraper()
        
        print("\n📱 Configuration:")
        print(f"   App ID: in.groww")
        print(f"   Country: United States (us) - Trying US store")
        print(f"   Language: English (en)")
        print(f"   Weeks: 8")
        print(f"   Max Reviews: 500")
        
        # Try US store first as it's more accessible
        reviews = await scraper.fetch_reviews(
            app_id='in.groww',
            weeks=8,
            max_reviews=500,
            country='us',
            language='en'
        )
        
        if not reviews:
            print("\n⚠️  No reviews found!")
            return None
        
        print(f"\n✅ Successfully fetched {len(reviews)} reviews!")
        
        # Show sample review
        if len(reviews) > 0:
            sample = reviews[0]
            print(f"\n📊 Sample Review:")
            print(f"   Rating: {sample.rating} stars")
            print(f"   Date: {sample.date.strftime('%Y-%m-%d')}")
            print(f"   Text (first 100 chars): {sample.text[:100]}...")
        
        print(f"\n📈 Statistics:")
        print(f"   5-star reviews: {len([r for r in reviews if r.rating == 5])}")
        print(f"   4-star reviews: {len([r for r in reviews if r.rating == 4])}")
        print(f"   3-star reviews: {len([r for r in reviews if r.rating == 3])}")
        print(f"   2-star reviews: {len([r for r in reviews if r.rating == 2])}")
        print(f"   1-star reviews: {len([r for r in reviews if r.rating == 1])}")
        
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        print(f"\n⭐ Average Rating: {avg_rating:.2f}/5.0")
        
        return reviews
        
    except Exception as e:
        print(f"\n❌ Error fetching reviews: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    reviews = asyncio.run(fetch_groww_reviews())
    
    if reviews:
        print("\n" + "=" * 60)
        print("✅ Groww review fetch test completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Test failed - no reviews fetched")
        print("=" * 60)
