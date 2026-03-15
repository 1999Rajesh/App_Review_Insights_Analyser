"""
Railway Scheduled Task for Weekly Review Pipeline

This script is designed to run on Railway as a scheduled task (cron job).
It executes the complete weekly review pipeline automatically.

Setup Instructions:
1. Deploy backend to Railway
2. Add environment variables in Railway dashboard
3. Create a scheduled task that runs this script weekly
4. Set schedule to run every Monday at 10:00 AM IST

Environment Variables Required:
- PLAY_STORE_DEFAULT_APP_ID=in.groww
- PLAY_STORE_LANGUAGE=en
- PLAY_STORE_COUNTRY=in
- MAX_REVIEWS_TO_FETCH=500
- REVIEW_WEEKS_RANGE=12
- MIN_REVIEW_WORD_COUNT=5
- ALLOW_EMOJIS=false
- REQUIRED_LANGUAGE=en
- SMTP_SENDER_EMAIL=your-email@gmail.com
- SMTP_PASSWORD=your-app-password
- SMTP_HOST=smtp.gmail.com
- SMTP_PORT=587
- WEEKLY_REPORT_EMAIL=recipient@example.com
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.weekly_review_pipeline import WeeklyReviewPipeline


def main():
    """Run the weekly review pipeline for Railway scheduled execution"""
    print("=" * 70)
    print("🤖 RAILWAY SCHEDULED TASK: WEEKLY REVIEW PIPELINE")
    print(f"⏰ Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 70)
    
    # Check required environment variables
    required_vars = [
        'PLAY_STORE_DEFAULT_APP_ID',
        'SMTP_SENDER_EMAIL',
        'WEEKLY_REPORT_EMAIL'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please configure these in Railway dashboard")
        sys.exit(1)
    
    print("✅ Environment variables configured")
    print(f"   App ID: {os.getenv('PLAY_STORE_DEFAULT_APP_ID')}")
    print(f"   Weeks: {os.getenv('REVIEW_WEEKS_RANGE', '12')}")
    print(f"   Max Reviews: {os.getenv('MAX_REVIEWS_TO_FETCH', '500')}")
    print(f"   Report Email: {os.getenv('WEEKLY_REPORT_EMAIL')}")
    
    # Run pipeline with email enabled
    pipeline = WeeklyReviewPipeline()
    result = pipeline.run(send_email=True)
    
    # Exit with appropriate code for Railway
    if result['success']:
        print("\n✅ Railway task completed successfully!")
        print(f"   Reviews: {result.get('reviews_collected', 0)}")
        print(f"   Themes: {result.get('themes_identified', 0)}")
        print(f"   Email sent: {result.get('email_sent', False)}")
        sys.exit(0)
    else:
        error_msg = result.get('errors', ['Unknown error'])[0]
        print(f"\n❌ Railway task failed: {error_msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
