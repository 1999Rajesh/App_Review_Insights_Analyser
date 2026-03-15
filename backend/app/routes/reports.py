from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Optional
from datetime import datetime
from app.models.review import WeeklyReport
from app.services.groq_analyzer import GroqAnalyzer
from app.services.email_sender import EmailSender
from app.routes.reviews import reports_db
from app.config import settings

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/latest")
async def get_latest_report() -> WeeklyReport:
    """
    Get the most recently generated weekly report.
    
    Returns:
        Latest weekly report
    """
    if not reports_db:
        raise HTTPException(
            status_code=404,
            detail="No reports available. Generate a weekly report first."
        )
    
    # Get most recent report
    latest_report = max(reports_db, key=lambda r: r.generated_at)
    return latest_report


@router.get("/")
async def get_all_reports() -> list[WeeklyReport]:
    """
    Get all generated weekly reports.
    
    Returns:
        List of all reports
    """
    return reports_db


@router.post("/generate-summary")
async def generate_summary_text(report_id: Optional[str] = None) -> Dict:
    """
    Generate human-readable summary from a report.
    
    Args:
        report_id: ID of specific report (uses latest if not provided)
        
    Returns:
        Formatted summary text
    """
    if not reports_db:
        raise HTTPException(
            status_code=404,
            detail="No reports available"
        )
    
    # Find report
    if report_id:
        report = next((r for r in reports_db if r.id == report_id), None)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
    else:
        report = max(reports_db, key=lambda r: r.generated_at)
    
    # Generate summary
    analyzer = GroqAnalyzer()
    
    week_start = report.week_start.strftime("%Y-%m-%d")
    week_end = report.week_end.strftime("%Y-%m-%d")
    
    summary = analyzer.generate_summary(
        themes=report.top_themes,
        total_reviews=report.total_reviews,
        week_start=week_start,
        week_end=week_end
    )
    
    return {
        "report_id": report.id,
        "summary": summary,
        "word_count": len(summary.split()),
        "generated_at": report.generated_at.isoformat()
    }


@router.delete("/")
async def delete_all_reports() -> Dict:
    """Clear all generated reports"""
    global reports_db
    reports_db = []
    return {"message": "All reports deleted successfully"}
