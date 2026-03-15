"""
Play Store Review Scraper Service
Fetches reviews from Google Play Store with PII protection and quality filtering.
"""

from google_play_scraper import Sort, reviews_all
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for consistent language detection
DetectorFactory.seed = 0


class PlayStoreScraper:
    """Service for scraping and filtering Play Store reviews."""
    
    def __init__(self):
        # Configuration from environment or defaults
        self.app_id = os.getenv('PLAY_STORE_DEFAULT_APP_ID', 'com.nextbillion.groww')
        self.lang = os.getenv('PLAY_STORE_LANGUAGE', 'en')
        self.country = os.getenv('PLAY_STORE_COUNTRY', 'in')
        self.max_reviews = int(os.getenv('MAX_REVIEWS_TO_FETCH', '500'))
        self.weeks_back = int(os.getenv('REVIEW_WEEKS_RANGE', '8'))
        
        # Quality filters
        self.min_word_count = int(os.getenv('MIN_REVIEW_WORD_COUNT', '5'))
        self.allow_emojis = os.getenv('ALLOW_EMOJIS', 'false').lower() == 'true'
        self.required_language = os.getenv('REQUIRED_LANGUAGE', 'en')
        
        # Storage
        self.data_dir = os.getenv('REVIEWS_DATA_DIR', 'data/reviews')
        
        # PII patterns (comprehensive list)
        self.pii_patterns = [
            # Email addresses
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
            
            # Phone numbers (various formats)
            (r'\b\d{10}\b', '[PHONE_REDACTED]'),  # 10 digits
            (r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '[PHONE_REDACTED]'),  # XXX-XXX-XXXX
            
            # Credit/debit card numbers
            (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD_REDACTED]'),
            
            # Indian PAN card
            (r'\b[A-Z]{5}\d{4}[A-Z]\b', '[PAN_REDACTED]'),
            
            # Aadhaar number (12 digits)
            (r'\b\d{12}\b', '[AADHAAR_REDACTED]'),
            
            # URLs
            (r'https?://\S+', '[URL_REDACTED]'),
            
            # IP addresses
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_REDACTED]'),
        ]
        
        # Emoji pattern (comprehensive unicode ranges)
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"  # dingbats
            u"\U000024C2-\U0001F251"  # enclosed characters
            "]+", flags=re.UNICODE)
    
    def has_emoji(self, text: str) -> bool:
        """Check if text contains emojis."""
        return bool(self.emoji_pattern.search(text))
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def is_english(self, text: str) -> bool:
        """Detect if text is in English."""
        try:
            return detect(text) == self.required_language
        except LangDetectException:
            # If detection fails, assume it's not the required language
            return False
    
    def remove_pii(self, text: str) -> str:
        """Remove PII from text by replacing with redaction markers."""
        cleaned = text
        for pattern, replacement in self.pii_patterns:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        return cleaned
    
    def should_keep_review(self, review_text: str) -> tuple[bool, str]:
        """
        Apply quality filters to determine if review should be kept.
        Returns (should_keep, reason)
        """
        # Check word count
        word_count = self.count_words(review_text)
        if word_count < self.min_word_count:
            return False, f"Too few words ({word_count} < {self.min_word_count})"
        
        # Check for emojis (if not allowed)
        if not self.allow_emojis and self.has_emoji(review_text):
            return False, "Contains emoji"
        
        # Check language
        if not self.is_english(review_text):
            return False, "Not in English"
        
        return True, "Passed all filters"
    
    def filter_by_date(self, reviews: List[Dict], weeks: int) -> List[Dict]:
        """Keep only reviews from last N weeks."""
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        filtered = []
        
        for review in reviews:
            review_date = review.get('at')
            
            # Handle both datetime objects and strings
            if isinstance(review_date, datetime):
                if review_date >= cutoff_date:
                    filtered.append(review)
            elif isinstance(review_date, str):
                try:
                    # Try to parse ISO format string
                    date_obj = datetime.fromisoformat(review_date.replace('Z', '+00:00'))
                    if date_obj.replace(tzinfo=None) >= cutoff_date:
                        filtered.append(review)
                except ValueError:
                    # If parsing fails, skip this review
                    continue
        
        return filtered
    
    async def fetch_and_store(self, weeks: Optional[int] = None, 
                             max_reviews: Optional[int] = None) -> Dict:
        """
        Main method to fetch reviews from Play Store and store them.
        
        Args:
            weeks: Number of weeks to look back (optional, uses config default)
            max_reviews: Maximum reviews to fetch (optional, uses config default)
            
        Returns:
            Dictionary with metadata about the scrape operation
            
        Raises:
            SystemExit: On any error (exits with code 1)
        """
        weeks = weeks or self.weeks_back
        max_reviews = max_reviews or self.max_reviews
        
        print(f"🚀 Starting Play Store scrape for app: {self.app_id}")
        print(f"📊 Fetching up to {max_reviews} reviews from last {weeks} weeks")
        
        try:
            # Step 1: Fetch reviews from Play Store
            print("⏳ Fetching reviews from Google Play Store...")
            result = reviews_all(
                self.app_id,
                lang=self.lang,
                country=self.country,
                sort=Sort.NEWEST,
                count=max_reviews
            )
            
            # Convert to dict format (result is already a list)
            reviews_dict = [dict(r) for r in result]
            print(f"✅ Fetched {len(reviews_dict)} raw reviews")
            
            if not reviews_dict:
                print("⚠️  No reviews found matching criteria")
                return {
                    'success': True,
                    'reviews_fetched': 0,
                    'message': 'No reviews found',
                    'metadata': {}
                }
            
            # Step 2: Filter by date
            print(f"📅 Filtering by date (last {weeks} weeks)...")
            filtered_reviews = self.filter_by_date(reviews_dict, weeks)
            print(f"✅ After date filter: {len(filtered_reviews)} reviews")
            
            # Step 3: Apply quality filters and PII removal
            print("🔍 Applying quality filters and PII removal...")
            clean_reviews = []
            filter_stats = {
                'too_short': 0,
                'has_emoji': 0,
                'wrong_language': 0,
                'pii_removed': 0
            }
            
            for review in filtered_reviews:
                text = review.get('content', '')
                
                # Apply quality filters
                keep, reason = self.should_keep_review(text)
                
                if not keep:
                    if 'Too few words' in reason:
                        filter_stats['too_short'] += 1
                    elif 'emoji' in reason:
                        filter_stats['has_emoji'] += 1
                    elif 'language' in reason:
                        filter_stats['wrong_language'] += 1
                    continue
                
                # Remove PII
                original_text = text
                review['content'] = self.remove_pii(text)
                if original_text != review['content']:
                    filter_stats['pii_removed'] += 1
                
                # Don't store title (privacy consideration)
                if 'title' in review:
                    del review['title']
                
                clean_reviews.append(review)
            
            print(f"✅ After quality filters: {len(clean_reviews)} reviews")
            print(f"   - Too short: {filter_stats['too_short']}")
            print(f"   - Has emoji: {filter_stats['has_emoji']}")
            print(f"   - Wrong language: {filter_stats['wrong_language']}")
            print(f"   - PII removed: {filter_stats['pii_removed']}")
            
            # Step 4: Prepare output
            today = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(self.data_dir, exist_ok=True)
            output_file = os.path.join(self.data_dir, f'{today}.json')
            
            # Calculate date range
            earliest_review = min([r.get('at') for r in clean_reviews if r.get('at')]) if clean_reviews else None
            latest_review = max([r.get('at') for r in clean_reviews if r.get('at')]) if clean_reviews else None
            
            metadata = {
                'scrapedAt': datetime.now().isoformat(),
                'packageId': self.app_id,
                'weeksRequested': weeks,
                'totalFetched': len(reviews_dict),
                'afterDateFilter': len(filtered_reviews),
                'totalAfterFilters': len(clean_reviews),
                'filterStats': filter_stats,
                'dateRange': {
                    'from': earliest_review.isoformat() if earliest_review else None,
                    'to': latest_review.isoformat() if latest_review else None
                },
                'configuration': {
                    'language': self.lang,
                    'country': self.country,
                    'minWordCount': self.min_word_count,
                    'allowEmojis': self.allow_emojis,
                    'requiredLanguage': self.required_language
                }
            }
            
            output_data = {
                'metadata': metadata,
                'reviews': clean_reviews
            }
            
            # Step 5: Write to file (CRITICAL: All or nothing - no partial writes)
            print(f"💾 Writing to {output_file}...")
            temp_file = output_file + '.tmp'
            
            try:
                # Write to temp file first
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                # Atomically rename to final name
                os.replace(temp_file, output_file)
                
                print(f"✅ Successfully saved {len(clean_reviews)} reviews")
                print(f"📁 File: {output_file}")
                
                return {
                    'success': True,
                    'reviews_fetched': len(clean_reviews),
                    'file_path': output_file,
                    'metadata': metadata
                }
                
            except IOError as e:
                # Clean up temp file if it exists
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                raise e
            
        except Exception as e:
            # CRITICAL: On ANY error, log and exit with non-zero code
            # Do NOT write partial data
            error_msg = f"❌ Error fetching reviews: {str(e)}"
            print(error_msg)
            print("🚨 Exiting with error code 1 - NO partial data written")
            raise SystemExit(1)
