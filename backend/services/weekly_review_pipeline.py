"""
Complete Weekly Review Pipeline

End-to-end automation:
1. Fetch reviews from Play Store (last 8-12 weeks)
2. Save in hybrid format (JSON + CSV)
3. Generate weekly one-page note (max 5 themes, top 3 shown)
4. Email the note (with PII protection)
5. Run automatically every week

Usage:
    python -m services.weekly_review_pipeline
"""

import os
import sys
from datetime import datetime
from typing import Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.hybrid_review_collector import HybridReviewCollector
from services.weekly_pulse_generator import WeeklyPulseNoteGenerator
from app.services.email_sender import EmailSender


class WeeklyReviewPipeline:
    """Complete automated weekly review analysis pipeline"""
    
    def __init__(self):
        self.collector = HybridReviewCollector()
        self.note_generator = WeeklyPulseNoteGenerator()
        self.email_sender = EmailSender()
        
        # Email configuration
        self.recipient_email = os.getenv('WEEKLY_REPORT_EMAIL', 'codeflex1999@gmail.com')
        self.sender_email = os.getenv('SMTP_SENDER_EMAIL', '')
    
    def run(self, send_email: bool = True) -> Dict:
        """
        Execute complete pipeline
        
        Args:
            send_email: Whether to send email (default True)
            
        Returns:
            Dictionary with pipeline results
        """
        print("=" * 70)
        print("🚀 WEEKLY REVIEW PIPELINE")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        pipeline_result = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'steps_completed': [],
            'errors': []
        }
        
        try:
            # STEP 1: Collect reviews (Hybrid JSON + CSV)
            print("\n" + "=" * 70)
            print("📥 STEP 1/4: COLLECTING REVIEWS")
            print("=" * 70)
            
            collection_result = self.collector.collect()
            
            if not collection_result.get('success'):
                raise Exception(f"Review collection failed: {collection_result.get('message', 'Unknown error')}")
            
            pipeline_result['steps_completed'].append('review_collection')
            pipeline_result['reviews_collected'] = collection_result.get('reviews_collected', 0)
            pipeline_result['json_file'] = collection_result.get('json_file')
            pipeline_result['csv_file'] = collection_result.get('csv_file')
            
            # Verify we have reviews to analyze
            if collection_result.get('reviews_collected', 0) == 0:
                print("⚠️ No reviews collected. Pipeline stopped.")
                pipeline_result['success'] = True
                pipeline_result['message'] = 'No reviews available'
                return pipeline_result
            
            # STEP 2: Generate weekly pulse note
            print("\n" + "=" * 70)
            print("📝 STEP 2/4: GENERATING WEEKLY PULSE NOTE")
            print("=" * 70)
            
            note_result = self.note_generator.generate(collection_result.get('json_file'))
            
            if not note_result.get('success'):
                raise Exception(f"Note generation failed: {note_result.get('message', 'Unknown error')}")
            
            pipeline_result['steps_completed'].append('note_generation')
            pipeline_result['note_file'] = note_result.get('note_file')
            pipeline_result['themes_identified'] = note_result.get('themes_identified', 0)
            pipeline_result['total_reviews_analyzed'] = note_result.get('total_reviews', 0)
            
            # STEP 3: Send email (optional)
            if send_email:
                print("\n" + "=" * 70)
                print("📧 STEP 3/4: SENDING EMAIL REPORT")
                print("=" * 70)
                
                if not self.sender_email:
                    print("⚠️ SMTP_SENDER_EMAIL not configured. Skipping email.")
                    pipeline_result['email_sent'] = False
                    pipeline_result['email_error'] = 'Email not configured'
                else:
                    try:
                        # Read the note content
                        note_content = note_result.get('note_content', '')
                        
                        # Create email subject
                        subject = f"Weekly App Review Pulse - Week {datetime.now().isocalendar()[1]}, {datetime.now().year}"
                        
                        # Send email
                        email_success = self.email_sender.send_weekly_digest(
                            report_content=note_content,
                            recipient_email=self.recipient_email,
                            subject=subject
                        )
                        
                        if email_success:
                            print(f"✅ Email sent successfully to {self.recipient_email}")
                            pipeline_result['steps_completed'].append('email_sent')
                            pipeline_result['email_sent'] = True
                            pipeline_result['email_recipient'] = self.recipient_email
                        else:
                            print("❌ Failed to send email")
                            pipeline_result['email_sent'] = False
                            pipeline_result['email_error'] = 'Email sending failed'
                    
                    except Exception as e:
                        print(f"❌ Email error: {str(e)}")
                        pipeline_result['email_sent'] = False
                        pipeline_result['email_error'] = str(e)
            else:
                print("\n⏭️ Email sending skipped (send_email=False)")
                pipeline_result['email_sent'] = False
            
            # STEP 4: Summary
            print("\n" + "=" * 70)
            print("✅ STEP 4/4: PIPELINE COMPLETE")
            print("=" * 70)
            
            print(f"\n📊 SUMMARY:")
            print(f"   ✅ Reviews collected: {pipeline_result['reviews_collected']}")
            print(f"   📄 JSON file: {pipeline_result.get('json_file', 'N/A')}")
            print(f"   📊 CSV file: {pipeline_result.get('csv_file', 'N/A')}")
            print(f"   🎯 Themes identified: {pipeline_result['themes_identified']}")
            print(f"   📝 Note file: {pipeline_result.get('note_file', 'N/A')}")
            print(f"   📧 Email sent: {pipeline_result.get('email_sent', False)}")
            
            if pipeline_result.get('email_recipient'):
                print(f"   📨 Sent to: {pipeline_result['email_recipient']}")
            
            pipeline_result['success'] = True
            
            print("\n" + "=" * 70)
            print("🎉 PIPELINE EXECUTION SUCCESSFUL")
            print("=" * 70)
            
            return pipeline_result
            
        except Exception as e:
            print(f"\n❌ PIPELINE ERROR: {str(e)}")
            pipeline_result['success'] = False
            pipeline_result['errors'].append(str(e))
            
            print("\n" + "=" * 70)
            print("🚨 PIPELINE FAILED")
            print("=" * 70)
            
            # Don't re-raise - return error in result
            return pipeline_result


def main():
    """Entry point for running the complete pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Weekly Review Analysis Pipeline')
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email (only generate files)'
    )
    parser.add_argument(
        '--weeks',
        type=int,
        default=12,
        help='Number of weeks to look back (default: 12)'
    )
    parser.add_argument(
        '--max-reviews',
        type=int,
        default=500,
        help='Maximum reviews to fetch (default: 500)'
    )
    
    args = parser.parse_args()
    
    # Set environment variables from arguments
    if args.weeks:
        os.environ['REVIEW_WEEKS_RANGE'] = str(args.weeks)
    if args.max_reviews:
        os.environ['MAX_REVIEWS_TO_FETCH'] = str(args.max_reviews)
    
    # Run pipeline
    pipeline = WeeklyReviewPipeline()
    result = pipeline.run(send_email=not args.no_email)
    
    # Exit with appropriate code
    if result['success']:
        print("\n✅ Pipeline completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Pipeline failed: {result.get('errors', ['Unknown error'])[0]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
