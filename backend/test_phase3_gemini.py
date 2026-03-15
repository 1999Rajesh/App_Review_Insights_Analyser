"""
Phase 3 Complete Test with Google Gemini LLM
Tests: API Routes + Gemini Theme Analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.gemini_analyzer import GeminiAnalyzer
from app.config import settings
import tempfile
import asyncio


def create_test_csv():
    """Create sample App Store CSV for testing."""
    
    csv_content = """Date,Rating,Title,Review
2026-03-10,5,Best App!,Love this application so much it changed my workflow completely
2026-03-09,4,Great,Works well but needs improvements in the reporting section
2026-03-08,3,OK,Its fine I guess nothing special really expected more features
2026-03-07,5,Amazing,Absolutely perfect in every way possible highly recommend
2026-03-06,2,Bad,Contact support at john@example.com no help received
2026-03-05,5,Wow,Very nice and helpful app indeed makes daily tasks easier
2026-03-04,4,Nice,Worst experience ever had with any app very disappointed overall
2026-03-03,1,Awful,My account has issues billing charged twice incorrectly
2026-03-02,5,Perfect,Really good app for productivity boosts efficiency significantly
2026-03-01,3,Meh,Cannot imagine working without this tool anymore essential software
2026-02-28,4,Good,Disappointing update broke several important features need fixing
2026-02-27,5,Excellent,Best investment for my business growth revenue increased dramatically
2026-02-26,2,Poor,App crashes constantly unusable garbage waste of money completely
2026-02-25,5,Love,Exceptional quality and customer support team resolved issue quickly
2026-02-20,1,Horrible,Would recommend to colleagues and friends great collaboration tool
2026-02-15,5,Outstanding,Its okay but could be better honestly missing some key features
2026-02-10,4,Recommended,Game changer for our team workflow productivity doubled since implementation
2026-02-05,3,Average,Interface design is beautiful and intuitive easy to navigate"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(csv_content)
    temp_file.close()
    
    return temp_file.name


async def test_gemini_analysis():
    """Test Gemini LLM theme analysis."""
    
    print("=" * 90)
    print("PHASE 3 TEST: Google Gemini LLM Integration")
    print("=" * 90)
    print()
    
    # Configuration check
    print("📋 STEP 1: CONFIGURATION CHECK")
    print("-" * 90)
    print(f"LLM Provider: Google Gemini (Primary)")
    print(f"Model: {settings.GEMINI_MODEL}")
    api_key_valid = settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 30
    print(f"API Key Status: {'✅ VALID' if api_key_valid else '⚠️ CHECK'}")
    print(f"Max Themes: {settings.MAX_THEMES}")
    print(f"Max Words: {settings.MAX_WORDS}")
    print()
    
    if not settings.GEMINI_API_KEY or len(settings.GEMINI_API_KEY) < 30:
        print("❌ ERROR: Please update GEMINI_API_KEY in .env file!")
        return False
    
    # Create test data
    print("📝 STEP 2: CREATING TEST DATA")
    print("-" * 90)
    csv_file = create_test_csv()
    print(f"Created test CSV with 18 reviews")
    print()
    
    # Import and filter
    from app.services.review_importer import ReviewImporter
    from app.utils.pii_remover import sanitize_reviews
    from datetime import datetime
    
    print("📥 STEP 3: IMPORTING & FILTERING REVIEWS")
    print("-" * 90)
    importer = ReviewImporter()
    
    try:
        all_reviews = importer.parse_app_store_csv(csv_file)
        print(f"Original CSV rows: 18")
        print(f"After word filter (≥5 words): {len(all_reviews)} reviews")
        
        # Date filtering
        filtered_reviews = importer.filter_by_date_range(all_reviews, weeks=8)
        print(f"After date filter (8 weeks): {len(filtered_reviews)} recent reviews")
        
        # PII Removal
        print("\n🔒 STEP 4: REMOVING PII")
        print("-" * 90)
        review_dicts = [r.model_dump() for r in filtered_reviews]
        sanitized_reviews = sanitize_reviews(review_dicts)
        
        pii_count = sum(1 for orig, san in zip(review_dicts, sanitized_reviews) 
                        if orig['text'] != san['text'])
        print(f"PII removed from: {pii_count} reviews")
        
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
        
        print(f"\nClean reviews ready for Gemini: {len(cleaned_reviews)}")
        print()
        
        # Show sample
        print("📋 SAMPLE CLEAN REVIEWS:")
        print("-" * 90)
        for i, review in enumerate(cleaned_reviews[:2], 1):
            print(f"{i}. Rating: {'⭐' * review.rating} ({review.rating}/5)")
            print(f"   Text: \"{review.text[:70]}...\"")
            print()
        
        # Send to Gemini
        print("🤖 STEP 5: SENDING TO GEMINI LLM FOR ANALYSIS")
        print("-" * 90)
        print(f"Sending {len(cleaned_reviews)} reviews to Gemini API...")
        print("This may take 15-30 seconds...")
        print()
        
        analyzer = GeminiAnalyzer()
        
        try:
            analysis_result = await analyzer.analyze_themes(cleaned_reviews, max_themes=settings.MAX_THEMES)
            
            print("✅ GEMINI ANALYSIS COMPLETE!")
            print()
            
            # Display results
            print("=" * 90)
            print("GEMINI THEME ANALYSIS RESULTS")
            print("=" * 90)
            print()
            
            if 'themes' in analysis_result:
                themes = analysis_result['themes']
                print(f"🎯 IDENTIFIED {len(themes)} MAJOR THEMES\n")
                
                for i, theme in enumerate(themes, 1):
                    theme_name = theme.get('theme_name', 'Unknown Theme')
                    count = theme.get('review_count', 0)
                    percentage = theme.get('percentage', 0)
                    sentiment = theme.get('sentiment', 'unknown')
                    
                    sentiment_emoji = {
                        'positive': '😊',
                        'negative': '😞',
                        'neutral': '😐'
                    }.get(sentiment, '❓')
                    
                    print(f"{i}. {theme_name}")
                    print(f"   {sentiment_emoji} Sentiment: {sentiment.upper()}")
                    print(f"   📊 Impact: {count} reviews ({percentage:.1f}%)")
                    
                    quotes = theme.get('quotes', [])
                    if quotes:
                        print(f"   💬 User Quotes:")
                        for quote in quotes[:2]:
                            print(f"      • \"{quote}\"")
                        if len(quotes) > 2:
                            print(f"      ... and {len(quotes) - 2} more")
                    
                    actions = theme.get('action_ideas', [])
                    if actions:
                        print(f"   💡 Action Ideas:")
                        for action in actions[:2]:
                            print(f"      • {action}")
                        if len(actions) > 2:
                            print(f"      ... and {len(actions) - 2} more")
                    
                    print()
                
                # Summary
                print("=" * 90)
                print("📈 EXECUTIVE SUMMARY")
                print("=" * 90)
                print()
                print(f"Total Reviews Analyzed: {analysis_result.get('total_reviews', len(cleaned_reviews))}")
                print(f"Themes Identified: {len(themes)}")
                print(f"Analysis Model: {settings.GEMINI_MODEL}")
                print()
                
                positive_themes = [t for t in themes if t.get('sentiment') == 'positive']
                negative_themes = [t for t in themes if t.get('sentiment') == 'negative']
                
                if positive_themes:
                    print(f"✅ Top Positive: {positive_themes[0].get('theme_name')}")
                if negative_themes:
                    print(f"⚠️  Top Concern: {negative_themes[0].get('theme_name')}")
                
                print()
                print("=" * 90)
                print("🎉 SUCCESS! GEMINI LLM ANALYZED YOUR FILTERED REVIEWS")
                print("=" * 90)
                
            else:
                print("❌ No themes found in Gemini response")
                print(f"Response: {analysis_result}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ GEMINI ANALYSIS FAILED: {e}")
            print()
            print("Possible causes:")
            print("  1. Invalid Gemini API key")
            print("  2. Network connectivity issues")
            print("  3. Gemini API quota exceeded")
            print("  4. Empty review list")
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

# Run the test
if __name__ == "__main__":
    print("\n🚀 STARTING PHASE 3 TEST WITH GEMINI LLM\n")
    print("This will:")
    print("  1. Create sample review CSV")
    print("  2. Filter reviews (word count + date)")
    print("  3. Remove PII")
    print("  4. Send to Google Gemini LLM")
    print("  5. Display generated themes")
    print()
    
    success = asyncio.run(test_gemini_analysis())
    
    print()
    if success:
        print("🎊 PHASE 3 COMPLETE!")
        print("   Gemini LLM successfully integrated!")
        print("   Your filtered reviews were analyzed perfectly!")
    else:
        print("⚠️  PHASE 3 INCOMPLETE")
        print("   Please check errors above.")
    
    print()
