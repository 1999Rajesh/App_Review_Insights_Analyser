"""
Weekly Pulse Report Scheduler

Automatically generates and emails weekly pulse reports every 5 minutes for testing.
Uses APScheduler for reliable job scheduling with timezone support.
Logs are stored in a dedicated scheduler log file.
"""

import asyncio
import logging
import os
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

from app.services.gemini_analyzer import GeminiAnalyzer
from app.services.email_sender import EmailSender
from app.routes.reviews import reviews_db
from app.config import settings

# Create dedicated scheduler logger with separate file
scheduler_logger = logging.getLogger('scheduler')
scheduler_logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# File handler for scheduler logs
file_handler = logging.FileHandler(settings.SCHEDULER_LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Console handler for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger (avoid duplicates)
if not scheduler_logger.handlers:
    scheduler_logger.addHandler(file_handler)
    scheduler_logger.addHandler(console_handler)


class WeeklyPulseScheduler:
    """Manage automated weekly pulse report generation and delivery"""
    
    def __init__(self):
        """Initialize the scheduler with interval-based triggering"""
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Kolkata'))
        self.is_running = False
        
        # Fixed recipient email for scheduler
        self.recipient_email = "codeflex1999@gmail.com"
        
        # Schedule interval: Every 5 minutes for testing
        self.interval_minutes = settings.SCHEDULER_INTERVAL_MINUTES
    
    async def generate_and_send_weekly_pulse(self):
        """
        Generate weekly pulse report and send via email.
        This is the main job that runs every 5 minutes.
        """
        scheduler_logger.info("=" * 60)
        scheduler_logger.info("🕐 SCHEDULER TRIGGERED: Generating Weekly Pulse Report")
        scheduler_logger.info(f"📧 Recipient: {self.recipient_email}")
        scheduler_logger.info(f"⏰ Time: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')}")
        scheduler_logger.info(f"🔄 Interval: Every {self.interval_minutes} minutes")
        scheduler_logger.info("=" * 60)
        
        try:
            # Check if we have reviews to analyze
            if not reviews_db:
                scheduler_logger.warning("⚠️ No reviews available in database. Skipping report generation.")
                return
            
            scheduler_logger.info(f"📊 Found {len(reviews_db)} reviews to analyze")
            
            # Use maximum 200 reviews for classification (as per hint)
            reviews_to_analyze = reviews_db[:200] if len(reviews_db) > 200 else reviews_db
            scheduler_logger.info(f"📝 Using {len(reviews_to_analyze)} reviews for AI classification (max 200)")
            
            # Step 1: Generate themes using Gemini AI (Phase 3)
            scheduler_logger.info("🤖 Step 1/4: Analyzing reviews with Gemini AI (Phase 3)...")
            analyzer = GeminiAnalyzer()
            analysis_result = await analyzer.analyze_themes(reviews_to_analyze, max_themes=5)
            themes = analysis_result['themes']
            
            if not themes:
                scheduler_logger.warning("⚠️ No themes identified. Skipping report.")
                return
            
            scheduler_logger.info(f"✅ Identified {len(themes)} themes")
            
            # Step 2: Create report content
            scheduler_logger.info("📝 Step 2/4: Creating report content...")
            report_content = self._create_report_content(
                themes=themes,
                total_reviews=len(reviews_to_analyze),
                model_used=settings.GEMINI_MODEL
            )
            
            # Step 3: Send email
            scheduler_logger.info("📧 Step 3/4: Sending email via SMTP...")
            email_sender = EmailSender()
            
            subject = f"Weekly App Review Pulse - {datetime.now().strftime('%B %d, %Y %H:%M')}"
            
            success = email_sender.send_weekly_digest(
                report_content=report_content,
                recipient_email=self.recipient_email,
                subject=subject
            )
            
            if success:
                scheduler_logger.info("✅ Step 4/4: Email sent successfully!")
                scheduler_logger.info(f"📨 Delivered to: {self.recipient_email}")
            else:
                scheduler_logger.error("❌ Failed to send email")
            
            scheduler_logger.info("=" * 60)
            scheduler_logger.info("🎉 WEEKLY PULSE COMPLETE")
            scheduler_logger.info(f"📄 Logs saved to: {settings.SCHEDULER_LOG_FILE}")
            scheduler_logger.info("=" * 60)
            
        except Exception as e:
            scheduler_logger.error(f"❌ Error generating weekly pulse: {str(e)}", exc_info=True)
            raise
    
    def _create_report_content(self, themes: list, total_reviews: int, model_used: str) -> str:
        """
        Create formatted report content for email.
        
        Args:
            themes: List of theme dictionaries from AI analysis
            total_reviews: Total number of reviews analyzed
            model_used: AI model used for analysis
            
        Returns:
            Formatted markdown report content
        """
        # Calculate sentiment distribution
        positive_count = sum(t['review_count'] for t in themes if t.get('sentiment') == 'positive')
        negative_count = sum(t['review_count'] for t in themes if t.get('sentiment') == 'negative')
        neutral_count = sum(t['review_count'] for t in themes if t.get('sentiment') == 'neutral')
        
        # Find top positive and concern
        positive_themes = [t for t in themes if t.get('sentiment') == 'positive']
        negative_themes = [t for t in themes if t.get('sentiment') == 'negative']
        
        top_positive = positive_themes[0]['theme_name'] if positive_themes else 'N/A'
        top_concern = negative_themes[0]['theme_name'] if negative_themes else 'N/A'
        
        # Build report
        report = f"""# 📊 Weekly App Review Pulse

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}  
**Analysis Period:** Last 8 weeks  
**Total Reviews Analyzed:** {total_reviews}

---

## 🎯 Executive Summary

This week's analysis identified **{len(themes)} major themes** from {total_reviews} app store reviews.

**Key Highlights:**
- 😊 **Top Positive:** {top_positive}
- ⚠️ **Top Concern:** {top_concern}
- 📈 **Sentiment Distribution:** 
  - Positive: {positive_count} reviews ({(positive_count/total_reviews*100):.1f}%)
  - Negative: {negative_count} reviews ({(negative_count/total_reviews*100):.1f}%)
  - Neutral: {neutral_count} reviews ({(neutral_count/total_reviews*100):.1f}%)

---

## 📋 Detailed Theme Analysis

"""
        
        # Add each theme
        for i, theme in enumerate(themes, 1):
            emoji = "😊" if theme.get('sentiment') == 'positive' else "😞" if theme.get('sentiment') == 'negative' else "😐"
            
            report += f"""### {i}. {theme['theme_name']} {emoji}

**Impact:** {theme['review_count']} reviews ({theme.get('percentage', 0):.1f}%)

**What Users Are Saying:**
"""
            
            # Add quotes
            for quote in theme.get('quotes', [])[:3]:
                report += f"- \"{quote}\"\n"
            
            report += "\n**Recommended Actions:**\n"
            
            # Add action ideas
            for j, action in enumerate(theme.get('action_ideas', [])[:3], 1):
                report += f"{j}. {action}\n"
            
            report += "\n---\n\n"
        
        # Add footer
        report += f"""
## 🤖 About This Report

- **AI Model Used:** {model_used}
- **Processing Time:** Automated analysis
- **Data Sources:** Apple App Store & Google Play Store
- **Frequency:** Weekly (Every Monday at 3:35 PM IST)

---

**Powered by App Review Insights Analyzer**  
*Turn app store reviews into actionable weekly insights*
"""
        
        return report
    
    def start(self):
        """Start the scheduler with 5-minute interval"""
        if self.is_running:
            scheduler_logger.warning("Scheduler is already running")
            return
        
        # Add job - Run every 5 minutes
        self.scheduler.add_job(
            func=self._run_scheduled_job,
            trigger=IntervalTrigger(
                minutes=self.interval_minutes,
                timezone=pytz.timezone('Asia/Kolkata')
            ),
            id='weekly_pulse_generator',
            name='Generate and send weekly pulse report every 5 minutes',
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        
        next_run = self.scheduler.get_job('weekly_pulse_generator').next_run_time
        scheduler_logger.info("=" * 60)
        scheduler_logger.info("🤖 WEEKLY PULSE SCHEDULER STARTED")
        scheduler_logger.info("=" * 60)
        scheduler_logger.info(f"✅ Scheduler Status: RUNNING")
        scheduler_logger.info(f"📧 Recipient: {self.recipient_email}")
        scheduler_logger.info(f"⏰ Schedule: Every {self.interval_minutes} minutes")
        scheduler_logger.info(f"🕐 Next Run: {next_run.strftime('%Y-%m-%d %I:%M %p IST')}")
        scheduler_logger.info(f"📄 Log File: {settings.SCHEDULER_LOG_FILE}")
        scheduler_logger.info("=" * 60)
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            scheduler_logger.warning("Scheduler is not running")
            return
        
        self.scheduler.shutdown(wait=False)
        self.is_running = False
        
        scheduler_logger.info("=" * 60)
        scheduler_logger.info("🛑 WEEKLY PULSE SCHEDULER STOPPED")
        scheduler_logger.info("=" * 60)
    
    async def _run_scheduled_job(self):
        """Wrapper to run async job in scheduler"""
        try:
            await self.generate_and_send_weekly_pulse()
        except Exception as e:
            scheduler_logger.error(f"Error in scheduled job: {str(e)}", exc_info=True)
    
    def get_next_run_time(self) -> datetime:
        """Get the next scheduled run time"""
        job = self.scheduler.get_job('weekly_pulse_generator')
        if job:
            return job.next_run_time
        return None
    
    def get_scheduler_status(self) -> dict:
        """Get current scheduler status"""
        next_run = self.get_next_run_time()
        
        return {
            'is_running': self.is_running,
            'recipient_email': self.recipient_email,
            'schedule': f"Every {self.interval_minutes} minutes",
            'next_run': next_run.isoformat() if next_run else None,
            'next_run_formatted': next_run.strftime('%Y-%m-%d %I:%M %p IST') if next_run else None,
            'timezone': 'Asia/Kolkata',
            'log_file': settings.SCHEDULER_LOG_FILE
        }


# Global scheduler instance
weekly_pulse_scheduler = WeeklyPulseScheduler()


def get_scheduler():
    """Get the global scheduler instance"""
    return weekly_pulse_scheduler
