from typing import List, Dict
import pandas as pd
from datetime import datetime, timedelta
import logging
from app.models.review import Review


class ReviewImporter:
    """Import and normalize app reviews from CSV files"""
    
    def __init__(self):
        self.required_columns = ['date', 'rating', 'title', 'text']
    
    def parse_app_store_csv(self, filepath: str) -> List[Review]:
        """
        Parse Apple App Store CSV format.
        
        Expected columns: Date, Rating, Title, Review
        
        Args:
            filepath: Path to App Store CSV file
            
        Returns:
            List of Review objects
        """
        df = pd.read_csv(filepath)
        
        # Map App Store columns to standard format
        column_mapping = {
            'Date': 'date',
            'Rating': 'rating', 
            'Title': 'title',
            'Review': 'text'
        }
        
        df = df.rename(columns=column_mapping)
        return self._normalize_dataframe(df, source="App Store")
    
    def parse_play_store_csv(self, filepath: str) -> List[Review]:
        """
        Parse Google Play Store CSV format.
        
        Expected columns: Date, Star Rating, Title, Text
        
        Args:
            filepath: Path to Play Store CSV file
            
        Returns:
            List of Review objects
        """
        df = pd.read_csv(filepath)
        
        # Map Play Store columns to standard format
        column_mapping = {
            'Date': 'date',
            'Star Rating': 'rating',
            'Title': 'title',
            'Text': 'text'
        }
        
        df = df.rename(columns=column_mapping)
        return self._normalize_dataframe(df, source="Play Store")
    
    def _normalize_dataframe(self, df: pd.DataFrame, source: str) -> List[Review]:
        """
        Standardize DataFrame into unified Review model.
        
        Args:
            df: DataFrame with standardized column names
            source: Source platform (App Store or Play Store)
            
        Returns:
            List of Review objects
        """
        import uuid
        
        # Validate required columns
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Ensure rating is integer
        df['rating'] = df['rating'].astype(int)
        
        # Fill NaN values with empty strings
        df['title'] = df['title'].fillna('')
        df['text'] = df['text'].fillna('')
        
        # Filter out reviews with less than 5 words in text
        df = df[df['text'].apply(lambda x: len(str(x).split()) >= 5)]
        
        # Create Review objects (title set to empty string as it's not required)
        reviews = []
        for _, row in df.iterrows():
            review = Review(
                id=str(uuid.uuid4()),
                source=source,
                rating=int(row['rating']),
                title='',  # Title not required, set to empty
                text=str(row['text']),
                date=row['date']
            )
            reviews.append(review)
        
        return reviews
    
    def filter_by_date_range(
        self, 
        reviews: List[Review], 
        weeks: int = 8
    ) -> List[Review]:
        """
        Filter reviews to only include recent ones within specified weeks.
        
        Args:
            reviews: List of reviews
            weeks: Number of weeks to look back (default: 8)
            
        Returns:
            Filtered list of reviews
        """
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        return [r for r in reviews if r.date >= cutoff_date]
    
    def import_from_multiple_sources(
        self, 
        file_paths: Dict[str, str],
        weeks: int = 8
    ) -> List[Review]:
        """
        Import reviews from multiple CSV files (both stores).
        
        Args:
            file_paths: Dict with keys 'app_store' and/or 'play_store'
            weeks: Number of weeks to look back
            
        Returns:
            Combined and filtered list of reviews
        """
        all_reviews = []
        
        if 'app_store' in file_paths:
            app_store_reviews = self.parse_app_store_csv(
                file_paths['app_store']
            )
            all_reviews.extend(app_store_reviews)
        
        if 'play_store' in file_paths:
            play_store_reviews = self.parse_play_store_csv(
                file_paths['play_store']
            )
            all_reviews.extend(play_store_reviews)
        
        # Filter by date range
        filtered_reviews = self.filter_by_date_range(all_reviews, weeks)
        
        return filtered_reviews
    
    def auto_import_sample_data(self, weeks: int = 8) -> List[Review]:
        """
        Automatically import sample review data from the sample_data directory.
        Looks for app_store_reviews.csv and play_store_reviews.csv files.
        
        Args:
            weeks: Number of weeks to look back
            
        Returns:
            Combined and filtered list of reviews from sample data
        """
        import os
        
        # Get the project root directory (parent of backend)
        # __file__ is in backend/app/services/review_importer.py
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        sample_data_dir = os.path.join(current_dir, 'sample_data')
        
        logger = logging.getLogger(__name__)
        logger.info(f"🔍 Looking for sample data in: {sample_data_dir}")
        logger.info(f"📁 Current directory exists: {os.path.exists(sample_data_dir)}")
        if os.path.exists(sample_data_dir):
            logger.info(f"📂 Files in sample_data: {os.listdir(sample_data_dir)}")
        all_reviews = []
        
        # Check for App Store sample data
        app_store_file = os.path.join(sample_data_dir, 'app_store_reviews.csv')
        if os.path.exists(app_store_file):
            try:
                logger.info(f"📂 Auto-importing App Store reviews from: {app_store_file}")
                app_store_reviews = self.parse_app_store_csv(app_store_file)
                all_reviews.extend(app_store_reviews)
                logger.info(f"✅ Loaded {len(app_store_reviews)} App Store reviews")
            except Exception as e:
                logger.error(f"Failed to load App Store sample data: {str(e)}")
        else:
            logger.warning(f"App Store sample file not found: {app_store_file}")
        
        # Check for Play Store sample data
        play_store_file = os.path.join(sample_data_dir, 'play_store_reviews.csv')
        if os.path.exists(play_store_file):
            try:
                logger.info(f"📂 Auto-importing Play Store reviews from: {play_store_file}")
                play_store_reviews = self.parse_play_store_csv(play_store_file)
                all_reviews.extend(play_store_reviews)
                logger.info(f"✅ Loaded {len(play_store_reviews)} Play Store reviews")
            except Exception as e:
                logger.error(f"Failed to load Play Store sample data: {str(e)}")
        else:
            logger.warning(f"Play Store sample file not found: {play_store_file}")
        
        # Filter by date range
        if all_reviews:
            filtered_reviews = self.filter_by_date_range(all_reviews, weeks)
            logger.info(f"📊 Total reviews loaded: {len(all_reviews)}, Filtered to last {weeks} weeks: {len(filtered_reviews)}")
            return filtered_reviews
        else:
            logger.warning("⚠️ No sample review files found in sample_data directory")
            return []
