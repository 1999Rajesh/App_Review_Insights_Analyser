from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime, timedelta
import uuid
from app.models.review import Review, WeeklyReport, ThemeAnalysis
from app.services.gemini_analyzer import GeminiAnalyzer
from app.routes.reviews import reviews_db, reports_db

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/generate-weekly-report")
async def generate_weekly_report() -> WeeklyReport:
    """
    Generate a weekly pulse report from uploaded reviews.
    
    Returns:
        Generated weekly report with top themes, quotes, and action ideas
    """
    if not reviews_db:
        raise HTTPException(
            status_code=400, 
            detail="No reviews uploaded. Please upload CSV files first."
        )
    
    try:
        # Initialize analyzer with Gemini (Phase 3)
        analyzer = GeminiAnalyzer()
        
        # Use maximum 200 reviews for classification (as per hint)
        reviews_to_analyze = reviews_db[:200] if len(reviews_db) > 200 else reviews_db
        
        # Analyze themes
        analysis_result = await analyzer.analyze_themes(
            reviews_to_analyze,
            max_themes=5
        )
        
        themes = analysis_result['themes']
        total_analyzed = analysis_result.get('total_reviews', len(reviews_to_analyze))
        
        # Convert theme dictionaries to ThemeAnalysis objects
        from app.models.review import ThemeAnalysis, SentimentType
        theme_objects = []
        for theme_data in themes:
            try:
                theme_obj = ThemeAnalysis(
                    theme_name=theme_data['theme_name'],
                    review_count=theme_data['review_count'],
                    percentage=theme_data['percentage'],
                    sentiment=SentimentType(theme_data['sentiment']),
                    quotes=theme_data['quotes'],
                    action_ideas=theme_data['action_ideas']
                )
                theme_objects.append(theme_obj)
            except Exception as e:
                print(f"Warning: Could not create ThemeAnalysis object: {e}")
                continue
        
        themes = theme_objects[:3]  # Top 3 themes
        
        # Calculate date range (most recent week)
        review_dates = [r.date for r in reviews_db]
        week_end = max(review_dates)
        week_start = week_end - timedelta(days=6)
        
        # Create report ID
        report_id = f"report_{uuid.uuid4().hex[:8]}"
        
        # Count words in the themes
        estimated_word_count = sum(
            len(theme.theme_name.split()) +
            len(str(theme.quotes).split()) +
            len(str(theme.action_ideas).split())
            for theme in themes
        )
        
        # Create report
        report = WeeklyReport(
            id=report_id,
            week_start=week_start,
            week_end=week_end,
            total_reviews=total_analyzed,
            top_themes=themes[:3],  # Top 3 themes only
            generated_at=datetime.now(),
            word_count=estimated_word_count
        )
        
        # Store in database
        reports_db.append(report)
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("/themes")
async def get_all_themes() -> Dict:
    """
    Get all identified themes from reviews.
    
    Returns:
        Dictionary of themes and their details
    """
    if not reports_db:
        raise HTTPException(
            status_code=404,
            detail="No reports generated yet. Generate a weekly report first."
        )
    
    latest_report = max(reports_db, key=lambda r: r.generated_at)
    
    return {
        "report_id": latest_report.id,
        "generated_at": latest_report.generated_at.isoformat(),
        "themes": [theme.model_dump() for theme in latest_report.top_themes]
    }
