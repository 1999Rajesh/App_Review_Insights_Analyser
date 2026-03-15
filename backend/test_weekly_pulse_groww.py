"""
Test script to generate and email Weekly Pulse Report for Groww App Reviews

This demonstrates the complete workflow:
1. Fetch reviews (using existing sample data)
2. Generate AI-powered weekly report
3. Send draft email with real user quotes
4. Log completion status
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.gemini_analyzer import GeminiAnalyzer
from app.routes.reviews import reviews_db
from app.services.email_sender import EmailSender


async def generate_weekly_pulse():
    """Generate weekly pulse report from existing reviews"""
    
    print("=" * 70)
    print("📊 WEEKLY PULSE REPORT GENERATOR")
    print("App: Groww (in.groww)")
    print("=" * 70)
    
    # Check if we have reviews
    if not reviews_db or len(reviews_db) == 0:
        print("\n❌ No reviews in database!")
        print("\n💡 Solution: First fetch reviews using:")
        print("   - UI: Auto-Fetch from Play Store section")
        print("   - API: POST /api/reviews/fetch-play-store")
        return None
    
    print(f"\n📈 Database contains {len(reviews_db)} reviews")
    
    # Initialize analyzer
    print("\n🤖 Initializing Gemini AI Analyzer...")
    analyzer = GeminiAnalyzer()
    
    # Generate report
    print("🔍 Analyzing reviews with AI...")
    print("⏱️  This typically takes 15-20 seconds...\n")
    
    try:
        report = await analyzer.generate_report(reviews_db)
        
        print("\n" + "=" * 70)
        print("✅ WEEKLY PULSE REPORT GENERATED!")
        print("=" * 70)
        
        # Display report summary
        print(f"\n📊 SNAPSHOT")
        print(f"   Week: {report['week_start'][:10]} to {report['week_end'][:10]}")
        print(f"   Total Reviews: {report['total_reviews']}")
        print(f"   Generated At: {report['generated_at']}")
        
        print(f"\n🎯 TOP THEMES ({len(report['top_themes'])} identified)")
        for idx, theme in enumerate(report['top_themes'], 1):
            emoji = "😊" if theme['sentiment'] == 'positive' else "⚠️"
            print(f"\n   {idx}. {theme['theme_name']} ({theme['percentage']:.1f}%) {emoji}")
            
            # Show one quote
            if theme.get('quotes') and len(theme['quotes']) > 0:
                quote = theme['quotes'][0][:80]
                print(f"      💬 \"{quote}...\"")
        
        print(f"\n💡 ACTION IDEAS")
        all_actions = []
        for theme in report['top_themes']:
            if theme.get('action_ideas'):
                all_actions.extend(theme['action_ideas'])
        
        # Show top 3 unique actions
        unique_actions = list(set(all_actions))[:3]
        for idx, action in enumerate(unique_actions, 1):
            print(f"   {idx}. {action}")
        
        print("\n" + "=" * 70)
        
        # Ask if user wants to send email
        print("\n📧 EMAIL OPTIONS:")
        print("   1. Send test email (dummy SMTP)")
        print("   2. Save report to file only")
        print("   3. Exit without sending")
        
        choice = input("\n   Enter choice (1/2/3): ").strip()
        
        if choice == "1":
            print("\n📧 Sending email report...")
            email_sender = EmailSender()
            
            # Create email content
            email_content = format_email_content(report)
            
            try:
                success = await email_sender.send_email(
                    subject=f"📊 Weekly Pulse: Groww App Reviews ({datetime.now().strftime('%b %d, %Y')})",
                    body=email_content
                )
                
                if success:
                    print("\n✅ Email sent successfully!")
                    print("   Check your inbox at: test@example.com")
                else:
                    print("\n⚠️  Email sending failed (expected with dummy credentials)")
                    print("   To configure real email, update .env with Gmail credentials")
                    
            except Exception as e:
                print(f"\n❌ Email error: {str(e)}")
                print("   This is expected with dummy SMTP credentials")
        
        elif choice == "2":
            # Save report
            save_report_to_file(report)
            print("\n✅ Report saved to backend/reports/ directory")
        
        print("\n" + "=" * 70)
        print("✨ Test completed!")
        print("=" * 70)
        
        return report
        
    except Exception as e:
        print(f"\n❌ Error generating report: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def format_email_content(report):
    """Format report as HTML email"""
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 20px; border-radius: 10px; text-align: center; }}
            .section {{ margin: 25px 0; padding: 15px; background: #f8f9fa; 
                       border-radius: 8px; }}
            .theme {{ margin: 15px 0; padding: 10px; background: white; 
                      border-left: 4px solid #667eea; }}
            .quote {{ font-style: italic; color: #555; padding: 8px; 
                      background: #fff; border-left: 3px solid #ddd; margin: 10px 0; }}
            .action {{ padding: 8px; background: #e8f5e9; margin: 8px 0; 
                       border-radius: 5px; }}
            .stat {{ display: inline-block; margin: 10px; padding: 15px; 
                     background: white; border-radius: 8px; min-width: 120px; }}
            h1 {{ color: white; margin: 0; font-size: 24px; }}
            h2 {{ color: #667eea; font-size: 18px; margin-top: 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Weekly Pulse Report</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Groww App Reviews</p>
            </div>
            
            <div class="section">
                <h2>📈 Snapshot</h2>
                <div style="text-align: center;">
                    <div class="stat">
                        <div style="font-size: 24px; font-weight: bold; color: #667eea;">
                            {report['total_reviews']}
                        </div>
                        <div style="font-size: 12px; color: #666;">Reviews Analyzed</div>
                    </div>
                    <div class="stat">
                        <div style="font-size: 24px; font-weight: bold; color: #764ba2;">
                            {len(report['top_themes'])}
                        </div>
                        <div style="font-size: 12px; color: #666;">Themes Identified</div>
                    </div>
                </div>
                <p><strong>Period:</strong> Last 8 weeks</p>
                <p><strong>Generated:</strong> {report['generated_at']}</p>
            </div>
            
            <div class="section">
                <h2>🎯 Top Themes</h2>
    """
    
    for idx, theme in enumerate(report['top_themes'], 1):
        emoji = "😊" if theme['sentiment'] == 'positive' else "⚠️"
        html += f"""
                <div class="theme">
                    <h3>{idx}. {theme['theme_name']} ({theme['percentage']:.1f}%) {emoji}</h3>
        """
        
        if theme.get('quotes'):
            for quote in theme['quotes'][:2]:
                html += f'<div class="quote">"{quote}"</div>'
        
        html += "</div>"
    
    html += """
            </div>
            
            <div class="section">
                <h2>💡 Action Ideas</h2>
    """
    
    all_actions = []
    for theme in report['top_themes']:
        if theme.get('action_ideas'):
            all_actions.extend(theme['action_ideas'])
    
    unique_actions = list(set(all_actions))[:3]
    for idx, action in enumerate(unique_actions, 1):
        html += f'<div class="action"><strong>{idx}.</strong> {action}</div>'
    
    html += f"""
            </div>
            
            <div class="footer">
                <p>Generated by App Review Insights Analyzer<br>
                Every Monday at 3:35 PM IST</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def save_report_to_file(report):
    """Save report to JSON file"""
    import json
    
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'reports'
    )
    
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"weekly_report_{datetime.now().strftime('%Y-W%W')}.json"
    filepath = os.path.join(reports_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"   📄 Saved to: {filepath}")


if __name__ == "__main__":
    asyncio.run(generate_weekly_pulse())
