"""
Hybrid Weekly Review Collector

Fetches Groww app reviews from Play Store and saves in BOTH formats:
1. JSON format (for fast API/Frontend) - with PII removal & quality filters
2. Weekly CSV format (for human browsing) - raw reviews organized by week

Runs automatically every week to build 8-12 week dataset.
"""

import csv
import os
import json
from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews_all
from typing import List, Dict
import re


class HybridReviewCollector:
    """Collect Play Store reviews in hybrid JSON + CSV format"""
    
    def __init__(self):
        # App configuration
        self.app_id = os.getenv('PLAY_STORE_DEFAULT_APP_ID', 'com.nextbillion.groww')
        self.lang = os.getenv('PLAY_STORE_LANGUAGE', 'en')
        self.country = os.getenv('PLAY_STORE_COUNTRY', 'in')
        
        # Fetch limits
        self.max_reviews = int(os.getenv('MAX_REVIEWS_TO_FETCH', '500'))
        self.weeks_range = int(os.getenv('REVIEW_WEEKS_RANGE', '12'))
        
        # Quality filters
        self.min_word_count = int(os.getenv('MIN_REVIEW_WORD_COUNT', '5'))
        self.allow_emojis = os.getenv('ALLOW_EMOJIS', 'false').lower() == 'true'
        self.required_language = os.getenv('REQUIRED_LANGUAGE', 'en')
        
        # Output directories
        self.json_data_dir = os.getenv('REVIEWS_DATA_DIR', 'data/reviews')
        self.csv_data_dir = os.getenv('CSV_DATA_DIR', 'weekly_reviews')
        
        # PII patterns for redaction
        self.pii_patterns = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
            (r'\b\d{10}\b', '[PHONE_REDACTED]'),
            (r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '[PHONE_REDACTED]'),
            (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD_REDACTED]'),
            (r'\b[A-Z]{5}\d{4}[A-Z]\b', '[PAN_REDACTED]'),
            (r'\b\d{12}\b', '[AADHAAR_REDACTED]'),
            (r'https?://\S+', '[URL_REDACTED]'),
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_REDACTED]'),
        ]
        
        # Emoji pattern
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
    
    def has_emoji(self, text: str) -> bool:
        """Check if text contains emojis"""
        return bool(self.emoji_pattern.search(text))
    
    def count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    def remove_pii(self, text: str) -> str:
        """Remove PII from text"""
        cleaned = text
        for pattern, replacement in self.pii_patterns:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        return cleaned
    
    def is_english_review(self, text: str) -> bool:
        """Simple check if review appears to be in English"""
        try:
            from langdetect import detect
            return detect(text) == 'en'
        except:
            return True  # If detection fails, assume it's English
    
    def should_keep_review(self, review_text: str) -> tuple:
        """Apply quality filters"""
        # Check word count
        if self.count_words(review_text) < self.min_word_count:
            return False, "too_short"
        
        # Check emojis
        if not self.allow_emojis and self.has_emoji(review_text):
            return False, "has_emoji"
        
        # Check language (optional)
        if not self.is_english_review(review_text):
            return False, "wrong_language"
        
        return True, "passed"
    
    def fetch_reviews(self) -> List[Dict]:
        """Fetch reviews from Google Play Store"""
        print(f"🚀 Fetching reviews for {self.app_id}...")
        print(f"📊 Max reviews: {self.max_reviews}, Weeks: {self.weeks_range}")
        
        try:
            result = reviews_all(
                self.app_id,
                lang=self.lang,
                country=self.country,
                sort=Sort.NEWEST,
                count=self.max_reviews
            )
            
            print(f"✅ Fetched {len(result)} raw reviews")
            return [dict(r) for r in result]
            
        except Exception as e:
            print(f"❌ Error fetching reviews: {str(e)}")
            raise
    
    def filter_by_date(self, reviews: List[Dict], weeks: int) -> List[Dict]:
        """Keep only reviews from last N weeks"""
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        filtered = []
        
        for review in reviews:
            review_date = review.get('at')
            
            if isinstance(review_date, datetime):
                if review_date >= cutoff_date:
                    filtered.append(review)
            elif isinstance(review_date, str):
                try:
                    date_obj = datetime.fromisoformat(review_date.replace('Z', '+00:00'))
                    if date_obj.replace(tzinfo=None) >= cutoff_date:
                        filtered.append(review)
                except ValueError:
                    continue
        
        print(f"📅 After date filter ({weeks} weeks): {len(filtered)} reviews")
        return filtered
    
    def apply_quality_filters(self, reviews: List[Dict]) -> tuple:
        """Apply quality filters and PII removal"""
        print("🔍 Applying quality filters and PII removal...")
        
        clean_reviews = []
        filter_stats = {'too_short': 0, 'has_emoji': 0, 'wrong_language': 0, 'pii_removed': 0}
        
        for review in reviews:
            text = review.get('content', '')
            
            # Apply quality filters
            keep, reason = self.should_keep_review(text)
            
            if not keep:
                filter_stats[reason] = filter_stats.get(reason, 0) + 1
                continue
            
            # Remove PII
            original_text = text
            review['content'] = self.remove_pii(text)
            if original_text != review['content']:
                filter_stats['pii_removed'] += 1
            
            # Remove title for privacy
            if 'title' in review:
                del review['title']
            
            clean_reviews.append(review)
        
        print(f"✅ After quality filters: {len(clean_reviews)} reviews")
        print(f"   - Too short: {filter_stats['too_short']}")
        print(f"   - Has emoji: {filter_stats['has_emoji']}")
        print(f"   - Wrong language: {filter_stats['wrong_language']}")
        print(f"   - PII removed: {filter_stats['pii_removed']}")
        
        return clean_reviews, filter_stats
    
    def save_to_json(self, reviews: List[Dict], filter_stats: Dict) -> str:
        """Save reviews to JSON format (for API/Frontend)"""
        today = datetime.now().strftime('%Y-%m-%d')
        output_file = os.path.join(self.json_data_dir, f'{today}.json')
        
        os.makedirs(self.json_data_dir, exist_ok=True)
        
        # Calculate date range
        dates = [r.get('at') for r in reviews if r.get('at')]
        earliest = min(dates) if dates else None
        latest = max(dates) if dates else None
        
        metadata = {
            'scrapedAt': datetime.now().isoformat(),
            'packageId': self.app_id,
            'weeksRequested': self.weeks_range,
            'totalFetched': self.max_reviews,
            'afterDateFilter': len(reviews),
            'totalAfterFilters': len(reviews),
            'filterStats': filter_stats,
            'dateRange': {
                'from': earliest.isoformat() if earliest else None,
                'to': latest.isoformat() if latest else None
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
            'reviews': reviews
        }
        
        # Write to temp file first, then rename (atomic operation)
        temp_file = output_file + '.tmp'
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            os.replace(temp_file, output_file)
            
            print(f"💾 Saved JSON to {output_file}")
            return output_file
            
        except IOError as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise e
    
    def save_to_weekly_csv(self, reviews: List[Dict]) -> str:
        """Save reviews to weekly CSV format (for human browsing)"""
        week_number = datetime.now().isocalendar()[1]
        year = datetime.now().year
        
        os.makedirs(self.csv_data_dir, exist_ok=True)
        
        filename = f"{self.csv_data_dir}/reviews_{year}_week_{week_number}.csv"
        
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["review_id", "score", "content", "date"])
            
            for idx, r in enumerate(reviews, start=1):
                review_id = r.get('reviewId', f'review_{idx}')
                score = r.get('score', 0)
                content = r.get('content', '')
                date = r.get('at')
                
                # Convert datetime to string if needed
                if isinstance(date, datetime):
                    date = date.strftime('%Y-%m-%d %H:%M:%S')
                
                writer.writerow([review_id, score, content, date])
        
        print(f"✅ Saved CSV to {filename}")
        return filename
    
    def collect(self) -> Dict:
        """Main method to collect reviews in hybrid format"""
        print("=" * 60)
        print("🔄 HYBRID REVIEW COLLECTOR")
        print("=" * 60)
        
        try:
            # Step 1: Fetch reviews
            raw_reviews = self.fetch_reviews()
            
            if not raw_reviews:
                print("⚠️ No reviews found")
                return {'success': True, 'message': 'No reviews found'}
            
            # Step 2: Filter by date (last 8-12 weeks)
            date_filtered = self.filter_by_date(raw_reviews, self.weeks_range)
            
            if not date_filtered:
                print("⚠️ No reviews in date range")
                return {'success': True, 'message': 'No reviews in date range'}
            
            # Step 3: Apply quality filters and PII removal
            clean_reviews, filter_stats = self.apply_quality_filters(date_filtered)
            
            if not clean_reviews:
                print("⚠️ No reviews after quality filters")
                return {'success': True, 'message': 'No reviews after filters'}
            
            # Step 4: Save in BOTH formats (HYBRID)
            json_file = self.save_to_json(clean_reviews, filter_stats)
            csv_file = self.save_to_weekly_csv(clean_reviews)
            
            print("=" * 60)
            print("✅ COLLECTION COMPLETE")
            print("=" * 60)
            print(f"📄 JSON file (API-ready): {json_file}")
            print(f"📊 CSV file (Human-readable): {csv_file}")
            print(f"🎯 Total clean reviews: {len(clean_reviews)}")
            print("=" * 60)
            
            return {
                'success': True,
                'reviews_collected': len(clean_reviews),
                'json_file': json_file,
                'csv_file': csv_file,
                'filter_stats': filter_stats
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise


def main():
    """Entry point for running the hybrid collector"""
    collector = HybridReviewCollector()
    result = collector.collect()
    
    if result['success']:
        print("\n🎉 Successfully collected reviews!")
        print(f"   Reviews: {result.get('reviews_collected', 0)}")
        print(f"   JSON: {result.get('json_file')}")
        print(f"   CSV: {result.get('csv_file')}")
    else:
        print(f"\n⚠️ {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()
