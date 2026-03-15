from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import os
import aiofiles
from app.models.review import Review, WeeklyReport
from app.services.review_importer import ReviewImporter
from app.utils.pii_remover import sanitize_reviews
from app.services.groq_analyzer import GroqAnalyzer
from app.services.email_sender import EmailSender
from app.services.google_play_scraper import get_play_scraper
from app.config import settings

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

# In-memory storage (replace with database in production)
reviews_db: List[Review] = []
reports_db: List[WeeklyReport] = []


@router.post("/upload")
async def upload_reviews(
    app_store_file: Optional[UploadFile] = File(None),
    play_store_file: Optional[UploadFile] = File(None)
) -> Dict:
    """
    Upload review CSV files from App Store and/or Play Store.
    
    Args:
        app_store_file: CSV file from Apple App Store
        play_store_file: CSV file from Google Play Store
        
    Returns:
        Summary of uploaded reviews
    """
    global reviews_db
    
    if not app_store_file and not play_store_file:
        raise HTTPException(
            status_code=400, 
            detail="At least one CSV file must be uploaded"
        )
    
    try:
        importer = ReviewImporter()
        file_paths = {}
        temp_dir = "temp_uploads"
        
        # Create temp directory
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded files temporarily
        if app_store_file:
            app_store_path = os.path.join(temp_dir, f"app_store_{uuid.uuid4()}.csv")
            async with aiofiles.open(app_store_path, 'wb') as out_file:
                content = await app_store_file.read()
                await out_file.write(content)
            file_paths['app_store'] = app_store_path
        
        if play_store_file:
            play_store_path = os.path.join(temp_dir, f"play_store_{uuid.uuid4()}.csv")
            async with aiofiles.open(play_store_path, 'wb') as out_file:
                content = await play_store_file.read()
                await out_file.write(content)
            file_paths['play_store'] = play_store_path
        
        # Import reviews
        new_reviews = importer.import_from_multiple_sources(
            file_paths, 
            weeks=settings.REVIEW_WEEKS_RANGE
        )
        
        # Remove PII
        sanitized_data = sanitize_reviews([r.model_dump() for r in new_reviews])
        cleaned_reviews = [Review(**data) for data in sanitized_data]
        
        # Add to database
        reviews_db.extend(cleaned_reviews)
        
        # Clean up temp files
        for path in file_paths.values():
            if os.path.exists(path):
                os.remove(path)
        
        return {
            "message": "Reviews uploaded successfully",
            "app_store_count": len([r for r in cleaned_reviews if r.source == "App Store"]),
            "play_store_count": len([r for r in cleaned_reviews if r.source == "Play Store"]),
            "total_reviews": len(cleaned_reviews),
            "total_in_database": len(reviews_db),
            "date_range_weeks": settings.REVIEW_WEEKS_RANGE
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")


@router.get("/")
async def get_reviews(
    source: Optional[str] = None,
    limit: int = 100
) -> List[Review]:
    """
    Get uploaded reviews with optional filtering.
    
    Args:
        source: Filter by source ("App Store" or "Play Store")
        limit: Maximum number of reviews to return
        
    Returns:
        List of reviews
    """
    filtered = reviews_db
    
    if source:
        filtered = [r for r in reviews_db if r.source == source]
    
    return filtered[:limit]


@router.delete("/")
async def delete_reviews() -> Dict:
    """Clear all uploaded reviews from database"""
    global reviews_db
    reviews_db = []
    return {"message": "All reviews deleted successfully"}


@router.get("/stats")
async def get_review_stats() -> Dict:
    """Get summary statistics of uploaded reviews"""
    if not reviews_db:
        return {
            "total": 0,
            "app_store": 0,
            "play_store": 0,
            "average_rating": 0,
            "date_range": None
        }
    
    avg_rating = sum(r.rating for r in reviews_db) / len(reviews_db)
    dates = [r.date for r in reviews_db]
    
    return {
        "total": len(reviews_db),
        "app_store": len([r for r in reviews_db if r.source == "App Store"]),
        "play_store": len([r for r in reviews_db if r.source == "Play Store"]),
        "average_rating": round(avg_rating, 2),
        "oldest_review": min(dates).isoformat(),
        "newest_review": max(dates).isoformat()
    }


@router.post("/import-sample-data")
async def import_sample_data(weeks: int = 8) -> Dict:
    """
    Manually trigger import of sample review data from sample_data directory.
    This endpoint can be used to reload sample data at any time.
    
    Args:
        weeks: Number of weeks to look back (default: 8)
        
    Returns:
        Summary of imported reviews
    """
    global reviews_db
    
    try:
        importer = ReviewImporter()
        sample_reviews = importer.auto_import_sample_data(weeks=weeks)
        
        if not sample_reviews:
            raise HTTPException(
                status_code=404,
                detail="No sample review files found in sample_data directory"
            )
        
        # Add to database
        reviews_db.extend(sample_reviews)
        
        return {
            "message": "Sample data imported successfully",
            "app_store_count": len([r for r in sample_reviews if r.source == "App Store"]),
            "play_store_count": len([r for r in sample_reviews if r.source == "Play Store"]),
            "total_imported": len(sample_reviews),
            "total_in_database": len(reviews_db),
            "date_range_weeks": weeks
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing sample data: {str(e)}")


@router.post("/fetch-play-store")
async def fetch_play_store_reviews(
    weeks: int = Body(default=8, description="Number of weeks to look back"),
    max_reviews: int = Body(default=500, description="Maximum number of reviews to fetch"),
    recipient_name: Optional[str] = Body(None, description="Recipient name for email"),
    recipient_email: Optional[str] = Body(None, description="Recipient email for email")
) -> Dict:
    """
    Fetch reviews directly from Google Play Store.
    Uses configured app ID from environment variables.
    No CSV upload required!
    
    Args:
        weeks: Weeks to look back
        max_reviews: Max reviews to fetch
        recipient_name: Optional recipient name
        recipient_email: Optional recipient email
        
    Returns:
        Summary of fetched reviews
    """
    global reviews_db
    
    try:
        # Use configured app ID from environment
        app_id = settings.PLAY_STORE_DEFAULT_APP_ID
        country = settings.PLAY_STORE_COUNTRY
        language = settings.PLAY_STORE_LANGUAGE
        
        # Validate app_id format
        scraper = get_play_scraper()
        if not scraper.validate_app_id(app_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid configured app_id format. Check PLAY_STORE_DEFAULT_APP_ID in environment"
            )
        
        # Fetch reviews
        play_reviews = await scraper.fetch_reviews(
            app_id=app_id,
            weeks=weeks,
            max_reviews=max_reviews,
            country=country,
            language=language
        )
        
        if not play_reviews:
            return {
                "message": "No reviews found matching criteria",
                "fetched_count": 0,
                "play_store_count": 0,
                "total_in_database": len(reviews_db)
            }
        
        # Remove PII
        sanitized_data = sanitize_reviews([r.model_dump() for r in play_reviews])
        cleaned_reviews = [Review(**data) for data in sanitized_data]
        
        # Add to database
        reviews_db.extend(cleaned_reviews)
        
        return {
            "message": f"Successfully fetched {len(cleaned_reviews)} reviews from Google Play Store",
            "app_id": app_id,
            "fetched_count": len(cleaned_reviews),
            "play_store_count": len(cleaned_reviews),
            "total_in_database": len(reviews_db),
            "weeks": weeks,
            "max_reviews_requested": max_reviews,
            "recipient_name": recipient_name,
            "recipient_email": recipient_email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Play Store reviews: {str(e)}")


@router.get("/settings")
async def get_settings() -> Dict:
    """Get current application settings"""
    return {
        "review_weeks_range": settings.REVIEW_WEEKS_RANGE,
        "max_reviews_to_fetch": settings.MAX_REVIEWS_TO_FETCH,
        "max_themes": settings.MAX_THEMES,
        "max_words": settings.MAX_WORDS,
        "play_store_country": settings.PLAY_STORE_COUNTRY,
        "play_store_language": settings.PLAY_STORE_LANGUAGE,
        "scheduler_interval_minutes": settings.SCHEDULER_INTERVAL_MINUTES
    }


@router.post("/settings")
async def update_settings(settings_update: Dict) -> Dict:
    """
    Update application settings.
    Note: Changes are temporary and will reset on server restart.
    For permanent changes, update .env file.
    """
    global settings
    
    updated_fields = []
    
    # Update settings that were provided
    if "review_weeks_range" in settings_update:
        settings.REVIEW_WEEKS_RANGE = int(settings_update["review_weeks_range"])
        updated_fields.append("review_weeks_range")
    
    if "max_reviews_to_fetch" in settings_update:
        settings.MAX_REVIEWS_TO_FETCH = int(settings_update["max_reviews_to_fetch"])
        updated_fields.append("max_reviews_to_fetch")
    
    if "max_themes" in settings_update:
        settings.MAX_THEMES = int(settings_update["max_themes"])
        updated_fields.append("max_themes")
    
    if "max_words" in settings_update:
        settings.MAX_WORDS = int(settings_update["max_words"])
        updated_fields.append("max_words")
    
    if "play_store_country" in settings_update:
        settings.PLAY_STORE_COUNTRY = settings_update["play_store_country"]
        updated_fields.append("play_store_country")
    
    if "play_store_language" in settings_update:
        settings.PLAY_STORE_LANGUAGE = settings_update["play_store_language"]
        updated_fields.append("play_store_language")
    
    return {
        "message": "Settings updated successfully",
        "updated_fields": updated_fields,
        "current_settings": {
            "review_weeks_range": settings.REVIEW_WEEKS_RANGE,
            "max_reviews_to_fetch": settings.MAX_REVIEWS_TO_FETCH,
            "max_themes": settings.MAX_THEMES,
            "max_words": settings.MAX_WORDS,
            "play_store_country": settings.PLAY_STORE_COUNTRY,
            "play_store_language": settings.PLAY_STORE_LANGUAGE,
            "scheduler_interval_minutes": settings.SCHEDULER_INTERVAL_MINUTES
        }
    }
