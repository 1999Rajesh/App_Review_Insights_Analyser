"""
Google Play Store Review Scraper

Automatically fetch reviews from Google Play Store using google-play-scraper.
No manual CSV upload required!
"""

import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from google_play_scraper import Sort, reviews_all
import uuid

from app.models.review import Review

logger = logging.getLogger(__name__)


class GooglePlayScraper:
    """Scrape reviews directly from Google Play Store"""
    
    def __init__(self):
        self.default_country = 'us'
        self.default_language = 'en'
    
    async def fetch_reviews(
        self,
        app_id: str,
        weeks: int = 8,
        max_reviews: int = 500,
        country: str = 'us',
        language: str = 'en'
    ) -> List[Review]:
        """
        Fetch reviews from Google Play Store.
        
        Args:
            app_id: Google Play Store app ID (e.g., com.example.app)
            weeks: Number of weeks to look back
            max_reviews: Maximum number of reviews to fetch
            country: Country code
            language: Language code
            
        Returns:
            List of Review objects
        """
        try:
            logger.info(f"📱 Fetching reviews for app: {app_id}")
            logger.info(f"📊 Max reviews: {max_reviews}, Weeks: {weeks}")
            
            # Calculate date threshold
            date_threshold = datetime.now() - timedelta(weeks=weeks)
            
            # Run synchronous google_play_scraper in executor
            loop = asyncio.get_event_loop()
            
            # Fetch reviews (google_play_scraper is synchronous)
            result = await loop.run_in_executor(
                None,
                lambda: reviews_all(
                    app_id,
                    lang=language,
                    country=country,
                    sort=Sort.NEWEST,
                    count=max_reviews
                )
            )
            
            if not result or len(result) == 0:
                logger.warning(f"No reviews found for app: {app_id}")
                return []
            
            logger.info(f"✅ Fetched {len(result)} raw reviews from Play Store")
            
            # Filter by date and convert to Review objects
            filtered_reviews = []
            for review_data in result:
                try:
                    # Parse review date
                    review_date = review_data.get('at')
                    if not review_date:
                        continue
                    
                    # Check if within date range
                    if review_date < date_threshold:
                        continue
                    
                    # Create Review object
                    review_text = review_data.get('content', '')
                    
                    # Skip reviews with less than 5 words
                    if len(review_text.split()) < 5:
                        continue
                    
                    review = Review(
                        id=str(uuid.uuid4()),
                        source="Play Store",
                        rating=int(review_data.get('score', 0)),
                        title='',  # Play Store doesn't always have titles
                        text=review_text,
                        date=review_date
                    )
                    filtered_reviews.append(review)
                    
                except Exception as e:
                    logger.error(f"Error processing review: {str(e)}")
                    continue
            
            logger.info(f"✅ Filtered to {len(filtered_reviews)} reviews from last {weeks} weeks")
            return filtered_reviews
            
        except Exception as e:
            logger.error(f"Failed to fetch Play Store reviews: {str(e)}", exc_info=True)
            raise Exception(f"Play Store scraping failed: {str(e)}")
    
    def validate_app_id(self, app_id: str) -> bool:
        """
        Validate Google Play Store app ID format.
        
        Example valid IDs:
        - com.whatsapp
        - com.instagram.android
        - com.spotify.music
        
        Args:
            app_id: App ID to validate
            
        Returns:
            True if valid format
        """
        import re
        pattern = r'^[a-z][a-z0-9_]+(\.[a-z0-9_]+)+$'
        return bool(re.match(pattern, app_id.lower()))


# Singleton instance
_google_play_scraper = None


def get_play_scraper() -> GooglePlayScraper:
    """Get the Google Play scraper instance"""
    global _google_play_scraper
    if _google_play_scraper is None:
        _google_play_scraper = GooglePlayScraper()
    return _google_play_scraper
