"""
Complete End-to-End Test: Send Filtered Reviews to LLM for Theme Analysis
This script demonstrates the full workflow from CSV → Filter → LLM → Themes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.review_importer import ReviewImporter
from app.utils.pii_remover import sanitize_reviews
from app.services.groq_analyzer import GroqAnalyzer
from app.config import settings
from datetime import datetime
import tempfile
import json


def create_comprehensive_test_csv():
    """Create a realistic test CSV with diverse reviews."""
    
    csv_content = """Date,Rating,Title,Review
2026-03-10,5,Best App!,Love this application so much it changed my workflow completely
2026-03-09,4,Great,Works well but needs improvements in the reporting section
2026-03-08,3,OK,Its fine I guess nothing special really expected more features
2026-03-07,5,Amazing,Absolutely perfect in every way possible highly recommend
2026-03-06,2,Bad,Contact support at john@example.com or call 555-123-4567 no help
2026-03-05,5,Wow,Very nice and helpful app indeed makes daily tasks easier
2026-03-04,4,Nice,Worst experience ever had with any app very disappointed overall
2026-03-03,1,Awful,My account #123456 has issues and card 1234-5678-9012-3456 charged twice
2026-03-02,5,Perfect,Really good app for productivity boosts efficiency significantly
2026-03-01,3,Meh,Cannot imagine working without this tool anymore essential software
2026-02-28,4,Good,Disappointing update broke several important features need fixing
2026-02-27,5,Excellent,Best investment for my business growth revenue increased dramatically
2026-02-26,2,Poor,App crashes constantly unusable garbage waste of money completely
2026-02-25,5,Love,Exceptional quality and customer support team resolved issue quickly
2026-02-20,1,Horrible,Would recommend to colleagues and friends great collaboration tool
2026-02-15,5,Outstanding,Its okay but could be better honestly missing some key features
2026-02-10,4,Recommended,Game changer for our team workflow productivity doubled since implementation
2026-02-05,3,Average,Interface design is beautiful and intuitive easy to navigate
2026-02-01,5,Fantastic,Loading speed needs improvement sometimes takes forever to open
2026-01-28,4,Good,Privacy features are top notch feel secure using this app
2026-01-25,5,Superb,Cross platform sync works flawlessly between all my devices
2026-01-20,3,Fair,Customer service response time is slow waited three days for reply
2026-01-15,4,Very Good,Value for money is excellent compared to competitors pricing
2026-01-10,5,Marvelous,Regular updates keep adding useful features developers listen to feedback"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(csv_content)
    temp_file.close()
    
    return temp_file.name


async def analyze_reviews_with_llm():
    """Send filtered reviews to LLM and get theme analysis."""
    
    print("=" * 90)
    print("END-TO-END TEST: CSV → FILTER → LLM → THEMES")
    print("=" * 90)
    print()
    
    # Step 1: Configuration Check
    print("📋 STEP 1: SYSTEM CONFIGURATION")
    print("-" * 90)
    print(f"Groq Model: {settings.GROQ_MODEL}")
    print(f"API Key Status: {'✅ VALID' if settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith('test') else '⚠️ INVALID'}")
    print(f"Max Themes: {settings.MAX_THEMES}")
    print(f"Max Words: {settings.MAX_WORDS}")
    print(f"Date Range: Last {settings.REVIEW_WEEKS_RANGE} weeks")
    print(f"Word Threshold: ≥5 words")
    print()
    
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY.startswith('your_') or settings.GROQ_API_KEY.startswith('test'):
        print("❌ ERROR: Please update GROQ_API_KEY in .env file with your actual key!")
        return False
    
    # Step 2: Create and Import Reviews
    print("📝 STEP 2: CREATING TEST DATA")
    print("-" * 90)
    csv_file = create_comprehensive_test_csv()
    print(f"Created test CSV with 24 diverse reviews")
    print()
    
    print("📥 STEP 3: IMPORTING & FILTERING REVIEWS")
    print("-" * 90)
    importer = ReviewImporter()
    
    try:
        # Parse CSV
        all_reviews = importer.parse_app_store_csv(csv_file)
        print(f"Original CSV rows: 24")
        print(f"After word filter (≥5 words): {len(all_reviews)} reviews kept")
        print(f"Filtered out: {24 - len(all_reviews)} reviews (< 5 words)")
        print()
        
        # Date filtering
        filtered_reviews = importer.filter_by_date_range(all_reviews, weeks=8)
        print(f"After date filter (8 weeks): {len(filtered_reviews)} recent reviews")
        if len(filtered_reviews) < len(all_reviews):
            print(f"Filtered out: {len(all_reviews) - len(filtered_reviews)} reviews (outside date range)")
        print()
        
        # PII Removal
        print("🔒 STEP 4: REMOVING PII")
        print("-" * 90)
        review_dicts = [r.model_dump() for r in filtered_reviews]
        sanitized_reviews = sanitize_reviews(review_dicts)
        
        pii_count = sum(1 for orig, san in zip(review_dicts, sanitized_reviews) 
                        if orig['text'] != san['text'])
        print(f"PII detected and removed from: {pii_count} reviews")
        
        # Show PII examples
        if pii_count > 0:
            print("\nPII Removal Examples:")
            for orig, san in zip(review_dicts, sanitized_reviews):
                if orig['text'] != san['text']:
                    print(f"  Before: {orig['text'][:70]}...")
                    print(f"  After:  {san['text'][:70]}...")
                    print()
                    break
        
        # Convert back to Review objects
        cleaned_reviews = []
        for data in sanitized_reviews:
            try:
                review = Review(
                    id=data['id'],
                    source=data['source'],
                    rating=data['rating'],
                    title=data['title'],
                    text=data['text'],
                    date=datetime.fromisoformat(data['date']) if isinstance(data['date'], str) else data['date']
                )
                cleaned_reviews.append(review)
            except Exception as e:
                print(f"Warning: Could not create review: {e}")
        
        print(f"Clean reviews ready for LLM: {len(cleaned_reviews)}")
        print()
        
        # Show sample reviews
        print("📋 SAMPLE CLEAN REVIEWS (First 3):")
        print("-" * 90)
        for i, review in enumerate(cleaned_reviews[:3], 1):
            print(f"\n{i}. Rating: {'⭐' * review.rating} ({review.rating}/5)")
            print(f"   Text: \"{review.text[:80]}...\"")
            print(f"   Date: {review.date.strftime('%Y-%m-%d')}")
        if len(cleaned_reviews) > 3:
            print(f"\n... and {len(cleaned_reviews) - 3} more reviews")
        print()
        
        # Statistics
        print("📊 REVIEW STATISTICS")
        print("-" * 90)
        avg_rating = sum(r.rating for r in cleaned_reviews) / len(cleaned_reviews)
        print(f"Total Reviews: {len(cleaned_reviews)}")
        print(f"Average Rating: {avg_rating:.2f}/5 ⭐")
        
        # Rating distribution
        ratings = {}
        for r in cleaned_reviews:
            ratings[r.rating] = ratings.get(r.rating, 0) + 1
        
        print(f"\nRating Distribution:")
        for rating in sorted(ratings.keys(), reverse=True):
            count = ratings[rating]
            bar = '█' * count
            print(f"  {rating}⭐: {bar} ({count})")
        print()
        
        # LLM Analysis
        print("🤖 STEP 5: SENDING TO GROQ LLM FOR THEME ANALYSIS")
        print("-" * 90)
        print(f"Sending {len(cleaned_reviews)} clean reviews to Groq API...")
        print("This may take 15-30 seconds...")
        print()
        
        analyzer = GroqAnalyzer()
        
        try:
            # Call LLM for analysis
            analysis_result = await analyzer.analyze_themes(cleaned_reviews, max_themes=settings.MAX_THEMES)
            
            print("✅ LLM ANALYSIS COMPLETE!")
            print()
            
            # Display Results
            print("=" * 90)
            print("LLM THEME ANALYSIS RESULTS")
            print("=" * 90)
            print()
            
            if 'themes' in analysis_result:
                themes = analysis_result['themes']
                print(f"🎯 IDENTIFIED {len(themes)} MAJOR THEMES\n")
                
                for i, theme in enumerate(themes, 1):
                    # Handle both dict and object formats
                    if isinstance(theme, dict):
                        theme_name = theme.get('theme_name', 'Unknown Theme')
                        count = theme.get('review_count', 0)
                        percentage = theme.get('percentage', 0)
                        sentiment = theme.get('sentiment', 'unknown')
                        quotes = theme.get('quotes', [])
                        actions = theme.get('action_ideas', [])
                    else:
                        # It's an object, use attributes
                        theme_name = getattr(theme, 'theme_name', 'Unknown Theme')
                        count = getattr(theme, 'review_count', 0)
                        percentage = getattr(theme, 'percentage', 0)
                        sentiment = getattr(theme, 'sentiment', 'unknown')
                        quotes = getattr(theme, 'quotes', [])
                        actions = getattr(theme, 'action_ideas', [])
                    
                    # Sentiment emoji
                    sentiment_emoji = {
                        'positive': '😊',
                        'negative': '😞',
                        'neutral': '😐'
                    }.get(sentiment, '❓')
                    
                    print(f"{i}. {theme_name}")
                    print(f"   {sentiment_emoji} Sentiment: {sentiment.upper()}")
                    print(f"   📊 Impact: {count} reviews ({percentage:.1f}%)")
                    
                    # Quotes
                    if quotes:
                        print(f"   💬 User Quotes:")
                        for quote in quotes[:2]:  # Show first 2
                            print(f"      • \"{quote}\"")
                        if len(quotes) > 2:
                            print(f"      ... and {len(quotes) - 2} more")
                    
                    # Action ideas
                    if actions:
                        print(f"   💡 Action Ideas:")
                        for action in actions[:2]:  # Show first 2
                            print(f"      • {action}")
                        if len(actions) > 2:
                            print(f"      ... and {len(actions) - 2} more")
                    
                    print()
                
                # Summary
                print("=" * 90)
                print("📈 EXECUTIVE SUMMARY")
                print("=" * 90)
                print()
                print(f"Total Reviews Analyzed: {len(cleaned_reviews)}")
                print(f"Themes Identified: {len(themes)}")
                print(f"Analysis Model: {settings.GROQ_MODEL}")
                print(f"Processing Time: ~{analysis_result.get('processing_time_seconds', 'N/A')}s")
                print()
                
                # Top positive and negative themes
                positive_themes = []
                negative_themes = []
                
                for t in themes:
                    if isinstance(t, dict):
                        sentiment = t.get('sentiment', '')
                        name = t.get('theme_name', '')
                    else:
                        sentiment = getattr(t, 'sentiment', '')
                        name = getattr(t, 'theme_name', '')
                    
                    if sentiment == 'positive':
                        positive_themes.append({'name': name})
                    elif sentiment == 'negative':
                        negative_themes.append({'name': name})
                
                if positive_themes:
                    print(f"✅ Top Positive: {positive_themes[0]['name']}")
                if negative_themes:
                    print(f"⚠️  Top Concern: {negative_themes[0]['name']}")
                
                print()
                print("=" * 90)
                print("🎉 SUCCESS! THEMES EXTRACTED FROM YOUR FILTERED REVIEWS")
                print("=" * 90)
                
            else:
                print("❌ No themes found in LLM response")
                print(f"Response: {analysis_result}")
            
            return True
            
        except Exception as e:
            print(f"❌ LLM ANALYSIS FAILED: {e}")
            print()
            print("Possible causes:")
            print("  1. Invalid or expired Groq API key")
            print("  2. Network connectivity issues")
            print("  3. Groq API rate limiting")
            print("  4. Empty review list")
            print("  5. API service temporarily unavailable")
            print()
            print("Troubleshooting:")
            print("  - Check your internet connection")
            print("  - Verify GROQ_API_KEY in .env file")
            print("  - Wait a few minutes and try again")
            return False
        
    except Exception as e:
        print(f"❌ ERROR IN WORKFLOW: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        if os.path.exists(csv_file):
            os.unlink(csv_file)


# Import Review model
from app.models.review import Review

# Run the analysis
if __name__ == "__main__":
    import asyncio
    
    print("\n🚀 STARTING COMPLETE END-TO-END TEST\n")
    print("This will:")
    print("  1. Create sample review CSV")
    print("  2. Filter reviews (word count + date range)")
    print("  3. Remove PII")
    print("  4. Send to Groq LLM for theme analysis")
    print("  5. Display generated themes and insights")
    print()
    
    success = asyncio.run(analyze_reviews_with_llm())
    
    print()
    if success:
        print("🎊 DEMONSTRATION COMPLETE!")
        print("   Your filtered reviews were successfully analyzed by Groq LLM!")
        print("   This is exactly how the system works with your real CSV files.")
    else:
        print("⚠️  DEMONSTRATION INCOMPLETE")
        print("   Please check errors above and try again.")
    
    print()
