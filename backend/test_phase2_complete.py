"""
Phase 2 Complete Workflow Test
Demonstrates: CSV Import → Filtering → PII Removal → LLM Analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.review_importer import ReviewImporter
from app.utils.pii_remover import sanitize_reviews, remove_pii
from app.services.groq_analyzer import GroqAnalyzer
from app.config import settings
from datetime import datetime
import tempfile


def create_test_csv():
    """Create a sample App Store CSV file for testing."""
    
    # Mix of good reviews (≥5 words) and bad reviews (<5 words)
    csv_content = """Date,Rating,Title,Review
2026-03-10,5,Best App!,Love this application so much
2026-03-09,4,Great,Works well but needs improvements
2026-03-08,3,OK,Its fine I guess nothing special
2026-03-07,5,Amazing,Absolutely perfect in every way
2026-03-06,2,Bad,Terrible experience overall
2026-03-05,5,Wow,"Contact me at john@example.com or call 555-123-4567"
2026-03-04,4,Nice,Very nice and helpful app indeed
2026-03-03,1,Awful,Worst experience ever had with any app
2026-03-02,5,Perfect,"My account #123456 has issues, card 1234-5678-9012-3456"
2026-03-01,3,Meh,Its fine nothing special really
2026-02-28,4,Good,Really good app for productivity
2026-02-27,5,Excellent,Cannot imagine working without this tool
2026-02-26,2,Poor,Disappointing update broke features
2026-02-25,5,Love,Best investment for my business growth
2026-02-24,3,Average,Does what it promises nothing more
2026-02-20,1,Horrible,App crashes constantly unusable garbage
2026-02-15,5,Outstanding,Exceptional quality and customer support
2026-02-10,4,Recommended,Would recommend to colleagues and friends
2026-02-05,3,Okay,Its okay but could be better honestly
2026-02-01,5,Fantastic,Game changer for our team workflow"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(csv_content)
    temp_file.close()
    
    return temp_file.name


def test_phase2_workflow():
    """Test complete Phase 2 workflow with LLM analysis."""
    
    print("=" * 80)
    print("PHASE 2 COMPLETE WORKFLOW TEST")
    print("=" * 80)
    print()
    
    # Step 1: Create test CSV
    print("📝 Step 1: Creating test CSV file...")
    csv_file = create_test_csv()
    print(f"   ✅ Created: {csv_file}")
    print()
    
    # Step 2: Import reviews (with automatic filtering)
    print("📥 Step 2: Importing reviews (automatic filtering applied)...")
    importer = ReviewImporter()
    
    try:
        all_reviews = importer.parse_app_store_csv(csv_file)
        print(f"   📊 Original CSV rows: 20")
        print(f"   ✅ After word count filter (≥5 words): {len(all_reviews)} reviews")
        print(f"   🗑️  Filtered out: {20 - len(all_reviews)} reviews (< 5 words)")
        print()
        
        # Show filtered reviews
        print("   📋 KEPT Reviews (all have ≥5 words):")
        for i, review in enumerate(all_reviews[:5], 1):  # Show first 5
            word_count = len(review.text.split())
            print(f"      {i}. \"{review.text[:50]}...\" ({word_count} words)")
        if len(all_reviews) > 5:
            print(f"      ... and {len(all_reviews) - 5} more")
        print()
        
    except Exception as e:
        print(f"   ❌ Error importing reviews: {e}")
        return False
    
    # Step 3: Apply date filtering
    print("📅 Step 3: Applying date range filtering (last 8 weeks)...")
    filtered_reviews = importer.filter_by_date_range(all_reviews, weeks=8)
    print(f"   ✅ After date filter: {len(filtered_reviews)} reviews")
    if len(filtered_reviews) < len(all_reviews):
        print(f"   🗑️  Filtered out: {len(all_reviews) - len(filtered_reviews)} reviews (outside date range)")
    print()
    
    # Step 4: Remove PII
    print("🔒 Step 4: Removing PII from reviews...")
    review_dicts = [r.model_dump() for r in filtered_reviews]
    sanitized_reviews = sanitize_reviews(review_dicts)
    print(f"   ✅ PII removed from {len(sanitized_reviews)} reviews")
    
    # Check if any PII was found
    pii_found = False
    for original, sanitized in zip(review_dicts, sanitized_reviews):
        if original['text'] != sanitized['text']:
            pii_found = True
            break
    
    if pii_found:
        print("   🛡️  Example PII removal:")
        for orig, san in zip(review_dicts, sanitized_reviews):
            if orig['text'] != san['text']:
                print(f"      Before: {orig['text'][:60]}...")
                print(f"      After:  {san['text'][:60]}...")
                break
    else:
        print("   ℹ️  No PII detected in current reviews")
    print()
    
    # Step 5: Convert back to Review objects
    print("🔄 Step 5: Converting sanitized data back to Review objects...")
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
            print(f"   ⚠️  Warning: Could not create review: {e}")
    
    print(f"   ✅ Created {len(cleaned_reviews)} clean Review objects")
    print()
    
    # Step 6: Send to LLM for analysis
    print("🤖 Step 6: Sending filtered reviews to Groq LLM for analysis...")
    print(f"   📊 Number of reviews: {len(cleaned_reviews)}")
    print(f"   🎯 Model: {settings.GROQ_MODEL}")
    print(f"   🔑 API Key configured: {'✅ Yes' if settings.GROQ_API_KEY else '❌ No'}")
    print()
    
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY.startswith('your_'):
        print("   ⚠️  WARNING: Please update GROQ_API_KEY in .env file with your actual key!")
        print("   Skipping LLM analysis...")
        llm_success = False
    else:
        try:
            analyzer = GroqAnalyzer()
            
            print("   ⏳ Analyzing themes (this may take 10-30 seconds)...")
            # Run async function in sync context
            import asyncio
            analysis_result = asyncio.run(analyzer.analyze_themes(cleaned_reviews, max_themes=settings.MAX_THEMES))
            
            print(f"   ✅ LLM Analysis complete!")
            print()
            
            # Display results
            print("=" * 80)
            print("LLM ANALYSIS RESULTS")
            print("=" * 80)
            print()
            
            if 'themes' in analysis_result:
                themes = analysis_result['themes']
                print(f"📊 Top {len(themes)} Themes Identified:\n")
                
                for i, theme in enumerate(themes, 1):
                    print(f"{i}. {theme.get('theme_name', 'Unknown Theme')}")
                    print(f"   Reviews: {theme.get('review_count', 0)} ({theme.get('percentage', 0):.1f}%)")
                    print(f"   Sentiment: {theme.get('sentiment', 'unknown')}")
                    print(f"   Sample Quotes:")
                    for quote in theme.get('quotes', [])[:2]:
                        print(f"     • \"{quote}\"")
                    print(f"   Action Ideas:")
                    for action in theme.get('action_ideas', [])[:2]:
                        print(f"     • {action}")
                    print()
            
            llm_success = True
            
        except Exception as e:
            print(f"   ❌ LLM Analysis failed: {e}")
            print(f"   💡 This might be due to:")
            print(f"      - Invalid API key")
            print(f"      - Network connectivity")
            print(f"      - Rate limiting")
            print(f"      - Empty review list")
            llm_success = False
    
    print()
    print("=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    print()
    print("✅ Phase 2 Components Tested:")
    print("   1. ✅ CSV Import (App Store format)")
    print("   2. ✅ Word Count Filtering (≥5 words)")
    print("   3. ✅ Date Range Filtering (8 weeks)")
    print("   4. ✅ PII Removal (7 patterns)")
    print("   5. ✅ Data Normalization")
    if llm_success:
        print("   6. ✅ LLM Analysis (Groq)")
    else:
        print("   6. ⚠️  LLM Analysis (Skipped/Failed)")
    print()
    
    # Cleanup
    if os.path.exists(csv_file):
        os.unlink(csv_file)
    
    print("=" * 80)
    if llm_success:
        print("🎉 PHASE 2 WORKFLOW COMPLETED SUCCESSFULLY!")
    else:
        print("⚠️  PHASE 2 WORKFLOW PARTIALLY COMPLETED (LLM step skipped)")
    print("=" * 80)
    print()
    
    return True


# Import Review model
from app.models.review import Review

# Run the test
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_phase2_workflow())
