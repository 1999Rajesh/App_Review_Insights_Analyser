from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Optional
from app.services.email_sender import EmailSender
from app.services.groq_analyzer import GroqAnalyzer
from app.routes.reports import reports_db
from app.config import settings

router = APIRouter(prefix="/api/email", tags=["email"])


@router.post("/send-draft")
async def send_email_draft(
    report_id: Optional[str] = None,
    recipient_email: Optional[str] = None,
    custom_subject: Optional[str] = None
) -> Dict:
    """
    Send weekly digest email with the generated report.
    
    Args:
        report_id: ID of specific report (uses latest if not provided)
        recipient_email: Override default recipient email
        custom_subject: Custom email subject line
        
    Returns:
        Confirmation of email sent
    """
    # Find report
    if not reports_db:
        raise HTTPException(
            status_code=404,
            detail="No reports available. Generate a weekly report first."
        )
    
    if report_id:
        report = next((r for r in reports_db if r.id == report_id), None)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
    else:
        report = max(reports_db, key=lambda r: r.generated_at)
    
    try:
        # Generate summary text
        analyzer = GroqAnalyzer()
        week_start = report.week_start.strftime("%Y-%m-%d")
        week_end = report.week_end.strftime("%Y-%m-%d")
        
        report_content = analyzer.generate_summary(
            themes=report.top_themes,
            total_reviews=report.total_reviews,
            week_start=week_start,
            week_end=week_end
        )
        
        # Create email subject
        subject = custom_subject or f"Weekly App Review Pulse - {week_end}"
        
        # Send email
        email_sender = EmailSender()
        email_sender.send_weekly_digest(
            report_content=report_content,
            recipient_email=recipient_email,
            subject=subject
        )
        
        return {
            "success": True,
            "message": "Email sent successfully",
            "recipient": recipient_email or settings.RECIPIENT_EMAIL,
            "subject": subject,
            "report_id": report.id,
            "sent_at": report.week_end.strftime("%Y-%m-%d")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )


@router.post("/test-connection")
async def test_email_connection() -> Dict:
    """
    Test SMTP connection with current settings.
    
    Returns:
        Connection test result
    """
    try:
        email_sender = EmailSender()
        email_sender.test_connection()
        
        return {
            "success": True,
            "message": "SMTP connection successful",
            "server": settings.SMTP_SERVER,
            "port": settings.SMTP_PORT,
            "sender": settings.SENDER_EMAIL
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SMTP connection failed: {str(e)}"
        )
